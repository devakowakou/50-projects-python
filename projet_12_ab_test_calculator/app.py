#!/usr/bin/env python3
"""
Calculateur de Tests A/B - Application Streamlit
Analyse statistique complète pour tests A/B
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.statistical_tests import ABTestCalculator, DataGenerator
from src.utils import DataLoader, ResultsFormatter, ExportUtils
from src.visualizations import ABTestVisualizer
from config import STATISTICAL_TESTS, CONFIDENCE_LEVELS, POWER_LEVELS, EFFECT_SIZES

# Configuration page
st.set_page_config(
    page_title="A/B Test Calculator",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("📊 Calculateur de Tests A/B")
    st.markdown("**Analyse statistique complète pour vos tests A/B**")
    
    # Sidebar
    st.sidebar.header("⚙️ Configuration")
    confidence_level = st.sidebar.selectbox(
        "Niveau de confiance", 
        CONFIDENCE_LEVELS, 
        index=1, 
        format_func=lambda x: f"{x:.0%}"
    )
    
    calculator = ABTestCalculator(confidence_level)
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Analyse de Données", 
        "🧮 Calculateur Manuel", 
        "📏 Taille d'Échantillon",
        "🎲 Générateur de Données"
    ])
    
    with tab1:
        analyze_data_tab(calculator)
    
    with tab2:
        manual_calculator_tab(calculator)
    
    with tab3:
        sample_size_tab(calculator)
    
    with tab4:
        data_generator_tab(calculator)

def analyze_data_tab(calculator):
    """Onglet analyse de données"""
    st.header("📈 Analyse de Données CSV")
    
    uploaded_file = st.file_uploader("Chargez vos données", type=['csv'])
    
    if uploaded_file:
        df = DataLoader.load_csv_data(uploaded_file)
        
        if not df.empty:
            st.subheader("📋 Aperçu des données")
            st.dataframe(df.head())
            
            col1, col2 = st.columns(2)
            with col1:
                group_col = st.selectbox("Colonne groupe", df.columns)
            with col2:
                metric_col = st.selectbox("Colonne métrique", df.select_dtypes(include=[np.number]).columns)
            
            if DataLoader.validate_ab_data(df, group_col, metric_col):
                groups = df[group_col].unique()
                group_a_data = df[df[group_col] == groups[0]][metric_col].values
                group_b_data = df[df[group_col] == groups[1]][metric_col].values
                
                # Test statistique
                test_result = calculator.t_test_two_sample(group_a_data, group_b_data)
                
                # Résultats
                display_test_results(test_result)
                
                # Visualisations
                st.subheader("📊 Visualisations")
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_dist = ABTestVisualizer.plot_distributions(group_a_data, group_b_data, test_result)
                    st.plotly_chart(fig_dist, use_container_width=True)
                
                with col2:
                    fig_ci = ABTestVisualizer.plot_confidence_interval(test_result)
                    st.plotly_chart(fig_ci, use_container_width=True)
                
                # Export
                export_results(test_result)
            else:
                st.error("❌ Données invalides. Vérifiez les colonnes.")

def manual_calculator_tab(calculator):
    """Onglet calculateur manuel"""
    st.header("🧮 Calculateur Manuel")
    
    test_type = st.radio("Type de test", ["Moyennes (T-Test)", "Proportions (Z-Test)"])
    
    if test_type == "Moyennes (T-Test)":
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Groupe A")
            n_a = st.number_input("Taille échantillon A", min_value=1, value=100)
            mean_a = st.number_input("Moyenne A", value=10.0)
            std_a = st.number_input("Écart-type A", min_value=0.1, value=2.0)
        
        with col2:
            st.subheader("Groupe B")
            n_b = st.number_input("Taille échantillon B", min_value=1, value=100)
            mean_b = st.number_input("Moyenne B", value=12.0)
            std_b = st.number_input("Écart-type B", min_value=0.1, value=2.0)
        
        if st.button("🔬 Calculer T-Test"):
            # Génération données simulées
            group_a, group_b = DataGenerator.generate_continuous_data(n_a, n_b, mean_a, mean_b, std_a, std_b)
            test_result = calculator.t_test_two_sample(group_a, group_b)
            
            display_test_results(test_result)
            
            # Visualisation
            fig_dist = ABTestVisualizer.plot_distributions(group_a, group_b, test_result)
            st.plotly_chart(fig_dist, use_container_width=True)
    
    else:  # Proportions
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Groupe A")
            n_a = st.number_input("Visiteurs A", min_value=1, value=1000)
            conv_a = st.number_input("Conversions A", min_value=0, max_value=n_a, value=50)
        
        with col2:
            st.subheader("Groupe B")
            n_b = st.number_input("Visiteurs B", min_value=1, value=1000)
            conv_b = st.number_input("Conversions B", min_value=0, max_value=n_b, value=65)
        
        if st.button("🔬 Calculer Z-Test"):
            test_result = calculator.z_test_proportions(conv_a, n_a, conv_b, n_b)
            
            display_test_results(test_result)
            
            # Visualisation proportions
            fig_prop = ABTestVisualizer.plot_proportions_comparison(test_result)
            st.plotly_chart(fig_prop, use_container_width=True)

def sample_size_tab(calculator):
    """Onglet calcul taille d'échantillon"""
    st.header("📏 Calculateur de Taille d'Échantillon")
    
    col1, col2 = st.columns(2)
    
    with col1:
        effect_size_type = st.selectbox("Taille d'effet", list(EFFECT_SIZES.keys()))
        effect_size = st.number_input("Ou valeur personnalisée", 
                                    value=EFFECT_SIZES[effect_size_type], 
                                    min_value=0.01, max_value=2.0, step=0.01)
    
    with col2:
        power = st.selectbox("Puissance statistique", POWER_LEVELS, index=0, format_func=lambda x: f"{x:.0%}")
    
    if st.button("📊 Calculer Taille d'Échantillon"):
        sample_size = calculator.calculate_sample_size(effect_size, power)
        
        st.success(f"**Taille d'échantillon recommandée**: {sample_size:,} par groupe")
        st.info(f"**Total participants**: {sample_size * 2:,}")
        
        # Analyse de puissance
        st.subheader("📈 Analyse de Puissance")
        sample_sizes = np.arange(10, sample_size * 2, max(1, sample_size // 20))
        powers = [calculator.calculate_power(effect_size, n) for n in sample_sizes]
        
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sample_sizes, y=powers, mode='lines+markers'))
        fig.add_hline(y=power, line_dash="dash", annotation_text=f"Puissance cible: {power:.0%}")
        fig.update_layout(title="Courbe de Puissance", xaxis_title="Taille échantillon", yaxis_title="Puissance")
        st.plotly_chart(fig, use_container_width=True)

