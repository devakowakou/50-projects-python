"""
Formatage des éléments pour le PDF
"""
from typing import Any, List
from datetime import datetime

def format_currency(value: float, symbol: str = "€") -> str:
    """Formate une valeur monétaire"""
    return f"{value:,.2f} {symbol}".replace(",", " ")

def format_percentage(value: float) -> str:
    """Formate un pourcentage"""
    return f"{value:.2f}%"

def format_number(value: float, decimals: int = 2) -> str:
    """Formate un nombre avec séparateurs"""
    return f"{value:,.{decimals}f}".replace(",", " ")

def format_date(date: Any, format_str: str = "%d/%m/%Y") -> str:
    """Formate une date"""
    if isinstance(date, str):
        try:
            date = datetime.fromisoformat(date)
        except:
            return date
    
    if hasattr(date, 'strftime'):
        return date.strftime(format_str)
    return str(date)

def truncate_text(text: str, max_length: int = 50) -> str:
    """Tronque un texte"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def prepare_table_data(data: List[List], headers: List[str] = None) -> List[List]:
    """
    Prépare les données pour une table PDF
    
    Args:
        data: Données brutes
        headers: En-têtes de colonnes
    
    Returns:
        Données formatées avec headers
    """
    table_data = []
    
    if headers:
        table_data.append(headers)
    
    for row in data:
        formatted_row = []
        for cell in row:
            if isinstance(cell, float):
                formatted_row.append(format_number(cell))
            elif isinstance(cell, (int, complex)):
                formatted_row.append(str(cell))
            else:
                formatted_row.append(str(cell))
        table_data.append(formatted_row)
    
    return table_data