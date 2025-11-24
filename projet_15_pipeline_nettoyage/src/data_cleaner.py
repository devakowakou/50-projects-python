"""Module principal de nettoyage des données."""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from rich.console import Console
from rich.progress import Progress, TaskID
import re
from datetime import datetime

console = Console()

class DataCleaner:
    """Nettoyeur de données avec stratégies configurables."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.cleaning_log = []
    
    def clean_dataframe(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Nettoie un DataFrame selon la configuration."""
        console.print("🧹 Début du nettoyage des données...")
        
        original_shape = df.shape
        df_cleaned = df.copy()
        
        with Progress() as progress:
            task = progress.add_task("Nettoyage en cours...", total=5)
            
            # 1. Nettoyage des valeurs manquantes
            df_cleaned = self._handle_missing_values(df_cleaned)
            progress.update(task, advance=1)
            
            # 2. Suppression des doublons
            df_cleaned = self._handle_duplicates(df_cleaned)
            progress.update(task, advance=1)
            
            # 3. Détection et traitement des outliers
            df_cleaned = self._handle_outliers(df_cleaned)
            progress.update(task, advance=1)
            
            # 4. Standardisation des formats
            df_cleaned = self._standardize_formats(df_cleaned)
            progress.update(task, advance=1)
            
            # 5. Validation finale
            df_cleaned = self._final_validation(df_cleaned)
            progress.update(task, advance=1)
        
        # Rapport de nettoyage
        cleaning_report = self._generate_cleaning_report(original_shape, df_cleaned.shape)
        
        console.print(f"✅ Nettoyage terminé : {original_shape[0]:,} → {df_cleaned.shape[0]:,} lignes")
        
        return df_cleaned, cleaning_report
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Gère les valeurs manquantes selon la stratégie configurée."""
        strategy = self.config['missing_values']['strategy']
        
        missing_before = df.isnull().sum().sum()
        
        if strategy == 'drop':
            df = df.dropna()
            self.cleaning_log.append(f"Suppression des lignes avec valeurs manquantes")
        
        elif strategy == 'mean':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            self.cleaning_log.append(f"Imputation par moyenne pour {len(numeric_cols)} colonnes numériques")
        
        elif strategy == 'median':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
            self.cleaning_log.append(f"Imputation par médiane pour {len(numeric_cols)} colonnes numériques")
        
        elif strategy == 'mode':
            for col in df.columns:
                if df[col].isnull().any():
                    mode_value = df[col].mode()
                    if len(mode_value) > 0:
                        df[col] = df[col].fillna(mode_value.iloc[0])
            self.cleaning_log.append("Imputation par mode pour toutes les colonnes")
        
        elif strategy == 'ffill':
            df = df.fillna(method='ffill')
            self.cleaning_log.append("Forward fill des valeurs manquantes")
        
        elif strategy == 'bfill':
            df = df.fillna(method='bfill')
            self.cleaning_log.append("Backward fill des valeurs manquantes")
        
        elif strategy == 'fill':
            fill_value = self.config['missing_values']['fill_value']
            df = df.fillna(fill_value)
            self.cleaning_log.append(f"Remplacement par valeur par défaut : {fill_value}")
        
        # Suppression des colonnes avec trop de valeurs manquantes
        threshold = self.config['missing_values']['drop_threshold']
        cols_to_drop = []
        for col in df.columns:
            missing_ratio = df[col].isnull().sum() / len(df)
            if missing_ratio > threshold:
                cols_to_drop.append(col)
        
        if cols_to_drop:
            df = df.drop(columns=cols_to_drop)
            self.cleaning_log.append(f"Suppression de {len(cols_to_drop)} colonnes avec >{threshold*100}% de valeurs manquantes")
        
        missing_after = df.isnull().sum().sum()
        console.print(f"  📊 Valeurs manquantes : {missing_before:,} → {missing_after:,}")
        
        return df
    
    def _handle_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Supprime les doublons."""
        duplicates_before = df.duplicated().sum()
        
        keep = self.config['duplicates']['keep']
        subset = self.config['duplicates']['subset']
        
        df = df.drop_duplicates(keep=keep, subset=subset)
        
        duplicates_removed = duplicates_before
        self.cleaning_log.append(f"Suppression de {duplicates_removed:,} doublons")
        
        console.print(f"  🔄 Doublons supprimés : {duplicates_removed:,}")
        
        return df
    
    def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Détecte et traite les outliers."""
        method = self.config['outliers']['method']
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        outliers_detected = 0
        
        for col in numeric_cols:
            if method == 'zscore':
                threshold = self.config['outliers']['zscore_threshold']
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outliers = z_scores > threshold
                
            elif method == 'iqr':
                threshold = self.config['outliers']['threshold']
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
                
            elif method == 'percentile':
                lower_p, upper_p = self.config['outliers']['percentile_bounds']
                lower_bound = df[col].quantile(lower_p / 100)
                upper_bound = df[col].quantile(upper_p / 100)
                outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
            
            # Traitement des outliers (ici on les remplace par les bornes)
            if outliers.any():
                outliers_count = outliers.sum()
                outliers_detected += outliers_count
                
                if method == 'iqr':
                    df.loc[outliers & (df[col] < lower_bound), col] = lower_bound
                    df.loc[outliers & (df[col] > upper_bound), col] = upper_bound
                elif method == 'percentile':
                    df.loc[outliers & (df[col] < lower_bound), col] = lower_bound
                    df.loc[outliers & (df[col] > upper_bound), col] = upper_bound
        
        if outliers_detected > 0:
            self.cleaning_log.append(f"Traitement de {outliers_detected:,} outliers par méthode {method}")
            console.print(f"  📈 Outliers traités : {outliers_detected:,}")
        
        return df
    
    def _standardize_formats(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardise les formats de données."""
        config = self.config['standardization']
        
        # Standardisation du texte
        text_cols = df.select_dtypes(include=['object']).columns
        
        for col in text_cols:
            if config['text_strip']:
                df[col] = df[col].astype(str).str.strip()
            
            if config['text_lowercase']:
                df[col] = df[col].astype(str).str.lower()
            
            if config['normalize_spaces']:
                df[col] = df[col].astype(str).str.replace(r'\s+', ' ', regex=True)
        
        # Standardisation des dates
        date_cols = df.select_dtypes(include=['datetime64']).columns
        date_format = config['date_format']
        
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Tentative de conversion de colonnes texte en dates
        for col in text_cols:
            if self._looks_like_date(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    self.cleaning_log.append(f"Conversion de {col} en format date")
                except:
                    pass
        
        self.cleaning_log.append("Standardisation des formats texte et dates")
        console.print("  🔤 Formats standardisés")
        
        return df
    
    def _looks_like_date(self, series: pd.Series) -> bool:
        """Vérifie si une série ressemble à des dates."""
        sample = series.dropna().head(10).astype(str)
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
        ]
        
        for pattern in date_patterns:
            matches = sample.str.match(pattern).sum()
            if matches > len(sample) * 0.8:  # 80% des valeurs matchent
                return True
        
        return False
    
    def _final_validation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validation finale et nettoyage des artefacts."""
        # Suppression des colonnes entièrement vides
        empty_cols = df.columns[df.isnull().all()].tolist()
        if empty_cols:
            df = df.drop(columns=empty_cols)
            self.cleaning_log.append(f"Suppression de {len(empty_cols)} colonnes vides")
        
        # Reset de l'index
        df = df.reset_index(drop=True)
        
        console.print("  ✅ Validation finale terminée")
        
        return df
    
    def _generate_cleaning_report(self, original_shape: Tuple[int, int], 
                                final_shape: Tuple[int, int]) -> Dict[str, Any]:
        """Génère un rapport de nettoyage."""
        return {
            'original_rows': original_shape[0],
            'original_columns': original_shape[1],
            'final_rows': final_shape[0],
            'final_columns': final_shape[1],
            'rows_removed': original_shape[0] - final_shape[0],
            'columns_removed': original_shape[1] - final_shape[1],
            'operations': self.cleaning_log.copy(),
            'cleaning_timestamp': datetime.now().isoformat()
        }