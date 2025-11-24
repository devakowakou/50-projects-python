"""Module de profilage automatique des données."""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from rich.console import Console
from rich.table import Table

console = Console()

class DataProfiler:
    """Analyseur automatique de profil de données."""
    
    def __init__(self):
        pass
    
    def profile_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Génère un profil complet du DataFrame."""
        console.print("🔍 Profilage des données en cours...")
        
        profile = {
            'overview': self._get_overview(df),
            'columns': self._profile_columns(df),
            'missing_values': self._analyze_missing_values(df),
            'duplicates': self._analyze_duplicates(df),
            'data_types': self._analyze_data_types(df)
        }
        
        self._display_profile_summary(profile)
        return profile
    
    def _get_overview(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Vue d'ensemble du dataset."""
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
            'total_cells': len(df) * len(df.columns),
            'missing_cells': df.isnull().sum().sum(),
            'missing_percentage': (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        }
    
    def _profile_columns(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """Profile chaque colonne individuellement."""
        columns_profile = {}
        
        for col in df.columns:
            col_data = df[col]
            
            profile = {
                'dtype': str(col_data.dtype),
                'non_null_count': col_data.count(),
                'null_count': col_data.isnull().sum(),
                'null_percentage': (col_data.isnull().sum() / len(col_data)) * 100,
                'unique_count': col_data.nunique(),
                'unique_percentage': (col_data.nunique() / col_data.count()) * 100 if col_data.count() > 0 else 0
            }
            
            # Statistiques spécifiques par type
            if pd.api.types.is_numeric_dtype(col_data):
                profile.update(self._numeric_stats(col_data))
            elif pd.api.types.is_datetime64_any_dtype(col_data):
                profile.update(self._datetime_stats(col_data))
            else:
                profile.update(self._text_stats(col_data))
            
            columns_profile[col] = profile
        
        return columns_profile
    
    def _numeric_stats(self, series: pd.Series) -> Dict[str, Any]:
        """Statistiques pour colonnes numériques."""
        return {
            'mean': series.mean(),
            'median': series.median(),
            'std': series.std(),
            'min': series.min(),
            'max': series.max(),
            'q25': series.quantile(0.25),
            'q75': series.quantile(0.75),
            'zeros_count': (series == 0).sum(),
            'negative_count': (series < 0).sum() if series.dtype in ['int64', 'float64'] else 0
        }
    
    def _datetime_stats(self, series: pd.Series) -> Dict[str, Any]:
        """Statistiques pour colonnes datetime."""
        return {
            'min_date': series.min(),
            'max_date': series.max(),
            'date_range_days': (series.max() - series.min()).days if series.count() > 0 else 0
        }
    
    def _text_stats(self, series: pd.Series) -> Dict[str, Any]:
        """Statistiques pour colonnes texte."""
        text_lengths = series.astype(str).str.len()
        
        return {
            'avg_length': text_lengths.mean(),
            'min_length': text_lengths.min(),
            'max_length': text_lengths.max(),
            'empty_strings': (series == '').sum(),
            'most_frequent': series.mode().iloc[0] if len(series.mode()) > 0 else None,
            'most_frequent_count': series.value_counts().iloc[0] if len(series.value_counts()) > 0 else 0
        }
    
    def _analyze_missing_values(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyse détaillée des valeurs manquantes."""
        missing_counts = df.isnull().sum()
        missing_percentages = (missing_counts / len(df)) * 100
        
        return {
            'total_missing': missing_counts.sum(),
            'columns_with_missing': (missing_counts > 0).sum(),
            'by_column': {
                col: {
                    'count': int(missing_counts[col]),
                    'percentage': float(missing_percentages[col])
                }
                for col in df.columns if missing_counts[col] > 0
            },
            'rows_with_missing': df.isnull().any(axis=1).sum(),
            'complete_rows': (~df.isnull().any(axis=1)).sum()
        }
    
    def _analyze_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyse des doublons."""
        duplicated_rows = df.duplicated()
        
        return {
            'total_duplicates': duplicated_rows.sum(),
            'duplicate_percentage': (duplicated_rows.sum() / len(df)) * 100,
            'unique_rows': len(df) - duplicated_rows.sum()
        }
    
    def _analyze_data_types(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyse des types de données."""
        type_counts = df.dtypes.value_counts()
        
        return {
            'type_distribution': {str(dtype): int(count) for dtype, count in type_counts.items()},
            'numeric_columns': list(df.select_dtypes(include=[np.number]).columns),
            'text_columns': list(df.select_dtypes(include=['object']).columns),
            'datetime_columns': list(df.select_dtypes(include=['datetime64']).columns)
        }
    
    def _display_profile_summary(self, profile: Dict[str, Any]) -> None:
        """Affiche un résumé du profil."""
        overview = profile['overview']
        
        table = Table(title="📊 Profil du Dataset")
        table.add_column("Métrique", style="cyan")
        table.add_column("Valeur", style="green")
        
        table.add_row("Lignes", f"{overview['rows']:,}")
        table.add_row("Colonnes", f"{overview['columns']:,}")
        table.add_row("Mémoire", f"{overview['memory_usage_mb']:.2f} MB")
        table.add_row("Valeurs manquantes", f"{overview['missing_cells']:,} ({overview['missing_percentage']:.1f}%)")
        table.add_row("Doublons", f"{profile['duplicates']['total_duplicates']:,}")
        
        console.print(table)
    
    def get_quality_score(self, profile: Dict[str, Any]) -> float:
        """Calcule un score de qualité des données (0-100)."""
        overview = profile['overview']
        
        # Facteurs de qualité
        completeness = 100 - overview['missing_percentage']
        uniqueness = 100 - profile['duplicates']['duplicate_percentage']
        
        # Score pondéré
        quality_score = (completeness * 0.6) + (uniqueness * 0.4)
        
        return round(quality_score, 1)