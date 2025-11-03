"""
Tests unitaires pour src/utils.py
"""
import pytest
from datetime import datetime
from src.utils import (
    DataValidator,
    NumberFormatter,
    DateTimeHelper,
    FileHelper,
    ValidationError,
    format_currency,
    format_percentage,
    format_number,
)


class TestDataValidator:
    """Tests pour la classe DataValidator"""
    
    def test_validate_positive_number_valid(self):
        """Test validation nombre positif valide"""
        validator = DataValidator()
        assert validator.validate_positive_number(10, "test") == 10
        assert validator.validate_positive_number(10.5, "test") == 10.5
    
    def test_validate_positive_number_zero_allowed(self):
        """Test validation avec zéro autorisé"""
        validator = DataValidator()
        assert validator.validate_positive_number(0, "test", allow_zero=True) == 0
    
    def test_validate_positive_number_zero_not_allowed(self):
        """Test validation avec zéro non autorisé"""
        validator = DataValidator()
        with pytest.raises(ValidationError):
            validator.validate_positive_number(0, "test", allow_zero=False)
    
    def test_validate_positive_number_negative(self):
        """Test validation nombre négatif"""
        validator = DataValidator()
        with pytest.raises(ValidationError, match="ne peut pas être négatif"):
            validator.validate_positive_number(-10, "test", allow_zero=True)
    
    def test_validate_positive_number_invalid_type(self):
        """Test validation type invalide"""
        validator = DataValidator()
        with pytest.raises(ValidationError, match="doit être un nombre"):
            validator.validate_positive_number("10", "test")
    
    def test_validate_percentage_valid(self):
        """Test validation pourcentage valide"""
        validator = DataValidator()
        assert validator.validate_percentage(50.0, "test") == 50.0
        assert validator.validate_percentage(0, "test") == 0.0
        assert validator.validate_percentage(100, "test") == 100.0
    
    def test_validate_percentage_out_of_range(self):
        """Test validation pourcentage hors limites"""
        validator = DataValidator()
        with pytest.raises(ValidationError, match="entre 0 et 100"):
            validator.validate_percentage(101, "test")
        with pytest.raises(ValidationError, match="entre 0 et 100"):
            validator.validate_percentage(-1, "test")
    
    def test_validate_budget_valid(self):
        """Test validation budget valide"""
        validator = DataValidator()
        assert validator.validate_budget(1000.0) == 1000.0
        assert validator.validate_budget(0) == 0.0
    
    def test_validate_budget_negative(self):
        """Test validation budget négatif"""
        validator = DataValidator()
        with pytest.raises(ValidationError, match="ne peut pas être négatif"):
            validator.validate_budget(-100)
    
    def test_validate_budget_exceeds_max(self):
        """Test validation budget dépassant le maximum"""
        validator = DataValidator()
        with pytest.raises(ValidationError, match="ne peut pas dépasser"):
            validator.validate_budget(11_000_000, max_budget=10_000_000)
    
    def test_validate_metrics_data_valid(self):
        """Test validation données métriques valides"""
        validator = DataValidator()
        data = {
            "cost": 1000.0,
            "revenue": 1500.0,
            "impressions": 10000,
            "clicks": 500,
            "conversions": 50,
        }
        result = validator.validate_metrics_data(data)
        assert result["cost"] == 1000.0
        assert result["conversions"] == 50
    
    def test_validate_metrics_data_missing_field(self):
        """Test validation données avec champ manquant"""
        validator = DataValidator()
        data = {"cost": 1000.0}
        with pytest.raises(ValidationError, match="est requis"):
            validator.validate_metrics_data(data)
    
    def test_validate_metrics_data_clicks_exceed_impressions(self):
        """Test validation clics dépassant impressions"""
        validator = DataValidator()
        data = {
            "cost": 1000.0,
            "revenue": 1500.0,
            "impressions": 100,
            "clicks": 200,
        }
        with pytest.raises(ValidationError, match="ne peut pas dépasser"):
            validator.validate_metrics_data(data)
    
    def test_validate_metrics_data_conversions_exceed_clicks(self):
        """Test validation conversions dépassant clics"""
        validator = DataValidator()
        data = {
            "cost": 1000.0,
            "revenue": 1500.0,
            "clicks": 50,
            "conversions": 100,
        }
        with pytest.raises(ValidationError, match="ne peut pas dépasser"):
            validator.validate_metrics_data(data)


