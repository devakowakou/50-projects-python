"""Application Dash pour le dashboard d'analyse social media."""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.config import settings
from frontend.components.charts import (
    create_followers_chart, create_engagement_chart, create_top_posts_chart,
    create_best_times_chart, create_content_performance_chart, 
    create_growth_trend_chart, create_platform_comparison_chart
)

# Importer les callbacks
from frontend.callbacks import dashboard_callbacks

# Initialiser l'app Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
    ],
    title="Social Analytics Dashboard"
)

# Layout principal
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("📊 Social Analytics Dashboard", className="text-center mb-4"),
        html.P("Analyse d'audiences Instagram & TikTok", className="text-center text-muted"),
        
        # Statut de connexion
        html.Div(id="connection-status", className="text-center mb-3")
    ], className="container-fluid bg-light py-4 mb-4"),
    
    # Contenu principal
    html.Div([
        # Métriques principales
        html.Div([
            html.H3("📈 Métriques Principales", className="mb-3"),
            html.Div(id="metrics-cards", className="row mb-4")
        ]),
        
        # Contrôles
        html.Div([
            html.Div([
                html.Label("Plateforme:", className="form-label"),
                dcc.Dropdown(
                    id="platform-dropdown",
                    options=[
                        {"label": "📷 Instagram", "value": "instagram"},
                        {"label": "🎵 TikTok", "value": "tiktok"},
                        {"label": "📊 Toutes", "value": "all"}
                    ],
                    value="all",
                    className="mb-3"
                )
            ], className="col-md-3"),
            
            html.Div([
                html.Label("Période (jours):", className="form-label"),
                dcc.Dropdown(
                    id="days-dropdown",
                    options=[
                        {"label": "7 jours", "value": 7},
                        {"label": "30 jours", "value": 30},
                        {"label": "90 jours", "value": 90}
                    ],
                    value=30,
                    className="mb-3"
                )
            ], className="col-md-3"),
            
            html.Div([
                html.Button("🔄 Actualiser", id="refresh-btn", 
                           className="btn btn-primary mb-3")
            ], className="col-md-3"),
            
            html.Div([
                html.Button("📊 Connecter Instagram", id="connect-ig-btn", 
                           className="btn btn-outline-primary me-2 mb-3"),
                html.Button("🎵 Connecter TikTok", id="connect-tt-btn", 
                           className="btn btn-outline-dark mb-3")
            ], className="col-md-3")
        ], className="row mb-4"),
        
        # Graphiques principaux
        html.Div([
            html.Div([
                dcc.Graph(id="followers-chart")
            ], className="col-md-6"),
            
            html.Div([
                dcc.Graph(id="engagement-chart")
            ], className="col-md-6")
        ], className="row mb-4"),
        
        # Graphiques secondaires
        html.Div([
            html.Div([
                dcc.Graph(id="growth-indicator")
            ], className="col-md-4"),
            
            html.Div([
                dcc.Graph(id="best-times-chart")
            ], className="col-md-8")
        ], className="row mb-4"),
        
        # Graphiques avancés
        html.Div([
            html.Div([
                dcc.Graph(id="top-posts-chart")
            ], className="col-md-6"),
            
            html.Div([
                dcc.Graph(id="content-performance-chart")
            ], className="col-md-6")
        ], className="row mb-4"),
        
        # Comparaison plateformes
        html.Div([
            html.Div([
                dcc.Graph(id="platform-comparison-chart")
            ], className="col-md-12")
        ], className="row mb-4"),
        
        # Recommandations
        html.Div([
            html.H3("💡 Recommandations", className="mb-3"),
            html.Div(id="recommendations", className="alert alert-info")
        ], className="row")
    ], className="container-fluid")
], className="min-vh-100 bg-light")


# Les callbacks sont maintenant dans dashboard_callbacks.py


if __name__ == "__main__":
    app.run_server(
        host=settings.DASH_HOST,
        port=settings.DASH_PORT,
        debug=settings.DEBUG
    )