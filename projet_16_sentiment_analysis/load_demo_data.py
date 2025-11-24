"""Script pour charger les données de démonstration."""

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from data.database import save_reviews_to_db
from nlp.sentiment_analyzer import SentimentAnalyzer


def load_demo_data():
    """Charger les données de démonstration dans la base."""
    
    # Charger les avis d'exemple
    demo_file = Path(__file__).parent / "data" / "sample_data" / "demo_reviews.json"
    
    with open(demo_file, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
    
    print(f"📊 Chargement de {len(reviews)} avis de démonstration...")
    
    # Analyser les sentiments
    analyzer = SentimentAnalyzer()
    analyses = analyzer.analyze_reviews_batch(reviews)
    
    # Sauvegarder en base
    save_reviews_to_db(reviews, analyses)
    
    # Afficher le résumé
    summary = analyzer.get_sentiment_summary(analyses)
    print("\n✅ Données de démonstration chargées!")
    print(f"📈 Résumé:")
    print(f"- Total avis: {summary['total_reviews']}")
    print(f"- Sentiment global: {summary['overall_sentiment']}")
    
    for sentiment, stats in summary['sentiment_distribution'].items():
        print(f"- {sentiment.title()}: {stats['count']} ({stats['percentage']:.1f}%)")
    
    print("\n🚀 Vous pouvez maintenant lancer le dashboard:")
    print("python main.py dashboard")


if __name__ == "__main__":
    load_demo_data()