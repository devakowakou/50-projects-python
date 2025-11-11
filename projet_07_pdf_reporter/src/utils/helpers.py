"""
Fonctions utilitaires diverses
"""
from datetime import datetime
from pathlib import Path
from typing import Union
import pandas as pd
import warnings

def generate_filename(prefix: str, extension: str = "pdf") -> str:
    """
    Génère un nom de fichier unique avec timestamp
    
    Args:
        prefix: Préfixe du nom de fichier
        extension: Extension (sans le point)
    
    Returns:
        Nom de fichier avec timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def validate_file_path(path: Union[str, Path]) -> Path:
    """
    Valide et convertit un chemin en Path
    
    Args:
        path: Chemin du fichier
    
    Returns:
        Path object
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {path}")
    return path

def format_number(value: float, decimals: int = 2, suffix: str = "") -> str:
    """
    Formate un nombre avec séparateurs de milliers
    
    Args:
        value: Valeur à formater
        decimals: Nombre de décimales
        suffix: Suffixe optionnel (€, %, etc.)
    
    Returns:
        Nombre formaté
    """
    formatted = f"{value:,.{decimals}f}".replace(",", " ")
    return f"{formatted}{suffix}" if suffix else formatted

def detect_date_columns(df: pd.DataFrame) -> list:
    """
    Détecte les colonnes de dates dans un DataFrame
    
    Args:
        df: DataFrame à analyser
    
    Returns:
        Liste des noms de colonnes de type date
    """
    date_columns = []
    
    for col in df.columns:
        # Vérifier si déjà datetime
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            date_columns.append(col)
        # Essayer de convertir les colonnes object
        elif df[col].dtype == "object":
            try:
                # Supprimer les warnings et essayer la conversion
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    # Essayer sur un échantillon d'abord
                    sample = df[col].dropna().head(10)
                    if len(sample) > 0:
                        pd.to_datetime(sample, errors="raise")
                        date_columns.append(col)
            except (ValueError, TypeError):
                # Pas une colonne de dates
                pass
    
    return date_columns

def safe_division(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Division sécurisée (évite division par zéro)
    
    Args:
        numerator: Numérateur
        denominator: Dénominateur
        default: Valeur par défaut si division impossible
    
    Returns:
        Résultat de la division ou valeur par défaut
    """
    try:
        return numerator / denominator if denominator != 0 else default
    except:
        return default