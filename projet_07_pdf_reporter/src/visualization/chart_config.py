"""
Configuration des styles et paramètres des graphiques
"""
from src.utils.constants import COLOR_PALETTES
from config import CHART_CONFIG

# Styles matplotlib
MATPLOTLIB_STYLE = "seaborn-v0_8"

# Configuration par type de graphique
CHART_STYLES = {
    "line": {
        "linewidth": 2,
        "marker": "o",
        "markersize": 4,
        "alpha": 0.8
    },
    "bar": {
        "width": 0.7,
        "alpha": 0.8,
        "edgecolor": "white"
    },
    "pie": {
        "autopct": "%1.1f%%",
        "startangle": 90,
        "explode_max": 0.1
    },
    "scatter": {
        "s": 50,
        "alpha": 0.6,
        "edgecolors": "black",
        "linewidth": 0.5
    }
}

# Dimensions des graphiques
FIGURE_SIZES = {
    "small": (8, 4),
    "medium": (10, 6),
    "large": (12, 8),
    "wide": (14, 6)
}

# Configuration des axes
AXIS_CONFIG = {
    "grid": True,
    "grid_alpha": 0.3,
    "grid_linestyle": "--",
    "title_fontsize": 14,
    "label_fontsize": 11,
    "tick_fontsize": 9
}

# Palettes de couleurs par template
TEMPLATE_COLORS = {
    "commercial": COLOR_PALETTES["professional"],
    "financier": COLOR_PALETTES["default"],
    "technique": COLOR_PALETTES["pastel"]
}

def get_chart_config(chart_type: str = "line", size: str = "medium") -> dict:
    """
    Retourne la configuration pour un type de graphique
    
    Args:
        chart_type: Type de graphique
        size: Taille du graphique
    
    Returns:
        Configuration complète
    """
    config = {
        "figsize": FIGURE_SIZES.get(size, FIGURE_SIZES["medium"]),
        "dpi": CHART_CONFIG["dpi"],
        "style": CHART_STYLES.get(chart_type, {}),
        "axis": AXIS_CONFIG
    }
    
    return config