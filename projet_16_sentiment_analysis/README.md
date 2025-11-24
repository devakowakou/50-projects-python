# 💭 Projet 16 : Analyse de Sentiment sur Reviews

**Status**: 🚧 EN COURS | **Date début**: 29 oct 2025 | **Branche**: `feature/projet-16-sentiment-analysis`

Système d'analyse de sentiment pour analyser les avis clients Amazon et Trustpilot avec scraping moderne et NLP avancé.

## 🎯 Objectif

Analyser automatiquement le sentiment des avis clients pour :
- **Détecter** les tendances de satisfaction
- **Identifier** les points d'amélioration
- **Comparer** les produits/services
- **Générer** des insights business

## 🔧 Stack Technique

| Composant | Technologie |
|-----------|-------------|
| **Scraping** | Botasaurus (anti-détection, headless) |
| **NLP** | NLTK, spaCy, TextBlob, Transformers |
| **ML** | Scikit-learn, BERT |
| **Frontend** | Streamlit |
| **Visualisation** | Plotly, WordCloud, Seaborn |
| **Base de données** | SQLite, Pandas |
| **Processing** | NumPy, Pandas |

## 🏗️ Architecture

```
projet_16_sentiment_analysis/
├── scrapers/                   # Scrapers Botasaurus
│   ├── amazon_scraper.py      # Scraper Amazon
│   ├── trustpilot_scraper.py  # Scraper Trustpilot
│   ├── base_scraper.py        # Classe de base
│   └── utils.py               # Utilitaires scraping
│
├── nlp/                        # Analyse NLP
│   ├── sentiment_analyzer.py  # Analyseur principal
│   ├── text_preprocessor.py   # Nettoyage texte
│   ├── models/                # Modèles ML
│   │   ├── bert_classifier.py # Modèle BERT
│   │   └── traditional_ml.py  # ML classique
│   └── utils.py               # Utilitaires NLP
│
├── data/                       # Gestion des données
│   ├── database.py            # Base de données
│   ├── models.py              # Modèles de données
│   └── sample_data/           # Données d'exemple
│
├── dashboard/                  # Interface Streamlit
│   ├── app.py                 # App principale
│   ├── components/            # Composants UI
│   │   ├── charts.py          # Graphiques
│   │   ├── metrics.py         # Métriques
│   │   └── filters.py         # Filtres
│   └── pages/                 # Pages du dashboard
│       ├── overview.py        # Vue d'ensemble
│       ├── analysis.py        # Analyse détaillée
│       └── comparison.py      # Comparaisons
│
├── config/                     # Configuration
│   ├── settings.py            # Paramètres
│   └── logging.py             # Logs
│
├── tests/                      # Tests
├── requirements.txt            # Dépendances
├── README.md                   # Ce fichier
└── main.py                     # Point d'entrée
```

## 🚀 Procédure de Développement

### Phase 1: Setup & Scraping (Semaine 1)
```bash
# 1. Setup Botasaurus
pip install botasaurus
pip install botasaurus[all]

# 2. Créer scrapers Amazon/Trustpilot
# 3. Tests anti-détection
# 4. Stockage données brutes
```

### Phase 2: NLP & Sentiment (Semaine 2)
```bash
# 1. Preprocessing texte
# 2. Modèles sentiment (TextBlob, VADER, BERT)
# 3. Classification par aspects
# 4. Extraction mots-clés
```

### Phase 3: Dashboard (Semaine 3)
```bash
# 1. Interface Streamlit
# 2. Visualisations interactives
# 3. Métriques temps réel
# 4. Filtres et comparaisons
```

### Phase 4: Optimisation (Semaine 4)
```bash
# 1. Performance et cache
# 2. Export rapports
# 3. Tests et documentation
# 4. Déploiement
```

## 🎯 Fonctionnalités

### ✅ Scraping Avancé
- [ ] **Amazon** : Avis produits avec pagination
- [ ] **Trustpilot** : Reviews entreprises
- [ ] **Anti-détection** : Rotation proxies, headers
- [ ] **Données structurées** : Note, texte, date, auteur

### 🧠 Analyse NLP
- [ ] **Preprocessing** : Nettoyage, normalisation
- [ ] **Sentiment** : Positif/Négatif/Neutre + score
- [ ] **Aspects** : Prix, qualité, service, livraison
- [ ] **Mots-clés** : Extraction automatique
- [ ] **Émotions** : Joie, colère, tristesse, peur

### 📊 Dashboard Interactif
- [ ] **Vue d'ensemble** : Métriques principales
- [ ] **Tendances** : Évolution sentiment dans le temps
- [ ] **Comparaisons** : Produits/concurrents
- [ ] **Word Cloud** : Mots les plus fréquents
- [ ] **Aspects** : Analyse par catégorie
- [ ] **Export** : PDF, CSV, JSON

## 🔍 Métriques Calculées

### Sentiment Global
```python
sentiment_score = (positifs - négatifs) / total_avis
satisfaction_rate = positifs / total_avis * 100
```

### Par Aspects
```python
aspect_sentiment = {
    "prix": score_prix,
    "qualité": score_qualité,
    "service": score_service,
    "livraison": score_livraison
}
```

### Tendances
```python
trend_analysis = sentiment_evolution_over_time()
seasonal_patterns = detect_seasonal_sentiment()
```

## 🤖 Modèles NLP

### 1. TextBlob (Rapide)
```python
from textblob import TextBlob
sentiment = TextBlob(text).sentiment.polarity
```

### 2. VADER (Réseaux sociaux)
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
scores = analyzer.polarity_scores(text)
```

### 3. BERT (Précis)
```python
from transformers import pipeline
classifier = pipeline("sentiment-analysis")
result = classifier(text)
```

## 🎮 Utilisation

### Scraping
```python
from scrapers.amazon_scraper import AmazonScraper

scraper = AmazonScraper()
reviews = scraper.scrape_product_reviews(product_url)
```

### Analyse
```python
from nlp.sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()
results = analyzer.analyze_reviews(reviews)
```

### Dashboard
```bash
streamlit run dashboard/app.py
```

## 📈 Objectifs de Performance

- **Scraping** : 1000+ avis/heure sans blocage
- **NLP** : Analyse 100 avis/seconde
- **Précision** : >85% sur sentiment global
- **Dashboard** : Temps de réponse <2s

## 🔒 Considérations Éthiques

- **Respect robots.txt** et conditions d'utilisation
- **Rate limiting** pour éviter la surcharge
- **Anonymisation** des données personnelles
- **Usage** uniquement à des fins d'analyse

---

## 🚀 Quick Start

```bash
# 1. Cloner et installer
git checkout feature/projet-16-sentiment-analysis
cd projet_16_sentiment_analysis
pip install -r requirements.txt

# 2. Configurer
cp config/settings.example.py config/settings.py

# 3. Tester scraping
python scrapers/amazon_scraper.py

# 4. Lancer dashboard
streamlit run dashboard/app.py
```

---

*Projet créé le 29 octobre 2025 - Challenge 50 Projets Python*