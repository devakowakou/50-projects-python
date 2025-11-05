import time
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import SessionLocal, init_db, LogRecord
from backend.services.log_parser import LogParser

class LogFileHandler(FileSystemEventHandler):
    """Handler pour surveiller les modifications du fichier de logs"""
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.parser = LogParser()
        self.last_position = 0
        init_db()
    
    def on_modified(self, event):
        if event.src_path == str(self.log_file):
            self.process_new_lines()
    
    def process_new_lines(self):
        """Traite les nouvelles lignes ajoutées au fichier"""
        try:
            with open(self.log_file, 'r') as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = f.tell()
            
            if not new_lines:
                return
            
            entries = []
            for line in new_lines:
                entry = self.parser.parse_line(line)
                if entry:
                    entries.append(entry)
            
            if entries:
                db = SessionLocal()
                try:
                    db_logs = [
                        LogRecord(
                            ip=e.ip,
                            timestamp=e.timestamp,
                            method=e.method,
                            url=e.url,
                            status_code=e.status_code,
                            response_time=e.response_time,
                            user_agent=e.user_agent
                        )
                        for e in entries
                    ]
                    db.bulk_save_objects(db_logs)
                    db.commit()
                    print(f"✅ {len(entries)} nouveaux logs importés")
                finally:
                    db.close()
        
        except Exception as e:
            print(f"❌ Erreur: {e}")

def main():
    # Détecter le fichier de logs
    base_path = Path(__file__).parent.parent / 'data' / 'raw_logs'
    massive_log = base_path / 'access_massive.log'
    normal_log = base_path / 'access.log'
    
    if massive_log.exists():
        log_file = massive_log
    elif normal_log.exists():
        log_file = normal_log
    else:
        print(f"❌ Aucun fichier de logs trouvé dans {base_path}")
        print("💡 Générez d'abord des logs:")
        print("   python scripts/generate_massive_logs.py")
        print("   python scripts/generate_sample_logs.py")
        return
    
    print(f"👀 Surveillance du fichier: {log_file}")
    print("Appuyez sur Ctrl+C pour arrêter")
    
    event_handler = LogFileHandler(log_file)
    observer = Observer()
    observer.schedule(event_handler, str(log_file.parent), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n👋 Arrêt du monitoring")
    
    observer.join()

if __name__ == '__main__':
    main()
