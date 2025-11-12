"""
Générateur de données e-commerce réalistes
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict
import uuid

from config import (
    DATA_CONFIG, TRAFFIC_SOURCES, PRODUCT_CATEGORIES,
    CATEGORY_PRICE_RANGES, SOURCE_WEIGHTS, CONVERSION_RATES
)


class EcommerceDataGenerator:
    """Générateur de données e-commerce avec 10K transactions et 30K sessions"""
    
    def __init__(self):
        self.start_date = datetime.now() - timedelta(days=DATA_CONFIG["date_range_days"])
        self.end_date = datetime.now()
        
    def generate_transaction(self, transaction_id: int) -> Dict:
        """Génère une transaction réaliste"""
        # Date aléatoire dans la période
        random_days = random.randint(0, DATA_CONFIG["date_range_days"])
        date = self.start_date + timedelta(days=random_days)
        
        # Catégorie et prix correspondant
        category = random.choice(PRODUCT_CATEGORIES)
        min_price, max_price = CATEGORY_PRICE_RANGES[category]
        amount = round(random.uniform(min_price, max_price), 2)
        
        # Source de trafic pondérée
        source = random.choices(
            TRAFFIC_SOURCES, 
            weights=list(SOURCE_WEIGHTS.values())
        )[0]
        
        return {
            "id": f"TXN_{transaction_id:05d}",
            "date": date.strftime("%Y-%m-%d"),
            "customer_id": f"CUST_{random.randint(1, 5000):04d}",
            "amount": amount,
            "category": category,
            "source": source,
            "products_count": random.randint(1, 5)
        }
    
    def generate_session(self, session_id: int) -> Dict:
        """Génère une session avec probabilité de conversion"""
        # Date aléatoire
        random_days = random.randint(0, DATA_CONFIG["date_range_days"])
        date = self.start_date + timedelta(days=random_days)
        
        # Source pondérée
        source = random.choices(
            TRAFFIC_SOURCES,
            weights=list(SOURCE_WEIGHTS.values())
        )[0]
        
        # Conversion basée sur le taux par source
        converted = random.random() < CONVERSION_RATES[source]
        
        return {
            "id": f"SESS_{session_id:06d}",
            "date": date.strftime("%Y-%m-%d"),
            "source": source,
            "converted": converted,
            "pages_viewed": random.randint(1, 15)
        }
    
    def generate_all_data(self) -> tuple[List[Dict], List[Dict]]:
        """Génère toutes les données (transactions + sessions)"""
        print("🔄 Génération des données e-commerce...")
        
        # Génération des transactions (10K)
        transactions = []
        for i in range(1, DATA_CONFIG["transactions_count"] + 1):
            transactions.append(self.generate_transaction(i))
            if i % 1000 == 0:
                print(f"   📦 {i:,} transactions générées")
        
        # Génération des sessions (30K)
        sessions_count = DATA_CONFIG["transactions_count"] * DATA_CONFIG["sessions_multiplier"]
        sessions = []
        for i in range(1, sessions_count + 1):
            sessions.append(self.generate_session(i))
            if i % 5000 == 0:
                print(f"   👥 {i:,} sessions générées")
        
        print(f"✅ Données générées: {len(transactions):,} transactions, {len(sessions):,} sessions")
        return transactions, sessions
    
    def save_data(self, transactions: List[Dict], sessions: List[Dict], data_dir: str = "data"):
        """Sauvegarde les données en JSON"""
        import os
        os.makedirs(data_dir, exist_ok=True)
        
        # Sauvegarde transactions
        with open(f"{data_dir}/transactions.json", "w") as f:
            json.dump(transactions, f, indent=2)
        
        # Sauvegarde sessions
        with open(f"{data_dir}/sessions.json", "w") as f:
            json.dump(sessions, f, indent=2)
        
        print(f"💾 Données sauvegardées dans {data_dir}/")


def generate_sample_data():
    """Fonction utilitaire pour générer les données"""
    generator = EcommerceDataGenerator()
    transactions, sessions = generator.generate_all_data()
    generator.save_data(transactions, sessions)
    return transactions, sessions


if __name__ == "__main__":
    generate_sample_data()