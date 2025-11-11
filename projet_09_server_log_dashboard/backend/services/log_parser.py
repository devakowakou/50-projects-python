import re
import logging
from datetime import datetime
from typing import Optional, List
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogEntry:
    """Représente une entrée de log parsée"""
    def __init__(self, ip: str, timestamp: datetime, method: str, 
                 url: str, status_code: int, user_agent: str, 
                 response_time: Optional[float] = None):
        self.ip = ip
        self.timestamp = timestamp
        self.method = method
        self.url = url
        self.status_code = status_code
        self.user_agent = user_agent
        self.response_time = response_time

    def to_dict(self) -> dict:
        return {
            'ip': self.ip,
            'timestamp': self.timestamp,
            'method': self.method,
            'url': self.url,
            'status_code': self.status_code,
            'user_agent': self.user_agent,
            'response_time': self.response_time
        }

class LogParser:
    """Parser pour logs Apache/Nginx format Combined"""
    
    APACHE_PATTERN = re.compile(
        r'(?P<ip>[\d.:a-fA-F]+) - - \[(?P<timestamp>[^\]]+)\] '
        r'"(?P<method>\w+) (?P<url>[^\s]+) HTTP/[\d.]+" '
        r'(?P<status>\d{3}) (?P<size>\d+|-) '
        r'"[^"]*" "(?P<user_agent>[^"]*)"'
        r'(?: (?P<response_time>\d+))?'
    )
    
    TIMESTAMP_FORMAT = '%d/%b/%Y:%H:%M:%S %z'
    
    def __init__(self):
        self.parsed_count = 0
        self.error_count = 0
        self.errors = []
    
    def parse_line(self, line: str, line_num: int = 0) -> Optional[LogEntry]:
        """Parse une ligne de log"""
        match = self.APACHE_PATTERN.match(line.strip())
        
        if not match:
            self.error_count += 1
            self.errors.append(f"Line {line_num}: Format non reconnu")
            return None
        
        try:
            data = match.groupdict()
            
            # Parser le timestamp
            try:
                timestamp = datetime.strptime(data['timestamp'], self.TIMESTAMP_FORMAT)
            except ValueError:
                # Essayer sans timezone
                timestamp = datetime.strptime(data['timestamp'].split()[0], '%d/%b/%Y:%H:%M:%S')
            
            # Extraire le temps de réponse si présent
            response_time = float(data['response_time']) if data.get('response_time') else None
            
            self.parsed_count += 1
            
            return LogEntry(
                ip=data['ip'],
                timestamp=timestamp,
                method=data['method'],
                url=data['url'],
                status_code=int(data['status']),
                user_agent=data['user_agent'],
                response_time=response_time
            )
            
        except Exception as e:
            self.error_count += 1
            self.errors.append(f"Line {line_num}: {str(e)}")
            logger.error(f"Erreur ligne {line_num}: {e}")
            return None
    
    def parse_file(self, filepath: Path) -> List[LogEntry]:
        """Parse un fichier complet"""
        logger.info(f"📖 Parsing du fichier: {filepath}")
        entries = []
        
        if not filepath.exists():
            logger.error(f"❌ Fichier introuvable: {filepath}")
            return entries
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, start=1):
                if line.strip():
                    entry = self.parse_line(line, line_num)
                    if entry:
                        entries.append(entry)
        
        logger.info(f"✅ Parsing terminé: {self.parsed_count} lignes OK, {self.error_count} erreurs")
        return entries
    
    def get_stats(self) -> dict:
        """Retourne les statistiques de parsing"""
        total = self.parsed_count + self.error_count
        return {
            'parsed': self.parsed_count,
            'errors': self.error_count,
            'success_rate': round(self.parsed_count / total * 100, 2) if total > 0 else 0
        }
