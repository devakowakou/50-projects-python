"""
Moteur de gestion des templates
"""
import json
from pathlib import Path
from typing import Dict, Optional
from config import TEMPLATES, TEMPLATES_DIR
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class TemplateEngine:
    """Classe pour gérer les templates de rapports"""
    
    def __init__(self):
        self.templates = TEMPLATES
        self.current_template = None
    
    def load_template(self, template_name: str) -> dict:
        """
        Charge la configuration d'un template
        
        Args:
            template_name: Nom du template
        
        Returns:
            dict: Configuration du template
        """
        template_path = self.templates_dir / f"{template_name}.json"
        
        if not template_path.exists():
            # Créer un template par défaut si inexistant
            default_config = self._get_default_template(template_name)
            self._save_template(template_name, default_config)
            return default_config
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
                # Vérifier si le fichier est vide
                if not content:
                    default_config = self._get_default_template(template_name)
                    self._save_template(template_name, default_config)
                    return default_config
                
                config = json.loads(content)
                return config
                
        except json.JSONDecodeError as e:
            # Si le JSON est invalide, recréer le template
            print(f"⚠️ Template {template_name} invalide, recréation...")
            default_config = self._get_default_template(template_name)
            self._save_template(template_name, default_config)
            return default_config
        except Exception as e:
            raise Exception(f"Erreur chargement template {template_name}: {str(e)}")

    def _get_default_template(self, template_name: str) -> dict:
        """
        Retourne la configuration par défaut d'un template
        
        Args:
            template_name: Nom du template
        
        Returns:
            dict: Configuration par défaut
        """
        default_templates = {
            "commercial": {
                "name": "Rapport Commercial",
                "description": "Rapport d'analyse commerciale",
                "kpis": ["chiffre_affaires", "nombre_ventes", "panier_moyen", "taux_conversion"],
                "charts": ["evolution_ventes", "top_produits", "repartition_ca"],
                "sections": ["synthese", "performance", "tendances", "recommandations"],
                "colors": {
                    "primary": "#2E86AB",
                    "secondary": "#A23B72",
                    "success": "#06A77D",
                    "warning": "#F18F01"
                }
            },
            "financier": {
                "name": "Rapport Financier",
                "description": "Rapport d'analyse financière",
                "kpis": ["revenus", "depenses", "benefice_net", "marge_beneficiaire"],
                "charts": ["evolution_tresorerie", "repartition_charges", "analyse_rentabilite"],
                "sections": ["synthese", "revenus", "depenses", "analyse"],
                "colors": {
                    "primary": "#1B4965",
                    "secondary": "#62B6CB",
                    "success": "#5FA052",
                    "warning": "#EE964B"
                }
            },
            "ressources_humaines": {
                "name": "Rapport RH",
                "description": "Rapport des ressources humaines",
                "kpis": ["effectif_total", "taux_turnover", "masse_salariale", "taux_absenteisme"],
                "charts": ["evolution_effectif", "pyramide_ages", "repartition_services"],
                "sections": ["effectifs", "mobilite", "formation", "social"],
                "colors": {
                    "primary": "#6A4C93",
                    "secondary": "#8AC926",
                    "success": "#1982C4",
                    "warning": "#FFCA3A"
                }
            }
        }
        
        return default_templates.get(template_name, default_templates["commercial"])

    def _save_template(self, template_name: str, config: dict) -> None:
        """
        Sauvegarde un template
        
        Args:
            template_name: Nom du template
            config: Configuration à sauvegarder
        """
        template_path = self.templates_dir / f"{template_name}.json"
        
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    
    def get_available_templates(self) -> Dict:
        """Retourne la liste des templates disponibles"""
        return {
            name: info["description"] 
            for name, info in self.templates.items()