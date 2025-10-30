"""
Module d'analyse des données COVID-19
"""
import pandas as pd
import numpy as np
import config


class CovidAnalyzer:
    """Analyseur de données COVID-19"""
    
    @staticmethod
    def calculate_metrics(df):
        """
        Calcule les métriques clés pour un pays
        
        Args:
            df: DataFrame des données d'un pays
            
        Returns:
            Dict avec les métriques
        """
        if df.empty:
            return None
        
        latest = df.iloc[-1]
        
        metrics = {
            'total_cases': int(latest['total_cases']) if pd.notna(latest['total_cases']) else 0,
            'total_deaths': int(latest['total_deaths']) if pd.notna(latest['total_deaths']) else 0,
            'total_vaccinations': int(latest['total_vaccinations']) if pd.notna(latest['total_vaccinations']) else 0,
            'people_vaccinated': int(latest['people_vaccinated']) if pd.notna(latest['people_vaccinated']) else 0,
            'people_fully_vaccinated': int(latest['people_fully_vaccinated']) if pd.notna(latest['people_fully_vaccinated']) else 0,
            'population': int(latest['population']) if pd.notna(latest['population']) else 0,
        }
        
        # Calculs dérivés
        if metrics['population'] > 0:
            metrics['cases_per_million'] = (metrics['total_cases'] / metrics['population']) * 1_000_000
            metrics['deaths_per_million'] = (metrics['total_deaths'] / metrics['population']) * 1_000_000
            metrics['vaccination_rate'] = (metrics['people_vaccinated'] / metrics['population']) * 100
        else:
            metrics['cases_per_million'] = 0
            metrics['deaths_per_million'] = 0
            metrics['vaccination_rate'] = 0
        
        # Taux de mortalité
        if metrics['total_cases'] > 0:
            metrics['mortality_rate'] = (metrics['total_deaths'] / metrics['total_cases']) * 100
        else:
            metrics['mortality_rate'] = 0
        
        # Dernière date de données
        metrics['last_update'] = latest['date'].strftime('%Y-%m-%d')
        
        return metrics
    
    @staticmethod
    def calculate_rolling_average(df, column, window=config.ROLLING_WINDOW):
        """
        Calcule la moyenne mobile
        
        Args:
            df: DataFrame
            column: Colonne à moyenner
            window: Fenêtre de calcul
            
        Returns:
            Series avec la moyenne mobile
        """
        return df[column].rolling(window=window, min_periods=1).mean()
    
    @staticmethod
    def calculate_daily_changes(df):
        """
        Calcule les variations quotidiennes
        
        Args:
            df: DataFrame d'un pays
            
        Returns:
            DataFrame avec colonnes de variation ajoutées
        """
        df = df.copy()
        
        # Variations quotidiennes
        df['new_cases_ma'] = CovidAnalyzer.calculate_rolling_average(df, 'new_cases')
        df['new_deaths_ma'] = CovidAnalyzer.calculate_rolling_average(df, 'new_deaths')
        
        return df
    
    @staticmethod
    def get_peak_info(df):
        """
        Trouve le pic de cas/décès
        
        Args:
            df: DataFrame d'un pays
            
        Returns:
            Dict avec infos sur les pics
        """
        if df.empty:
            return None
        
        peak_cases_idx = df['new_cases'].idxmax()
        peak_deaths_idx = df['new_deaths'].idxmax()
        
        return {
            'peak_cases_date': df.loc[peak_cases_idx, 'date'].strftime('%Y-%m-%d'),
            'peak_cases_value': int(df.loc[peak_cases_idx, 'new_cases']),
            'peak_deaths_date': df.loc[peak_deaths_idx, 'date'].strftime('%Y-%m-%d'),
            'peak_deaths_value': int(df.loc[peak_deaths_idx, 'new_deaths']),
        }
    
    @staticmethod
    def compare_countries(df, countries):
        """
        Compare les dernières données de plusieurs pays
        
        Args:
            df: DataFrame complet
            countries: Liste de pays à comparer
            
        Returns:
            DataFrame de comparaison
        """
        comparison = []
        
        for country in countries:
            country_df = df[df['location'] == country]
            if not country_df.empty:
                metrics = CovidAnalyzer.calculate_metrics(country_df)
                if metrics:
                    comparison.append({
                        'Pays': country,
                        'Cas totaux': metrics['total_cases'],
                        'Décès totaux': metrics['total_deaths'],
                        'Cas/Million': round(metrics['cases_per_million'], 2),
                        'Décès/Million': round(metrics['deaths_per_million'], 2),
                        'Taux vaccination (%)': round(metrics['vaccination_rate'], 2),
                        'Taux mortalité (%)': round(metrics['mortality_rate'], 2),
                    })
        
        return pd.DataFrame(comparison)
    
    @staticmethod
    def get_alert_level(cases_per_million):
        """
        Détermine le niveau d'alerte selon le nombre de cas
        
        Args:
            cases_per_million: Cas pour 1 million d'habitants
            
        Returns:
            Tuple (niveau, couleur)
        """
        if cases_per_million < config.ALERT_THRESHOLD_LOW:
            return ("Faible", "green")
        elif cases_per_million < config.ALERT_THRESHOLD_MEDIUM:
            return ("Modéré", "orange")
        elif cases_per_million < config.ALERT_THRESHOLD_HIGH:
            return ("Élevé", "red")
        else:
            return ("Très élevé", "darkred")
    
    @staticmethod
    def filter_by_date_range(df, start_date, end_date):
        """
        Filtre les données par plage de dates
        
        Args:
            df: DataFrame
            start_date: Date de début
            end_date: Date de fin
            
        Returns:
            DataFrame filtré
        """
        return df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()
