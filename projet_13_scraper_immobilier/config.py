"""Configuration pour le Scraper Immobilier"""

# Sites immobiliers
REAL_ESTATE_SITES = {
    "seloger": {
        "name": "SeLoger",
        "base_url": "https://www.seloger.com",
        "search_path": "/list.htm"
    },
    "leboncoin": {
        "name": "LeBonCoin",
        "base_url": "https://www.leboncoin.fr",
        "search_path": "/recherche"
    }
}

# Types de biens
PROPERTY_TYPES = {
    "appartement": "Appartement",
    "maison": "Maison",
    "studio": "Studio",
    "loft": "Loft"
}

# Villes principales
CITIES = {
    "paris": {"name": "Paris", "code": "75000"},
    "lyon": {"name": "Lyon", "code": "69000"},
    "marseille": {"name": "Marseille", "code": "13000"},
    "toulouse": {"name": "Toulouse", "code": "31000"},
    "nice": {"name": "Nice", "code": "06000"}
}

# Paramètres de scraping
SCRAPING_CONFIG = {
    "delay": 2,  # secondes entre requêtes
    "timeout": 10,
    "max_pages": 5,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Couleurs pour visualisations
COLORS = {
    "price_low": "#2ecc71",
    "price_medium": "#f39c12",
    "price_high": "#e74c3c",
    "surface": "#3498db"
}