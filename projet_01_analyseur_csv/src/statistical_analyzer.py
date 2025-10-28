"""
Module d'analyse statistique descriptive
Responsabilité: Calculer toutes les statistiques descriptives
Version 2.2 - Optimisée avec calculs en un seul passage
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Optional
from functools import lru_cache


class StatisticalAnalyzer:
    """Classe pour effectuer l'analyse statistique descriptive (Version Optimisée)"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        # Cache pour éviter recalculs
        self._stats_cache = {}
    
    def get_basic_statistics(self, column: Optional[str] = None) -> pd.DataFrame:
        """
        Calcule les statistiques de base (OPTIMISÉ - un seul passage)
        
        Args:
            column: Colonne spécifique (None = toutes les colonnes numériques)
            
        Returns:
            DataFrame avec les statistiques
        """
        if column:
            data = self.df[[column]]
        else:
            data = self.df[self.numeric_columns]
        
        # Utiliser describe() qui est optimisé en C - UN SEUL PASSAGE
        desc = data.describe()
        
        # Calculer les stats supplémentaires en un passage
        q1 = desc.loc['25%']
        q3 = desc.loc['75%']
        iqr = q3 - q1
        mean = desc.loc['mean']
        std = desc.loc['std']
        
        # Construire le résultat avec les valeurs déjà calculées
        stats_dict = {
            'Moyenne': mean,
            'Médiane': desc.loc['50%'],
            'Écart-type': std,
            'Variance': std ** 2,  # Calculé depuis std au lieu de var()
            'Minimum': desc.loc['min'],
            'Maximum': desc.loc['max'],
            'Q1 (25%)': q1,
            'Q3 (75%)': q3,
            'IQR': iqr,
            'Étendue': desc.loc['max'] - desc.loc['min'],
            'CV (%)': (std / mean * 100).round(2),
        }
        
        return pd.DataFrame(stats_dict).T
    
    def get_advanced_statistics(self, column: str) -> Dict:
        """
        Calcule des statistiques avancées pour une colonne (avec cache)
        
        Args:
            column: Nom de la colonne
            
        Returns:
            Dictionnaire avec les statistiques avancées
        """
        # Vérifier le cache
        cache_key = f"advanced_{column}"
        if cache_key in self._stats_cache:
            return self._stats_cache[cache_key]
        
        data = self.df[column].dropna()
        
        # Calculer une seule fois
        mean_val = data.mean()
        std_val = data.std()
        
        result = {
            'skewness': stats.skew(data),
            'kurtosis': stats.kurtosis(data),
            'mode': data.mode().values[0] if len(data.mode()) > 0 else None,
            'coef_variation': (std_val / mean_val * 100) if mean_val != 0 else None,
            'erreur_standard': stats.sem(data),
            'intervalle_confiance_95': stats.t.interval(
                0.95, len(data)-1, loc=mean_val, scale=stats.sem(data)
            )
        }
        
        # Mettre en cache
        self._stats_cache[cache_key] = result
        return result
    
    def get_distribution_analysis(self, column: str) -> Dict:
        """
        Analyse la distribution d'une colonne
        
        Args:
            column: Nom de la colonne
            
        Returns:
            Dictionnaire avec l'analyse de distribution
        """
        data = self.df[column].dropna()
        
        # Test de normalité Shapiro-Wilk (si échantillon < 5000)
        if len(data) < 5000:
            shapiro_stat, shapiro_p = stats.shapiro(data)
        else:
            shapiro_stat, shapiro_p = None, None
        
        # Test de normalité Kolmogorov-Smirnov
        ks_stat, ks_p = stats.kstest(data, 'norm', args=(data.mean(), data.std()))
        
        return {
            'est_normal_shapiro': shapiro_p > 0.05 if shapiro_p else None,
            'shapiro_p_value': shapiro_p,
            'est_normal_ks': ks_p > 0.05,
            'ks_p_value': ks_p,
            'asymetrie': 'Symétrique' if abs(stats.skew(data)) < 0.5 else 
                        ('Asymétrique à droite' if stats.skew(data) > 0 else 'Asymétrique à gauche')
        }
    
    def get_frequency_analysis(self, column: str, top_n: int = 10) -> pd.DataFrame:
        """
        Analyse de fréquence pour colonnes catégoriques
        
        Args:
            column: Nom de la colonne
            top_n: Nombre de valeurs les plus fréquentes
            
        Returns:
            DataFrame avec fréquences
        """
        freq = self.df[column].value_counts().head(top_n)
        percent = (freq / len(self.df) * 100).round(2)
        
        return pd.DataFrame({
            'Valeur': freq.index,
            'Fréquence': freq.values,
            'Pourcentage': percent.values
        })
    
    def get_missing_values_analysis(self) -> pd.DataFrame:
        """
        Analyse des valeurs manquantes
        
        Returns:
            DataFrame avec l'analyse des valeurs manquantes
        """
        missing_count = self.df.isnull().sum()
        missing_percent = (missing_count / len(self.df) * 100).round(2)
        
        analysis = pd.DataFrame({
            'Colonne': self.df.columns,
            'Valeurs_Manquantes': missing_count.values,
            'Pourcentage': missing_percent.values,
            'Type': self.df.dtypes.values
        })
        
        return analysis[analysis['Valeurs_Manquantes'] > 0].sort_values(
            'Valeurs_Manquantes', ascending=False
        )
    
    def get_unique_values_summary(self) -> pd.DataFrame:
        """
        Résumé des valeurs uniques par colonne
        
        Returns:
            DataFrame avec le compte des valeurs uniques
        """
        summary = pd.DataFrame({
            'Colonne': self.df.columns,
            'Valeurs_Uniques': [self.df[col].nunique() for col in self.df.columns],
            'Pourcentage_Unicite': [
                (self.df[col].nunique() / len(self.df) * 100).round(2) 
                for col in self.df.columns
            ],
            'Type': self.df.dtypes.values
        })
        
        return summary.sort_values('Valeurs_Uniques', ascending=False)
    
    def get_percentiles(self, column: str, percentiles: List[float] = None) -> Dict:
        """
        Calcule les percentiles pour une colonne
        
        Args:
            column: Nom de la colonne
            percentiles: Liste des percentiles (ex: [0.1, 0.25, 0.5, 0.75, 0.9])
            
        Returns:
            Dictionnaire des percentiles
        """
        if percentiles is None:
            percentiles = [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
        
        return {
            f"{int(p*100)}%": self.df[column].quantile(p) 
            for p in percentiles
        }
    
    def get_summary_by_category(self, numeric_col: str, category_col: str) -> pd.DataFrame:
        """
        Statistiques résumées par catégorie
        
        Args:
            numeric_col: Colonne numérique à analyser
            category_col: Colonne catégorique pour grouper
            
        Returns:
            DataFrame avec statistiques par catégorie
        """
        return self.df.groupby(category_col)[numeric_col].agg([
            ('Moyenne', 'mean'),
            ('Médiane', 'median'),
            ('Écart-type', 'std'),
            ('Min', 'min'),
            ('Max', 'max'),
            ('Compte', 'count')
        ]).round(2)
    
    def get_complete_summary(self) -> Dict:
        """
        Résumé complet de toutes les analyses
        
        Returns:
            Dictionnaire avec toutes les analyses
        """
        return {
            'dimensions': {
                'lignes': len(self.df),
                'colonnes': len(self.df.columns),
                'colonnes_numeriques': len(self.numeric_columns),
                'colonnes_categoriques': len(self.df.select_dtypes(include=['object']).columns)
            },
            'qualite_donnees': {
                'valeurs_totales': self.df.size,
                'valeurs_manquantes': self.df.isnull().sum().sum(),
                'pourcentage_completude': ((1 - self.df.isnull().sum().sum() / self.df.size) * 100).round(2),
                'duplicatas': self.df.duplicated().sum()
            },
            'memoire': f"{self.df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
        }
