"""Classe de base pour les scrapers avec Botasaurus."""

from botasaurus import *
from typing import List, Dict, Optional
import time
import random
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import SCRAPING_CONFIG


class BaseScraper:
    """Classe de base pour tous les scrapers."""
    
    def __init__(self):
        self.config = SCRAPING_CONFIG
        self.reviews = []
    
    def random_delay(self):
        """Délai aléatoire entre les requêtes."""
        delay = random.uniform(*self.config["delay_range"])
        time.sleep(delay)
    
    def clean_text(self, text: str) -> str:
        """Nettoyer le texte des avis."""
        if not text:
            return ""
        
        # Supprimer les espaces multiples
        text = " ".join(text.split())
        
        # Supprimer les caractères spéciaux problématiques
        text = text.replace("\n", " ").replace("\r", " ")
        text = text.replace("\t", " ").strip()
        
        return text
    
    def extract_rating(self, rating_element) -> Optional[float]:
        """Extraire la note d'un élément."""
        if not rating_element:
            return None
        
        try:
            # Chercher différents formats de notation
            rating_text = rating_element.get_text() if hasattr(rating_element, 'get_text') else str(rating_element)
            
            # Format "4.5 out of 5" ou "4,5/5"
            import re
            rating_match = re.search(r'(\d+[.,]\d+|\d+)', rating_text)
            if rating_match:
                rating = float(rating_match.group(1).replace(',', '.'))
                return min(rating, 5.0)  # Limiter à 5
                
        except (ValueError, AttributeError):
            pass
        
        return None
    
    def create_review_dict(self, title: str, text: str, rating: float, 
                          date: str, author: str, platform: str, 
                          product_id: str = None) -> Dict:
        """Créer un dictionnaire standardisé pour un avis."""
        return {
            "title": self.clean_text(title) if title else "",
            "text": self.clean_text(text),
            "rating": rating,
            "date": date,
            "author": self.clean_text(author) if author else "Anonymous",
            "platform": platform,
            "product_id": product_id,
            "scraped_at": datetime.now().isoformat(),
            "text_length": len(self.clean_text(text)) if text else 0
        }
    
    def validate_review(self, review: Dict) -> bool:
        """Valider qu'un avis est complet et valide."""
        required_fields = ["text", "rating", "platform"]
        
        for field in required_fields:
            if field not in review or not review[field]:
                return False
        
        # Vérifier la longueur du texte
        if len(review["text"]) < 10:
            return False
        
        # Vérifier la note
        if not (0 <= review["rating"] <= 5):
            return False
        
        return True
    
    def save_reviews(self, reviews: List[Dict], filename: str = None):
        """Sauvegarder les avis dans un fichier JSON."""
        import json
        from pathlib import Path
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reviews_{timestamp}.json"
        
        filepath = Path("data") / filename
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {len(reviews)} avis sauvegardés dans {filepath}")
        return filepath