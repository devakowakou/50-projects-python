"""
Calculateur de métriques marketing et ROI
"""
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field
from src.utils import DataValidator, ValidationError


@dataclass
class CampaignMetrics:
    """Classe pour stocker les métriques d'une campagne"""
    
    # Coûts et revenus
    cost: float = 0.0
    revenue: float = 0.0
    
    # Métriques d'engagement
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    leads: int = 0
    
    # Métriques calculées
    roi: Optional[float] = None
    roas: Optional[float] = None
    cpc: Optional[float] = None
    cpm: Optional[float] = None
    cpa: Optional[float] = None
    cpl: Optional[float] = None
    ctr: Optional[float] = None
    conversion_rate: Optional[float] = None
    
    # Métadonnées
    campaign_name: str = ""
    industry: str = ""
    notes: str = ""
    
    def __post_init__(self):
        """Validation après initialisation"""
        self._validate()
    
    def _validate(self):
        """Valide les données de la campagne"""
        validator = DataValidator()
        
        # Validation des nombres positifs
        self.cost = validator.validate_positive_number(
            self.cost, "Coût", allow_zero=True
        )
        self.revenue = validator.validate_positive_number(
            self.revenue, "Revenu", allow_zero=True
        )
        
        # Validation des entiers
        if self.impressions < 0:
            raise ValidationError("Les impressions ne peuvent pas être négatives")
        if self.clicks < 0:
            raise ValidationError("Les clics ne peuvent pas être négatifs")
        if self.conversions < 0:
            raise ValidationError("Les conversions ne peuvent pas être négatives")
        
        # Validation de cohérence
        if self.clicks > self.impressions and self.impressions > 0:
            raise ValidationError(
                "Les clics ne peuvent pas dépasser les impressions"
            )
        if self.conversions > self.clicks and self.clicks > 0:
            raise ValidationError(
                "Les conversions ne peuvent pas dépasser les clics"
            )


