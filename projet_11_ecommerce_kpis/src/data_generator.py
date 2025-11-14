"""
Générateur de données e-commerce réalistes
"""
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker('fr_FR')

class EcommerceDataGenerator:
    def __init__(self):
        self.categories = ['Électronique', 'Vêtements', 'Maison', 'Sport', 'Beauté', 'Livres']
        self.channels = ['SEO', 'SEM', 'Social', 'Direct', 'Email']
        
    def generate_products(self, n_products=100):
        """Génère un catalogue de produits"""
        products = []
        for i in range(n_products):
            category = random.choice(self.categories)
            base_price = random.uniform(10, 500)
            
            products.append({
                'product_id': f'PROD_{i+1:04d}',
                'name': fake.catch_phrase(),
                'category': category,
                'price': round(base_price, 2),
                'cost': round(base_price * 0.6, 2)
            })
        
        return pd.DataFrame(products)
    
    def generate_customers(self, n_customers=1000):
        """Génère une base de clients"""
        customers = []
        for i in range(n_customers):
            customers.append({
                'customer_id': f'CUST_{i+1:05d}',
                'name': fake.name(),
                'email': fake.email(),
                'city': fake.city(),
                'registration_date': fake.date_between(start_date='-2y', end_date='today')
            })
        
        return pd.DataFrame(customers)
    
    def generate_orders(self, products_df, customers_df, n_orders=5000):
        """Génère des commandes réalistes"""
        orders = []
        order_items = []
        
        # Générer du trafic (visiteurs)
        visitors_data = []
        
        start_date = datetime.now() - timedelta(days=365)
        
        for i in range(n_orders):
            order_date = fake.date_time_between(start_date=start_date, end_date='now')
            customer = customers_df.sample(1).iloc[0]
            channel = random.choice(self.channels)
            
            # Nombre d'articles par commande (1-5)
            n_items = np.random.choice([1, 2, 3, 4, 5], p=[0.4, 0.3, 0.15, 0.1, 0.05])
            
            order_total = 0
            order_id = f'ORD_{i+1:06d}'
            
            # Générer les articles de la commande
            selected_products = products_df.sample(n_items)
            
            for _, product in selected_products.iterrows():
                quantity = random.randint(1, 3)
                item_total = product['price'] * quantity
                order_total += item_total
                
                order_items.append({
                    'order_id': order_id,
                    'product_id': product['product_id'],
                    'quantity': quantity,
                    'unit_price': product['price'],
                    'total_price': item_total
                })
            
            orders.append({
                'order_id': order_id,
                'customer_id': customer['customer_id'],
                'order_date': order_date,
                'channel': channel,
                'total_amount': round(order_total, 2),
                'status': 'completed'
            })
        
        # Générer du trafic (plus de visiteurs que de commandes)
        n_visitors = n_orders * random.randint(8, 15)  # Taux conversion 7-12%
        
        for i in range(n_visitors):
            visit_date = fake.date_time_between(start_date=start_date, end_date='now')
            channel = random.choice(self.channels)
            
            visitors_data.append({
                'visit_date': visit_date,
                'channel': channel,
                'visitor_id': f'VIS_{i+1:07d}'
            })
        
        return pd.DataFrame(orders), pd.DataFrame(order_items), pd.DataFrame(visitors_data)