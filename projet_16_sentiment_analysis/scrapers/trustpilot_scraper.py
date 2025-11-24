"""Scraper Trustpilot avec Botasaurus."""

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
def scrape_trustpilot_reviews(driver: AntiDetectDriver, data):
    """Scraper principal pour Trustpilot avec Botasaurus."""
    
    company_url = data["url"]
    max_pages = data.get("max_pages", 3)
    
    # S'assurer que l'URL est correcte
    if not company_url.startswith("https://www.trustpilot.com/review/"):
        if "trustpilot.com" in company_url:
            company_url = company_url
        else:
            company_url = f"https://www.trustpilot.com/review/{company_url}"
    
    driver.get(company_url)
    driver.wait(3)
    
    all_reviews = []
    
    for page in range(max_pages):
        print(f"📄 Scraping Trustpilot page {page + 1}/{max_pages}")
        
        # Attendre que les avis se chargent
        driver.wait_for_element('[data-service-review-card-paper]', timeout=10)
        
        # Extraire les avis de la page actuelle
        reviews = driver.select_all('[data-service-review-card-paper]')
        
        for review in reviews:
            try:
                # Titre de l'avis
                title_elem = review.select('[data-service-review-title-typography]')
                title = title_elem.text if title_elem else ""
                
                # Texte de l'avis
                text_elem = review.select('[data-service-review-text-typography]')
                text = text_elem.text if text_elem else ""
                
                # Note (étoiles) - Trustpilot utilise des images d'étoiles
                rating_elem = review.select('[data-service-review-rating]')
                rating = 0
                if rating_elem:
                    # Chercher dans les attributs ou classes
                    rating_attr = rating_elem.get_attribute("data-service-review-rating")
                    if rating_attr:
                        rating = int(rating_attr)
                    else:
                        # Alternative: compter les étoiles pleines
                        stars = review.select_all('[name="star-full"]')
                        rating = len(stars)
                
                # Date
                date_elem = review.select('[data-service-review-date-time-ago]')
                date = date_elem.text if date_elem else ""
                
                # Auteur
                author_elem = review.select('[data-consumer-name-typography]')
                author = author_elem.text if author_elem else "Anonymous"
                
                # Créer l'objet avis
                review_data = {
                    "title": title.strip(),
                    "text": text.strip(),
                    "rating": rating,
                    "date": date.strip(),
                    "author": author.strip(),
                    "platform": "trustpilot",
                    "company_url": company_url,
                    "scraped_at": datetime.now().isoformat()
                }
                
                # Valider et ajouter
                if review_data["text"] and len(review_data["text"]) > 10:
                    all_reviews.append(review_data)
                    
            except Exception as e:
                print(f"❌ Erreur lors de l'extraction d'un avis Trustpilot: {e}")
                continue
        
        # Aller à la page suivante
        if page < max_pages - 1:
            try:
                # Trustpilot utilise différents sélecteurs pour la pagination
                next_button = driver.select('[data-pagination-button-next]')
                if not next_button:
                    next_button = driver.select('a[name="pagination-button-next"]')
                
                if next_button and not next_button.get_attribute("disabled"):
                    driver.click(next_button)
                    driver.wait(3)
                else:
                    print("🔚 Pas de page suivante trouvée")
                    break
            except:
                print("🔚 Impossible d'aller à la page suivante")
                break
    
    return all_reviews


class TrustpilotScraper(BaseScraper):
    """Scraper spécialisé pour Trustpilot."""
    
    def __init__(self):
        super().__init__()
        self.platform = "trustpilot"
    
    def scrape_company_reviews(self, company_url: str, max_pages: int = 3) -> List[Dict]:
        """Scraper les avis d'une entreprise sur Trustpilot."""
        
        print(f"🏢 Scraping Trustpilot: {company_url}")
        
        # Utiliser Botasaurus pour scraper
        data = {
            "url": company_url,
            "max_pages": max_pages
        }
        
        try:
            reviews = scrape_trustpilot_reviews(data)
            
            # Nettoyer et valider les avis
            valid_reviews = []
            for review in reviews:
                if self.validate_review(review):
                    valid_reviews.append(review)
            
            print(f"✅ {len(valid_reviews)} avis valides extraits")
            return valid_reviews
            
        except Exception as e:
            print(f"❌ Erreur lors du scraping Trustpilot: {e}")
            return []
    
    def validate_review(self, review: Dict) -> bool:
        """Validation spécifique Trustpilot."""
        if not super().validate_review(review):
            return False
        
        # Vérifications spécifiques Trustpilot
        if review["rating"] < 1 or review["rating"] > 5:
            return False
        
        return True


# Test du scraper
if __name__ == "__main__":
    scraper = TrustpilotScraper()
    
    # URL d'exemple (remplacer par une vraie URL)
    test_url = "https://www.trustpilot.com/review/amazon.com"
    
    reviews = scraper.scrape_company_reviews(test_url, max_pages=2)
    
    if reviews:
        scraper.save_reviews(reviews, "trustpilot_test_reviews.json")
        print(f"📊 Premier avis: {reviews[0]}")
    else:
        print("❌ Aucun avis extrait")