class TestNumberFormatter:
    """Tests pour la classe NumberFormatter"""
    
    def test_format_currency_basic(self):
        """Test formatage devise basique"""
        formatter = NumberFormatter()
        assert formatter.format_currency(1234.56) == "1 234,56 €"
        assert formatter.format_currency(1000) == "1 000,00 €"
    
    def test_format_currency_custom_currency(self):
        """Test formatage avec devise personnalisée"""
        formatter = NumberFormatter()
        assert formatter.format_currency(1234.56, currency="$") == "1 234,56 $"
    
    def test_format_currency_decimals(self):
        """Test formatage avec nombre de décimales"""
        formatter = NumberFormatter()
        assert formatter.format_currency(1234.567, decimals=0) == "1 235 €"
        assert formatter.format_currency(1234.567, decimals=3) == "1 234,567 €"
    
    def test_format_percentage_positive(self):
        """Test formatage pourcentage positif"""
        formatter = NumberFormatter()
        assert formatter.format_percentage(15.5) == "+15,50 %"
        assert formatter.format_percentage(15.5, include_sign=False) == "15,50 %"
    
    def test_format_percentage_negative(self):
        """Test formatage pourcentage négatif"""
        formatter = NumberFormatter()
        assert formatter.format_percentage(-5.25) == "-5,25 %"
    
    def test_format_percentage_zero(self):
        """Test formatage pourcentage zéro"""
        formatter = NumberFormatter()
        assert formatter.format_percentage(0) == "0,00 %"
    
    def test_format_number_integer(self):
        """Test formatage nombre entier"""
        formatter = NumberFormatter()
        assert formatter.format_number(1234567) == "1 234 567"
    
    def test_format_number_float(self):
        """Test formatage nombre décimal"""
        formatter = NumberFormatter()
        assert formatter.format_number(1234.56, decimals=2) == "1 234,56"
    
    def test_format_number_compact(self):
        """Test formatage compact"""
        formatter = NumberFormatter()
        assert formatter.format_number(1500, compact=True) == "1.5K"
        assert formatter.format_number(1500000, compact=True) == "1.5M"
        assert formatter.format_number(1500000000, compact=True) == "1.5B"
        assert formatter.format_number(500, compact=True) == "500"
    
    def test_format_metric_roi(self):
        """Test formatage métrique ROI"""
        formatter = NumberFormatter()
        assert formatter.format_metric(25.5, "roi") == "+25,50 %"
    
    def test_format_metric_cpc(self):
        """Test formatage métrique CPC"""
        formatter = NumberFormatter()
        assert formatter.format_metric(2.50, "cpc") == "2,50 €"
    
    def test_format_metric_unknown(self):
        """Test formatage métrique inconnue"""
        formatter = NumberFormatter()
        result = formatter.format_metric(1234, "unknown")
        assert "1234" in result or "1 234" in result


class TestDateTimeHelper:
    """Tests pour la classe DateTimeHelper"""
    
    def test_get_timestamp(self):
        """Test génération timestamp"""
        helper = DateTimeHelper()
        timestamp = helper.get_timestamp()
        assert isinstance(timestamp, str)
        assert "T" in timestamp  # Format ISO
    
    def test_format_datetime(self):
        """Test formatage date/heure"""
        helper = DateTimeHelper()
        dt = datetime(2024, 3, 15, 14, 30)
        formatted = helper.format_datetime(dt)
        assert formatted == "15/03/2024 14:30"
    
    def test_format_datetime_custom_format(self):
        """Test formatage avec format personnalisé"""
        helper = DateTimeHelper()
        dt = datetime(2024, 3, 15)
        formatted = helper.format_datetime(dt, format_str="%Y-%m-%d")
        assert formatted == "2024-03-15"
    
    def test_get_date_range_label(self):
        """Test labels de périodes"""
        helper = DateTimeHelper()
        assert helper.get_date_range_label(1) == "Aujourd'hui"
        assert helper.get_date_range_label(7) == "7 derniers jours"
        assert helper.get_date_range_label(30) == "30 derniers jours"
        assert helper.get_date_range_label(90) == "3 derniers mois"
        assert helper.get_date_range_label(45) == "45 derniers jours"


class TestFileHelper:
    """Tests pour la classe FileHelper"""
    
    def test_sanitize_filename_basic(self):
        """Test nettoyage nom de fichier basique"""
        helper = FileHelper()
        assert helper.sanitize_filename("test.pdf") == "test.pdf"
    
    def test_sanitize_filename_invalid_chars(self):
        """Test nettoyage caractères invalides"""
        helper = FileHelper()
        result = helper.sanitize_filename("test<>:|?.pdf")
        assert "<" not in result
        assert ">" not in result
        assert ":" not in result
    
    def test_sanitize_filename_long(self):
        """Test nettoyage nom de fichier long"""
        helper = FileHelper()
        long_name = "a" * 250 + ".pdf"
        result = helper.sanitize_filename(long_name)
        assert len(result) <= 200
    
    def test_generate_export_filename_with_timestamp(self):
        """Test génération nom de fichier avec timestamp"""
        helper = FileHelper()
        filename = helper.generate_export_filename("report", "pdf", include_timestamp=True)
        assert filename.startswith("report_")
        assert filename.endswith(".pdf")
        assert len(filename) > len("report_.pdf")
    
    def test_generate_export_filename_without_timestamp(self):
        """Test génération nom de fichier sans timestamp"""
        helper = FileHelper()
        filename = helper.generate_export_filename("report", "pdf", include_timestamp=False)
        assert filename == "report.pdf"


class TestHelperFunctions:
    """Tests pour les fonctions helper globales"""
    
    def test_format_currency_shortcut(self):
        """Test fonction raccourci format_currency"""
        result = format_currency(1234.56)
        assert "1 234" in result or "1234" in result
        assert "€" in result
    
    def test_format_percentage_shortcut(self):
        """Test fonction raccourci format_percentage"""
        result = format_percentage(25.5)
        assert "25" in result
        assert "%" in result
    
    def test_format_number_shortcut(self):
        """Test fonction raccourci format_number"""
        result = format_number(1234567)
        assert "1234567" in result or "1 234 567" in result


# Configuration pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.utils", "--cov-report=html"])