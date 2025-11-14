#!/usr/bin/env python3
"""
Scraper Immobilier - Application Streamlit
Analyse des prix immobiliers par quartier
"""

import streamlit as st
import pandas as pd
from src.scraper import RealEstateScraper, DatabaseManager
from src.analyzer import PriceAnalyzer, TrendAnalyzer
from src.visualizations import RealEstateVisualizer
from config import CITIES, PROPERTY_TYPES

# Configuration page
st.set_page_config(
    page_title="Scraper Immobilier",
    page_icon="🏠",
    layout="wide"
)

def main():
    st.title("🏠 Scraper Immobilier - Analyse par Quartier")
    st.markdown("**Analyse des prix immobiliers et détection des bonnes affaires**")
    
    # Sidebar
    st.sidebar.header("⚙️ Configuration")
    
    # Initialisation
    scraper = RealEstateScraper()
    db_manager = DatabaseManager()
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Scraping", 
        "📊 Analyse Globale", 
        "🏘️ Analyse par Quartier",
        "💎 Bonnes Affaires"
    ])
    
    with tab1:
        scraping_tab(scraper, db_manager)
    
    with tab2:
        global_analysis_tab(db_manager)
    
    with tab3:
        quartier_analysis_tab(db_manager)
    
    with tab4:
        deals_analysis_tab(db_manager)

def scraping_tab(scraper, db_manager):
    """Onglet scraping"""
    st.header("🔍 Collecte de Données")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Paramètres")
        city = st.selectbox("Ville", list(CITIES.keys()), format_func=lambda x: CITIES[x]['name'])
        property_type = st.selectbox("Type de bien", list(PROPERTY_TYPES.keys()), format_func=lambda x: PROPERTY_TYPES[x])
        max_results = st.number_input("Nombre max de résultats", min_value=10, max_value=500, value=100)
    
    with col2:
        st.subheader("🎯 Actions")
        
        if st.button("🎲 Générer Données d'Exemple", type="primary"):
            with st.spinner("Génération des données..."):
                properties = scraper.scrape_sample_data()
                db_manager.save_properties(properties)
                st.success(f"✅ {len(properties)} biens générés et sauvegardés")
        
        if st.button("🗑️ Vider la Base"):
            db_manager.init_database()  # Recrée la table vide
            st.success("✅ Base de données vidée")
    
    # Aperçu des données
    df = db_manager.load_properties()
    if not df.empty:
        st.subheader("📋 Données Collectées")
        st.dataframe(df.head(10))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Biens", len(df))
        with col2:
            st.metric("Prix Moyen", f"{df['price'].mean():,.0f} €")
        with col3:
            st.metric("Prix/m² Moyen", f"{df['price_per_m2'].mean():,.0f} €")

def global_analysis_tab(db_manager):
    """Onglet analyse globale"""
    st.header("📊 Analyse Globale du Marché")
    
    df = db_manager.load_properties()
    
    if df.empty:
        st.warning("⚠️ Aucune donnée disponible. Utilisez l'onglet Scraping pour collecter des données.")
        return
    
    analyzer = PriceAnalyzer(df)
    stats = analyzer.get_price_statistics()
    
    # Métriques principales
    st.subheader("📈 Métriques Clés")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Biens", f"{stats['total_properties']:,}")
    with col2:
        st.metric("Prix Moyen", f"{stats['avg_price']:,.0f} €")
    with col3:
        st.metric("Prix/m² Moyen", f"{stats['avg_price_per_m2']:,.0f} €")
    with col4:
        st.metric("Surface Moyenne", f"{stats['avg_surface']:.0f} m²")
    
    # Visualisations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribution des Prix")
        fig_dist = RealEstateVisualizer.plot_price_distribution(df)
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        st.subheader("🔗 Surface vs Prix")
        fig_scatter = RealEstateVisualizer.plot_surface_vs_price(df)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Analyse de distribution
    st.subheader("📈 Analyse Statistique")
    dist_analysis = analyzer.price_distribution_analysis()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Outliers", f"{dist_analysis['outliers_count']} ({dist_analysis['outliers_percentage']:.1f}%)")
    with col2:
        st.metric("Asymétrie", f"{dist_analysis['skewness']:.2f}")
    with col3:
        st.metric("Kurtosis", f"{dist_analysis['kurtosis']:.2f}")

