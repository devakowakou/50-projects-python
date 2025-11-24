"""Analyseur de sentiment principal avec plusieurs modèles."""

from typing import Dict, List, Tuple
import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .text_preprocessor import TextPreprocessor


class SentimentAnalyzer:
    """Analyseur de sentiment utilisant plusieurs modèles."""
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Seuils pour la classification
        self.thresholds = {
            "positive": 0.1,
            "negative": -0.1
        }
    
    def analyze_with_textblob(self, text: str) -> Dict:
        """Analyse avec TextBlob."""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 à 1
            subjectivity = blob.sentiment.subjectivity  # 0 à 1
            
            # Classification
            if polarity > self.thresholds["positive"]:
                sentiment = "positive"
            elif polarity < self.thresholds["negative"]:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            return {
                "model": "textblob",
                "sentiment": sentiment,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "confidence": abs(polarity)
            }
        except Exception as e:
            return {
                "model": "textblob",
                "sentiment": "neutral",
                "polarity": 0.0,
                "subjectivity": 0.0,
                "confidence": 0.0,
                "error": str(e)
            }
    
    def analyze_with_vader(self, text: str) -> Dict:
        """Analyse avec VADER."""
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            
            # VADER retourne: neg, neu, pos, compound
            compound = scores['compound']  # Score global -1 à 1
            
            # Classification basée sur le score compound
            if compound >= 0.05:
                sentiment = "positive"
            elif compound <= -0.05:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            return {
                "model": "vader",
                "sentiment": sentiment,
                "compound": compound,
                "positive": scores['pos'],
                "negative": scores['neg'],
                "neutral": scores['neu'],
                "confidence": abs(compound)
            }
        except Exception as e:
            return {
                "model": "vader",
                "sentiment": "neutral",
                "compound": 0.0,
                "positive": 0.0,
                "negative": 0.0,
                "neutral": 1.0,
                "confidence": 0.0,
                "error": str(e)
            }
    
    def analyze_single_review(self, text: str) -> Dict:
        """Analyser un seul avis avec tous les modèles."""
        if not text or len(text.strip()) < 3:
            return {
                "text": text,
                "error": "Text too short or empty"
            }
        
        # Préprocessing
        cleaned_text = self.preprocessor.preprocess_for_sentiment(text)
        
        # Analyses avec différents modèles
        textblob_result = self.analyze_with_textblob(cleaned_text)
        vader_result = self.analyze_with_vader(cleaned_text)
        
        # Consensus entre les modèles
        consensus = self._get_consensus([textblob_result, vader_result])
        
        # Extraction d'aspects
        aspects = self.preprocessor.extract_aspects(text)
        
        # Statistiques du texte
        stats = self.preprocessor.get_text_stats(text)
        
        return {
            "text": text,
            "cleaned_text": cleaned_text,
            "textblob": textblob_result,
            "vader": vader_result,
            "consensus": consensus,
            "aspects": aspects,
            "stats": stats
        }
    
    def analyze_reviews_batch(self, reviews: List[Dict]) -> List[Dict]:
        """Analyser un lot d'avis."""
        results = []
        
        for i, review in enumerate(reviews):
            print(f"📊 Analyse {i+1}/{len(reviews)}")
            
            text = review.get("text", "")
            analysis = self.analyze_single_review(text)
            
            # Ajouter les métadonnées de l'avis
            analysis.update({
                "review_id": review.get("id", i),
                "rating": review.get("rating"),
                "platform": review.get("platform"),
                "date": review.get("date"),
                "author": review.get("author")
            })
            
            results.append(analysis)
        
        return results
    
    def _get_consensus(self, results: List[Dict]) -> Dict:
        """Obtenir un consensus entre plusieurs modèles."""
        sentiments = []
        confidences = []
        
        for result in results:
            if "error" not in result:
                sentiments.append(result["sentiment"])
                confidences.append(result.get("confidence", 0))
        
        if not sentiments:
            return {"sentiment": "neutral", "confidence": 0.0, "agreement": 0.0}
        
        # Sentiment majoritaire
        from collections import Counter
        sentiment_counts = Counter(sentiments)
        consensus_sentiment = sentiment_counts.most_common(1)[0][0]
        
        # Niveau d'accord
        agreement = sentiment_counts[consensus_sentiment] / len(sentiments)
        
        # Confiance moyenne
        avg_confidence = np.mean(confidences)
        
        return {
            "sentiment": consensus_sentiment,
            "confidence": avg_confidence,
            "agreement": agreement,
            "model_count": len(results)
        }
    
    def get_sentiment_summary(self, analyses: List[Dict]) -> Dict:
        """Résumé des sentiments pour un ensemble d'analyses."""
        if not analyses:
            return {}
        
        sentiments = []
        ratings = []
        aspects_all = {}
        
        for analysis in analyses:
            # Sentiment consensus
            consensus = analysis.get("consensus", {})
            if consensus.get("sentiment"):
                sentiments.append(consensus["sentiment"])
            
            # Rating
            rating = analysis.get("rating")
            if rating:
                ratings.append(rating)
            
            # Aspects
            aspects = analysis.get("aspects", {})
            for aspect, words in aspects.items():
                if aspect not in aspects_all:
                    aspects_all[aspect] = []
                aspects_all[aspect].extend(words)
        
        # Statistiques des sentiments
        from collections import Counter
        sentiment_counts = Counter(sentiments)
        total_reviews = len(sentiments)
        
        sentiment_stats = {}
        for sentiment in ["positive", "negative", "neutral"]:
            count = sentiment_counts.get(sentiment, 0)
            sentiment_stats[sentiment] = {
                "count": count,
                "percentage": (count / total_reviews * 100) if total_reviews > 0 else 0
            }
        
        # Statistiques des ratings
        rating_stats = {}
        if ratings:
            rating_stats = {
                "average": np.mean(ratings),
                "median": np.median(ratings),
                "min": min(ratings),
                "max": max(ratings),
                "count": len(ratings)
            }
        
        # Top aspects
        top_aspects = {}
        for aspect, words in aspects_all.items():
            word_counts = Counter(words)
            top_aspects[aspect] = {
                "total_mentions": len(words),
                "unique_words": len(set(words)),
                "top_words": word_counts.most_common(5)
            }
        
        return {
            "total_reviews": total_reviews,
            "sentiment_distribution": sentiment_stats,
            "rating_stats": rating_stats,
            "top_aspects": top_aspects,
            "overall_sentiment": sentiment_counts.most_common(1)[0][0] if sentiment_counts else "neutral"
        }


