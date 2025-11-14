"""Utilitaires pour A/B Test Calculator"""

import pandas as pd
import streamlit as st
import json
from datetime import datetime
from typing import Dict

class DataLoader:
    @staticmethod
    def load_csv_data(uploaded_file) -> pd.DataFrame:
        """Charge CSV"""
        try:
            return pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Erreur: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def validate_ab_data(df: pd.DataFrame, group_col: str, metric_col: str) -> bool:
        """Valide données A/B"""
        if df.empty or group_col not in df.columns or metric_col not in df.columns:
            return False
        return len(df[group_col].unique()) == 2

class ResultsFormatter:
    @staticmethod
    def format_test_results(test_result: Dict) -> Dict[str, str]:
        """Formate résultats"""
        return {
            "Test": test_result['test_type'].upper(),
            "Statistique": f"{test_result['statistic']:.4f}",
            "P-value": f"{test_result['p_value']:.6f}",
            "Significatif": "✅ Oui" if test_result['significant'] else "❌ Non",
            "Taille d'effet": f"{test_result['effect_size']:.4f}",
            "Différence": f"{test_result['difference']:.4f}",
            "Changement": f"{test_result['relative_change']:+.2f}%"
        }
    
    @staticmethod
    def interpret_results(test_result: Dict) -> str:
        """Interprète résultats"""
        if test_result['significant']:
            return f"✅ **Significatif** : Différence détectée.\n📈 Amélioration: **{test_result['relative_change']:+.1f}%**"
        else:
            return "❌ **Non significatif** : Pas de différence détectée.\n🔍 Continuez le test ou augmentez l'échantillon."

class ExportUtils:
    @staticmethod
    def export_results_json(test_result: Dict) -> str:
        """Export JSON"""
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "results": test_result
        }
        return json.dumps(export_data, indent=2, default=str)
    
    @staticmethod
    def create_report(test_result: Dict, interpretation: str) -> str:
        """Crée rapport"""
        return f"""# Rapport A/B Test

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Résultats
- **Test**: {test_result['test_type'].upper()}
- **Statistique**: {test_result['statistic']:.4f}
- **P-value**: {test_result['p_value']:.6f}
- **Significatif**: {'Oui' if test_result['significant'] else 'Non'}

## Interprétation
{interpretation}
"""