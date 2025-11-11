import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict
from datetime import datetime


class WeatherCharts:
    """Générateur de graphiques météo avec Plotly"""
    
    @staticmethod
    def create_temperature_line(history: List[Dict], city: str, unit_symbol: str = '°C') -> go.Figure:
        """
        Crée un graphique linéaire de température
        
        Args:
            history: Liste des données historiques
            city: Nom de la ville
            unit_symbol: Symbole de l'unité
            
        Returns:
            Figure Plotly
        """
        df = pd.DataFrame(history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        fig = go.Figure()
        
        # Température actuelle
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['temperature'],
            mode='lines+markers',
            name='Température',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=6),
            hovertemplate='<b>%{x|%d/%m %H:%M}</b><br>Temp: %{y}' + unit_symbol + '<extra></extra>'
        ))
        
        # Température min/max (zone)
        if 'temp_min' in df.columns and 'temp_max' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['temp_max'],
                mode='lines',
                name='Max',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['temp_min'],
                mode='lines',
                name='Min/Max',
                fill='tonexty',
                fillcolor='rgba(255, 107, 107, 0.2)',
                line=dict(width=0),
                hovertemplate='Min: %{y}' + unit_symbol + '<extra></extra>'
            ))
        
        fig.update_layout(
            title=f'🌡️ Évolution de la température - {city}',
            xaxis_title='Date et heure',
            yaxis_title=f'Température ({unit_symbol})',
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_forecast_chart(forecasts: List[Dict], city: str, unit_symbol: str = '°C') -> go.Figure:
        """
        Crée un graphique de prévisions avec température et pluie
        
        Args:
            forecasts: Liste des prévisions
            city: Nom de la ville
            unit_symbol: Symbole de l'unité
            
        Returns:
            Figure Plotly avec deux axes Y
        """
        df = pd.DataFrame(forecasts)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Créer figure avec axes secondaires
        fig = make_subplots(
            specs=[[{"secondary_y": True}]],
            subplot_titles=[f'📅 Prévisions - {city}']
        )
        
        # Température
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['temperature'],
                mode='lines+markers',
                name='Température',
                line=dict(color='#FF6B6B', width=3),
                marker=dict(size=8),
                hovertemplate='<b>%{x|%d/%m %H:%M}</b><br>Temp: %{y}' + unit_symbol + '<extra></extra>'
            ),
            secondary_y=False
        )
        
        # Probabilité de pluie (barres)
        fig.add_trace(
            go.Bar(
                x=df['timestamp'],
                y=df['pop'],
                name='Pluie',
                marker_color='rgba(100, 149, 237, 0.5)',
                hovertemplate='Pluie: %{y}%<extra></extra>'
            ),
            secondary_y=True
        )
        
        # Mise en forme
        fig.update_xaxes(title_text='Date et heure')
        fig.update_yaxes(title_text=f'Température ({unit_symbol})', secondary_y=False)
        fig.update_yaxes(title_text='Probabilité de pluie (%)', secondary_y=True, range=[0, 100])
        
        fig.update_layout(
            hovermode='x unified',
            template='plotly_white',
            height=450,
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def create_multi_city_comparison(cities_data: Dict[str, List[Dict]], unit_symbol: str = '°C') -> go.Figure:
        """
        Compare les températures de plusieurs villes
        
        Args:
            cities_data: Dict {ville: [historique]}
            unit_symbol: Symbole de l'unité
            
        Returns:
            Figure Plotly
        """
        fig = go.Figure()
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
        
        for idx, (city, history) in enumerate(cities_data.items()):
            if not history:
                continue
                
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            color = colors[idx % len(colors)]
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['temperature'],
                mode='lines+markers',
                name=city,
                line=dict(color=color, width=2),
                marker=dict(size=6),
                hovertemplate=f'<b>{city}</b><br>%{{x|%d/%m %H:%M}}<br>Temp: %{{y}}{unit_symbol}<extra></extra>'
            ))
        
        fig.update_layout(
            title='🌍 Comparaison multi-villes',
            xaxis_title='Date et heure',
            yaxis_title=f'Température ({unit_symbol})',
            hovermode='x unified',
            template='plotly_white',
            height=500,
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
    def create_weather_metrics_gauge(current_weather: Dict) -> go.Figure:
        """
        Crée des jauges pour les métriques météo
        
        Args:
            current_weather: Données météo actuelles
            
        Returns:
            Figure Plotly avec jauges
        """
        fig = make_subplots(
            rows=2, cols=2,
            specs=[
                [{'type': 'indicator'}, {'type': 'indicator'}],
                [{'type': 'indicator'}, {'type': 'indicator'}]
            ],
            subplot_titles=('Humidité', 'Pression', 'Vent', 'Nuages')
        )
        
        # Humidité
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=current_weather['humidity'],
            title={'text': "💧"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "lightblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 60], 'color': "gray"},
                    {'range': [60, 100], 'color': "darkgray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ), row=1, col=1)
        
        # Pression
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=current_weather['pressure'],
            title={'text': "🌪️"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [950, 1050]},
                'bar': {'color': "orange"},
                'steps': [
                    {'range': [950, 1000], 'color': "lightgray"},
                    {'range': [1000, 1020], 'color': "gray"},
                    {'range': [1020, 1050], 'color': "darkgray"}
                ]
            }
        ), row=1, col=2)
        
        # Vent
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=current_weather['wind_speed'],
            title={'text': "💨"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 30]},
                'bar': {'color': "lightgreen"},
                'steps': [
                    {'range': [0, 5], 'color': "lightgray"},
                    {'range': [5, 15], 'color': "gray"},
                    {'range': [15, 30], 'color': "darkgray"}
                ]
            }
        ), row=2, col=1)
        
        # Nuages
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=current_weather['clouds'],
            title={'text': "☁️"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "lightsteelblue"},
                'steps': [
                    {'range': [0, 25], 'color': "lightgray"},
                    {'range': [25, 75], 'color': "gray"},
                    {'range': [75, 100], 'color': "darkgray"}
                ]
            }
        ), row=2, col=2)
        
        fig.update_layout(
            height=500,
            showlegend=False,
            template='plotly_white'
        )
        
        return fig
    
    @staticmethod
    def create_humidity_pressure_chart(history: List[Dict], city: str) -> go.Figure:
        """
        Crée un graphique combiné humidité/pression
        
        Args:
            history: Données historiques
            city: Nom de la ville
            
        Returns:
            Figure Plotly
        """
        df = pd.DataFrame(history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=(
                f'💧 Humidité - {city}',
                f'🌪️ Pression atmosphérique - {city}'
            ),
            vertical_spacing=0.12
        )
        
        # Humidité
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['humidity'],
                mode='lines',
                name='Humidité',
                fill='tozeroy',
                fillcolor='rgba(100, 149, 237, 0.3)',
                line=dict(color='#6495ED', width=2),
                hovertemplate='%{x|%d/%m %H:%M}<br>Humidité: %{y}%<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Pression
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['pressure'],
                mode='lines',
                name='Pression',
                fill='tozeroy',
                fillcolor='rgba(255, 140, 0, 0.3)',
                line=dict(color='#FF8C00', width=2),
                hovertemplate='%{x|%d/%m %H:%M}<br>Pression: %{y} hPa<extra></extra>'
            ),
            row=2, col=1
        )
        
        fig.update_xaxes(title_text='Date et heure', row=2, col=1)
        fig.update_yaxes(title_text='Humidité (%)', row=1, col=1)
        fig.update_yaxes(title_text='Pression (hPa)', row=2, col=1)
        
        fig.update_layout(
            height=600,
            hovermode='x unified',
            template='plotly_white',
            showlegend=False
        )
        
        return fig
