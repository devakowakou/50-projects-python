"""Analyseur de prix immobilier"""

import pandas as pd
import numpy as np
from typing import Dict, List
from scipy import stats

class PriceAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def get_price_statistics(self) -> Dict:
        """Statistiques générales des prix"""
        if self.df.empty:
            return {}
        
        return {
            "total_properties": len(self.df),
            "avg_price": self.df['price'].mean(),
            "median_price": self.df['price'].median(),
            "std_price": self.df['price'].std(),
            "min_price": self.df['price'].min(),
            "max_price": self.df['price'].max(),
            "avg_price_per_m2": self.df['price_per_m2'].mean(),
            "median_price_per_m2": self.df['price_per_m2'].median(),
            "avg_surface": self.df['surface'].mean()
        }
    
    def analyze_by_quartier(self) -> pd.DataFrame:
        """Analyse par quartier"""
        if self.df.empty:
            return pd.DataFrame()
        
        quartier_stats = self.df.groupby('quartier').agg({
            'price': ['count', 'mean', 'median', 'std', 'min', 'max'],
            'price_per_m2': ['mean', 'median'],
            'surface': ['mean', 'median'],
            'rooms': ['mean']
        }).round(0)
        
        # Aplatir les colonnes
        quartier_stats.columns = ['_'.join(col).strip() for col in quartier_stats.columns]
        quartier_stats = quartier_stats.reset_index()
        
        # Renommer pour plus de clarté
        quartier_stats.rename(columns={
            'price_count': 'nb_biens',
            'price_mean': 'prix_moyen',
            'price_median': 'prix_median',
            'price_per_m2_mean': 'prix_m2_moyen',
            'surface_mean': 'surface_moyenne'
        }, inplace=True)
        
        return quartier_stats.sort_values('prix_m2_moyen', ascending=False)
    
    def find_best_deals(self, top_n: int = 10) -> pd.DataFrame:
        """Trouve les meilleures affaires"""
        if self.df.empty:
            return pd.DataFrame()
        
        # Calcul du score (prix/m² par rapport à la médiane du quartier)
        quartier_medians = self.df.groupby('quartier')['price_per_m2'].median()
        
        def calculate_deal_score(row):
            quartier_median = quartier_medians.get(row['quartier'], row['price_per_m2'])
            return (quartier_median - row['price_per_m2']) / quartier_median * 100
        
        self.df['deal_score'] = self.df.apply(calculate_deal_score, axis=1)
        
        best_deals = self.df.nlargest(top_n, 'deal_score')[
            ['title', 'price', 'surface', 'price_per_m2', 'quartier', 'deal_score']
        ]
        
        return best_deals
    
    def price_distribution_analysis(self) -> Dict:
        """Analyse de la distribution des prix"""
        if self.df.empty:
            return {}
        
        prices = self.df['price']
        
        # Quartiles
        q1 = prices.quantile(0.25)
        q3 = prices.quantile(0.75)
        iqr = q3 - q1
        
        # Détection d'outliers
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = prices[(prices < lower_bound) | (prices > upper_bound)]
        
        return {
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "outliers_count": len(outliers),
            "outliers_percentage": len(outliers) / len(prices) * 100,
            "skewness": stats.skew(prices),
            "kurtosis": stats.kurtosis(prices)
        }
    
    def compare_quartiers(self, quartier1: str, quartier2: str) -> Dict:
        """Compare deux quartiers"""
        q1_data = self.df[self.df['quartier'] == quartier1]['price_per_m2']
        q2_data = self.df[self.df['quartier'] == quartier2]['price_per_m2']
        
        if len(q1_data) == 0 or len(q2_data) == 0:
            return {}
        
        # Test statistique
        t_stat, p_value = stats.ttest_ind(q1_data, q2_data)
        
        return {
            "quartier1": quartier1,
            "quartier2": quartier2,
            "mean_diff": q1_data.mean() - q2_data.mean(),
            "mean_diff_pct": ((q1_data.mean() - q2_data.mean()) / q2_data.mean()) * 100,
            "t_statistic": t_stat,
            "p_value": p_value,
            "significant": p_value < 0.05
        }

class TrendAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def surface_price_correlation(self) -> Dict:
        """Corrélation surface-prix"""
        if self.df.empty or len(self.df) < 2:
            return {}
        
        correlation = self.df['surface'].corr(self.df['price'])
        
        return {
            "correlation": correlation,
            "correlation_strength": self._interpret_correlation(correlation)
        }
    
    def _interpret_correlation(self, corr: float) -> str:
        """Interprète la force de corrélation"""
        abs_corr = abs(corr)
        if abs_corr >= 0.8:
            return "Très forte"
        elif abs_corr >= 0.6:
            return "Forte"
        elif abs_corr >= 0.4:
            return "Modérée"
        elif abs_corr >= 0.2:
            return "Faible"
        else:
            return "Très faible"