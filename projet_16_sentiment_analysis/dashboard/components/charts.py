"""Composants de graphiques pour le dashboard."""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64


def create_sentiment_pie_chart(sentiment_stats: Dict) -> go.Figure:
    """Graphique en camembert des sentiments."""
    if not sentiment_stats:
        return go.Figure().add_annotation(text="Aucune donnée", x=0.5, y=0.5)
    
    sentiments = list(sentiment_stats.keys())
    counts = [sentiment_stats[s]["count"] for s in sentiments]
    
    colors = {
        "positive": "#2E8B57",
        "negative": "#DC143C", 
        "neutral": "#FFD700"
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=sentiments,
        values=counts,
        marker_colors=[colors.get(s, "#808080") for s in sentiments],
        textinfo='label+percent',
        textfont_size=12
    )])
    
    fig.update_layout(
        title="Distribution des Sentiments",
        font=dict(size=14),
        showlegend=True
    )
    
    return fig


def create_rating_histogram(reviews: List[Dict]) -> go.Figure:
    """Histogramme des notes."""
    if not reviews:
        return go.Figure().add_annotation(text="Aucune donnée", x=0.5, y=0.5)
    
    ratings = [r.get("rating") for r in reviews if r.get("rating")]
    
    if not ratings:
        return go.Figure().add_annotation(text="Aucune note disponible", x=0.5, y=0.5)
    
    fig = px.histogram(
        x=ratings,
        nbins=5,
        title="Distribution des Notes",
        labels={"x": "Note", "y": "Nombre d'avis"},
        color_discrete_sequence=["#1f77b4"]
    )
    
    fig.update_layout(
        xaxis=dict(tickmode='linear', tick0=1, dtick=1),
        bargap=0.1
    )
    
    return fig


def create_sentiment_by_rating(reviews: List[Dict]) -> go.Figure:
    """Sentiment par note."""
    if not reviews:
        return go.Figure().add_annotation(text="Aucune donnée", x=0.5, y=0.5)
    
    # Préparer les données
    data = []
    for review in reviews:
        if review.get("rating") and review.get("consensus_sentiment"):
            data.append({
                "rating": review["rating"],
                "sentiment": review["consensus_sentiment"]
            })
    
    if not data:
        return go.Figure().add_annotation(text="Aucune donnée sentiment/rating", x=0.5, y=0.5)
    
    df = pd.DataFrame(data)
    
    # Compter les sentiments par note
    sentiment_counts = df.groupby(["rating", "sentiment"]).size().reset_index(name="count")
    
    fig = px.bar(
        sentiment_counts,
        x="rating",
        y="count",
        color="sentiment",
        title="Sentiment par Note",
        labels={"rating": "Note", "count": "Nombre d'avis"},
        color_discrete_map={
            "positive": "#2E8B57",
            "negative": "#DC143C",
            "neutral": "#FFD700"
        }
    )
    
    return fig


def create_platform_comparison(reviews: List[Dict]) -> go.Figure:
    """Comparaison entre plateformes."""
    if not reviews:
        return go.Figure().add_annotation(text="Aucune donnée", x=0.5, y=0.5)
    
    # Grouper par plateforme
    platform_data = {}
    for review in reviews:
        platform = review.get("platform", "unknown")
        if platform not in platform_data:
            platform_data[platform] = {"positive": 0, "negative": 0, "neutral": 0, "total": 0}
        
        sentiment = review.get("consensus_sentiment", "neutral")
        platform_data[platform][sentiment] += 1
        platform_data[platform]["total"] += 1
    
    # Créer le graphique
    platforms = list(platform_data.keys())
    positive = [platform_data[p]["positive"] for p in platforms]
    negative = [platform_data[p]["negative"] for p in platforms]
    neutral = [platform_data[p]["neutral"] for p in platforms]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(name="Positif", x=platforms, y=positive, marker_color="#2E8B57"))
    fig.add_trace(go.Bar(name="Négatif", x=platforms, y=negative, marker_color="#DC143C"))
    fig.add_trace(go.Bar(name="Neutre", x=platforms, y=neutral, marker_color="#FFD700"))
    
    fig.update_layout(
        title="Comparaison des Sentiments par Plateforme",
        xaxis_title="Plateforme",
        yaxis_title="Nombre d'avis",
        barmode="stack"
    )
    
    return fig


