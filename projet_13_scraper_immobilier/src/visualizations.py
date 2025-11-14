"""Visualisations pour l'analyse immobilière"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config import COLORS

class RealEstateVisualizer:
    @staticmethod
    def plot_price_distribution(df: pd.DataFrame) -> go.Figure:
        """Distribution des prix"""
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=df['price'],
            nbinsx=30,
            name='Prix',
            marker_color=COLORS['price_medium']
        ))
        
        fig.update_layout(
            title='Distribution des Prix',
            xaxis_title='Prix (€)',
            yaxis_title='Nombre de biens',
            height=400
        )
        
        return fig
    
    @staticmethod
    def plot_price_by_quartier(quartier_stats: pd.DataFrame) -> go.Figure:
        """Prix par quartier"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=quartier_stats['quartier'],
            y=quartier_stats['prix_m2_moyen'],
            marker_color=COLORS['price_high'],
            text=quartier_stats['prix_m2_moyen'].round(0),
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Prix Moyen au m² par Quartier',
            xaxis_title='Quartier',
            yaxis_title='Prix/m² (€)',
            height=500
        )
        
        return fig
    
    @staticmethod
    def plot_surface_vs_price(df: pd.DataFrame) -> go.Figure:
        """Surface vs Prix"""
        fig = px.scatter(
            df, 
            x='surface', 
            y='price',
            color='quartier',
            size='rooms',
            hover_data=['price_per_m2'],
            title='Relation Surface - Prix'
        )
        
        fig.update_layout(height=500)
        return fig
    
    @staticmethod
    def plot_quartier_comparison(quartier_stats: pd.DataFrame) -> go.Figure:
        """Comparaison des quartiers"""
        fig = go.Figure()
        
        # Prix moyen
        fig.add_trace(go.Scatter(
            x=quartier_stats['quartier'],
            y=quartier_stats['prix_m2_moyen'],
            mode='markers+lines',
            name='Prix/m² moyen',
            marker=dict(size=quartier_stats['nb_biens'], sizemode='diameter', sizeref=2),
            line=dict(color=COLORS['price_high'])
        ))
        
        fig.update_layout(
            title='Comparaison des Quartiers (taille = nombre de biens)',
            xaxis_title='Quartier',
            yaxis_title='Prix/m² (€)',
            height=500
        )
        
        return fig
    
    @staticmethod
    def plot_price_range_by_quartier(df: pd.DataFrame) -> go.Figure:
        """Fourchette de prix par quartier"""
        fig = go.Figure()
        
        for quartier in df['quartier'].unique():
            quartier_data = df[df['quartier'] == quartier]['price_per_m2']
            
            fig.add_trace(go.Box(
                y=quartier_data,
                name=quartier,
                boxpoints='outliers'
            ))
        
        fig.update_layout(
            title='Distribution des Prix/m² par Quartier',
            yaxis_title='Prix/m² (€)',
            height=500
        )
        
        return fig