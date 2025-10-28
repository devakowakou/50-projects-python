"""
Analyseur de budget - Calculs et statistiques
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import calendar

class BudgetAnalyzer:
    def __init__(self, df: pd.DataFrame):
        """
        Initialise l'analyseur avec un DataFrame de transactions
        """
        self.df = df.copy() if not df.empty else pd.DataFrame()
        
        if not self.df.empty and 'date' in self.df.columns:
            self.df['date'] = pd.to_datetime(self.df['date'])
            self.df['montant'] = pd.to_numeric(self.df['montant'], errors='coerce')
    
    def get_summary_metrics(self) -> Dict:
        """
        Calcule les métriques principales du budget
        Returns: Dict avec solde, revenus, dépenses, économies
        """
        if self.df.empty:
            return {
                'solde': 0.0,
                'revenus': 0.0,
                'depenses': 0.0,
                'economies': 0.0,
                'taux_epargne': 0.0
            }
        
        revenus = self.df[self.df['type'] == 'revenu']['montant'].sum()
        depenses = self.df[self.df['type'] == 'depense']['montant'].sum()
        solde = revenus - depenses
        economies = revenus - depenses
        taux_epargne = (economies / revenus * 100) if revenus > 0 else 0
        
        return {
            'solde': round(solde, 2),
            'revenus': round(revenus, 2),
            'depenses': round(depenses, 2),
            'economies': round(economies, 2),
            'taux_epargne': round(taux_epargne, 1)
        }
    
    def get_monthly_summary(self, year: int = None, month: int = None) -> Dict:
        """
        Résumé pour un mois spécifique
        Si year/month non fournis, utilise le mois actuel
        """
        if self.df.empty:
            return self.get_summary_metrics()
        
        if year is None or month is None:
            today = datetime.now()
            year = today.year
            month = today.month
        
        # Filtrer par mois
        df_month = self.df[
            (self.df['date'].dt.year == year) & 
            (self.df['date'].dt.month == month)
        ]
        
        if df_month.empty:
            return self.get_summary_metrics()
        
        analyzer = BudgetAnalyzer(df_month)
        return analyzer.get_summary_metrics()
    
    def get_spending_by_category(self) -> pd.DataFrame:
        """
        Dépenses regroupées par catégorie
        Returns: DataFrame avec catégorie, montant, pourcentage
        """
        if self.df.empty:
            return pd.DataFrame()
        
        df_depenses = self.df[self.df['type'] == 'depense'].copy()
        
        if df_depenses.empty:
            return pd.DataFrame()
        
        category_spending = df_depenses.groupby('categorie')['montant'].sum().reset_index()
        category_spending.columns = ['Catégorie', 'Montant']
        
        total = category_spending['Montant'].sum()
        category_spending['Pourcentage'] = (category_spending['Montant'] / total * 100).round(1)
        
        category_spending = category_spending.sort_values('Montant', ascending=False)
        
        return category_spending
    
    def get_income_by_category(self) -> pd.DataFrame:
        """
        Revenus regroupés par catégorie
        Returns: DataFrame avec catégorie, montant, pourcentage
        """
        if self.df.empty:
            return pd.DataFrame()
        
        df_revenus = self.df[self.df['type'] == 'revenu'].copy()
        
        if df_revenus.empty:
            return pd.DataFrame()
        
        category_income = df_revenus.groupby('categorie')['montant'].sum().reset_index()
        category_income.columns = ['Catégorie', 'Montant']
        
        total = category_income['Montant'].sum()
        category_income['Pourcentage'] = (category_income['Montant'] / total * 100).round(1)
        
        category_income = category_income.sort_values('Montant', ascending=False)
        
        return category_income
    
    def get_daily_trend(self) -> pd.DataFrame:
        """
        Tendance journalière (revenus et dépenses cumulés)
        """
        if self.df.empty:
            return pd.DataFrame()
        
        df_sorted = self.df.sort_values('date')
        
        # Créer des séries pour revenus et dépenses
        df_revenus = df_sorted[df_sorted['type'] == 'revenu'][['date', 'montant']].copy()
        df_depenses = df_sorted[df_sorted['type'] == 'depense'][['date', 'montant']].copy()
        
        df_revenus = df_revenus.groupby('date')['montant'].sum().cumsum().reset_index()
        df_revenus.columns = ['Date', 'Revenus Cumulés']
        
        df_depenses = df_depenses.groupby('date')['montant'].sum().cumsum().reset_index()
        df_depenses.columns = ['Date', 'Dépenses Cumulées']
        
        # Merge et remplir les valeurs manquantes
        df_trend = pd.merge(df_revenus, df_depenses, on='Date', how='outer').ffill().fillna(0)
        df_trend['Solde'] = df_trend['Revenus Cumulés'] - df_trend['Dépenses Cumulées']
        
        return df_trend
    
    def get_budget_status(self, budgets: Dict[str, float]) -> pd.DataFrame:
        """
        État du budget par catégorie
        Args:
            budgets: Dict {categorie: budget_mensuel}
        Returns: DataFrame avec catégorie, dépensé, budget, restant, pourcentage
        """
        if self.df.empty:
            return pd.DataFrame()
        
        spending = self.get_spending_by_category()
        
        if spending.empty:
            return pd.DataFrame()
        
        status_data = []
        
        for categorie, budget in budgets.items():
            spent = spending[spending['Catégorie'] == categorie]['Montant'].sum()
            remaining = budget - spent
            percentage = (spent / budget * 100) if budget > 0 else 0
            
            status_data.append({
                'Catégorie': categorie,
                'Dépensé': round(spent, 2),
                'Budget': budget,
                'Restant': round(remaining, 2),
                'Pourcentage': round(percentage, 1)
            })
        
        df_status = pd.DataFrame(status_data)
        df_status = df_status.sort_values('Pourcentage', ascending=False)
        
        return df_status
    
    def get_alerts(self, budgets: Dict[str, float], warning_threshold: float = 80, 
                   danger_threshold: float = 100) -> List[Dict]:
        """
        Génère des alertes basées sur les budgets
        Args:
            budgets: Dict {categorie: budget_mensuel}
            warning_threshold: Seuil d'alerte warning (%)
            danger_threshold: Seuil d'alerte danger (%)
        Returns: Liste d'alertes
        """
        if self.df.empty:
            return []
        
        budget_status = self.get_budget_status(budgets)
        
        if budget_status.empty:
            return []
        
        alerts = []
        
        for _, row in budget_status.iterrows():
            percentage = row['Pourcentage']
            categorie = row['Catégorie']
            spent = row['Dépensé']
            budget = row['Budget']
            
            if percentage >= danger_threshold:
                alerts.append({
                    'level': 'danger',
                    'message': f"Budget dépassé pour {categorie}: {spent}€ / {budget}€ ({percentage}%)"
                })
            elif percentage >= warning_threshold:
                alerts.append({
                    'level': 'warning',
                    'message': f"Attention {categorie}: {spent}€ / {budget}€ ({percentage}%)"
                })
        
        return alerts
    
    def compare_periods(self, period1_df: pd.DataFrame, period2_df: pd.DataFrame) -> Dict:
        """
        Compare deux périodes (ex: mois actuel vs mois précédent)
        """
        analyzer1 = BudgetAnalyzer(period1_df)
        analyzer2 = BudgetAnalyzer(period2_df)
        
        metrics1 = analyzer1.get_summary_metrics()
        metrics2 = analyzer2.get_summary_metrics()
        
        comparison = {}
        for key in ['revenus', 'depenses', 'economies']:
            diff = metrics1[key] - metrics2[key]
            diff_pct = (diff / metrics2[key] * 100) if metrics2[key] > 0 else 0
            comparison[key] = {
                'current': metrics1[key],
                'previous': metrics2[key],
                'diff': round(diff, 2),
                'diff_pct': round(diff_pct, 1)
            }
        
        return comparison
    
    def get_top_transactions(self, n: int = 10, transaction_type: str = 'depense') -> pd.DataFrame:
        """
        Retourne les N plus grandes transactions d'un type
        """
        if self.df.empty:
            return pd.DataFrame()
        
        df_filtered = self.df[self.df['type'] == transaction_type].copy()
        df_top = df_filtered.nlargest(n, 'montant')
        
        return df_top[['date', 'categorie', 'description', 'montant']]
