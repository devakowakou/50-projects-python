"""Script principal pour l'extraction de données."""

import argparse
from src.api_clients.twitter_client import TwitterClient
from src.api_clients.reddit_client import RedditClient
from src.processing.clean_data import DataCleaner
from src.processing.sentiment_analysis import SentimentAnalyzer
from src.utils.config import Config


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description="Extracteur de données depuis APIs")
    parser.add_argument("--source", choices=["twitter", "reddit"], required=True,
                        help="Source de données")
    parser.add_argument("--query", type=str, help="Terme de recherche")
    parser.add_argument("--subreddit", type=str, help="Nom du subreddit (pour Reddit)")
    parser.add_argument("--limit", type=int, default=50, help="Nombre de résultats")
    
    args = parser.parse_args()
    
    print(f"\n🚀 Lancement de l'extraction depuis {args.source.upper()}\n")
    
    if args.source == "twitter":
        if not args.query:
            print("❌ --query requis pour Twitter")
            return
        
        client = TwitterClient()
        tweets = client.search_tweets(args.query, args.limit)
        
        if tweets:
            df = DataCleaner.clean_twitter_data(tweets)
            df = SentimentAnalyzer.add_sentiment_to_df(df)
            
            # Sauvegarder
            output_file = Config.PROCESSED_DATA_DIR / f"twitter_{args.query.replace(' ', '_')}.csv"
            df.to_csv(output_file, index=False)
            print(f"\n💾 Données sauvegardées: {output_file}")
            
            # Statistiques
            stats = SentimentAnalyzer.get_sentiment_stats(df)
            print(f"\n📊 Statistiques:")
            print(f"  - Total: {stats['total']}")
            print(f"  - Positif: {stats['positive']} ({stats['positive_pct']}%)")
            print(f"  - Neutre: {stats['neutral']} ({stats['neutral_pct']}%)")
            print(f"  - Négatif: {stats['negative']} ({stats['negative_pct']}%)")
            print(f"  - Score moyen: {stats['avg_score']}")
    
    elif args.source == "reddit":
        if not args.subreddit:
            print("❌ --subreddit requis pour Reddit")
            return
        
        client = RedditClient()
        posts = client.search_subreddit(args.subreddit, args.query, args.limit)
        
        if posts:
            df = DataCleaner.clean_reddit_data(posts)
            df = SentimentAnalyzer.add_sentiment_to_df(df, 'title_clean')
            
            # Sauvegarder
            output_file = Config.PROCESSED_DATA_DIR / f"reddit_{args.subreddit}.csv"
            df.to_csv(output_file, index=False)
            print(f"\n💾 Données sauvegardées: {output_file}")
            
            # Statistiques
            stats = SentimentAnalyzer.get_sentiment_stats(df)
            print(f"\n📊 Statistiques:")
            print(f"  - Total: {stats['total']}")
            print(f"  - Positif: {stats['positive']} ({stats['positive_pct']}%)")
            print(f"  - Neutre: {stats['neutral']} ({stats['neutral_pct']}%)")
            print(f"  - Négatif: {stats['negative']} ({stats['negative_pct']}%)")
            print(f"  - Score moyen: {stats['avg_score']}")
    
    print("\n✅ Extraction terminée!\n")


if __name__ == "__main__":
    main()
