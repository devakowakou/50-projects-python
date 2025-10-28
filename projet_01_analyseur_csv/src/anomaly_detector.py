"""
Module de détection d'anomalies et outliers
Responsabilité: Identifier les valeurs aberrantes dans les données
Version 2.2 - Optimisée avec parallélisation
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed


class AnomalyDetector:
    """Classe pour détecter les anomalies et outliers (Version Optimisée)"""
    
    # Constantes d'optimisation
    MAX_WORKERS = 4  # Nombre de threads pour parallélisation
    ENABLE_PARALLEL = True  # Activer la parallélisation
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        self.outliers_info = {}
    
    def detect_outliers_iqr(self, column: str, multiplier: float = 1.5) -> Dict:
        """
        Détecte les outliers avec la méthode IQR (OPTIMISÉ)
        
        Args:
            column: Nom de la colonne
            multiplier: Multiplicateur IQR (1.5 = outliers modérés, 3 = outliers extrêmes)
            
        Returns:
            Dictionnaire avec les outliers détectés
        """
        data = self.df[column].dropna()
        
        # Utiliser describe() pour calculer Q1, Q3 en un seul passage
        desc = data.describe()
        Q1 = desc['25%']
        Q3 = desc['75%']
        IQR = Q3 - Q1
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        outliers_mask = (self.df[column] < lower_bound) | (self.df[column] > upper_bound)
        outliers = self.df[outliers_mask][column]
        
        return {
            'methode': 'IQR',
            'colonne': column,
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR,
            'limite_inferieure': lower_bound,
            'limite_superieure': upper_bound,
            'nombre_outliers': len(outliers),
            'pourcentage': round(len(outliers) / len(data) * 100, 2) if len(data) > 0 else 0,
            'outliers_indices': outliers.index.tolist(),
            'outliers_valeurs': outliers.tolist()
        }
    
    def detect_outliers_zscore(self, column: str, threshold: float = 3) -> Dict:
        """
        Détecte les outliers avec la méthode Z-Score
        
        Args:
            column: Nom de la colonne
            threshold: Seuil Z-Score (généralement 3)
            
        Returns:
            Dictionnaire avec les outliers détectés
        """
        data = self.df[column].dropna()
        
        mean = data.mean()
        std = data.std()
        
        z_scores = np.abs(stats.zscore(data))
        outliers_mask = z_scores > threshold
        outliers = data[outliers_mask]
        
        return {
            'methode': 'Z-Score',
            'colonne': column,
            'moyenne': mean,
            'ecart_type': std,
            'seuil': threshold,
            'nombre_outliers': len(outliers),
            'pourcentage': round(len(outliers) / len(data) * 100, 2),
            'outliers_indices': outliers.index.tolist(),
            'outliers_valeurs': outliers.tolist(),
            'z_scores_max': round(z_scores.max(), 2)
        }
    
    def detect_outliers_all_columns(self, method: str = 'IQR', 
                                   threshold: float = 1.5) -> pd.DataFrame:
        """
        Détecte les outliers pour toutes les colonnes numériques (OPTIMISÉ - parallèle)
        
        Args:
            method: Méthode de détection ('IQR' ou 'Z-Score')
            threshold: Seuil (1.5 pour IQR, 3 pour Z-Score)
            
        Returns:
            DataFrame avec le résumé des outliers
        """
        results = []
        
        # Version parallélisée si activée et plusieurs colonnes
        if self.ENABLE_PARALLEL and len(self.numeric_columns) > 2:
            with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
                # Soumettre toutes les tâches
                future_to_col = {}
                for col in self.numeric_columns:
                    if method.upper() == 'IQR':
                        future = executor.submit(self.detect_outliers_iqr, col, threshold)
                    else:
                        future = executor.submit(self.detect_outliers_zscore, col, threshold)
                    future_to_col[future] = col
                
                # Collecter les résultats
                for future in as_completed(future_to_col):
                    col = future_to_col[future]
                    try:
                        result = future.result()
                        results.append({
                            'Colonne': col,
                            'Méthode': method,
                            'Nombre_Outliers': result['nombre_outliers'],
                            'Pourcentage': result['pourcentage'],
                            'Min_Outlier': min(result['outliers_valeurs']) if result['outliers_valeurs'] else None,
                            'Max_Outlier': max(result['outliers_valeurs']) if result['outliers_valeurs'] else None
                        })
                        self.outliers_info[col] = result
                    except Exception as e:
                        # En cas d'erreur, continuer avec les autres colonnes
                        pass
        else:
            # Version séquentielle (fallback)
            for col in self.numeric_columns:
                if method.upper() == 'IQR':
                    result = self.detect_outliers_iqr(col, threshold)
                else:
                    result = self.detect_outliers_zscore(col, threshold)
                
                results.append({
                    'Colonne': col,
                    'Méthode': method,
                    'Nombre_Outliers': result['nombre_outliers'],
                    'Pourcentage': result['pourcentage'],
                    'Min_Outlier': min(result['outliers_valeurs']) if result['outliers_valeurs'] else None,
                    'Max_Outlier': max(result['outliers_valeurs']) if result['outliers_valeurs'] else None
                })
                
                # Stocker pour référence
                self.outliers_info[col] = result
        
        return pd.DataFrame(results).sort_values('Nombre_Outliers', ascending=False)
    
    def get_outliers_summary(self) -> Dict:
        """
        Résumé global des outliers détectés
        
        Returns:
            Dictionnaire avec le résumé
        """
        if not self.outliers_info:
            return {'message': 'Aucune détection effectuée'}
        
        total_outliers = sum(info['nombre_outliers'] for info in self.outliers_info.values())
        
        return {
            'colonnes_analysees': len(self.outliers_info),
            'total_outliers': total_outliers,
            'colonnes_avec_outliers': sum(1 for info in self.outliers_info.values() 
                                         if info['nombre_outliers'] > 0),
            'pourcentage_moyen': round(
                np.mean([info['pourcentage'] for info in self.outliers_info.values()]), 2
            )
        }
    
    def visualize_outliers_info(self, column: str) -> Dict:
        """
        Informations détaillées pour visualiser les outliers
        
        Args:
            column: Nom de la colonne
            
        Returns:
            Dictionnaire avec les infos pour visualisation
        """
        if column not in self.outliers_info:
            # Détecter d'abord avec IQR
            self.detect_outliers_iqr(column)
        
        info = self.outliers_info[column]
        data = self.df[column].dropna()
        
        return {
            'colonne': column,
            'valeurs_normales': data[~data.index.isin(info['outliers_indices'])].tolist(),
            'outliers': info['outliers_valeurs'],
            'limites': {
                'inferieure': info.get('limite_inferieure'),
                'superieure': info.get('limite_superieure')
            },
            'statistiques': {
                'Q1': info.get('Q1'),
                'mediane': data.median(),
                'Q3': info.get('Q3'),
                'moyenne': data.mean()
            }
        }
    
    def flag_outliers_in_dataframe(self, method: str = 'IQR', 
                                  threshold: float = 1.5) -> pd.DataFrame:
        """
        Ajoute des colonnes de flag pour marquer les outliers
        
        Args:
            method: Méthode de détection
            threshold: Seuil
            
        Returns:
            DataFrame avec colonnes de flags ajoutées
        """
        df_flagged = self.df.copy()
        
        for col in self.numeric_columns:
            if method.upper() == 'IQR':
                outliers_info = self.detect_outliers_iqr(col, threshold)
            else:
                outliers_info = self.detect_outliers_zscore(col, threshold)
            
            # Créer une colonne de flag
            flag_col_name = f'{col}_outlier'
            df_flagged[flag_col_name] = False
            df_flagged.loc[outliers_info['outliers_indices'], flag_col_name] = True
        
        return df_flagged
    
    def get_multivariate_outliers(self, columns: List[str] = None) -> List[int]:
        """
        Détecte les outliers multivariés (basé sur la distance de Mahalanobis)
        
        Args:
            columns: Liste des colonnes à considérer (None = toutes numériques)
            
        Returns:
            Liste des indices des outliers multivariés
        """
        if columns is None:
            columns = self.numeric_columns
        
        data = self.df[columns].dropna()
        
        if len(data) < len(columns) + 1:
            return []
        
        try:
            # Calculer la distance de Mahalanobis
            mean = data.mean()
            cov = data.cov()
            inv_cov = np.linalg.inv(cov)
            
            diff = data - mean
            mahal_distances = np.sqrt(
                np.sum(diff @ inv_cov * diff, axis=1)
            )
            
            # Seuil basé sur la distribution Chi-carré
            threshold = stats.chi2.ppf(0.95, len(columns))
            outliers_mask = mahal_distances > threshold
            
            return data[outliers_mask].index.tolist()
            
        except np.linalg.LinAlgError:
            return []
    
    def compare_methods(self, column: str) -> pd.DataFrame:
        """
        Compare les résultats de différentes méthodes de détection
        
        Args:
            column: Nom de la colonne
            
        Returns:
            DataFrame comparant les méthodes
        """
        iqr_result = self.detect_outliers_iqr(column, 1.5)
        zscore_result = self.detect_outliers_zscore(column, 3)
        iqr_extreme = self.detect_outliers_iqr(column, 3)
        
        comparison = pd.DataFrame({
            'Méthode': ['IQR (1.5)', 'IQR (3.0)', 'Z-Score (3)'],
            'Outliers_Détectés': [
                iqr_result['nombre_outliers'],
                iqr_extreme['nombre_outliers'],
                zscore_result['nombre_outliers']
            ],
            'Pourcentage': [
                iqr_result['pourcentage'],
                iqr_extreme['pourcentage'],
                zscore_result['pourcentage']
            ]
        })
        
        return comparison
    
    def suggest_treatment(self, column: str) -> Dict:
        """
        Suggère des traitements pour les outliers
        
        Args:
            column: Nom de la colonne
            
        Returns:
            Dictionnaire avec suggestions
        """
        if column not in self.outliers_info:
            self.detect_outliers_iqr(column)
        
        info = self.outliers_info[column]
        pourcentage = info['pourcentage']
        
        suggestions = []
        
        if pourcentage < 1:
            suggestions.append("Supprimer les outliers (impact minimal)")
        if pourcentage < 5:
            suggestions.append("Winsorization (plafonner aux limites IQR)")
        
        suggestions.append("Transformation logarithmique")
        suggestions.append("Garder les outliers (peuvent être importants)")
        suggestions.append("Analyser manuellement chaque cas")
        
        return {
            'colonne': column,
            'pourcentage_outliers': pourcentage,
            'suggestions': suggestions,
            'recommandation': suggestions[0] if suggestions else "Aucune action nécessaire"
        }
