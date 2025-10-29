"""
Configuration globale pour le Amazon Price Tracker
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# ========================================
# CONFIGURATION AMAZON
# ========================================

# Domaine Amazon à scraper
AMAZON_DOMAIN = os.getenv('AMAZON_DOMAIN', 'amazon.fr')

# Sélecteurs CSS pour le prix (multiples fallbacks)
PRICE_SELECTORS = [
    'span.a-price-whole',
    'span#priceblock_ourprice',
    'span.a-offscreen',
    'span#priceblock_dealprice',
    'span.priceToPay span.a-price-whole',
]

# Sélecteurs CSS pour le nom du produit
NAME_SELECTORS = [
    'span#productTitle',
    'h1#title',
    'h1.a-size-large',
]

# Sélecteurs CSS pour l'image
IMAGE_SELECTORS = [
    'img#landingImage',
    'img.a-dynamic-image',
    'div#imgTagWrapperId img',
]

# Sélecteurs CSS pour la disponibilité
AVAILABILITY_SELECTORS = [
    'div#availability span',
    'span.a-size-medium.a-color-success',
    'span.a-size-medium.a-color-price',
]

# User-Agents pour rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

# Délai entre les requêtes (secondes)
REQUEST_DELAY = 2

# Nombre de tentatives en cas d'échec
MAX_RETRIES = 3

# Timeout pour les requêtes (secondes)
REQUEST_TIMEOUT = 10


# ========================================
# CONFIGURATION EMAIL
# ========================================

SMTP_EMAIL = os.getenv('SMTP_EMAIL', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))

# Template email
EMAIL_SUBJECT = "🔔 Alerte Prix Amazon - {product_name}"
EMAIL_TEMPLATE = """
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #FF9900; color: white; padding: 20px; text-align: center; }}
        .content {{ background-color: #f9f9f9; padding: 20px; }}
        .price {{ font-size: 24px; font-weight: bold; color: #B12704; }}
        .target {{ font-size: 18px; color: #067D62; }}
        .button {{ background-color: #FF9900; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Alerte Prix Amazon</h1>
        </div>
        <div class="content">
            <h2>{product_name}</h2>
            <p>Le prix du produit que vous suivez a atteint votre objectif !</p>
            <p>Prix actuel : <span class="price">{current_price} €</span></p>
            <p>Prix cible : <span class="target">{target_price} €</span></p>
            <p>Économie potentielle : <strong>{savings} €</strong></p>
            <a href="{product_url}" class="button">Voir le produit sur Amazon</a>
        </div>
    </div>
</body>
</html>
"""


# ========================================
# CONFIGURATION BASE DE DONNÉES
# ========================================

DB_PATH = 'data/tracker.db'


# ========================================
# CONFIGURATION INTERFACE
# ========================================

# Titre de l'application
APP_TITLE = "Amazon Price Tracker"
APP_ICON = "🛒"

# Nombre de jours pour l'historique par défaut
DEFAULT_HISTORY_DAYS = 30

# Limite de produits trackables (MVP)
MAX_PRODUCTS = 20

# Couleurs des alertes
COLOR_SUCCESS = "#067D62"
COLOR_WARNING = "#FF9900"
COLOR_DANGER = "#B12704"
