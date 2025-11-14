"""Callbacks pour le dashboard principal."""

from dash import Input, Output, callback, html
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.config import settings
from frontend.components.charts import (
    create_followers_chart, create_engagement_chart, create_top_posts_chart,
    create_best_times_chart, create_content_performance_chart, 
    create_growth_trend_chart, create_platform_comparison_chart
)

API_BASE_URL = f"http://{settings.API_HOST}:{settings.API_PORT}"


def fetch_api_data(endpoint: str, params: dict = None):
    """Récupérer des données depuis l'API."""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection Error: {str(e)}"}


@callback(
    Output("connection-status", "children"),
    Input("refresh-btn", "n_clicks")
)
def update_connection_status(n_clicks):
    """Mettre à jour le statut de connexion."""
    auth_status = fetch_api_data("/auth/status")
    
    if "error" in auth_status:
        return html.Div([
            html.Span("🔴 API non disponible", className="badge bg-danger me-2"),
            html.Small("Vérifiez que le backend est démarré", className="text-muted")
        ])
    
    if auth_status.get("authenticated"):
        accounts = auth_status.get("accounts", [])
        badges = []
        for account in accounts:
            platform = account["platform"]
            username = account["username"]
            color = "success" if platform == "instagram" else "dark"
            icon = "📷" if platform == "instagram" else "🎵"
            badges.append(
                html.Span(f"{icon} @{username}", className=f"badge bg-{color} me-2")
            )
        return html.Div(badges)
    else:
        return html.Div([
            html.Span("⚪ Mode Démo", className="badge bg-secondary me-2"),
            html.Small("Connectez vos comptes pour des données réelles", className="text-muted")
        ])


@callback(
    Output("metrics-cards", "children"),
    [Input("platform-dropdown", "value"),
     Input("days-dropdown", "value"),
     Input("refresh-btn", "n_clicks")]
)
def update_metrics(platform, days, n_clicks):
    """Mettre à jour les cartes de métriques."""
    
    # Récupérer les métriques depuis l'API
    metrics = fetch_api_data("/analytics/metrics", {"platform": platform, "days": days})
    
    if "error" in metrics:
        # Données de fallback
        metrics = {
            "followers": 15420,
            "reach": 89340,
            "impressions": 125680,
            "growth_rate": 2.3,
            "engagement_rate": 4.2
        }
    
    cards = [
        html.Div([
            html.Div([
                html.H4("👥 Followers", className="card-title"),
                html.H2(f"{metrics.get('followers', 0):,}", className="text-primary"),
                html.Small(f"+{metrics.get('growth_rate', 0):.1f}% vs hier", 
                          className="text-success" if metrics.get('growth_rate', 0) > 0 else "text-danger")
            ], className="card-body text-center")
        ], className="card col-md-3 mx-1"),
        
        html.Div([
            html.Div([
                html.H4("💝 Engagement", className="card-title"),
                html.H2(f"{metrics.get('engagement_rate', 0):.1f}%", className="text-info"),
                html.Small("Taux moyen", className="text-muted")
            ], className="card-body text-center")
        ], className="card col-md-3 mx-1"),
        
        html.Div([
            html.Div([
                html.H4("👀 Reach", className="card-title"),
                html.H2(f"{metrics.get('reach', 0):,}", className="text-warning"),
                html.Small(f"Sur {days} jours", className="text-muted")
            ], className="card-body text-center")
        ], className="card col-md-3 mx-1"),
        
        html.Div([
            html.Div([
                html.H4("📊 Impressions", className="card-title"),
                html.H2(f"{metrics.get('impressions', 0):,}", className="text-secondary"),
                html.Small(f"Sur {days} jours", className="text-muted")
            ], className="card-body text-center")
        ], className="card col-md-3 mx-1")
    ]
    
    return cards


@callback(
    Output("followers-chart", "figure"),
    [Input("platform-dropdown", "value"),
     Input("days-dropdown", "value"),
     Input("refresh-btn", "n_clicks")]
)
def update_followers_chart(platform, days, n_clicks):
    """Graphique d'évolution des followers."""
    data = fetch_api_data("/analytics/followers-evolution", {"platform": platform, "days": days})
    return create_followers_chart(data)


