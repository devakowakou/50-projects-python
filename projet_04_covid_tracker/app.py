"""
COVID-19 Global Tracker - Application Streamlit
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.append(str(Path(__file__).parent))

import config
from src.data_loader import CovidDataLoader
from src.analyzer import CovidAnalyzer
from src.visualizer import CovidVisualizer


# Configuration de la page
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)


# Initialiser les gestionnaires (avec cache)
@st.cache_resource
def init_managers():
    """Initialise les gestionnaires (cached)"""
    loader = CovidDataLoader()
    analyzer = CovidAnalyzer()
    visualizer = CovidVisualizer()
    return loader, analyzer, visualizer


@st.cache_data(ttl=3600)  # Cache 1h
def load_covid_data(force_refresh=False):
    """Charge les données COVID avec cache"""
    loader, _, _ = init_managers()
    return loader.load_data(force_refresh=force_refresh)


loader, analyzer, visualizer = init_managers()


def show_header():
    """Affiche l'en-tête de l'application"""
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem; color: white; text-align: center;">
            <h1>🦠 {config.APP_TITLE}</h1>
            <p>Données mondiales sur la pandémie COVID-19</p>
        </div>
    """, unsafe_allow_html=True)


def show_metrics(metrics):
    """Affiche les métriques principales"""
    if not metrics:
        st.warning("Pas de données disponibles pour ce pays")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Cas totaux",
            f"{metrics['total_cases']:,.0f}",
            f"{metrics['cases_per_million']:.0f} /million"
        )
    
    with col2:
        st.metric(
            "Décès totaux",
            f"{metrics['total_deaths']:,.0f}",
            f"{metrics['mortality_rate']:.2f}% taux"
        )
    
    with col3:
        st.metric(
            "Vaccinations",
            f"{metrics['total_vaccinations']:,.0f}",
            f"{metrics['vaccination_rate']:.1f}% population"
        )
    
    with col4:
        alert_level, alert_color = analyzer.get_alert_level(metrics['cases_per_million'])
        st.metric(
            "Niveau d'alerte",
            alert_level,
            f"{metrics['cases_per_million']:.0f} cas/M"
        )
        st.markdown(f"<div style='background-color: {alert_color}; height: 5px; border-radius: 3px; margin-top: -10px;'></div>", 
                   unsafe_allow_html=True)


