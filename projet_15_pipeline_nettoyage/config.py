"""Configuration du pipeline de nettoyage de données."""

from typing import Dict, Any, List
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEANED_DATA_DIR = DATA_DIR / "cleaned"
REPORTS_DIR = DATA_DIR / "reports"

# Configuration du nettoyage
CLEANING_CONFIG: Dict[str, Any] = {
    'missing_values': {
        'strategy': 'median',  # mean, median, mode, drop, fill, ffill, bfill
        'fill_value': None,
        'drop_threshold': 0.5  # Supprimer colonnes avec >50% de valeurs manquantes
    },
    'outliers': {
        'method': 'iqr',  # zscore, iqr, percentile
        'threshold': 1.5,  # Pour IQR
        'zscore_threshold': 3,  # Pour Z-score
        'percentile_bounds': (1, 99)  # Pour percentiles
    },
    'duplicates': {
        'keep': 'first',  # first, last, False
        'subset': None  # Colonnes à considérer pour doublons
    },
    'standardization': {
        'text_lowercase': True,
        'text_strip': True,
        'date_format': '%Y-%m-%d',
        'normalize_spaces': True
    }
}

# Types de fichiers supportés
SUPPORTED_FORMATS: List[str] = ['.csv', '.xlsx', '.xls', '.json', '.parquet']

# Configuration d'export
EXPORT_CONFIG: Dict[str, Any] = {
    'csv': {'index': False, 'encoding': 'utf-8'},
    'parquet': {'index': False, 'compression': 'snappy'},
    'json': {'orient': 'records', 'indent': 2}
}

# Configuration des rapports
REPORT_CONFIG: Dict[str, Any] = {
    'include_plots': True,
    'plot_format': 'png',
    'detailed_stats': True,
    'export_formats': ['json', 'txt']
}

# Limites de performance
PERFORMANCE_LIMITS: Dict[str, int] = {
    'max_rows_memory': 1_000_000,  # Basculer vers chunking au-delà
    'chunk_size': 10_000,
    'max_file_size_mb': 500
}