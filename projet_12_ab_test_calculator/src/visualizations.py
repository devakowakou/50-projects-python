"""Visualisations pour tests A/B"""

import plotly.graph_objects as go
import numpy as np
from typing import Dict
from config import COLORS

class ABTestVisualizer:
    @staticmethod
    def plot_distributions(group_a: np.array, group_b: np.array, test_result: Dict) -> go.Figure:
        """Graphique des distributions"""
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=group_a, name='Groupe A', opacity=0.7, 
            marker_color=COLORS['group_a'], nbinsx=30
        ))
        
        fig.add_trace(go.Histogram(
            x=group_b, name='Groupe B', opacity=0.7,
            marker_color=COLORS['group_b'], nbinsx=30
        ))
        
        fig.update_layout(
            title='Distribution des Groupes A et B',
            xaxis_title='Valeur', yaxis_title='Fréquence',
            barmode='overlay', height=400
        )
        return fig
    
    @staticmethod
    def plot_confidence_interval(test_result: Dict) -> go.Figure:
        """Graphique intervalle de confiance"""
        diff = test_result['difference']
        ci_lower, ci_upper = test_result['confidence_interval']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[diff], y=[0], mode='markers',
            marker=dict(size=15, color=COLORS['significant'] if test_result['significant'] else COLORS['not_significant']),
            name='Différence observée'
        ))
        
        fig.add_trace(go.Scatter(
            x=[ci_lower, ci_upper], y=[0, 0],
            mode='lines+markers', line=dict(width=4),
            name='Intervalle confiance'
        ))
        
        fig.add_vline(x=0, line_dash="dash", line_color="gray")
        fig.update_layout(
            title='Intervalle de Confiance',
            xaxis_title='Différence', height=300
        )
        return fig
    
    @staticmethod
    def plot_proportions_comparison(test_result: Dict) -> go.Figure:
        """Comparaison des proportions"""
        groups = ['Groupe A', 'Groupe B']
        rates = [test_result['group_a']['rate'], test_result['group_b']['rate']]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=groups, y=rates,
            marker_color=[COLORS['group_a'], COLORS['group_b']],
            text=[f"{rate:.1%}" for rate in rates],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Comparaison Taux de Conversion',
            yaxis=dict(tickformat='.1%'), height=400
        )
        return fig