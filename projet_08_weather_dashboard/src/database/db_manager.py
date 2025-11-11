import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path
import sys

# Ajouter le dossier parent au path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.config import Config
from src.database.models import WEATHER_HISTORY_SCHEMA, FORECAST_HISTORY_SCHEMA, INDEXES


class DatabaseManager:
    """Gestionnaire de base de données pour l'historique météo"""
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialise le gestionnaire de base de données
        
        Args:
            db_path: Chemin vers la base de données (utilise Config si None)
        """
        self.db_path = db_path or Config.DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Crée les tables si elles n'existent pas"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Créer les tables
            cursor.execute(WEATHER_HISTORY_SCHEMA)
            cursor.execute(FORECAST_HISTORY_SCHEMA)
            
            # Créer les index
            for index_sql in INDEXES:
                cursor.execute(index_sql)
            
            conn.commit()
    
    def save_current_weather(self, weather_data: Dict) -> bool:
        """
        Sauvegarde les données météo actuelles
        
        Args:
            weather_data: Dictionnaire avec les données météo formatées
            
        Returns:
            True si succès, False sinon
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO weather_history (
                        city, country, timestamp, temperature, feels_like,
                        temp_min, temp_max, pressure, humidity, description,
                        icon, wind_speed, wind_deg, clouds, visibility, units
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    weather_data['city'],
                    weather_data['country'],
                    weather_data['timestamp'],
                    weather_data['temperature'],
                    weather_data['feels_like'],
                    weather_data['temp_min'],
                    weather_data['temp_max'],
                    weather_data['pressure'],
                    weather_data['humidity'],
                    weather_data['description'],
                    weather_data['icon'],
                    weather_data['wind_speed'],
                    weather_data['wind_deg'],
                    weather_data['clouds'],
                    weather_data['visibility'],
                    weather_data['units']
                ))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            print(f"❌ Erreur DB: {e}")
            return False
    
    def save_forecast(self, city: str, country: str, forecasts: List[Dict], units: str = 'metric') -> bool:
        """
        Sauvegarde les prévisions météo
        
        Args:
            city: Nom de la ville
            country: Code pays
            forecasts: Liste des prévisions
            units: Système d'unités
            
        Returns:
            True si succès, False sinon
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for forecast in forecasts:
                    cursor.execute("""
                        INSERT INTO forecast_history (
                            city, country, forecast_timestamp, temperature,
                            feels_like, temp_min, temp_max, pressure, humidity,
                            description, icon, wind_speed, clouds, pop, units
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        city,
                        country,
                        forecast['timestamp'],
                        forecast['temperature'],
                        forecast['feels_like'],
                        forecast['temp_min'],
                        forecast['temp_max'],
                        forecast['pressure'],
                        forecast['humidity'],
                        forecast['description'],
                        forecast['icon'],
                        forecast['wind_speed'],
                        forecast['clouds'],
                        forecast['pop'],
                        units
                    ))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            print(f"❌ Erreur DB: {e}")
            return False
    
    def get_weather_history(self, city: str, days: int = 7) -> List[Dict]:
        """
        Récupère l'historique météo d'une ville
        
        Args:
            city: Nom de la ville
            days: Nombre de jours d'historique
            
        Returns:
            Liste de dictionnaires avec l'historique
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                start_date = datetime.now() - timedelta(days=days)
                
                cursor.execute("""
                    SELECT * FROM weather_history
                    WHERE city = ? AND timestamp >= ?
                    ORDER BY timestamp DESC
                """, (city, start_date))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except sqlite3.Error as e:
            print(f"❌ Erreur DB: {e}")
            return []
    
    def get_temperature_stats(self, city: str, days: int = 30) -> Dict:
        """
        Calcule les statistiques de température pour une ville
        
        Args:
            city: Nom de la ville
            days: Période en jours
            
        Returns:
            Dictionnaire avec min, max, moyenne
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                start_date = datetime.now() - timedelta(days=days)
                
                cursor.execute("""
                    SELECT 
                        MIN(temperature) as min_temp,
                        MAX(temperature) as max_temp,
                        AVG(temperature) as avg_temp,
                        AVG(humidity) as avg_humidity,
                        AVG(pressure) as avg_pressure
                    FROM weather_history
                    WHERE city = ? AND timestamp >= ?
                """, (city, start_date))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'min_temp': round(row[0], 1) if row[0] else None,
                        'max_temp': round(row[1], 1) if row[1] else None,
                        'avg_temp': round(row[2], 1) if row[2] else None,
                        'avg_humidity': round(row[3], 1) if row[3] else None,
                        'avg_pressure': round(row[4], 1) if row[4] else None
                    }
                return {}
                
        except sqlite3.Error as e:
            print(f"❌ Erreur DB: {e}")
            return {}
    
    def get_all_cities(self) -> List[str]:
        """Récupère la liste de toutes les villes dans l'historique"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT city FROM weather_history
                    ORDER BY city
                """)
                return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"❌ Erreur DB: {e}")
            return []
    
    def cleanup_old_data(self, days: int = 90):
        """
        Nettoie les données anciennes
        
        Args:
            days: Supprime les données plus anciennes que X jours
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cutoff_date = datetime.now() - timedelta(days=days)
                
                cursor.execute("DELETE FROM weather_history WHERE timestamp < ?", (cutoff_date,))
                cursor.execute("DELETE FROM forecast_history WHERE saved_at < ?", (cutoff_date,))
                
                conn.commit()
                print(f"✅ Nettoyage: données de plus de {days} jours supprimées")
                
        except sqlite3.Error as e:
            print(f"❌ Erreur nettoyage: {e}")
