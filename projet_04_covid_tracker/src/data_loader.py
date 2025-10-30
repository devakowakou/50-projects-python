"""
Module de chargement et mise en cache des données COVID-19
"""
import pandas as pd
import requests
from pathlib import Path
from datetime import datetime, timedelta
import config


class CovidDataLoader:
    """Gestionnaire de chargement des données COVID-19"""
    
    def __init__(self):
        """Initialise le loader"""
        self.data_path = Path(config.DATA_CACHE_PATH)
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _is_cache_valid(self):
        """
        Vérifie si le cache est encore valide
        
        Returns:
            bool: True si le cache est valide
        """
        if not self.data_path.exists():
            return False
        
        # Vérifier l'âge du fichier
        file_time = datetime.fromtimestamp(self.data_path.stat().st_mtime)
        expiry_time = datetime.now() - timedelta(hours=config.CACHE_EXPIRY_HOURS)
        
        return file_time > expiry_time
    
    def _download_data(self):
        """
        Télécharge les données depuis Our World in Data
        
        Returns:
            DataFrame ou None si erreur
        """
        try:
            print("📥 Téléchargement des données COVID-19...")
            
            # Télécharger le CSV
            df = pd.read_csv(
                config.COVID_DATA_URL,
                usecols=config.COLUMNS_TO_LOAD,
                parse_dates=['date'],
                dtype={'iso_code': 'object', 'continent': 'object', 'location': 'object'}
            )
            
            # Sauvegarder dans le cache
            df.to_csv(self.data_path, index=False)
            
            print(f"✅ Données téléchargées : {len(df)} lignes")
            return df
            
        except Exception as e:
            print(f"❌ Erreur lors du téléchargement : {e}")
            return None
    
    def _load_from_cache(self):
        """
        Charge les données depuis le cache local
        
        Returns:
            DataFrame ou None si erreur
        """
        try:
            print("📂 Chargement depuis le cache local...")
            df = pd.read_csv(self.data_path, parse_dates=['date'])
            print(f"✅ Données chargées : {len(df)} lignes")
            return df
        except Exception as e:
            print(f"❌ Erreur lors du chargement du cache : {e}")
            return None
    
    def load_data(self, force_refresh=False):
        """
        Charge les données COVID-19 (cache ou téléchargement)
        
        Args:
            force_refresh: Forcer le téléchargement même si cache valide
            
        Returns:
            DataFrame avec les données COVID
        """
        # Si force refresh ou cache invalide, télécharger
        if force_refresh or not self._is_cache_valid():
            df = self._download_data()
            if df is None:
                # Si téléchargement échoue, essayer le cache
                print("⚠️ Tentative de chargement depuis le cache...")
                df = self._load_from_cache()
        else:
            # Cache valide, charger depuis le cache
            df = self._load_from_cache()
        
        if df is None:
            raise Exception("Impossible de charger les données COVID-19")
        
        # Nettoyage basique
        df = self._clean_data(df)
        
        return df
    
    def _clean_data(self, df):
        """
        Nettoie et prépare les données
        
        Args:
            df: DataFrame brut
            
        Returns:
            DataFrame nettoyé
        """
        # Supprimer les lignes sans pays
        df = df.dropna(subset=['location'])
        
        # Convertir la date en datetime si ce n'est pas déjà fait
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            df['date'] = pd.to_datetime(df['date'])
        
        # Trier par pays et date
        df = df.sort_values(['location', 'date'])
        
        # Remplir les valeurs manquantes pour les colonnes numériques
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)
        
        return df
    
    def get_available_countries(self, df):
        """
        Récupère la liste des pays disponibles
        
        Args:
            df: DataFrame des données COVID
            
        Returns:
            Liste triée des pays
        """
        return sorted(df['location'].unique().tolist())
    
    def get_country_data(self, df, country):
        """
        Récupère les données pour un pays spécifique
        
        Args:
            df: DataFrame des données COVID
            country: Nom du pays
            
        Returns:
            DataFrame filtré pour ce pays
        """
        return df[df['location'] == country].copy()
    
    def get_date_range(self, df):
        """
        Récupère la plage de dates disponible
        
        Args:
            df: DataFrame des données COVID
            
        Returns:
            Tuple (date_min, date_max)
        """
        return df['date'].min(), df['date'].max()
