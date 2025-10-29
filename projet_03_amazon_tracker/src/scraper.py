"""
Module de scraping Amazon
"""
import re
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import config


class AmazonScraper:
    """Scraper pour extraire les informations des produits Amazon"""
    
    def __init__(self):
        """Initialise le scraper"""
        self.ua = UserAgent()
        self.session = requests.Session()
    
    def _get_headers(self):
        """
        Génère des headers HTTP aléatoires
        
        Returns:
            Dict avec les headers
        """
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
    
    def _make_request(self, url, retries=config.MAX_RETRIES):
        """
        Effectue une requête HTTP avec retry logic
        
        Args:
            url: URL à scraper
            retries: Nombre de tentatives
            
        Returns:
            Response object ou None
        """
        for attempt in range(retries):
            try:
                time.sleep(config.REQUEST_DELAY)  # Délai entre requêtes
                
                response = self.session.get(
                    url,
                    headers=self._get_headers(),
                    timeout=config.REQUEST_TIMEOUT
                )
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 503:
                    # Service temporairement indisponible, réessayer
                    wait_time = (attempt + 1) * 2
                    print(f"Service indisponible, attente {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"Erreur HTTP {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"Timeout (tentative {attempt + 1}/{retries})")
            except requests.exceptions.RequestException as e:
                print(f"Erreur de requête: {e}")
        
        return None
    
    def _extract_asin(self, url):
        """
        Extrait l'ASIN depuis l'URL Amazon
        
        Args:
            url: URL du produit
            
        Returns:
            ASIN ou None
        """
        # Pattern: /dp/ASIN/ ou /product/ASIN/
        match = re.search(r'/(?:dp|product)/([A-Z0-9]{10})', url)
        if match:
            return match.group(1)
        return None
    
    def _extract_price(self, soup):
        """
        Extrait le prix depuis le HTML
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Prix (float) ou None
        """
        for selector in config.PRICE_SELECTORS:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                # Nettoyer et parser le prix
                price = self._parse_price(price_text)
                if price:
                    return price
        
        return None
    
    def _parse_price(self, price_text):
        """
        Parse une chaîne de prix en float
        
        Args:
            price_text: Texte contenant le prix
            
        Returns:
            Prix (float) ou None
        """
        # Patterns possibles: "49,99", "49.99", "49,99 €", "€49.99"
        match = re.search(r'(\d+)[,.](\d{2})', price_text)
        if match:
            try:
                return float(f"{match.group(1)}.{match.group(2)}")
            except ValueError:
                pass
        return None
    
    def _extract_name(self, soup):
        """
        Extrait le nom du produit
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Nom du produit ou None
        """
        for selector in config.NAME_SELECTORS:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None
    
    def _extract_image(self, soup):
        """
        Extrait l'URL de l'image du produit
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            URL de l'image ou None
        """
        for selector in config.IMAGE_SELECTORS:
            element = soup.select_one(selector)
            if element:
                # Essayer plusieurs attributs
                for attr in ['data-old-hires', 'data-a-dynamic-image', 'src']:
                    img_url = element.get(attr)
                    if img_url:
                        # Pour data-a-dynamic-image, c'est un JSON
                        if attr == 'data-a-dynamic-image':
                            try:
                                import json
                                images = json.loads(img_url)
                                return list(images.keys())[0]
                            except:
                                pass
                        else:
                            return img_url
        return None
    
    def _extract_availability(self, soup):
        """
        Extrait la disponibilité du produit
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            String de disponibilité
        """
        for selector in config.AVAILABILITY_SELECTORS:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if 'stock' in text.lower() or 'disponible' in text.lower():
                    return 'In Stock'
                elif 'indisponible' in text.lower():
                    return 'Out of Stock'
        
        return 'Unknown'
    
    def scrape_product(self, url):
        """
        Scrape toutes les informations d'un produit Amazon
        
        Args:
            url: URL du produit
            
        Returns:
            Dict avec les infos ou None si erreur
        """
        print(f"🔍 Scraping: {url[:60]}...")
        
        response = self._make_request(url)
        if not response:
            print("❌ Impossible de récupérer la page")
            return None
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Extraire les informations
        asin = self._extract_asin(url)
        name = self._extract_name(soup)
        price = self._extract_price(soup)
        image_url = self._extract_image(soup)
        availability = self._extract_availability(soup)
        
        # Vérifier que les infos essentielles sont présentes
        if not name or not price:
            print("❌ Impossible d'extraire le nom ou le prix")
            return None
        
        product_data = {
            'url': url,
            'asin': asin,
            'name': name,
            'price': price,
            'image_url': image_url,
            'availability': availability
        }
        
        print(f"✅ Produit trouvé: {name} - {price}€")
        
        return product_data
    
    def validate_url(self, url):
        """
        Valide qu'une URL est bien une URL Amazon
        
        Args:
            url: URL à valider
            
        Returns:
            True si valide, False sinon
        """
        domain = config.AMAZON_DOMAIN
        return domain in url.lower() and ('/dp/' in url or '/product/' in url)
