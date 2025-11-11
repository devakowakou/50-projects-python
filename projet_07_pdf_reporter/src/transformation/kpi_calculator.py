"""
Calculateur de KPIs
"""
import pandas as pd
from typing import Dict, Any
from config import KPI_CONFIG

class KPICalculator:
    """Calculateur de KPIs dynamique selon le type de données"""
    
    def __init__(self, template_type: str = "commercial"):
        self.template_type = template_type
        self.kpis = {}
    
    def calculate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calcule les KPIs selon le template
        
        Args:
            df: DataFrame
            
        Returns:
            Dictionnaire des KPIs calculés
        """
        if self.template_type == "commercial":
            self.kpis = self._calculate_commercial(df)
        elif self.template_type == "financier":
            self.kpis = self._calculate_financier(df)
        elif self.template_type == "ressources_humaines":
            self.kpis = self._calculate_rh(df)
        else:
            self.kpis = self._calculate_generic(df)
        
        return self.kpis
    
    def _calculate_commercial(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calcule KPIs commerciaux"""
        kpis = {}
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_cols:
            # Chiffre d'affaires total
            kpis['chiffre_affaires'] = df[numeric_cols[0]].sum()
            
            # Nombre de ventes
            kpis['nombre_ventes'] = len(df)
            
            # Panier moyen
            kpis['panier_moyen'] = df[numeric_cols[0]].mean() if len(numeric_cols) > 0 else 0
            
            # Évolution (si possible)
            if len(numeric_cols) > 1:
                kpis['taux_croissance'] = (
                    (df[numeric_cols[0]].sum() - df[numeric_cols[1]].sum()) / 
                    df[numeric_cols[1]].sum() * 100 if df[numeric_cols[1]].sum() != 0 else 0
                )
        
        return kpis
    
    def _calculate_financier(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calcule KPIs financiers"""
        kpis = {}
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) >= 2:
            # Revenus
            kpis['revenus'] = df[numeric_cols[0]].sum()
            
            # Dépenses
            kpis['depenses'] = df[numeric_cols[1]].sum()
            
            # Bénéfice net
            kpis['benefice_net'] = kpis['revenus'] - kpis['depenses']
            
            # Marge bénéficiaire
            kpis['marge_beneficiaire'] = (
                kpis['benefice_net'] / kpis['revenus'] * 100 
                if kpis['revenus'] != 0 else 0
            )
        
        return kpis
    
    def _calculate_rh(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calcule KPIs RH"""
        kpis = {}
        
        # Effectif total
        kpis['effectif_total'] = len(df)
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_cols:
            # Masse salariale
            kpis['masse_salariale'] = df[numeric_cols[0]].sum()
            
            # Salaire moyen
            kpis['salaire_moyen'] = df[numeric_cols[0]].mean()
            
            # Salaire médian
            kpis['salaire_median'] = df[numeric_cols[0]].median()
        
        return kpis
    
    def _calculate_generic(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calcule KPIs génériques"""
        kpis = {}
        
        # Statistiques de base
        kpis['total_lignes'] = len(df)
        kpis['total_colonnes'] = len(df.columns)
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_cols:
            kpis['somme_totale'] = df[numeric_cols].sum().sum()
            kpis['moyenne_generale'] = df[numeric_cols].mean().mean()
        
        return kpis
    
    def format_kpis_for_display(self) -> Dict[str, str]:
        """
        Formate les KPIs pour l'affichage
        
        Returns:
            Dictionnaire des KPIs formatés
        """
        formatted = {}
        
        for key, value in self.kpis.items():
            if isinstance(value, (int, float)):
                if 'taux' in key or 'marge' in key or 'croissance' in key:
                    # Formatage en pourcentage
                    formatted[key] = KPI_CONFIG['percentage_format'].format(value)
                elif 'chiffre' in key or 'revenu' in key or 'depense' in key or 'salaire' in key:
                    # Formatage monétaire
                    formatted[key] = f"{value:,.{KPI_CONFIG['decimal_places']}f} {KPI_CONFIG['currency_symbol']}".replace(',', KPI_CONFIG['thousand_separator'])
                else:
                    # Formatage numérique standard
                    formatted[key] = f"{value:,.{KPI_CONFIG['decimal_places']}f}".replace(',', KPI_CONFIG['thousand_separator'])
            else:
                formatted[key] = str(value)
        
        return formatted