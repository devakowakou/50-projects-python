"""Tests statistiques pour A/B testing"""

import numpy as np
from scipy import stats
from typing import Dict, Tuple

class ABTestCalculator:
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level
        self.alpha = 1 - confidence_level
    
    def t_test_two_sample(self, group_a: np.array, group_b: np.array) -> Dict:
        """Test t pour comparer deux moyennes"""
        n_a, n_b = len(group_a), len(group_b)
        mean_a, mean_b = np.mean(group_a), np.mean(group_b)
        std_a, std_b = np.std(group_a, ddof=1), np.std(group_b, ddof=1)
        
        t_stat, p_value = stats.ttest_ind(group_a, group_b)
        diff = mean_b - mean_a
        
        # Cohen's d
        pooled_std = np.sqrt(((n_a-1)*std_a**2 + (n_b-1)*std_b**2) / (n_a+n_b-2))
        cohens_d = diff / pooled_std
        
        return {
            "test_type": "t-test",
            "statistic": t_stat,
            "p_value": p_value,
            "significant": p_value < self.alpha,
            "effect_size": cohens_d,
            "group_a": {"n": n_a, "mean": mean_a, "std": std_a},
            "group_b": {"n": n_b, "mean": mean_b, "std": std_b},
            "difference": diff,
            "relative_change": (diff / mean_a) * 100 if mean_a != 0 else 0,
            "confidence_interval": (diff - 1.96*np.sqrt(std_a**2/n_a + std_b**2/n_b), 
                                  diff + 1.96*np.sqrt(std_a**2/n_a + std_b**2/n_b))
        }
    
    def z_test_proportions(self, successes_a: int, n_a: int, successes_b: int, n_b: int) -> Dict:
        """Test Z pour comparer proportions"""
        p_a = successes_a / n_a
        p_b = successes_b / n_b
        p_pool = (successes_a + successes_b) / (n_a + n_b)
        
        se = np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
        z_stat = (p_b - p_a) / se if se > 0 else 0
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        
        diff = p_b - p_a
        h = 2 * (np.arcsin(np.sqrt(p_b)) - np.arcsin(np.sqrt(p_a)))
        
        return {
            "test_type": "z-test",
            "statistic": z_stat,
            "p_value": p_value,
            "significant": p_value < self.alpha,
            "effect_size": h,
            "group_a": {"n": n_a, "successes": successes_a, "rate": p_a},
            "group_b": {"n": n_b, "successes": successes_b, "rate": p_b},
            "difference": diff,
            "relative_change": (diff / p_a) * 100 if p_a != 0 else 0,
            "confidence_interval": (diff - 1.96*np.sqrt(p_a*(1-p_a)/n_a + p_b*(1-p_b)/n_b),
                                  diff + 1.96*np.sqrt(p_a*(1-p_a)/n_a + p_b*(1-p_b)/n_b))
        }
    
    def calculate_sample_size(self, effect_size: float, power: float = 0.8) -> int:
        """Calcule taille d'échantillon nécessaire"""
        z_alpha = stats.norm.ppf(1 - self.alpha/2)
        z_beta = stats.norm.ppf(power)
        n = 2 * ((z_alpha + z_beta) / effect_size) ** 2
        return max(int(np.ceil(n)), 10)
    
    def calculate_power(self, effect_size: float, sample_size: int) -> float:
        """Calcule la puissance statistique"""
        z_alpha = stats.norm.ppf(1 - self.alpha/2)
        z_beta = effect_size * np.sqrt(sample_size/2) - z_alpha
        power = stats.norm.cdf(z_beta)
        return max(0, min(1, power))

class DataGenerator:
    @staticmethod
    def generate_continuous_data(n_a: int, n_b: int, mean_a: float, mean_b: float,
                               std_a: float = 1.0, std_b: float = 1.0) -> Tuple[np.array, np.array]:
        """Génère données continues pour test t"""
        group_a = np.random.normal(mean_a, std_a, n_a)
        group_b = np.random.normal(mean_b, std_b, n_b)
        return group_a, group_b