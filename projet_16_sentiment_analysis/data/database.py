"""Base de données pour stocker les avis et analyses."""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DATABASE_PATH


class ReviewDatabase:
    """Gestionnaire de base de données pour les avis."""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or DATABASE_PATH
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialiser la base de données avec les tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    text TEXT NOT NULL,
                    rating INTEGER,
                    date TEXT,
                    author TEXT,
                    platform TEXT NOT NULL,
                    product_url TEXT,
                    company_url TEXT,
                    scraped_at TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sentiment_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    review_id INTEGER,
                    textblob_sentiment TEXT,
                    textblob_polarity REAL,
                    textblob_subjectivity REAL,
                    vader_sentiment TEXT,
                    vader_compound REAL,
                    vader_positive REAL,
                    vader_negative REAL,
                    vader_neutral REAL,
                    consensus_sentiment TEXT,
                    consensus_confidence REAL,
                    aspects TEXT,
                    analyzed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (review_id) REFERENCES reviews (id)
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_reviews_platform ON reviews(platform);
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
            """)
    
    def insert_review(self, review: Dict) -> int:
        """Insérer un avis dans la base."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO reviews (title, text, rating, date, author, platform, 
                                   product_url, company_url, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                review.get("title", ""),
                review.get("text", ""),
                review.get("rating"),
                review.get("date", ""),
                review.get("author", ""),
                review.get("platform", ""),
                review.get("product_url"),
                review.get("company_url"),
                review.get("scraped_at", datetime.now().isoformat())
            ))
            return cursor.lastrowid
    
    def insert_sentiment_analysis(self, review_id: int, analysis: Dict):
        """Insérer une analyse de sentiment."""
        with sqlite3.connect(self.db_path) as conn:
            textblob = analysis.get("textblob", {})
            vader = analysis.get("vader", {})
            consensus = analysis.get("consensus", {})
            aspects = analysis.get("aspects", {})
            
            conn.execute("""
                INSERT INTO sentiment_analysis (
                    review_id, textblob_sentiment, textblob_polarity, textblob_subjectivity,
                    vader_sentiment, vader_compound, vader_positive, vader_negative, vader_neutral,
                    consensus_sentiment, consensus_confidence, aspects
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                review_id,
                textblob.get("sentiment"),
                textblob.get("polarity"),
                textblob.get("subjectivity"),
                vader.get("sentiment"),
                vader.get("compound"),
                vader.get("positive"),
                vader.get("negative"),
                vader.get("neutral"),
                consensus.get("sentiment"),
                consensus.get("confidence"),
                json.dumps(aspects)
            ))
    
    def get_reviews(self, platform: str = None, limit: int = 100) -> List[Dict]:
        """Récupérer les avis avec filtres."""
        query = "SELECT * FROM reviews"
        params = []
        
        if platform:
            query += " WHERE platform = ?"
            params.append(platform)
        
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_sentiment_stats(self, platform: str = None) -> Dict:
        """Statistiques de sentiment."""
        query = """
            SELECT 
                sa.consensus_sentiment,
                COUNT(*) as count,
                AVG(r.rating) as avg_rating,
                AVG(sa.consensus_confidence) as avg_confidence
            FROM sentiment_analysis sa
            JOIN reviews r ON sa.review_id = r.id
        """
        params = []
        
        if platform:
            query += " WHERE r.platform = ?"
            params.append(platform)
        
        query += " GROUP BY sa.consensus_sentiment"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            results = cursor.fetchall()
            
            stats = {}
            total = sum(row["count"] for row in results)
            
            for row in results:
                sentiment = row["consensus_sentiment"]
                stats[sentiment] = {
                    "count": row["count"],
                    "percentage": (row["count"] / total * 100) if total > 0 else 0,
                    "avg_rating": row["avg_rating"],
                    "avg_confidence": row["avg_confidence"]
                }
            
            return stats
    
    def get_recent_reviews_with_sentiment(self, limit: int = 50) -> List[Dict]:
        """Récupérer les avis récents avec leur analyse."""
        query = """
            SELECT 
                r.*, 
                sa.consensus_sentiment,
                sa.consensus_confidence,
                sa.textblob_polarity,
                sa.vader_compound
            FROM reviews r
            LEFT JOIN sentiment_analysis sa ON r.id = sa.review_id
            ORDER BY r.created_at DESC
            LIMIT ?
        """
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, (limit,))
            return [dict(row) for row in cursor.fetchall()]


# Fonctions utilitaires
def save_reviews_to_db(reviews: List[Dict], analyses: List[Dict] = None):
    """Sauvegarder des avis et leurs analyses dans la DB."""
    db = ReviewDatabase()
    
    for i, review in enumerate(reviews):
        review_id = db.insert_review(review)
        
        if analyses and i < len(analyses):
            db.insert_sentiment_analysis(review_id, analyses[i])
    
    print(f"✅ {len(reviews)} avis sauvegardés dans la base de données")


if __name__ == "__main__":
    # Test de la base de données
    db = ReviewDatabase()
    
    # Avis de test
    test_review = {
        "title": "Great product!",
        "text": "This is an amazing product with excellent quality.",
        "rating": 5,
        "platform": "amazon",
        "author": "TestUser"
    }
    
    review_id = db.insert_review(test_review)
    print(f"✅ Avis inséré avec ID: {review_id}")
    
    # Récupérer les avis
    reviews = db.get_reviews(limit=5)
    print(f"📊 {len(reviews)} avis récupérés")
    
    for review in reviews:
        print(f"- {review['platform']}: {review['text'][:50]}...")