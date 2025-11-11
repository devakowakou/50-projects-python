"""Nettoyage et transformation des données collectées."""

import pandas as pd
import re
from typing import List, Dict


class DataCleaner:
    """Classe pour nettoyer et transformer les données."""
    
    @staticmethod
    def clean_twitter_data(tweets: List[Dict]) -> pd.DataFrame:
        """
        Nettoyer les données Twitter.
        
        Args:
            tweets: Liste de tweets bruts
            
        Returns:
            DataFrame nettoyé
        """
        if not tweets:
            return pd.DataFrame()
        
        df = pd.DataFrame(tweets)
        
        # Supprimer les doublons
        df = df.drop_duplicates(subset=['id'])
        
        # Nettoyer le texte
        df['text_clean'] = df['text'].apply(DataCleaner._clean_text)
        
        # Convertir les dates
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Calculer un score d'engagement
        df['engagement'] = df['likes'] + df['retweets'] * 2 + df['replies']
        
        return df
    
    @staticmethod
    def clean_reddit_data(posts: List[Dict]) -> pd.DataFrame:
        """
        Nettoyer les données Reddit.
        
        Args:
            posts: Liste de posts bruts
            
        Returns:
            DataFrame nettoyé
        """
        if not posts:
            return pd.DataFrame()
        
        df = pd.DataFrame(posts)
        
        # Supprimer les doublons
        df = df.drop_duplicates(subset=['id'])
        
        # Nettoyer le texte
        df['title_clean'] = df['title'].apply(DataCleaner._clean_text)
        df['text_clean'] = df['text'].apply(DataCleaner._clean_text)
        
        # Convertir les dates
        if 'created_utc' in df.columns:
            df['created_utc'] = pd.to_datetime(df['created_utc'])
        
        # Calculer un score d'engagement
        df['engagement'] = df['score'] + df['num_comments'] * 2
        
        return df
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Nettoyer un texte (URLs, mentions, hashtags, etc.).
        
        Args:
            text: Texte brut
            
        Returns:
            Texte nettoyé
        """
        if not isinstance(text, str):
            return ""
        
        # Supprimer les URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Supprimer les mentions (@username)
        text = re.sub(r'@\w+', '', text)
        
        # Supprimer les hashtags (optionnel)
        # text = re.sub(r'#\w+', '', text)
        
        # Supprimer les caractères spéciaux multiples
        text = re.sub(r'\s+', ' ', text)
        
        # Nettoyer les espaces
        text = text.strip()
        
        return text
