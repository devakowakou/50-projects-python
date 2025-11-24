"""Scraper Amazon avec Botasaurus."""

from botasaurus import *
from typing import List, Dict
import re
from datetime import datetime
from .base_scraper import BaseScraper


@browser(
    headless=True,
    block_images=True,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)
def scrape_amazon_reviews(driver: AntiDetectDriver, data):
    """Scraper principal pour Amazon avec Botasaurus."""
    
    product_url = data["url"]
    max_pages = data.get("max_pages", 3)
    
    # Aller à la page des avis
    if "/dp/" in product_url:
        # Extraire l'ASIN du produit
        asin_match = re.search(r'/dp/([A-Z0-9]{10})', product_url)
        if asin_match:
            asin = asin_match.group(1)
            reviews_url = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm"
        else:
            reviews_url = product_url
    else:
        reviews_url = product_url
    
    driver.get(reviews_url)
    driver.wait(2)
    
    all_reviews = []
    
    for page in range(max_pages):
        print(f"📄 Scraping page {page + 1}/{max_pages}")
        
        # Attendre que les avis se chargent
        driver.wait_for_element('[data-hook="review"]', timeout=10)
        
        # Extraire les avis de la page actuelle
        reviews = driver.select_all('[data-hook="review"]')
        
        for review in reviews:
            try:
                # Titre de l'avis
                title_elem = review.select('[data-hook="review-title"]')
                title = title_elem.text if title_elem else ""
                
                # Texte de l'avis
                text_elem = review.select('[data-hook="review-body"]')
                text = text_elem.text if text_elem else ""
                
                # Note (étoiles)
                rating_elem = review.select('[data-hook="review-star-rating"]')
                rating = 0
                if rating_elem:
                    rating_text = rating_elem.get_attribute("class") or ""
                    rating_match = re.search(r'a-star-(\d)', rating_text)
                    if rating_match:
                        rating = int(rating_match.group(1))
                
                # Date
                date_elem = review.select('[data-hook="review-date"]')
                date = date_elem.text if date_elem else ""
                
                # Auteur
                author_elem = review.select('[class*="author"]')
                author = author_elem.text if author_elem else "Anonymous"
                
                # Créer l'objet avis
                review_data = {
                    "title": title.strip(),
                    "text": text.strip(),
                    "rating": rating,
                    "date": date.strip(),
                    "author": author.strip(),
                    "platform": "amazon",
                    "product_url": product_url,
                    "scraped_at": datetime.now().isoformat()
                }
                
                # Valider et ajouter
                if review_data["text"] and len(review_data["text"]) > 10:
                    all_reviews.append(review_data)
                    
            except Exception as e:
                print(f"❌ Erreur lors de l'extraction d'un avis: {e}")
                continue
        
        # Aller à la page suivante
        if page < max_pages - 1:
            try:
                next_button = driver.select('[data-hook="pagination-bar"] .a-last a')
                if next_button:
                    driver.click(next_button)
                    driver.wait(3)
                else:
                    print("🔚 Pas de page suivante trouvée")
                    break
            except:
                print("🔚 Impossible d'aller à la page suivante")
                break
    
    return all_reviews


class AmazonScraper(BaseScraper):
    """Scraper spécialisé pour Amazon."""
    
    def __init__(self):
        super().__init__()
        self.platform = "amazon"
    
    def scrape_product_reviews(self, product_url: str, max_pages: int = 3) -> List[Dict]:
        """Scraper les avis d'un produit Amazon."""
        
        print(f"🛒 Scraping Amazon: {product_url}")
        
        # Utiliser Botasaurus pour scraper
        data = {
            "url": product_url,
            "max_pages": max_pages
        }
        
        try:
            reviews = scrape_amazon_reviews(data)
            
            # Nettoyer et valider les avis
            valid_reviews = []
            for review in reviews:
                if self.validate_review(review):
                    valid_reviews.append(review)
            
            print(f"✅ {len(valid_reviews)} avis valides extraits")
            return valid_reviews
            
        except Exception as e:
            print(f"❌ Erreur lors du scraping Amazon: {e}")
            return []
    
    def validate_review(self, review: Dict) -> bool:
        """Validation spécifique Amazon."""
        if not super().validate_review(review):
            return False
        
        # Vérifications spécifiques Amazon
        if review["rating"] < 1 or review["rating"] > 5:
            return False
        
        return True


# Test du scraper
if __name__ == "__main__":
    scraper = AmazonScraper()
    
    # URL d'exemple (remplacer par une vraie URL)
    test_url = "https://www.amazon.com/dp/B08N5WRWNW"  # Echo Dot exemple
    
    reviews = scraper.scrape_product_reviews(test_url, max_pages=2)
    
    if reviews:
        scraper.save_reviews(reviews, "amazon_test_reviews.json")
        print(f"📊 Premier avis: {reviews[0]}")
    else:
        print("❌ Aucun avis extrait")