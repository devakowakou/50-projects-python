"""
Tests unitaires pour src/calculator.py
"""
import pytest
from src.calculator import ROICalculator, CampaignMetrics
from src.utils import ValidationError


class TestCampaignMetrics:
    """Tests pour la classe CampaignMetrics"""
    
    def test_campaign_metrics_creation_valid(self):
        """Test création métriques valides"""
        metrics = CampaignMetrics(
            cost=1000.0,
            revenue=1500.0,
            impressions=10000,
            clicks=500,
            conversions=50
        )
        assert metrics.cost == 1000.0
        assert metrics.revenue == 1500.0
        assert metrics.impressions == 10000
        assert metrics.clicks == 500
        assert metrics.conversions == 50
    
    def test_campaign_metrics_default_values(self):
        """Test valeurs par défaut"""
        metrics = CampaignMetrics()
        assert metrics.cost == 0.0
        assert metrics.revenue == 0.0
        assert metrics.impressions == 0
        assert metrics.roi is None
    
    def test_campaign_metrics_validation_negative_cost(self):
        """Test validation coût négatif"""
        with pytest.raises(ValidationError):
            CampaignMetrics(cost=-100)
    
    def test_campaign_metrics_validation_clicks_exceed_impressions(self):
        """Test validation clics > impressions"""
        with pytest.raises(ValidationError, match="ne peuvent pas dépasser"):
            CampaignMetrics(impressions=100, clicks=200)
    
    def test_campaign_metrics_validation_conversions_exceed_clicks(self):
        """Test validation conversions > clics"""
        with pytest.raises(ValidationError, match="ne peuvent pas dépasser"):
            CampaignMetrics(clicks=50, conversions=100)
    
    def test_campaign_metrics_with_metadata(self):
        """Test création avec métadonnées"""
        metrics = CampaignMetrics(
            cost=1000.0,
            revenue=1500.0,
            campaign_name="Summer Campaign",
            industry="E-commerce",
            notes="Test campaign"
        )
        assert metrics.campaign_name == "Summer Campaign"
        assert metrics.industry == "E-commerce"
        assert metrics.notes == "Test campaign"


