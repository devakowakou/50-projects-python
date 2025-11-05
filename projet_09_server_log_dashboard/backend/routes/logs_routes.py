from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from backend.database import get_db, LogRecord
from backend.models.log_model import LogEntryResponse

router = APIRouter(prefix="/api/logs", tags=["logs"])

@router.get("/recent", response_model=List[LogEntryResponse])
def get_recent_logs(
    limit: int = Query(20, ge=1, le=100, description="Nombre de logs à retourner"),
    offset: int = Query(0, ge=0, description="Décalage pour pagination"),
    status_code: Optional[int] = Query(None, description="Filtrer par code HTTP"),
    db: Session = Depends(get_db)
):
    """Récupère les logs les plus récents"""
    query = db.query(LogRecord).order_by(LogRecord.timestamp.desc())
    
    if status_code:
        query = query.filter(LogRecord.status_code == status_code)
    
    logs = query.offset(offset).limit(limit).all()
    return logs

@router.get("/{log_id}", response_model=LogEntryResponse)
def get_log_by_id(log_id: int, db: Session = Depends(get_db)):
    """Récupère un log spécifique par son ID"""
    log = db.query(LogRecord).filter(LogRecord.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log non trouvé")
    return log

@router.get("/search/by-ip")
def search_by_ip(
    ip: str = Query(..., description="Adresse IP à rechercher"),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Recherche tous les logs d'une IP"""
    logs = db.query(LogRecord).filter(
        LogRecord.ip == ip
    ).order_by(LogRecord.timestamp.desc()).limit(limit).all()
    
    return {
        'ip': ip,
        'count': len(logs),
        'logs': logs
    }
