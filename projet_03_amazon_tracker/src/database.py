"""
Module de gestion de la base de données SQLite
"""
import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
import config


class DatabaseManager:
    """Gestionnaire de la base de données SQLite"""
    
    def __init__(self, db_path=None):
        """
        Initialise le gestionnaire de base de données
        
        Args:
            db_path: Chemin vers le fichier de base de données
        """
        self.db_path = db_path or config.DB_PATH
        self._init_database()
    
    def _init_database(self):
        """Crée les tables si elles n'existent pas"""
        # Créer le dossier data si nécessaire
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table products
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                asin TEXT,
                name TEXT NOT NULL,
                current_price REAL,
                target_price REAL,
                image_url TEXT,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_checked TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Table price_history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                price REAL NOT NULL,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                availability TEXT DEFAULT 'In Stock',
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        ''')
        
        # Index pour performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_product_id 
            ON price_history(product_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_checked_at 
            ON price_history(checked_at)
        ''')
        
        conn.commit()
        conn.close()
    
    def add_product(self, url, name, price, target_price, asin=None, image_url=None):
        """
        Ajoute un nouveau produit à suivre
        
        Args:
            url: URL du produit
            name: Nom du produit
            price: Prix actuel
            target_price: Prix cible
            asin: ASIN du produit
            image_url: URL de l'image
            
        Returns:
            ID du produit créé ou None si erreur
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now()
            
            cursor.execute('''
                INSERT INTO products (url, asin, name, current_price, target_price, 
                                     image_url, last_checked)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (url, asin, name, price, target_price, image_url, now))
            
            product_id = cursor.lastrowid
            
            # Ajouter le premier enregistrement de prix
            cursor.execute('''
                INSERT INTO price_history (product_id, price, availability)
                VALUES (?, ?, ?)
            ''', (product_id, price, 'In Stock'))
            
            conn.commit()
            conn.close()
            
            return product_id
        except sqlite3.IntegrityError:
            # Produit existe déjà
            return None
        except Exception as e:
            print(f"Erreur lors de l'ajout du produit: {e}")
            return None
    
    def get_all_products(self):
        """
        Récupère tous les produits actifs
        
        Returns:
            DataFrame avec tous les produits
        """
        conn = sqlite3.connect(self.db_path)
        query = '''
            SELECT id, url, asin, name, current_price, target_price, 
                   image_url, added_date, last_checked, is_active
            FROM products
            WHERE is_active = 1
            ORDER BY added_date DESC
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def get_product_by_id(self, product_id):
        """
        Récupère un produit par son ID
        
        Args:
            product_id: ID du produit
            
        Returns:
            Dict avec les infos du produit ou None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, url, asin, name, current_price, target_price, 
                   image_url, added_date, last_checked, is_active
            FROM products
            WHERE id = ?
        ''', (product_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'url': result[1],
                'asin': result[2],
                'name': result[3],
                'current_price': result[4],
                'target_price': result[5],
                'image_url': result[6],
                'added_date': result[7],
                'last_checked': result[8],
                'is_active': result[9]
            }
        return None
    
    def update_price(self, product_id, new_price, availability='In Stock'):
        """
        Met à jour le prix d'un produit et ajoute un enregistrement à l'historique
        
        Args:
            product_id: ID du produit
            new_price: Nouveau prix
            availability: Disponibilité du produit
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now()
        
        # Mettre à jour le produit
        cursor.execute('''
            UPDATE products
            SET current_price = ?, last_checked = ?
            WHERE id = ?
        ''', (new_price, now, product_id))
        
        # Ajouter à l'historique
        cursor.execute('''
            INSERT INTO price_history (product_id, price, availability)
            VALUES (?, ?, ?)
        ''', (product_id, new_price, availability))
        
        conn.commit()
        conn.close()
    
    def get_price_history(self, product_id, days=30):
        """
        Récupère l'historique des prix d'un produit
        
        Args:
            product_id: ID du produit
            days: Nombre de jours d'historique
            
        Returns:
            DataFrame avec l'historique
        """
        conn = sqlite3.connect(self.db_path)
        query = '''
            SELECT price, checked_at, availability
            FROM price_history
            WHERE product_id = ?
            AND checked_at >= datetime('now', '-' || ? || ' days')
            ORDER BY checked_at ASC
        '''
        df = pd.read_sql_query(query, conn, params=(product_id, days))
        conn.close()
        
        if not df.empty:
            df['checked_at'] = pd.to_datetime(df['checked_at'])
        
        return df
    
    def get_products_below_target(self):
        """
        Récupère les produits dont le prix est inférieur ou égal au prix cible
        
        Returns:
            Liste de dictionnaires avec les infos des produits
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, url, name, current_price, target_price
            FROM products
            WHERE is_active = 1
            AND current_price IS NOT NULL
            AND target_price IS NOT NULL
            AND current_price <= target_price
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        products = []
        for row in results:
            products.append({
                'id': row[0],
                'url': row[1],
                'name': row[2],
                'current_price': row[3],
                'target_price': row[4]
            })
        
        return products
    
    def delete_product(self, product_id):
        """
        Supprime un produit (soft delete)
        
        Args:
            product_id: ID du produit
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE products
            SET is_active = 0
            WHERE id = ?
        ''', (product_id,))
        
        conn.commit()
        conn.close()
    
    def get_product_count(self):
        """
        Récupère le nombre total de produits actifs
        
        Returns:
            Nombre de produits
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM products WHERE is_active = 1')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def add_demo_products(self):
        """
        Ajoute des produits de démonstration pour tester l'interface
        """
        import random
        from datetime import datetime, timedelta
        
        demo_products = [
            {
                'name': 'Apple AirPods Pro (2ème génération)',
                'url': 'https://www.amazon.fr/dp/B0CHWRXH8B',
                'asin': 'B0CHWRXH8B',
                'current_price': 279.00,
                'target_price': 250.00,
                'image_url': 'https://m.media-amazon.com/images/I/61SUj2aKoEL._AC_SL1500_.jpg',
            },
            {
                'name': 'Logitech MX Master 3S Souris Sans Fil',
                'url': 'https://www.amazon.fr/dp/B09HM94VDS',
                'asin': 'B09HM94VDS',
                'current_price': 89.99,
                'target_price': 75.00,
                'image_url': 'https://m.media-amazon.com/images/I/61ni3t1ryQL._AC_SL1500_.jpg',
            },
            {
                'name': 'Samsung Galaxy Buds2 Pro',
                'url': 'https://www.amazon.fr/dp/B0B3KBVNPM',
                'asin': 'B0B3KBVNPM',
                'current_price': 149.00,
                'target_price': 130.00,
                'image_url': 'https://m.media-amazon.com/images/I/51SHNR1+CrL._AC_SL1000_.jpg',
            },
            {
                'name': 'Kindle Paperwhite (16 Go)',
                'url': 'https://www.amazon.fr/dp/B08N3K1H8J',
                'asin': 'B08N3K1H8J',
                'current_price': 159.99,
                'target_price': 140.00,
                'image_url': 'https://m.media-amazon.com/images/I/51QCk82iGcL._AC_SL1000_.jpg',
            },
            {
                'name': 'Sony WH-1000XM5 Casque Bluetooth',
                'url': 'https://www.amazon.fr/dp/B09XS7JWHH',
                'asin': 'B09XS7JWHH',
                'current_price': 329.00,
                'target_price': 299.00,
                'image_url': 'https://m.media-amazon.com/images/I/51K32BqSO5L._AC_SL1500_.jpg',
            },
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for product in demo_products:
            try:
                now = datetime.now()
                
                # Ajouter le produit
                cursor.execute('''
                    INSERT OR IGNORE INTO products (url, asin, name, current_price, target_price, 
                                         image_url, last_checked)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (product['url'], product['asin'], product['name'], 
                      product['current_price'], product['target_price'], 
                      product['image_url'], now))
                
                product_id = cursor.lastrowid
                
                if product_id > 0:
                    # Générer un historique de prix sur 30 jours
                    base_price = product['current_price']
                    
                    for i in range(30, -1, -1):
                        # Variation aléatoire de +/- 10%
                        variation = random.uniform(-0.10, 0.10)
                        price = round(base_price * (1 + variation), 2)
                        date = now - timedelta(days=i)
                        
                        cursor.execute('''
                            INSERT INTO price_history (product_id, price, checked_at, availability)
                            VALUES (?, ?, ?, ?)
                        ''', (product_id, price, date, 'In Stock'))
            
            except Exception as e:
                print(f"Erreur lors de l'ajout du produit démo: {e}")
        
        conn.commit()
        conn.close()
