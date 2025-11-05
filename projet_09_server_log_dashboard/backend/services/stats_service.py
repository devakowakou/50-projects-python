from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from database import LogRecord

class StatsService:
    """Service pour calculer les statistiques"""
    
    @staticmethod
    def get_overview(db: Session, 
                     start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None) -> Dict:
        """Statistiques globales"""
        query = db.query(LogRecord)
        
        # Filtrage par date si fourni
        if start_date:
            query = query.filter(LogRecord.timestamp >= start_date)
        if end_date:
            query = query.filter(LogRecord.timestamp <= end_date)
        
        total = query.count()
        unique_ips = query.with_entities(func.count(distinct(LogRecord.ip))).scalar()
        errors_4xx = query.filter(
            LogRecord.status_code >= 400, 
            LogRecord.status_code < 500
        ).count()
        errors_5xx = query.filter(LogRecord.status_code >= 500).count()
        
        # Temps de réponse moyen
        avg_time = query.with_entities(
            func.avg(LogRecord.response_time)
        ).scalar()
        
        # Plage de dates
        first_log = query.order_by(LogRecord.timestamp.asc()).first()
        last_log = query.order_by(LogRecord.timestamp.desc()).first()
        
        return {
            'total_requests': total,
            'unique_ips': unique_ips or 0,
            'errors_4xx': errors_4xx,
            'errors_5xx': errors_5xx,
            'error_rate': round((errors_4xx + errors_5xx) / total * 100, 2) if total > 0 else 0,
            'avg_response_time': round(float(avg_time), 2) if avg_time else None,
            'date_range': {
                'start': first_log.timestamp.isoformat() if first_log else None,
                'end': last_log.timestamp.isoformat() if last_log else None
            }
        }
    
    @staticmethod
    def get_top_urls(db: Session, limit: int = 10) -> List[Dict]:
        """URLs les plus visitées"""
        results = db.query(
            LogRecord.url,
            func.count(LogRecord.id).label('count')
        ).group_by(LogRecord.url).order_by(func.count(LogRecord.id).desc()).limit(limit).all()
        
        return [{'url': url, 'count': count} for url, count in results]
    
    @staticmethod
    def get_status_distribution(db: Session) -> List[Dict]:
        """Distribution des codes HTTP"""
        results = db.query(
            LogRecord.status_code,
            func.count(LogRecord.id).label('count')
        ).group_by(LogRecord.status_code).order_by(LogRecord.status_code).all()
        
        return [{'status': status, 'count': count} for status, count in results]
    
    @staticmethod
    def get_requests_by_hour(db: Session, days: int = 7) -> List[Dict]:
        """Requêtes par heure sur les N derniers jours"""
        start_date = datetime.now() - timedelta(days=days)
        
        results = db.query(
            func.strftime('%Y-%m-%d %H:00:00', LogRecord.timestamp).label('hour'),
            func.count(LogRecord.id).label('count')
        ).filter(
            LogRecord.timestamp >= start_date
        ).group_by('hour').order_by('hour').all()
        
        return [{'hour': hour, 'count': count} for hour, count in results]
