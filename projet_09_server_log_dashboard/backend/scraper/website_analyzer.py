import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import time
import logging

logger = logging.getLogger(__name__)

class WebsiteAnalyzer:
    """Analyse de sites web concurrents pour benchmarking"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def analyze_website(self, url: str) -> Dict:
        """
        Analyse complète d'un site web
        
        Returns:
            Métriques de performance et SEO
        """
        logger.info(f"🔍 Analyse de {url}...")
        
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            load_time = (time.time() - start_time) * 1000  # en ms
            
            if response.status_code != 200:
                return {
                    'url': url,
                    'status': 'error',
                    'status_code': response.status_code,
                    'error': f'HTTP {response.status_code}'
                }
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Métriques extraites
            metrics = {
                'url': url,
                'status': 'success',
                'status_code': response.status_code,
                'load_time_ms': round(load_time, 2),
                'page_size_kb': round(len(response.content) / 1024, 2),
                'title': soup.title.string if soup.title else None,
                'meta_description': self._get_meta_description(soup),
                'h1_count': len(soup.find_all('h1')),
                'images_count': len(soup.find_all('img')),
                'links_count': len(soup.find_all('a')),
                'scripts_count': len(soup.find_all('script')),
                'stylesheets_count': len(soup.find_all('link', rel='stylesheet')),
                'has_https': url.startswith('https://'),
                'has_analytics': self._detect_analytics(soup),
                'mobile_friendly': self._check_mobile_viewport(soup),
                'encoding': response.encoding
            }
            
            # Score de performance (0-100)
            metrics['performance_score'] = self._calculate_performance_score(metrics)
            
            logger.info(f"✅ {url} analysé (Score: {metrics['performance_score']}/100)")
            return metrics
            
        except requests.exceptions.Timeout:
            return {'url': url, 'status': 'error', 'error': 'Timeout'}
        except requests.exceptions.RequestException as e:
            return {'url': url, 'status': 'error', 'error': str(e)}
        except Exception as e:
            logger.error(f"❌ Erreur analyse {url}: {e}")
            return {'url': url, 'status': 'error', 'error': str(e)}
    
    def _get_meta_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrait la meta description"""
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta.get('content') if meta else None
    
    def _detect_analytics(self, soup: BeautifulSoup) -> Dict:
        """Détecte les outils d'analytics présents"""
        html_str = str(soup)
        
        return {
            'google_analytics': 'google-analytics.com' in html_str or 'gtag' in html_str,
            'google_tag_manager': 'googletagmanager.com' in html_str,
            'facebook_pixel': 'facebook.net' in html_str or 'fbq' in html_str,
            'hotjar': 'hotjar.com' in html_str
        }
    
    def _check_mobile_viewport(self, soup: BeautifulSoup) -> bool:
        """Vérifie si le site a une balise viewport mobile"""
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        return viewport is not None
    
    def _calculate_performance_score(self, metrics: Dict) -> int:
        """Calcule un score de performance sur 100"""
        score = 100
        
        # Pénalités
        if metrics['load_time_ms'] > 3000:
            score -= 30
        elif metrics['load_time_ms'] > 1000:
            score -= 15
        
        if metrics['page_size_kb'] > 2000:
            score -= 20
        elif metrics['page_size_kb'] > 1000:
            score -= 10
        
        if not metrics['has_https']:
            score -= 10
        
        if not metrics['mobile_friendly']:
            score -= 10
        
        if metrics['images_count'] > 50:
            score -= 5
        
        return max(0, score)
    
    def compare_websites(self, urls: List[str]) -> List[Dict]:
        """Compare plusieurs sites web"""
        results = []
        
        for url in urls:
            result = self.analyze_website(url)
            results.append(result)
            time.sleep(1)  # Rate limiting
        
        return results
