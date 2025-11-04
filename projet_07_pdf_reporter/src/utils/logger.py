"""
Configuration du système de logging
"""
import logging
import sys
from config import LOG_LEVEL, LOG_FORMAT, LOG_FILE

def setup_logger(name: str = "pdf_reporter") -> logging.Logger:
    """
    Configure et retourne un logger
    
    Args:
        name: Nom du logger
        
    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name)
    
    # Éviter duplication des handlers
    if logger.handlers:
        return logger
    
    # Niveau de log
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Format
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Handler console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler fichier
    try:
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Impossible de créer le fichier de log: {e}")
    
    return logger