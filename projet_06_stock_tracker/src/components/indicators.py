"""
Composants pour la gestion des indicateurs techniques
"""

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

def create_indicator_controls():
    """Crée les contrôles pour les indicateurs techniques"""
    return html.Div([
        dbc.Accordion([
            # Moyennes Mobiles
            dbc.AccordionItem([
                html.Div([
                    dbc.Checklist(
                        id='sma-checklist',
                        options=[
                            {'label': ' SMA 20', 'value': 20},
                            {'label': ' SMA 50', 'value': 50},
                            {'label': ' SMA 200', 'value': 200}
                        ],
                        value=[20, 50],
                        inline=True
                    ),
                    dbc.Checklist(
                        id='ema-checklist',
                        options=[
                            {'label': ' EMA 12', 'value': 12},
                            {'label': ' EMA 26', 'value': 26}
                        ],
                        value=[12, 26],
                        inline=True
                    )
                ])
            ], title="📊 Moyennes Mobiles"),
            
            # Oscillateurs
            dbc.AccordionItem([
                html.Div([
                    dbc.Checklist(
                        id='oscillators-checklist',
                        options=[
                            {'label': ' RSI (14)', 'value': 'rsi'},
                            {'label': ' MACD', 'value': 'macd'},
                            {'label': ' Stochastique', 'value': 'stochastic'},
                            {'label': ' Williams %R', 'value': 'williams'}
                        ],
                        value=['rsi', 'macd'],
                        inline=False
                    )
                ])
            ], title="📈 Oscillateurs"),
            
            # Bandes et Volatilité
            dbc.AccordionItem([
                html.Div([
                    dbc.Checklist(
                        id='volatility-checklist',
                        options=[
                            {'label': ' Bandes de Bollinger', 'value': 'bollinger'},
                            {'label': ' ATR (Average True Range)', 'value': 'atr'},
                            {'label': ' Volatilité Historique', 'value': 'historical_vol'}
                        ],
                        value=['bollinger'],
                        inline=False
                    ),
                    html.Div([
                        dbc.Label("Écart-type Bollinger:"),
                        dcc.Slider(
                            id='bollinger-std',
                            min=1,
                            max=3,
                            step=0.5,
                            value=2,
                            marks={1: '1', 1.5: '1.5', 2: '2', 2.5: '2.5', 3: '3'}
                        )
                    ], className="mt-2")
                ])
            ], title="🌊 Volatilité"),
            
            # Support/Résistance
            dbc.AccordionItem([
                html.Div([
                    dbc.Checklist(
                        id='support-resistance-checklist',
                        options=[
                            {'label': ' Points Pivots', 'value': 'pivot'},
                            {'label': ' Niveaux Fibonacci', 'value': 'fibonacci'},
                            {'label': ' Support/Résistance Dynamique', 'value': 'dynamic_sr'}
                        ],
                        value=[],
                        inline=False
                    )
                ])
            ], title="🎯 Support/Résistance")
        ], start_collapsed=True)
    ])

def create_indicator_summary(indicators_data):
    """Crée un résumé des indicateurs calculés"""
    if not indicators_data:
        return dbc.Alert("Aucun indicateur calculé", color="secondary")
    
    cards = []
    
    # RSI
    if 'RSI' in indicators_data:
        rsi_value = indicators_data['RSI'].iloc[-1] if hasattr(indicators_data['RSI'], 'iloc') else indicators_data['RSI'][-1]
        rsi_color = "success" if rsi_value < 30 else "danger" if rsi_value > 70 else "warning"
        rsi_text = "Survendu" if rsi_value < 30 else "Suracheté" if rsi_value > 70 else "Neutre"
        
        cards.append(
            dbc.Card([
                dbc.CardBody([
                    html.H6("RSI (14)", className="card-title"),
                    html.H4(f"{rsi_value:.1f}", className=f"text-{rsi_color}"),
                    html.Small(rsi_text, className="text-muted")
                ])
            ], className="text-center")
        )
    
    # MACD
    if all(key in indicators_data for key in ['MACD', 'MACD_Signal']):
        macd_value = indicators_data['MACD'].iloc[-1] if hasattr(indicators_data['MACD'], 'iloc') else indicators_data['MACD'][-1]
        signal_value = indicators_data['MACD_Signal'].iloc[-1] if hasattr(indicators_data['MACD_Signal'], 'iloc') else indicators_data['MACD_Signal'][-1]
        macd_color = "success" if macd_value > signal_value else "danger"
        macd_trend = "Haussier" if macd_value > signal_value else "Baissier"
        
        cards.append(
            dbc.Card([
                dbc.CardBody([
                    html.H6("MACD", className="card-title"),
                    html.H4(f"{macd_value:.3f}", className=f"text-{macd_color}"),
                    html.Small(macd_trend, className="text-muted")
                ])
            ], className="text-center")
        )
    
    # Moyennes Mobiles
    sma_signals = []
    for period in [20, 50, 200]:
        col_name = f'SMA_{period}'
        if col_name in indicators_data:
            sma_value = indicators_data[col_name].iloc[-1] if hasattr(indicators_data[col_name], 'iloc') else indicators_data[col_name][-1]
            sma_signals.append(f"SMA{period}: {sma_value:.2f}")
    
    if sma_signals:
        cards.append(
            dbc.Card([
                dbc.CardBody([
                    html.H6("Moyennes Mobiles", className="card-title"),
                    html.Div([html.Small(f"{signal}", className="d-block") for signal in sma_signals])
                ])
            ])
        )
    
    return dbc.Row([dbc.Col(card, width=4) for card in cards], className="g-2")

def create_technical_gauges(indicators_data):
    """Crée des jauges pour les indicateurs techniques"""
    figures = []
    
    # Jauge RSI
    if 'RSI' in indicators_data:
        rsi_value = indicators_data['RSI'].iloc[-1] if hasattr(indicators_data['RSI'], 'iloc') else indicators_data['RSI'][-1]
        
        fig_rsi = go.Figure(go.Indicator(
            mode="gauge+number",
            value=rsi_value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "RSI"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "lightyellow"},
                    {'range': [70, 100], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': rsi_value
                }
            }
        ))
        fig_rsi.update_layout(height=200, margin=dict(t=30, b=10))
        figures.append(fig_rsi)
    
    return figures