def main():
    """Fonction principale"""
    show_header()
    
    # Sidebar
    st.sidebar.title("Configuration")
    
    # Charger les données
    try:
        with st.spinner("Chargement des données..."):
            force_refresh = st.sidebar.button("🔄 Rafraîchir les données")
            df = load_covid_data(force_refresh=force_refresh)
        
        st.sidebar.success(f"✅ Données chargées : {len(df):,} enregistrements")
        
        # Dernière mise à jour
        last_date = df['date'].max()
        st.sidebar.info(f"📅 Dernière mise à jour : {last_date.strftime('%Y-%m-%d')}")
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données : {e}")
        return
    
    # Sélection du pays
    countries = loader.get_available_countries(df)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Sélection du pays")
    
    selected_country = st.sidebar.selectbox(
        "Pays principal",
        countries,
        index=countries.index('France') if 'France' in countries else 0
    )
    
    # Sélection de la période
    st.sidebar.markdown("---")
    st.sidebar.subheader("Période d'analyse")
    
    preset_period = st.sidebar.selectbox(
        "Période prédéfinie",
        list(config.PRESET_PERIODS.keys())
    )
    
    # Calculer les dates
    end_date = df['date'].max()
    if config.PRESET_PERIODS[preset_period]:
        start_date = end_date - timedelta(days=config.PRESET_PERIODS[preset_period])
    else:
        start_date = df['date'].min()
    
    # Filtrer les données
    country_df = loader.get_country_data(df, selected_country)
    country_df = analyzer.filter_by_date_range(country_df, start_date, end_date)
    country_df = analyzer.calculate_daily_changes(country_df)
    
    # Métriques principales
    st.markdown(f"## 📊 Vue d'ensemble - {selected_country}")
    metrics = analyzer.calculate_metrics(country_df)
    if metrics is None:
        st.warning("Pas de données disponibles pour ce pays")
        st.stop()
    show_metrics(metrics)
    
    st.markdown("---")
    
    # Graphiques
    tab1, tab2, tab3 = st.tabs(["📈 Évolution", "🌍 Comparaison", "💉 Vaccination"])
    
    with tab1:
        st.markdown("### Évolution temporelle")
        
        col1, col2 = st.columns(2)
        
        with col1:
            metric_choice = st.selectbox(
                "Choisir la métrique",
                ['new_cases', 'new_deaths', 'total_cases', 'total_deaths'],
                format_func=lambda x: {
                    'new_cases': 'Nouveaux cas',
                    'new_deaths': 'Nouveaux décès',
                    'total_cases': 'Cas cumulés',
                    'total_deaths': 'Décès cumulés'
                }[x]
            )
        
        fig = visualizer.create_timeline_chart(country_df, selected_country, metric_choice)
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistiques sur la période
        st.markdown("### 📋 Statistiques de la période")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total cas (période)",
                f"{country_df['new_cases'].sum():,.0f}"
            )
        
        with col2:
            st.metric(
                "Total décès (période)",
                f"{country_df['new_deaths'].sum():,.0f}"
            )
        
        with col3:
            peak_info = analyzer.get_peak_info(country_df)
            if peak_info:
                st.metric(
                    "Pic de cas",
                    f"{peak_info['peak_cases_value']:,.0f}",
                    f"Le {peak_info['peak_cases_date']}"
                )
    
    with tab2:
        st.markdown("### Comparaison entre pays")
        
        # Sélection des pays à comparer
        compare_countries = st.multiselect(
            "Sélectionnez les pays à comparer",
            countries,
            default=[selected_country] + [c for c in config.DEFAULT_COUNTRIES if c in countries and c != selected_country][:3],
            max_selections=config.MAX_COUNTRIES_COMPARISON
        )
        
        if len(compare_countries) < 2:
            st.warning("Sélectionnez au moins 2 pays pour la comparaison")
        else:
            # Graphique de comparaison temporelle
            compare_df = df[df['location'].isin(compare_countries)]
            compare_df = analyzer.filter_by_date_range(compare_df, start_date, end_date)
            
            metric_compare = st.selectbox(
                "Métrique à comparer",
                ['total_cases', 'total_deaths', 'new_cases', 'total_vaccinations'],
                format_func=lambda x: {
                    'total_cases': 'Cas totaux',
                    'total_deaths': 'Décès totaux',
                    'new_cases': 'Nouveaux cas',
                    'total_vaccinations': 'Vaccinations'
                }[x]
            )
            
            fig_compare = visualizer.create_comparison_chart(compare_df, compare_countries, metric_compare)
            st.plotly_chart(fig_compare, use_container_width=True)
            
            # Tableau de comparaison
            st.markdown("### 📊 Tableau comparatif")
            comparison_table = analyzer.compare_countries(df, compare_countries)
            st.dataframe(comparison_table, use_container_width=True)
            
            # Graphique en barres
            bar_metric = st.selectbox(
                "Métrique pour graphique en barres",
                comparison_table.columns[1:],  # Exclure la colonne "Pays"
                key="bar_metric"
            )
            
            fig_bar = visualizer.create_bar_chart(comparison_table, bar_metric)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab3:
        st.markdown(f"### État de la vaccination - {selected_country}")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_pie = visualizer.create_pie_chart(metrics)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            if metrics:
                st.markdown("#### Détails")
                st.metric("Population totale", f"{metrics['population']:,.0f}")
                st.metric("Personnes vaccinées", f"{metrics['people_vaccinated']:,.0f}")
                st.metric("Complètement vaccinés", f"{metrics['people_fully_vaccinated']:,.0f}")
                st.metric("Taux de vaccination", f"{metrics['vaccination_rate']:.1f}%")
            else:
                st.warning("Pas de données de vaccination disponibles pour ce pays")    
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>Données fournies par <a href='https://github.com/owid/covid-19-data' target='_blank'>Our World in Data</a></p>
            <p>Projet 4/50 du Challenge Python | Dernière mise à jour : {}</p>
        </div>
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M')), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
