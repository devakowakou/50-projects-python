"""
Module de génération des graphiques
"""
import matplotlib
matplotlib.use('Agg')  # Backend non-interactif pour Streamlit
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import tempfile
from pathlib import Path
from typing import Optional, List, Tuple
from src.utils.logger import setup_logger
from src.visualization.chart_config import (
    get_chart_config, 
    TEMPLATE_COLORS,
    MATPLOTLIB_STYLE
)

logger = setup_logger(__name__)

# Définir le style matplotlib
plt.style.use(MATPLOTLIB_STYLE)

class ChartGenerator:
    """Classe pour générer des graphiques"""
    
    def __init__(self, template_type: str = "commercial"):
        self.template_type = template_type
        self.colors = TEMPLATE_COLORS.get(template_type, TEMPLATE_COLORS["commercial"])
        self.charts_created = []
    
    def _save_chart(self, fig, filename: Optional[str] = None) -> str:
        """
        Sauvegarde un graphique et retourne le chemin
        
        Args:
            fig: Figure matplotlib
            filename: Nom du fichier (auto-généré si None)
        
        Returns:
            Chemin du fichier PNG
        """
        if filename is None:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            filepath = tmp.name
        else:
            filepath = filename
        
        fig.tight_layout()
        fig.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        
        self.charts_created.append(filepath)
        logger.info(f"💾 Graphique sauvegardé: {Path(filepath).name}")
        
        return filepath
    
    def plot_timeseries(
        self,
        df: pd.DataFrame,
        date_column: str,
        value_column: str,
        title: str = "Évolution temporelle",
        ylabel: str = "Valeur"
    ) -> str:
        """
        Génère un graphique de série temporelle
        
        Args:
            df: DataFrame
            date_column: Colonne de dates
            value_column: Colonne de valeurs
            title: Titre du graphique
            ylabel: Label axe Y
        
        Returns:
            Chemin du fichier PNG
        """
        config = get_chart_config("line", "medium")
        
        fig, ax = plt.subplots(figsize=config["figsize"], dpi=config["dpi"])
        
        ax.plot(
            df[date_column],
            df[value_column],
            color=self.colors[0],
            **config["style"]
        )
        
        ax.set_title(title, fontsize=config["axis"]["title_fontsize"], fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=config["axis"]["label_fontsize"])
        ax.grid(True, alpha=config["axis"]["grid_alpha"], linestyle=config["axis"]["grid_linestyle"])
        
        # Rotation des labels de dates
        plt.xticks(rotation=45, ha='right')
        
        return self._save_chart(fig)
    
    def plot_bar_chart(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        title: str = "Comparaison",
        top_n: Optional[int] = None,
        horizontal: bool = False
    ) -> str:
        """
        Génère un graphique en barres
        
        Args:
            df: DataFrame
            x_column: Colonne X
            y_column: Colonne Y
            title: Titre
            top_n: Afficher seulement les N premiers
            horizontal: Barres horizontales
        
        Returns:
            Chemin du fichier PNG
        """
        config = get_chart_config("bar", "medium")
        
        # Filtrer top N si spécifié
        if top_n:
            df = df.nlargest(top_n, y_column)
        
        fig, ax = plt.subplots(figsize=config["figsize"], dpi=config["dpi"])
        
        if horizontal:
            ax.barh(df[x_column], df[y_column], color=self.colors[0], **config["style"])
            ax.set_xlabel(y_column, fontsize=config["axis"]["label_fontsize"])
        else:
            ax.bar(df[x_column], df[y_column], color=self.colors[0], **config["style"])
            ax.set_ylabel(y_column, fontsize=config["axis"]["label_fontsize"])
            plt.xticks(rotation=45, ha='right')
        
        ax.set_title(title, fontsize=config["axis"]["title_fontsize"], fontweight='bold')
        ax.grid(True, alpha=config["axis"]["grid_alpha"], axis='y')
        
        return self._save_chart(fig)
    
    def plot_pie_chart(
        self,
        data: dict,
        title: str = "Répartition",
        top_n: Optional[int] = 5
    ) -> str:
        """
        Génère un graphique camembert
        
        Args:
            data: Dictionnaire {label: valeur}
            title: Titre
            top_n: Afficher les N premiers + "Autres"
        
        Returns:
            Chemin du fichier PNG
        """
        config = get_chart_config("pie", "medium")
        
        # Trier et limiter
        sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
        
        if top_n and len(sorted_data) > top_n:
            top_items = dict(list(sorted_data.items())[:top_n])
            others_sum = sum(list(sorted_data.values())[top_n:])
            top_items["Autres"] = others_sum
            sorted_data = top_items
        
        fig, ax = plt.subplots(figsize=config["figsize"], dpi=config["dpi"])
        
        ax.pie(
            sorted_data.values(),
            labels=sorted_data.keys(),
            colors=self.colors,
            **config["style"]
        )
        
        ax.set_title(title, fontsize=config["axis"]["title_fontsize"], fontweight='bold')
        
        return self._save_chart(fig)
    
    def plot_multi_lines(
        self,
        df: pd.DataFrame,
        date_column: str,
        value_columns: List[str],
        title: str = "Comparaison multi-séries",
        ylabel: str = "Valeur"
    ) -> str:
        """
        Génère un graphique avec plusieurs séries
        
        Args:
            df: DataFrame
            date_column: Colonne de dates
            value_columns: Liste des colonnes à tracer
            title: Titre
            ylabel: Label axe Y
        
        Returns:
            Chemin du fichier PNG
        """
        config = get_chart_config("line", "medium")
        
        fig, ax = plt.subplots(figsize=config["figsize"], dpi=config["dpi"])
        
        for i, col in enumerate(value_columns):
            color = self.colors[i % len(self.colors)]
            ax.plot(
                df[date_column],
                df[col],
                label=col,
                color=color,
                **config["style"]
            )
        
        ax.set_title(title, fontsize=config["axis"]["title_fontsize"], fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=config["axis"]["label_fontsize"])
        ax.legend(loc='best')
        ax.grid(True, alpha=config["axis"]["grid_alpha"])
        
        plt.xticks(rotation=45, ha='right')
        
        return self._save_chart(fig)
    
    def cleanup(self):
        """Supprime les fichiers temporaires créés"""
        for filepath in self.charts_created:
            try:
                Path(filepath).unlink(missing_ok=True)
            except Exception as e:
                logger.warning(f"⚠️ Impossible de supprimer {filepath}: {e}")
        
        logger.info(f"🧹 {len(self.charts_created)} graphiques nettoyés")
        self.charts_created = []