"""
Configuration des paramètres de performance
Version 2.2 - Optimisations
"""

# ============= LIMITES DE FICHIERS =============
MAX_FILE_SIZE_MB = 500  # Taille maximale de fichier (MB)
CHUNK_THRESHOLD_MB = 10  # Seuil pour chargement par chunks (MB)
CHUNK_SIZE_ROWS = 50_000  # Nombre de lignes par chunk

# ============= ÉCHANTILLONNAGE =============
ENABLE_AUTO_SAMPLING = True  # Activer échantillonnage automatique
SAMPLE_THRESHOLD_ROWS = 100_000  # Seuil pour échantillonnage (lignes)
SAMPLE_SIZE_CORRELATION = 50_000  # Taille échantillon pour corrélations
SAMPLE_SIZE_VISUALIZATION = 10_000  # Taille échantillon pour visualisations

# ============= PARALLÉLISATION =============
ENABLE_PARALLEL_PROCESSING = True  # Activer parallélisation
MAX_WORKERS = 4  # Nombre de threads pour calculs parallèles
MIN_COLUMNS_FOR_PARALLEL = 3  # Nombre minimum de colonnes pour parallélisation

# ============= LIMITES DE COLONNES =============
MAX_COLUMNS_CORRELATION = 50  # Nombre max de colonnes pour matrice corrélation
MAX_BINS_HISTOGRAM = 50  # Nombre max de bins pour histogrammes

# ============= CACHE =============
ENABLE_CACHE = True  # Activer système de cache
CACHE_TTL = 3600  # Durée de vie du cache (secondes)

# ============= ENCODAGE =============
ENCODING_SAMPLE_SIZE = 10_000  # Taille échantillon pour détection encodage (bytes)

# ============= AFFICHAGE =============
SHOW_PERFORMANCE_METRICS = True  # Afficher temps d'exécution
SHOW_MEMORY_USAGE = True  # Afficher utilisation mémoire
SHOW_SAMPLE_WARNINGS = True  # Avertir quand échantillonnage actif

# ============= TIMEOUTS =============
MAX_OPERATION_TIME = 300  # Timeout max pour une opération (secondes)

# ============= MESSAGES =============
MESSAGES = {
    'large_file_warning': " Fichier volumineux détecté. Optimisations activées.",
    'sampling_active': " Échantillonnage activé : {sample_size:,} lignes sur {total_size:,}",
    'parallel_processing': "⚡ Traitement parallèle activé ({workers} threads)",
    'cache_hit': "✓ Résultat en cache",
    'performance_tip': " Pour de meilleures performances, réduisez le nombre de colonnes ou la taille du fichier"
}

# ============= PROFILING =============
ENABLE_PROFILING = False  # Mode debug - profiler les performances
LOG_SLOW_OPERATIONS = True  # Logger les opérations lentes (> 5 secondes)
SLOW_OPERATION_THRESHOLD = 5.0  # Seuil pour opération lente (secondes)
