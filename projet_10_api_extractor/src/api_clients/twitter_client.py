"""Client pour l'API Twitter/X."""

import tweepy
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from src.utils.config import Config


class TwitterClient:
    """Client pour interagir avec l'API Twitter/X."""
    
    def __init__(self):
        """Initialiser le client Twitter avec les credentials."""
        if not Config.TWITTER_BEARER_TOKEN:
            raise ValueError("TWITTER_BEARER_TOKEN manquant dans .env")
        
        self.client = tweepy.Client(bearer_token=Config.TWITTER_BEARER_TOKEN)
        
    def search_tweets(
        self, 
        query: str, 
        max_results: int = 100,
        save_raw: bool = True
    ) -> List[Dict]:
        """
        Rechercher des tweets selon une requête.
        
        Args:
            query: Requête de recherche (ex: "python programming")
            max_results: Nombre maximum de résultats (10-100 par requête)
            save_raw: Sauvegarder les données brutes en JSON
            
        Returns:
            Liste de dictionnaires contenant les tweets
        """
        tweets_data = []
        
        try:
            # Limiter max_results à 100 (limite de l'API)
            max_results = min(max_results, 100)
            
            # Recherche avec des champs supplémentaires
            response = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['created_at', 'author_id', 'public_metrics', 'lang'],
                expansions=['author_id'],
                user_fields=['username', 'name', 'verified']
            )
            
            if not response.data:
                print(f"Aucun tweet trouvé pour: {query}")
                return []
            
            # Créer un mapping des auteurs
            users = {user.id: user for user in response.includes.get('users', [])}
            
            # Extraire les données pertinentes
            for tweet in response.data:
                author = users.get(tweet.author_id, {})
                
                tweet_dict = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at.isoformat() if tweet.created_at else None,
                    'author_id': tweet.author_id,
                    'author_username': getattr(author, 'username', None),
                    'author_name': getattr(author, 'name', None),
                    'likes': tweet.public_metrics.get('like_count', 0),
                    'retweets': tweet.public_metrics.get('retweet_count', 0),
                    'replies': tweet.public_metrics.get('reply_count', 0),
                    'lang': tweet.lang
                }
                tweets_data.append(tweet_dict)
            
            print(f"✅ {len(tweets_data)} tweets collectés pour '{query}'")
            
            # Sauvegarder les données brutes
            if save_raw:
                self._save_raw_data(tweets_data, query)
            
            return tweets_data
            
        except tweepy.TweepyException as e:
            print(f"❌ Erreur Twitter API: {e}")
            return []
    
    def _save_raw_data(self, data: List[Dict], query: str):
        """Sauvegarder les données brutes en JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"twitter_{query.replace(' ', '_')}_{timestamp}.json"
        filepath = Config.RAW_DATA_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Données sauvegardées: {filepath}")
