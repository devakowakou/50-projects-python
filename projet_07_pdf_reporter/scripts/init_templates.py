"""
Script d'initialisation des templates
"""
import json
from pathlib import Path

def init_templates():
    """Initialise les templates par défaut"""
    
    templates_dir = Path(__file__).parent.parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    templates = {
        "commercial": {
            "name": "Rapport Commercial",
            "description": "Rapport d'analyse commerciale",
            "kpis": ["chiffre_affaires", "nombre_ventes", "panier_moyen"],
            "charts": ["evolution_ventes", "top_produits"],
            "sections": ["synthese", "performance", "tendances"]
        },
        "financier": {
            "name": "Rapport Financier",
            "description": "Rapport d'analyse financière",
            "kpis": ["revenus", "depenses", "benefice_net"],
            "charts": ["evolution_tresorerie", "repartition_charges"],
            "sections": ["synthese", "revenus", "depenses"]
        },
        "ressources_humaines": {
            "name": "Rapport RH",
            "description": "Rapport des ressources humaines",
            "kpis": ["effectif_total", "taux_turnover", "masse_salariale"],
            "charts": ["evolution_effectif", "pyramide_ages"],
            "sections": ["effectifs", "mobilite", "formation"]
        }
    }
    
    for name, config in templates.items():
        template_path = templates_dir / f"{name}.json"
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print(f"✅ Template créé: {template_path}")

if __name__ == "__main__":
    init_templates()
    print("\n🎉 Tous les templates ont été initialisés!")
