"""Scraper immobilier principal"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from typing import List, Dict
from config import SCRAPING_CONFIG
import sqlite3
from datetime import datetime

class RealEstateScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': SCRAPING_CONFIG['user_agent']
        })
        self.delay = SCRAPING_CONFIG['delay']
    
    def scrape_sample_data(self) -> List[Dict]:
        """Génère données d'exemple (simulation)"""
        import random
        
        quartiers = [
            "Marais", "Montmartre", "Saint-Germain", "Bastille", "République",
            "Belleville", "Oberkampf", "Nation", "Châtelet", "Opéra"
        ]
        
        properties = []
        for i in range(100):
            quartier = random.choice(quartiers)
            surface = random.randint(20, 120)
            price_per_m2 = random.randint(8000, 15000)
            price = surface * price_per_m2
            
            properties.append({
                "id": f"prop_{i:03d}",
                "title": f"Appartement {surface}m² - {quartier}",
                "price": price,
                "surface": surface,
                "price_per_m2": price_per_m2,
                "rooms": random.randint(1, 5),
                "quartier": quartier,
                "address": f"{random.randint(1, 200)} rue de {quartier}",
                "description": f"Bel appartement de {surface}m² dans le quartier {quartier}",
                "scraped_at": datetime.now().isoformat()
            })
        
        return properties
    
    def clean_price(self, price_text: str) -> int:
        """Nettoie le prix"""
        if not price_text:
            return 0
        
        # Supprime tout sauf les chiffres
        price = re.sub(r'[^\d]', '', price_text)
        return int(price) if price else 0
    
    def clean_surface(self, surface_text: str) -> int:
        """Nettoie la surface"""
        if not surface_text:
            return 0
        
        match = re.search(r'(\d+)', surface_text)
        return int(match.group(1)) if match else 0
    
    def extract_quartier(self, address: str) -> str:
        """Extrait le quartier de l'adresse"""
        # Logique simplifiée
        quartiers_map = {
            "75001": "Louvre", "75002": "Bourse", "75003": "Temple",
            "75004": "Hôtel-de-Ville", "75005": "Panthéon", "75006": "Luxembourg",
            "75007": "Palais-Bourbon", "75008": "Élysée", "75009": "Opéra",
            "75010": "Enclos-St-Laurent", "75011": "Popincourt", "75012": "Reuilly"
        }
        
        for code, quartier in quartiers_map.items():
            if code in address:
                return quartier
        
        return "Autre"

class DatabaseManager:
    def __init__(self, db_path: str = "data/properties.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                id TEXT PRIMARY KEY,
                title TEXT,
                price INTEGER,
                surface INTEGER,
                price_per_m2 INTEGER,
                rooms INTEGER,
                quartier TEXT,
                address TEXT,
                description TEXT,
                scraped_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_properties(self, properties: List[Dict]):
        """Sauvegarde les propriétés"""
        conn = sqlite3.connect(self.db_path)
        
        df = pd.DataFrame(properties)
        df.to_sql('properties', conn, if_exists='replace', index=False)
        
        conn.close()
    
    def load_properties(self) -> pd.DataFrame:
        """Charge les propriétés"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM properties", conn)
            conn.close()
            return df
        except:
            return pd.DataFrame()
    
    def get_quartier_stats(self) -> pd.DataFrame:
        """Statistiques par quartier"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                quartier,
                COUNT(*) as nb_biens,
                AVG(price) as prix_moyen,
                AVG(price_per_m2) as prix_m2_moyen,
                AVG(surface) as surface_moyenne,
                MIN(price) as prix_min,
                MAX(price) as prix_max
            FROM properties 
            GROUP BY quartier
            ORDER BY prix_m2_moyen DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df