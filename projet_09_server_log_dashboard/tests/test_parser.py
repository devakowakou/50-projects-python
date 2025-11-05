import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.log_parser import LogParser

def test_parse_valid_line():
    """Test parsing d'une ligne valide"""
    parser = LogParser()
    line = '192.168.1.1 - - [01/Jan/2024:12:00:00 +0000] "GET /home HTTP/1.1" 200 1234 "-" "Mozilla/5.0" 150'
    
    entry = parser.parse_line(line)
    
    assert entry is not None
    assert entry.ip == '192.168.1.1'
    assert entry.method == 'GET'
    assert entry.url == '/home'
    assert entry.status_code == 200
    assert entry.response_time == 150.0

def test_parse_invalid_line():
    """Test parsing d'une ligne invalide"""
    parser = LogParser()
    line = 'invalid log line'
    
    entry = parser.parse_line(line)
    
    assert entry is None
    assert parser.error_count == 1

def test_parser_stats():
    """Test des statistiques de parsing"""
    parser = LogParser()
    
    parser.parse_line('192.168.1.1 - - [01/Jan/2024:12:00:00 +0000] "GET /home HTTP/1.1" 200 1234 "-" "Mozilla" 150')
    parser.parse_line('invalid line')
    
    stats = parser.get_stats()
    
    assert stats['parsed'] == 1
    assert stats['errors'] == 1
    assert stats['success_rate'] == 50.0
