"""
Visualisations pour le dashboard e-commerce
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

class EcommerceVisualizations:
    
    @staticmethod
    def display_kpi_cards(kpis):
        """Affiche les KPIs principaux en cartes"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            evolution = kpis.get('total_revenue_evolution', 0)
            delta_color = "normal" if evolution >= 0 else "inverse"
            st.metric(
                "💰 Chiffre d'Affaires",
                f"{kpis['total_revenue']:,.0f} €",
                f"{evolution:+.1f}%",
                delta_color=delta_color
            )
        
        with col2:
            evolution = kpis.get('avg_order_value_evolution', 0)
            delta_color = "normal" if evolution >= 0 else "inverse"
            st.metric(
                "🛒 Panier Moyen",
                f"{kpis['avg_order_value']:.2f} €",
                f"{evolution:+.1f}%",
                delta_color=delta_color
            )
        
        with col3:
            evolution = kpis.get('conversion_rate_evolution', 0)
            delta_color = "normal" if evolution >= 0 else "inverse"
            st.metric(
                "📈 Taux de Conversion",
                f"{kpis['conversion_rate']:.2f}%",
                f"{evolution:+.1f}%",
                delta_color=delta_color
            )
        
        with col4:
            evolution = kpis.get('total_orders_evolution', 0)
            delta_color = "normal" if evolution >= 0 else "inverse"
            st.metric(
                "📦 Commandes",
                f"{kpis['total_orders']:,}",
                f"{evolution:+.1f}%",
                delta_color=delta_color
            )
    
    @staticmethod
    def plot_revenue_evolution(revenue_data):
        """Graphique d'évolution du CA"""
        fig = px.line(
            revenue_data,
            x='order_date',
            y='total_amount',
            title='📊 Évolution du Chiffre d\'Affaires',
            labels={'total_amount': 'CA (€)', 'order_date': 'Date'}
        )
        
        fig.update_traces(line_color='#1f77b4', line_width=3)
        fig.update_layout(
            height=400,
            showlegend=False,
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def plot_top_products(top_products_data):
        """Graphique des top produits"""
        fig = px.bar(
            top_products_data.head(10),
            x='total_price',
            y='name',
            orientation='h',
            title='🏆 Top 10 Produits par CA',
            labels={'total_price': 'CA (€)', 'name': 'Produit'}
        )
        
        fig.update_layout(
            height=500,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    @staticmethod
    def plot_revenue_by_category(category_data):
        """Graphique CA par catégorie"""
        fig = px.pie(
            category_data,
            values='total_price',
            names='category',
            title='🎯 Répartition du CA par Catégorie'
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        return fig
    
    @staticmethod
    def plot_conversion_funnel(kpis):
        """Entonnoir de conversion"""
        fig = go.Figure(go.Funnel(
            y=['Visiteurs', 'Commandes'],
            x=[kpis['total_visitors'], kpis['total_orders']],
            textinfo="value+percent initial"
        ))
        
        fig.update_layout(
            title='🔄 Funnel de Conversion',
            height=300
        )
        
        return fig
    
    @staticmethod
    def plot_conversion_by_channel(channel_data):
        """Conversion par canal"""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Visiteurs par Canal', 'Taux de Conversion par Canal'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Visiteurs par canal
        fig.add_trace(
            go.Bar(
                x=channel_data['channel'],
                y=channel_data['visitors'],
                name='Visiteurs',
                marker_color='lightblue'
            ),
            row=1, col=1
        )
        
        # Taux de conversion par canal
        fig.add_trace(
            go.Bar(
                x=channel_data['channel'],
                y=channel_data['conversion_rate'],
                name='Conversion (%)',
                marker_color='orange'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title='📱 Performance par Canal',
            height=400,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def plot_orders_vs_visitors(kpis):
        """Comparaison commandes vs visiteurs"""
        categories = ['Visiteurs', 'Commandes']
        values = [kpis['total_visitors'], kpis['total_orders']]
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=values,
                marker_color=['lightcoral', 'lightgreen']
            )
        ])
        
        fig.update_layout(
            title='👥 Visiteurs vs Commandes',
            height=300,
            showlegend=False
        )
        
        return fig