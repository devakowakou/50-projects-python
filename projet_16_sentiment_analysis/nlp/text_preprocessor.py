"""Préprocesseur de texte pour l'analyse de sentiment."""

import re
import string
from typing import List, Dict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


class TextPreprocessor:
    """Classe pour le préprocessing des textes d'avis."""
    
    def __init__(self, language: str = "english"):
        self.language = language
        self.lemmatizer = WordNetLemmatizer()
        
        # Télécharger les ressources NLTK nécessaires
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
        
        self.stop_words = set(stopwords.words(language))
        
        # Mots de négation à préserver
        self.negation_words = {
            'not', 'no', 'never', 'nothing', 'nowhere', 'noone', 'none', 
            'not', 'havent', 'hasnt', 'hadnt', 'cant', 'couldnt', 'shouldnt', 
            'wont', 'wouldnt', 'dont', 'doesnt', 'didnt', 'isnt', 'arent', 'aint'
        }
        
        # Retirer les mots de négation des stop words
        self.stop_words = self.stop_words - self.negation_words
    
    def clean_text(self, text: str) -> str:
        """Nettoyage de base du texte."""
        if not text:
            return ""
        
        # Convertir en minuscules
        text = text.lower()
        
        # Supprimer les URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Supprimer les mentions et hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Supprimer les caractères spéciaux mais garder la ponctuation importante
        text = re.sub(r'[^\w\s!?.,]', '', text)
        
        # Normaliser les espaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenisation du texte."""
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Supprimer les mots vides en préservant la négation."""
        return [token for token in tokens if token not in self.stop_words]
    
    def lemmatize(self, tokens: List[str]) -> List[str]:
        """Lemmatisation des tokens."""
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def preprocess_for_sentiment(self, text: str, keep_punctuation: bool = True) -> str:
        """Préprocessing spécialisé pour l'analyse de sentiment."""
        if not text:
            return ""
        
        # Nettoyage de base
        text = self.clean_text(text)
        
        if keep_punctuation:
            # Garder la ponctuation pour l'analyse de sentiment
            # Normaliser certaines ponctuations
            text = re.sub(r'!+', '!', text)  # Multiples ! -> !
            text = re.sub(r'\?+', '?', text)  # Multiples ? -> ?
            text = re.sub(r'\.+', '.', text)  # Multiples . -> .
        else:
            # Supprimer la ponctuation
            text = text.translate(str.maketrans('', '', string.punctuation))
        
        return text
    
    def preprocess_for_keywords(self, text: str) -> List[str]:
        """Préprocessing pour l'extraction de mots-clés."""
        # Nettoyage
        text = self.clean_text(text)
        
        # Tokenisation
        tokens = self.tokenize(text)
        
        # Supprimer les mots vides
        tokens = self.remove_stopwords(tokens)
        
        # Supprimer les tokens trop courts
        tokens = [token for token in tokens if len(token) > 2]
        
        # Lemmatisation
        tokens = self.lemmatize(tokens)
        
        return tokens
    
    def extract_aspects(self, text: str) -> Dict[str, List[str]]:
        """Extraire les aspects mentionnés dans le texte."""
        text = text.lower()
        
        # Dictionnaire des aspects avec mots-clés associés
        aspects = {
            "price": ["price", "cost", "expensive", "cheap", "affordable", "money", "dollar", "euro", "budget"],
            "quality": ["quality", "good", "bad", "excellent", "poor", "great", "terrible", "amazing", "awful"],
            "service": ["service", "staff", "employee", "help", "support", "customer", "representative"],
            "delivery": ["delivery", "shipping", "fast", "slow", "quick", "delayed", "arrived", "package"],
            "product": ["product", "item", "goods", "material", "build", "design", "feature", "function"]
        }
        
        found_aspects = {}
        
        for aspect, keywords in aspects.items():
            found_words = []
            for keyword in keywords:
                if keyword in text:
                    found_words.append(keyword)
            
            if found_words:
                found_aspects[aspect] = found_words
        
        return found_aspects
    
    def get_text_stats(self, text: str) -> Dict:
        """Obtenir des statistiques sur le texte."""
        if not text:
            return {"length": 0, "words": 0, "sentences": 0}
        
        # Compter les mots
        words = len(text.split())
        
        # Compter les phrases (approximatif)
        sentences = len(re.findall(r'[.!?]+', text))
        
        return {
            "length": len(text),
            "words": words,
            "sentences": max(sentences, 1),  # Au moins 1 phrase
            "avg_word_length": len(text) / max(words, 1)
        }


# Test du préprocesseur
if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    
    # Texte d'exemple
    test_text = """
    This product is AMAZING!!! The quality is excellent and the price is very affordable.
    However, the delivery was quite slow... Customer service was helpful though.
    I would definitely recommend this to others! 5 stars!
    """
    
    print("📝 Texte original:")
    print(test_text)
    
    print("\n🧹 Texte nettoyé:")
    cleaned = preprocessor.preprocess_for_sentiment(test_text)
    print(cleaned)
    
    print("\n🔑 Mots-clés extraits:")
    keywords = preprocessor.preprocess_for_keywords(test_text)
    print(keywords)
    
    print("\n📊 Aspects détectés:")
    aspects = preprocessor.extract_aspects(test_text)
    print(aspects)
    
    print("\n📈 Statistiques:")
    stats = preprocessor.get_text_stats(test_text)
    print(stats)