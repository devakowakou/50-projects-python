"""
Calculatrice A/B Test - Application Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="📊 A/B Test Calculator",
    page_icon="📊",
    layout="wide"
)

# Imports des modules
from src.statistical_tests import ABTestCalculator, DataGenerator
from src.visualizations import ABTestVisualizer
from src.utils import DataLoader, ResultsFormatter, ExportUtils, SampleSizeHelper
from config import CONFIDENCE_LEVELS, POWER_LEVELS, EFFECT_SIZES


def main():
    """Application principale"""
    
    st.title("📊 Calculatrice de Significativité Statistique A/B Test")
    st.markdown("**Analysez vos tests A/B avec des méthodes statistiques rigoureuses**")
    
    # Sidebar - Configuration
    st.sidebar.header("⚙️ Configuration")
    
    confidence_level = st.sidebar.selectbox(
        "Niveau de confiance",
        CONFIDENCE_LEVELS,
        index=1,  # 95% par défaut
        format_func=lambda x: f"{x:.0%}"
    )
    
    # Initialisation du calculateur
    calculator = ABTestCalculator(confidence_level=confidence_level)
    
    # Onglets principaux
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧪 Test Statistique", 
        "📊 Analyse de Puissance", 
        "📈 Calculateur d'Échantillon",
        "📁 Import de Données"
    ])
    
    with tab1:
        run_statistical_test(calculator)
    
    with tab2:
        run_power_analysis(calculator)
    
    with tab3:
        run_sample_size_calculator(calculator)
    
    with tab4:
        run_data_import(calculator)


def run_statistical_test(calculator):
    """Interface pour les tests statistiques"""
    
    st.subheader("🧪 Test Statistique")
    
    test_type = st.selectbox(
        "Type de test",
        ["t-test", "z-test", "chi2-test"],
        help="Choisissez le test approprié selon vos données"
    )
    
    if test_type == "t-test":
        run_t_test(calculator)
    elif test_type == "z-test":
        run_z_test(calculator)
    elif test_type == "chi2-test":
        run_chi2_test(calculator)


def run_t_test(calculator):
    """Interface pour le t-test"""
    
    st.markdown("### T-Test : Comparaison de Moyennes")
    st.info("💡 Utilisez ce test pour comparer des métriques continues (revenus, temps, etc.)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Groupe A (Contrôle)**")
        n_a = st.number_input("Taille échantillon A", min_value=10, value=100, key="t_n_a")
        mean_a = st.number_input("Moyenne A", value=50.0, key="t_mean_a")
        std_a = st.number_input("Écart-type A", min_value=0.1, value=10.0, key="t_std_a")
    
    with col2:
        st.markdown("**Groupe B (Test)**")
        n_b = st.number_input("Taille échantillon B", min_value=10, value=100, key="t_n_b")
        mean_b = st.number_input("Moyenne B", value=55.0, key="t_mean_b")
        std_b = st.number_input("Écart-type B", min_value=0.1, value=10.0, key="t_std_b")
    
    if st.button("🔬 Lancer le T-Test", type="primary"):
        
        # Génération des données
        group_a, group_b = DataGenerator.generate_continuous_data(
            n_a, n_b, mean_a, mean_b, std_a, std_b
        )
        
        # Test statistique
        result = calculator.t_test_two_sample(group_a, group_b)
        
        # Affichage des résultats
        display_test_results(result, group_a, group_b)


def run_z_test(calculator):
    """Interface pour le z-test"""
    
    st.markdown("### Z-Test : Comparaison de Proportions")
    st.info("💡 Utilisez ce test pour comparer des taux de conversion")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Groupe A (Contrôle)**")
        n_a = st.number_input("Visiteurs A", min_value=10, value=1000, key="z_n_a")
        conv_a = st.number_input("Conversions A", min_value=0, max_value=n_a, value=50, key="z_conv_a")
        st.metric("Taux A", f"{conv_a/n_a:.1%}")
    
    with col2:
        st.markdown("**Groupe B (Test)**")
        n_b = st.number_input("Visiteurs B", min_value=10, value=1000, key="z_n_b")
        conv_b = st.number_input("Conversions B", min_value=0, max_value=n_b, value=65, key="z_conv_b")
        st.metric("Taux B", f"{conv_b/n_b:.1%}")
    
    if st.button("🔬 Lancer le Z-Test", type="primary"):
        
        # Test statistique
        result = calculator.z_test_proportions(conv_a, n_a, conv_b, n_b)
        
        # Affichage des résultats
        display_proportion_results(result)


def run_chi2_test(calculator):
    """Interface pour le test chi-carré"""
    
    st.markdown("### Test Chi-carré : Test d'Indépendance")
    st.info("💡 Utilisez ce test pour analyser des variables catégorielles")
    
    # Interface simplifiée pour tableau de contingence 2x2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Groupe A**")
        a_success = st.number_input("Succès A", min_value=0, value=45, key="chi2_a_s")
        a_failure = st.number_input("Échecs A", min_value=0, value=55, key="chi2_a_f")
    
    with col2:
        st.markdown("**Groupe B**")
        b_success = st.number_input("Succès B", min_value=0, value=60, key="chi2_b_s")
        b_failure = st.number_input("Échecs B", min_value=0, value=40, key="chi2_b_f")
    
    # Tableau de contingence
    contingency_table = np.array([[a_success, a_failure], [b_success, b_failure]])
    
    st.markdown("**Tableau de contingence**")
    df_table = pd.DataFrame(
        contingency_table,
        columns=['Succès', 'Échecs'],
        index=['Groupe A', 'Groupe B']
    )
    st.dataframe(df_table)
    
    if st.button("🔬 Lancer le Test Chi-carré", type="primary"):
        
        # Test statistique
        result = calculator.chi2_test(contingency_table)
        
        # Affichage des résultats
        display_chi2_results(result)


def display_test_results(result, group_a=None, group_b=None):
    """Affiche les résultats d'un test statistique"""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Résultats")
        
        # Métriques principales
        formatted_results = ResultsFormatter.format_test_results(result)
        for key, value in formatted_results.items():
            st.metric(key, value)
    
    with col2:
        st.markdown("### 🎯 Interprétation")
        interpretation = ResultsFormatter.interpret_results(result)
        st.markdown(interpretation)
    
    # Visualisations
    if group_a is not None and group_b is not None:
        st.markdown("### 📈 Visualisations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_dist = ABTestVisualizer.plot_distributions(group_a, group_b, result)
            st.plotly_chart(fig_dist, use_container_width=True)
        
        with col2:
            fig_ci = ABTestVisualizer.plot_confidence_interval(result)
            st.plotly_chart(fig_ci, use_container_width=True)
    
    # Export
    add_export_section(result, interpretation)


def display_proportion_results(result):
    """Affiche les résultats d'un test de proportions"""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Résultats")
        formatted_results = ResultsFormatter.format_test_results(result)
        for key, value in formatted_results.items():
            st.metric(key, value)
    
    with col2:
        st.markdown("### 🎯 Interprétation")
        interpretation = ResultsFormatter.interpret_results(result)
        st.markdown(interpretation)
    
    # Visualisations
    st.markdown("### 📈 Visualisations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_prop = ABTestVisualizer.plot_proportions_comparison(result)
        st.plotly_chart(fig_prop, use_container_width=True)
    
    with col2:
        fig_ci = ABTestVisualizer.plot_confidence_interval(result)
        st.plotly_chart(fig_ci, use_container_width=True)
    
    add_export_section(result, interpretation)


def display_chi2_results(result):
    """Affiche les résultats d'un test chi-carré"""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Résultats")
        formatted_results = ResultsFormatter.format_test_results(result)
        for key, value in formatted_results.items():
            st.metric(key, value)
    
    with col2:
        st.markdown("### 🎯 Interprétation")
        interpretation = ResultsFormatter.interpret_results(result)
        st.markdown(interpretation)
    
    add_export_section(result, interpretation)


def run_power_analysis(calculator):
    """Interface pour l'analyse de puissance"""
    
    st.subheader("📊 Analyse de Puissance Statistique")
    st.info("💡 Analysez la puissance de votre test selon différents paramètres")
    
    col1, col2 = st.columns(2)
    
    with col1:
        effect_size = st.slider("Taille d'effet", 0.1, 2.0, 0.5, 0.1)
        sample_size = st.slider("Taille d'échantillon (par groupe)", 10, 1000, 100, 10)
    
    with col2:
        power = calculator.calculate_power(effect_size, sample_size)
        st.metric("Puissance calculée", f"{power:.1%}")
        
        if power < 0.8:
            st.warning("⚠️ Puissance insuffisante (< 80%)")
        else:
            st.success("✅ Puissance suffisante (≥ 80%)")
    
    # Graphique d'analyse de puissance
    st.markdown("### 📈 Analyse Interactive")
    
    effect_sizes = np.linspace(0.1, 1.5, 20)
    sample_sizes = np.linspace(20, 500, 20)
    
    powers = np.zeros((len(sample_sizes), len(effect_sizes)))
    for i, ss in enumerate(sample_sizes):
        for j, es in enumerate(effect_sizes):
            powers[i, j] = calculator.calculate_power(es, int(ss))
    
    fig_power = ABTestVisualizer.plot_power_analysis(effect_sizes, sample_sizes, powers)
    st.plotly_chart(fig_power, use_container_width=True)


def run_sample_size_calculator(calculator):
    """Interface pour le calculateur de taille d'échantillon"""
    
    st.subheader("📈 Calculateur de Taille d'Échantillon")
    st.info("💡 Déterminez la taille d'échantillon nécessaire pour votre test")
    
    col1, col2 = st.columns(2)
    
    with col1:
        effect_size = st.selectbox(
            "Taille d'effet attendue",
            list(EFFECT_SIZES.keys()),
            format_func=lambda x: f"{x.title()} ({EFFECT_SIZES[x]})"
        )
        effect_value = EFFECT_SIZES[effect_size]
        
        power = st.selectbox(
            "Puissance souhaitée",
            POWER_LEVELS,
            index=0,  # 80% par défaut
            format_func=lambda x: f"{x:.0%}"
        )
    
    with col2:
        sample_size = calculator.calculate_sample_size(effect_value, power)
        st.metric("Taille d'échantillon requise", f"{sample_size:,} par groupe")
        st.metric("Total participants", f"{sample_size * 2:,}")
    
    # Estimation de durée
    st.markdown("### ⏱️ Estimation de Durée")
    
    daily_visitors = st.number_input(
        "Visiteurs quotidiens",
        min_value=1,
        value=1000,
        help="Nombre de visiteurs par jour sur votre site"
    )
    
    allocation_ratio = st.slider(
        "% alloué au test A/B",
        0.1, 1.0, 0.5, 0.1,
        format="%.0%%",
        help="Pourcentage du trafic alloué au test"
    )
    
    duration = SampleSizeHelper.estimate_test_duration(
        sample_size, daily_visitors, allocation_ratio
    )
    
    if "error" not in duration:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Durée estimée", f"{duration['days']} jours")
        with col2:
            st.metric("En semaines", f"{duration['weeks']} semaines")
        with col3:
            st.metric("Échantillon/jour", f"{duration['daily_sample_rate']}")
    
    # Graphique taille d'échantillon vs puissance
    power_levels = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    sample_sizes = [calculator.calculate_sample_size(effect_value, p) for p in power_levels]
    
    fig_sample = ABTestVisualizer.plot_sample_size_calculator(effect_value, power_levels, sample_sizes)
    st.plotly_chart(fig_sample, use_container_width=True)


def run_data_import(calculator):
    """Interface pour l'import de données"""
    
    st.subheader("📁 Import de Données")
    st.info("💡 Importez vos propres données pour analyse")
    
    uploaded_file = st.file_uploader(
        "Choisissez un fichier CSV",
        type=['csv'],
        help="Le fichier doit contenir au minimum une colonne groupe et une colonne métrique"
    )
    
    if uploaded_file is not None:
        df = DataLoader.load_csv_data(uploaded_file)
        
        if not df.empty:
            st.markdown("### 👀 Aperçu des Données")
            st.dataframe(df.head())
            
            # Configuration des colonnes
            col1, col2 = st.columns(2)
            
            with col1:
                group_col = st.selectbox("Colonne groupe", df.columns)
            
            with col2:
                metric_col = st.selectbox("Colonne métrique", df.columns)
            
            if DataLoader.validate_ab_data(df, group_col, metric_col):
                
                # Analyse des données
                groups = df[group_col].unique()
                group_a_data = df[df[group_col] == groups[0]][metric_col].values
                group_b_data = df[df[group_col] == groups[1]][metric_col].values
                
                st.markdown("### 📊 Statistiques Descriptives")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**{groups[0]}**")
                    st.metric("Taille", len(group_a_data))
                    st.metric("Moyenne", f"{np.mean(group_a_data):.2f}")
                    st.metric("Écart-type", f"{np.std(group_a_data):.2f}")
                
                with col2:
                    st.markdown(f"**{groups[1]}**")
                    st.metric("Taille", len(group_b_data))
                    st.metric("Moyenne", f"{np.mean(group_b_data):.2f}")
                    st.metric("Écart-type", f"{np.std(group_b_data):.2f}")
                
                if st.button("🔬 Analyser les Données", type="primary"):
                    
                    # Test automatique selon le type de données
                    if df[metric_col].dtype in ['int64', 'float64']:
                        result = calculator.t_test_two_sample(group_a_data, group_b_data)
                        display_test_results(result, group_a_data, group_b_data)
                    else:
                        st.error("Type de données non supporté pour l'analyse automatique")


def add_export_section(result, interpretation):
    """Ajoute une section d'export des résultats"""
    
    st.markdown("### 📥 Export des Résultats")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export JSON
        json_data = ExportUtils.export_results_json(result)
        st.download_button(
            label="📋 Télécharger JSON",
            data=json_data,
            file_name=f"ab_test_results_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )
    
    with col2:
        # Export rapport
        report = ExportUtils.create_report(result, interpretation)
        st.download_button(
            label="📄 Télécharger Rapport",
            data=report,
            file_name=f"ab_test_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown"
        )


if __name__ == "__main__":
    main()