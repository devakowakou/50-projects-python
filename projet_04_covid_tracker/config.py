"""
Configuration globale pour le COVID-19 Tracker
"""

# ========================================
# SOURCE DE DONNÉES
# ========================================

# Our World in Data - GitHub (données complètes)
COVID_DATA_URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# Colonnes à charger (pour optimiser la mémoire)
COLUMNS_TO_LOAD = [
    'iso_code',
    'continent',
    'location',
    'date',
    'total_cases',
    'new_cases',
    'total_deaths',
    'new_deaths',
    'total_vaccinations',
    'people_vaccinated',
    'people_fully_vaccinated',
    'population',
    'total_cases_per_million',
    'total_deaths_per_million',
]

# Cache local
DATA_CACHE_PATH = 'data/covid_data.csv'
CACHE_EXPIRY_HOURS = 24  # Recharger les données après 24h


# ========================================
# CONFIGURATION INTERFACE
# ========================================

APP_TITLE = "COVID-19 Global Tracker"
APP_ICON = "🦠"

# Pays par défaut
DEFAULT_COUNTRIES = ['France', 'United States', 'Germany', 'Italy', 'Spain']

# Nombre max de pays comparables
MAX_COUNTRIES_COMPARISON = 10

# Périodes prédéfinies
PRESET_PERIODS = {
    '7 derniers jours': 7,
    '30 derniers jours': 30,
    '3 derniers mois': 90,
    '6 derniers mois': 180,
    '1 an': 365,
    'Toute la période': None
}


# ========================================
# CONFIGURATION VISUALISATIONS
# ========================================

# Couleurs des graphiques
COLOR_CASES = '#FF9900'
COLOR_DEATHS = '#B12704'
COLOR_VACCINATIONS = '#067D62'
COLOR_RECOVERED = '#4CAF50'

# Template Plotly
PLOTLY_TEMPLATE = 'plotly_white'

# Hauteur des graphiques
CHART_HEIGHT = 400


# ========================================
# MÉTRIQUES CALCULÉES
# ========================================

# Fenêtre pour moyenne mobile
ROLLING_WINDOW = 7

# Seuils d'alerte (cas pour 100k habitants)
ALERT_THRESHOLD_LOW = 50
ALERT_THRESHOLD_MEDIUM = 150
ALERT_THRESHOLD_HIGH = 300
