"""Module d'export de données et génération de rapports."""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console
from datetime import datetime

console = Console()

class DataExporter:
    """Exporteur de données avec génération de rapports."""
    
    def __init__(self):
        self.supported_formats = {'.csv', '.parquet', '.json', '.xlsx'}
    
    def export_dataframe(self, df: pd.DataFrame, output_path: str, 
                        include_report: bool = True,
                        metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Exporte un DataFrame avec rapport optionnel."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Déterminer le format d'export
        format_ext = output_path.suffix.lower()
        if format_ext not in self.supported_formats:
            format_ext = '.csv'  # Fallback
            output_path = output_path.with_suffix('.csv')
        
        console.print(f"💾 Export vers {output_path.name} ({format_ext})...")
        
        # Export du DataFrame
        try:
            if format_ext == '.csv':
                df.to_csv(output_path, index=False, encoding='utf-8')
            elif format_ext == '.parquet':
                df.to_parquet(output_path, index=False, compression='snappy')
            elif format_ext == '.json':
                df.to_json(output_path, orient='records', indent=2)
            elif format_ext == '.xlsx':
                df.to_excel(output_path, index=False)
            
            file_size = output_path.stat().st_size / (1024 * 1024)  # MB
            
            export_metadata = {
                'output_file': str(output_path),
                'format': format_ext,
                'file_size_mb': file_size,
                'rows_exported': len(df),
                'columns_exported': len(df.columns),
                'export_timestamp': datetime.now().isoformat()
            }
            
            console.print(f"✅ Export réussi : {file_size:.2f} MB")
            
            # Génération du rapport si demandé
            if include_report and metadata:
                report_path = self._generate_report(output_path, metadata, export_metadata)
                export_metadata['report_file'] = str(report_path)
            
            return export_metadata
            
        except Exception as e:
            console.print(f"❌ Erreur d'export : {e}")
            raise
    
    def _generate_report(self, output_path: Path, metadata: Dict[str, Any], 
                        export_metadata: Dict[str, Any]) -> Path:
        """Génère un rapport de nettoyage détaillé."""
        report_path = output_path.parent / f"rapport_{output_path.stem}.txt"
        
        initial_profile = metadata.get('initial_profile', {})
        final_profile = metadata.get('final_profile', {})
        cleaning_report = metadata.get('cleaning_report', {})
        load_metadata = metadata.get('load_metadata', {})
        
        # Génération du rapport texte
        report_content = self._create_text_report(
            initial_profile, final_profile, cleaning_report, 
            load_metadata, export_metadata
        )
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # Génération du rapport JSON
        json_report_path = output_path.parent / f"rapport_{output_path.stem}.json"
        json_report = {
            'metadata': load_metadata,
            'initial_profile': initial_profile,
            'final_profile': final_profile,
            'cleaning_report': cleaning_report,
            'export_metadata': export_metadata
        }
        
        with open(json_report_path, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2, default=str)
        
        console.print(f"📋 Rapport généré : {report_path.name}")
        
        return report_path
    
    def _create_text_report(self, initial_profile: Dict[str, Any], 
                           final_profile: Dict[str, Any],
                           cleaning_report: Dict[str, Any],
                           load_metadata: Dict[str, Any],
                           export_metadata: Dict[str, Any]) -> str:
        """Crée le contenu du rapport texte."""
        
        # En-tête
        report = f"""🧹 RAPPORT DE NETTOYAGE DE DONNÉES
{'=' * 50}

📁 FICHIER TRAITÉ
├── Nom : {load_metadata.get('filename', 'N/A')}
├── Format : {load_metadata.get('format', 'N/A')}
├── Taille originale : {load_metadata.get('size_mb', 0):.2f} MB
├── Encodage : {load_metadata.get('encoding', 'N/A')}
└── Séparateur : {load_metadata.get('separator', 'N/A')}

📊 RÉSUMÉ DES TRANSFORMATIONS
├── Lignes : {initial_profile.get('overview', {}).get('rows', 0):,} → {final_profile.get('overview', {}).get('rows', 0):,} ({cleaning_report.get('rows_removed', 0):+,})
├── Colonnes : {initial_profile.get('overview', {}).get('columns', 0)} → {final_profile.get('overview', {}).get('columns', 0)} ({cleaning_report.get('columns_removed', 0):+})
├── Valeurs manquantes : {initial_profile.get('overview', {}).get('missing_cells', 0):,} → {final_profile.get('overview', {}).get('missing_cells', 0):,}
├── Doublons : {initial_profile.get('duplicates', {}).get('total_duplicates', 0):,} → {final_profile.get('duplicates', {}).get('total_duplicates', 0):,}
└── Mémoire : {initial_profile.get('overview', {}).get('memory_usage_mb', 0):.2f} → {final_profile.get('overview', {}).get('memory_usage_mb', 0):.2f} MB

🔧 OPÉRATIONS EFFECTUÉES
"""
        
        # Opérations de nettoyage
        operations = cleaning_report.get('operations', [])
        for i, operation in enumerate(operations, 1):
            report += f"├── {i}. {operation}\n"
        
        if not operations:
            report += "└── Aucune opération effectuée\n"
        else:
            report = report.rstrip('\n') + '\n'
            report = report[:-4] + '└──' + report[-2:]
        
        # Qualité des données
        initial_quality = self._calculate_quality_score(initial_profile)
        final_quality = self._calculate_quality_score(final_profile)
        
        report += f"""
🎯 QUALITÉ DES DONNÉES
├── Score initial : {initial_quality:.1f}%
├── Score final : {final_quality:.1f}%
└── Amélioration : {final_quality - initial_quality:+.1f}%

📈 DÉTAIL PAR COLONNE (TOP 10 PROBLÉMATIQUES)
"""
        
        # Top colonnes avec problèmes
        problematic_cols = self._get_problematic_columns(initial_profile)
        for i, (col, issues) in enumerate(problematic_cols[:10], 1):
            report += f"├── {i}. {col} : {issues}\n"
        
        if not problematic_cols:
            report += "└── Aucune colonne problématique détectée\n"
        else:
            report = report.rstrip('\n') + '\n'
            report = report[:-4] + '└──' + report[-2:]
        
        # Métadonnées d'export
        report += f"""
💾 EXPORT
├── Fichier de sortie : {export_metadata.get('output_file', 'N/A')}
├── Format : {export_metadata.get('format', 'N/A')}
├── Taille finale : {export_metadata.get('file_size_mb', 0):.2f} MB
├── Lignes exportées : {export_metadata.get('rows_exported', 0):,}
├── Colonnes exportées : {export_metadata.get('columns_exported', 0)}
└── Timestamp : {export_metadata.get('export_timestamp', 'N/A')}

⏱️ PERFORMANCE
└── Traitement terminé le : {cleaning_report.get('cleaning_timestamp', 'N/A')}

{'=' * 50}
🎉 Nettoyage terminé avec succès !
Dataset prêt pour l'analyse ou la modélisation.
"""
        
        return report
    
    def _calculate_quality_score(self, profile: Dict[str, Any]) -> float:
        """Calcule un score de qualité simple."""
        overview = profile.get('overview', {})
        duplicates = profile.get('duplicates', {})
        
        if not overview:
            return 0.0
        
        completeness = 100 - overview.get('missing_percentage', 100)
        uniqueness = 100 - duplicates.get('duplicate_percentage', 0)
        
        return (completeness * 0.6) + (uniqueness * 0.4)
    
    def _get_problematic_columns(self, profile: Dict[str, Any]) -> list:
        """Identifie les colonnes les plus problématiques."""
        columns_profile = profile.get('columns', {})
        problematic = []
        
        for col, col_profile in columns_profile.items():
            issues = []
            
            null_pct = col_profile.get('null_percentage', 0)
            if null_pct > 20:
                issues.append(f"{null_pct:.1f}% manquant")
            
            unique_pct = col_profile.get('unique_percentage', 0)
            if unique_pct < 10 and col_profile.get('unique_count', 0) > 1:
                issues.append(f"peu de variété ({unique_pct:.1f}%)")
            
            if issues:
                problematic.append((col, ", ".join(issues)))
        
        # Trier par nombre de problèmes
        return sorted(problematic, key=lambda x: len(x[1]), reverse=True)
    
    def export_sample(self, df: pd.DataFrame, output_path: str, 
                     sample_size: int = 1000) -> Dict[str, Any]:
        """Exporte un échantillon du DataFrame."""
        sample_df = df.sample(n=min(sample_size, len(df)), random_state=42)
        
        sample_path = Path(output_path).parent / f"sample_{Path(output_path).name}"
        
        return self.export_dataframe(sample_df, str(sample_path), include_report=False)