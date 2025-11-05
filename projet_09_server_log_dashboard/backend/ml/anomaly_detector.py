import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from datetime import datetime
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class AnomalyDetector:
    """Détection d'anomalies dans les logs avec ML"""
    
    def __init__(self, contamination: float = 0.1):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def prepare_features(self, logs_data: List[Dict]) -> np.ndarray:
        """Extrait les features pour la détection d'anomalies"""
        if not logs_data:
            return np.array([])
        
        features = []
        time_windows = {}
        
        for log in logs_data:
            minute = log['timestamp'].replace(second=0, microsecond=0)
            if minute not in time_windows:
                time_windows[minute] = {
                    'requests': 0,
                    'errors': 0,
                    'response_times': [],
                    'ips': set(),
                    'methods': {'GET': 0, 'POST': 0}
                }
            
            time_windows[minute]['requests'] += 1
            if log['status_code'] >= 400:
                time_windows[minute]['errors'] += 1
            if log.get('response_time'):
                time_windows[minute]['response_times'].append(log['response_time'])
            time_windows[minute]['ips'].add(log['ip'])
            time_windows[minute]['methods'][log['method']] = \
                time_windows[minute]['methods'].get(log['method'], 0) + 1
        
        for minute, stats in time_windows.items():
            avg_response = np.mean(stats['response_times']) if stats['response_times'] else 0
            error_rate = stats['errors'] / stats['requests'] if stats['requests'] > 0 else 0
            get_post_ratio = stats['methods']['GET'] / max(stats['methods']['POST'], 1)
            
            features.append([
                stats['requests'],
                error_rate,
                avg_response,
                len(stats['ips']),
                get_post_ratio
            ])
        
        return np.array(features)
    
    def train(self, logs_data: List[Dict]) -> None:
        """Entraîne le modèle sur des données historiques"""
        logger.info("🧠 Entraînement du modèle de détection d'anomalies...")
        
        features = self.prepare_features(logs_data)
        if len(features) == 0:
            logger.warning("⚠️ Pas assez de données pour l'entraînement")
            return
        
        features_scaled = self.scaler.fit_transform(features)
        self.model.fit(features_scaled)
        self.is_trained = True
        
        logger.info(f"✅ Modèle entraîné sur {len(features)} fenêtres temporelles")
    
    def detect(self, logs_data: List[Dict]) -> Tuple[List[Dict], int]:
        """Détecte les anomalies dans les logs"""
        if not self.is_trained:
            logger.warning("⚠️ Modèle non entraîné, entraînement automatique...")
            self.train(logs_data)
        
        features = self.prepare_features(logs_data)
        if len(features) == 0:
            return [], 0
        
        features_scaled = self.scaler.transform(features)
        predictions = self.model.predict(features_scaled)
        scores = self.model.score_samples(features_scaled)
        
        anomalies = []
        for idx, (pred, score) in enumerate(zip(predictions, scores)):
            if pred == -1:
                anomalies.append({
                    'index': idx,
                    'score': float(score),
                    'severity': 'HIGH' if score < -0.5 else 'MEDIUM',
                    'features': features[idx].tolist()
                })
        
        anomaly_count = len(anomalies)
        logger.info(f"🔍 Détection: {anomaly_count} anomalies trouvées sur {len(features)} fenêtres")
        
        return anomalies, anomaly_count
    
    def get_anomaly_description(self, anomaly: Dict) -> str:
        """Génère une description textuelle de l'anomalie"""
        features = anomaly['features']
        requests, error_rate, avg_time, unique_ips, ratio = features
        
        descriptions = []
        
        if requests > 100:
            descriptions.append(f"Pic de trafic inhabituel ({int(requests)} req/min)")
        if error_rate > 0.2:
            descriptions.append(f"Taux d'erreur élevé ({error_rate*100:.1f}%)")
        if avg_time > 2000:
            descriptions.append(f"Temps de réponse anormal ({avg_time:.0f}ms)")
        if unique_ips > 50:
            descriptions.append(f"Nombre d'IPs suspect ({int(unique_ips)})")
        
        return " | ".join(descriptions) if descriptions else "Comportement anormal détecté"
