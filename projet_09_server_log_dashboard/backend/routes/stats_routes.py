from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from backend.database import get_db
from backend.services.stats_service import StatsService
from backend.models.log_model import StatsOverview

router = APIRouter(prefix="/api/stats", tags=["statistics"])

@router.get("/overview", response_model=StatsOverview)
def get_overview_stats(
    start_date: Optional[datetime] = Query(None, description="Date de début (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="Date de fin (ISO format)"),
    db: Session = Depends(get_db)
):
    """Statistiques globales du dashboard"""
    return StatsService.get_overview(db, start_date, end_date)

@router.get("/top-urls")
def get_top_urls(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Top des URLs les plus visitées"""
    return StatsService.get_top_urls(db, limit)

@router.get("/status-distribution")
def get_status_distribution(db: Session = Depends(get_db)):
    """Distribution des codes HTTP"""
    return StatsService.get_status_distribution(db)

@router.get("/requests-timeline")
def get_requests_timeline(
    days: int = Query(7, ge=1, le=30, description="Nombre de jours"),
    db: Session = Depends(get_db)
):
    """Timeline des requêtes par heure"""
    return StatsService.get_requests_by_hour(db, days)
