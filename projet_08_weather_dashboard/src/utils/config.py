import os
from pathlib import Path
from dotenv import load_dotenv
# Charger les variables d'environnement
load_dotenv()

class Config:
    """Configuration globale de l'application"""
    
    # API Configuration
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    # Default settings
    DEFAULT_CITY = os.getenv('DEFAULT_CITY', 'Paris')
    DEFAULT_UNITS = os.getenv('DEFAULT_UNITS', 'metric')  # metric, imperial, standard
    
    # Database
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    DB_PATH = PROJECT_ROOT / 'data' / 'weather_history.db'
    
    # API Limits
    CACHE_DURATION = 600  # 10 minutes en secondes
    MAX_REQUESTS_PER_DAY = 1000
    
    @classmethod
    def validate(cls):
        """Valide que la configuration est correcte"""
        if not cls.OPENWEATHER_API_KEY:
            raise ValueError(
                "❌ Clé API manquante!\n"
                "1. Créez un compte sur https://openweathermap.org/api\n"
                "2. Copiez .env.example vers .env\n"
                "3. Ajoutez votre clé API dans .env"
            )
        return True
    
    @classmethod
    def get_units_symbol(cls, units=None):
        """Retourne le symbole de température selon l'unité"""
        units = units or cls.DEFAULT_UNITS
        symbols = {
            'metric': '°C',
            'imperial': '°F',
            'standard': 'K'
        }
        return symbols.get(units, '°C')
