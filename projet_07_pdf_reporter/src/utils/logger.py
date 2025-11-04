"""
Configuration du logging pour l'application
"""
import logging
import sys
from pathlib import Path
from config import LOG_LEVEL, LOG_FORMAT, BASE_DIR

def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    Configure et retourne un logger
    
    Args:
        name: Nom du logger
        log_file: Chemin du fichier de log (optionnel)
    
    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Formatter
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optionnel)
    if log_file:
        log_path = BASE_DIR / "logs"
        log_path.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_path / log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger