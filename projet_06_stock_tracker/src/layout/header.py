"""
Composant Header de l'application
"""

import dash_bootstrap_components as dbc
from dash import html

def create_header():
    """Crée le header de l'application"""
    return dbc.Navbar(
        dbc.Container([
            # Logo et titre
            dbc.Row([
                dbc.Col([
                    html.H1("📈 Stock Analysis Dashboard", 
                           className="navbar-brand mb-0 h1",
                           style={'fontSize': '1.5rem', 'fontWeight': 'bold'})
                ], width="auto")
            ], align="center", className="g-0"),
            
            # Contrôles du header
            dbc.Row([
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button("🔄 Actualiser", id="refresh-btn", color="primary", size="sm"),
                        dbc.Button("💾 Sauvegarder", id="save-btn", color="success", size="sm"),
                        dbc.Button("⚙️ Paramètres", id="settings-btn", color="secondary", size="sm"),
                    ])
                ], width="auto")
            ], align="center")
        ], fluid=True),
        color="dark",
        dark=True,
        sticky="top",
        className="mb-3"
    )