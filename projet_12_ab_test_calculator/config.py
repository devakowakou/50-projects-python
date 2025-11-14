"""Configuration pour la Calculatrice A/B Test"""

STATISTICAL_TESTS = {
    "t_test": {"name": "T-Test", "description": "Compare moyennes"},
    "z_test": {"name": "Z-Test", "description": "Compare proportions"},
    "chi2_test": {"name": "Chi-carré", "description": "Test indépendance"}
}

CONFIDENCE_LEVELS = [0.90, 0.95, 0.99]
POWER_LEVELS = [0.80, 0.85, 0.90, 0.95]
EFFECT_SIZES = {"small": 0.2, "medium": 0.5, "large": 0.8}

COLORS = {
    "group_a": "#1f77b4",
    "group_b": "#ff7f0e", 
    "significant": "#2ca02c",
    "not_significant": "#d62728"
}