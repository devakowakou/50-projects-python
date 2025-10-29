"""
Module d'analyse des prix
"""
import pandas as pd
import numpy as np
from src.database import DatabaseManager


class PriceAnalyzer:
    """Analyseur de prix et générateur d'alertes"""
    
    def __init__(self, db_manager=None):
        """
        Initialise l'analyseur
        
        Args:
            db_manager: Instance de DatabaseManager
        """
        self.db = db_manager or DatabaseManager()
    
    def get_price_stats(self, product_id, days=30):
        """
        Calcule les statistiques de prix pour un produit
        
        Args:
            product_id: ID du produit
            days: Nombre de jours d'historique
            
        Returns:
            Dict avec les statistiques
        """
        df = self.db.get_price_history(product_id, days)
        
        if df.empty:
            return None
        
        stats = {
            'min': df['price'].min(),
            'max': df['price'].max(),
            'mean': df['price'].mean(),
            'median': df['price'].median(),
            'std': df['price'].std(),
            'current': df['price'].iloc[-1],
            'first': df['price'].iloc[0],
            'count': len(df)
        }
        
        # Calculer la variation
        if stats['first'] > 0:
            stats['variation_percent'] = ((stats['current'] - stats['first']) / stats['first']) * 100
        else:
            stats['variation_percent'] = 0
        
        return stats
    
    def get_price_trend(self, product_id, days=30):
        """
        Détermine la tendance du prix
        
        Args:
            product_id: ID du produit
            days: Nombre de jours d'historique
            
        Returns:
            'hausse' | 'baisse' | 'stable' | None
        """
        df = self.db.get_price_history(product_id, days)
        
        if len(df) < 2:
            return None
        
        # Comparer les 7 derniers jours avec les 7 jours précédents
        if len(df) >= 14:
            recent = df.tail(7)['price'].mean()
            previous = df.iloc[-14:-7]['price'].mean()
        else:
            # Si moins de 14 jours, comparer première moitié vs deuxième moitié
            mid = len(df) // 2
            previous = df.iloc[:mid]['price'].mean()
            recent = df.iloc[mid:]['price'].mean()
        
        # Seuil de 2% pour considérer un changement
        threshold = 0.02
        diff = (recent - previous) / previous
        
        if diff > threshold:
            return 'hausse'
        elif diff < -threshold:
            return 'baisse'
        else:
            return 'stable'
    
    def check_alerts(self):
        """
        Vérifie tous les produits et retourne ceux nécessitant une alerte
        
        Returns:
            Liste de dicts avec les infos des produits en alerte
        """
        products = self.db.get_products_below_target()
        
        alerts = []
        for product in products:
            savings = product['target_price'] - product['current_price']
            savings_percent = (savings / product['target_price']) * 100
            
            alerts.append({
                'id': product['id'],
                'name': product['name'],
                'url': product['url'],
                'current_price': product['current_price'],
                'target_price': product['target_price'],
                'savings': savings,
                'savings_percent': savings_percent
            })
        
        return alerts
    
    def get_best_price_info(self, product_id, days=30):
        """
        Détermine si c'est le bon moment pour acheter
        
        Args:
            product_id: ID du produit
            days: Nombre de jours d'historique
            
        Returns:
            Dict avec recommandation
        """
        stats = self.get_price_stats(product_id, days)
        trend = self.get_price_trend(product_id, days)
        product = self.db.get_product_by_id(product_id)
        
        if not stats or not product:
            return None
        
        current = stats['current']
        min_price = stats['min']
        max_price = stats['max']
        mean_price = stats['mean']
        
        # Calculer la position du prix actuel
        price_range = max_price - min_price
        if price_range > 0:
            position = ((current - min_price) / price_range) * 100
        else:
            position = 50
        
        # Recommandation
        if current <= min_price * 1.05:  # Dans les 5% du minimum
            recommendation = "🟢 Excellent prix ! C'est le moment d'acheter"
            urgency = "high"
        elif current <= mean_price:  # En dessous de la moyenne
            if trend == 'baisse':
                recommendation = "🟡 Bon prix et en baisse. Vous pouvez attendre encore un peu"
                urgency = "medium"
            else:
                recommendation = "🟢 Bon prix ! Recommandé d'acheter"
                urgency = "high"
        elif current <= mean_price * 1.1:  # Proche de la moyenne
            if trend == 'baisse':
                recommendation = "🟡 Prix correct et en baisse. Attendez"
                urgency = "low"
            else:
                recommendation = "🟠 Prix moyen. Vous pouvez attendre"
                urgency = "low"
        else:  # Au-dessus de la moyenne
            recommendation = "🔴 Prix élevé. Attendez une baisse"
            urgency = "none"
        
        return {
            'recommendation': recommendation,
            'urgency': urgency,
            'position': position,
            'is_below_target': current <= product['target_price'] if product['target_price'] else False,
            'days_tracked': stats['count']
        }
    
    def calculate_savings_potential(self):
        """
        Calcule les économies potentielles totales
        
        Returns:
            Dict avec les économies totales
        """
        products = self.db.get_products_below_target()
        
        total_savings = 0
        product_count = len(products)
        
        for product in products:
            savings = product['target_price'] - product['current_price']
            total_savings += savings
        
        return {
            'total_savings': total_savings,
            'product_count': product_count,
            'average_savings': total_savings / product_count if product_count > 0 else 0
        }
