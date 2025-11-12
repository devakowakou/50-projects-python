"""
Dashboard E-commerce KPIs - Application Streamlit
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="🛒 E-commerce KPIs Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Imports des modules
from src.data_generator import generate_sample_data
from src.kpi_calculator import EcommerceKPICalculator
from src.visualizations import EcommerceCharts
from src.utils import DataLoader, DateFilter, MetricFormatter, ExportUtils


def main():
    """Application principale"""
    
    # Header
    st.title("🛒 Dashboard E-commerce KPIs")
    st.markdown("**Analyse des performances avec 5 KPIs essentiels**")
    
    # Vérification et génération des données
    if not os.path.exists("data/transactions.json") or not os.path.exists("data/sessions.json"):
        st.warning("⚠️ Données non trouvées. Génération en cours...")
        
        with st.spinner("🔄 Génération de 10,000 transactions et 30,000 sessions..."):
            generate_sample_data()
        
        st.success("✅ Données générées avec succès!")
        st.rerun()
    
    # Chargement des données
    transactions_df = DataLoader.load_transactions()
    sessions_df = DataLoader.load_sessions()
    
    if transactions_df.empty or sessions_df.empty:
        st.error("❌ Impossible de charger les données")
        return
    
    # Filtres temporels
    start_date, end_date = DateFilter.create_date_filter(transactions_df)
    
    # Application des filtres
    filtered_transactions = DateFilter.filter_dataframe_by_date(transactions_df, start_date, end_date)
    filtered_sessions = DateFilter.filter_dataframe_by_date(sessions_df, start_date, end_date)
    
    # Calculateur KPIs
    kpi_calc = EcommerceKPICalculator(filtered_transactions, filtered_sessions)
    
    # Sidebar - Informations
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Informations")
    st.sidebar.metric("Transactions", f"{len(filtered_transactions):,}")
    st.sidebar.metric("Sessions", f"{len(filtered_sessions):,}")
    st.sidebar.metric("Période", f"{(end_date - start_date).days} jours")
    
    # KPIs Principaux
    st.subheader("📊 KPIs Principaux")
    
    kpis = kpi_calc.get_main_kpis()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Chiffre d'Affaires",
            MetricFormatter.format_currency(kpis['total_revenue'])
        )
    
    with col2:
        st.metric(
            "🛒 Panier Moyen",
            MetricFormatter.format_currency(kpis['average_order_value'])
        )
    
    with col3:
        st.metric(
            "🎯 Taux de Conversion",
            MetricFormatter.format_percentage(kpis['conversion_rate'])
        )
    
    with col4:
        st.metric(
            "📦 Transactions",
            MetricFormatter.format_number(kpis['total_transactions'])
        )
    
    # Graphiques d'évolution
    st.subheader("📈 Évolutions Temporelles")
    
    time_data = kpi_calc.get_time_series_data('D')
    
    col1, col2 = st.columns(2)
    
    with col1:
        revenue_chart = EcommerceCharts.create_revenue_evolution(time_data)
        st.plotly_chart(revenue_chart, use_container_width=True)
    
    with col2:
        conversion_chart = EcommerceCharts.create_conversion_evolution(time_data)
        st.plotly_chart(conversion_chart, use_container_width=True)
    
    # Analyses par segment
    st.subheader("🔍 Analyses par Segment")
    
    col1, col2 = st.columns(2)
    
    # CA par source
    revenue_by_source = kpi_calc.calculate_revenue_by_source()
    with col1:
        source_chart = EcommerceCharts.create_revenue_by_source(revenue_by_source)
        st.plotly_chart(source_chart, use_container_width=True)
    
    # Performance par catégorie
    revenue_by_category = kpi_calc.calculate_revenue_by_category()
    with col2:
        category_chart = EcommerceCharts.create_category_performance(revenue_by_category)
        st.plotly_chart(category_chart, use_container_width=True)
    
    # Conversion par source
    st.subheader("🎯 Analyse de Conversion")
    
    conversion_by_source = kpi_calc.get_conversion_by_source()
    conversion_source_chart = EcommerceCharts.create_conversion_by_source(conversion_by_source)
    st.plotly_chart(conversion_source_chart, use_container_width=True)
    
    # Tableaux détaillés
    st.subheader("📋 Données Détaillées")
    
    tab1, tab2, tab3 = st.tabs(["💰 CA par Source", "🏷️ CA par Catégorie", "🎯 Conversion par Source"])
    
    with tab1:
        st.dataframe(revenue_by_source, use_container_width=True)
    
    with tab2:
        st.dataframe(revenue_by_category, use_container_width=True)
    
    with tab3:
        st.dataframe(conversion_by_source, use_container_width=True)
    
    # Export
    st.sidebar.markdown("---")
    st.sidebar.subheader("📥 Export")
    
    # Rapport Markdown
    report = ExportUtils.create_summary_report(kpis, revenue_by_source, revenue_by_category)
    st.sidebar.download_button(
        label="📄 Rapport Markdown",
        data=report,
        file_name=f"rapport_kpis_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown"
    )
    
    # Données CSV
    csv_data = ExportUtils.export_to_csv(filtered_transactions, "transactions_filtered.csv")
    st.sidebar.download_button(
        label="📊 Transactions CSV",
        data=csv_data,
        file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    # Export JSON
    json_data = filtered_transactions.to_json(orient='records', indent=2)
    st.sidebar.download_button(
        label="📋 Données JSON",
        data=json_data,
        file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )
    
    # Export PDF
    pdf_data = ExportUtils.create_pdf_report(kpis, revenue_by_source, revenue_by_category)
    st.sidebar.download_button(
        label="📄 Rapport PDF",
        data=pdf_data,
        file_name=f"rapport_kpis_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf"
    )


if __name__ == "__main__":
    main()