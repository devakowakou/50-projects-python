"""
Générateur de graphiques
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile
from config import CHART_CONFIG, TEMP_DIR

class ChartGenerator:
    """Générateur de graphiques pour rapports"""
    
    def __init__(self, template_type: str = "commercial"):
        self.template_type = template_type
        self.temp_files = []
        
        # Configuration style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette(CHART_CONFIG["colors"])
    
    def plot_timeseries(
        self, 
        df: pd.DataFrame, 
        date_col: str, 
        value_col: str,
        title: str = "Évolution temporelle"
    ) -> str:
        """
        Crée un graphique de série temporelle
        
        Args:
            df: DataFrame
            date_col: Colonne de dates
            value_col: Colonne de valeurs
            title: Titre du graphique
            
        Returns:
            Chemin du fichier image
        """
        fig, ax = plt.subplots(figsize=CHART_CONFIG["figure_size"])
        
        # Plot
        ax.plot(df[date_col], df[value_col], marker='o', linewidth=2)
        
        # Styling
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel(date_col, fontsize=12)
        ax.set_ylabel(value_col, fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Sauvegarde
        output_path = self._save_figure(fig, "timeseries")
        plt.close(fig)
        
        return output_path
    
    def plot_bar(
        self,
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        title: str = "Graphique en barres"
    ) -> str:
        """Crée un graphique en barres"""
        fig, ax = plt.subplots(figsize=CHART_CONFIG["figure_size"])
        
        # Limiter à top 10
        data = df.nlargest(10, y_col) if len(df) > 10 else df
        
        ax.bar(data[x_col], data[y_col], color=CHART_CONFIG["colors"][0])
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_col, fontsize=12)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        output_path = self._save_figure(fig, "bar")
        plt.close(fig)
        
        return output_path
    
    def plot_pie(
        self,
        df: pd.DataFrame,
        labels_col: str,
        values_col: str,
        title: str = "Répartition"
    ) -> str:
        """Crée un graphique en camembert"""
        fig, ax = plt.subplots(figsize=CHART_CONFIG["figure_size"])
        
        # Top 5 + Autres
        data = df.nlargest(5, values_col)
        
        ax.pie(
            data[values_col], 
            labels=data[labels_col],
            autopct='%1.1f%%',
            startangle=90,
            colors=CHART_CONFIG["colors"]
        )
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        
        output_path = self._save_figure(fig, "pie")
        plt.close(fig)
        
        return output_path
    
    def _save_figure(self, fig, chart_type: str) -> str:
        """Sauvegarde une figure et retourne le chemin"""
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".png",
            dir=TEMP_DIR,
            prefix=f"{chart_type}_"
        )
        
        filepath = temp_file.name
        fig.savefig(filepath, dpi=CHART_CONFIG["dpi"], bbox_inches='tight')
        
        self.temp_files.append(filepath)
        
        return filepath
    
    def cleanup(self):
        """Nettoie les fichiers temporaires"""
        import os
        for filepath in self.temp_files:
            try:
                if os.path.exists(filepath):
                    os.unlink(filepath)
            except Exception:
                pass
        
        self.temp_files = []