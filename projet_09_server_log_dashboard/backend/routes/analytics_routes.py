from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from backend.database import get_db, LogRecord
from backend.services.session_analyzer import SessionAnalyzer
from backend.ml.anomaly_detector import AnomalyDetector
from backend.scraper.website_analyzer import WebsiteAnalyzer

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

# Instances globales
session_analyzer = SessionAnalyzer()
anomaly_detector = AnomalyDetector()
website_analyzer = WebsiteAnalyzer()

@router.get("/sessions")
def analyze_sessions(
    hours: int = Query(24, ge=1, le=168, description="Période d'analyse en heures"),
    db: Session = Depends(get_db)
):
    """Analyse complète des sessions utilisateur"""
    cutoff = datetime.now() - timedelta(hours=hours)
    
    logs = db.query(LogRecord).filter(
        LogRecord.timestamp >= cutoff
    ).order_by(LogRecord.timestamp.asc()).all()
    
    logs_data = [
        {
            'ip': log.ip,
            'timestamp': log.timestamp,
            'url': log.url,
            'status_code': log.status_code,
            'method': log.method,
            'user_agent': log.user_agent
        }
        for log in logs
    ]
    
    stats = session_analyzer.analyze_logs(logs_data)
    
    return {
        'period_hours': hours,
        'total_logs_analyzed': len(logs_data),
        **stats
    }

@router.post("/anomalies/detect")
def detect_anomalies(
    hours: int = Query(24, ge=1, le=168),
    retrain: bool = Query(False, description="Ré-entraîner le modèle"),
    db: Session = Depends(get_db)
):
    """Détecte les anomalies dans les logs récents"""
    cutoff = datetime.now() - timedelta(hours=hours)
    
    logs = db.query(LogRecord).filter(
        LogRecord.timestamp >= cutoff
    ).all()
    
    logs_data = [
        {
            'ip': log.ip,
            'timestamp': log.timestamp,
            'url': log.url,
            'status_code': log.status_code,
            'method': log.method,
            'response_time': log.response_time
        }
        for log in logs
    ]
    
    if retrain or not anomaly_detector.is_trained:
        anomaly_detector.train(logs_data)
    
    anomalies, count = anomaly_detector.detect(logs_data)
    
    # Enrichir avec descriptions
    for anomaly in anomalies:
        anomaly['description'] = anomaly_detector.get_anomaly_description(anomaly)
    
    return {
        'period_hours': hours,
        'total_logs_analyzed': len(logs_data),
        'anomalies_detected': count,
        'anomalies': anomalies[:20],  # Top 20
        'alert_level': 'HIGH' if count > 10 else 'MEDIUM' if count > 5 else 'LOW'
    }

@router.post("/benchmark")
def benchmark_websites(urls: List[str] = Query(..., description="URLs à analyser")):
    """Analyse comparative de sites web concurrents"""
    if len(urls) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 URLs")
    
    results = website_analyzer.compare_websites(urls)
    
    # Ranking par performance
    successful = [r for r in results if r['status'] == 'success']
    ranked = sorted(successful, key=lambda x: x.get('performance_score', 0), reverse=True)
    
    return {
        'total_analyzed': len(urls),
        'successful': len(successful),
        'failed': len(results) - len(successful),
        'results': results,
        'ranking': [
            {
                'url': r['url'],
                'score': r['performance_score'],
                'load_time': r['load_time_ms']
            }
            for r in ranked
        ]
    }

@router.get("/insights")
def get_insights(
    hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """Génère des insights et recommandations intelligentes"""
    cutoff = datetime.now() - timedelta(hours=hours)
    
    # Statistiques
    total = db.query(LogRecord).filter(LogRecord.timestamp >= cutoff).count()
    errors = db.query(LogRecord).filter(
        LogRecord.timestamp >= cutoff,
        LogRecord.status_code >= 400
    ).count()
    
    slow_requests = db.query(LogRecord).filter(
        LogRecord.timestamp >= cutoff,
        LogRecord.response_time > 2000
    ).count()
    
    # Top pages lentes
    slow_pages = db.query(
        LogRecord.url,
        func.avg(LogRecord.response_time).label('avg_time'),
        func.count(LogRecord.id).label('count')
    ).filter(
        LogRecord.timestamp >= cutoff,
        LogRecord.response_time.isnot(None)
    ).group_by(LogRecord.url).order_by('avg_time DESC').limit(5).all()
    
    # Générer recommandations
    recommendations = []
    
    if errors / total > 0.1:
        recommendations.append({
            'type': 'CRITICAL',
            'title': 'Taux d\'erreur élevé',
            'description': f'{(errors/total)*100:.1f}% des requêtes échouent',
            'action': 'Vérifier les logs d\'erreur et corriger les endpoints défaillants'
        })
    
    if slow_requests / total > 0.2:
        recommendations.append({
            'type': 'WARNING',
            'title': 'Performances dégradées',
            'description': f'{(slow_requests/total)*100:.1f}% des requêtes > 2s',
            'action': 'Optimiser les requêtes lentes et mettre en place du caching'
        })
    
    return {
        'period_hours': hours,
        'total_requests': total,
        'error_rate': round((errors / total) * 100, 2) if total > 0 else 0,
        'slow_requests_rate': round((slow_requests / total) * 100, 2) if total > 0 else 0,
        'slowest_pages': [
            {'url': url, 'avg_time_ms': float(avg_time), 'requests': count}
            for url, avg_time, count in slow_pages
        ],
        'recommendations': recommendations,
        'health_score': max(0, 100 - (errors/total)*50 - (slow_requests/total)*30) if total > 0 else 100
    }
