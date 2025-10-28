"""
Générateur de données exemple pour le dashboard
"""
import json
import random
from datetime import datetime, timedelta
import uuid

def generate_example_transactions(num_transactions: int = 100) -> list:
    """
    Génère des transactions exemple réalistes
    """
    
    # Catégories et montants typiques
    depenses_config = {
        " Alimentation": {"min": 5, "max": 150, "freq": 0.25},
        " Logement": {"min": 500, "max": 1000, "freq": 0.05},
        " Transport": {"min": 2, "max": 80, "freq": 0.15},
        " Factures": {"min": 30, "max": 150, "freq": 0.08},
        " Loisirs": {"min": 10, "max": 100, "freq": 0.15},
        " Shopping": {"min": 20, "max": 200, "freq": 0.12},
        " Santé": {"min": 15, "max": 80, "freq": 0.05},
        " Éducation": {"min": 20, "max": 100, "freq": 0.05},
        " Épargne": {"min": 100, "max": 500, "freq": 0.05},
        " Autres": {"min": 10, "max": 100, "freq": 0.05}
    }
    
    revenus_config = {
        " Salaire": {"min": 2000, "max": 3500, "freq": 0.7},
        " Prime/Bonus": {"min": 200, "max": 1000, "freq": 0.1},
        " Freelance": {"min": 150, "max": 800, "freq": 0.15},
        " Investissements": {"min": 50, "max": 300, "freq": 0.03},
        " Autres": {"min": 20, "max": 200, "freq": 0.02}
    }
    
    descriptions_depenses = {
        " Alimentation": ["Courses Carrefour", "Restaurant", "Boulangerie", "Marché", "Lidl", "Auchan"],
        " Logement": ["Loyer", "Charges", "Assurance habitation"],
        " Transport": ["Essence", "Ticket métro", "Uber", "Péage", "Parking"],
        " Factures": ["EDF", "Internet Orange", "Téléphone", "Netflix", "Spotify"],
        " Loisirs": ["Cinéma", "Concert", "Bar", "Restaurant", "Sport"],
        " Shopping": ["Vêtements", "Chaussures", "Accessoires", "Amazon"],
        " Santé": ["Pharmacie", "Médecin", "Dentiste", "Mutuelle"],
        " Éducation": ["Livres", "Formation", "Cours en ligne"],
        " Épargne": ["Livret A", "PEL", "Assurance-vie"],
        " Autres": ["Cadeau", "Divers", "Frais bancaires"]
    }
    
    descriptions_revenus = {
        " Salaire": ["Salaire mensuel", "Salaire"],
        " Prime/Bonus": ["Prime annuelle", "Bonus performance", "13ème mois"],
        " Freelance": ["Mission freelance", "Projet client", "Prestation"],
        " Investissements": ["Dividendes", "Intérêts", "Plus-value"],
        " Autres": ["Remboursement", "Vente occasion", "Autre revenu"]
    }
    
    modes_paiement = [" Carte Bancaire", " Espèces", " Virement", " Mobile Payment", " Prélèvement Automatique"]
    
    transactions = []
    
    # Générer des transactions sur les 90 derniers jours
    start_date = datetime.now() - timedelta(days=90)
    
    # Calculer le nombre de dépenses et revenus
    num_depenses = int(num_transactions * 0.85)  # 85% dépenses
    num_revenus = num_transactions - num_depenses
    
    # Générer les dépenses
    for _ in range(num_depenses):
        # Choisir une catégorie selon la fréquence
        categories = list(depenses_config.keys())
        weights = [depenses_config[cat]["freq"] for cat in categories]
        categorie = random.choices(categories, weights=weights)[0]
        
        config = depenses_config[categorie]
        montant = round(random.uniform(config["min"], config["max"]), 2)
        
        # Date aléatoire
        days_ago = random.randint(0, 90)
        date = start_date + timedelta(days=days_ago)
        
        # Description
        description = random.choice(descriptions_depenses[categorie])
        
        # Mode de paiement
        mode = random.choice(modes_paiement)
        
        transaction = {
            "id": str(uuid.uuid4()),
            "date": date.strftime("%Y-%m-%d"),
            "type": "depense",
            "montant": montant,
            "categorie": categorie,
            "description": description,
            "mode_paiement": mode,
            "created_at": datetime.now().isoformat()
        }
        
        transactions.append(transaction)
    
    # Générer les revenus
    for _ in range(num_revenus):
        # Choisir une catégorie selon la fréquence
        categories = list(revenus_config.keys())
        weights = [revenus_config[cat]["freq"] for cat in categories]
        categorie = random.choices(categories, weights=weights)[0]
        
        config = revenus_config[categorie]
        montant = round(random.uniform(config["min"], config["max"]), 2)
        
        # Date aléatoire (salaires plutôt en début de mois)
        if categorie == " Salaire":
            # Salaire au début du mois
            month_offset = random.randint(0, 2)
            date = datetime.now() - timedelta(days=30*month_offset)
            date = date.replace(day=1)
        else:
            days_ago = random.randint(0, 90)
            date = start_date + timedelta(days=days_ago)
        
        # Description
        description = random.choice(descriptions_revenus[categorie])
        
        transaction = {
            "id": str(uuid.uuid4()),
            "date": date.strftime("%Y-%m-%d"),
            "type": "revenu",
            "montant": montant,
            "categorie": categorie,
            "description": description,
            "mode_paiement": " Virement",
            "created_at": datetime.now().isoformat()
        }
        
        transactions.append(transaction)
    
    # Trier par date (plus récent en premier)
    transactions.sort(key=lambda x: x["date"], reverse=True)
    
    return transactions


if __name__ == "__main__":
    # Générer et sauvegarder les données exemple
    transactions = generate_example_transactions(100)
    
    output_file = "data/exemple_transactions.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transactions, f, indent=2, ensure_ascii=False)
    
    print(f" {len(transactions)} transactions générées dans {output_file}")
