"""
Visualisations spécialisées pour le dashboard e-commerce
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict


class EcommerceCharts:
    """Générateur de graphiques pour KPIs e-commerce"""
    
    @staticmethod
    def create_revenue_evolution(time_data: pd.DataFrame) -> go.Figure:
        """Graphique d'évolution du CA dans le temps"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=time_data['date'],
            y=time_data['amount'],
            mode='lines+markers',
            name='Chiffre d\'affaires',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6),
            hovertemplate='<b>%{x}</b><br>CA: €%{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='📈 Évolution du Chiffre d\'Affaires',
            xaxis_title='Date',
            yaxis_title='Chiffre d\'Affaires (€)',
            hovermode='x unified',
            showlegend=False,
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_conversion_evolution(time_data: pd.DataFrame) -> go.Figure:
        """Graphique d'évolution du taux de conversion"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=time_data['date'],
            y=time_data['conversion_rate'],
            mode='lines+markers',
            name='Taux de conversion',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=6),
            hovertemplate='<b>%{x}</b><br>Conversion: %{y:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title='📊 Évolution du Taux de Conversion',
            xaxis_title='Date',
            yaxis_title='Taux de Conversion (%)',
            hovermode='x unified',
            showlegend=False,
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_revenue_by_source(revenue_by_source: pd.DataFrame) -> go.Figure:
        """Graphique CA par source de trafic"""
        fig = px.bar(
            revenue_by_source.reset_index(),
            x='source',
            y='total_revenue',
            title='💰 Chiffre d\'Affaires par Source de Trafic',
            color='total_revenue',
            color_continuous_scale='Blues'
        )
        
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>CA: €%{y:,.0f}<extra></extra>'
        )
        
        fig.update_layout(
            xaxis_title='Source de Trafic',
            yaxis_title='Chiffre d\'Affaires (€)',
            showlegend=False,
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_category_performance(revenue_by_category: pd.DataFrame) -> go.Figure:
        """Graphique performance par catégorie (top 8)"""
        top_categories = revenue_by_category.head(8)
        
        fig = px.pie(
            top_categories.reset_index(),
            values='total_revenue',
            names='category',
            title='🏷️ Top 8 Catégories par Revenus'
        )
        
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>CA: €%{value:,.0f}<br>Part: %{percent}<extra></extra>'
        )
        
        fig.update_layout(height=400)
        
        return fig
    
    @staticmethod
    def create_conversion_by_source(conversion_data: pd.DataFrame) -> go.Figure:
        """Graphique taux de conversion par source"""
        fig = px.bar(
            conversion_data,
            x='source',
            y='conversion_rate',
            title='🎯 Taux de Conversion par Source',
            color='conversion_rate',
            color_continuous_scale='Greens'
        )
        
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Conversion: %{y:.1f}%<extra></extra>'
        )
        
        fig.update_layout(
            xaxis_title='Source de Trafic',
            yaxis_title='Taux de Conversion (%)',
            showlegend=False,
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_kpi_summary_chart(kpis: Dict) -> go.Figure:
        """Graphique résumé des KPIs principaux"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('CA Total', 'Panier Moyen', 'Taux Conversion', 'Transactions'),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # CA Total
        fig.add_trace(go.Indicator(
            mode="number",
            value=kpis['total_revenue'],
            number={'prefix': "€", 'valueformat': ',.0f'},
            title={'text': "Chiffre d'Affaires"},
        ), row=1, col=1)
        
        # Panier Moyen
        fig.add_trace(go.Indicator(
            mode="number",
            value=kpis['average_order_value'],
            number={'prefix': "€", 'valueformat': ',.0f'},
            title={'text': "Panier Moyen"},
        ), row=1, col=2)
        
        # Taux de Conversion
        fig.add_trace(go.Indicator(
            mode="number",
            value=kpis['conversion_rate'],
            number={'suffix': "%", 'valueformat': '.1f'},
            title={'text': "Taux de Conversion"},
        ), row=2, col=1)
        
        # Nombre de Transactions
        fig.add_trace(go.Indicator(
            mode="number",
            value=kpis['total_transactions'],
            number={'valueformat': ','},
            title={'text': "Transactions"},
        ), row=2, col=2)
        
        fig.update_layout(height=300, title_text="📊 KPIs Principaux")
        
        return fig