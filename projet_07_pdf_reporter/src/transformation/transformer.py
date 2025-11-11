"""
Transformateur de données
"""
import pandas as pd
import numpy as np
from typing import Optional, Dict
import warnings

# Logging optionnel
try:
    from src.utils.logger import setup_logger
    logger = setup_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

class Transformer:
    """Transformateur de données avec normalisation et nettoyage"""
    
    def __init__(self):
        self.transformations_applied = []
    
    def normalize(self, df: pd.DataFrame, inplace: bool = False) -> pd.DataFrame:
        """
        Normalise un DataFrame (nettoyage de base)
        
        Args:
            df: DataFrame à normaliser
            inplace: Modifier le DataFrame original
        
        Returns:
            DataFrame normalisé
        """
        if not inplace:
            df = df.copy()
        
        initial_shape = df.shape
        
        # Supprimer colonnes entièrement vides
        df = df.dropna(axis=1, how='all')
        
        # Supprimer lignes entièrement vides
        df = df.dropna(axis=0, how='all')
        
        # Nettoyer les noms de colonnes
        df.columns = df.columns.str.strip()
        
        # Supprimer doublons
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            df = df.drop_duplicates()
            logger.info(f"🔍 {duplicates} doublons supprimés")
        
        final_shape = df.shape
        
        logger.info(
            f"✅ Normalisation: {initial_shape} → {final_shape}"
        )
        
        self.transformations_applied.append("normalize")
        return df
    
    def convert_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convertit les colonnes de dates au format datetime
        
        Args:
            df: DataFrame à convertir
            
        Returns:
            DataFrame avec dates converties
        """
        df_converted = df.copy()
        converted_count = 0
        
        for col in df_converted.columns:
            # Essayer de convertir en datetime
            if df_converted[col].dtype == 'object':
                try:
                    # Supprimer les warnings pour la conversion
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        # Essayer la conversion
                        converted = pd.to_datetime(
                            df_converted[col], 
                            errors='coerce',
                            infer_datetime_format=True
                        )
                        
                        # Vérifier si la conversion a réussi (au moins 50% de valeurs non-null)
                        if converted.notna().sum() / len(converted) >= 0.5:
                            df_converted[col] = converted
                            converted_count += 1
                            logger.info(f"📅 Colonne '{col}' convertie en datetime")
                except Exception:
                    pass
        
        if converted_count > 0:
            logger.info(f"✅ {converted_count} colonne(s) de dates converties")
        
        return df_converted
    
    def handle_missing_values(
        self, 
        df: pd.DataFrame,
        strategy: str = "drop",
        fill_value: Optional[any] = None
    ) -> pd.DataFrame:
        """
        Gère les valeurs manquantes
        
        Args:
            df: DataFrame
            strategy: 'drop', 'fill', 'forward', 'backward'
            fill_value: Valeur de remplacement si strategy='fill'
        
        Returns:
            DataFrame avec valeurs manquantes traitées
        """
        df = df.copy()
        
        missing_before = df.isnull().sum().sum()
        
        if strategy == "drop":
            df = df.dropna()
        elif strategy == "fill":
            df = df.fillna(fill_value if fill_value is not None else 0)
        elif strategy == "forward":
            df = df.fillna(method='ffill')
        elif strategy == "backward":
            df = df.fillna(method='bfill')
        else:
            logger.warning(f"⚠️ Stratégie '{strategy}' non reconnue")
        
        missing_after = df.isnull().sum().sum()
        
        logger.info(
            f"🔧 Valeurs manquantes: {missing_before} → {missing_after}"
        )
        
        self.transformations_applied.append(f"handle_missing_{strategy}")
        return df
    
    def filter_by_date(
        self,
        df: pd.DataFrame,
        date_column: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Filtre le DataFrame par plage de dates
        
        Args:
            df: DataFrame
            date_column: Nom de la colonne de date
            start_date: Date de début (format YYYY-MM-DD)
            end_date: Date de fin (format YYYY-MM-DD)
        
        Returns:
            DataFrame filtré
        """
        df = df.copy()
        
        if date_column not in df.columns:
            raise ValueError(f"Colonne '{date_column}' introuvable")
        
        # Convertir en datetime si nécessaire
        if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
            df[date_column] = pd.to_datetime(df[date_column])
        
        initial_rows = len(df)
        
        if start_date:
            df = df[df[date_column] >= pd.to_datetime(start_date)]
        
        if end_date:
            df = df[df[date_column] <= pd.to_datetime(end_date)]
        
        final_rows = len(df)
        
        logger.info(
            f"📊 Filtrage par date: {initial_rows} → {final_rows} lignes"
        )
        
        self.transformations_applied.append("filter_by_date")
        return df
    
    def aggregate_by_period(
        self,
        df: pd.DataFrame,
        date_column: str,
        value_column: str,
        period: str = "M",
        agg_func: str = "sum"
    ) -> pd.DataFrame:
        """
        Agrège les données par période
        
        Args:
            df: DataFrame
            date_column: Colonne de date
            value_column: Colonne à agréger
            period: 'D' (jour), 'W' (semaine), 'M' (mois), 'Y' (année)
            agg_func: Fonction d'agrégation ('sum', 'mean', 'count')
        
        Returns:
            DataFrame agrégé
        """
        df = df.copy()
        
        # Convertir en datetime
        if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
            df[date_column] = pd.to_datetime(df[date_column])
        
        # Définir comme index
        df = df.set_index(date_column)
        
        # Agréger
        if agg_func == "sum":
            result = df[value_column].resample(period).sum()
        elif agg_func == "mean":
            result = df[value_column].resample(period).mean()
        elif agg_func == "count":
            result = df[value_column].resample(period).count()
        else:
            raise ValueError(f"Fonction d'agrégation '{agg_func}' non supportée")
        
        result = result.reset_index()
        
        logger.info(
            f"📈 Agrégation par période '{period}': {len(result)} points"
        )
        
        self.transformations_applied.append(f"aggregate_{period}_{agg_func}")
        return result
    
    def get_summary_stats(self, df: pd.DataFrame) -> Dict:
        """
        Calcule des statistiques descriptives
        
        Args:
            df: DataFrame
        
        Returns:
            Dictionnaire de statistiques
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        stats = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "numeric_columns": len(numeric_cols),
            "missing_values": int(df.isnull().sum().sum()),
            "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024**2, 2)
        }
        
        # Stats par colonne numérique
        if len(numeric_cols) > 0:
            stats["numeric_stats"] = {}
            for col in numeric_cols:
                stats["numeric_stats"][col] = {
                    "min": float(df[col].min()),
                    "max": float(df[col].max()),
                    "mean": float(df[col].mean()),
                    "median": float(df[col].median()),
                    "std": float(df[col].std())
                }
        
        return stats
    
    def remove_outliers(
        self, 
        df: pd.DataFrame, 
        columns: Optional[list] = None,
        method: str = "iqr"
    ) -> pd.DataFrame:
        """
        Supprime les outliers
        
        Args:
            df: DataFrame
            columns: Colonnes à traiter (None = toutes les numériques)
            method: Méthode ('iqr', 'zscore')
            
        Returns:
            DataFrame sans outliers
        """
        df_clean = df.copy()
        
        if columns is None:
            columns = df_clean.select_dtypes(include=['number']).columns
        
        if method == "iqr":
            for col in columns:
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                df_clean = df_clean[
                    (df_clean[col] >= lower_bound) & 
                    (df_clean[col] <= upper_bound)
                ]
        
        elif method == "zscore":
            for col in columns:
                z_scores = np.abs((df_clean[col] - df_clean[col].mean()) / df_clean[col].std())
                df_clean = df_clean[z_scores < 3]
        
        return df_clean