def data_generator_tab(calculator):
    """Onglet générateur de données"""
    st.header("🎲 Générateur de Données de Test")
    
    col1, col2 = st.columns(2)
    
    with col1:
        n_samples = st.number_input("Échantillons par groupe", min_value=10, value=500)
        mean_a = st.number_input("Moyenne groupe A", value=100.0)
        mean_b = st.number_input("Moyenne groupe B", value=105.0)
    
    with col2:
        std_dev = st.number_input("Écart-type", min_value=0.1, value=15.0)
        noise_level = st.slider("Niveau de bruit", 0.0, 1.0, 0.1)
    
    if st.button("🎲 Générer Données"):
        # Génération avec bruit
        group_a, group_b = DataGenerator.generate_continuous_data(
            n_samples, n_samples, mean_a, mean_b, std_dev, std_dev
        )
        
        # Ajout de bruit
        if noise_level > 0:
            group_a += np.random.normal(0, noise_level * std_dev, len(group_a))
            group_b += np.random.normal(0, noise_level * std_dev, len(group_b))
        
        # Création DataFrame
        df_generated = pd.DataFrame({
            'group': ['A'] * len(group_a) + ['B'] * len(group_b),
            'value': np.concatenate([group_a, group_b])
        })
        
        st.subheader("📋 Données Générées")
        st.dataframe(df_generated.head(10))
        
        # Test automatique
        test_result = calculator.t_test_two_sample(group_a, group_b)
        display_test_results(test_result)
        
        # Téléchargement
        csv = df_generated.to_csv(index=False)
        st.download_button("💾 Télécharger CSV", csv, "ab_test_data.csv", "text/csv")

def display_test_results(test_result):
    """Affiche les résultats du test"""
    st.subheader("🔬 Résultats du Test")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("P-value", f"{test_result['p_value']:.6f}")
    with col2:
        st.metric("Statistique", f"{test_result['statistic']:.4f}")
    with col3:
        st.metric("Taille d'effet", f"{test_result['effect_size']:.4f}")
    with col4:
        color = "normal" if test_result['significant'] else "inverse"
        st.metric("Significatif", "✅ Oui" if test_result['significant'] else "❌ Non")
    
    # Tableau détaillé
    formatted_results = ResultsFormatter.format_test_results(test_result)
    st.table(pd.DataFrame([formatted_results]).T.rename(columns={0: "Valeur"}))
    
    # Interprétation
    interpretation = ResultsFormatter.interpret_results(test_result)
    st.markdown(f"### 💡 Interprétation\n{interpretation}")

def export_results(test_result):
    """Section export des résultats"""
    st.subheader("💾 Export des Résultats")
    
    col1, col2 = st.columns(2)
    
    with col1:
        json_data = ExportUtils.export_results_json(test_result)
        st.download_button("📄 Export JSON", json_data, "ab_test_results.json", "application/json")
    
    with col2:
        interpretation = ResultsFormatter.interpret_results(test_result)
        report = ExportUtils.create_report(test_result, interpretation)
        st.download_button("📋 Rapport Markdown", report, "ab_test_report.md", "text/markdown")

if __name__ == "__main__":
    main()