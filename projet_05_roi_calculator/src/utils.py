"""
Fonctions utilitaires pour le ROI Marketing Calculator
"""
from typing import Union, Optional, Dict, Any
from datetime import datetime
import json
import re


class ValidationError(Exception):
    """Exception personnalisée pour les erreurs de validation"""
    pass


class DataValidator:
    """Validateur de données pour les métriques marketing"""
    
    @staticmethod
    def validate_positive_number(
        value: Union[int, float],
        name: str,
        allow_zero: bool = False
    ) -> Union[int, float]:
        """
        Valide qu'un nombre est positif
        
        Args:
            value: Valeur à valider
            name: Nom du paramètre (pour le message d'erreur)
            allow_zero: Si True, accepte 0 comme valeur valide
            
        Returns:
            La valeur validée
            
        Raises:
            ValidationError: Si la validation échoue
        """
        if not isinstance(value, (int, float)):
            raise ValidationError(f"{name} doit être un nombre")
        
        if allow_zero:
            if value < 0:
                raise ValidationError(f"{name} ne peut pas être négatif")
        else:
            if value <= 0:
                raise ValidationError(f"{name} doit être strictement positif")
        
        return value
    
    @staticmethod
    def validate_percentage(value: float, name: str) -> float:
        """
        Valide qu'un pourcentage est dans la plage [0, 100]
        
        Args:
            value: Valeur à valider
            name: Nom du paramètre
            
        Returns:
            La valeur validée
            
        Raises:
            ValidationError: Si la validation échoue
        """
        if not isinstance(value, (int, float)):
            raise ValidationError(f"{name} doit être un nombre")
        
        if not 0 <= value <= 100:
            raise ValidationError(f"{name} doit être entre 0 et 100")
        
        return float(value)
    
    @staticmethod
    def validate_budget(budget: float, max_budget: float = 10_000_000) -> float:
        """
        Valide un budget
        
        Args:
            budget: Budget à valider
            max_budget: Budget maximum autorisé
            
        Returns:
            Le budget validé
            
        Raises:
            ValidationError: Si la validation échoue
        """
        if not isinstance(budget, (int, float)):
            raise ValidationError("Le budget doit être un nombre")
        
        if budget < 0:
            raise ValidationError("Le budget ne peut pas être négatif")
        
        if budget > max_budget:
            raise ValidationError(
                f"Le budget ne peut pas dépasser {format_currency(max_budget)}"
            )
        
        return float(budget)
    
    @staticmethod
    def validate_metrics_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valide un dictionnaire de métriques
        
        Args:
            data: Dictionnaire contenant les métriques
            
        Returns:
            Le dictionnaire validé
            
        Raises:
            ValidationError: Si la validation échoue
        """
        required_fields = ["cost", "revenue"]
        
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Le champ '{field}' est requis")
        
        # Validation des valeurs numériques
        if "cost" in data:
            data["cost"] = DataValidator.validate_positive_number(
                data["cost"], "Coût", allow_zero=True
            )
        
        if "revenue" in data:
            data["revenue"] = DataValidator.validate_positive_number(
                data["revenue"], "Revenu", allow_zero=True
            )
        
        if "impressions" in data:
            data["impressions"] = int(DataValidator.validate_positive_number(
                data["impressions"], "Impressions", allow_zero=False
            ))
        
        if "clicks" in data:
            data["clicks"] = int(DataValidator.validate_positive_number(
                data["clicks"], "Clics", allow_zero=True
            ))
        
        if "conversions" in data:
            data["conversions"] = int(DataValidator.validate_positive_number(
                data["conversions"], "Conversions", allow_zero=True
            ))
        
        # Validation de cohérence
        if "clicks" in data and "impressions" in data:
            if data["clicks"] > data["impressions"]:
                raise ValidationError(
                    "Le nombre de clics ne peut pas dépasser le nombre d'impressions"
                )
        
        if "conversions" in data and "clicks" in data:
            if data["conversions"] > data["clicks"]:
                raise ValidationError(
                    "Le nombre de conversions ne peut pas dépasser le nombre de clics"
                )
        
        return data


class NumberFormatter:
    """Formateur de nombres pour l'affichage"""
    
    @staticmethod
    def format_currency(
        amount: float,
        currency: str = "€",
        decimals: int = 2
    ) -> str:
        """
        Formate un montant en devise
        
        Args:
            amount: Montant à formater
            currency: Symbole de la devise
            decimals: Nombre de décimales
            
        Returns:
            Montant formaté (ex: "1 234,56 €")
        """
        formatted = f"{amount:,.{decimals}f}".replace(",", " ").replace(".", ",")
        return f"{formatted} {currency}"
    
    @staticmethod
    def format_percentage(
        value: float,
        decimals: int = 2,
        include_sign: bool = True
    ) -> str:
        """
        Formate un pourcentage
        
        Args:
            value: Valeur à formater
            decimals: Nombre de décimales
            include_sign: Inclure le signe + pour les valeurs positives
            
        Returns:
            Pourcentage formaté (ex: "+15,23 %")
        """
        sign = "+" if value > 0 and include_sign else ""
        formatted = f"{value:.{decimals}f}".replace(".", ",")
        return f"{sign}{formatted} %"
    
    @staticmethod
    def format_number(
        value: Union[int, float],
        decimals: int = 0,
        compact: bool = False
    ) -> str:
        """
        Formate un nombre
        
        Args:
            value: Nombre à formater
            decimals: Nombre de décimales
            compact: Utiliser notation compacte (K, M, B)
            
        Returns:
            Nombre formaté
        """
        if compact:
            return NumberFormatter._format_compact(value)
        
        if decimals == 0:
            return f"{int(value):,}".replace(",", " ")
        else:
            formatted = f"{value:,.{decimals}f}".replace(",", " ").replace(".", ",")
            return formatted
    
    @staticmethod
    def _format_compact(value: float) -> str:
        """Formate un nombre en notation compacte"""
        abs_value = abs(value)
        sign = "-" if value < 0 else ""
        
        if abs_value >= 1_000_000_000:
            return f"{sign}{abs_value/1_000_000_000:.1f}B"
        elif abs_value >= 1_000_000:
            return f"{sign}{abs_value/1_000_000:.1f}M"
        elif abs_value >= 1_000:
            return f"{sign}{abs_value/1_000:.1f}K"
        else:
            return f"{sign}{abs_value:.0f}"
    
    @staticmethod
    def format_metric(
        value: float,
        metric_type: str,
        decimals: int = 2
    ) -> str:
        """
        Formate une métrique selon son type
        
        Args:
            value: Valeur de la métrique
            metric_type: Type de métrique (roi, cpc, cpm, etc.)
            decimals: Nombre de décimales
            
        Returns:
            Métrique formatée
        """
        metric_type = metric_type.lower()
        
        if metric_type in ["roi", "roas", "ctr", "conversion_rate"]:
            return NumberFormatter.format_percentage(value, decimals)
        elif metric_type in ["cpc", "cpm", "cpa", "cpl", "cost", "revenue"]:
            return NumberFormatter.format_currency(value, decimals=decimals)
        else:
            return NumberFormatter.format_number(value, decimals)


