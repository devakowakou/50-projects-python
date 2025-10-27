"""
Module de génération de rapports
Responsabilité: Exporter les résultats en différents formats
"""

import pandas as pd
import json
from datetime import datetime
from typing import Dict, Optional


class ReportGenerator:
    """Classe pour générer et exporter des rapports"""
    
    def __init__(self, df: pd.DataFrame, analysis_results: Dict = None):
        self.df = df
        self.analysis_results = analysis_results or {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def export_to_csv(self, filepath: str = None) -> str:
        """
        Export les données en CSV
        
        Args:
            filepath: Chemin du fichier (optionnel)
            
        Returns:
            Chemin du fichier créé
        """
        if filepath is None:
            filepath = f"export_donnees_{self.timestamp}.csv"
        
        self.df.to_csv(filepath, index=False, encoding='utf-8-sig')
        return filepath
    
    def export_statistics_to_json(self, stats_dict: Dict, 
                                  filepath: str = None) -> str:
        """
        Export les statistiques en JSON
        
        Args:
            stats_dict: Dictionnaire des statistiques
            filepath: Chemin du fichier
            
        Returns:
            Chemin du fichier créé
        """
        if filepath is None:
            filepath = f"statistiques_{self.timestamp}.json"
        
        # Convertir les valeurs numpy/pandas en types Python natifs
        def convert_to_native(obj):
            if isinstance(obj, (pd.Series, pd.DataFrame)):
                return obj.to_dict()
            elif hasattr(obj, 'item'):  # numpy types
                return obj.item()
            elif isinstance(obj, dict):
                return {k: convert_to_native(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_native(item) for item in obj]
            else:
                return obj
        
        stats_native = convert_to_native(stats_dict)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stats_native, f, indent=4, ensure_ascii=False)
        
        return filepath
    
    def generate_markdown_report(self, analysis_summary: Dict) -> str:
        """
        Génère un rapport en format Markdown
        
        Args:
            analysis_summary: Résumé de l'analyse
            
        Returns:
            Contenu du rapport en Markdown
        """
        report = f"""# 📊 Rapport d'Analyse CSV
        
**Date de génération:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📈 Informations Générales

- **Nombre de lignes:** {len(self.df):,}
- **Nombre de colonnes:** {len(self.df.columns)}
- **Colonnes numériques:** {len(self.df.select_dtypes(include=['number']).columns)}
- **Colonnes catégoriques:** {len(self.df.select_dtypes(include=['object']).columns)}

---

## 🔍 Qualité des Données

"""
        
        # Valeurs manquantes
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            report += "### ⚠️ Valeurs Manquantes\n\n"
            missing_df = missing[missing > 0].sort_values(ascending=False)
            for col, count in missing_df.items():
                percent = (count / len(self.df) * 100)
                report += f"- **{col}:** {count} ({percent:.2f}%)\n"
        else:
            report += "### ✅ Aucune valeur manquante\n\n"
        
        report += "\n---\n\n"
        
        # Duplicatas
        duplicates = self.df.duplicated().sum()
        report += f"### 🔄 Lignes Dupliquées: {duplicates}\n\n"
        
        report += "---\n\n"
        
        # Statistiques descriptives pour colonnes numériques
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            report += "## 📊 Statistiques Descriptives\n\n"
            
            for col in numeric_cols[:5]:  # Limiter à 5 colonnes
                report += f"### {col}\n\n"
                report += f"- **Moyenne:** {self.df[col].mean():.2f}\n"
                report += f"- **Médiane:** {self.df[col].median():.2f}\n"
                report += f"- **Écart-type:** {self.df[col].std():.2f}\n"
                report += f"- **Min:** {self.df[col].min():.2f}\n"
                report += f"- **Max:** {self.df[col].max():.2f}\n\n"
        
        report += "---\n\n"
        report += "*Rapport généré automatiquement par Analyseur CSV Professionnel*\n"
        
        return report
    
    def save_markdown_report(self, analysis_summary: Dict, 
                           filepath: str = None) -> str:
        """
        Sauvegarde le rapport Markdown
        
        Args:
            analysis_summary: Résumé de l'analyse
            filepath: Chemin du fichier
            
        Returns:
            Chemin du fichier créé
        """
        if filepath is None:
            filepath = f"rapport_analyse_{self.timestamp}.md"
        
        report_content = self.generate_markdown_report(analysis_summary)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return filepath
    
    def export_cleaned_data(self, cleaned_df: pd.DataFrame, 
                          filepath: str = None) -> str:
        """
        Export les données nettoyées
        
        Args:
            cleaned_df: DataFrame nettoyé
            filepath: Chemin du fichier
            
        Returns:
            Chemin du fichier créé
        """
        if filepath is None:
            filepath = f"donnees_nettoyees_{self.timestamp}.csv"
        
        cleaned_df.to_csv(filepath, index=False, encoding='utf-8-sig')
        return filepath
    
    def generate_summary_dict(self) -> Dict:
        """
        Génère un dictionnaire résumé complet
        
        Returns:
            Dictionnaire avec toutes les informations
        """
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        
        summary = {
            'metadata': {
                'date_analyse': datetime.now().isoformat(),
                'nombre_lignes': len(self.df),
                'nombre_colonnes': len(self.df.columns),
                'colonnes': self.df.columns.tolist()
            },
            'types_colonnes': {
                'numeriques': self.df.select_dtypes(include=['number']).columns.tolist(),
                'categoriques': self.df.select_dtypes(include=['object']).columns.tolist(),
                'dates': self.df.select_dtypes(include=['datetime']).columns.tolist()
            },
            'qualite': {
                'valeurs_manquantes_total': int(self.df.isnull().sum().sum()),
                'pourcentage_completude': float((1 - self.df.isnull().sum().sum() / self.df.size) * 100),
                'duplicatas': int(self.df.duplicated().sum())
            },
            'statistiques_numeriques': {}
        }
        
        # Ajouter stats pour chaque colonne numérique
        for col in numeric_cols:
            summary['statistiques_numeriques'][col] = {
                'moyenne': float(self.df[col].mean()),
                'mediane': float(self.df[col].median()),
                'ecart_type': float(self.df[col].std()),
                'min': float(self.df[col].min()),
                'max': float(self.df[col].max())
            }
        
        return summary
    
    def create_excel_report(self, stats_df: Dict[str, pd.DataFrame], 
                          filepath: str = None) -> str:
        """
        Crée un rapport Excel avec plusieurs feuilles
        
        Args:
            stats_df: Dictionnaire de DataFrames (nom_feuille: DataFrame)
            filepath: Chemin du fichier
            
        Returns:
            Chemin du fichier créé
        """
        if filepath is None:
            filepath = f"rapport_complet_{self.timestamp}.xlsx"
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Feuille des données brutes
            self.df.to_excel(writer, sheet_name='Données', index=False)
            
            # Feuilles additionnelles
            for sheet_name, df in stats_df.items():
                df.to_excel(writer, sheet_name=sheet_name, index=True)
        
        return filepath
