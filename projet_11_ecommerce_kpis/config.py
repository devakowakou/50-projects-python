"""
Configuration pour le Dashboard E-commerce KPIs
"""

# Paramètres de génération de données
DATA_CONFIG = {
    "transactions_count": 10000,
    "sessions_multiplier": 3,  # 30K sessions pour 10K transactions
    "date_range_days": 90,     # 3 mois de données
}

# Sources de trafic
TRAFFIC_SOURCES = ["organic", "paid", "social", "email"]

# Catégories de produits (10 au total)
PRODUCT_CATEGORIES = [
    "Electronics", "Fashion", "Home", "Books", "Sports",
    "Beauty", "Toys", "Food", "Health", "Automotive"
]

# Configuration des prix par catégorie (min, max)
CATEGORY_PRICE_RANGES = {
    "Electronics": (50, 1500),
    "Fashion": (20, 300),
    "Home": (30, 800),
    "Books": (10, 50),
    "Sports": (25, 400),
    "Beauty": (15, 150),
    "Toys": (10, 100),
    "Food": (5, 80),
    "Health": (20, 200),
    "Automotive": (40, 1000)
}

# Pondération des sources (probabilités)
SOURCE_WEIGHTS = {
    "organic": 0.4,    # 40% du trafic
    "paid": 0.3,       # 30% du trafic
    "social": 0.2,     # 20% du trafic
    "email": 0.1       # 10% du trafic
}

# Taux de conversion par source
CONVERSION_RATES = {
    "organic": 0.035,   # 3.5%
    "paid": 0.045,      # 4.5%
    "social": 0.025,    # 2.5%
    "email": 0.055      # 5.5%
}

# Configuration Streamlit
STREAMLIT_CONFIG = {
    "page_title": "🛒 E-commerce KPIs Dashboard",
    "page_icon": "🛒",
    "layout": "wide"
}

# Formatage des métriques
METRIC_FORMATS = {
    "currency": "€{:,.0f}",
    "percentage": "{:.1f}%",
    "number": "{:,}"
}