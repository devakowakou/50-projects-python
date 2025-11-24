"""Pipeline principal de nettoyage de données."""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
import time

from .data_loader import DataLoader
from .data_profiler import DataProfiler
from .data_cleaner import DataCleaner
from .data_exporter import DataExporter
from ..config import CLEANING_CONFIG

console = Console()

class DataCleaningPipeline:
    """Pipeline complet de nettoyage de données."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or CLEANING_CONFIG
        self.loader = DataLoader()
        self.profiler = DataProfiler()
        self.cleaner = DataCleaner(self.config)
        self.exporter = DataExporter()
    
    def process_file(self, input_path: str, output_path: str, 
                    strategies: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Traite un fichier complet avec le pipeline."""
        start_time = time.time()
        
        # Mise à jour de la config si stratégies personnalisées
        if strategies:
            self._update_config(strategies)
            self.cleaner = DataCleaner(self.config)
        
        console.print(Panel.fit(
            f"🚀 PIPELINE DE NETTOYAGE\n"
            f"📁 Fichier : {Path(input_path).name}\n"
            f"📤 Sortie : {Path(output_path).name}",
            title="Début du traitement"
        ))
        
        try:
            # 1. Chargement
            df, load_metadata = self.loader.load_file(input_path)
            
            # 2. Profilage initial
            initial_profile = self.profiler.profile_dataframe(df)
            quality_before = self.profiler.get_quality_score(initial_profile)
            
            # 3. Nettoyage
            df_cleaned, cleaning_report = self.cleaner.clean_dataframe(df)
            
            # 4. Profilage final
            final_profile = self.profiler.profile_dataframe(df_cleaned)
            quality_after = self.profiler.get_quality_score(final_profile)
            
            # 5. Export
            export_metadata = self.exporter.export_dataframe(
                df_cleaned, output_path, 
                include_report=True,
                metadata={
                    'initial_profile': initial_profile,
                    'final_profile': final_profile,
                    'cleaning_report': cleaning_report,
                    'load_metadata': load_metadata
                }
            )
            
            # Résumé final
            processing_time = time.time() - start_time
            
            result = {
                'success': True,
                'input_file': str(input_path),
                'output_file': str(output_path),
                'processing_time': processing_time,
                'quality_improvement': quality_after - quality_before,
                'summary': {
                    'original_rows': initial_profile['overview']['rows'],
                    'final_rows': final_profile['overview']['rows'],
                    'rows_removed': initial_profile['overview']['rows'] - final_profile['overview']['rows'],
                    'quality_before': quality_before,
                    'quality_after': quality_after,
                    'operations_count': len(cleaning_report['operations'])
                }
            }
            
            self._display_final_summary(result)
            
            return result
            
        except Exception as e:
            console.print(f"❌ Erreur dans le pipeline : {e}")
            return {
                'success': False,
                'error': str(e),
                'input_file': str(input_path)
            }
    
    def process_directory(self, input_dir: str, output_dir: str) -> Dict[str, Any]:
        """Traite tous les fichiers d'un dossier."""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Dossier non trouvé : {input_dir}")
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Trouver tous les fichiers supportés
        supported_files = []
        for ext in self.loader.supported_formats:
            supported_files.extend(input_path.glob(f"*{ext}"))
        
        console.print(f"📁 Traitement de {len(supported_files)} fichiers...")
        
        results = []
        for file_path in supported_files:
            output_file = output_path / f"cleaned_{file_path.name}"
            result = self.process_file(str(file_path), str(output_file))
            results.append(result)
        
        # Résumé global
        successful = sum(1 for r in results if r['success'])
        total_time = sum(r.get('processing_time', 0) for r in results)
        
        return {
            'total_files': len(supported_files),
            'successful': successful,
            'failed': len(supported_files) - successful,
            'total_processing_time': total_time,
            'results': results
        }
    
    def _update_config(self, strategies: Dict[str, Any]) -> None:
        """Met à jour la configuration avec les stratégies personnalisées."""
        if 'missing_values' in strategies:
            self.config['missing_values']['strategy'] = strategies['missing_values']
        
        if 'outliers' in strategies:
            self.config['outliers']['method'] = strategies['outliers']
        
        if 'duplicates' in strategies:
            self.config['duplicates']['keep'] = 'first' if strategies['duplicates'] else False
        
        if 'standardize' in strategies and strategies['standardize']:
            # Activer toutes les standardisations
            for key in self.config['standardization']:
                if isinstance(self.config['standardization'][key], bool):
                    self.config['standardization'][key] = True
    
    def _display_final_summary(self, result: Dict[str, Any]) -> None:
        """Affiche le résumé final du traitement."""
        summary = result['summary']
        
        console.print(Panel.fit(
            f"✅ TRAITEMENT TERMINÉ\n\n"
            f"📊 Lignes : {summary['original_rows']:,} → {summary['final_rows']:,} "
            f"({summary['rows_removed']:+,})\n"
            f"🎯 Qualité : {summary['quality_before']:.1f}% → {summary['quality_after']:.1f}% "
            f"({result['quality_improvement']:+.1f}%)\n"
            f"🔧 Opérations : {summary['operations_count']}\n"
            f"⏱️ Temps : {result['processing_time']:.2f}s",
            title="Résumé",
            style="green"
        ))
    
    def get_config(self) -> Dict[str, Any]:
        """Retourne la configuration actuelle."""
        return self.config.copy()
    
    def set_config(self, config: Dict[str, Any]) -> None:
        """Définit une nouvelle configuration."""
        self.config = config
        self.cleaner = DataCleaner(self.config)