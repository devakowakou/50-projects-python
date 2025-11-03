"""
ROI Marketing Calculator - Package principal
"""

__version__ = "1.0.0"
__author__ = "Votre Nom"

# Imports principaux pour faciliter l'utilisation
from src.calculator import ROICalculator, CampaignMetrics
from src.utils import (
    DataValidator,
    NumberFormatter,
    ValidationError,
    format_currency,
    format_percentage,
    format_number,
)

__all__ = [
    "ROICalculator",
    "CampaignMetrics",
    "DataValidator",
    "NumberFormatter",
    "ValidationError",
    "format_currency",
    "format_percentage",
    "format_number",
]