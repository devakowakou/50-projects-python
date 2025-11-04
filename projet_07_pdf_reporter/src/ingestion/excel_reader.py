"""
Lecteur de fichiers Excel
"""
import pandas as pd
from pathlib import Path
from typing import Optional
from config import EXCEL_CONFIG

class ExcelReader:
    """Lecteur de fichiers Excel avec gestion robuste"""
    
    def __init__(self):
        self.max_file_size = EXCEL_CONFIG["max_file_size_mb"] * 1024 * 1024
    
    def read_excel(self, file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """
        Lit un fichier Excel et retourne un DataFrame
        
        Args:
            file_path: Chemin du fichier
            sheet_name: Nom de la feuille (None = première feuille)
            
        Returns:
            DataFrame avec les données
        """
        path = Path(file_path)
        
        # Vérifier existence
        if not path.exists():
            raise FileNotFoundError(f"Fichier introuvable: {file_path}")
        
        # Vérifier taille
        if path.stat().st_size > self.max_file_size:
            raise ValueError(f"Fichier trop volumineux (max {EXCEL_CONFIG['max_file_size_mb']} Mo)")
        
        # Vérifier extension
        if path.suffix not in EXCEL_CONFIG["allowed_extensions"]:
            raise ValueError(f"Extension invalide. Formats acceptés: {EXCEL_CONFIG['allowed_extensions']}")
        
        try:
            # Lecture du fichier
            df = pd.read_excel(file_path, sheet_name=sheet_name or 0)
            
            # Nettoyage basique
            df = self._clean_dataframe(df)
            
            return df
            
        except Exception as e:
            raise Exception(f"Erreur lecture Excel: {str(e)}")
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Nettoyage basique du DataFrame
        
        Args:
            df: DataFrame à nettoyer
            
        Returns:
            DataFrame nettoyé
        """
        # Supprimer colonnes entièrement vides
        df = df.dropna(axis=1, how='all')
        
        # Supprimer lignes entièrement vides
        df = df.dropna(axis=0, how='all')
        
        # Nettoyer les noms de colonnes
        df.columns = df.columns.str.strip()
        
        # Reset index
        df = df.reset_index(drop=True)
        
        return df
    
    def get_sheet_names(self, file_path: str) -> list:
        """
        Récupère les noms des feuilles du fichier Excel
        
        Args:
            file_path: Chemin du fichier
            
        Returns:
            Liste des noms de feuilles
        """
        try:
            excel_file = pd.ExcelFile(file_path)
            return excel_file.sheet_names
        except Exception as e:
            raise Exception(f"Erreur lecture feuilles: {str(e)}")