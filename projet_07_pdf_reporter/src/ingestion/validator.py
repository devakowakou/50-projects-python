"""
Validateur de données avec détection automatique du type
"""
import pandas as pd
from typing import Tuple, List
from config import VALIDATION_RULES

class DataValidator:
    """Validateur de données flexible"""
    
    def __init__(self, template_type: str = "auto"):
        self.template_type = template_type
        self.errors = []
        self.warnings = []
    
    def validate(self, df: pd.DataFrame) -> Tuple[bool, List[str], List[str]]:
        """
        Valide un DataFrame
        
        Args:
            df: DataFrame à valider
            
        Returns:
            Tuple (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Validation structure
        self._validate_structure(df)
        
        # Validation contenu
        self._validate_content(df)
        
        # Validation spécifique au type
        if self.template_type != "auto":
            self._validate_template_specific(df)
        
        is_valid = len(self.errors) == 0
        
        return is_valid, self.errors, self.warnings
    
    def detect_data_type(self, df: pd.DataFrame) -> str:
        """
        Détecte automatiquement le type de données
        
        Args:
            df: DataFrame à analyser
            
        Returns:
            Type détecté ('commercial', 'financier', 'ressources_humaines')
        """
        columns_lower = [col.lower() for col in df.columns]
        
        # Mots-clés pour chaque type
        commercial_keywords = ['vente', 'client', 'produit', 'chiffre', 'ca', 'commande']
        financier_keywords = ['revenu', 'depense', 'cout', 'benefice', 'tresorerie', 'budget']
        rh_keywords = ['employe', 'salaire', 'effectif', 'formation', 'conge', 'absence']
        
        # Comptage des correspondances
        scores = {
            'commercial': sum(any(kw in col for kw in commercial_keywords) for col in columns_lower),
            'financier': sum(any(kw in col for kw in financier_keywords) for col in columns_lower),
            'ressources_humaines': sum(any(kw in col for kw in rh_keywords) for col in columns_lower)
        }
        
        # Retourner le type avec le meilleur score
        detected = max(scores, key=scores.get)
        
        # Si aucun score > 0, retourner commercial par défaut
        return detected if scores[detected] > 0 else 'commercial'
    
    def _validate_structure(self, df: pd.DataFrame) -> None:
        """Valide la structure du DataFrame"""
        
        # Vérifier nombre de lignes
        if len(df) < VALIDATION_RULES["min_rows"]:
            self.errors.append(f"Nombre de lignes insuffisant (minimum {VALIDATION_RULES['min_rows']})")
        
        if len(df) > VALIDATION_RULES["max_rows"]:
            self.errors.append(f"Nombre de lignes trop élevé (maximum {VALIDATION_RULES['max_rows']})")
        
        # Vérifier colonnes
        if len(df.columns) == 0:
            self.errors.append("Aucune colonne trouvée")
        
        # Vérifier colonnes numériques
        numeric_cols = df.select_dtypes(include=['number']).columns
        numeric_ratio = len(numeric_cols) / len(df.columns) if len(df.columns) > 0 else 0
        
        if numeric_ratio < VALIDATION_RULES["required_numeric_ratio"]:
            self.warnings.append(
                f"Peu de colonnes numériques ({numeric_ratio:.1%}). "
                f"Minimum recommandé: {VALIDATION_RULES['required_numeric_ratio']:.1%}"
            )
    
    def _validate_content(self, df: pd.DataFrame) -> None:
        """Valide le contenu du DataFrame"""
        
        # Vérifier valeurs manquantes
        missing_ratio = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
        
        if missing_ratio > 0.5:
            self.warnings.append(f"Beaucoup de valeurs manquantes ({missing_ratio:.1%})")
        elif missing_ratio > 0.2:
            self.warnings.append(f"Valeurs manquantes: {missing_ratio:.1%}")
        
        # Vérifier doublons
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            self.warnings.append(f"{duplicates} ligne(s) dupliquée(s) détectée(s)")
    
    def _validate_template_specific(self, df: pd.DataFrame) -> None:
        """Validation spécifique selon le template"""
        
        if self.template_type == "commercial":
            self._validate_commercial(df)
        elif self.template_type == "financier":
            self._validate_financier(df)
        elif self.template_type == "ressources_humaines":
            self._validate_rh(df)
    
    def _validate_commercial(self, df: pd.DataFrame) -> None:
        """Validation pour données commerciales"""
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) == 0:
            self.warnings.append("Aucune colonne numérique pour l'analyse commerciale")
    
    def _validate_financier(self, df: pd.DataFrame) -> None:
        """Validation pour données financières"""
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) < 2:
            self.warnings.append("Au moins 2 colonnes numériques recommandées pour l'analyse financière")
    
    def _validate_rh(self, df: pd.DataFrame) -> None:
        """Validation pour données RH"""
        if len(df) < 10:
            self.warnings.append("Peu de données pour une analyse RH significative")