"""
Module de calcul des KPIs métier - VERSION FLEXIBLE
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional
from src.utils.logger import setup_logger
from src.utils.helpers import safe_division

logger = setup_logger(__name__)

class KPICalculator:
    """Classe pour calculer les indicateurs clés de performance de manière flexible"""
    
    def __init__(self, template_type: str = "generic"):
        self.template_type = template_type
        self.kpis = {}
    
    def calculate_generic_kpis(self, df: pd.DataFrame) -> Dict:
        """
        Calcule des KPIs génériques pour n'importe quel dataset
        
        Args:
            df: DataFrame
        
        Returns:
            Dictionnaire de KPIs
        """
        logger.info("📊 Calcul des KPIs génériques...")
        
        kpis = {}
        
        try:
            # KPIs basiques
            kpis["total_lignes"] = len(df)
            kpis["total_colonnes"] = len(df.columns)
            
            # Colonnes numériques
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            kpis["colonnes_numeriques"] = len(numeric_cols)
            
            if len(numeric_cols) > 0:
                # Prendre la première colonne numérique pour des stats
                main_col = numeric_cols[0]
                kpis[f"somme_{main_col}"] = float(df[main_col].sum())
                kpis[f"moyenne_{main_col}"] = float(df[main_col].mean())
                kpis[f"max_{main_col}"] = float(df[main_col].max())
                kpis[f"min_{main_col}"] = float(df[main_col].min())
            
            # Colonnes de texte
            text_cols = df.select_dtypes(include=['object']).columns
            if len(text_cols) > 0:
                main_text_col = text_cols[0]
                kpis[f"valeurs_uniques_{main_text_col}"] = int(df[main_text_col].nunique())
            
            # Taux de complétion
            completion_rate = (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            kpis["taux_completion_pct"] = round(completion_rate, 2)
            
            logger.info(f"✅ {len(kpis)} KPIs génériques calculés")
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul KPIs: {e}")
        
        self.kpis = kpis
        return kpis
    
    def calculate_commercial_kpis(self, df: pd.DataFrame) -> Dict:
        """Calcule les KPIs commerciaux si colonnes disponibles"""
        logger.info("📊 Tentative calcul KPIs commerciaux...")
        
        kpis = {}
        
        # Recherche flexible des colonnes
        price_col = self._find_column(df, ['prix', 'price', 'montant', 'amount'])
        qty_col = self._find_column(df, ['quantité', 'quantity', 'qty', 'qte'])
        ca_col = self._find_column(df, ['ca', 'chiffre', 'revenue', 'total'])
        
        if price_col:
            kpis["prix_moyen"] = float(df[price_col].mean())
        
        if qty_col:
            kpis["quantite_totale"] = int(df[qty_col].sum())
        
        if ca_col:
            kpis["ca_total"] = float(df[ca_col].sum())
        
        # Si pas assez de données commerciales, passer en mode générique
        if len(kpis) < 2:
            logger.info("Pas assez de données commerciales, passage en mode générique")
            return self.calculate_generic_kpis(df)
        
        self.kpis = kpis
        return kpis
    
    def _find_column(self, df: pd.DataFrame, keywords: list) -> Optional[str]:
        """
        Trouve une colonne par mots-clés
        
        Args:
            df: DataFrame
            keywords: Liste de mots-clés à chercher
        
        Returns:
            Nom de colonne ou None
        """
        for col in df.columns:
            col_lower = col.lower()
            if any(kw in col_lower for kw in keywords):
                return col
        return None
    
    def calculate(self, df: pd.DataFrame) -> Dict:
        """
        Calcule les KPIs selon le type de template ou en mode générique
        
        Args:
            df: DataFrame
        
        Returns:
            Dictionnaire de KPIs
        """
        if self.template_type == "commercial":
            return self.calculate_commercial_kpis(df)
        elif self.template_type == "generic":
            return self.calculate_generic_kpis(df)
        else:
            # Par défaut, mode générique
            return self.calculate_generic_kpis(df)
    
    def format_kpis_for_display(self) -> Dict[str, str]:
        """
        Formate les KPIs pour affichage
        
        Returns:
            Dictionnaire de KPIs formatés
        """
        formatted = {}
        
        for key, value in self.kpis.items():
            if isinstance(value, (int, float)):
                if "pct" in key or "taux" in key:
                    formatted[key] = f"{value:.2f}%"
                elif "ca" in key.lower() or "prix" in key.lower():
                    formatted[key] = f"{value:,.2f} €"
                else:
                    formatted[key] = f"{value:,.0f}" if isinstance(value, int) else f"{value:,.2f}"
            else:
                formatted[key] = str(value)
        
        return formatted