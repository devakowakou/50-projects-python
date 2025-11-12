"""
Utilitaires pour la calculatrice A/B Test
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import streamlit as st
from datetime import datetime
import json


class DataLoader:
    """Chargeur de données pour tests A/B"""
    
    @staticmethod
    def load_csv_data(uploaded_file) -> pd.DataFrame:
        """Charge des données depuis un fichier CSV"""
        try:
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Erreur lors du chargement: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def validate_ab_data(df: pd.DataFrame, group_col: str, metric_col: str) -> bool:
        """Valide les données A/B"""
        if df.empty:
            return False
        
        if group_col not in df.columns or metric_col not in df.columns:
            st.error(f"Colonnes manquantes: {group_col} ou {metric_col}")
            return False
        
        groups = df[group_col].unique()
        if len(groups) != 2:
            st.error(f"Il faut exactement 2 groupes, trouvé: {len(groups)}")
            return False
        
        return True


class ResultsFormatter:
    """Formateur de résultats pour l'affichage"""
    
    @staticmethod
    def format_test_results(test_result: Dict) -> Dict[str, str]:
        """Formate les résultats pour l'affichage"""
        
        formatted = {
            "Test": test_result['test_type'].upper(),
            "Statistique": f"{test_result['statistic']:.4f}",
            "P-value": f"{test_result['p_value']:.6f}",
            "Significatif": "✅ Oui" if test_result['significant'] else "❌ Non",
            "Taille d'effet": f"{test_result['effect_size']:.4f}"
        }
        
        if 'difference' in test_result:
            formatted["Différence"] = f"{test_result['difference']:.4f}"
            formatted["Changement relatif"] = f"{test_result['relative_change']:+.2f}%"
        
        if 'confidence_interval' in test_result:
            ci_lower, ci_upper = test_result['confidence_interval']
            formatted["Intervalle confiance"] = f"[{ci_lower:.4f}, {ci_upper:.4f}]"
        
        return formatted
    
    @staticmethod
    def interpret_results(test_result: Dict) -> str:
        """Interprète les résultats en langage naturel"""
        
        if test_result['test_type'] == 't-test':
            return ResultsFormatter._interpret_t_test(test_result)
        elif test_result['test_type'] == 'z-test':
            return ResultsFormatter._interpret_z_test(test_result)
        elif test_result['test_type'] == 'chi2-test':
            return ResultsFormatter._interpret_chi2_test(test_result)
        else:
            return "Résultats non interprétables"
    
    @staticmethod
    def _interpret_t_test(result: Dict) -> str:
        """Interprétation du t-test"""
        
        interpretation = []
        
        if result['significant']:
            interpretation.append("✅ **Résultat significatif** : Il y a une différence statistiquement significative entre les groupes.")
            
            if result['difference'] > 0:
                interpretation.append(f"📈 Le groupe B performe **{result['relative_change']:+.1f}%** mieux que le groupe A.")
            else:
                interpretation.append(f"📉 Le groupe B performe **{result['relative_change']:+.1f}%** moins bien que le groupe A.")
        else:
            interpretation.append("❌ **Résultat non significatif** : Pas de différence statistiquement significative détectée.")
            interpretation.append("🔍 Considérez augmenter la taille d'échantillon ou la durée du test.")
        
        # Taille d'effet
        effect_size = abs(result['effect_size'])
        if effect_size < 0.2:
            interpretation.append("📏 **Taille d'effet faible** (< 0.2)")
        elif effect_size < 0.5:
            interpretation.append("📏 **Taille d'effet moyenne** (0.2 - 0.5)")
        else:
            interpretation.append("📏 **Taille d'effet importante** (> 0.5)")
        
        return "\n\n".join(interpretation)
    
    @staticmethod
    def _interpret_z_test(result: Dict) -> str:
        """Interprétation du z-test"""
        
        interpretation = []
        
        if result['significant']:
            interpretation.append("✅ **Différence significative** dans les taux de conversion.")
            
            rate_a = result['group_a']['rate']
            rate_b = result['group_b']['rate']
            
            interpretation.append(f"📊 **Groupe A** : {rate_a:.1%} de conversion")
            interpretation.append(f"📊 **Groupe B** : {rate_b:.1%} de conversion")
            interpretation.append(f"📈 **Amélioration** : {result['relative_change']:+.1f}%")
        else:
            interpretation.append("❌ **Pas de différence significative** dans les taux de conversion.")
            interpretation.append("🔍 Continuez le test ou augmentez la taille d'échantillon.")
        
        return "\n\n".join(interpretation)
    
    @staticmethod
    def _interpret_chi2_test(result: Dict) -> str:
        """Interprétation du test chi-carré"""
        
        interpretation = []
        
        if result['significant']:
            interpretation.append("✅ **Association significative** entre les variables.")
            interpretation.append(f"📊 **Cramér's V** : {result['effect_size']:.3f}")
        else:
            interpretation.append("❌ **Pas d'association significative** entre les variables.")
        
        return "\n\n".join(interpretation)


class ExportUtils:
    """Utilitaires d'export des résultats"""
    
    @staticmethod
    def export_results_json(test_result: Dict, metadata: Dict = None) -> str:
        """Exporte les résultats en JSON"""
        
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "test_results": test_result,
            "metadata": metadata or {}
        }
        
        return json.dumps(export_data, indent=2, default=str)
    
    @staticmethod
    def create_report(test_result: Dict, interpretation: str) -> str:
        """Crée un rapport complet"""
        
        report = f"""# Rapport de Test A/B

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Résultats du Test

**Type de test**: {test_result['test_type'].upper()}
**Statistique**: {test_result['statistic']:.4f}
**P-value**: {test_result['p_value']:.6f}
**Significatif**: {'Oui' if test_result['significant'] else 'Non'}

## Interprétation

{interpretation}

## Données Techniques

```json
{json.dumps(test_result, indent=2, default=str)}
```

---
*Rapport généré par A/B Test Calculator*
"""
        
        return report


class SampleSizeHelper:
    """Assistant pour le calcul de taille d'échantillon"""
    
    @staticmethod
    def estimate_test_duration(sample_size_per_group: int, daily_visitors: int, 
                             allocation_ratio: float = 0.5) -> Dict:
        """Estime la durée nécessaire du test"""
        
        total_sample_needed = sample_size_per_group * 2
        daily_sample = daily_visitors * allocation_ratio
        
        if daily_sample <= 0:
            return {"error": "Nombre de visiteurs quotidiens invalide"}
        
        days_needed = total_sample_needed / daily_sample
        weeks_needed = days_needed / 7
        
        return {
            "days": int(np.ceil(days_needed)),
            "weeks": round(weeks_needed, 1),
            "total_sample_needed": total_sample_needed,
            "daily_sample_rate": int(daily_sample)
        }
    
    @staticmethod
    def minimum_detectable_effect(sample_size: int, power: float = 0.8, 
                                alpha: float = 0.05) -> float:
        """Calcule l'effet minimum détectable"""
        
        from scipy import stats
        
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(power)
        
        mde = (z_alpha + z_beta) * np.sqrt(2/sample_size)
        
        return mde