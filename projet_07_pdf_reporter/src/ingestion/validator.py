"""
Module de validation des données - VERSION FLEXIBLE
"""
import pandas as pd
from typing import List, Dict, Tuple
from src.utils.logger import setup_logger
from src.utils.constants import ERROR_MESSAGES

logger = setup_logger(__name__)

class DataValidator:
    """Classe pour valider les données Excel de manière flexible"""
    
    def __init__(self, template_type: str = "auto"):
        self.template_type = template_type
        self.errors = []
        self.warnings = []
    
    def validate(self, df: pd.DataFrame) -> Tuple[bool, List[str], List[str]]:
        """
        Valide un DataFrame de manière flexible
        
        Args:
            df: DataFrame à valider
        
        Returns:
            (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Validations basiques uniquement
        self._check_empty_data(df)
        self._check_minimum_data(df)
        self._check_missing_values_threshold(df)
        
        is_valid = len(self.errors) == 0
        
        if is_valid:
            logger.info("✅ Validation réussie")
        else:
            logger.warning(f"❌ Validation échouée: {len(self.errors)} erreur(s)")
        
        return is_valid, self.errors, self.warnings
    
    def _check_empty_data(self, df: pd.DataFrame):
        """Vérifie que le DataFrame n'est pas vide"""
        if df.empty:
            self.errors.append(ERROR_MESSAGES["empty_data"])
    
    def _check_minimum_data(self, df: pd.DataFrame):
        """Vérifie qu'il y a un minimum de données exploitables"""
        if len(df) < 2:
            self.errors.append("Fichier doit contenir au moins 2 lignes de données")
        
        if len(df.columns) < 2:
            self.errors.append("Fichier doit contenir au moins 2 colonnes")
    
    def _check_missing_values_threshold(self, df: pd.DataFrame):
        """Avertit si trop de valeurs manquantes dans certaines colonnes"""
        missing_counts = df.isnull().sum()
        total_rows = len(df)
        
        # Compter les colonnes complètement vides
        completely_empty = (missing_counts == total_rows).sum()
        
        if completely_empty > len(df.columns) * 0.5:
            self.warnings.append(
                f"⚠️ {completely_empty} colonnes sont complètement vides (peuvent être supprimées)"
            )
        
        # Avertir pour colonnes avec >50% de valeurs manquantes (mais pas 100%)
        for col, count in missing_counts.items():
            pct = (count / total_rows) * 100
            if 50 < pct < 100:
                self.warnings.append(
                    f"⚠️ Colonne '{col}': {pct:.1f}% de valeurs manquantes"
                )
    
    def detect_data_type(self, df: pd.DataFrame) -> str:
        """
        Détecte automatiquement le type de données
        
        Args:
            df: DataFrame
        
        Returns:
            Type détecté ('commercial', 'financier', 'technique', 'generic')
        """
        columns_lower = [col.lower() for col in df.columns]
        
        # Détection commercial
        commercial_keywords = ['prix', 'price', 'quantité', 'quantity', 'ca', 'vente', 'sales', 'produit', 'product']
        if any(kw in ' '.join(columns_lower) for kw in commercial_keywords):
            return "commercial"
        
        # Détection financier
        financial_keywords = ['debit', 'credit', 'solde', 'compte', 'balance', 'montant', 'amount']
        if any(kw in ' '.join(columns_lower) for kw in financial_keywords):
            return "financier"
        
        # Détection technique
        technical_keywords = ['métrique', 'metric', 'performance', 'latency', 'throughput', 'cpu', 'memory']
        if any(kw in ' '.join(columns_lower) for kw in technical_keywords):
            return "technique"
        
        return "generic"
    
    def get_validation_report(self) -> Dict:
        """
        Génère un rapport de validation
        
        Returns:
            Dictionnaire avec le rapport
        """
        return {
            "is_valid": len(self.errors) == 0,
            "errors_count": len(self.errors),
            "warnings_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings
        }