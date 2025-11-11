"""
Configuration globale du projet PDF Reporter
"""
from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUTS_DIR = BASE_DIR / "outputs"
TEMP_DIR = BASE_DIR / "temp"
LOGS_DIR = BASE_DIR / "logs"

# Créer les dossiers si inexistants
for directory in [DATA_DIR, TEMPLATES_DIR, OUTPUTS_DIR, TEMP_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# Configuration Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "app.log"

# Configuration Excel
EXCEL_CONFIG = {
    "max_file_size_mb": 50,
    "allowed_extensions": [".xlsx", ".xls"],
    "encoding": "utf-8"
}

# Configuration PDF
PDF_CONFIG = {
    "page_size": "A4",
    "margin": 20,
    "font_family": "Helvetica",
    "font_size": 11,
    "title_size": 18,
    "header_size": 14
}

# Configuration graphiques
CHART_CONFIG = {
    "figure_size": (10, 6),
    "dpi": 100,
    "style": "seaborn-v0_8-darkgrid",
    "colors": ["#2E86AB", "#A23B72", "#06A77D", "#F18F01", "#C73E1D"]
}

# Configuration KPIs
KPI_CONFIG = {
    "decimal_places": 2,
    "thousand_separator": " ",
    "currency_symbol": "€",
    "percentage_format": "{:.2f}%"
}

# Templates disponibles
TEMPLATES = {
    "commercial": {
        "name": "Rapport Commercial",
        "description": "Rapport d'analyse commerciale",
        "kpis": ["chiffre_affaires", "nombre_ventes", "panier_moyen", "taux_conversion"],
        "charts": ["evolution_ventes", "top_produits", "repartition_ca"],
        "sections": ["synthese", "performance", "tendances", "recommandations"],
        "colors": {
            "primary": "#2E86AB",
            "secondary": "#A23B72",
            "success": "#06A77D",
            "warning": "#F18F01"
        }
    },
    "financier": {
        "name": "Rapport Financier",
        "description": "Rapport d'analyse financière",
        "kpis": ["revenus", "depenses", "benefice_net", "marge_beneficiaire"],
        "charts": ["evolution_tresorerie", "repartition_charges", "analyse_rentabilite"],
        "sections": ["synthese", "revenus", "depenses", "analyse"],
        "colors": {
            "primary": "#1B4965",
            "secondary": "#62B6CB",
            "success": "#5FA052",
            "warning": "#EE964B"
        }
    },
    "ressources_humaines": {
        "name": "Rapport RH",
        "description": "Rapport des ressources humaines",
        "kpis": ["effectif_total", "taux_turnover", "masse_salariale", "taux_absenteisme"],
        "charts": ["evolution_effectif", "pyramide_ages", "repartition_services"],
        "sections": ["effectifs", "mobilite", "formation", "social"],
        "colors": {
            "primary": "#6A4C93",
            "secondary": "#8AC926",
            "success": "#1982C4",
            "warning": "#FFCA3A"
        }
    }
}

# Templates par défaut (alias pour rétrocompatibilité)
DEFAULT_TEMPLATES = {
    "commercial": "Rapport d'analyse commerciale",
    "financier": "Rapport d'analyse financière",
    "ressources_humaines": "Rapport des ressources humaines"
}

# Validation
VALIDATION_RULES = {
    "min_rows": 1,
    "max_rows": 100000,
    "required_numeric_ratio": 0.1  # Au moins 10% de colonnes numériques
}