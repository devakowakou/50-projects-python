"""Point d'entrée principal du projet d'analyse de sentiment."""

import argparse
import sys
from pathlib import Path

# Ajouter le chemin du projet
sys.path.append(str(Path(__file__).parent))

from scrapers.amazon_scraper import AmazonScraper
from scrapers.trustpilot_scraper import TrustpilotScraper
from nlp.sentiment_analyzer import SentimentAnalyzer
from data.database import ReviewDatabase, save_reviews_to_db


def scrape_and_analyze(platform: str, url: str, max_pages: int = 2):
    """Scraper et analyser des avis."""
    print(f"🚀 Démarrage du scraping {platform}")
    
    # Initialiser le scraper
    if platform.lower() == "amazon":
        scraper = AmazonScraper()
        reviews = scraper.scrape_product_reviews(url, max_pages)
    elif platform.lower() == "trustpilot":
        scraper = TrustpilotScraper()
        reviews = scraper.scrape_company_reviews(url, max_pages)
    else:
        print("❌ Plateforme non supportée. Utilisez 'amazon' ou 'trustpilot'")
        return
    
    if not reviews:
        print("❌ Aucun avis trouvé")
        return
    
    print(f"✅ {len(reviews)} avis scrapés")
    
    # Analyser les sentiments
    print("🧠 Analyse des sentiments...")
    analyzer = SentimentAnalyzer()
    analyses = analyzer.analyze_reviews_batch(reviews)
    
    # Sauvegarder en base
    print("💾 Sauvegarde en base de données...")
    save_reviews_to_db(reviews, analyses)
    
    # Résumé
    summary = analyzer.get_sentiment_summary(analyses)
    print("\n📊 Résumé de l'analyse:")
    print(f"Total avis: {summary['total_reviews']}")
    print(f"Sentiment global: {summary['overall_sentiment']}")
    
    for sentiment, stats in summary['sentiment_distribution'].items():
        print(f"{sentiment.title()}: {stats['count']} ({stats['percentage']:.1f}%)")


def launch_dashboard():
    """Lancer le dashboard Streamlit."""
    import subprocess
    import os
    
    dashboard_path = Path(__file__).parent / "dashboard" / "app.py"
    
    print("🚀 Lancement du dashboard Streamlit...")
    print("📱 Le dashboard sera disponible sur: http://localhost:8501")
    
    try:
        subprocess.run([
            "streamlit", "run", str(dashboard_path),
            "--server.port", "8501",
            "--server.headless", "true"
        ])
    except FileNotFoundError:
        print("❌ Streamlit n'est pas installé. Installez-le avec: pip install streamlit")
    except KeyboardInterrupt:
        print("\n👋 Dashboard fermé")


def show_stats():
    """Afficher les statistiques de la base de données."""
    db = ReviewDatabase()
    
    print("📊 Statistiques de la base de données:")
    
    # Avis par plateforme
    reviews = db.get_reviews(limit=10000)
    platforms = {}
    for review in reviews:
        platform = review.get("platform", "unknown")
        platforms[platform] = platforms.get(platform, 0) + 1
    
    print(f"\nTotal avis: {len(reviews)}")
    for platform, count in platforms.items():
        print(f"{platform.title()}: {count}")
    
    # Statistiques de sentiment
    sentiment_stats = db.get_sentiment_stats()
    if sentiment_stats:
        print("\nDistribution des sentiments:")
        for sentiment, stats in sentiment_stats.items():
            print(f"{sentiment.title()}: {stats['count']} ({stats['percentage']:.1f}%)")


def main():
    """Fonction principale avec arguments CLI."""
    parser = argparse.ArgumentParser(description="Analyse de sentiment sur reviews")
    
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")
    
    # Commande scrape
    scrape_parser = subparsers.add_parser("scrape", help="Scraper des avis")
    scrape_parser.add_argument("platform", choices=["amazon", "trustpilot"], 
                              help="Plateforme à scraper")
    scrape_parser.add_argument("url", help="URL du produit/entreprise")
    scrape_parser.add_argument("--pages", type=int, default=2, 
                              help="Nombre de pages à scraper")
    
    # Commande dashboard
    subparsers.add_parser("dashboard", help="Lancer le dashboard Streamlit")
    
    # Commande stats
    subparsers.add_parser("stats", help="Afficher les statistiques")
    
    # Commande test
    test_parser = subparsers.add_parser("test", help="Tester les composants")
    test_parser.add_argument("--component", choices=["scraper", "nlp", "db"], 
                            help="Composant à tester")
    
    args = parser.parse_args()
    
    if args.command == "scrape":
        scrape_and_analyze(args.platform, args.url, args.pages)
    
    elif args.command == "dashboard":
        launch_dashboard()
    
    elif args.command == "stats":
        show_stats()
    
    elif args.command == "test":
        run_tests(args.component)
    
    else:
        parser.print_help()


def run_tests(component: str = None):
    """Exécuter les tests."""
    print("🧪 Exécution des tests...")
    
    if not component or component == "db":
        print("\n📊 Test de la base de données...")
        try:
            db = ReviewDatabase()
            test_review = {
                "text": "Test review for database",
                "rating": 5,
                "platform": "test"
            }
            review_id = db.insert_review(test_review)
            print(f"✅ Base de données OK (ID: {review_id})")
        except Exception as e:
            print(f"❌ Erreur base de données: {e}")
    
    if not component or component == "nlp":
        print("\n🧠 Test de l'analyse NLP...")
        try:
            analyzer = SentimentAnalyzer()
            test_text = "This product is amazing! Great quality and fast delivery."
            result = analyzer.analyze_single_review(test_text)
            print(f"✅ NLP OK - Sentiment: {result['consensus']['sentiment']}")
        except Exception as e:
            print(f"❌ Erreur NLP: {e}")
    
    if not component or component == "scraper":
        print("\n🕷️ Test des scrapers...")
        print("⚠️ Tests scrapers nécessitent des URLs réelles")
        print("Utilisez: python main.py scrape amazon <URL>")


if __name__ == "__main__":
    main()