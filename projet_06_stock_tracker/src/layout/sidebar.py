"""
Composant Sidebar de l'application
"""

import dash_bootstrap_components as dbc
from dash import html, dcc

def create_sidebar():
    """Crée la sidebar avec les contrôles"""
    return dbc.Card([
        dbc.CardHeader("🎯 Contrôles d'Analyse", className="fw-bold"),
        
        dbc.CardBody([
            # Sélecteur de symbole
            html.Div([
                html.Label("Symbole Boursier:", className="form-label"),
                dcc.Dropdown(
                    id='symbol-selector',
                    options=[
                        {'label': 'Apple (AAPL)', 'value': 'AAPL'},
                        {'label': 'Tesla (TSLA)', 'value': 'TSLA'},
                        {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
                        {'label': 'Google (GOOGL)', 'value': 'GOOGL'},
                        {'label': 'Amazon (AMZN)', 'value': 'AMZN'},
                        {'label': 'Meta (META)', 'value': 'META'},
                        {'label': 'Nvidia (NVDA)', 'value': 'NVDA'},
                        {'label': 'Netflix (NFLX)', 'value': 'NFLX'},
                    ],
                    value='AAPL',
                    clearable=False,
                    className="mb-3"
                ),
            ]),
            
            # Sélecteur de période
            html.Div([
                html.Label("Période:", className="form-label"),
                dcc.Dropdown(
                    id='period-selector',
                    options=[
                        {'label': '1 Mois', 'value': '1mo'},
                        {'label': '3 Mois', 'value': '3mo'},
                        {'label': '6 Mois', 'value': '6mo'},
                        {'label': '1 An', 'value': '1y'},
                        {'label': '2 Ans', 'value': '2y'},
                        {'label': '5 Ans', 'value': '5y'},
                    ],
                    value='6mo',
                    clearable=False,
                    className="mb-3"
                ),
            ]),
            
            # Indicateurs techniques
            html.Div([
                html.Label("Indicateurs Techniques:", className="form-label"),
                dbc.Checklist(
                    id='indicators-checklist',
                    options=[
                        {'label': ' Moyennes Mobiles (SMA)', 'value': 'sma'},
                        {'label': ' RSI', 'value': 'rsi'},
                        {'label': ' MACD', 'value': 'macd'},
                        {'label': ' Bandes de Bollinger', 'value': 'bollinger'},
                    ],
                    value=['sma', 'rsi'],
                    className="mb-3"
                ),
            ]),
            
            # Bouton d'analyse
            dbc.Button(
                "🔍 Analyser",
                id="analyze-btn",
                color="primary",
                className="w-100 mb-3",
                size="lg"
            ),
            
            # Informations du symbole
            html.Div(id="symbol-info", className="mt-3 p-2 bg-light rounded")
            
        ], style={'maxHeight': '80vh', 'overflowY': 'auto'})
    ], style={'height': 'fit-content', 'position': 'sticky', 'top': '80px'})