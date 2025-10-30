"""
Module de visualisation des données COVID-19
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import config


class CovidVisualizer:
    """Générateur de graphiques pour les données COVID-19"""
    
    @staticmethod
    def create_timeline_chart(df, country, metric='new_cases'):
        """
        Crée un graphique d'évolution temporelle
        
        Args:
            df: DataFrame du pays
            country: Nom du pays
            metric: Métrique à afficher
            
        Returns:
            Figure Plotly
        """
        # Mapping des métriques
        metric_config = {
            'new_cases': {
                'title': 'Nouveaux cas quotidiens',
                'y_label': 'Nombre de cas',
                'color': config.COLOR_CASES,
                'ma_col': 'new_cases_ma'
            },
            'new_deaths': {
                'title': 'Nouveaux décès quotidiens',
                'y_label': 'Nombre de décès',
                'color': config.COLOR_DEATHS,
                'ma_col': 'new_deaths_ma'
            },
            'total_cases': {
                'title': 'Cas cumulés',
                'y_label': 'Nombre de cas',
                'color': config.COLOR_CASES,
                'ma_col': None
            },
            'total_deaths': {
                'title': 'Décès cumulés',
                'y_label': 'Nombre de décès',
                'color': config.COLOR_DEATHS,
                'ma_col': None
            },
        }
        
        conf = metric_config.get(metric, metric_config['new_cases'])
        
        fig = go.Figure()
        
        # Convertir dates en liste
        dates = df['date'].tolist()
        values = df[metric].tolist()
        
        # Trace principale
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines',
            name=conf['title'],
            line=dict(color=conf['color'], width=1),
            opacity=0.3
        ))
        
        # Moyenne mobile si disponible
        if conf['ma_col'] and conf['ma_col'] in df.columns:
            ma_values = df[conf['ma_col']].tolist()
            fig.add_trace(go.Scatter(
                x=dates,
                y=ma_values,
                mode='lines',
                name=f'Moyenne mobile {config.ROLLING_WINDOW}j',
                line=dict(color=conf['color'], width=3)
            ))
        
        fig.update_layout(
            title=f"{conf['title']} - {country}",
            xaxis_title="Date",
            yaxis_title=conf['y_label'],
            template=config.PLOTLY_TEMPLATE,
            hovermode='x unified',
            height=config.CHART_HEIGHT
        )
        
        return fig
    
    @staticmethod
    def create_comparison_chart(df, countries, metric='total_cases'):
        """
        Crée un graphique de comparaison entre pays
        
        Args:
            df: DataFrame complet
            countries: Liste de pays à comparer
            metric: Métrique à comparer
            
        Returns:
            Figure Plotly
        """
        fig = go.Figure()
        
        metric_labels = {
            'total_cases': 'Cas totaux',
            'total_deaths': 'Décès totaux',
            'new_cases': 'Nouveaux cas',
            'total_vaccinations': 'Vaccinations totales'
        }
        
        for country in countries:
            country_df = df[df['location'] == country]
            if not country_df.empty:
                dates = country_df['date'].tolist()
                values = country_df[metric].tolist()
                
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=values,
                    mode='lines',
                    name=country,
                    line=dict(width=2)
                ))
        
        fig.update_layout(
            title=f"Comparaison : {metric_labels.get(metric, metric)}",
            xaxis_title="Date",
            yaxis_title=metric_labels.get(metric, metric),
            template=config.PLOTLY_TEMPLATE,
            hovermode='x unified',
            height=config.CHART_HEIGHT,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    @staticmethod
    def create_bar_chart(comparison_df, metric_col):
        """
        Crée un graphique en barres pour comparaison
        
        Args:
            comparison_df: DataFrame de comparaison
            metric_col: Colonne de métrique à afficher
            
        Returns:
            Figure Plotly
        """
        if comparison_df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="Pas de données disponibles",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Trier par valeur décroissante
        df_sorted = comparison_df.sort_values(metric_col, ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_sorted[metric_col],
            y=df_sorted['Pays'],
            orientation='h',
            marker_color=config.COLOR_CASES,
            text=df_sorted[metric_col].apply(lambda x: f"{x:,.0f}"),
            textposition='outside'
        ))
        
        fig.update_layout(
            title=f"Comparaison : {metric_col}",
            xaxis_title=metric_col,
            yaxis_title="",
            template=config.PLOTLY_TEMPLATE,
            height=max(400, len(df_sorted) * 40),
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_pie_chart(metrics):
        """
        Crée un graphique camembert pour la vaccination
        
        Args:
            metrics: Dict des métriques d'un pays
            
        Returns:
            Figure Plotly
        """
        if not metrics or metrics['population'] == 0:
            fig = go.Figure()
            fig.add_annotation(
                text="Données de vaccination non disponibles",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False
            )
            return fig
        
        vaccinated = metrics['people_fully_vaccinated']
        partially = metrics['people_vaccinated'] - metrics['people_fully_vaccinated']
        not_vaccinated = metrics['population'] - metrics['people_vaccinated']
        
        # S'assurer que les valeurs sont positives
        partially = max(0, partially)
        not_vaccinated = max(0, not_vaccinated)
        
        labels = ['Complètement vaccinés', 'Partiellement vaccinés', 'Non vaccinés']
        values = [vaccinated, partially, not_vaccinated]
        colors = [config.COLOR_VACCINATIONS, config.COLOR_CASES, '#E0E0E0']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            title="État de la vaccination",
            template=config.PLOTLY_TEMPLATE,
            height=400
        )
        
        return fig
