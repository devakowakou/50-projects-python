"""Module de chargement de données multi-formats."""

import pandas as pd
import json
import chardet
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from rich.console import Console

console = Console()

class DataLoader:
    """Chargeur de données intelligent pour multiple formats."""
    
    def __init__(self):
        self.supported_formats = {'.csv', '.xlsx', '.xls', '.json', '.parquet'}
    
    def load_file(self, file_path: Path) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Charge un fichier et retourne le DataFrame + métadonnées."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Fichier non trouvé : {file_path}")
        
        suffix = file_path.suffix.lower()
        if suffix not in self.supported_formats:
            raise ValueError(f"Format non supporté : {suffix}")
        
        console.print(f"📂 Chargement de {file_path.name}...")
        
        metadata = {
            'filename': file_path.name,
            'size_mb': file_path.stat().st_size / (1024 * 1024),
            'format': suffix
        }
        
        try:
            if suffix == '.csv':
                df, csv_meta = self._load_csv(file_path)
                metadata.update(csv_meta)
            elif suffix in ['.xlsx', '.xls']:
                df = self._load_excel(file_path)
            elif suffix == '.json':
                df = self._load_json(file_path)
            elif suffix == '.parquet':
                df = pd.read_parquet(file_path)
            
            metadata.update({
                'rows': len(df),
                'columns': len(df.columns),
                'memory_mb': df.memory_usage(deep=True).sum() / (1024 * 1024)
            })
            
            console.print(f"✅ Chargé : {metadata['rows']:,} lignes, {metadata['columns']} colonnes")
            return df, metadata
            
        except Exception as e:
            console.print(f"❌ Erreur de chargement : {e}")
            raise
    
    def _load_csv(self, file_path: Path) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Charge un CSV avec détection d'encodage."""
        # Détection d'encodage
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)
            encoding_result = chardet.detect(raw_data)
            encoding = encoding_result['encoding'] or 'utf-8'
        
        # Tentative de chargement avec différents séparateurs
        separators = [',', ';', '\t', '|']
        
        for sep in separators:
            try:
                df = pd.read_csv(file_path, encoding=encoding, sep=sep, nrows=5)
                if len(df.columns) > 1:  # Séparateur trouvé
                    df_full = pd.read_csv(file_path, encoding=encoding, sep=sep)
                    return df_full, {'encoding': encoding, 'separator': sep}
            except:
                continue
        
        # Fallback
        df = pd.read_csv(file_path, encoding=encoding)
        return df, {'encoding': encoding, 'separator': ','}
    
    def _load_excel(self, file_path: Path) -> pd.DataFrame:
        """Charge un fichier Excel."""
        return pd.read_excel(file_path)
    
    def _load_json(self, file_path: Path) -> pd.DataFrame:
        """Charge un fichier JSON."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            return pd.DataFrame([data])
        else:
            raise ValueError("Format JSON non supporté")
    
    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Retourne les informations d'un fichier sans le charger."""
        file_path = Path(file_path)
        
        return {
            'name': file_path.name,
            'size_mb': file_path.stat().st_size / (1024 * 1024),
            'format': file_path.suffix.lower(),
            'supported': file_path.suffix.lower() in self.supported_formats
        }