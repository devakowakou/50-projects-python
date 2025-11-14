"""
Calculateur de KPIs e-commerce
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class EcommerceKPICalculator:
    def __init__(self, orders_df, order_items_df, visitors_df, products_df):
        self.orders = orders_df.copy()
        self.order_items = order_items_df.copy()
        self.visitors = visitors_df.copy()
        self.products = products_df.copy()
        
        # Convertir les dates si les DataFrames ne sont pas vides
        if not self.orders.empty and 'order_date' in self.orders.columns:
            self.orders['order_date'] = pd.to_datetime(self.orders['order_date'])
        if not self.visitors.empty and 'visit_date' in self.visitors.columns:
            self.visitors['visit_date'] = pd.to_datetime(self.visitors['visit_date'])
    
    def calculate_main_kpis(self, start_date=None, end_date=None, channel=None):
        """Calcule les KPIs principaux"""
        # Filtrer les données
        orders_filtered = self._filter_orders(start_date, end_date, channel)
        visitors_filtered = self._filter_visitors(start_date, end_date, channel)
        
        # CA Total
        total_revenue = orders_filtered['total_amount'].sum() if not orders_filtered.empty else 0
        
        # Nombre de commandes
        total_orders = len(orders_filtered)
        
        # Panier moyen
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Nombre de visiteurs
        total_visitors = len(visitors_filtered)
        
        # Taux de conversion
        conversion_rate = (total_orders / total_visitors * 100) if total_visitors > 0 else 0
        
        return {
            'total_revenue': round(total_revenue, 2),
            'total_orders': total_orders,
            'avg_order_value': round(avg_order_value, 2),
            'total_visitors': total_visitors,
            'conversion_rate': round(conversion_rate, 2)
        }
    
    def calculate_evolution(self, days=30):
        """Calcule l'évolution des KPIs sur une période"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Période actuelle
        current_kpis = self.calculate_main_kpis(start_date, end_date)
        
        # Période précédente
        prev_end_date = start_date
        prev_start_date = prev_end_date - timedelta(days=days)
        prev_kpis = self.calculate_main_kpis(prev_start_date, prev_end_date)
        
        # Calcul des évolutions
        evolution = {}
        for key in current_kpis:
            if prev_kpis[key] > 0:
                evolution[f'{key}_evolution'] = round(
                    ((current_kpis[key] - prev_kpis[key]) / prev_kpis[key]) * 100, 1
                )
            else:
                evolution[f'{key}_evolution'] = 0
        
        return {**current_kpis, **evolution}
    
    def get_revenue_by_period(self, period='D', days=30):
        """CA par période (jour, semaine, mois)"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        orders_filtered = self._filter_orders(start_date, end_date)
        
        revenue_by_period = orders_filtered.groupby(
            orders_filtered['order_date'].dt.to_period(period)
        )['total_amount'].sum().reset_index()
        
        revenue_by_period['order_date'] = revenue_by_period['order_date'].astype(str)
        
        return revenue_by_period
    
    def get_top_products(self, limit=10, days=30):
        """Top produits par CA"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        orders_filtered = self._filter_orders(start_date, end_date)
        order_ids = orders_filtered['order_id'].tolist()
        
        items_filtered = self.order_items[self.order_items['order_id'].isin(order_ids)]
        
        top_products = items_filtered.groupby('product_id').agg({
            'total_price': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        # Joindre avec les infos produits
        top_products = top_products.merge(self.products, on='product_id')
        top_products = top_products.sort_values('total_price', ascending=False).head(limit)
        
        return top_products
    
    def get_revenue_by_category(self, days=30):
        """CA par catégorie"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        orders_filtered = self._filter_orders(start_date, end_date)
        order_ids = orders_filtered['order_id'].tolist()
        
        items_filtered = self.order_items[self.order_items['order_id'].isin(order_ids)]
        items_with_products = items_filtered.merge(self.products, on='product_id')
        
        revenue_by_category = items_with_products.groupby('category')['total_price'].sum().reset_index()
        revenue_by_category = revenue_by_category.sort_values('total_price', ascending=False)
        
        return revenue_by_category
    
    def get_conversion_by_channel(self, days=30):
        """Taux de conversion par canal"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        orders_by_channel = self._filter_orders(start_date, end_date).groupby('channel').size()
        visitors_by_channel = self._filter_visitors(start_date, end_date).groupby('channel').size()
        
        conversion_by_channel = pd.DataFrame({
            'channel': orders_by_channel.index,
            'orders': orders_by_channel.values,
            'visitors': visitors_by_channel.reindex(orders_by_channel.index, fill_value=0).values
        })
        
        conversion_by_channel['conversion_rate'] = (
            conversion_by_channel['orders'] / conversion_by_channel['visitors'] * 100
        ).round(2)
        
        return conversion_by_channel.sort_values('conversion_rate', ascending=False)
    
    def _filter_orders(self, start_date=None, end_date=None, channel=None):
        """Filtre les commandes"""
        filtered = self.orders.copy()
        
        if start_date:
            filtered = filtered[filtered['order_date'] >= start_date]
        if end_date:
            filtered = filtered[filtered['order_date'] <= end_date]
        if channel:
            filtered = filtered[filtered['channel'] == channel]
            
        return filtered
    
    def _filter_visitors(self, start_date=None, end_date=None, channel=None):
        """Filtre les visiteurs"""
        filtered = self.visitors.copy()
        
        if start_date:
            filtered = filtered[filtered['visit_date'] >= start_date]
        if end_date:
            filtered = filtered[filtered['visit_date'] <= end_date]
        if channel:
            filtered = filtered[filtered['channel'] == channel]
            
        return filtered