"""Endpoints d'analyse des données sociales."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from shared.database import get_db, SocialAccount, SocialInsight, Post
from shared.utils import calculate_engagement_rate, calculate_growth_rate, get_top_posts, get_best_posting_times

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/metrics")
async def get_metrics(
    platform: Optional[str] = Query(None, description="Platform filter: instagram, tiktok, or all"),
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """Récupérer les métriques principales."""
    
    # Date de début
    start_date = datetime.now() - timedelta(days=days)
    
    # Query de base
    query = db.query(SocialInsight).join(SocialAccount).filter(
        SocialInsight.date >= start_date
    )
    
    if platform and platform != "all":
        query = query.filter(SocialAccount.platform == platform)
    
    insights = query.all()
    
    if not insights:
        return {"error": "No data found"}
    
    # Calculer les métriques
    latest_insights = db.query(SocialInsight).join(SocialAccount).filter(
        SocialInsight.date >= datetime.now() - timedelta(days=1)
    )
    
    if platform and platform != "all":
        latest_insights = latest_insights.filter(SocialAccount.platform == platform)
    
    latest = latest_insights.all()
    
    total_followers = sum(insight.followers_count or 0 for insight in latest)
    total_reach = sum(insight.reach or 0 for insight in latest)
    total_impressions = sum(insight.impressions or 0 for insight in latest)
    
    # Calculer la croissance
    yesterday_insights = db.query(SocialInsight).join(SocialAccount).filter(
        SocialInsight.date >= datetime.now() - timedelta(days=2),
        SocialInsight.date < datetime.now() - timedelta(days=1)
    )
    
    if platform and platform != "all":
        yesterday_insights = yesterday_insights.filter(SocialAccount.platform == platform)
    
    yesterday = yesterday_insights.all()
    yesterday_followers = sum(insight.followers_count or 0 for insight in yesterday)
    
    growth_rate = calculate_growth_rate(total_followers, yesterday_followers)
    
    return {
        "followers": total_followers,
        "reach": total_reach,
        "impressions": total_impressions,
        "growth_rate": round(growth_rate, 2),
        "engagement_rate": 4.2,  # Calculé dynamiquement plus tard
        "period_days": days,
        "platform": platform or "all"
    }


@router.get("/followers-evolution")
async def get_followers_evolution(
    platform: Optional[str] = Query(None),
    days: int = Query(30),
    db: Session = Depends(get_db)
):
    """Évolution des followers dans le temps."""
    
    start_date = datetime.now() - timedelta(days=days)
    
    query = db.query(SocialInsight).join(SocialAccount).filter(
        SocialInsight.date >= start_date
    ).order_by(SocialInsight.date)
    
    if platform and platform != "all":
        query = query.filter(SocialAccount.platform == platform)
    
    insights = query.all()
    
    # Grouper par date
    daily_data = {}
    for insight in insights:
        date_str = insight.date.strftime("%Y-%m-%d")
        if date_str not in daily_data:
            daily_data[date_str] = 0
        daily_data[date_str] += insight.followers_count or 0
    
    return {
        "dates": list(daily_data.keys()),
        "followers": list(daily_data.values()),
        "platform": platform or "all"
    }


@router.get("/engagement-analysis")
async def get_engagement_analysis(
    platform: Optional[str] = Query(None),
    days: int = Query(30),
    db: Session = Depends(get_db)
):
    """Analyse de l'engagement."""
    
    start_date = datetime.now() - timedelta(days=days)
    
    query = db.query(Post).join(SocialAccount).filter(
        Post.timestamp >= start_date
    )
    
    if platform and platform != "all":
        query = query.filter(SocialAccount.platform == platform)
    
    posts = query.all()
    
    if not posts:
        return {"error": "No posts found"}
    
    # Calculer l'engagement par jour
    daily_engagement = {}
    for post in posts:
        date_str = post.timestamp.strftime("%Y-%m-%d")
        if date_str not in daily_engagement:
            daily_engagement[date_str] = []
        
        engagement = (
            (post.likes_count or 0) + 
            (post.comments_count or 0) + 
            (post.shares_count or 0)
        )
        daily_engagement[date_str].append(engagement)
    
    # Moyenne par jour
    avg_daily_engagement = {
        date: sum(engagements) / len(engagements)
        for date, engagements in daily_engagement.items()
    }
    
    return {
        "dates": list(avg_daily_engagement.keys()),
        "engagement": list(avg_daily_engagement.values()),
        "platform": platform or "all"
    }