class TestROICalculator:
    """Tests pour la classe ROICalculator"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.calculator = ROICalculator()
    
    # Tests calculate_roi
    def test_calculate_roi_positive(self):
        """Test calcul ROI positif"""
        roi = self.calculator.calculate_roi(revenue=1500, cost=1000)
        assert roi == 50.0
    
    def test_calculate_roi_negative(self):
        """Test calcul ROI négatif"""
        roi = self.calculator.calculate_roi(revenue=800, cost=1000)
        assert roi == -20.0
    
    def test_calculate_roi_zero_cost(self):
        """Test calcul ROI avec coût zéro"""
        roi = self.calculator.calculate_roi(revenue=1500, cost=0)
        assert roi == 0.0
    
    def test_calculate_roi_breakeven(self):
        """Test calcul ROI au point d'équilibre"""
        roi = self.calculator.calculate_roi(revenue=1000, cost=1000)
        assert roi == 0.0
    
    def test_calculate_roi_invalid_cost(self):
        """Test calcul ROI avec coût invalide"""
        with pytest.raises(ValidationError):
            self.calculator.calculate_roi(revenue=1500, cost=-100)
    
    # Tests calculate_roas
    def test_calculate_roas_basic(self):
        """Test calcul ROAS basique"""
        roas = self.calculator.calculate_roas(revenue=3000, cost=1000)
        assert roas == 3.0
    
    def test_calculate_roas_less_than_one(self):
        """Test calcul ROAS < 1"""
        roas = self.calculator.calculate_roas(revenue=500, cost=1000)
        assert roas == 0.5
    
    def test_calculate_roas_zero_cost(self):
        """Test calcul ROAS avec coût zéro"""
        roas = self.calculator.calculate_roas(revenue=1000, cost=0)
        assert roas == 0.0
    
    # Tests calculate_cpc
    def test_calculate_cpc_basic(self):
        """Test calcul CPC basique"""
        cpc = self.calculator.calculate_cpc(total_cost=1000, clicks=500)
        assert cpc == 2.0
    
    def test_calculate_cpc_zero_clicks(self):
        """Test calcul CPC avec zéro clics"""
        cpc = self.calculator.calculate_cpc(total_cost=1000, clicks=0)
        assert cpc == 0.0
    
    def test_calculate_cpc_high_value(self):
        """Test calcul CPC avec valeur élevée"""
        cpc = self.calculator.calculate_cpc(total_cost=10000, clicks=100)
        assert cpc == 100.0
    
    # Tests calculate_cpm
    def test_calculate_cpm_basic(self):
        """Test calcul CPM basique"""
        cpm = self.calculator.calculate_cpm(total_cost=1000, impressions=100000)
        assert cpm == 10.0
    
    def test_calculate_cpm_high_impressions(self):
        """Test calcul CPM avec beaucoup d'impressions"""
        cpm = self.calculator.calculate_cpm(total_cost=500, impressions=1000000)
        assert cpm == 0.5
    
    def test_calculate_cpm_zero_impressions(self):
        """Test calcul CPM avec zéro impressions"""
        cpm = self.calculator.calculate_cpm(total_cost=1000, impressions=0)
        assert cpm == 0.0
    
    # Tests calculate_cpa
    def test_calculate_cpa_basic(self):
        """Test calcul CPA basique"""
        cpa = self.calculator.calculate_cpa(total_cost=1000, conversions=50)
        assert cpa == 20.0
    
    def test_calculate_cpa_zero_conversions(self):
        """Test calcul CPA avec zéro conversions"""
        cpa = self.calculator.calculate_cpa(total_cost=1000, conversions=0)
        assert cpa == 0.0
    
    def test_calculate_cpa_high_cost(self):
        """Test calcul CPA avec coût élevé"""
        cpa = self.calculator.calculate_cpa(total_cost=10000, conversions=10)
        assert cpa == 1000.0
    
    # Tests calculate_cpl
    def test_calculate_cpl_basic(self):
        """Test calcul CPL basique"""
        cpl = self.calculator.calculate_cpl(total_cost=1000, leads=100)
        assert cpl == 10.0
    
    def test_calculate_cpl_zero_leads(self):
        """Test calcul CPL avec zéro leads"""
        cpl = self.calculator.calculate_cpl(total_cost=1000, leads=0)
        assert cpl == 0.0
    
    # Tests calculate_ctr
    def test_calculate_ctr_basic(self):
        """Test calcul CTR basique"""
        ctr = self.calculator.calculate_ctr(clicks=2000, impressions=100000)
        assert ctr == 2.0
    
    def test_calculate_ctr_high_rate(self):
        """Test calcul CTR élevé"""
        ctr = self.calculator.calculate_ctr(clicks=5000, impressions=100000)
        assert ctr == 5.0
    
    def test_calculate_ctr_low_rate(self):
        """Test calcul CTR faible"""
        ctr = self.calculator.calculate_ctr(clicks=500, impressions=100000)
        assert ctr == 0.5
    
    def test_calculate_ctr_zero_impressions(self):
        """Test calcul CTR avec zéro impressions"""
        ctr = self.calculator.calculate_ctr(clicks=100, impressions=0)
        assert ctr == 0.0
    
    # Tests calculate_conversion_rate
    def test_calculate_conversion_rate_basic(self):
        """Test calcul taux de conversion basique"""
        rate = self.calculator.calculate_conversion_rate(conversions=100, clicks=2000)
        assert rate == 5.0
    
    def test_calculate_conversion_rate_high(self):
        """Test calcul taux de conversion élevé"""
        rate = self.calculator.calculate_conversion_rate(conversions=200, clicks=1000)
        assert rate == 20.0
    
    def test_calculate_conversion_rate_zero_clicks(self):
        """Test calcul taux de conversion avec zéro clics"""
        rate = self.calculator.calculate_conversion_rate(conversions=100, clicks=0)
        assert rate == 0.0
    
    # Tests calculate_breakeven
    def test_calculate_breakeven_basic(self):
        """Test calcul seuil de rentabilité basique"""
        breakeven = self.calculator.calculate_breakeven(
            fixed_costs=10000,
            price_per_unit=100,
            variable_cost_per_unit=40
        )
        assert pytest.approx(breakeven, rel=0.01) == 166.67
    
    def test_calculate_breakeven_high_margin(self):
        """Test seuil de rentabilité avec marge élevée"""
        breakeven = self.calculator.calculate_breakeven(
            fixed_costs=5000,
            price_per_unit=100,
            variable_cost_per_unit=20
        )
        assert pytest.approx(breakeven, rel=0.01) == 62.5
    
    def test_calculate_breakeven_invalid_margin(self):
        """Test seuil de rentabilité avec marge invalide"""
        with pytest.raises(ValidationError, match="supérieur au coût variable"):
            self.calculator.calculate_breakeven(
                fixed_costs=10000,
                price_per_unit=50,
                variable_cost_per_unit=60
            )
    
    def test_calculate_breakeven_zero_margin(self):
        """Test seuil de rentabilité avec marge zéro"""
        with pytest.raises(ValidationError):
            self.calculator.calculate_breakeven(
                fixed_costs=10000,
                price_per_unit=50,
                variable_cost_per_unit=50
            )
    
    # Tests calculate_all_metrics
    def test_calculate_all_metrics_complete(self):
        """Test calcul de toutes les métriques avec données complètes"""
        metrics = CampaignMetrics(
            cost=1000.0,
            revenue=1500.0,
            impressions=100000,
            clicks=2000,
            conversions=100
        )
        
        result = self.calculator.calculate_all_metrics(metrics)
        
        assert result.roi == 50.0
        assert result.roas == 1.5
        assert result.cpc == 0.5
        assert result.cpm == 10.0
        assert result.cpa == 10.0
        assert result.ctr == 2.0
        assert result.conversion_rate == 5.0
    
    def test_calculate_all_metrics_partial(self):
        """Test calcul métriques avec données partielles"""
        metrics = CampaignMetrics(
            cost=1000.0,
            revenue=1500.0,
            impressions=100000
        )
        
        result = self.calculator.calculate_all_metrics(metrics)
        
        assert result.roi == 50.0
        assert result.roas == 1.5
        assert result.cpm == 10.0
        assert result.cpc is None  # Pas de clics
        assert result.ctr is None
    
    def test_calculate_all_metrics_with_leads(self):
        """Test calcul métriques avec leads"""
        metrics = CampaignMetrics(
            cost=1000.0,
            revenue=1500.0,
            leads=200
        )
        
        result = self.calculator.calculate_all_metrics(metrics)
        
        assert result.roi == 50.0
        assert result.cpl == 5.0
    
    # Tests get_metrics_summary
    def test_get_metrics_summary(self):
        """Test génération résumé des métriques"""
        metrics = CampaignMetrics(
            cost=1000.0,
            revenue=1500.0,
            impressions=100000,
            clicks=2000,
            conversions=100
        )
        
        metrics = self.calculator.calculate_all_metrics(metrics)
        summary = self.calculator.get_metrics_summary(metrics)
        
        assert "Coût Total" in summary
        assert "Revenu Total" in summary
        assert "ROI" in summary
        assert "CPC" in summary
        assert "€" in summary["Coût Total"]
    
    def test_get_metrics_summary_partial(self):
        """Test résumé avec données partielles"""
        metrics = CampaignMetrics(
            cost=500.0,
            revenue=1000.0
        )
        
        metrics = self.calculator.calculate_all_metrics(metrics)
        summary = self.calculator.get_metrics_summary(metrics)
        
        assert "Coût Total" in summary
        assert "ROI" in summary
        assert "CPC" not in summary  # Pas de données de clics


