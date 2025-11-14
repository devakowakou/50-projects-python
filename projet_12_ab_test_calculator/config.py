"""
Configuration pour la Calculatrice A/B Test
"""

# Configuration des tests statistiques
STATISTICAL_TESTS = {
    "t_test": {
        "name": "T-Test (moyennes)",
        "description": "Compare les moyennes de deux groupes",
        "use_case": "Revenus, temps sur site, panier moyen"
    },
    "z_test": {
        "name": "Z-Test (proportions)",
        "description": "Compare les proportions de deux groupes",
        "use_case": "Taux de conversion, taux de clic"
    },
    "chi2_test": {
        "name": "Chi-carré",
        "description": "Test d'indépendance entre variables",
        "use_case": "Catégories, segments"
    }
}

# Niveaux de confiance standards
CONFIDENCE_LEVELS = [0.90, 0.95, 0.99]
DEFAULT_CONFIDENCE = 0.95

# Puissance statistique
POWER_LEVELS = [0.80, 0.85, 0.90, 0.95]
DEFAULT_POWER = 0.80

# Tailles d'effet
EFFECT_SIZES = {
    "small": 0.2,
    "medium": 0.5,
    "large": 0.8
}

# Configuration Streamlit
STREAMLIT_CONFIG = {
    "page_title": "📊 A/B Test Calculator",
    "page_icon": "📊",
    "layout": "wide"
}

# Couleurs pour les graphiques
COLORS = {
    "group_a": "#1f77b4",  # Bleu
    "group_b": "#ff7f0e",  # Orange
    "significant": "#2ca02c",  # Vert
    "not_significant": "#d62728"  # Rouge
}

# Messages d'interprétation
INTERPRETATION = {
    "significant": "✅ Différence statistiquement significative",
    "not_significant": "❌ Pas de différence significative",
    "underpowered": "⚠️ Test sous-puissant, augmentez la taille d'échantillon"
}