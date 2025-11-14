"""Composants de graphiques pour le dashboard."""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List


def create_followers_chart(data: Dict) -> go.Figure:
    """Créer le graphique d'évolution des followers."""
    if not data.get("dates") or not data.get("followers"):
        return go.Figure().add_annotation(text="Aucune donnée disponible", 
                                        xref="paper", yref="paper", x=0.5, y=0.5)
    
    fig = px.line(
        x=data["dates"], 
        y=data["followers"],
        title="📈 Évolution des Followers",
        labels={"x": "Date", "y": "Nombre de followers"}
    )
    
    fig.update_traces(line_color="#1f77b4", line_width=3)
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        title_font_size=16
    )
    
    return fig


def create_engagement_chart(data: Dict) -> go.Figure:
    """Créer le graphique d'engagement."""
    if not data.get("dates") or not data.get("engagement"):
        return go.Figure().add_annotation(text="Aucune donnée disponible", 
                                        xref="paper", yref="paper", x=0.5, y=0.5)
    
    fig = px.bar(
        x=data["dates"], 
        y=data["engagement"],
        title="💝 Engagement Quotidien",
        labels={"x": "Date", "y": "Engagement moyen"}
    )
    
    fig.update_traces(marker_color="#ff7f0e")
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        title_font_size=16
    )
    
    return fig


def create_top_posts_chart(posts: List[Dict]) -> go.Figure:
    """Créer le graphique des meilleurs posts."""
    if not posts:
        return go.Figure().add_annotation(text="Aucun post disponible", 
                                        xref="paper", yref="paper", x=0.5, y=0.5)
    
    # Prendre les 5 meilleurs posts
    top_5 = posts[:5]
    
    post_names = [f"Post {i+1}" for i in range(len(top_5))]
    likes = [post.get("likes_count", 0) for post in top_5]
    comments = [post.get("comments_count", 0) for post in top_5]
    shares = [post.get("shares_count", 0) for post in top_5]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name="Likes",
        x=post_names,
        y=likes,
        marker_color="#1f77b4"
    ))
    
    fig.add_trace(go.Bar(
        name="Comments",
        x=post_names,
        y=comments,
        marker_color="#ff7f0e"
    ))
    
    fig.add_trace(go.Bar(
        name="Shares",
        x=post_names,
        y=shares,
        marker_color="#2ca02c"
    ))
    
    fig.update_layout(
        title="🏆 Top 5 Posts par Engagement",
        xaxis_title="Posts",
        yaxis_title="Interactions",
        barmode="group",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        title_font_size=16
    )
    
    return fig


def create_best_times_chart(best_times: Dict) -> go.Figure:
    """Créer le graphique des meilleures heures."""
    if not best_times:
        return go.Figure().add_annotation(text="Aucune donnée disponible", 
                                        xref="paper", yref="paper", x=0.5, y=0.5)
    
    hours = list(best_times.keys())
    engagement = list(best_times.values())
    
    fig = px.bar(
        x=hours,
        y=engagement,
        title="⏰ Meilleures Heures de Publication",
        labels={"x": "Heure", "y": "Engagement moyen"}
    )
    
    fig.update_traces(marker_color="#d62728")
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        title_font_size=16,
        xaxis=dict(tickmode='linear')
    )
    
    return fig


def create_content_performance_chart(performance: Dict) -> go.Figure:
    """Créer le graphique de performance par type de contenu."""
    if not performance:
        return go.Figure().add_annotation(text="Aucune donnée disponible", 
                                        xref="paper", yref="paper", x=0.5, y=0.5)
    
    content_types = list(performance.keys())
    avg_engagement = [performance[ct]["avg_engagement"] for ct in content_types]
    total_posts = [performance[ct]["total_posts"] for ct in content_types]
    
    # Créer un graphique combiné
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Engagement Moyen", "Nombre de Posts"),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Engagement moyen
    fig.add_trace(
        go.Bar(x=content_types, y=avg_engagement, name="Engagement", 
               marker_color="#9467bd"),
        row=1, col=1
    )
    
    # Nombre de posts
    fig.add_trace(
        go.Bar(x=content_types, y=total_posts, name="Posts", 
               marker_color="#8c564b"),
        row=1, col=2
    )
    
    fig.update_layout(
        title="📊 Performance par Type de Contenu",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        title_font_size=16,
        showlegend=False
    )
    
    return fig


def create_growth_trend_chart(metrics: Dict) -> go.Figure:
    """Créer un indicateur de croissance."""
    growth_rate = metrics.get("growth_rate", 0)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=growth_rate,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "📈 Taux de Croissance (%)"},
        delta={'reference': 0},
        gauge={
            'axis': {'range': [-10, 10]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-10, -2], 'color': "lightgray"},
                {'range': [-2, 2], 'color': "gray"},
                {'range': [2, 10], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 5
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="white",
        font=dict(size=12),
        height=300
    )
    
    return fig


def create_platform_comparison_chart(instagram_data: Dict, tiktok_data: Dict) -> go.Figure:
    """Créer un graphique de comparaison entre plateformes."""
    platforms = ["Instagram", "TikTok"]
    followers = [
        instagram_data.get("followers", 0),
        tiktok_data.get("followers", 0)
    ]
    engagement = [
        instagram_data.get("engagement_rate", 0),
        tiktok_data.get("engagement_rate", 0)
    ]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Followers", "Taux d'Engagement (%)"),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    fig.add_trace(
        go.Bar(x=platforms, y=followers, name="Followers", 
               marker_color=["#E4405F", "#000000"]),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=platforms, y=engagement, name="Engagement", 
               marker_color=["#E4405F", "#000000"]),
        row=1, col=2
    )
    
    fig.update_layout(
        title="📱 Comparaison Instagram vs TikTok",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        title_font_size=16,
        showlegend=False
    )
    
    return fig