def create_confidence_scatter(reviews: List[Dict]) -> go.Figure:
    """Graphique de confiance vs sentiment."""
    if not reviews:
        return go.Figure().add_annotation(text="Aucune donnée", x=0.5, y=0.5)
    
    data = []
    for review in reviews:
        if review.get("consensus_confidence") and review.get("consensus_sentiment"):
            data.append({
                "confidence": review["consensus_confidence"],
                "sentiment": review["consensus_sentiment"],
                "rating": review.get("rating", 3)
            })
    
    if not data:
        return go.Figure().add_annotation(text="Aucune donnée de confiance", x=0.5, y=0.5)
    
    df = pd.DataFrame(data)
    
    fig = px.scatter(
        df,
        x="confidence",
        y="sentiment",
        size="rating",
        color="sentiment",
        title="Confiance des Prédictions",
        labels={"confidence": "Confiance", "sentiment": "Sentiment"},
        color_discrete_map={
            "positive": "#2E8B57",
            "negative": "#DC143C",
            "neutral": "#FFD700"
        }
    )
    
    return fig


def create_wordcloud_image(texts: List[str]) -> str:
    """Créer un nuage de mots et retourner l'image en base64."""
    if not texts:
        return ""
    
    # Combiner tous les textes
    combined_text = " ".join(texts)
    
    if len(combined_text.strip()) < 10:
        return ""
    
    try:
        # Créer le WordCloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="white",
            max_words=100,
            colormap="viridis"
        ).generate(combined_text)
        
        # Convertir en image
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        
        # Sauvegarder en base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
        img_buffer.seek(0)
        
        img_base64 = base64.b64encode(img_buffer.read()).decode()
        plt.close()
        
        return f"data:image/png;base64,{img_base64}"
        
    except Exception as e:
        print(f"Erreur WordCloud: {e}")
        return ""


def create_metrics_cards(sentiment_stats: Dict, total_reviews: int) -> Dict:
    """Créer les métriques principales."""
    if not sentiment_stats:
        return {
            "total_reviews": 0,
            "positive_rate": 0,
            "negative_rate": 0,
            "avg_confidence": 0
        }
    
    positive_count = sentiment_stats.get("positive", {}).get("count", 0)
    negative_count = sentiment_stats.get("negative", {}).get("count", 0)
    
    # Calculer les taux
    positive_rate = (positive_count / total_reviews * 100) if total_reviews > 0 else 0
    negative_rate = (negative_count / total_reviews * 100) if total_reviews > 0 else 0
    
    # Confiance moyenne
    confidences = [stats.get("avg_confidence", 0) for stats in sentiment_stats.values()]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    return {
        "total_reviews": total_reviews,
        "positive_rate": positive_rate,
        "negative_rate": negative_rate,
        "avg_confidence": avg_confidence
    }


def create_timeline_chart(reviews: List[Dict]) -> go.Figure:
    """Graphique d'évolution temporelle des sentiments."""
    if not reviews:
        return go.Figure().add_annotation(text="Aucune donnée", x=0.5, y=0.5)
    
    # Préparer les données avec dates
    data = []
    for review in reviews:
        date = review.get("created_at") or review.get("scraped_at")
        sentiment = review.get("consensus_sentiment")
        
        if date and sentiment:
            data.append({
                "date": pd.to_datetime(date).date(),
                "sentiment": sentiment
            })
    
    if not data:
        return go.Figure().add_annotation(text="Aucune donnée temporelle", x=0.5, y=0.5)
    
    df = pd.DataFrame(data)
    
    # Grouper par date et sentiment
    timeline = df.groupby(["date", "sentiment"]).size().reset_index(name="count")
    
    fig = px.line(
        timeline,
        x="date",
        y="count",
        color="sentiment",
        title="Évolution des Sentiments dans le Temps",
        labels={"date": "Date", "count": "Nombre d'avis"},
        color_discrete_map={
            "positive": "#2E8B57",
            "negative": "#DC143C",
            "neutral": "#FFD700"
        }
    )
    
    return fig