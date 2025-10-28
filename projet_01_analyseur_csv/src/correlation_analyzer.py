"""
Module d'analyse de corrélation
Responsabilité: Calculer et analyser les corrélations entre variables
Version 2.2 - Optimisée avec cache et échantillonnage
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional


class CorrelationAnalyzer:
    """Classe pour analyser les corrélations entre variables (Version Optimisée)"""
    
    # Constantes d'optimisation
    MAX_COLUMNS = 50  # Limiter le nombre de colonnes pour la matrice
    SAMPLE_THRESHOLD = 100_000  # Si > 100K lignes, échantillonner
    SAMPLE_SIZE = 50_000  # Taille de l'échantillon
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        # Cache pour matrice de corrélation
        self._corr_cache = {}
    
    def get_correlation_matrix(self, method: str = 'pearson', use_sample: bool = None) -> pd.DataFrame:
        """
        Calcule la matrice de corrélation (OPTIMISÉ avec cache et échantillonnage)
        
        Args:
            method: Méthode de corrélation ('pearson', 'spearman', 'kendall')
            use_sample: Forcer échantillonnage (None = auto si > 100K lignes)
            
        Returns:
            DataFrame avec la matrice de corrélation
        """
        if len(self.numeric_columns) < 2:
            return pd.DataFrame()
        
        # Vérifier le cache
        cache_key = f"corr_{method}"
        if cache_key in self._corr_cache:
            return self._corr_cache[cache_key]
        
        # Limiter le nombre de colonnes si trop nombreuses
        cols_to_use = self.numeric_columns[:self.MAX_COLUMNS] if len(self.numeric_columns) > self.MAX_COLUMNS else self.numeric_columns
        
        # Décider si échantillonnage nécessaire
        if use_sample is None:
            use_sample = len(self.df) > self.SAMPLE_THRESHOLD
        
        # Préparer les données
        if use_sample and len(self.df) > self.SAMPLE_THRESHOLD:
            # Échantillonnage aléatoire pour gros datasets
            df_sample = self.df[cols_to_use].sample(n=self.SAMPLE_SIZE, random_state=42)
            corr_matrix = df_sample.corr(method=method)
        else:
            corr_matrix = self.df[cols_to_use].corr(method=method)
        
        # Mettre en cache
        self._corr_cache[cache_key] = corr_matrix
        return corr_matrix
    
    def get_correlation_pairs(self, threshold: float = 0.7, 
                             method: str = 'pearson') -> List[Dict]:
        """
        Trouve les paires de variables fortement corrélées
        
        Args:
            threshold: Seuil de corrélation (valeur absolue)
            method: Méthode de corrélation
            
        Returns:
            Liste de dictionnaires avec les paires corrélées
        """
        corr_matrix = self.get_correlation_matrix(method=method)
        
        if corr_matrix.empty:
            return []
        
        pairs = []
        
        # Parcourir la matrice triangulaire supérieure
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                
                if abs(corr_value) >= threshold:
                    pairs.append({
                        'variable_1': corr_matrix.columns[i],
                        'variable_2': corr_matrix.columns[j],
                        'correlation': round(corr_value, 3),
                        'force': self._interpret_correlation(abs(corr_value)),
                        'direction': 'Positive' if corr_value > 0 else 'Négative'
                    })
        
        # Trier par valeur absolue de corrélation
        pairs.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        return pairs
    
    def _interpret_correlation(self, corr_value: float) -> str:
        """
        Interprète la force de la corrélation
        
        Args:
            corr_value: Valeur absolue de la corrélation
            
        Returns:
            Interprétation textuelle
        """
        if corr_value >= 0.9:
            return "Très forte"
        elif corr_value >= 0.7:
            return "Forte"
        elif corr_value >= 0.5:
            return "Modérée"
        elif corr_value >= 0.3:
            return "Faible"
        else:
            return "Très faible"
    
    def test_correlation_significance(self, col1: str, col2: str) -> Dict:
        """
        Test de significativité de la corrélation entre deux variables
        
        Args:
            col1: Première colonne
            col2: Deuxième colonne
            
        Returns:
            Dictionnaire avec résultats du test
        """
        data1 = self.df[col1].dropna()
        data2 = self.df[col2].dropna()
        
        # Utiliser seulement les indices communs
        common_idx = data1.index.intersection(data2.index)
        data1 = data1.loc[common_idx]
        data2 = data2.loc[common_idx]
        
        # Test de Pearson
        pearson_corr, pearson_p = stats.pearsonr(data1, data2)
        
        # Test de Spearman
        spearman_corr, spearman_p = stats.spearmanr(data1, data2)
        
        return {
            'pearson': {
                'correlation': round(pearson_corr, 4),
                'p_value': round(pearson_p, 4),
                'significatif': pearson_p < 0.05
            },
            'spearman': {
                'correlation': round(spearman_corr, 4),
                'p_value': round(spearman_p, 4),
                'significatif': spearman_p < 0.05
            }
        }
    
    def get_top_correlations(self, target_column: str, n: int = 5) -> pd.DataFrame:
        """
        Trouve les N variables les plus corrélées avec une variable cible
        
        Args:
            target_column: Colonne cible
            n: Nombre de corrélations à retourner
            
        Returns:
            DataFrame avec les corrélations triées
        """
        if target_column not in self.numeric_columns:
            return pd.DataFrame()
        
        correlations = self.df[self.numeric_columns].corrwith(self.df[target_column])
        
        # Exclure la corrélation avec elle-même
        correlations = correlations.drop(target_column)
        
        # Trier par valeur absolue
        correlations_abs = correlations.abs().sort_values(ascending=False)
        top_vars = correlations_abs.head(n).index
        
        result = pd.DataFrame({
            'Variable': top_vars,
            'Corrélation': [correlations[var] for var in top_vars],
            'Corrélation_Abs': [abs(correlations[var]) for var in top_vars],
            'Force': [self._interpret_correlation(abs(correlations[var])) for var in top_vars]
        })
        
        return result
    
    def get_correlation_summary(self, method: str = 'pearson') -> Dict:
        """
        Résumé général des corrélations
        
        Args:
            method: Méthode de corrélation
            
        Returns:
            Dictionnaire avec le résumé
        """
        corr_matrix = self.get_correlation_matrix(method=method)
        
        if corr_matrix.empty:
            return {
                'message': 'Pas assez de colonnes numériques pour calculer les corrélations'
            }
        
        # Extraire les valeurs triangulaires supérieures (sans diagonale)
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
        correlations = corr_matrix.where(mask).stack().values
        
        return {
            'nombre_variables': len(self.numeric_columns),
            'nombre_paires': len(correlations),
            'correlation_moyenne': round(np.mean(correlations), 3),
            'correlation_max': round(np.max(correlations), 3),
            'correlation_min': round(np.min(correlations), 3),
            'paires_fortement_correlees': len([c for c in correlations if abs(c) >= 0.7]),
            'paires_moderement_correlees': len([c for c in correlations if 0.5 <= abs(c) < 0.7]),
            'paires_faiblement_correlees': len([c for c in correlations if abs(c) < 0.5])
        }
    
    def detect_multicollinearity(self, threshold: float = 0.9) -> List[Tuple[str, str, float]]:
        """
        Détecte les problèmes de multicolinéarité
        
        Args:
            threshold: Seuil de corrélation pour détecter la multicolinéarité
            
        Returns:
            Liste de tuples (var1, var2, correlation)
        """
        corr_matrix = self.get_correlation_matrix(method='pearson')
        
        if corr_matrix.empty:
            return []
        
        multicollinear = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                
                if abs(corr_value) >= threshold:
                    multicollinear.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        round(corr_value, 3)
                    ))
        
        return multicollinear
    
    def calculate_partial_correlation(self, x: str, y: str, control_vars: List[str]) -> float:
        """
        Calcule la corrélation partielle entre X et Y en contrôlant d'autres variables
        
        Args:
            x: Première variable
            y: Deuxième variable
            control_vars: Variables de contrôle
            
        Returns:
            Coefficient de corrélation partielle
        """
        # Créer un sous-ensemble avec toutes les variables nécessaires
        all_vars = [x, y] + control_vars
        data = self.df[all_vars].dropna()
        
        if len(data) < 3:
            return np.nan
        
        # Calculer la matrice de corrélation inverse
        corr_matrix = data.corr()
        
        try:
            precision_matrix = np.linalg.inv(corr_matrix)
            
            # La corrélation partielle est calculée à partir de la matrice de précision
            idx_x = all_vars.index(x)
            idx_y = all_vars.index(y)
            
            partial_corr = -precision_matrix[idx_x, idx_y] / np.sqrt(
                precision_matrix[idx_x, idx_x] * precision_matrix[idx_y, idx_y]
            )
            
            return round(partial_corr, 4)
            
        except np.linalg.LinAlgError:
            return np.nan
