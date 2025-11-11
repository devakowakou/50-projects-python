import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import SessionLocal, init_db, LogRecord
from backend.services.log_parser import LogParser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_batch(lines_batch: list, batch_num: int) -> int:
    """Traite un batch de lignes en parallèle"""
    parser = LogParser()
    entries = []
    
    for line_num, line in lines_batch:
        entry = parser.parse_line(line, line_num)
        if entry:
            entries.append(entry)
    
    if not entries:
        return 0
    
    # Insertion en base
    db = SessionLocal()
    try:
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
            for entry in entries
        ]
        
        db.bulk_save_objects(db_logs)
        db.commit()
        
        logger.info(f"✓ Batch {batch_num}: {len(entries)} logs importés")
        return len(entries)
    
    except Exception as e:
        logger.error(f"❌ Erreur batch {batch_num}: {e}")
        db.rollback()
        return 0
    finally:
        db.close()

def import_massive_logs(log_file: Path, batch_size: int = 10000):
    """Import parallèle de gros volumes de logs"""
    
    init_db()
    
    logger.info(f"📖 Lecture du fichier: {log_file}")
    
    # Lire toutes les lignes
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        all_lines = [(i, line) for i, line in enumerate(f, 1) if line.strip()]
    
    total_lines = len(all_lines)
    logger.info(f"📊 {total_lines:,} lignes à traiter")
    
    # Diviser en batches
    batches = []
    for i in range(0, total_lines, batch_size):
        batch = all_lines[i:i+batch_size]
        batches.append((batch, i // batch_size))
    
    logger.info(f"📦 {len(batches)} batches créés")
    
    # Traitement parallèle
    num_workers = multiprocessing.cpu_count()
    logger.info(f"🚀 Démarrage avec {num_workers} workers...")
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(lambda args: process_batch(*args), batches)
        total_imported = sum(results)
    
    logger.info(f"✅ Import terminé: {total_imported:,}/{total_lines:,} logs importés")
    logger.info(f"📈 Taux de succès: {(total_imported/total_lines)*100:.2f}%")

def main():
    # Détecter le fichier de logs (massive ou normal)
    massive_log = Path(__file__).parent.parent / 'data' / 'raw_logs' / 'access_massive.log'
    normal_log = Path(__file__).parent.parent / 'data' / 'raw_logs' / 'access.log'
    
    if massive_log.exists():
        log_file = massive_log
        logger.info("🎯 Fichier MASSIF détecté")
    elif normal_log.exists():
        log_file = normal_log
        logger.info("📄 Fichier normal détecté")
    else:
        logger.error("❌ Aucun fichier de logs trouvé")
        logger.info("💡 Générez d'abord des logs:")
        logger.info("   - python scripts/generate_massive_logs.py  (2M logs)")
        logger.info("   - python scripts/generate_sample_logs.py   (5K logs)")
        return
    
    import_massive_logs(log_file)

if __name__ == '__main__':
    main()
