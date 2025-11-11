"""Client pour l'API Reddit."""

import praw
import json
from datetime import datetime
from typing import List, Dict, Optional
from src.utils.config import Config


class RedditClient:
    """Client pour interagir avec l'API Reddit."""
    
    def __init__(self):
        """Initialiser le client Reddit avec les credentials."""
        if not all([Config.REDDIT_CLIENT_ID, Config.REDDIT_CLIENT_SECRET]):
            raise ValueError("Credentials Reddit manquants dans .env")
        
        self.reddit = praw.Reddit(
            client_id=Config.REDDIT_CLIENT_ID,
            client_secret=Config.REDDIT_CLIENT_SECRET,
            user_agent=Config.REDDIT_USER_AGENT
        )
    
    def search_subreddit(
        self,
        subreddit_name: str,
        query: Optional[str] = None,
        limit: int = 100,
        time_filter: str = "week",
        save_raw: bool = True
    ) -> List[Dict]:
        """
        Rechercher des posts dans un subreddit.
        
        Args:
            subreddit_name: Nom du subreddit (ex: "python")
            query: Terme de recherche optionnel
            limit: Nombre maximum de posts
            time_filter: Filtre temporel (hour, day, week, month, year, all)
            save_raw: Sauvegarder les données brutes
            
        Returns:
            Liste de dictionnaires contenant les posts
        """
        posts_data = []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Recherche ou top posts
            if query:
                submissions = subreddit.search(query, limit=limit, time_filter=time_filter)
            else:
                submissions = subreddit.hot(limit=limit)
            
            for post in submissions:
                post_dict = {
                    'id': post.id,
                    'title': post.title,
                    'text': post.selftext,
                    'author': str(post.author),
                    'created_utc': datetime.fromtimestamp(post.created_utc).isoformat(),
                    'score': post.score,
                    'upvote_ratio': post.upvote_ratio,
                    'num_comments': post.num_comments,
                    'url': post.url,
                    'subreddit': subreddit_name
                }
                posts_data.append(post_dict)
            
            print(f"✅ {len(posts_data)} posts collectés depuis r/{subreddit_name}")
            
            if save_raw:
                self._save_raw_data(posts_data, subreddit_name, query)
            
            return posts_data
            
        except Exception as e:
            print(f"❌ Erreur Reddit API: {e}")
            return []
    
    def _save_raw_data(self, data: List[Dict], subreddit: str, query: Optional[str]):
        """Sauvegarder les données brutes en JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_part = f"_{query.replace(' ', '_')}" if query else ""
        filename = f"reddit_{subreddit}{query_part}_{timestamp}.json"
        filepath = Config.RAW_DATA_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Données sauvegardées: {filepath}")
