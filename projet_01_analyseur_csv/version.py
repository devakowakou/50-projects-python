"""
Version de l'application
"""

__version__ = "2.2.0"
__version_name__ = "Performance Boost"
__release_date__ = "2025-10-28"
__status__ = "Production"

VERSION_INFO = {
    'version': __version__,
    'version_name': __version_name__,
    'release_date': __release_date__,
    'status': __status__,
    'python_required': '>=3.9',
    'main_features': [
        'Chargement optimisé par chunks',
        'Statistiques en un seul passage',
        'Corrélations avec échantillonnage',
        'Détection d\'anomalies parallélisée',
        'Visualisations optimisées',
        'Système de cache intégré',
        'Monitoring de performance'
    ],
    'performance_gains': {
        'chargement': '40-50%',
        'statistiques': '80-90%',
        'correlations': '60-70%',
        'anomalies': '50-60%',
        'visualisations': '70-80%',
        'global': '5-10x plus rapide'
    }
}

def get_version_string() -> str:
    """Retourne la version formatée"""
    return f"v{__version__} - {__version_name__} ({__release_date__})"

def print_version_info():
    """Affiche les informations de version"""
    print(f"Analyseur CSV Professionnel")
    print(f"Version: {__version__} ({__version_name__})")
    print(f"Date: {__release_date__}")
    print(f"Statut: {__status__}")
    print(f"\nOptimisations:")
    for feature in VERSION_INFO['main_features']:
        print(f"  • {feature}")
    print(f"\nGains de performance:")
    for module, gain in VERSION_INFO['performance_gains'].items():
        print(f"  • {module.capitalize()}: {gain}")
