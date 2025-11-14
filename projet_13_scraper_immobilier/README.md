# 🏠 Projet 13 : Scraper Immobilier avec Analyse de Prix par Quartier

**Status**: ✅ TERMINÉ | **Date**: Novembre 2025

Application web complète pour scraper et analyser les prix immobiliers par quartier avec détection automatique des bonnes affaires.

## 🎯 Objectifs

- **Web Scraping** : Collecte automatisée de données immobilières
- **Analyse Géographique** : Prix par quartier et comparaisons
- **Détection d'Opportunités** : Identification des bonnes affaires
- **Visualisations** : Graphiques interactifs et cartes

## 🛠️ Stack Technique

- **Frontend** : Streamlit
- **Scraping** : BeautifulSoup, Requests
- **Base de Données** : SQLite
- **Analyse** : Pandas, NumPy, SciPy
- **Visualisation** : Plotly

## ⚡ Fonctionnalités

### 🔍 Scraping de Données
- ✅ Génération de données d'exemple (simulation)
- ✅ Nettoyage et validation des données
- ✅ Stockage en base SQLite
- ✅ Gestion des erreurs et timeouts

### 📊 Analyse Globale
- ✅ Statistiques descriptives complètes
- ✅ Distribution des prix et surfaces
- ✅ Détection d'outliers
- ✅ Corrélations surface-prix

### 🏘️ Analyse par Quartier
- ✅ Comparaison des prix/m² par quartier
- ✅ Statistiques détaillées par zone
- ✅ Tests statistiques de comparaison
- ✅ Visualisations interactives

### 💎 Détection de Bonnes Affaires
- ✅ Score de bonne affaire basé sur la médiane du quartier
- ✅ Classement des meilleures opportunités
- ✅ Filtrage par quartier
- ✅ Métriques d'économies potentielles

### 📊 Visualisations
- ✅ Distribution des prix (histogrammes)
- ✅ Prix par quartier (barres)
- ✅ Scatter plot surface vs prix
- ✅ Box plots par quartier
- ✅ Comparaisons interactives

## 🚀 Installation & Lancement

```bash
# Installation
pip install -r requirements.txt

# Lancement
streamlit run app.py
# ou
python run.py
```

## 📱 Interface

L'application propose 4 onglets principaux :

1. **🔍 Scraping** : Collecte et génération de données
2. **📊 Analyse Globale** : Vue d'ensemble du marché
3. **🏘️ Analyse par Quartier** : Comparaisons géographiques
4. **💎 Bonnes Affaires** : Détection d'opportunités

## 🏠 Types de Données Collectées

### Propriétés Immobilières
- **Prix** : Prix total et prix/m²
- **Surface** : Superficie en m²
- **Localisation** : Quartier et adresse
- **Caractéristiques** : Nombre de pièces
- **Métadonnées** : Date de scraping, source

### Analyses Générées
- **Statistiques** : Moyenne, médiane, écart-type
- **Comparaisons** : Tests statistiques entre quartiers
- **Scores** : Évaluation des bonnes affaires
- **Tendances** : Corrélations et distributions

## 📊 Métriques Calculées

### Prix et Surfaces
- **Prix moyen/médian** par quartier
- **Prix/m² moyen/médian** par zone
- **Surface moyenne** par type de bien
- **Fourchettes de prix** (min/max)

### Analyses Statistiques
- **Outliers** : Détection des prix aberrants
- **Asymétrie** : Skewness de la distribution
- **Kurtosis** : Forme de la distribution
- **Corrélations** : Relations entre variables

### Bonnes Affaires
- **Score de deal** : % d'économie vs médiane quartier
- **Classement** : Top des meilleures opportunités
- **Économies** : Montants et pourcentages

## 📁 Structure du Projet

```
projet_13_scraper_immobilier/
├── app.py                    # Application Streamlit principale
├── run.py                    # Script de lancement
├── config.py                 # Configuration
├── requirements.txt          # Dépendances
├── README.md                 # Documentation
├── src/
│   ├── scraper.py           # Module de scraping
│   ├── analyzer.py          # Analyses statistiques
│   └── visualizations.py    # Graphiques
├── data/
│   └── properties.db        # Base SQLite (créée automatiquement)
└── tests/                   # Tests unitaires
```

## 🧪 Exemple d'Utilisation

### Génération de Données
```python
# 100 propriétés simulées dans 10 quartiers parisiens
# Prix: 8,000€ - 15,000€/m²
# Surfaces: 20m² - 120m²
```

### Analyse par Quartier
```python
# Marais: 12,500€/m² (15 biens)
# Montmartre: 11,200€/m² (8 biens)
# Différence: +11.6% (significative p<0.05)
```

### Bonnes Affaires
```python
# Appartement 45m² - Bastille
# Prix: 450,000€ (10,000€/m²)
# Score: -15.2% vs médiane quartier
# Économie estimée: 80,000€
```

## 📈 Statistiques du Projet

| Métrique | Valeur |
|----------|--------|
| Lignes de code | ~500 |
| Modules | 4 |
| Types d'analyses | 6 |
| Visualisations | 5 |
| Métriques calculées | 15+ |

## 🎓 Compétences Développées

### Web Scraping
- ✅ Requêtes HTTP avec gestion d'erreurs
- ✅ Parsing HTML avec BeautifulSoup
- ✅ Nettoyage et validation de données
- ✅ Respect des bonnes pratiques (délais, user-agent)

### Analyse de Données
- ✅ Statistiques descriptives avancées
- ✅ Tests d'hypothèses (t-test)
- ✅ Détection d'outliers
- ✅ Analyse de corrélations

### Base de Données
- ✅ SQLite pour stockage persistant
- ✅ Requêtes SQL d'agrégation
- ✅ Gestion des transactions
- ✅ Optimisation des performances

### Visualisation
- ✅ Graphiques interactifs Plotly
- ✅ Tableaux de bord Streamlit
- ✅ Métriques et KPIs
- ✅ Interface utilisateur intuitive

## 🔄 Améliorations Futures

- [ ] Scraping réel (SeLoger, LeBonCoin)
- [ ] Géolocalisation avec cartes interactives
- [ ] Alertes email pour nouvelles bonnes affaires
- [ ] Prédiction de prix avec ML
- [ ] Export des rapports PDF
- [ ] API REST pour intégration

## ⚠️ Considérations Éthiques

- **Respect des robots.txt** des sites
- **Limitation du taux de requêtes**
- **Utilisation responsable des données**
- **Conformité RGPD**

## 📚 Ressources

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/)
- [Requests Documentation](https://docs.python-requests.org/)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [Web Scraping Ethics](https://blog.apify.com/web-scraping-ethics/)

---

**🎯 Projet 13/50 terminé** | **Progression**: 26% | **Prochaine étape**: Projet 14