"""
Dashboard E-commerce KPIs
Application Streamlit pour analyser les performances e-commerce
"""
import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# Import des modules locaux
from src.data_generator import EcommerceDataGenerator
from src.kpi_calculator import EcommerceKPICalculator
from src.visualizations import EcommerceVisualizations

# Configuration de la page
st.set_page_config(
    page_title="Dashboard E-commerce KPIs",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_or_generate_data():
    """Charge ou génère les données e-commerce"""
    data_dir = "data"
    
    # Vérifier si les données existent
    files_exist = all(os.path.exists(f"{data_dir}/{file}") for file in 
                     ['products.csv', 'customers.csv', 'orders.csv', 'order_items.csv', 'visitors.csv'])
    
    if not files_exist:
        st.info("🔄 Génération des données e-commerce...")
        
        # Créer le dossier data s'il n'existe pas
        os.makedirs(data_dir, exist_ok=True)
        
        # Générer les données
        generator = EcommerceDataGenerator()
        
        products_df = generator.generate_products(100)
        customers_df = generator.generate_customers(1000)
        orders_df, order_items_df, visitors_df = generator.generate_orders(
            products_df, customers_df, 5000
        )
        
        # Sauvegarder
        products_df.to_csv(f"{data_dir}/products.csv", index=False)
        customers_df.to_csv(f"{data_dir}/customers.csv", index=False)
        orders_df.to_csv(f"{data_dir}/orders.csv", index=False)
        order_items_df.to_csv(f"{data_dir}/order_items.csv", index=False)
        visitors_df.to_csv(f"{data_dir}/visitors.csv", index=False)
        
        st.success("✅ Données générées avec succès!")
    
    # Charger les données
    products_df = pd.read_csv(f"{data_dir}/products.csv")
    customers_df = pd.read_csv(f"{data_dir}/customers.csv")
    orders_df = pd.read_csv(f"{data_dir}/orders.csv")
    order_items_df = pd.read_csv(f"{data_dir}/order_items.csv")
    visitors_df = pd.read_csv(f"{data_dir}/visitors.csv")
    
    return products_df, customers_df, orders_df, order_items_df, visitors_df

def main():
    # Titre principal
    st.title("🛒 Dashboard E-commerce KPIs")
    st.markdown("---")
    
    # Chargement des données
    products_df, customers_df, orders_df, order_items_df, visitors_df = load_or_generate_data()
    
    # Initialiser le calculateur de KPIs
    kpi_calc = EcommerceKPICalculator(orders_df, order_items_df, visitors_df, products_df)
    viz = EcommerceVisualizations()
    
    # Sidebar pour les filtres
    st.sidebar.header("🎛️ Filtres")
    
    # Sélection de la période
    period_options = {
        "7 derniers jours": 7,
        "30 derniers jours": 30,
        "90 derniers jours": 90,
        "1 an": 365
    }
    
    selected_period = st.sidebar.selectbox(
        "📅 Période d'analyse",
        list(period_options.keys()),
        index=1
    )
    days = period_options[selected_period]
    
    # Sélection du canal
    channels = ['Tous'] + list(orders_df['channel'].unique())
    selected_channel = st.sidebar.selectbox("📱 Canal", channels)
    channel_filter = None if selected_channel == 'Tous' else selected_channel
    
    # Calcul des KPIs avec évolution
    kpis = kpi_calc.calculate_evolution(days)
    
    # Affichage des KPIs principaux
    st.subheader("📊 KPIs Principaux")
    viz.display_kpi_cards(kpis)
    
    st.markdown("---")
    
    # Layout en colonnes pour les graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        # Évolution du CA
        revenue_data = kpi_calc.get_revenue_by_period('D', days)
        if not revenue_data.empty:
            fig_revenue = viz.plot_revenue_evolution(revenue_data)
            st.plotly_chart(fig_revenue, use_container_width=True)
        
        # CA par catégorie
        category_data = kpi_calc.get_revenue_by_category(days)
        if not category_data.empty:
            fig_category = viz.plot_revenue_by_category(category_data)
            st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        # Funnel de conversion
        fig_funnel = viz.plot_conversion_funnel(kpis)
        st.plotly_chart(fig_funnel, use_container_width=True)
        
        # Conversion par canal
        channel_data = kpi_calc.get_conversion_by_channel(days)
        if not channel_data.empty:
            fig_channels = viz.plot_conversion_by_channel(channel_data)
            st.plotly_chart(fig_channels, use_container_width=True)
    
    # Top produits
    st.subheader("🏆 Top Produits")
    top_products = kpi_calc.get_top_products(10, days)
    if not top_products.empty:
        fig_products = viz.plot_top_products(top_products)
        st.plotly_chart(fig_products, use_container_width=True)
        
        # Tableau détaillé
        with st.expander("📋 Détails des Top Produits"):
            st.dataframe(
                top_products[['name', 'category', 'total_price', 'quantity']].round(2),
                use_container_width=True
            )
    
    # Statistiques détaillées
    st.markdown("---")
    st.subheader("📈 Statistiques Détaillées")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👥 Total Visiteurs", f"{kpis['total_visitors']:,}")
        st.metric("🛍️ Total Commandes", f"{kpis['total_orders']:,}")
    
    with col2:
        st.metric("💰 CA Total", f"{kpis['total_revenue']:,.2f} €")
        st.metric("🛒 Panier Moyen", f"{kpis['avg_order_value']:.2f} €")
    
    with col3:
        st.metric("📊 Taux Conversion", f"{kpis['conversion_rate']:.2f}%")
        revenue_per_visitor = kpis['total_revenue'] / kpis['total_visitors'] if kpis['total_visitors'] > 0 else 0
        st.metric("💵 CA/Visiteur", f"{revenue_per_visitor:.2f} €")

if __name__ == "__main__":
    main()