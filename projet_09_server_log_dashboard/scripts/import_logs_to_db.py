import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import SessionLocal, init_db, LogRecord
from backend.services.log_parser import LogParser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def import_logs(log_file: Path, batch_size: int = 500):
    """Importe les logs dans la base de données"""
    
    # Initialiser la DB
    init_db()
    
    # Parser le fichier
    parser = LogParser()
    entries = parser.parse_file(log_file)
    
    if not entries:
        logger.error("❌ Aucun log parsé")
        return
    
    logger.info(f"📦 Import de {len(entries)} logs en base...")
    
    # Session DB
    db = SessionLocal()
    
    try:
        # Import par batch
        for i in range(0, len(entries), batch_size):
            batch = entries[i:i + batch_size]
            
            # Convertir en objets SQLAlchemy
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
    
    # Afficher les stats de parsing
    stats = parser.get_stats()
    logger.info(f"📊 Stats: {stats['parsed']} OK, {stats['errors']} erreurs ({stats['success_rate']}% succès)")

def main():
    log_file = Path(__file__).parent.parent / 'data' / 'raw_logs' / 'access.log'
    
    if not log_file.exists():
        logger.error(f"❌ Fichier introuvable: {log_file}")
        logger.info("💡 Lancer d'abord: python scripts/generate_sample_logs.py")
        return
    
    import_logs(log_file)

if __name__ == '__main__':
    main()
