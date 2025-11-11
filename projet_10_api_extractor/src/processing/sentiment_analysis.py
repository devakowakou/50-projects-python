"""Analyse de sentiment sur les textes collectés."""

import pandas as pd
from textblob import TextBlob
from typing import Tuple


class SentimentAnalyzer:
    """Classe pour analyser le sentiment des textes."""
    
    @staticmethod
    def analyze_sentiment(text: str) -> Tuple[float, str]:
        """
        Analyser le sentiment d'un texte.
        
        Args:
            text: Texte à analyser
            
        Returns:
            Tuple (polarité, catégorie)
            - polarité: score entre -1 (négatif) et 1 (positif)
            - catégorie: 'positive', 'neutral', 'negative'
        """
        if not isinstance(text, str) or not text.strip():
            return 0.0, 'neutral'
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        # Catégoriser
        if polarity > 0.1:
            category = 'positive'
        elif polarity < -0.1:
            category = 'negative'
        else:
            category = 'neutral'
        
        return polarity, category
    
    @staticmethod
    def add_sentiment_to_df(df: pd.DataFrame, text_column: str = 'text_clean') -> pd.DataFrame:
        """
        Ajouter les colonnes de sentiment à un DataFrame.
        
        Args:
            df: DataFrame avec les textes
            text_column: Nom de la colonne contenant le texte
            
        Returns:
            DataFrame avec colonnes sentiment ajoutées
        """
        if text_column not in df.columns:
            print(f"⚠️ Colonne '{text_column}' introuvable")
            return df
        
        # Analyser le sentiment
        results = df[text_column].apply(SentimentAnalyzer.analyze_sentiment)
        
        df['sentiment_score'] = results.apply(lambda x: x[0])
        df['sentiment_category'] = results.apply(lambda x: x[1])
        
        return df
    
    @staticmethod
    def get_sentiment_stats(df: pd.DataFrame) -> dict:
        """
        Obtenir des statistiques sur le sentiment.
        
        Args:
            df: DataFrame avec colonnes sentiment
            
        Returns:
            Dictionnaire de statistiques
        """
        if 'sentiment_category' not in df.columns:
            return {}
        
        counts = df['sentiment_category'].value_counts()
        total = len(df)
        
        stats = {
            'total': total,
            'positive': counts.get('positive', 0),
            'neutral': counts.get('neutral', 0),
            'negative': counts.get('negative', 0),
            'positive_pct': round(counts.get('positive', 0) / total * 100, 2),
            'neutral_pct': round(counts.get('neutral', 0) / total * 100, 2),
            'negative_pct': round(counts.get('negative', 0) / total * 100, 2),
            'avg_score': round(df['sentiment_score'].mean(), 3)
        }
        
        return stats