# Tests d'intégration
class TestIntegration:
    """Tests d'intégration pour le module calculator"""
    
    def test_complete_campaign_workflow(self):
        """Test workflow complet d'une campagne"""
        # Création d'une campagne
        campaign = CampaignMetrics(
            cost=5000.0,
            revenue=8000.0,
            impressions=500000,
            clicks=10000,
            conversions=500,
            campaign_name="Summer Sale 2024",
            industry="E-commerce"
        )
        
        # Calcul de toutes les métriques
        calculator = ROICalculator()
        campaign = calculator.calculate_all_metrics(campaign)
        
        # Vérifications
        assert campaign.roi == 60.0
        assert campaign.roas == 1.6
        assert campaign.cpc == 0.5
        assert campaign.cpm == 10.0
        assert campaign.cpa == 10.0
        assert campaign.ctr == 2.0
        assert campaign.conversion_rate == 5.0
        
        # Génération du résumé
        summary = calculator.get_metrics_summary(campaign)
        assert len(summary) > 5
    
    def test_low_performance_campaign(self):
        """Test campagne avec faible performance"""
        campaign = CampaignMetrics(
            cost=10000.0,
            revenue=8000.0,
            impressions=1000000,
            clicks=5000,
            conversions=100
        )
        
        calculator = ROICalculator()
        campaign = calculator.calculate_all_metrics(campaign)
        
        # ROI négatif
        assert campaign.roi == -20.0
        assert campaign.roas < 1.0
        assert campaign.ctr == 0.5
        assert campaign.conversion_rate == 2.0


# Configuration pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.calculator", "--cov-report=html"])