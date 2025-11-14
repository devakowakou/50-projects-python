#!/usr/bin/env python3
"""
A/B Test Calculator - Streamlit application

This file merges previous variants and provides a unified, conflict-free
Streamlit UI for running t-tests, z-tests, chi2 tests, power and sample size
calculations, data import/analysis, data generation and result export.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Project modules
from src.statistical_tests import ABTestCalculator, DataGenerator
from src.visualizations import ABTestVisualizer
from src.utils import DataLoader, ResultsFormatter, ExportUtils, SampleSizeHelper
from config import CONFIDENCE_LEVELS, POWER_LEVELS, EFFECT_SIZES


st.set_page_config(
    page_title="📊 A/B Test Calculator",
    page_icon="📊",
    layout="wide",
)


def main():
    st.title("📊 Calculatrice A/B Test")
    st.markdown("**Analysez vos tests A/B avec des méthodes statistiques rigoureuses.**")
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    confidence_level = st.sidebar.selectbox(
        "Niveau de confiance",
        CONFIDENCE_LEVELS,
        index=1,
        format_func=lambda x: f"{x:.0%}",
    )

    calculator = ABTestCalculator(confidence_level=confidence_level)

    # Consolidated tabs
    tab_test, tab_analysis, tab_sample, tab_generator, tab_power, tab_import = st.tabs([
        "🧪 Test Statistique",
        "📈 Analyse de Données",
        "📏 Taille d'Échantillon",
        "🎲 Générateur de Données",
        "📊 Analyse de Puissance",
        "📁 Import de Données",
    ])

    with tab_test:
        run_statistical_test(calculator)

    with tab_analysis:
        analyze_data_tab(calculator)

    with tab_sample:
        run_sample_size_calculator(calculator)

    with tab_generator:
        data_generator_tab(calculator)

    with tab_power:
        run_power_analysis(calculator)

    with tab_import:
        run_data_import(calculator)


def run_statistical_test(calculator):
    st.header("🧪 Test Statistique")
    test_type = st.selectbox(
        "Type de test", ["t-test", "z-test", "chi2-test"], index=0
    )

    if test_type == "t-test":
        run_t_test(calculator)
    elif test_type == "z-test":
        run_z_test(calculator)
    else:
        run_chi2_test(calculator)


def run_t_test(calculator):
    st.markdown("### T-Test — Comparaison de Moyennes")
    col1, col2 = st.columns(2)
    with col1:
        n_a = st.number_input("Taille échantillon A", min_value=10, value=100, key="t_n_a")
        mean_a = st.number_input("Moyenne A", value=50.0, key="t_mean_a")
        std_a = st.number_input("Écart-type A", min_value=0.1, value=10.0, key="t_std_a")
    with col2:
        n_b = st.number_input("Taille échantillon B", min_value=10, value=100, key="t_n_b")
        mean_b = st.number_input("Moyenne B", value=55.0, key="t_mean_b")
        std_b = st.number_input("Écart-type B", min_value=0.1, value=10.0, key="t_std_b")

    if st.button("🔬 Lancer le T-Test"):
        group_a, group_b = DataGenerator.generate_continuous_data(
            n_a, n_b, mean_a, mean_b, std_a, std_b
        )
        result = calculator.t_test_two_sample(group_a, group_b)
        display_test_results(result, group_a, group_b)


def run_z_test(calculator):
    st.markdown("### Z-Test — Comparaison de Proportions")
    col1, col2 = st.columns(2)
    with col1:
        n_a = st.number_input("Visiteurs A", min_value=10, value=1000, key="z_n_a")
        conv_a = st.number_input("Conversions A", min_value=0, max_value=10**9, value=50, key="z_conv_a")
    with col2:
        n_b = st.number_input("Visiteurs B", min_value=10, value=1000, key="z_n_b")
        conv_b = st.number_input("Conversions B", min_value=0, max_value=10**9, value=65, key="z_conv_b")

    if st.button("🔬 Lancer le Z-Test"):
        result = calculator.z_test_proportions(conv_a, n_a, conv_b, n_b)
        display_proportion_results(result)


def run_chi2_test(calculator):
    st.markdown("### Chi² Test — Indépendance (2x2 simplifié)")
    col1, col2 = st.columns(2)
    with col1:
        a_success = st.number_input("Succès A", min_value=0, value=45, key="chi2_a_s")
        a_failure = st.number_input("Échecs A", min_value=0, value=55, key="chi2_a_f")
    with col2:
        b_success = st.number_input("Succès B", min_value=0, value=60, key="chi2_b_s")
        b_failure = st.number_input("Échecs B", min_value=0, value=40, key="chi2_b_f")

    contingency_table = np.array([[a_success, a_failure], [b_success, b_failure]])
    st.dataframe(pd.DataFrame(contingency_table, columns=["Succès", "Échecs"], index=["Groupe A", "Groupe B"]))

    if st.button("🔬 Lancer le Chi² Test"):
        result = calculator.chi2_test(contingency_table)
        display_chi2_results(result)


def analyze_data_tab(calculator):
    st.header("📈 Analyse de Données CSV")
    uploaded_file = st.file_uploader("Chargez vos données (CSV)", type=["csv"])

    if uploaded_file is not None:
        df = DataLoader.load_csv_data(uploaded_file)
        if df.empty:
            st.error("Le fichier est vide ou mal formé.")
            return

        st.subheader("Aperçu des données")
        st.dataframe(df.head())

        col1, col2 = st.columns(2)
        with col1:
            group_col = st.selectbox("Colonne groupe", df.columns)
        with col2:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            metric_col = st.selectbox("Colonne métrique", numeric_cols if numeric_cols else df.columns)

        if st.button("Analyser"):
            if not DataLoader.validate_ab_data(df, group_col, metric_col):
                st.error("Données invalides pour un test A/B. Vérifiez les colonnes sélectionnées.")
                return

            groups = df[group_col].unique()
            if len(groups) < 2:
                st.error("Il faut au moins deux groupes pour comparer.")
                return

            group_a = df[df[group_col] == groups[0]][metric_col].dropna().values
            group_b = df[df[group_col] == groups[1]][metric_col].dropna().values

            result = calculator.t_test_two_sample(group_a, group_b)
            display_test_results(result, group_a, group_b)


def data_generator_tab(calculator):
    st.header("🎲 Générateur de Données")
    col1, col2 = st.columns(2)
    with col1:
        n = st.number_input("Échantillons par groupe", min_value=10, value=500)
        mean_a = st.number_input("Moyenne A", value=100.0)
        mean_b = st.number_input("Moyenne B", value=105.0)
    with col2:
        std = st.number_input("Écart-type", min_value=0.1, value=15.0)
        noise = st.slider("Niveau de bruit", 0.0, 1.0, 0.1)

    if st.button("Générer données"):
        group_a, group_b = DataGenerator.generate_continuous_data(n, n, mean_a, mean_b, std, std)
        if noise > 0:
            group_a = group_a + np.random.normal(0, noise * std, len(group_a))
            group_b = group_b + np.random.normal(0, noise * std, len(group_b))

        df_generated = pd.DataFrame({"group": ["A"] * len(group_a) + ["B"] * len(group_b), "value": np.concatenate([group_a, group_b])})
        st.dataframe(df_generated.head(10))

        result = calculator.t_test_two_sample(group_a, group_b)
        display_test_results(result)

        csv = df_generated.to_csv(index=False)
        st.download_button("Télécharger CSV", csv, file_name="ab_test_data.csv", mime="text/csv")


def run_power_analysis(calculator):
    st.header("📊 Analyse de Puissance")
    col1, col2 = st.columns(2)
    with col1:
        effect_size = st.slider("Taille d'effet", 0.1, 2.0, 0.5, 0.1)
        sample_size = st.slider("Taille d'échantillon (par groupe)", 10, 5000, 100, 10)
    with col2:
        power = calculator.calculate_power(effect_size, sample_size)
        st.metric("Puissance calculée", f"{power:.1%}")
        if power < 0.8:
            st.warning("Puissance insuffisante (< 80%)")
        else:
            st.success("Puissance suffisante (≥ 80%)")

    # Interactive heatmap/curve
    effect_sizes = np.linspace(0.1, 1.5, 20)
    sample_sizes = np.linspace(20, 2000, 20, dtype=int)
    powers = np.zeros((len(sample_sizes), len(effect_sizes)))
    for i, ss in enumerate(sample_sizes):
        for j, es in enumerate(effect_sizes):
            powers[i, j] = calculator.calculate_power(es, int(ss))

    fig_power = ABTestVisualizer.plot_power_analysis(effect_sizes, sample_sizes, powers)
    st.plotly_chart(fig_power, use_container_width=True)


def run_sample_size_calculator(calculator):
    st.header("📏 Calculateur de Taille d'Échantillon")
    col1, col2 = st.columns(2)
    with col1:
        effect_key = st.selectbox("Taille d'effet attendue", list(EFFECT_SIZES.keys()), format_func=lambda x: f"{x.title()} ({EFFECT_SIZES[x]})")
        effect_value = EFFECT_SIZES[effect_key]
        power = st.selectbox("Puissance souhaitée", POWER_LEVELS, index=0, format_func=lambda x: f"{x:.0%}")
    with col2:
        sample_size = calculator.calculate_sample_size(effect_value, power)
        st.metric("Taille échantillon requise (par groupe)", f"{sample_size:,}")
        st.metric("Total participants", f"{sample_size * 2:,}")

    st.markdown("### Estimation durée (optionnelle)")
    daily_visitors = st.number_input("Visiteurs quotidiens", min_value=1, value=1000)
    allocation = st.slider("% alloué au test", 0.1, 1.0, 0.5, 0.1)
    duration = SampleSizeHelper.estimate_test_duration(sample_size, daily_visitors, allocation)
    if "error" not in duration:
        st.metric("Durée estimée (jours)", f"{duration['days']}")
        st.metric("En semaines", f"{duration['weeks']}")
        st.metric("Échantillon/jour", f"{duration['daily_sample_rate']}")


def run_data_import(calculator):
    st.header("📁 Import de Données")
    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])
    if uploaded_file is None:
        return

    df = DataLoader.load_csv_data(uploaded_file)
    if df.empty:
        st.error("Le fichier est vide ou mal formé.")
        return

    st.subheader("Aperçu")
    st.dataframe(df.head())

    group_col = st.selectbox("Colonne groupe", df.columns)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    metric_col = st.selectbox("Colonne métrique", numeric_cols if numeric_cols else df.columns)

    if st.button("Analyser les données importées"):
        if not DataLoader.validate_ab_data(df, group_col, metric_col):
            st.error("Données invalides pour test A/B")
            return

        groups = df[group_col].unique()
        if len(groups) < 2:
            st.error("Il faut au moins deux groupes pour comparer.")
            return

        group_a = df[df[group_col] == groups[0]][metric_col].dropna().values
        group_b = df[df[group_col] == groups[1]][metric_col].dropna().values
        result = calculator.t_test_two_sample(group_a, group_b)
        display_test_results(result, group_a, group_b)


def display_test_results(result, group_a=None, group_b=None):
    st.subheader("Résultats")
    formatted = ResultsFormatter.format_test_results(result)
    cols = st.columns(4)
    keys = list(formatted.keys())
    for i, c in enumerate(cols):
        if i < len(keys):
            k = keys[i]
            c.metric(k, str(formatted[k]))

    st.markdown("### Interprétation")
    interpretation = ResultsFormatter.interpret_results(result)
    st.markdown(interpretation)

    if group_a is not None and group_b is not None:
        col1, col2 = st.columns(2)
        with col1:
            fig_dist = ABTestVisualizer.plot_distributions(group_a, group_b, result)
            st.plotly_chart(fig_dist, use_container_width=True)
        with col2:
            fig_ci = ABTestVisualizer.plot_confidence_interval(result)
            st.plotly_chart(fig_ci, use_container_width=True)

    add_export_section(result, interpretation)


def display_proportion_results(result):
    st.subheader("Résultats (Proportions)")
    formatted = ResultsFormatter.format_test_results(result)
    for k, v in formatted.items():
        st.metric(k, str(v))

    st.markdown("### Interprétation")
    interpretation = ResultsFormatter.interpret_results(result)
    st.markdown(interpretation)

    fig_prop = ABTestVisualizer.plot_proportions_comparison(result)
    st.plotly_chart(fig_prop, use_container_width=True)

    fig_ci = ABTestVisualizer.plot_confidence_interval(result)
    st.plotly_chart(fig_ci, use_container_width=True)

    add_export_section(result, interpretation)


def display_chi2_results(result):
    st.subheader("Résultats (Chi²)")
    formatted = ResultsFormatter.format_test_results(result)
    for k, v in formatted.items():
        st.metric(k, str(v))

    st.markdown("### Interprétation")
    interpretation = ResultsFormatter.interpret_results(result)
    st.markdown(interpretation)
    add_export_section(result, interpretation)


def add_export_section(result, interpretation):
    st.markdown("---")
    st.subheader("Export des résultats")
    col1, col2 = st.columns(2)
    with col1:
        json_data = ExportUtils.export_results_json(result)
        st.download_button("Export JSON", json_data, file_name="ab_test_results.json", mime="application/json")
    with col2:
        report = ExportUtils.create_report(result, interpretation)
        st.download_button("Rapport Markdown", report, file_name="ab_test_report.md", mime="text/markdown")


if __name__ == "__main__":
    main()
