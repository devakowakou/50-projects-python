"""
Composants graphiques Plotly
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class ChartBuilder:
    def __init__(self):
        pass
    
    def create_price_chart(self, data: pd.DataFrame, symbol: str, indicators: list = None) -> go.Figure:
        """Crée un graphique de prix avec indicateurs"""
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(f'{symbol} - Prix et Volume', 'RSI'),
            row_heights=[0.7, 0.3]
        )
        
        # Graphique des prix (candlesticks ou ligne)
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name='Prix de clôture',
                line=dict(color='#1f77b4', width=2)
            ),
            row=1, col=1
        )
        
        # Volume
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker_color='rgba(0,0,0,0.3)',
                opacity=0.5
            ),
            row=1, col=1
        )
        
        # Ajout des indicateurs
        if indicators:
            for indicator in indicators:
                if indicator in data.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=data.index,
                            y=data[indicator],
                            mode='lines',
                            name=indicator,
                            line=dict(width=1)
                        ),
                        row=1, col=1
                    )
        
        # RSI
        if 'RSI' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['RSI'],
                    mode='lines',
                    name='RSI',
                    line=dict(color='purple', width=2)
                ),
                row=2, col=1
            )
            
            # Lignes RSI 30 et 70
            fig.add_hline(y=30, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        
        fig.update_layout(
            height=600,
            showlegend=True,
            template="plotly_white",
            xaxis_rangeslider_visible=False
        )
        
        return fig
    
    def create_technical_chart(self, data: pd.DataFrame, symbol: str) -> go.Figure:
        """Crée un graphique technique avancé"""
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(
                f'{symbol} - Prix et MACD',
                'MACD',
                'RSI'
            ),
            row_heights=[0.5, 0.25, 0.25]
        )
        
        # Prix
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name='Prix',
                line=dict(color='#1f77b4', width=2)
            ),
            row=1, col=1
        )
        
        # MACD
        if all(col in data.columns for col in ['MACD', 'MACD_Signal']):
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['MACD'],
                    mode='lines',
                    name='MACD',
                    line=dict(color='blue', width=2)
                ),
                row=2, col=1
            )
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['MACD_Signal'],
                    mode='lines',
                    name='Signal',
                    line=dict(color='red', width=2)
                ),
                row=2, col=1
            )
            
            # Histogramme MACD
            if 'MACD_Histogram' in data.columns:
                colors = ['green' if x >= 0 else 'red' for x in data['MACD_Histogram']]
                fig.add_trace(
                    go.Bar(
                        x=data.index,
                        y=data['MACD_Histogram'],
                        name='Histogram',
                        marker_color=colors,
                        opacity=0.6
                    ),
                    row=2, col=1
                )
        
        # RSI
        if 'RSI' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['RSI'],
                    mode='lines',
                    name='RSI',
                    line=dict(color='purple', width=2)
                ),
                row=3, col=1
            )
            fig.add_hline(y=30, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
        
        fig.update_layout(
            height=800,
            showlegend=True,
            template="plotly_white"
        )
        
        return fig