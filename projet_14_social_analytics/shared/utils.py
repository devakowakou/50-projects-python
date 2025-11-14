"""Utilitaires partagés pour le projet."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd


def calculate_engagement_rate(likes: int, comments: int, shares: int, 
                            saves: int, followers: int) -> float:
    """Calculer le taux d'engagement d'un post."""
    if followers == 0:
        return 0.0
    
    total_interactions = likes + comments + shares + saves
    return (total_interactions / followers) * 100


def calculate_reach_rate(reach: int, followers: int) -> float:
    """Calculer le taux de reach."""
    if followers == 0:
        return 0.0
    
    return (reach / followers) * 100


def calculate_growth_rate(current: int, previous: int) -> float:
    """Calculer le taux de croissance."""
    if previous == 0:
        return 0.0
    
    return ((current - previous) / previous) * 100


def get_best_posting_times(posts_data: List[Dict]) -> Dict[str, int]:
    """Analyser les meilleures heures de publication."""
    if not posts_data:
        return {}
    
    df = pd.DataFrame(posts_data)
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    df['engagement'] = df['likes_count'] + df['comments_count'] + df['shares_count']
    
    # Grouper par heure et calculer l'engagement moyen
    hourly_engagement = df.groupby('hour')['engagement'].mean().to_dict()
    
    # Retourner les heures triées par engagement
    return dict(sorted(hourly_engagement.items(), key=lambda x: x[1], reverse=True))


def get_top_posts(posts_data: List[Dict], limit: int = 10) -> List[Dict]:
    """Obtenir les meilleurs posts par engagement."""
    if not posts_data:
        return []
    
    # Calculer l'engagement total pour chaque post
    for post in posts_data:
        post['total_engagement'] = (
            post.get('likes_count', 0) + 
            post.get('comments_count', 0) + 
            post.get('shares_count', 0) +
            post.get('saves_count', 0)
        )
    
    # Trier par engagement et retourner le top
    sorted_posts = sorted(posts_data, key=lambda x: x['total_engagement'], reverse=True)
    return sorted_posts[:limit]


def analyze_content_performance(posts_data: List[Dict]) -> Dict[str, float]:
    """Analyser la performance par type de contenu."""
    if not posts_data:
        return {}
    
    df = pd.DataFrame(posts_data)
    df['engagement'] = df['likes_count'] + df['comments_count'] + df['shares_count']
    
    # Grouper par type de média
    performance_by_type = df.groupby('media_type')['engagement'].mean().to_dict()
    
    return performance_by_type


def format_number(number: int) -> str:
    """Formater un nombre pour l'affichage (K, M, B)."""
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return str(number)


def get_date_range(days: int = 30) -> tuple:
    """Obtenir une plage de dates (fin, début)."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def validate_instagram_token(token: str) -> bool:
    """Valider un token Instagram (placeholder)."""
    # TODO: Implémenter la validation réelle avec l'API Instagram
    return len(token) > 10


def validate_tiktok_token(token: str) -> bool:
    """Valider un token TikTok (placeholder)."""
    # TODO: Implémenter la validation réelle avec l'API TikTok
    return len(token) > 10


def generate_recommendations(account_data: Dict) -> List[str]:
    """Générer des recommandations basées sur les données."""
    recommendations = []
    
    # Analyse du taux d'engagement
    engagement_rate = account_data.get('engagement_rate', 0)
    if engagement_rate < 2.0:
        recommendations.append("🔥 Votre taux d'engagement est faible. Essayez de publier du contenu plus interactif.")
    elif engagement_rate > 5.0:
        recommendations.append("🎉 Excellent taux d'engagement ! Continuez sur cette lancée.")
    
    # Analyse de la fréquence de publication
    posts_per_week = account_data.get('posts_per_week', 0)
    if posts_per_week < 3:
        recommendations.append("📅 Publiez plus régulièrement (3-5 posts par semaine recommandés).")
    elif posts_per_week > 10:
        recommendations.append("⚠️ Attention à ne pas sur-publier, cela peut réduire l'engagement.")
    
    # Analyse des heures de publication
    best_hours = account_data.get('best_hours', [])
    if best_hours:
        top_hour = best_hours[0]
        recommendations.append(f"⏰ Votre meilleure heure de publication est {top_hour}h.")
    
    return recommendations