# Test de l'analyseur
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    # Avis d'exemple
    test_reviews = [
        {
            "text": "This product is absolutely amazing! Great quality and fast delivery. Highly recommend!",
            "rating": 5,
            "platform": "amazon"
        },
        {
            "text": "Terrible experience. Poor quality and very expensive. Would not buy again.",
            "rating": 1,
            "platform": "amazon"
        },
        {
            "text": "It's okay, nothing special. Average quality for the price.",
            "rating": 3,
            "platform": "trustpilot"
        }
    ]
    
    print("🧠 Test de l'analyseur de sentiment")
    
    # Analyser les avis
    results = analyzer.analyze_reviews_batch(test_reviews)
    
    # Afficher les résultats
    for i, result in enumerate(results):
        print(f"\n📝 Avis {i+1}:")
        print(f"Texte: {result['text'][:100]}...")
        print(f"Consensus: {result['consensus']['sentiment']} (confiance: {result['consensus']['confidence']:.2f})")
        print(f"TextBlob: {result['textblob']['sentiment']} ({result['textblob']['polarity']:.2f})")
        print(f"VADER: {result['vader']['sentiment']} ({result['vader']['compound']:.2f})")
        print(f"Aspects: {list(result['aspects'].keys())}")
    
    # Résumé global
    print("\n📊 Résumé global:")
    summary = analyzer.get_sentiment_summary(results)
    print(f"Total avis: {summary['total_reviews']}")
    print(f"Sentiment global: {summary['overall_sentiment']}")
    print("Distribution:")
    for sentiment, stats in summary['sentiment_distribution'].items():
        print(f"  {sentiment}: {stats['count']} ({stats['percentage']:.1f}%)")