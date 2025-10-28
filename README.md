# 🐍 Challenge 50 Projets Python - Data & Analytics

Bienvenue dans mon challenge de 50 projets Python axés sur la data science, l'analyse de données et l'automatisation !

##  Vue d'Ensemble

**Date de début**: 26 octobre 2025  
**Objectif**: Compléter 50 projets pratiques en Python  
**Focus**: Data Science, Analytics, Visualisation, Automatisation

**Progression actuelle**: 2/50 (4%) 

```
████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 4%
```

---

##  Projets Complétés

###  Projet 1 : Analyseur CSV Professionnel
**Status**:  TERMINÉ | **Date**: 27 oct 2025 | **Dossier**: [`projet_01_analyseur_csv/`](./projet_01_analyseur_csv/)

Application web complète avec Streamlit pour l'analyse approfondie de fichiers CSV.

**Stack Technique**:
- Frontend: Streamlit
- Data Processing: Pandas & NumPy  
- Visualisation: Plotly (graphiques interactifs)
- Analyse: SciPy (statistiques)

**Fonctionnalités**:
-  Chargement et validation CSV/Excel avec détection d'encodage
-  Nettoyage des données (5 stratégies d'imputation)
-  Statistiques descriptives complètes (15+ métriques)
-  Analyse de corrélations (Pearson, Spearman, Kendall)
-  Détection d'anomalies (IQR, Z-Score, Mahalanobis)
-  8+ types de visualisations interactives
-  Génération de rapports (CSV, JSON, Markdown)

**Chiffres**: ~2,384 lignes de code | 7 modules | Documentation complète

[📖 Voir le README →](./projet_01_analyseur_csv/README.md)

---

###  Projet 2 : Dashboard de Suivi de Budget Personnel
**Status**:  TERMINÉ | **Date**: 28 oct 2025 | **Dossier**: [`projet_02_budget_dashboard/`](./projet_02_budget_dashboard/)

Application web de gestion de budget personnel avec analyses et visualisations interactives.

**Stack Technique**:
- Frontend: Streamlit
- Data Processing: Pandas
- Visualisation: Plotly
- Stockage: JSON

**Fonctionnalités**:
-  CRUD complet des transactions (revenus/dépenses)
-  Dashboard avec 4 métriques clés (solde, revenus, dépenses, économies)
-  Graphiques interactifs (tendance, camembert, barres)
-  Système d'alertes (dépassement budget)
-  Filtres par période et catégorie
-  État des budgets par catégorie
-  Export CSV/JSON
-  100 transactions exemple générées

**Chiffres**: ~800 lignes de code | 3 modules | Interface intuitive

[📖 Voir le README →](./projet_02_budget_dashboard/README.md)

---

## 🚧 Projets en Développement

*Aucun projet en cours actuellement*

---

## 📅 Projets Planifiés (Top 10)

| # | Projet | Technologies Prévues | Priorité |
|---|--------|---------------------|----------|
| 2 | ~~Dashboard de suivi de budget personnel~~ |  Streamlit, Plotly |  **TERMINÉ** |
| 3 | Scraper de prix Amazon avec alertes | BeautifulSoup, Scrapy |  Haute |
| 4 | Visualiseur de données COVID | Pandas, Plotly | Moyenne |
| 5 | Calculatrice de ROI marketing | NumPy, Streamlit | Moyenne |
| 6 | Tracker de cours d'actions | yfinance, Plotly | Moyenne |
| 7 | Générateur de rapports PDF depuis Excel | ReportLab, openpyxl | Moyenne |
| 8 | Dashboard métro avec prévisions | Pandas, Prophet | Basse |
| 9 | Analyseur de logs web | Regex, Pandas | Basse |
| 10 | Extracteur de données APIs publiques | Requests, FastAPI | Basse |

[ Voir la liste complète des 50 projets →](./PROGRESSION.md)

---

## 🛠️ Stack Technologique

### Acquises 
- **Data Processing**: Pandas, NumPy
- **Visualisation**: Plotly, Streamlit
- **Statistiques**: SciPy
- **Gestion Fichiers**: openpyxl, chardet

### À Apprendre 📚
- **Web Scraping**: BeautifulSoup, Scrapy, Selenium
- **Machine Learning**: Scikit-learn, TensorFlow
- **Bases de Données**: SQLite, PostgreSQL, MongoDB
- **APIs**: FastAPI, Flask
- **Big Data**: Dask, PySpark
- **Time Series**: Prophet, Statsmodels
- **NLP**: NLTK, spaCy

---

##  Statistiques Globales

| Métrique | Valeur |
|----------|--------|
| Projets terminés | 2 |
| Projets en cours | 0 |
| Jours actifs | 3 |
| Lignes de code totales | 3,184 |
| Technologies maîtrisées | 6 |
| Documentation (pages) | 5 |

---

##  Compétences Développées

### Techniques
-  Architecture logicielle modulaire
-  Séparation des responsabilités (SoC)
-  Type hints et documentation
-  Gestion d'erreurs robuste
-  Interface utilisateur moderne

### Data Science
-  Analyse exploratoire de données (EDA)
-  Nettoyage et preprocessing
-  Statistiques descriptives avancées
-  Tests d'hypothèses statistiques
-  Détection d'anomalies
-  Analyse de corrélations
-  Visualisation interactive

---

## 📂 Structure du Repository

```
50-projects-python/
├── README.md                      # Ce fichier
├── PROGRESSION.md                 # Suivi détaillé
│
├── projet_01_analyseur_csv/       #  TERMINÉ
│   ├── src/                       # 7 modules Python
│   ├── app.py                     # Application Streamlit
│   ├── config.py                  # Configuration
│   ├── requirements.txt           # Dépendances
│   ├── README.md                  # Documentation
│   └── ...
│
├── projet_02_dashboard_budget/    # 🔜 À VENIR
├── projet_03_scraper_amazon/      # 🔜 À VENIR
└── ...
```

---

## 🚀 Quick Start

### Cloner le repository
```bash
git clone <your-repo-url>
cd 50-projects-python
```

### Lancer un projet
```bash
# Exemple: Projet 1
cd projet_01_analyseur_csv
./run.sh

# Ou manuellement
pip install -r requirements.txt
streamlit run app.py
```

---

##  Principes de Développement

### Architecture
 **Modularité**: Un module = une responsabilité  
 **Réutilisabilité**: Code DRY (Don't Repeat Yourself)  
 **Maintenabilité**: Documentation et type hints  
 **Testabilité**: Modules indépendants

### Bonnes Pratiques
 **PEP 8**: Style guide Python  
 **Docstrings**: Documentation inline  
 **Type Hints**: Annotations de types  
 **Error Handling**: Gestion robuste des erreurs  
 **Git**: Commits réguliers et descriptifs

### Documentation
 **README**: Guide utilisateur  
 **Documentation Technique**: Architecture et concepts  
 **Code Comments**: Explications inline  
 **Examples**: Fichiers de données d'exemple

---

##  Objectifs du Challenge

### Court Terme (1 mois)
- [x] Projet 1 terminé 
- [ ] 10 projets complétés (20%)
- [ ] Maîtriser Streamlit et Plotly
- [ ] Apprendre web scraping

### Moyen Terme (3 mois)
- [ ] 25 projets complétés (50%)
- [ ] Maîtriser Machine Learning basique
- [ ] Créer un portfolio en ligne
- [ ] Contribuer à des projets open source

### Long Terme (6 mois)
- [ ] 50 projets complétés (100%) 
- [ ] Portfolio complet de projets
- [ ] Blog technique sur les apprentissages
- [ ] Compétences professionnelles en Data Science

---

##  Leçons Apprises

### Projet 1
1. **Architecture avant code** = gain de temps énorme
2. **Modules indépendants** = debug plus facile
3. **Documentation parallèle** = pas de rattrapage
4. **Type hints** = moins d'erreurs runtime
5. **Streamlit** = prototypage ultra-rapide

---

## 🏆 Milestones

- [ ] 🥉 **Bronze** (10 projets - 20%)
- [ ] 🥈 **Argent** (25 projets - 50%)
- [ ] 🥇 **Or** (40 projets - 80%)
- [ ] 💎 **Diamant** (50 projets - 100%)

**Progression actuelle**: En route vers le Bronze ! 

---

## 📚 Ressources

### Documentation Officielle
- [Python Docs](https://docs.python.org/3/)
- [Pandas Guide](https://pandas.pydata.org/docs/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [SciPy Reference](https://docs.scipy.org/)

### Apprentissage
- [Real Python](https://realpython.com/)
- [Kaggle Learn](https://www.kaggle.com/learn)
- [DataCamp](https://www.datacamp.com/)
- [Python for Data Analysis (Book)](https://wesmckinney.com/book/)

### Inspiration
- [Awesome Python](https://github.com/vinta/awesome-python)
- [Python Weekly](https://www.pythonweekly.com/)
- [Towards Data Science](https://towardsdatascience.com/)

---

## 🤝 Contribution

Ce repository documente mon parcours d'apprentissage personnel. Cependant, suggestions et feedbacks sont les bienvenus !

**Contact**: [Votre email ou profil]

---

##  Licence

MIT License - Libre d'utilisation et modification

---

##  Mises à Jour

### 27 octobre 2025
-  Projet 1 complété avec succès
-  2,384 lignes de code
- 📚 Documentation complète créée
-  Prêt pour Projet 2

---

<div align="center">

**🐍 Fait avec ❤️ et Python 🐍**

*"The best way to learn is by doing"*

**Progression: 1/50** | **Suivez le parcours !** 🚀

[ Retour en haut](#-challenge-50-projets-python---data--analytics)

</div>
