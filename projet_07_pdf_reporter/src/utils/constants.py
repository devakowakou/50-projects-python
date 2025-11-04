"""
Constantes globales de l'application
"""

# Extensions de fichiers supportées
SUPPORTED_EXCEL_EXTENSIONS = [".xlsx", ".xls"]

# Types de données pour validation
DATA_TYPES = {
    "numeric": ["int64", "float64", "int32", "float32"],
    "text": ["object", "string"],
    "datetime": ["datetime64[ns]", "datetime64"]
}

# Colonnes requises par template
REQUIRED_COLUMNS = {
    "commercial": ["Date", "Produit", "Quantité", "Prix", "CA"],
    "financier": ["Date", "Compte", "Débit", "Crédit", "Solde"],
    "technique": ["Timestamp", "Métrique", "Valeur", "Unité"]
}

# Palettes de couleurs
COLOR_PALETTES = {
    "default": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
    "professional": ["#003f5c", "#58508d", "#bc5090", "#ff6361", "#ffa600"],
    "pastel": ["#a8e6cf", "#dcedc1", "#ffd3b6", "#ffaaa5", "#ff8b94"]
}

# Messages d'erreur
ERROR_MESSAGES = {
    "no_file": "Aucun fichier n'a été uploadé",
    "invalid_extension": "Extension de fichier non supportée",
    "empty_data": "Le fichier ne contient aucune donnée",
    "missing_columns": "Colonnes requises manquantes",
    "invalid_template": "Template non reconnu"
}

# Status codes
STATUS = {
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "loading": "⏳"
}