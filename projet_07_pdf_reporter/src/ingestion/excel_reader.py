"""
Module de lecture et extraction de données Excel
"""
import pandas as pd
from pathlib import Path
from typing import Union, Optional, List, Dict
from src.utils.logger import setup_logger
from src.utils.constants import SUPPORTED_EXCEL_EXTENSIONS

logger = setup_logger(__name__)

class ExcelReader:
    """Classe pour lire et extraire des données depuis fichiers Excel"""
    
    def __init__(self):
        self.current_file = None
        self.sheets = []
    
    def read_excel(
        self, 
        file_path: Union[str, Path], 
        sheet_name: Optional[Union[str, int]] = 0,
        **kwargs
    ) -> pd.DataFrame:
        """
        Lit un fichier Excel et retourne un DataFrame
        
        Args:
            file_path: Chemin du fichier Excel
            sheet_name: Nom ou index de la feuille (0 par défaut)
            **kwargs: Arguments supplémentaires pour pd.read_excel
        
        Returns:
            DataFrame contenant les données
        
        Raises:
            ValueError: Si extension non supportée
            FileNotFoundError: Si fichier introuvable
        """
        file_path = Path(file_path)
        
        # Validation extension
        if file_path.suffix not in SUPPORTED_EXCEL_EXTENSIONS:
            raise ValueError(
                f"Extension {file_path.suffix} non supportée. "
                f"Extensions valides: {', '.join(SUPPORTED_EXCEL_EXTENSIONS)}"
            )
        
        # Validation existence
        if not file_path.exists():
            raise FileNotFoundError(f"Fichier introuvable: {file_path}")
        
        logger.info(f"Lecture du fichier: {file_path.name}")
        
        try:
            df = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                engine="openpyxl",
                **kwargs
            )
            
            self.current_file = file_path
            logger.info(
                f"✅ Fichier lu avec succès: {len(df)} lignes, "
                f"{len(df.columns)} colonnes"
            )
            
            return df
            
        except Exception as e:
            logger.error(f"Erreur lors de la lecture: {str(e)}")
            raise
    
    def get_sheet_names(self, file_path: Union[str, Path]) -> List[str]:
        """
        Récupère la liste des noms de feuilles dans un fichier Excel
        
        Args:
            file_path: Chemin du fichier Excel
        
        Returns:
            Liste des noms de feuilles
        """
        file_path = Path(file_path)
        
        try:
            excel_file = pd.ExcelFile(file_path, engine="openpyxl")
            self.sheets = excel_file.sheet_names
            logger.info(f"Feuilles détectées: {', '.join(self.sheets)}")
            return self.sheets
            
        except Exception as e:
            logger.error(f"Erreur lors de la lecture des feuilles: {str(e)}")
            raise
    
    def infer_schema(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Analyse le schéma d'un DataFrame
        
        Args:
            df: DataFrame à analyser
        
        Returns:
            Dictionnaire {colonne: type}
        """
        schema = {}
        for col in df.columns:
            dtype = str(df[col].dtype)
            schema[col] = dtype
        
        logger.info(f"Schéma détecté: {len(schema)} colonnes")
        return schema
    
    def get_metadata(self, file_path: Union[str, Path]) -> Dict:
        """
        Extrait les métadonnées d'un fichier Excel
        
        Args:
            file_path: Chemin du fichier
        
        Returns:
            Dictionnaire de métadonnées
        """
        file_path = Path(file_path)
        
        metadata = {
            "filename": file_path.name,
            "size_bytes": file_path.stat().st_size,
            "size_mb": round(file_path.stat().st_size / (1024*1024), 2),
            "modified": pd.Timestamp.fromtimestamp(
                file_path.stat().st_mtime
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "sheets": self.get_sheet_names(file_path)
        }
        
        return metadata