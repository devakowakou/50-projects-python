import time
import random
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import SessionLocal, init_db, LogRecord
from backend.services.log_parser import LogParser

URLS = ['/', '/api/users', '/api/data', '/dashboard', '/login']
METHODS = ['GET', 'POST', 'PUT', 'DELETE']
STATUS_CODES = [200, 200, 200, 304, 404, 500]

def generate_realtime_log() -> str:
    """Génère un log en temps réel"""
    ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    now = datetime.now()
    ts_str = now.strftime('%d/%b/%Y:%H:%M:%S +0000')
    method = random.choice(METHODS)
    url = random.choice(URLS)
    status = random.choice(STATUS_CODES)
    size = random.randint(100, 5000)
    ua = "Mozilla/5.0 (RealTime Stream)"
    response_time = random.randint(10, 1000)
    
    return f'{ip} - - [{ts_str}] "{method} {url} HTTP/1.1" {status} {size} "-" "{ua}" {response_time}\n'

def main():
    """Simule un flux continu de logs"""
    init_db()
    parser = LogParser()
    
    print("🌊 Streaming de logs en temps réel...")
    print("⏱️  1 log toutes les 100ms (10 logs/sec)")
    print("Appuyez sur Ctrl+C pour arrêter\n")
    
    count = 0
    
    try:
        while True:
            # Générer un log
            log_line = generate_realtime_log()
            entry = parser.parse_line(log_line)
            
            if entry:
                # Insérer en base
                db = SessionLocal()
                try:
                    db_log = LogRecord(
                        ip=entry.ip,
                        timestamp=entry.timestamp,
                        method=entry.method,
                        url=entry.url,
                        status_code=entry.status_code,
                        response_time=entry.response_time,
                        user_agent=entry.user_agent
                    )
                    db.add(db_log)
                    db.commit()
                    
                    count += 1
                    if count % 10 == 0:
                        print(f"✅ {count} logs streamés | Dernier: {entry.method} {entry.url} [{entry.status_code}]")
                
                finally:
                    db.close()
            
            time.sleep(0.1)  # 100ms entre chaque log
    
    except KeyboardInterrupt:
        print(f"\n👋 Arrêt du streaming après {count} logs")

if __name__ == '__main__':
    main()