class ROICalculator:
    """Calculateur de ROI et métriques marketing"""
    
    def __init__(self):
        self.validator = DataValidator()
    
    def calculate_roi(self, revenue: float, cost: float) -> float:
        """
        Calcule le Return on Investment (ROI)
        
        ROI = (Revenu - Coût) / Coût × 100
        
        Args:
            revenue: Revenu généré par la campagne
            cost: Coût total de la campagne
            
        Returns:
            ROI en pourcentage
            
        Examples:
            >>> calc = ROICalculator()
            >>> calc.calculate_roi(15000, 10000)
            50.0
        """
        revenue = self.validator.validate_positive_number(
            revenue, "Revenu", allow_zero=True
        )
        cost = self.validator.validate_positive_number(
            cost, "Coût", allow_zero=True
        )
        
        if cost == 0:
            return 0.0
        
        return ((revenue - cost) / cost) * 100
    
    def calculate_roas(self, revenue: float, cost: float) -> float:
        """
        Calcule le Return on Ad Spend (ROAS)
        
        ROAS = Revenu / Coût
        
        Args:
            revenue: Revenu généré
            cost: Coût publicitaire
            
        Returns:
            ROAS (ratio)
            
        Examples:
            >>> calc = ROICalculator()
            >>> calc.calculate_roas(15000, 10000)
            1.5
        """
        revenue = self.validator.validate_positive_number(
            revenue, "Revenu", allow_zero=True
        )
        cost = self.validator.validate_positive_number(
            cost, "Coût", allow_zero=True
        )
        
        if cost == 0:
            return 0.0
        
        return revenue / cost
    
    def calculate_cpc(self, total_cost: float, clicks: int) -> float:
        """
        Calcule le Cost Per Click (CPC)
        
        CPC = Coût Total / Nombre de Clics
        
        Args:
            total_cost: Coût total de la campagne
            clicks: Nombre de clics
            
        Returns:
            CPC en devise
            
        Examples:
            >>> calc = ROICalculator()
            >>> calc.calculate_cpc(1000, 500)
            2.0
        """
        total_cost = self.validator.validate_positive_number(
            total_cost, "Coût total", allow_zero=True
        )
        clicks = int(self.validator.validate_positive_number(
            clicks, "Clics", allow_zero=True
        ))
        
        if clicks == 0:
            return 0.0
        
        return total_cost / clicks
    
    def calculate_cpm(self, total_cost: float, impressions: int) -> float:
        """
        Calcule le Cost Per Mille (CPM)
        
        CPM = (Coût Total / Impressions) × 1000
        
        Args:
            total_cost: Coût total de la campagne
            impressions: Nombre d'impressions
            
        Returns:
            CPM pour 1000 impressions
            
        Examples:
            >>> calc = ROICalculator()
            >>> calc.calculate_cpm(1000, 100000)
            10.0
        """
        total_cost = self.validator.validate_positive_number(
            total_cost, "Coût total", allow_zero=True
        )
        impressions = int(self.validator.validate_positive_number(
            impressions, "Impressions", allow_zero=False
        ))
        
        if impressions == 0:
            return 0.0
        
        return (total_cost / impressions) * 1000
    
    def calculate_cpa(self, total_cost: float, conversions: int) -> float:
        """
        Calcule le Cost Per Acquisition (CPA)
        
        CPA = Coût Total / Conversions
        
        Args:
            total_cost: Coût total de la campagne
            conversions: Nombre de conversions
            
        Returns:
            CPA en devise
            
        Examples:
            >>> calc = ROICalculator()
            >>> calc.calculate_cpa(1000, 50)
            20.0
        """
        total_cost = self.validator.validate_positive_number(
            total_cost, "Coût total", allow_zero=True
        )
        conversions = int(self.validator.validate_positive_number(
            conversions, "Conversions", allow_zero=True
        ))
        
        if conversions == 0:
            return 0.0
        
        return total_cost / conversions
    
    def calculate_cpl(self, total_cost: float, leads: int) -> float:
        """
        Calcule le Cost Per Lead (CPL)
        
        CPL = Coût Total / Leads
        
        Args:
            total_cost: Coût total de la campagne
            leads: Nombre de leads générés
            
        Returns:
            CPL en devise
        """
        total_cost = self.validator.validate_positive_number(
            total_cost, "Coût total", allow_zero=True
        )
        leads = int(self.validator.validate_positive_number(
            leads, "Leads", allow_zero=True
        ))
        
        if leads == 0:
            return 0.0
        
        return total_cost / leads
    
    def calculate_ctr(self, clicks: int, impressions: int) -> float:
        """
        Calcule le Click Through Rate (CTR)
        
        CTR = (Clics / Impressions) × 100
        
        Args:
            clicks: Nombre de clics
            impressions: Nombre d'impressions
            
        Returns:
            CTR en pourcentage
            
        Examples:
            >>> calc = ROICalculator()
            >>> calc.calculate_ctr(2000, 100000)
            2.0
        """
        clicks = int(self.validator.validate_positive_number(
            clicks, "Clics", allow_zero=True
        ))
        impressions = int(self.validator.validate_positive_number(
            impressions, "Impressions", allow_zero=False
        ))
        
        if impressions == 0:
            return 0.0
        
        return (clicks / impressions) * 100
    
    def calculate_conversion_rate(self, conversions: int, clicks: int) -> float:
        """
        Calcule le taux de conversion
        
        Taux de Conversion = (Conversions / Clics) × 100
        
        Args:
            conversions: Nombre de conversions
            clicks: Nombre de clics
            
        Returns:
            Taux de conversion en pourcentage
            
        Examples:
            >>> calc = ROICalculator()
            >>> calc.calculate_conversion_rate(100, 2000)
            5.0
        """
        conversions = int(self.validator.validate_positive_number(
            conversions, "Conversions", allow_zero=True
        ))
        clicks = int(self.validator.validate_positive_number(
            clicks, "Clics", allow_zero=True
        ))
        
        if clicks == 0:
            return 0.0
        
        return (conversions / clicks) * 100
    
    def calculate_breakeven(
        self,
        fixed_costs: float,
        price_per_unit: float,
        variable_cost_per_unit: float
    ) -> float:
        """
        Calcule le seuil de rentabilité (breakeven point)
        
        Seuil = Coûts Fixes / (Prix Unitaire - Coût Variable Unitaire)
        
        Args:
            fixed_costs: Coûts fixes
            price_per_unit: Prix de vente unitaire
            variable_cost_per_unit: Coût variable unitaire
            
        Returns:
            Nombre d'unités à vendre pour atteindre le seuil
            
        Examples:
            >>> calc = ROICalculator()
            >>> calc.calculate_breakeven(10000, 100, 40)
            166.67
        """
        fixed_costs = self.validator.validate_positive_number(
            fixed_costs, "Coûts fixes", allow_zero=True
        )
        price_per_unit = self.validator.validate_positive_number(
            price_per_unit, "Prix unitaire", allow_zero=False
        )
        variable_cost_per_unit = self.validator.validate_positive_number(
            variable_cost_per_unit, "Coût variable unitaire", allow_zero=True
        )
        
        margin = price_per_unit - variable_cost_per_unit
        
        if margin <= 0:
            raise ValidationError(
                "Le prix unitaire doit être supérieur au coût variable"
            )
        
        return fixed_costs / margin
    
    def calculate_all_metrics(self, metrics: CampaignMetrics) -> CampaignMetrics:
        """
        Calcule toutes les métriques possibles pour une campagne
        
        Args:
            metrics: Objet CampaignMetrics avec les données de base
            
        Returns:
            CampaignMetrics mis à jour avec toutes les métriques calculées
        """
        # ROI et ROAS
        if metrics.cost > 0:
            metrics.roi = self.calculate_roi(metrics.revenue, metrics.cost)
            metrics.roas = self.calculate_roas(metrics.revenue, metrics.cost)
        
        # Métriques basées sur les impressions
        if metrics.impressions > 0:
            if metrics.cost > 0:
                metrics.cpm = self.calculate_cpm(metrics.cost, metrics.impressions)
            if metrics.clicks > 0:
                metrics.ctr = self.calculate_ctr(metrics.clicks, metrics.impressions)
        
        # Métriques basées sur les clics
        if metrics.clicks > 0:
            if metrics.cost > 0:
                metrics.cpc = self.calculate_cpc(metrics.cost, metrics.clicks)
            if metrics.conversions > 0:
                metrics.conversion_rate = self.calculate_conversion_rate(
                    metrics.conversions, metrics.clicks
                )
        
        # Métriques basées sur les conversions
        if metrics.conversions > 0 and metrics.cost > 0:
            metrics.cpa = self.calculate_cpa(metrics.cost, metrics.conversions)
        
        # CPL si des leads sont disponibles
        if metrics.leads > 0 and metrics.cost > 0:
            metrics.cpl = self.calculate_cpl(metrics.cost, metrics.leads)
        
        return metrics
    
    def get_metrics_summary(self, metrics: CampaignMetrics) -> Dict[str, any]:
        """
        Génère un résumé des métriques avec formatage
        
        Args:
            metrics: Métriques de la campagne
            
        Returns:
            Dictionnaire avec résumé formaté
        """
        from src.utils import format_currency, format_percentage, format_number
        
        summary = {
            "Coût Total": format_currency(metrics.cost),
            "Revenu Total": format_currency(metrics.revenue),
            "Profit": format_currency(metrics.revenue - metrics.cost),
        }
        
        if metrics.roi is not None:
            summary["ROI"] = format_percentage(metrics.roi)
        
        if metrics.roas is not None:
            summary["ROAS"] = f"{metrics.roas:.2f}x"
        
        if metrics.cpc is not None:
            summary["CPC"] = format_currency(metrics.cpc)
        
        if metrics.cpm is not None:
            summary["CPM"] = format_currency(metrics.cpm)
        
        if metrics.cpa is not None:
            summary["CPA"] = format_currency(metrics.cpa)
        
        if metrics.ctr is not None:
            summary["CTR"] = format_percentage(metrics.ctr)
        
        if metrics.conversion_rate is not None:
            summary["Taux de Conversion"] = format_percentage(metrics.conversion_rate)
        
        # Données de volume
        if metrics.impressions > 0:
            summary["Impressions"] = format_number(metrics.impressions)
        if metrics.clicks > 0:
            summary["Clics"] = format_number(metrics.clicks)
        if metrics.conversions > 0:
            summary["Conversions"] = format_number(metrics.conversions)
        
        return summary