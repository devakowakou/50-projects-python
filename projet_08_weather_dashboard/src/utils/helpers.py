import time
from functools import wraps
from typing import Callable, Any
import streamlit as st
from datetime import datetime, timedelta


class Cache:
    """Gestionnaire de cache simple pour les appels API"""
    
    _cache = {}
    
    @classmethod
    def get(cls, key: str) -> Any:
        """Récupère une valeur du cache si elle n'est pas expirée"""
        if key in cls._cache:
            data, expiry = cls._cache[key]
            if datetime.now() < expiry:
                return data
            else:
                del cls._cache[key]
        return None
    
    @classmethod
    def set(cls, key: str, value: Any, duration_seconds: int = 600):
        """Stocke une valeur dans le cache avec expiration"""
        expiry = datetime.now() + timedelta(seconds=duration_seconds)
        cls._cache[key] = (value, expiry)
    
    @classmethod
    def clear(cls):
        """Vide tout le cache"""
        cls._cache.clear()
    
    @classmethod
    def size(cls) -> int:
        """Retourne le nombre d'éléments en cache"""
        # Nettoyer les entrées expirées
        expired_keys = [
            k for k, (_, expiry) in cls._cache.items()
            if datetime.now() >= expiry
        ]
        for key in expired_keys:
            del cls._cache[key]
        return len(cls._cache)


def cached_api_call(duration_seconds: int = 600):
    """
    Décorateur pour mettre en cache les appels API
    
    Args:
        duration_seconds: Durée de validité du cache en secondes
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Créer une clé unique basée sur la fonction et ses arguments
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            
            # Vérifier le cache
            cached_result = Cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Appeler la fonction si pas en cache
            result = func(*args, **kwargs)
            
            # Mettre en cache si résultat valide
            if result is not None:
                Cache.set(cache_key, result, duration_seconds)
            
            return result
        return wrapper
    return decorator


def error_handler(func: Callable) -> Callable:
    """Décorateur pour gérer les erreurs de manière élégante"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"❌ Erreur dans {func.__name__}: {str(e)}")
            return None
    return wrapper


def format_timestamp(timestamp: datetime, format_str: str = "%d/%m/%Y %H:%M") -> str:
    """Formate un timestamp de manière lisible"""
    try:
        return timestamp.strftime(format_str)
    except:
        return "Date invalide"


def get_weather_emoji(description: str) -> str:
    """Retourne un emoji correspondant à la description météo"""
    description = description.lower()
    
    if 'clear' in description or 'ensoleillé' in description:
        return '☀️'
    elif 'cloud' in description or 'nuage' in description:
        return '☁️'
    elif 'rain' in description or 'pluie' in description:
        return '🌧️'
    elif 'thunder' in description or 'orage' in description:
        return '⛈️'
    elif 'snow' in description or 'neige' in description:
        return '❄️'
    elif 'mist' in description or 'fog' in description or 'brume' in description:
        return '🌫️'
    else:
        return '🌤️'


def validate_city_name(city: str) -> bool:
    """Valide le nom d'une ville"""
    if not city or len(city.strip()) < 2:
        return False
    # Autoriser lettres, espaces, tirets, apostrophes
    return all(c.isalpha() or c in ' -\'' for c in city)


def format_wind_direction(degrees: int) -> str:
    """Convertit les degrés en direction cardinale"""
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    idx = round(degrees / 45) % 8
    return directions[idx]


def calculate_heat_index(temp_celsius: float, humidity: int) -> float:
    """
    Calcule l'indice de chaleur (ressenti en fonction de l'humidité)
    Formule simplifiée
    """
    if temp_celsius < 27:
        return temp_celsius
    
    # Formule simplifiée de l'indice de chaleur
    hi = -8.78469475556 + 1.61139411 * temp_celsius + 2.33854883889 * humidity
    hi += -0.14611605 * temp_celsius * humidity
    hi += -0.012308094 * temp_celsius**2
    hi += -0.0164248277778 * humidity**2
    
    return round(hi, 1)
