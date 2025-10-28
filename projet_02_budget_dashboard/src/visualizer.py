"""
Générateur de visualisations pour le dashboard
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Optional

class Visualizer:
    def __init__(self, colors: Dict[str, str]):
        """
        Initialise le visualiseur avec les couleurs du thème
        """
        self.colors = colors
    
    def create_pie_chart(self, df: pd.DataFrame, values_col: str, names_col: str, 
                        title: str, color_map: Optional[Dict] = None) -> go.Figure:
        """
        Crée un graphique en camembert
        """
        if df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="Aucune donnée disponible",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        fig = px.pie(
            df, 
            values=values_col, 
            names=names_col,
            title=title,
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Montant: %{value}€<br>Pourcentage: %{percent}<extra></extra>'
        )
        
        fig.update_layout(
            showlegend=True,
            height=400,
            margin=dict(t=50, b=20, l=20, r=20)
        )
        
        return fig
    
    def create_bar_chart(self, df: pd.DataFrame, x_col: str, y_col: str, 
                        title: str, color: str = None) -> go.Figure:
        """
        Crée un graphique en barres
        """
        if df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="Aucune donnée disponible",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            title=title,
            text=y_col,
            color_discrete_sequence=[color] if color else None
        )
        
        fig.update_traces(
            texttemplate='%{text:.2f}€',
            textposition='outside'
        )
        
        fig.update_layout(
            xaxis_title=x_col,
            yaxis_title="Montant (€)",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_trend_chart(self, df: pd.DataFrame, title: str = "Évolution du Budget") -> go.Figure:
        """
        Crée un graphique de tendance avec revenus, dépenses et solde
        """
        if df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="Aucune donnée disponible",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Convertir les dates en format approprié pour éviter le warning
        df = df.copy()
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            dates = df['Date'].tolist()
        else:
            dates = df['Date']
        
        fig = go.Figure()
        
        # Revenus cumulés
        if 'Revenus Cumulés' in df.columns:
            fig.add_trace(go.Scatter(
                x=dates,
                y=df['Revenus Cumulés'],
                mode='lines+markers',
                name='Revenus',
                line=dict(color=self.colors['revenus'], width=2),
                marker=dict(size=6),
                hovertemplate='<b>Revenus</b><br>Date: %{x}<br>Montant: %{y:.2f}€<extra></extra>'
            ))
        
        # Dépenses cumulées
        if 'Dépenses Cumulées' in df.columns:
            fig.add_trace(go.Scatter(
                x=dates,
                y=df['Dépenses Cumulées'],
                mode='lines+markers',
                name='Dépenses',
                line=dict(color=self.colors['depenses'], width=2),
                marker=dict(size=6),
                hovertemplate='<b>Dépenses</b><br>Date: %{x}<br>Montant: %{y:.2f}€<extra></extra>'
            ))
        
        # Solde
        if 'Solde' in df.columns:
            fig.add_trace(go.Scatter(
                x=dates,
                y=df['Solde'],
                mode='lines+markers',
                name='Solde',
                line=dict(color=self.colors['solde'], width=3, dash='dash'),
                marker=dict(size=8),
                hovertemplate='<b>Solde</b><br>Date: %{x}<br>Montant: %{y:.2f}€<extra></extra>'
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Montant (€)",
            height=450,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def create_budget_status_chart(self, df: pd.DataFrame, 
                                   title: str = "État des Budgets par Catégorie") -> go.Figure:
        """
        Crée un graphique de l'état des budgets
        """
        if df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="Aucune donnée disponible",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Déterminer les couleurs selon le pourcentage
        colors = []
        for pct in df['Pourcentage']:
            if pct >= 100:
                colors.append('#dc3545')  # Rouge
            elif pct >= 80:
                colors.append('#ffc107')  # Jaune
            else:
                colors.append('#28a745')  # Vert
        
        fig = go.Figure()
        
        # Barres pour le dépensé
        fig.add_trace(go.Bar(
            x=df['Catégorie'],
            y=df['Dépensé'],
            name='Dépensé',
            marker_color=colors,
            text=df['Dépensé'],
            texttemplate='%{text:.0f}€',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Dépensé: %{y:.2f}€<extra></extra>'
        ))
        
        # Ligne pour le budget
        fig.add_trace(go.Scatter(
            x=df['Catégorie'],
            y=df['Budget'],
            name='Budget',
            mode='lines+markers',
            line=dict(color='black', width=2, dash='dash'),
            marker=dict(size=8, symbol='diamond'),
            hovertemplate='<b>%{x}</b><br>Budget: %{y:.2f}€<extra></extra>'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Catégorie",
            yaxis_title="Montant (€)",
            height=450,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def create_monthly_comparison_chart(self, df: pd.DataFrame, 
                                       title: str = "Comparaison Mensuelle") -> go.Figure:
        """
        Crée un graphique de comparaison mensuelle
        """
        if df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="Aucune donnée disponible",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Copier pour éviter les modifications
        df = df.copy()
        
        # Grouper par mois et type
        df['YearMonth'] = pd.to_datetime(df['date']).dt.to_period('M').astype(str)
        
        monthly = df.groupby(['YearMonth', 'type'])['montant'].sum().reset_index()
        
        # Pivoter pour avoir revenus et dépenses en colonnes
        monthly_pivot = monthly.pivot(index='YearMonth', columns='type', values='montant').fillna(0)
        
        fig = go.Figure()
        
        if 'revenu' in monthly_pivot.columns:
            fig.add_trace(go.Bar(
                x=monthly_pivot.index,
                y=monthly_pivot['revenu'],
                name='Revenus',
                marker_color=self.colors['revenus'],
                text=monthly_pivot['revenu'],
                texttemplate='%{text:.0f}€',
                textposition='outside'
            ))
        
        if 'depense' in monthly_pivot.columns:
            fig.add_trace(go.Bar(
                x=monthly_pivot.index,
                y=monthly_pivot['depense'],
                name='Dépenses',
                marker_color=self.colors['depenses'],
                text=monthly_pivot['depense'],
                texttemplate='%{text:.0f}€',
                textposition='outside'
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Mois",
            yaxis_title="Montant (€)",
            height=400,
            barmode='group',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
