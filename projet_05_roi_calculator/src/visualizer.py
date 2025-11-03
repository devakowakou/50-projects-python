"""
Module pour la visualisation des résultats marketing
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Optional

class MarketingVisualizer:
    def __init__(self):
        pass
    
    def create_roi_gauge(self, roi_percentage: float) -> go.Figure:
        """
        Crée un gauge chart adaptatif pour le ROI
        """
        # Déterminer la plage dynamique en fonction du ROI
        if roi_percentage < 0:
            min_range = min(-100, roi_percentage - 50)
            max_range = max(100, abs(roi_percentage) + 50)
        else:
            min_range = -50
            max_range = max(200, roi_percentage + 50)
        
        # Déterminer la couleur en fonction du ROI
        if roi_percentage < 0:
            bar_color = "red"
        elif roi_percentage < 50:
            bar_color = "orange"
        else:
            bar_color = "green"
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=roi_percentage,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={
                'text': f"ROI: {roi_percentage}%",
                'font': {'size': 20}
            },
            delta={
                'reference': 0,
                'increasing': {'color': "green"},
                'decreasing': {'color': "red"}
            },
            number={
                'font': {'size': 30},
                'valueformat': '.1f',
                'suffix': '%'
            },
            gauge={
                'axis': {
                    'range': [min_range, max_range],
                    'tickwidth': 1,
                    'tickcolor': "darkblue"
                },
                'bar': {'color': bar_color, 'thickness': 0.8},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [min_range, 0], 'color': 'lightcoral'},
                    {'range': [0, 50], 'color': 'lightyellow'},
                    {'range': [50, max_range], 'color': 'lightgreen'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': roi_percentage
                }
            }
        ))
        
        fig.update_layout(
            height=350,
            margin=dict(t=80, b=20, l=20, r=20),
            font={'color': "darkblue", 'family': "Arial"},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_metrics_comparison(self, metrics_data: Dict) -> go.Figure:
        """
        Crée un graphique à barres pour comparer les métriques
        """
        if not metrics_data:
            # Données exemple si aucune donnée fournie
            metrics_data = {
                'metrics': ['ROI', 'CPC', 'CPM', 'CTR'],
                'values': [45, 2.5, 25, 3.2],
                'colors': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
            }
        
        fig = go.Figure(data=[
            go.Bar(
                x=metrics_data['metrics'],
                y=metrics_data['values'],
                marker_color=metrics_data.get('colors', '#1f77b4'),
                text=metrics_data['values'],
                texttemplate='%{text:.1f}',
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Comparaison des Métriques Marketing",
            xaxis_title="Métriques",
            yaxis_title="Valeurs",
            showlegend=False,
            height=400,
            template="plotly_white"
        )
        
        return fig
    
    def create_scenario_comparison(self, scenarios: List[Dict]) -> go.Figure:
        """
        Crée un graphique comparatif des scénarios
        """
        if not scenarios:
            # Données exemple
            scenarios = [
                {'name': 'Scénario Actuel', 'roi': 45, 'profit': 5000},
                {'name': 'Budget +20%', 'roi': 52, 'profit': 6200},
                {'name': 'Coût -10%', 'roi': 58, 'profit': 5800}
            ]
        
        scenario_names = [s['name'] for s in scenarios]
        roi_values = [s['roi'] for s in scenarios]
        profit_values = [s['profit'] for s in scenarios]
        
        fig = go.Figure()
        
        # ROI en barres
        fig.add_trace(go.Bar(
            name='ROI (%)',
            x=scenario_names,
            y=roi_values,
            yaxis='y',
            offsetgroup=1,
            marker_color='#1f77b4',
            text=roi_values,
            texttemplate='%{text:.1f}%',
            textposition='auto',
        ))
        
        # Profit en ligne
        fig.add_trace(go.Scatter(
            name='Profit (€)',
            x=scenario_names,
            y=profit_values,
            yaxis='y2',
            mode='lines+markers+text',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=10),
            text=[f'€{p:,.0f}' for p in profit_values],
            textposition="top center"
        ))
        
        fig.update_layout(
            title="Comparaison des Scénarios Marketing",
            xaxis=dict(title="Scénarios"),
            yaxis=dict(
                title="ROI (%)",
                titlefont=dict(color="#1f77b4"),
                tickfont=dict(color="#1f77b4")
            ),
            yaxis2=dict(
                title="Profit (€)",
                titlefont=dict(color="#ff7f0e"),
                tickfont=dict(color="#ff7f0e"),
                anchor="x",
                overlaying="y",
                side="right"
            ),
            showlegend=True,
            height=500,
            template="plotly_white"
        )
        
        return fig
    
    def create_conversion_chart(self, conversion_data: Dict) -> go.Figure:
        """
        Crée un graphique pour visualiser les conversions
        """
        if not conversion_data:
            conversion_data = {
                'before': {'cpc': 2.0, 'cpm': 20.0},
                'after': {'cpc': 1.8, 'cpm': 18.0},
                'labels': ['Avant', 'Après']
            }
        
        fig = go.Figure()
        
        # CPC
        fig.add_trace(go.Bar(
            name='CPC (€)',
            x=conversion_data['labels'],
            y=[conversion_data['before']['cpc'], conversion_data['after']['cpc']],
            marker_color='#1f77b4',
            text=[conversion_data['before']['cpc'], conversion_data['after']['cpc']],
            texttemplate='€%{text:.2f}',
            textposition='auto',
        ))
        
        # CPM
        fig.add_trace(go.Bar(
            name='CPM (€)',
            x=conversion_data['labels'],
            y=[conversion_data['before']['cpm'], conversion_data['after']['cpm']],
            marker_color='#ff7f0e',
            text=[conversion_data['before']['cpm'], conversion_data['after']['cpm']],
            texttemplate='€%{text:.1f}',
            textposition='auto',
        ))
        
        fig.update_layout(
            title="Impact des Conversions sur les Coûts",
            xaxis_title="Période",
            yaxis_title="Coûts (€)",
            barmode='group',
            showlegend=True,
            height=400,
            template="plotly_white"
        )
        
        return fig
    
    def create_break_even_chart(self, fixed_costs: float, price: float, variable_cost: float) -> go.Figure:
        """
        Crée un graphique de seuil de rentabilité
        """
        # Calcul du seuil de rentabilité
        contribution_margin = price - variable_cost
        breakeven_units = fixed_costs / contribution_mgress_margin
        
        # Génération des données
        units = list(range(0, int(breakeven_units * 2) + 1, max(1, int(breakeven_units * 2 / 20))))
        revenue = [u * price for u in units]
        total_costs = [fixed_costs + (u * variable_cost) for u in units]
        profit = [rev - cost for rev, cost in zip(revenue, total_costs)]
        
        fig = go.Figure()
        
        # Revenus
        fig.add_trace(go.Scatter(
            x=units, y=revenue,
            mode='lines',
            name='Revenus',
            line=dict(color='green', width=3)
        ))
        
        # Coûts totaux
        fig.add_trace(go.Scatter(
            x=units, y=total_costs,
            mode='lines',
            name='Coûts Totaux',
            line=dict(color='red', width=3)
        ))
        
        # Coûts fixes
        fig.add_trace(go.Scatter(
            x=units, y=[fixed_costs] * len(units),
            mode='lines',
            name='Coûts Fixes',
            line=dict(color='orange', width=2, dash='dash')
        ))
        
        # Point de seuil de rentabilité
        fig.add_trace(go.Scatter(
            x=[breakeven_units], y=[breakeven_units * price],
            mode='markers+text',
            name='Seuil Rentabilité',
            marker=dict(color='black', size=12),
            text=[f'Seuil: {breakeven_units:.0f} units'],
            textposition="top right"
        ))
        
        fig.update_layout(
            title=f"Analyse du Seuil de Rentabilité\n(Seuil: {breakeven_units:.0f} units)",
            xaxis_title="Quantité Vendue",
            yaxis_title="Montant (€)",
            showlegend=True,
            height=500,
            template="plotly_white"
        )
        
        return fig