@callback(
    Output("engagement-chart", "figure"),
    [Input("platform-dropdown", "value"),
     Input("days-dropdown", "value"),
     Input("refresh-btn", "n_clicks")]
)
def update_engagement_chart(platform, days, n_clicks):
    """Graphique d'engagement."""
    data = fetch_api_data("/analytics/engagement-analysis", {"platform": platform, "days": days})
    return create_engagement_chart(data)


@callback(
    Output("growth-indicator", "figure"),
    [Input("platform-dropdown", "value"),
     Input("days-dropdown", "value"),
     Input("refresh-btn", "n_clicks")]
)
def update_growth_indicator(platform, days, n_clicks):
    """Indicateur de croissance."""
    metrics = fetch_api_data("/analytics/metrics", {"platform": platform, "days": days})
    return create_growth_trend_chart(metrics)


@callback(
    Output("best-times-chart", "figure"),
    [Input("platform-dropdown", "value"),
     Input("refresh-btn", "n_clicks")]
)
def update_best_times_chart(platform, n_clicks):
    """Graphique des meilleures heures."""
    data = fetch_api_data("/analytics/best-times", {"platform": platform})
    best_times = data.get("best_hours", {})
    return create_best_times_chart(best_times)


@callback(
    Output("top-posts-chart", "figure"),
    [Input("platform-dropdown", "value"),
     Input("refresh-btn", "n_clicks")]
)
def update_top_posts_chart(platform, n_clicks):
    """Graphique des meilleurs posts."""
    data = fetch_api_data("/analytics/top-posts", {"platform": platform, "limit": 5})
    posts = data.get("posts", [])
    return create_top_posts_chart(posts)


@callback(
    Output("content-performance-chart", "figure"),
    [Input("platform-dropdown", "value"),
     Input("refresh-btn", "n_clicks")]
)
def update_content_performance_chart(platform, n_clicks):
    """Graphique de performance par type de contenu."""
    data = fetch_api_data("/analytics/content-performance", {"platform": platform})
    performance = data.get("performance_by_type", {})
    return create_content_performance_chart(performance)


@callback(
    Output("platform-comparison-chart", "figure"),
    [Input("days-dropdown", "value"),
     Input("refresh-btn", "n_clicks")]
)
def update_platform_comparison_chart(days, n_clicks):
    """Graphique de comparaison entre plateformes."""
    instagram_data = fetch_api_data("/analytics/metrics", {"platform": "instagram", "days": days})
    tiktok_data = fetch_api_data("/analytics/metrics", {"platform": "tiktok", "days": days})
    return create_platform_comparison_chart(instagram_data, tiktok_data)


@callback(
    Output("recommendations", "children"),
    [Input("platform-dropdown", "value"),
     Input("refresh-btn", "n_clicks")]
)
def update_recommendations(platform, n_clicks):
    """Mettre à jour les recommandations."""
    
    # Récupérer les données pour générer des recommandations
    metrics = fetch_api_data("/analytics/metrics", {"platform": platform, "days": 30})
    
    recommendations = []
    
    # Analyse du taux d'engagement
    engagement_rate = metrics.get("engagement_rate", 0)
    if engagement_rate < 2.0:
        recommendations.append("🔥 Votre taux d'engagement est faible. Essayez de publier du contenu plus interactif.")
    elif engagement_rate > 5.0:
        recommendations.append("🎉 Excellent taux d'engagement ! Continuez sur cette lancée.")
    
    # Analyse de la croissance
    growth_rate = metrics.get("growth_rate", 0)
    if growth_rate < 0:
        recommendations.append("📉 Votre audience diminue. Analysez vos derniers posts et adaptez votre stratégie.")
    elif growth_rate > 5:
        recommendations.append("🚀 Croissance excellente ! Identifiez ce qui fonctionne et reproduisez-le.")
    
    # Recommandations générales
    if platform == "instagram":
        recommendations.append("📷 Instagram: Utilisez des Stories et Reels pour augmenter votre reach.")
    elif platform == "tiktok":
        recommendations.append("🎵 TikTok: Suivez les tendances et utilisez des hashtags populaires.")
    else:
        recommendations.append("📊 Diversifiez votre contenu entre les deux plateformes pour maximiser votre audience.")
    
    if not recommendations:
        recommendations.append("✅ Vos performances sont bonnes ! Continuez à publier régulièrement.")
    
    return html.Ul([html.Li(rec) for rec in recommendations])