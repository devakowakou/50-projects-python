"""
Module de nettoyage et preprocessing des données
Responsabilité: Traiter les valeurs manquantes, duplicatas, conversions
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List


class DataCleaner:
    """Classe pour nettoyer et prétraiter les données"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.original_df = df.copy()
        self.cleaning_log = []
    
    def get_missing_values_summary(self) -> pd.DataFrame:
        """
        Résumé des valeurs manquantes
        
        Returns:
            DataFrame avec le nombre et pourcentage de valeurs manquantes
        """
        missing_count = self.df.isnull().sum()
        missing_percent = (missing_count / len(self.df)) * 100
        
        summary = pd.DataFrame({
            'Colonne': missing_count.index,
            'Valeurs_Manquantes': missing_count.values,
            'Pourcentage': missing_percent.values
        })
        
        return summary[summary['Valeurs_Manquantes'] > 0].sort_values(
            'Valeurs_Manquantes', ascending=False
        )
    
    def handle_missing_values(self, strategy: str = 'drop', 
                            columns: Optional[List[str]] = None,
                            fill_value: Optional[float] = None) -> None:
        """
        Traite les valeurs manquantes
        
        Args:
            strategy: Stratégie ('drop', 'mean', 'median', 'mode', 'custom')
            columns: Liste des colonnes à traiter (None = toutes)
            fill_value: Valeur personnalisée pour strategy='custom'
        """
        if columns is None:
            columns = self.df.columns.tolist()
        
        initial_rows = len(self.df)
        
        if strategy == 'drop':
            self.df = self.df.dropna(subset=columns)
            self.cleaning_log.append(
                f"Supprimé {initial_rows - len(self.df)} lignes avec valeurs manquantes"
            )
        
        elif strategy in ['mean', 'median', 'mode']:
            for col in columns:
                if col in self.df.select_dtypes(include=['number']).columns:
                    if strategy == 'mean':
                        fill_val = self.df[col].mean()
                    elif strategy == 'median':
                        fill_val = self.df[col].median()
                    else:  # mode
                        fill_val = self.df[col].mode()[0] if not self.df[col].mode().empty else 0
                    
                    missing_count = self.df[col].isnull().sum()
                    self.df[col].fillna(fill_val, inplace=True)
                    self.cleaning_log.append(
                        f"Rempli {missing_count} valeurs manquantes dans '{col}' avec {strategy}"
                    )
        
        elif strategy == 'custom' and fill_value is not None:
            for col in columns:
                missing_count = self.df[col].isnull().sum()
                self.df[col].fillna(fill_value, inplace=True)
                self.cleaning_log.append(
                    f"Rempli {missing_count} valeurs manquantes dans '{col}' avec {fill_value}"
                )
    
    def remove_duplicates(self, subset: Optional[List[str]] = None) -> int:
        """
        Supprime les lignes dupliquées
        
        Args:
            subset: Colonnes à considérer pour détecter les duplicatas
            
        Returns:
            Nombre de duplicatas supprimés
        """
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset, keep='first')
        removed = initial_rows - len(self.df)
        
        if removed > 0:
            self.cleaning_log.append(f"Supprimé {removed} lignes dupliquées")
        
        return removed
    
    def convert_column_type(self, column: str, target_type: str) -> bool:
        """
        Convertit le type d'une colonne
        
        Args:
            column: Nom de la colonne
            target_type: Type cible ('int', 'float', 'str', 'datetime', 'category')
            
        Returns:
            bool: Succès de la conversion
        """
        try:
            if target_type == 'int':
                self.df[column] = pd.to_numeric(self.df[column], errors='coerce').astype('Int64')
            elif target_type == 'float':
                self.df[column] = pd.to_numeric(self.df[column], errors='coerce')
            elif target_type == 'str':
                self.df[column] = self.df[column].astype(str)
            elif target_type == 'datetime':
                self.df[column] = pd.to_datetime(self.df[column], errors='coerce')
            elif target_type == 'category':
                self.df[column] = self.df[column].astype('category')
            
            self.cleaning_log.append(f"Converti '{column}' en {target_type}")
            return True
            
        except Exception as e:
            self.cleaning_log.append(f"Échec conversion '{column}': {str(e)}")
            return False
    
    def normalize_column_names(self) -> None:
        """Normalise les noms de colonnes (minuscules, sans espaces)"""
        old_names = self.df.columns.tolist()
        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.replace('[^a-z0-9_]', '', regex=True)
        )
        self.cleaning_log.append("Noms de colonnes normalisés")
    
    def remove_outliers_iqr(self, columns: Optional[List[str]] = None, 
                           multiplier: float = 1.5) -> int:
        """
        Supprime les outliers selon la méthode IQR
        
        Args:
            columns: Colonnes numériques à traiter
            multiplier: Multiplicateur IQR (défaut: 1.5)
            
        Returns:
            Nombre de lignes supprimées
        """
        if columns is None:
            columns = self.df.select_dtypes(include=['number']).columns.tolist()
        
        initial_rows = len(self.df)
        
        for col in columns:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - multiplier * IQR
            upper_bound = Q3 + multiplier * IQR
            
            self.df = self.df[
                (self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)
            ]
        
        removed = initial_rows - len(self.df)
        if removed > 0:
            self.cleaning_log.append(f"Supprimé {removed} outliers (méthode IQR)")
        
        return removed
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """Retourne les données nettoyées"""
        return self.df
    
    def get_cleaning_log(self) -> List[str]:
        """Retourne le journal de nettoyage"""
        return self.cleaning_log
    
    def reset_to_original(self) -> None:
        """Réinitialise aux données originales"""
        self.df = self.original_df.copy()
        self.cleaning_log = []
        self.cleaning_log.append("Données réinitialisées")
    
    def get_data_quality_report(self) -> Dict:
        """
        Génère un rapport de qualité des données
        
        Returns:
            Dictionnaire avec métriques de qualité
        """
        return {
            'lignes_total': len(self.df),
            'colonnes_total': len(self.df.columns),
            'valeurs_manquantes_total': self.df.isnull().sum().sum(),
            'pourcentage_completude': (1 - self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100,
            'duplicatas': self.df.duplicated().sum(),
            'memoire_utilise': f"{self.df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
        }
