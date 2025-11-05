import requests
import os
from typing import Dict, List, Optional

class APIClient:
    """Client pour communiquer avec l'API backend"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv('API_URL', 'http://localhost:8000')
    
    def get_health(self) -> Dict:
        """Vérifie le statut de l'API"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.json()
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_overview_stats(self) -> Dict:
        """Récupère les statistiques globales"""
        response = requests.get(f"{self.base_url}/api/stats/overview")
        response.raise_for_status()
        return response.json()
    
    def get_recent_logs(self, limit: int = 20) -> List[Dict]:
        """Récupère les logs récents (max 10000)"""
        if limit > 10000:
            limit = 10000
        response = requests.get(f"{self.base_url}/api/logs/recent?limit={limit}")
        response.raise_for_status()
        return response.json()
    
    def export_logs(self, hours: int = 24, format: str = "json"):
        """Exporte les logs sans limite stricte"""
        response = requests.get(
            f"{self.base_url}/api/logs/export",
            params={"hours": hours, "format": format}
        )
        response.raise_for_status()
        
        # Si CSV, retourner le contenu brut
        if format == "csv":
            return response.text
        
        # Si JSON, retourner le dict
        return response.json()
    
    def get_top_urls(self, limit: int = 10) -> List[Dict]:
        """Récupère les URLs les plus visitées"""
        response = requests.get(f"{self.base_url}/api/stats/top-urls?limit={limit}")
        response.raise_for_status()
        return response.json()
    
    def get_status_distribution(self) -> List[Dict]:
        """Récupère la distribution des codes HTTP"""
        response = requests.get(f"{self.base_url}/api/stats/status-distribution")
        response.raise_for_status()
        return response.json()
    
    def get_requests_timeline(self, days: int = 7) -> List[Dict]:
        """Récupère la timeline des requêtes"""
        response = requests.get(f"{self.base_url}/api/stats/requests-timeline?days={days}")
        response.raise_for_status()
        return response.json()
    
    def get_sessions_analysis(self, hours: int = 24) -> Dict:
        """Récupère l'analyse des sessions"""
        response = requests.get(f"{self.base_url}/api/analytics/sessions?hours={hours}")
        response.raise_for_status()
        return response.json()
    
    def detect_anomalies(self, hours: int = 24, retrain: bool = False) -> Dict:
        """Détecte les anomalies"""
        response = requests.post(
            f"{self.base_url}/api/analytics/anomalies/detect?hours={hours}&retrain={retrain}"
        )
        response.raise_for_status()
        return response.json()
    
    def benchmark_websites(self, urls: List[str]) -> Dict:
        """Benchmark des sites web"""
        response = requests.post(
            f"{self.base_url}/api/analytics/benchmark",
            params={"urls": urls}
        )
        response.raise_for_status()
        return response.json()
    
    def get_insights(self, hours: int = 24) -> Dict:
        """Récupère les insights et recommandations"""
        response = requests.get(f"{self.base_url}/api/analytics/insights?hours={hours}")
        response.raise_for_status()
        return response.json()
