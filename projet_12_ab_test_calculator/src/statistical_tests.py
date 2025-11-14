"""
Tests statistiques pour A/B testing
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Tuple, Optional
import math


class ABTestCalculator:
    """Calculateur de tests A/B avec différents tests statistiques"""
    
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level
        self.alpha = 1 - confidence_level
    
    def t_test_two_sample(self, group_a: np.array, group_b: np.array, 
                         equal_var: bool = True) -> Dict:
        """Test t de Student pour comparer deux moyennes"""
        
        # Statistiques descriptives
        n_a, n_b = len(group_a), len(group_b)
        mean_a, mean_b = np.mean(group_a), np.mean(group_b)
        std_a, std_b = np.std(group_a, ddof=1), np.std(group_b, ddof=1)
        
        # Test t
        t_stat, p_value = stats.ttest_ind(group_a, group_b, equal_var=equal_var)
        
        # Intervalle de confiance pour la différence
        diff = mean_b - mean_a
        if equal_var:
            pooled_std = np.sqrt(((n_a-1)*std_a**2 + (n_b-1)*std_b**2) / (n_a+n_b-2))
            se_diff = pooled_std * np.sqrt(1/n_a + 1/n_b)
            df = n_a + n_b - 2
        else:
            se_diff = np.sqrt(std_a**2/n_a + std_b**2/n_b)
            df = (std_a**2/n_a + std_b**2/n_b)**2 / (
                (std_a**2/n_a)**2/(n_a-1) + (std_b**2/n_b)**2/(n_b-1)
            )
        
        t_critical = stats.t.ppf(1 - self.alpha/2, df)
        ci_lower = diff - t_critical * se_diff
        ci_upper = diff + t_critical * se_diff
        
        # Taille d'effet (Cohen's d)
        pooled_std_effect = np.sqrt(((n_a-1)*std_a**2 + (n_b-1)*std_b**2) / (n_a+n_b-2))
        cohens_d = diff / pooled_std_effect
        
        return {
            "test_type": "t-test",
            "statistic": t_stat,
            "p_value": p_value,
            "significant": p_value < self.alpha,
            "confidence_interval": (ci_lower, ci_upper),
            "effect_size": cohens_d,
            "group_a": {"n": n_a, "mean": mean_a, "std": std_a},
            "group_b": {"n": n_b, "mean": mean_b, "std": std_b},
            "difference": diff,
            "relative_change": (diff / mean_a) * 100 if mean_a != 0 else 0
        }
    
    def z_test_proportions(self, successes_a: int, n_a: int, 
                          successes_b: int, n_b: int) -> Dict:
        """Test Z pour comparer deux proportions"""
        
        p_a = successes_a / n_a
        p_b = successes_b / n_b
        
        # Proportion poolée
        p_pool = (successes_a + successes_b) / (n_a + n_b)
        
        # Erreur standard
        se = np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
        
        # Statistique Z
        z_stat = (p_b - p_a) / se if se > 0 else 0
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        
        # Intervalle de confiance pour la différence
        diff = p_b - p_a
        se_diff = np.sqrt(p_a*(1-p_a)/n_a + p_b*(1-p_b)/n_b)
        z_critical = stats.norm.ppf(1 - self.alpha/2)
        ci_lower = diff - z_critical * se_diff
        ci_upper = diff + z_critical * se_diff
        
        # Taille d'effet (h de Cohen)
        h = 2 * (np.arcsin(np.sqrt(p_b)) - np.arcsin(np.sqrt(p_a)))
        
        return {
            "test_type": "z-test",
            "statistic": z_stat,
            "p_value": p_value,
            "significant": p_value < self.alpha,
            "confidence_interval": (ci_lower, ci_upper),
            "effect_size": h,
            "group_a": {"n": n_a, "successes": successes_a, "rate": p_a},
            "group_b": {"n": n_b, "successes": successes_b, "rate": p_b},
            "difference": diff,
            "relative_change": (diff / p_a) * 100 if p_a != 0 else 0
        }
    
    def chi2_test(self, contingency_table: np.array) -> Dict:
        """Test du chi-carré d'indépendance"""
        
        chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        # Cramér's V (taille d'effet)
        n = np.sum(contingency_table)
        cramers_v = np.sqrt(chi2_stat / (n * (min(contingency_table.shape) - 1)))
        
        return {
            "test_type": "chi2-test",
            "statistic": chi2_stat,
            "p_value": p_value,
            "degrees_of_freedom": dof,
            "significant": p_value < self.alpha,
            "effect_size": cramers_v,
            "observed": contingency_table,
            "expected": expected
        }
    
    def calculate_sample_size(self, effect_size: float, power: float = 0.8, 
                            test_type: str = "t_test") -> int:
        """Calcule la taille d'échantillon nécessaire"""
        
        alpha = self.alpha
        beta = 1 - power
        
        if test_type == "t_test":
            # Pour un test t bilatéral
            z_alpha = stats.norm.ppf(1 - alpha/2)
            z_beta = stats.norm.ppf(power)
            n = 2 * ((z_alpha + z_beta) / effect_size) ** 2
        
        elif test_type == "z_test":
            # Pour un test z de proportions
            z_alpha = stats.norm.ppf(1 - alpha/2)
            z_beta = stats.norm.ppf(power)
            n = 2 * ((z_alpha + z_beta) / effect_size) ** 2
        
        else:
            n = 100  # Valeur par défaut
        
        return max(int(np.ceil(n)), 10)
    
    def calculate_power(self, effect_size: float, sample_size: int, 
                       test_type: str = "t_test") -> float:
        """Calcule la puissance statistique"""
        
        alpha = self.alpha
        
        if test_type == "t_test":
            z_alpha = stats.norm.ppf(1 - alpha/2)
            z_beta = effect_size * np.sqrt(sample_size/2) - z_alpha
            power = stats.norm.cdf(z_beta)
        
        elif test_type == "z_test":
            z_alpha = stats.norm.ppf(1 - alpha/2)
            z_beta = effect_size * np.sqrt(sample_size/2) - z_alpha
            power = stats.norm.cdf(z_beta)
        
        else:
            power = 0.8  # Valeur par défaut
        
        return max(0, min(1, power))


class DataGenerator:
    """Générateur de données pour tests A/B"""
    
    @staticmethod
    def generate_continuous_data(n_a: int, n_b: int, mean_a: float, mean_b: float,
                               std_a: float = 1.0, std_b: float = 1.0) -> Tuple[np.array, np.array]:
        """Génère des données continues pour test t"""
        group_a = np.random.normal(mean_a, std_a, n_a)
        group_b = np.random.normal(mean_b, std_b, n_b)
        return group_a, group_b
    
    @staticmethod
    def generate_binary_data(n_a: int, n_b: int, p_a: float, p_b: float) -> Tuple[int, int]:
        """Génère des données binaires pour test z"""
        successes_a = np.random.binomial(n_a, p_a)
        successes_b = np.random.binomial(n_b, p_b)
        return successes_a, successes_b
