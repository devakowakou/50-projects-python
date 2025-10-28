"""
Module de visualisation avec Plotly
Responsabilité: Créer tous les graphiques interactifs
Version 2.2 - Optimisée avec échantillonnage et cache
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Optional


class Visualizer:
    """Classe pour créer des visualisations interactives avec Plotly (Version Optimisée)"""
    
    # Constantes d'optimisation
    SAMPLE_THRESHOLD = 50_000  # Si > 50K lignes, échantillonner
    SAMPLE_SIZE = 10_000  # Taille de l'échantillon pour visualisations
    MAX_BINS = 50  # Nombre maximum de bins pour histogrammes
    
    def __init__(self, df: pd.DataFrame, theme: str = 'plotly_white'):
        self.df = df
        self.theme = theme
        self.color_palette = px.colors.qualitative.Set2
        # Cache pour stats déjà calculées
        self._stats_cache = {}
    
    def _get_sample(self, df: pd.DataFrame) -> pd.DataFrame:
        """Échantillonne les données si trop volumineuses"""
        if len(df) > self.SAMPLE_THRESHOLD:
            return df.sample(n=self.SAMPLE_SIZE, random_state=42)
        return df
    
    def _get_cached_stats(self, column: str) -> tuple:
        """Récupère ou calcule mean/std (avec cache)"""
        if column not in self._stats_cache:
            data = self.df[column].dropna()
            self._stats_cache[column] = (data.mean(), data.std(), data.min(), data.max())
        return self._stats_cache[column]
    
    def create_histogram(self, column: str, nbins: int = 30, 
                        show_distribution: bool = True) -> go.Figure:
        """
        Crée un histogramme interactif (OPTIMISÉ avec échantillonnage)
        
        Args:
            column: Nom de la colonne
            nbins: Nombre de bins
            show_distribution: Afficher la courbe de distribution normale
            
        Returns:
            Figure Plotly
        """
        # Échantillonner si nécessaire
        df_viz = self._get_sample(self.df)
        
        # Limiter le nombre de bins pour gros datasets
        effective_bins = min(nbins, self.MAX_BINS)
        
        fig = go.Figure()
        
        # Histogramme
        fig.add_trace(go.Histogram(
            x=df_viz[column],
            nbinsx=effective_bins,
            name='Distribution',
            marker_color=self.color_palette[0],
            opacity=0.7
        ))
        
        # Ajouter la courbe de distribution normale si demandé
        if show_distribution:
            # Utiliser stats cachées au lieu de recalculer
            mean, std, min_val, max_val = self._get_cached_stats(column)
            
            x_range = np.linspace(min_val, max_val, 100)
            y_normal = ((1 / (std * np.sqrt(2 * np.pi))) * 
                       np.exp(-0.5 * ((x_range - mean) / std) ** 2))
            
            # Normaliser pour l'histogramme
            y_normal = y_normal * len(df_viz) * (max_val - min_val) / effective_bins
            
            fig.add_trace(go.Scatter(
                x=x_range,
                y=y_normal,
                mode='lines',
                name='Distribution Normale',
                line=dict(color='red', width=2)
            ))
        
        title = f'Distribution de {column}'
        if len(self.df) > self.SAMPLE_THRESHOLD:
            title += f' (échantillon de {self.SAMPLE_SIZE:,} lignes)'
        
        fig.update_layout(
            title=title,
            xaxis_title=column,
            yaxis_title='Fréquence',
            template=self.theme,
            hovermode='x unified'
        )
        
        return fig
    
    def create_boxplot(self, columns: List[str] = None, 
                      orientation: str = 'v') -> go.Figure:
        """
        Crée des box plots pour visualiser les outliers (OPTIMISÉ avec échantillonnage)
        
        Args:
            columns: Liste des colonnes (None = toutes numériques)
            orientation: 'v' (vertical) ou 'h' (horizontal)
            
        Returns:
            Figure Plotly
        """
        if columns is None:
            columns = self.df.select_dtypes(include=['number']).columns.tolist()
        
        # Échantillonner si nécessaire
        df_viz = self._get_sample(self.df)
        
        fig = go.Figure()
        
        for i, col in enumerate(columns):
            if orientation == 'v':
                fig.add_trace(go.Box(
                    y=df_viz[col],
                    name=col,
                    marker_color=self.color_palette[i % len(self.color_palette)],
                    boxmean='sd'  # Affiche moyenne et écart-type
                ))
            else:
                fig.add_trace(go.Box(
                    x=df_viz[col],
                    name=col,
                    marker_color=self.color_palette[i % len(self.color_palette)],
                    boxmean='sd'
                ))
        
        title = 'Box Plots - Détection des Outliers'
        if len(self.df) > self.SAMPLE_THRESHOLD:
            title += f' (échantillon de {self.SAMPLE_SIZE:,} lignes)'
        
        fig.update_layout(
            title=title,
            template=self.theme,
            showlegend=True,
            hovermode='closest'
        )
        
        return fig
    
    def create_correlation_heatmap(self, corr_matrix: pd.DataFrame, 
                                  method: str = 'pearson') -> go.Figure:
        """
        Crée une heatmap de corrélation
        
        Args:
            corr_matrix: Matrice de corrélation
            method: Méthode de corrélation utilisée
            
        Returns:
            Figure Plotly
        """
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title='Corrélation')
        ))
        
        fig.update_layout(
            title=f'Matrice de Corrélation ({method.capitalize()})',
            xaxis_title='Variables',
            yaxis_title='Variables',
            template=self.theme,
            width=800,
            height=800
        )
        
        return fig
    
    def create_scatter_plot(self, x_col: str, y_col: str, 
                          color_col: Optional[str] = None,
                          size_col: Optional[str] = None,
                          trendline: bool = True) -> go.Figure:
        """
        Crée un scatter plot interactif
        
        Args:
            x_col: Colonne pour l'axe X
            y_col: Colonne pour l'axe Y
            color_col: Colonne pour la couleur
            size_col: Colonne pour la taille des points
            trendline: Afficher la ligne de tendance
            
        Returns:
            Figure Plotly
        """
        fig = px.scatter(
            self.df,
            x=x_col,
            y=y_col,
            color=color_col,
            size=size_col,
            trendline='ols' if trendline else None,
            template=self.theme,
            title=f'{y_col} vs {x_col}'
        )
        
        fig.update_traces(marker=dict(opacity=0.7))
        
        fig.update_layout(
            hovermode='closest',
            xaxis_title=x_col,
            yaxis_title=y_col
        )
        
        return fig
    
    def create_bar_chart(self, column: str, top_n: int = 10, 
                        sort: bool = True) -> go.Figure:
        """
        Crée un bar chart pour les variables catégoriques
        
        Args:
            column: Nom de la colonne
            top_n: Nombre de catégories à afficher
            sort: Trier par fréquence
            
        Returns:
            Figure Plotly
        """
        value_counts = self.df[column].value_counts().head(top_n)
        
        if not sort:
            value_counts = value_counts.sort_index()
        
        fig = go.Figure(data=[
            go.Bar(
                x=value_counts.index,
                y=value_counts.values,
                marker_color=self.color_palette[0],
                text=value_counts.values,
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title=f'Top {top_n} valeurs de {column}',
            xaxis_title=column,
            yaxis_title='Fréquence',
            template=self.theme,
            showlegend=False
        )
        
        return fig
    
    def create_missing_values_chart(self) -> go.Figure:
        """
        Visualise les valeurs manquantes
        
        Returns:
            Figure Plotly
        """
        missing_data = self.df.isnull().sum()
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        
        if len(missing_data) == 0:
            # Créer un graphique vide avec message
            fig = go.Figure()
            fig.add_annotation(
                text="✅ Aucune valeur manquante !",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color="green")
            )
            return fig
        
        missing_percent = (missing_data / len(self.df) * 100).round(2)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=missing_data.index,
            y=missing_data.values,
            name='Valeurs manquantes',
            marker_color=self.color_palette[3],
            text=[f'{val} ({pct}%)' for val, pct in zip(missing_data.values, missing_percent.values)],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Analyse des Valeurs Manquantes',
            xaxis_title='Colonnes',
            yaxis_title='Nombre de valeurs manquantes',
            template=self.theme,
            showlegend=False
        )
        
        return fig
    
    def create_violin_plot(self, column: str, by: Optional[str] = None) -> go.Figure:
        """
        Crée un violin plot
        
        Args:
            column: Colonne numérique
            by: Colonne catégorique pour grouper
            
        Returns:
            Figure Plotly
        """
        if by:
            fig = go.Figure()
            categories = self.df[by].unique()
            
            for i, cat in enumerate(categories):
                data = self.df[self.df[by] == cat][column]
                fig.add_trace(go.Violin(
                    y=data,
                    name=str(cat),
                    box_visible=True,
                    meanline_visible=True,
                    fillcolor=self.color_palette[i % len(self.color_palette)],
                    opacity=0.6
                ))
            
            title = f'Distribution de {column} par {by}'
        else:
            fig = go.Figure(data=go.Violin(
                y=self.df[column],
                box_visible=True,
                meanline_visible=True,
                fillcolor=self.color_palette[0],
                opacity=0.6
            ))
            title = f'Distribution de {column}'
        
        fig.update_layout(
            title=title,
            yaxis_title=column,
            template=self.theme
        )
        
        return fig
    
    def create_pie_chart(self, column: str, top_n: int = 10) -> go.Figure:
        """
        Crée un pie chart
        
        Args:
            column: Colonne catégorique
            top_n: Nombre de catégories
            
        Returns:
            Figure Plotly
        """
        value_counts = self.df[column].value_counts().head(top_n)
        
        fig = go.Figure(data=[go.Pie(
            labels=value_counts.index,
            values=value_counts.values,
            hole=0.3,  # Donut chart
            textinfo='label+percent',
            marker=dict(colors=self.color_palette)
        )])
        
        fig.update_layout(
            title=f'Répartition de {column}',
            template=self.theme
        )
        
        return fig
    
    def create_line_chart(self, x_col: str, y_cols: List[str]) -> go.Figure:
        """
        Crée un line chart
        
        Args:
            x_col: Colonne pour l'axe X
            y_cols: Liste de colonnes pour l'axe Y
            
        Returns:
            Figure Plotly
        """
        fig = go.Figure()
        
        for i, col in enumerate(y_cols):
            fig.add_trace(go.Scatter(
                x=self.df[x_col],
                y=self.df[col],
                mode='lines+markers',
                name=col,
                line=dict(color=self.color_palette[i % len(self.color_palette)], width=2),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            title=f'Évolution',
            xaxis_title=x_col,
            yaxis_title='Valeurs',
            template=self.theme,
            hovermode='x unified'
        )
        
        return fig
    
    def create_summary_dashboard(self) -> go.Figure:
        """
        Crée un dashboard résumé avec plusieurs graphiques
        
        Returns:
            Figure Plotly avec subplots
        """
        numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()[:2]
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Distribution',
                'Box Plot',
                'Valeurs Manquantes',
                'Statistiques'
            ),
            specs=[[{'type': 'histogram'}, {'type': 'box'}],
                   [{'type': 'bar'}, {'type': 'table'}]]
        )
        
        if len(numeric_cols) > 0:
            # Histogramme
            fig.add_trace(
                go.Histogram(x=self.df[numeric_cols[0]], name=numeric_cols[0]),
                row=1, col=1
            )
            
            # Box plot
            fig.add_trace(
                go.Box(y=self.df[numeric_cols[0]], name=numeric_cols[0]),
                row=1, col=2
            )
        
        # Valeurs manquantes
        missing = self.df.isnull().sum()
        missing = missing[missing > 0]
        if len(missing) > 0:
            fig.add_trace(
                go.Bar(x=missing.index, y=missing.values),
                row=2, col=1
            )
        
        fig.update_layout(
            height=800,
            showlegend=False,
            template=self.theme,
            title_text="Dashboard Résumé"
        )
        
        return fig
