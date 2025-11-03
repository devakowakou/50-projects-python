"""
Configuration de l'application Stock Analysis Dashboard
"""

import os

# Configuration de la base de données
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'stock_analysis.db')}"

# Configuration des données boursières
DEFAULT_SYMBOLS = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "NFLX"]
DEFAULT_TIMEFRAME = "6mo"
DEFAULT_PERIOD = "1y"

# Configuration des indicateurs techniques
INDICATOR_CONFIG = {
    "sma_periods": [20, 50, 200],
    "ema_periods": [12, 26],
    "rsi_period": 14,
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,
    "bollinger_period": 20,
    "bollinger_std": 2
}

# Configuration de l'interface
CHART_CONFIG = {
    "height": 600,
    "template": "plotly_white",
    "colors": {
        "primary": "#1f77b4",
        "secondary": "#ff7f0e", 
        "success": "#2ca02c",
        "danger": "#d62728",
        "warning": "#ffbb78",
        "info": "#17a2b8"
    }
}

# Configuration du layout - AJOUTÉE
LAYOUT_CONFIG = {
    "sidebar_width": 2,
    "main_width": 10,
    "header_height": "60px"
}

# Configuration des intervalles de mise à jour
UPDATE_CONFIG = {
    "data_refresh_interval": 60000,  # 1 minute en millisecondes
    "chart_animation_duration": 500
}