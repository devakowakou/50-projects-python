"""
Visualisations pour les tests A/B
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Tuple
from config import COLORS


class ABTestVisualizer:
    """Générateur de visualisations pour tests A/B"""
    
    @staticmethod
    def plot_distributions(group_a: np.array, group_b: np.array, 
                          test_result: Dict) -> go.Figure:
        """Graphique des distributions des deux groupes"""
        
        fig = go.Figure()
        
        # Histogrammes
        fig.add_trace(go.Histogram(
            x=group_a,
            name='Groupe A (Contrôle)',
            opacity=0.7,
            marker_color=COLORS['group_a'],
            nbinsx=30
        ))
        
        fig.add_trace(go.Histogram(
            x=group_b,
            name='Groupe B (Test)',
            opacity=0.7,
            marker_color=COLORS['group_b'],
            nbinsx=30
        ))
        
        # Lignes des moyennes
        fig.add_vline(
            x=test_result['group_a']['mean'],
            line_dash="dash",
            line_color=COLORS['group_a'],
            annotation_text=f"Moyenne A: {test_result['group_a']['mean']:.2f}"
        )
        
        fig.add_vline(
            x=test_result['group_b']['mean'],
            line_dash="dash",
            line_color=COLORS['group_b'],
            annotation_text=f"Moyenne B: {test_result['group_b']['mean']:.2f}"
        )
        
        fig.update_layout(
            title='Distribution des Groupes A et B',
            xaxis_title='Valeur',
            yaxis_title='Fréquence',
            barmode='overlay',
            height=400
        )
        
        return fig
    
    @staticmethod
    def plot_confidence_interval(test_result: Dict) -> go.Figure:
        """Graphique de l'intervalle de confiance"""
        
        diff = test_result['difference']
        ci_lower, ci_upper = test_result['confidence_interval']
        
        fig = go.Figure()
        
        # Point de la différence
        fig.add_trace(go.Scatter(
            x=[diff],
            y=[0],
            mode='markers',
            marker=dict(
                size=15,
                color=COLORS['significant'] if test_result['significant'] else COLORS['not_significant']
            ),
            name='Différence observée'
        ))
        
        # Intervalle de confiance
        fig.add_trace(go.Scatter(
            x=[ci_lower, ci_upper],
            y=[0, 0],
            mode='lines+markers',
            line=dict(width=4),
            marker=dict(size=8),
            name=f'IC à {int((1-0.05)*100)}%'
        ))
        
        # Ligne de référence (pas de différence)
        fig.add_vline(
            x=0,
            line_dash="dash",
            line_color="gray",
            annotation_text="Pas de différence"
        )
        
        fig.update_layout(
            title='Intervalle de Confiance de la Différence',
            xaxis_title='Différence',
            yaxis=dict(showticklabels=False),
            height=300,
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def plot_power_analysis(effect_sizes: np.array, sample_sizes: np.array, 
                           powers: np.array) -> go.Figure:
        """Graphique d'analyse de puissance"""
        
        fig = go.Figure()
        
        # Surface de puissance
        fig.add_trace(go.Contour(
            x=effect_sizes,
            y=sample_sizes,
            z=powers,
            colorscale='Viridis',
            contours=dict(
                showlabels=True,
                labelfont=dict(size=12, color='white')
            )
        ))
        
        fig.update_layout(
            title='Analyse de Puissance Statistique',
            xaxis_title='Taille d\'effet',
            yaxis_title='Taille d\'échantillon',
            height=500
        )
        
        return fig
    
    @staticmethod
    def plot_proportions_comparison(test_result: Dict) -> go.Figure:
        """Graphique de comparaison des proportions"""
        
        groups = ['Groupe A', 'Groupe B']
        rates = [test_result['group_a']['rate'], test_result['group_b']['rate']]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=groups,
            y=rates,
            marker_color=[COLORS['group_a'], COLORS['group_b']],
            text=[f"{rate:.1%}" for rate in rates],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Comparaison des Taux de Conversion',
            xaxis_title='Groupe',
            yaxis_title='Taux de conversion',
            yaxis=dict(tickformat='.1%'),
            height=400
        )
        
        return fig
    
    @staticmethod
    def plot_sample_size_calculator(effect_size: float, power_levels: list, 
                                  sample_sizes: list) -> go.Figure:
        """Graphique du calculateur de taille d'échantillon"""
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=power_levels,
            y=sample_sizes,
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(size=8),
            name=f'Taille d\'effet: {effect_size}'
        ))
        
        # Ligne de référence pour 80% de puissance
        fig.add_hline(
            y=sample_sizes[power_levels.index(0.8)] if 0.8 in power_levels else None,
            line_dash="dash",
            line_color="red",
            annotation_text="Puissance recommandée (80%)"
        )
        
        fig.update_layout(
            title='Taille d\'Échantillon Requise par Puissance',
            xaxis_title='Puissance statistique',
            yaxis_title='Taille d\'échantillon (par groupe)',
            xaxis=dict(tickformat='.0%'),
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_results_summary(test_result: Dict) -> go.Figure:
        """Résumé visuel des résultats"""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Statistique', 'P-value', 'Taille d\'effet', 'Significatif'),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Statistique de test
        fig.add_trace(go.Indicator(
            mode="number",
            value=test_result['statistic'],
            number={'valueformat': '.3f'},
            title={'text': f"{test_result['test_type']} statistique"},
        ), row=1, col=1)
        
        # P-value
        fig.add_trace(go.Indicator(
            mode="number+gauge",
            value=test_result['p_value'],
            number={'valueformat': '.4f'},
            title={'text': "P-value"},
            gauge={
                'axis': {'range': [None, 0.1]},
                'bar': {'color': COLORS['significant'] if test_result['significant'] else COLORS['not_significant']},
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 0.05
                }
            }
        ), row=1, col=2)
        
        # Taille d'effet
        fig.add_trace(go.Indicator(
            mode="number",
            value=abs(test_result['effect_size']),
            number={'valueformat': '.3f'},
            title={'text': "Taille d'effet"},
        ), row=2, col=1)
        
        # Significatif
        fig.add_trace(go.Indicator(
            mode="number",
            value=1 if test_result['significant'] else 0,
            number={'valueformat': '.0f'},
            title={'text': "Significatif (1=Oui, 0=Non)"},
        ), row=2, col=2)
        
        fig.update_layout(height=400, title_text="Résumé des Résultats")
        
        return fig