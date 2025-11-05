from fastapi import APIRouter, Depends, Query, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import csv
from io import StringIO
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from database import get_db, LogRecord
from models.log_model import LogEntryResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/logs", tags=["logs"])

@router.get("/recent", response_model=List[LogEntryResponse])
def get_recent_logs(
    limit: int = Query(20, ge=1, le=10000, description="Nombre de logs à retourner (max 10000)"),
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
    ip: str = Query(...),
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

@router.get("/export")
def export_logs(
    hours: int = Query(24, ge=1, le=720, description="Période en heures (max 30 jours)"),
    format: str = Query("json", description="Format d'export (json ou csv)"),
    db: Session = Depends(get_db)
):
    """Export de logs pour analyse externe (sans limite stricte)"""
    
    # Debug
    logger.info(f"📥 Export request: hours={hours}, format={format} (type: {type(format)})")
    
    # Normaliser le format en minuscules
    format = format.lower()
    
    # Validation manuelle
    if format not in ["json", "csv"]:
        logger.error(f"❌ Format invalide: {format}")
        raise HTTPException(status_code=422, detail=f"Format '{format}' invalide. Utilisez 'json' ou 'csv'")
    
    logger.info(f"✅ Format validé: {format}")
    
    cutoff = datetime.now() - timedelta(hours=hours)
    
    logs = db.query(LogRecord).filter(
        LogRecord.timestamp >= cutoff
    ).order_by(LogRecord.timestamp.desc()).all()
    
    if format == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['id', 'ip', 'timestamp', 'method', 'url', 'status_code', 'response_time', 'user_agent'])
        
        for log in logs:
            writer.writerow([
                log.id, 
                log.ip, 
                log.timestamp.isoformat(), 
                log.method,
                log.url, 
                log.status_code, 
                log.response_time, 
                log.user_agent
            ])
        
        csv_content = output.getvalue()
        return Response(
            content=csv_content, 
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=logs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
        )
    
    # JSON par défaut
    return {
        'total': len(logs),
        'period_hours': hours,
        'export_date': datetime.now().isoformat(),
        'logs': [
            {
                'id': log.id,
                'ip': log.ip,
                'timestamp': log.timestamp.isoformat(),
                'method': log.method,
                'url': log.url,
                'status_code': log.status_code,
                'response_time': log.response_time,
                'user_agent': log.user_agent
            }
            for log in logs
        ]
    }
