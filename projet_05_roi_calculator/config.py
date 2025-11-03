"""
Configuration et constantes pour le ROI Marketing Calculator
"""
from typing import Dict, List
from dataclasses import dataclass


# ============================================================================
# CONFIGURATION GÉNÉRALE
# ============================================================================

APP_TITLE = "📊 ROI Marketing Calculator"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Calculez le ROI et convertissez vos métriques marketing"

# Chemins
DATA_DIR = "data"
EXPORTS_DIR = f"{DATA_DIR}/exports"
HISTORY_DIR = f"{DATA_DIR}/history"

# Limites de validation
MAX_BUDGET = 10_000_000  # 10M
MIN_BUDGET = 0
MAX_IMPRESSIONS = 100_000_000  # 100M
MIN_CLICKS = 0
MAX_CONVERSIONS = 1_000_000


# ============================================================================
# FORMULES MARKETING
# ============================================================================

@dataclass
class MarketingFormulas:
    """Formules marketing standard"""
    
    @staticmethod
    def roi(revenue: float, cost: float) -> float:
        """
        ROI = (Revenu - Coût) / Coût × 100
        
        Args:
            revenue: Revenu généré
            cost: Coût de la campagne
            
        Returns:
            ROI en pourcentage
        """
        if cost == 0:
            return 0.0
        return ((revenue - cost) / cost) * 100
    
    @staticmethod
    def roas(revenue: float, cost: float) -> float:
        """
        ROAS = Revenu / Coût
        Return on Ad Spend
        """
        if cost == 0:
            return 0.0
        return revenue / cost
    
    @staticmethod
    def cpc(total_cost: float, clicks: int) -> float:
        """
        CPC = Coût Total / Nombre de Clics
        Cost Per Click
        """
        if clicks == 0:
            return 0.0
        return total_cost / clicks
    
    @staticmethod
    def cpm(total_cost: float, impressions: int) -> float:
        """
        CPM = (Coût Total / Impressions) × 1000
        Cost Per Mille (pour 1000 impressions)
        """
        if impressions == 0:
            return 0.0
        return (total_cost / impressions) * 1000
    
    @staticmethod
    def cpa(total_cost: float, conversions: int) -> float:
        """
        CPA = Coût Total / Conversions
        Cost Per Acquisition
        """
        if conversions == 0:
            return 0.0
        return total_cost / conversions
    
    @staticmethod
    def ctr(clicks: int, impressions: int) -> float:
        """
        CTR = (Clics / Impressions) × 100
        Click Through Rate
        """
        if impressions == 0:
            return 0.0
        return (clicks / impressions) * 100
    
    @staticmethod
    def conversion_rate(conversions: int, clicks: int) -> float:
        """
        Taux de Conversion = (Conversions / Clics) × 100
        """
        if clicks == 0:
            return 0.0
        return (conversions / clicks) * 100
    
    @staticmethod
    def breakeven(fixed_costs: float, price: float, variable_cost: float) -> float:
        """
        Seuil de Rentabilité = Coûts Fixes / (Prix - Coût Variable)
        """
        margin = price - variable_cost
        if margin <= 0:
            return float('inf')
        return fixed_costs / margin
    
    @staticmethod
    def cpl(total_cost: float, leads: int) -> float:
        """
        CPL = Coût Total / Leads
        Cost Per Lead
        """
        if leads == 0:
            return 0.0
        return total_cost / leads


# ============================================================================
# CONVERSIONS ENTRE MÉTRIQUES
# ============================================================================

@dataclass
class MetricConversions:
    """Conversions entre différentes métriques"""
    
    @staticmethod
    def cpc_to_cpm(cpc: float, ctr: float) -> float:
        """
        CPM = CPC × CTR × 10
        (CTR en pourcentage)
        """
        return cpc * (ctr / 100) * 1000
    
    @staticmethod
    def cpm_to_cpc(cpm: float, ctr: float) -> float:
        """
        CPC = CPM / (CTR × 10)
        """
        if ctr == 0:
            return 0.0
        return cpm / ((ctr / 100) * 1000)
    
    @staticmethod
    def cpa_to_cpc(cpa: float, conversion_rate: float) -> float:
        """
        CPC = CPA × Taux de Conversion
        """
        return cpa * (conversion_rate / 100)
    
    @staticmethod
    def cpc_to_cpa(cpc: float, conversion_rate: float) -> float:
        """
        CPA = CPC / Taux de Conversion
        """
        if conversion_rate == 0:
            return 0.0
        return cpc / (conversion_rate / 100)


# ============================================================================
# VALEURS PAR DÉFAUT
# ============================================================================

DEFAULT_METRICS = {
    "budget": 10000.0,
    "impressions": 100000,
    "clicks": 2000,
    "conversions": 100,
    "revenue": 15000.0,
    "ctr": 2.0,
    "conversion_rate": 5.0,
}

# Benchmarks par industrie (valeurs moyennes)
INDUSTRY_BENCHMARKS: Dict[str, Dict[str, float]] = {
    "E-commerce": {
        "ctr": 2.5,
        "conversion_rate": 3.0,
        "cpa": 50.0,
        "roi": 300.0,
    },
    "B2B": {
        "ctr": 1.8,
        "conversion_rate": 2.5,
        "cpa": 150.0,
        "roi": 200.0,
    },
    "SaaS": {
        "ctr": 2.2,
        "conversion_rate": 5.0,
        "cpa": 100.0,
        "roi": 400.0,
    },
    "Retail": {
        "ctr": 3.0,
        "conversion_rate": 4.0,
        "cpa": 40.0,
        "roi": 250.0,
    },
    "Services": {
        "ctr": 2.0,
        "conversion_rate": 3.5,
        "cpa": 80.0,
        "roi": 180.0,
    },
}


# ============================================================================
# STYLE ET THÈME
# ============================================================================

# Couleurs du thème
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "danger": "#d62728",
    "warning": "#ff9800",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40",
}

# Configuration des graphiques
CHART_CONFIG = {
    "height": 400,
    "template": "plotly_white",
    "font_family": "Arial",
    "font_size": 12,
}

# Messages d'aide
HELP_MESSAGES = {
    "roi": "Le ROI mesure la rentabilité d'un investissement en pourcentage.",
    "roas": "Le ROAS indique combien de revenus vous générez pour chaque euro dépensé.",
    "cpc": "Le CPC représente le coût moyen par clic sur vos annonces.",
    "cpm": "Le CPM est le coût pour 1000 impressions de votre annonce.",
    "cpa": "Le CPA est le coût pour acquérir un nouveau client.",
    "ctr": "Le CTR est le pourcentage de personnes qui cliquent après avoir vu votre annonce.",
    "conversion_rate": "Le taux de conversion est le pourcentage de visiteurs qui réalisent l'action souhaitée.",
}


# ============================================================================
# EXPORT ET RAPPORTS
# ============================================================================

# Templates de rapport
REPORT_SECTIONS: List[str] = [
    "Résumé Exécutif",
    "Métriques Principales",
    "Analyse de Performance",
    "Recommandations",
    "Détails Techniques",
]

# Format d'export
EXPORT_FORMATS = ["PDF", "CSV", "JSON"]

# Configuration PDF
PDF_CONFIG = {
    "format": "A4",
    "orientation": "Portrait",
    "unit": "mm",
    "font_family": "Arial",
    "title_size": 16,
    "heading_size": 12,
    "body_size": 10,
}