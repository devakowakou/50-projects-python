# 🚀 Quick Start - Analyse de Sentiment

## 📦 Installation

```bash
# 1. Aller dans le projet
cd projet_16_sentiment_analysis

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Charger les données de démonstration
python load_demo_data.py

# 4. Lancer le dashboard
python main.py dashboard
```

**➡️ Dashboard disponible sur:** http://localhost:8501

## 🎯 Utilisation

### 🕷️ Scraping
```bash
# Amazon
python main.py scrape amazon "https://amazon.com/dp/PRODUCT_ID"

# Trustpilot  
python main.py scrape trustpilot "https://trustpilot.com/review/company.com"
```

### 📊 Dashboard
```bash
python main.py dashboard
```

### 📈 Statistiques
```bash
python main.py stats
```

### 🧪 Tests
```bash
python main.py test
```

## ✅ Fonctionnalités

### Scraping Avancé
- **Botasaurus** : Anti-détection automatique
- **Amazon** : Avis produits avec pagination
- **Trustpilot** : Reviews entreprises
- **Validation** : Données structurées

### Analyse NLP
- **TextBlob** : Sentiment rapide
- **VADER** : Optimisé réseaux sociaux
- **Consensus** : Combinaison des modèles
- **Aspects** : Prix, qualité, service, livraison

### Dashboard Interactif
- **Métriques** : Taux positif/négatif, confiance
- **Graphiques** : Camembert, histogrammes, scatter
- **WordCloud** : Nuage de mots par sentiment
- **Export** : CSV, rapports markdown

## 🎮 Interface Dashboard

### Sidebar
- **Nouveau scraping** : URL + plateforme
- **Filtres** : Par plateforme

### Métriques Principales
- Total avis analysés
- Taux positif/négatif
- Confiance moyenne

### Visualisations
- Distribution des sentiments
- Sentiment par note
- Comparaison plateformes
- Évolution temporelle
- Confiance des prédictions

### Données
- Tableau des avis récents
- Export CSV/Markdown

## 📊 Exemple de Résultats

```
📈 Résumé:
- Total avis: 10
- Sentiment global: positive

- Positive: 4 (40.0%)
- Negative: 3 (30.0%)  
- Neutral: 3 (30.0%)
```

## 🔧 Configuration

### Paramètres Scraping
- Délai entre requêtes : 1-3 secondes
- Retry automatique : 3 tentatives
- User agents rotatifs

### Seuils NLP
- Positif : > 0.1
- Négatif : < -0.1
- Neutre : -0.1 à 0.1

## 🚨 Considérations

### Éthique
- Respecter robots.txt
- Rate limiting approprié
- Usage analytique uniquement

### Performance
- Cache des analyses
- Pagination des résultats
- Optimisation base de données

---

**🎯 Projet fonctionnel en 5 minutes !**