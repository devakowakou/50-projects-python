import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import SessionLocal, init_db, LogRecord
from backend.services.log_parser import LogParser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def import_logs(log_file: Path, batch_size: int = 500):
    """Importe les logs dans la base de données"""
    
    init_db()
    
    parser = LogParser()
    entries = parser.parse_file(log_file)
    
    if not entries:
        logger.error("❌ Aucun log parsé")
        return
    
    logger.info(f"📦 Import de {len(entries)} logs en base...")
    
    db = SessionLocal()
    
    try:
        for i in range(0, len(entries), batch_size):
            batch = entries[i:i + batch_size]
            
            db_logs = [
                LogRecord(
                    ip=entry.ip,
                    timestamp=entry.timestamp,
                    method=entry.method,
                    url=entry.url,
                    status_code=entry.status_code,
                    response_time=entry.response_time,
                    user_agent=entry.user_agent
                )
                for entry in batch
            ]
            
            db.bulk_save_objects(db_logs)
            db.commit()
            
            logger.info(f"  ✓ {min(i + batch_size, len(entries))}/{len(entries)} logs importés")
        
        logger.info(f"✅ Import terminé: {len(entries)} logs en base")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'import: {e}")
        db.rollback()
    finally:
        db.close()
    
    stats = parser.get_stats()
    logger.info(f"📊 Stats: {stats['parsed']} OK, {stats['errors']} erreurs ({stats['success_rate']}% succès)")

def main():
    # Détecter le fichier de logs (massive ou normal)
    base_path = Path(__file__).parent.parent / 'data' / 'raw_logs'
    massive_log = base_path / 'access_massive.log'
    normal_log = base_path / 'access.log'
    
    if massive_log.exists():
        log_file = massive_log
        logger.info("🎯 Fichier MASSIF détecté (utilise import_production_logs.py pour performances optimales)")
    elif normal_log.exists():
        log_file = normal_log
        logger.info("📄 Fichier normal détecté")
    else:
        logger.error(f"❌ Fichier introuvable: {normal_log}")
        logger.info("💡 Générez d'abord des logs:")
        logger.info("   - python scripts/generate_massive_logs.py  (2M logs)")
        logger.info("   - python scripts/generate_sample_logs.py   (5K logs)")
        return
    
    import_logs(log_file)

if __name__ == '__main__':
    main()
