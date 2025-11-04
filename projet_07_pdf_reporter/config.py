"""
Configuration globale du projet
"""
import os
from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
SAMPLES_DIR = DATA_DIR / "samples"
OUTPUTS_DIR = BASE_DIR / "outputs"
TEMPLATES_DIR = BASE_DIR / "templates"
TESTS_DIR = BASE_DIR / "tests"

# Création des dossiers si nécessaire
OUTPUTS_DIR.mkdir(exist_ok=True)
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

# Configuration des templates disponibles
TEMPLATES = {
    "commercial": {
        "name": "Rapport Commercial",
        "description": "KPIs commerciaux, ventes, performances",
        "config_file": TEMPLATES_DIR / "commercial" / "template.json",
        "styles": TEMPLATES_DIR / "commercial" / "styles.css"
    },
    "financier": {
        "name": "Rapport Financier",
        "description": "États financiers, ratios, analyses",
        "config_file": TEMPLATES_DIR / "financier" / "template.json",
        "styles": TEMPLATES_DIR / "financier" / "styles.css"
    },
    "technique": {
        "name": "Rapport Technique",
        "description": "Métriques techniques, performances",
        "config_file": TEMPLATES_DIR / "technique" / "template.json",
        "styles": TEMPLATES_DIR / "technique" / "styles.css"
    }
}

# Configuration PDF
PDF_CONFIG = {
    "page_size": "A4",
    "margin": 2,  # cm
    "font_name": "Helvetica",
    "font_size": 10
}

# Configuration graphiques
CHART_CONFIG = {
    "dpi": 150,
    "figsize": (10, 6),
    "style": "seaborn-v0_8",
    "color_palette": "Set2"
}

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"