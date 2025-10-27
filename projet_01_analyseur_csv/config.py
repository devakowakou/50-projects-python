"""
Configuration globale pour l'analyseur CSV
"""

# Paramètres de l'application
APP_TITLE = "📊 Analyseur CSV Professionnel"
APP_ICON = "📈"
APP_LAYOUT = "wide"

# Paramètres de chargement des données
MAX_FILE_SIZE_MB = 200
SUPPORTED_FORMATS = ["csv", "xlsx", "xls"]
DEFAULT_ENCODING = "utf-8"
ALTERNATIVE_ENCODINGS = ["latin-1", "iso-8859-1", "cp1252"]

# Paramètres statistiques
CONFIDENCE_LEVEL = 0.95
OUTLIER_METHOD = "IQR"  # Options: "IQR", "Z-Score"
IQR_MULTIPLIER = 1.5
Z_SCORE_THRESHOLD = 3

# Paramètres de corrélation
CORRELATION_METHODS = ["pearson", "spearman", "kendall"]
CORRELATION_THRESHOLD = 0.7  # Seuil pour corrélations significatives

# Paramètres de visualisation
PLOTLY_THEME = "plotly_white"
COLOR_PALETTE = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

# Paramètres de nettoyage
MISSING_VALUE_STRATEGIES = {
    "Supprimer les lignes": "drop",
    "Remplir avec la moyenne": "mean",
    "Remplir avec la médiane": "median",
    "Remplir avec le mode": "mode",
    "Remplir avec une valeur personnalisée": "custom"
}

# Messages d'erreur
ERROR_MESSAGES = {
    "file_not_found": "❌ Fichier introuvable",
    "invalid_format": "❌ Format de fichier non supporté",
    "empty_file": "❌ Le fichier est vide",
    "encoding_error": "❌ Erreur d'encodage du fichier",
    "no_numeric_columns": "⚠️ Aucune colonne numérique détectée"
}

# Messages de succès
SUCCESS_MESSAGES = {
    "file_loaded": "✅ Fichier chargé avec succès",
    "data_cleaned": "✅ Données nettoyées",
    "analysis_complete": "✅ Analyse terminée"
}
