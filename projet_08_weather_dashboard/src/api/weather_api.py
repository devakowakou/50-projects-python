import requests
from typing import Dict, Optional
from datetime import datetime
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.config import Config
from src.utils.helpers import cached_api_call, error_handler


class WeatherAPI:
    """Interface pour l'API OpenWeatherMap"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise l'API météo
        
        Args:
            api_key: Clé API OpenWeatherMap (utilise Config si None)
        """
        self.api_key = api_key or Config.OPENWEATHER_API_KEY
        self.base_url = Config.BASE_URL
        
        if not self.api_key:
            raise ValueError("Clé API manquante. Configurez OPENWEATHER_API_KEY dans .env")
    
    @cached_api_call(duration_seconds=600)  # Cache de 10 minutes
    @error_handler
    def get_current_weather(self, city: str, units: str = 'metric') -> Optional[Dict]:
        """
        Récupère la météo actuelle pour une ville
        
        Args:
            city: Nom de la ville
            units: Système d'unités (metric, imperial, standard)
            
        Returns:
            Dictionnaire avec les données météo ou None si erreur
        """
        endpoint = f"{self.base_url}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units,
            'lang': 'fr'
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Formatter les données
            return self._format_current_weather(data, units)
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"❌ Ville '{city}' introuvable. Vérifiez l'orthographe.")
            elif e.response.status_code == 401:
                print(f"❌ Clé API invalide ou expirée.")
            else:
                print(f"❌ Erreur HTTP {e.response.status_code}: {e}")
            return None
        except requests.exceptions.Timeout:
            print(f"❌ Délai d'attente dépassé pour {city}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de connexion: {e}")
            return None
    
    @cached_api_call(duration_seconds=600)
    @error_handler
    def get_forecast(self, city: str, units: str = 'metric', days: int = 5) -> Optional[Dict]:
        """
        Récupère les prévisions météo (5 jours par défaut)
        
        Args:
            city: Nom de la ville
            units: Système d'unités
            days: Nombre de jours (max 5 en gratuit)
            
        Returns:
            Dictionnaire avec les prévisions ou None si erreur
        """
        endpoint = f"{self.base_url}/forecast"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units,
            'lang': 'fr',
            'cnt': min(days * 8, 40)  # 8 prévisions par jour (toutes les 3h)
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Formatter les données
            return self._format_forecast(data, units)
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"❌ Ville '{city}' introuvable. Vérifiez l'orthographe.")
            elif e.response.status_code == 401:
                print(f"❌ Clé API invalide ou expirée.")
            else:
                print(f"❌ Erreur HTTP {e.response.status_code}: {e}")
            return None
        except requests.exceptions.Timeout:
            print(f"❌ Délai d'attente dépassé pour {city}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de connexion: {e}")
            return None
    
    def _format_current_weather(self, data: Dict, units: str) -> Dict:
        """Formate les données météo actuelles"""
        return {
            'city': data['name'],
            'country': data['sys']['country'],
            'timestamp': datetime.fromtimestamp(data['dt']),
            'temperature': round(data['main']['temp'], 1),
            'feels_like': round(data['main']['feels_like'], 1),
            'temp_min': round(data['main']['temp_min'], 1),
            'temp_max': round(data['main']['temp_max'], 1),
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'].capitalize(),
            'icon': data['weather'][0]['icon'],
            'wind_speed': round(data['wind']['speed'], 1),
            'wind_deg': data['wind'].get('deg', 0),
            'clouds': data['clouds']['all'],
            'visibility': data.get('visibility', 0) / 1000,  # en km
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']),
            'units': units,
            'unit_symbol': Config.get_units_symbol(units)
        }
    
    def _format_forecast(self, data: Dict, units: str) -> Dict:
        """Formate les données de prévisions"""
        forecasts = []
        
        for item in data['list']:
            forecasts.append({
                'timestamp': datetime.fromtimestamp(item['dt']),
                'temperature': round(item['main']['temp'], 1),
                'feels_like': round(item['main']['feels_like'], 1),
                'temp_min': round(item['main']['temp_min'], 1),
                'temp_max': round(item['main']['temp_max'], 1),
                'pressure': item['main']['pressure'],
                'humidity': item['main']['humidity'],
                'description': item['weather'][0]['description'].capitalize(),
                'icon': item['weather'][0]['icon'],
                'wind_speed': round(item['wind']['speed'], 1),
                'clouds': item['clouds']['all'],
                'pop': round(item.get('pop', 0) * 100)  # Probabilité de pluie en %
            })
        
        return {
            'city': data['city']['name'],
            'country': data['city']['country'],
            'forecasts': forecasts,
            'units': units,
            'unit_symbol': Config.get_units_symbol(units)
        }
    
    def test_connection(self) -> bool:
        """Teste la connexion à l'API"""
        result = self.get_current_weather('Paris')
        return result is not None
