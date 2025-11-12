"""
Calculateur des 5 KPIs e-commerce principaux
"""

import pandas as pd
from typing import Dict, List, Tuple
from config import METRIC_FORMATS


class EcommerceKPICalculator:
    """Calculateur des KPIs e-commerce avec méthodes optimisées"""
    
    def __init__(self, transactions_df: pd.DataFrame, sessions_df: pd.DataFrame):
        self.transactions = transactions_df
        self.sessions = sessions_df
        
        # Conversion des dates
        self.transactions['date'] = pd.to_datetime(self.transactions['date'])
        self.sessions['date'] = pd.to_datetime(self.sessions['date'])
    
    def calculate_total_revenue(self) -> float:
        """KPI 1: Chiffre d'affaires total"""
        return self.transactions['amount'].sum()
    
    def calculate_average_order_value(self) -> float:
        """KPI 2: Panier moyen (AOV)"""
        return self.transactions['amount'].mean()
    
    def calculate_conversion_rate(self) -> float:
        """KPI 3: Taux de conversion global"""
        total_sessions = len(self.sessions)
        converted_sessions = len(self.sessions[self.sessions['converted'] == True])
        return (converted_sessions / total_sessions) * 100 if total_sessions > 0 else 0
    
    def calculate_revenue_by_source(self) -> pd.DataFrame:
        """KPI 4: CA par source de trafic"""
        revenue_by_source = self.transactions.groupby('source')['amount'].agg([
            'sum', 'count', 'mean'
        ]).round(2)
        revenue_by_source.columns = ['total_revenue', 'transactions', 'avg_order_value']
        return revenue_by_source.sort_values('total_revenue', ascending=False)
    
    def calculate_revenue_by_category(self) -> pd.DataFrame:
        """KPI 5: Revenus par catégorie"""
        revenue_by_category = self.transactions.groupby('category')['amount'].agg([
            'sum', 'count', 'mean'
        ]).round(2)
        revenue_by_category.columns = ['total_revenue', 'transactions', 'avg_order_value']
        return revenue_by_category.sort_values('total_revenue', ascending=False)
    
    def get_main_kpis(self) -> Dict[str, float]:
        """Retourne les 5 KPIs principaux formatés"""
        return {
            "total_revenue": self.calculate_total_revenue(),
            "average_order_value": self.calculate_average_order_value(),
            "conversion_rate": self.calculate_conversion_rate(),
            "total_transactions": len(self.transactions),
            "total_sessions": len(self.sessions)
        }
    
    def get_time_series_data(self, period: str = 'D') -> pd.DataFrame:
        """Données temporelles pour graphiques d'évolution"""
        # Revenus par jour/semaine/mois
        revenue_ts = self.transactions.groupby(
            self.transactions['date'].dt.to_period(period)
        )['amount'].sum().reset_index()
        revenue_ts['date'] = revenue_ts['date'].dt.to_timestamp()
        
        # Sessions par période
        sessions_ts = self.sessions.groupby(
            self.sessions['date'].dt.to_period(period)
        ).size().reset_index(name='sessions')
        sessions_ts['date'] = sessions_ts['date'].dt.to_timestamp()
        
        # Conversion par période
        conversion_ts = self.sessions.groupby(
            self.sessions['date'].dt.to_period(period)
        )['converted'].agg(['sum', 'count']).reset_index()
        conversion_ts['date'] = conversion_ts['date'].dt.to_timestamp()
        conversion_ts['conversion_rate'] = (conversion_ts['sum'] / conversion_ts['count']) * 100
        
        # Merge des données
        time_data = revenue_ts.merge(sessions_ts, on='date', how='outer')
        time_data = time_data.merge(conversion_ts[['date', 'conversion_rate']], on='date', how='outer')
        time_data = time_data.fillna(0).sort_values('date')
        
        return time_data
    
    def get_conversion_by_source(self) -> pd.DataFrame:
        """Taux de conversion par source"""
        conversion_by_source = self.sessions.groupby('source')['converted'].agg([
            'sum', 'count'
        ]).reset_index()
        conversion_by_source['conversion_rate'] = (
            conversion_by_source['sum'] / conversion_by_source['count']
        ) * 100
        conversion_by_source = conversion_by_source.sort_values('conversion_rate', ascending=False)
        return conversion_by_source
    
    def format_metric(self, value: float, metric_type: str) -> str:
        """Formate une métrique selon son type"""
        format_str = METRIC_FORMATS.get(metric_type, "{:.2f}")
        return format_str.format(value)