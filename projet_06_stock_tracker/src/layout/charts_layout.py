"""
Layout principal des graphiques et visualisations
"""

import dash_bootstrap_components as dbc
from dash import html, dcc

def create_charts_layout():
    """Crée le layout principal des graphiques"""
    return dbc.Container([
        dbc.Tabs([
            # Onglet 1: Analyse Principale
            dbc.Tab([
                html.Div([
                    # Graphique principal
                    dbc.Card([
                        dbc.CardHeader("📊 Graphique des Prix et Indicateurs"),
                        dbc.CardBody([
                            dcc.Graph(
                                id='price-chart',
                                config={'displayModeBar': True, 'scrollZoom': True}
                            )
                        ])
                    ], className="mb-3"),
                    
                    # Signaux détectés
                    dbc.Card([
                        dbc.CardHeader("🎯 Signaux Techniques Détectés"),
                        dbc.CardBody([
                            html.Div(id="signals-display", className="alert-container")
                        ])
                    ])
                ])
            ], label="Analyse Principale", tab_id="tab-main"),
            
            # Onglet 2: Analyse Technique Avancée
            dbc.Tab([
                html.Div([
                    dbc.Card([
                        dbc.CardHeader("🔬 Analyse Technique Avancée"),
                        dbc.CardBody([
                            dcc.Graph(
                                id='technical-chart',
                                config={'displayModeBar': True}
                            )
                        ])
                    ])
                ])
            ], label="Analyse Avancée", tab_id="tab-technical"),
            
            # Onglet 3: Historique
            dbc.Tab([
                html.Div([
                    dbc.Card([
                        dbc.CardHeader("📚 Historique des Analyses"),
                        dbc.CardBody([
                            html.Div(id="history-display"),
                            dbc.Button("Charger plus...", id="load-more-history", color="outline-primary")
                        ])
                    ])
                ])
            ], label="Historique", tab_id="tab-history"),
            
            # Onglet 4: Alertes
            dbc.Tab([
                html.Div([
                    dbc.Card([
                        dbc.CardHeader("🔔 Gestion des Alertes"),
                        dbc.CardBody([
                            html.Div(id="alerts-management"),
                            dbc.Button("➕ Nouvelle Alerte", id="new-alert-btn", color="success")
                        ])
                    ])
                ])
            ], label="Alertes", tab_id="tab-alerts")
        ], id="main-tabs", active_tab="tab-main")
    ], fluid=True)