"""Configuration du projet d'analyse de sentiment."""

import os
from pathlib import Path

# Chemins
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "nlp" / "models"

# Base de données
DATABASE_PATH = DATA_DIR / "reviews.db"

# Scraping
SCRAPING_CONFIG = {
    "delay_range": (1, 3),  # Délai entre requêtes (secondes)
    "max_retries": 3,
    "timeout": 30,
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    ]
}

# NLP
NLP_CONFIG = {
    "languages": ["en", "fr"],
    "min_text_length": 10,
    "max_text_length": 5000,
    "sentiment_threshold": {
        "positive": 0.1,
        "negative": -0.1
    }
}

# Dashboard
DASHBOARD_CONFIG = {
    "host": "localhost",
    "port": 8501,
    "theme": "light"
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": PROJECT_ROOT / "logs" / "app.log"
}