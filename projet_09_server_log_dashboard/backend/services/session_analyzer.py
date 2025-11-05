from datetime import datetime, timedelta
from typing import List, Dict
from collections import defaultdict
import hashlib

class SessionAnalyzer:
    """Analyse des sessions utilisateur et parcours clients"""
    
    def __init__(self, session_timeout: int = 30):
        self.session_timeout = timedelta(minutes=session_timeout)
    
    def generate_session_id(self, ip: str, user_agent: str) -> str:
        """Génère un identifiant de session unique"""
        data = f"{ip}:{user_agent}".encode()
        return hashlib.md5(data).hexdigest()[:16]
    
    def analyze_logs(self, logs: List[Dict]) -> Dict:
        """Analyse les logs pour extraire les sessions"""
        sorted_logs = sorted(logs, key=lambda x: x['timestamp'])
        
        sessions = defaultdict(lambda: {
            'pages': [],
            'start_time': None,
            'end_time': None,
            'requests': 0,
            'errors': 0,
            'ip': None,
            'user_agent': None
        })
        
        for log in sorted_logs:
            session_id = self.generate_session_id(log['ip'], log['user_agent'])
            session = sessions[session_id]
            
            if session['start_time'] is None:
                session['start_time'] = log['timestamp']
                session['ip'] = log['ip']
                session['user_agent'] = log['user_agent']
            else:
                time_diff = log['timestamp'] - session['end_time']
                if time_diff > self.session_timeout:
                    session_id = f"{session_id}_{len([s for s in sessions if s.startswith(session_id)])}"
                    session = sessions[session_id]
                    session['start_time'] = log['timestamp']
                    session['ip'] = log['ip']
                    session['user_agent'] = log['user_agent']
            
            session['end_time'] = log['timestamp']
            session['pages'].append({
                'url': log['url'],
                'timestamp': log['timestamp'],
                'status': log['status_code'],
                'method': log['method']
            })
            session['requests'] += 1
            if log['status_code'] >= 400:
                session['errors'] += 1
        
        return self._compute_statistics(dict(sessions))
    
    def _compute_statistics(self, sessions: Dict) -> Dict:
        """Calcule les statistiques agrégées"""
        total_sessions = len(sessions)
        
        if total_sessions == 0:
            return {
                'total_sessions': 0,
                'avg_duration': 0,
                'avg_pages_per_session': 0,
                'bounce_rate': 0,
                'conversion_paths': []
            }
        
        durations = []
        pages_per_session = []
        bounce_count = 0
        
        for session in sessions.values():
            if session['start_time'] and session['end_time']:
                duration = (session['end_time'] - session['start_time']).total_seconds()
                durations.append(duration)
            
            pages_per_session.append(session['requests'])
            
            if session['requests'] == 1:
                bounce_count += 1
        
        conversion_paths = self._extract_top_paths(sessions, limit=10)
        
        return {
            'total_sessions': total_sessions,
            'avg_duration': sum(durations) / len(durations) if durations else 0,
            'avg_pages_per_session': sum(pages_per_session) / len(pages_per_session),
            'bounce_rate': (bounce_count / total_sessions) * 100,
            'conversion_paths': conversion_paths,
            'session_details': self._format_sessions(sessions)
        }
    
    def _extract_top_paths(self, sessions: Dict, limit: int = 10) -> List[Dict]:
        """Extrait les parcours clients les plus fréquents"""
        paths = defaultdict(int)
        
        for session in sessions.values():
            if len(session['pages']) > 1:
                path = ' → '.join([page['url'] for page in session['pages'][:5]])
                paths[path] += 1
        
        sorted_paths = sorted(paths.items(), key=lambda x: x[1], reverse=True)[:limit]
        
        return [{'path': path, 'count': count} for path, count in sorted_paths]
    
    def _format_sessions(self, sessions: Dict) -> List[Dict]:
        """Formate les sessions pour l'API"""
        formatted = []
        
        for session_id, session in sessions.items():
            duration = (session['end_time'] - session['start_time']).total_seconds() \
                       if session['start_time'] and session['end_time'] else 0
            
            formatted.append({
                'session_id': session_id,
                'ip': session['ip'],
                'start_time': session['start_time'].isoformat() if session['start_time'] else None,
                'duration': duration,
                'pages_visited': session['requests'],
                'errors': session['errors'],
                'pages': [p['url'] for p in session['pages'][:10]]
            })
        
        return formatted[:100]