def quartier_analysis_tab(db_manager):
    """Onglet analyse par quartier"""
    st.header("🏘️ Analyse par Quartier")
    
    df = db_manager.load_properties()
    
    if df.empty:
        st.warning("⚠️ Aucune donnée disponible.")
        return
    
    analyzer = PriceAnalyzer(df)
    quartier_stats = analyzer.analyze_by_quartier()
    
    # Tableau des statistiques
    st.subheader("📋 Statistiques par Quartier")
    st.dataframe(quartier_stats, use_container_width=True)
    
    # Visualisations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Prix/m² par Quartier")
        fig_bar = RealEstateVisualizer.plot_price_by_quartier(quartier_stats)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("📈 Comparaison Quartiers")
        fig_comp = RealEstateVisualizer.plot_quartier_comparison(quartier_stats)
        st.plotly_chart(fig_comp, use_container_width=True)
    
    # Distribution par quartier
    st.subheader("📦 Distribution des Prix par Quartier")
    fig_box = RealEstateVisualizer.plot_price_range_by_quartier(df)
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Comparaison de quartiers
    st.subheader("⚖️ Comparaison de Quartiers")
    col1, col2 = st.columns(2)
    
    quartiers = df['quartier'].unique()
    with col1:
        quartier1 = st.selectbox("Quartier 1", quartiers)
    with col2:
        quartier2 = st.selectbox("Quartier 2", quartiers, index=1 if len(quartiers) > 1 else 0)
    
    if st.button("🔍 Comparer"):
        comparison = analyzer.compare_quartiers(quartier1, quartier2)
        
        if comparison:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Différence Prix/m²", f"{comparison['mean_diff']:+.0f} €")
            with col2:
                st.metric("Différence %", f"{comparison['mean_diff_pct']:+.1f}%")
            with col3:
                significance = "✅ Significative" if comparison['significant'] else "❌ Non significative"
                st.metric("Différence", significance)

def deals_analysis_tab(db_manager):
    """Onglet bonnes affaires"""
    st.header("💎 Détection des Bonnes Affaires")
    
    df = db_manager.load_properties()
    
    if df.empty:
        st.warning("⚠️ Aucune donnée disponible.")
        return
    
    analyzer = PriceAnalyzer(df)
    
    # Paramètres
    col1, col2 = st.columns(2)
    with col1:
        top_n = st.number_input("Nombre de bonnes affaires", min_value=5, max_value=50, value=10)
    with col2:
        quartier_filter = st.selectbox("Filtrer par quartier", ["Tous"] + list(df['quartier'].unique()))
    
    # Filtrage
    filtered_df = df if quartier_filter == "Tous" else df[df['quartier'] == quartier_filter]
    filtered_analyzer = PriceAnalyzer(filtered_df)
    
    # Meilleures affaires
    best_deals = filtered_analyzer.find_best_deals(top_n)
    
    if not best_deals.empty:
        st.subheader("🏆 Top des Bonnes Affaires")
        
        # Formatage pour affichage
        display_deals = best_deals.copy()
        display_deals['price'] = display_deals['price'].apply(lambda x: f"{x:,.0f} €")
        display_deals['price_per_m2'] = display_deals['price_per_m2'].apply(lambda x: f"{x:,.0f} €/m²")
        display_deals['deal_score'] = display_deals['deal_score'].apply(lambda x: f"{x:+.1f}%")
        
        st.dataframe(display_deals, use_container_width=True)
        
        # Métriques des bonnes affaires
        st.subheader("📊 Analyse des Bonnes Affaires")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_saving = best_deals['deal_score'].mean()
            st.metric("Économie Moyenne", f"{avg_saving:+.1f}%")
        
        with col2:
            best_quartier = best_deals['quartier'].mode().iloc[0] if not best_deals.empty else "N/A"
            st.metric("Meilleur Quartier", best_quartier)
        
        with col3:
            avg_surface = best_deals['surface'].mean()
            st.metric("Surface Moyenne", f"{avg_surface:.0f} m²")
    
    else:
        st.info("ℹ️ Aucune bonne affaire détectée avec les critères actuels.")

if __name__ == "__main__":
    main()