@router.get("/top-posts")
async def get_top_posts_endpoint(
    platform: Optional[str] = Query(None),
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    """Récupérer les meilleurs posts."""
    
    query = db.query(Post).join(SocialAccount)
    
    if platform and platform != "all":
        query = query.filter(SocialAccount.platform == platform)
    
    posts = query.all()
    
    # Convertir en dictionnaires
    posts_data = []
    for post in posts:
        posts_data.append({
            "id": post.id,
            "platform_post_id": post.platform_post_id,
            "caption": post.caption,
            "media_type": post.media_type,
            "timestamp": post.timestamp.isoformat(),
            "likes_count": post.likes_count or 0,
            "comments_count": post.comments_count or 0,
            "shares_count": post.shares_count or 0,
            "saves_count": post.saves_count or 0,
            "reach": post.reach,
            "impressions": post.impressions
        })
    
    top_posts = get_top_posts(posts_data, limit)
    
    return {
        "posts": top_posts,
        "platform": platform or "all",
        "total_analyzed": len(posts_data)
    }


@router.get("/best-times")
async def get_best_posting_times(
    platform: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Analyser les meilleures heures de publication."""
    
    query = db.query(Post).join(SocialAccount)
    
    if platform and platform != "all":
        query = query.filter(SocialAccount.platform == platform)
    
    posts = query.all()
    
    if not posts:
        return {"error": "No posts found"}
    
    # Convertir en dictionnaires
    posts_data = []
    for post in posts:
        posts_data.append({
            "timestamp": post.timestamp.isoformat(),
            "likes_count": post.likes_count or 0,
            "comments_count": post.comments_count or 0,
            "shares_count": post.shares_count or 0
        })
    
    best_times = get_best_posting_times(posts_data)
    
    return {
        "best_hours": best_times,
        "platform": platform or "all",
        "total_posts_analyzed": len(posts_data)
    }


@router.get("/content-performance")
async def get_content_performance(
    platform: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Analyser la performance par type de contenu."""
    
    query = db.query(Post).join(SocialAccount)
    
    if platform and platform != "all":
        query = query.filter(SocialAccount.platform == platform)
    
    posts = query.all()
    
    if not posts:
        return {"error": "No posts found"}
    
    # Grouper par type de média
    performance_by_type = {}
    for post in posts:
        media_type = post.media_type or "UNKNOWN"
        if media_type not in performance_by_type:
            performance_by_type[media_type] = {
                "total_posts": 0,
                "total_engagement": 0,
                "avg_likes": 0,
                "avg_comments": 0,
                "avg_shares": 0
            }
        
        engagement = (
            (post.likes_count or 0) + 
            (post.comments_count or 0) + 
            (post.shares_count or 0)
        )
        
        performance_by_type[media_type]["total_posts"] += 1
        performance_by_type[media_type]["total_engagement"] += engagement
        performance_by_type[media_type]["avg_likes"] += post.likes_count or 0
        performance_by_type[media_type]["avg_comments"] += post.comments_count or 0
        performance_by_type[media_type]["avg_shares"] += post.shares_count or 0
    
    # Calculer les moyennes
    for media_type in performance_by_type:
        total_posts = performance_by_type[media_type]["total_posts"]
        performance_by_type[media_type]["avg_engagement"] = (
            performance_by_type[media_type]["total_engagement"] / total_posts
        )
        performance_by_type[media_type]["avg_likes"] /= total_posts
        performance_by_type[media_type]["avg_comments"] /= total_posts
        performance_by_type[media_type]["avg_shares"] /= total_posts
    
    return {
        "performance_by_type": performance_by_type,
        "platform": platform or "all"
    }