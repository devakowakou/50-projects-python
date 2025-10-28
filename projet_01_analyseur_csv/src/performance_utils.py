"""
Utilitaires pour mesure et affichage des performances
Version 2.2
"""

import time
import streamlit as st
from functools import wraps
from typing import Callable, Any
import config_performance as perf_config


class PerformanceMonitor:
    """Classe pour monitorer les performances"""
    
    def __init__(self):
        self.timings = {}
    
    def measure_time(self, func: Callable) -> Callable:
        """
        Décorateur pour mesurer le temps d'exécution
        
        Args:
            func: Fonction à mesurer
            
        Returns:
            Fonction wrappée
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            
            # Stocker le timing
            func_name = func.__name__
            self.timings[func_name] = elapsed_time
            
            # Logger si lent
            if perf_config.LOG_SLOW_OPERATIONS and elapsed_time > perf_config.SLOW_OPERATION_THRESHOLD:
                st.warning(f" Opération lente : {func_name} ({elapsed_time:.2f}s)")
            
            # Afficher si activé
            if perf_config.SHOW_PERFORMANCE_METRICS:
                st.caption(f"⏱️ {func_name}: {elapsed_time:.2f}s")
            
            return result
        return wrapper
    
    def get_timings(self) -> dict:
        """Retourne tous les timings enregistrés"""
        return self.timings
    
    def reset(self):
        """Réinitialise les timings"""
        self.timings = {}


def format_memory_size(bytes_size: int) -> str:
    """
    Formate une taille en bytes de manière lisible
    
    Args:
        bytes_size: Taille en bytes
        
    Returns:
        String formaté (ex: "2.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


def show_dataset_info(df, file_info: dict = None):
    """
    Affiche les informations sur le dataset avec métriques de performance
    
    Args:
        df: DataFrame
        file_info: Informations du fichier
    """
    if perf_config.SHOW_MEMORY_USAGE:
        memory_usage = df.memory_usage(deep=True).sum()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(" Lignes", f"{len(df):,}")
        with col2:
            st.metric(" Colonnes", len(df.columns))
        with col3:
            st.metric("💾 Mémoire", format_memory_size(memory_usage))
        with col4:
            if file_info and 'taille' in file_info:
                st.metric(" Taille fichier", file_info['taille'])
        
        # Avertissement si gros dataset
        if len(df) > perf_config.SAMPLE_THRESHOLD_ROWS:
            st.info(perf_config.MESSAGES['large_file_warning'])


def show_sampling_warning(total_rows: int, sample_size: int):
    """
    Affiche un avertissement sur l'échantillonnage actif
    
    Args:
        total_rows: Nombre total de lignes
        sample_size: Taille de l'échantillon
    """
    if perf_config.SHOW_SAMPLE_WARNINGS and sample_size < total_rows:
        st.warning(
            perf_config.MESSAGES['sampling_active'].format(
                sample_size=sample_size,
                total_size=total_rows
            )
        )


def show_performance_summary(monitor: PerformanceMonitor):
    """
    Affiche un résumé des performances
    
    Args:
        monitor: Instance de PerformanceMonitor
    """
    if not perf_config.SHOW_PERFORMANCE_METRICS:
        return
    
    timings = monitor.get_timings()
    if not timings:
        return
    
    with st.expander("⏱️ Résumé des performances", expanded=False):
        total_time = sum(timings.values())
        
        st.metric("Temps total", f"{total_time:.2f}s")
        
        # Détail par opération
        for func_name, elapsed in sorted(timings.items(), key=lambda x: x[1], reverse=True):
            percentage = (elapsed / total_time * 100) if total_time > 0 else 0
            st.text(f"• {func_name}: {elapsed:.2f}s ({percentage:.1f}%)")


# Instance globale du moniteur
performance_monitor = PerformanceMonitor()