class DateTimeHelper:
    """Aide pour la gestion des dates et heures"""
    
    @staticmethod
    def get_timestamp() -> str:
        """Retourne un timestamp au format ISO"""
        return datetime.now().isoformat()
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%d/%m/%Y %H:%M") -> str:
        """
        Formate une date/heure
        
        Args:
            dt: Objet datetime
            format_str: Format de sortie
            
        Returns:
            Date formatée
        """
        return dt.strftime(format_str)
    
    @staticmethod
    def get_date_range_label(days: int) -> str:
        """
        Génère un label pour une période
        
        Args:
            days: Nombre de jours
            
        Returns:
            Label de la période
        """
        if days == 1:
            return "Aujourd'hui"
        elif days == 7:
            return "7 derniers jours"
        elif days == 30:
            return "30 derniers jours"
        elif days == 90:
            return "3 derniers mois"
        else:
            return f"{days} derniers jours"


class FileHelper:
    """Aide pour la gestion des fichiers"""
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Nettoie un nom de fichier
        
        Args:
            filename: Nom de fichier à nettoyer
            
        Returns:
            Nom de fichier nettoyé
        """
        # Remplace les caractères invalides
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Limite la longueur
        filename = filename[:200]
        return filename
    
    @staticmethod
    def generate_export_filename(
        prefix: str,
        extension: str,
        include_timestamp: bool = True
    ) -> str:
        """
        Génère un nom de fichier pour l'export
        
        Args:
            prefix: Préfixe du nom de fichier
            extension: Extension du fichier
            include_timestamp: Inclure un timestamp
            
        Returns:
            Nom de fichier généré
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if include_timestamp:
            filename = f"{prefix}_{timestamp}.{extension}"
        else:
            filename = f"{prefix}.{extension}"
        
        return FileHelper.sanitize_filename(filename)
    
    @staticmethod
    def save_json(data: Dict[str, Any], filepath: str) -> None:
        """
        Sauvegarde des données en JSON
        
        Args:
            data: Données à sauvegarder
            filepath: Chemin du fichier
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        """
        Charge des données depuis JSON
        
        Args:
            filepath: Chemin du fichier
            
        Returns:
            Données chargées
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)


# Fonctions helpers globales pour l'usage courant
def format_currency(amount: float, currency: str = "€", decimals: int = 2) -> str:
    """Raccourci pour formater une devise"""
    return NumberFormatter.format_currency(amount, currency, decimals)


def format_percentage(value: float, decimals: int = 2) -> str:
    """Raccourci pour formater un pourcentage"""
    return NumberFormatter.format_percentage(value, decimals)


def format_number(value: Union[int, float], decimals: int = 0) -> str:
    """Raccourci pour formater un nombre"""
    return NumberFormatter.format_number(value, decimals)


def validate_positive(value: Union[int, float], name: str) -> Union[int, float]:
    """Raccourci pour valider un nombre positif"""
    return DataValidator.validate_positive_number(value, name)