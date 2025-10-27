# 📊 Analyseur CSV Professionnel v2.1

> Projet 1 des "50 Projets Python" - Analyseur CSV avec statistiques descriptives et rapports professionnels

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production--Ready-success)](.)

---

## 🎯 Description

Application web interactive pour analyser des fichiers CSV/Excel avec :
- ✅ Statistiques descriptives avancées
- ✅ Nettoyage et transformation de données
- ✅ Détection d'anomalies (3 méthodes)
- ✅ Visualisations interactives (Plotly)
- ✅ Rapports professionnels (PDF, DOCX, HTML)
- ✅ Recommandations automatiques intelligentes

---

## 📂 Structure du Projet

```
projet_01_analyseur_csv/
├── app.py                      # Application Streamlit principale
├── config.py                   # Configuration globale
├── requirements.txt            # Dépendances Python
├── run.sh                      # Script de lancement rapide
│
├── src/                        # Modules métier
│   ├── data_loader.py          # Chargement et validation
│   ├── data_cleaner.py         # Nettoyage de données
│   ├── statistical_analyzer.py # Analyses statistiques
│   ├── correlation_analyzer.py # Analyses de corrélations
│   ├── anomaly_detector.py     # Détection d'anomalies
│   ├── visualizer.py           # Visualisations Plotly
│   ├── report_generator.py     # Rapports basiques
│   └── modern_report_generator.py # Rapports modernes (PDF/DOCX/HTML)
│
├── data/                       # Données
│   └── exemple_ventes.csv      # Dataset exemple
│
├── assets/                     # Ressources
│   └── style.css               # Styles personnalisés
│
├── docs/                       # 📚 Documentation
│   ├── INDEX.md                # Index de la documentation
│   ├── README.md               # Vue d'ensemble
│   ├── INSTALLATION_RAPIDE.md  # Guide installation
│   ├── DOCUMENTATION_TECHNIQUE.md # Architecture
│   ├── AMELIORATIONS.md        # Fonctionnalités v2.0
│   ├── CORRECTIONS_RAPPORTS.md # Corrections v2.1
│   └── ... (autres docs)
│
├── tests/                      # 🧪 Tests
│   ├── README.md               # Guide des tests
│   └── test_rapports_corriges.py # Tests automatiques
│
└── outputs/                    # 📤 Fichiers générés
    ├── reports/                # Rapports PDF/DOCX/HTML
    └── exports/                # Exports CSV/JSON/Excel
```

---

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+
- pip

### Installation en 3 étapes

```bash
# 1. Cloner/naviguer vers le projet
cd projet_01_analyseur_csv

# 2. Créer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# 3. Installer les dépendances
pip install -r requirements.txt
```

### Lancement

```bash
# Méthode 1 : Script automatique (recommandé)
./run.sh

# Méthode 2 : Commande directe
streamlit run app.py
```

L'application s'ouvrira automatiquement sur **http://localhost:8501**

---

## 📊 Fonctionnalités

### 1. 📥 Chargement de Données
- Support CSV (tous encodages avec détection auto)
- Support Excel (.xlsx, .xls)
- Validation automatique
- Dataset exemple intégré

### 2. 🧹 Nettoyage de Données
- Suppression valeurs manquantes
- Suppression duplicatas
- Imputation (moyenne/médiane)
- Normalisation (Min-Max, Z-Score)
- Forward/Backward fill

### 3. 📈 Analyses Statistiques
- 15+ métriques descriptives
- Statistiques par colonne
- Analyse de distribution
- Détection des types de données

### 4. 🔗 Corrélations
- Pearson, Spearman, Kendall
- Matrice interactive
- Heatmap colorée

### 5. 🔍 Détection d'Anomalies
- Méthode IQR
- Z-Score
- Distance de Mahalanobis

### 6. 📊 Visualisations
- Histogrammes
- Box plots
- Scatter plots
- Heatmaps
- Et 4+ autres types

### 7. 📄 Rapports Professionnels ⭐
- **PDF** : Rapports avec tableaux stylisés
- **DOCX** : Documents Word éditables
- **HTML** : Pages web interactives
- **Recommandations** : Analyse automatique intelligente

---

## 💡 Utilisation

### Interface Streamlit

L'application comporte 7 onglets :

1. **📊 Aperçu** : Visualisation et informations générales
2. **🧹 Nettoyage** : 5 stratégies de nettoyage
3. **📈 Statistiques** : Analyses détaillées
4. **🔗 Corrélations** : 3 méthodes de corrélation
5. **🔍 Anomalies** : Détection des outliers
6. **📊 Visualisations** : 8+ types de graphiques
7. **📄 Rapports** : Génération PDF/DOCX/HTML

### Exemple Code Python

```python
from src.modern_report_generator import ModernReportGenerator
import pandas as pd

# Charger les données
df = pd.read_csv('data/exemple_ventes.csv')

# Générer un rapport PDF
gen = ModernReportGenerator(df)
gen.generate_pdf_report(
    filepath="outputs/reports/mon_rapport.pdf",
    company_name="Ma Société",
    include_charts=True
)
```

---

## 🛠️ Technologies

### Core Stack
- **Streamlit** 1.28.0 - Interface web
- **Pandas** 2.1.1 - Manipulation de données
- **NumPy** 1.25.2 - Calculs numériques
- **Plotly** 5.17.0 - Visualisations interactives
- **SciPy** 1.11.3 - Statistiques avancées

### Rapports Modernes
- **ReportLab** 4.4.4 - Génération PDF
- **python-docx** 1.2.0 - Documents Word
- **python-pptx** 1.0.2 - PowerPoint (futur)

### Utilitaires
- **chardet** 5.2.0 - Détection d'encodage
- **openpyxl** 3.1.2 - Support Excel

---

## 📚 Documentation

### Documentation Complète
Voir le dossier [`docs/`](docs/) pour toute la documentation :

- **[INDEX.md](docs/INDEX.md)** - Index de tous les documents
- **[INSTALLATION_RAPIDE.md](docs/INSTALLATION_RAPIDE.md)** - Guide en 3 minutes
- **[DOCUMENTATION_TECHNIQUE.md](docs/DOCUMENTATION_TECHNIQUE.md)** - Architecture
- **[AMELIORATIONS.md](docs/AMELIORATIONS.md)** - Nouvelles fonctionnalités
- **[CORRECTIONS_RAPPORTS.md](docs/CORRECTIONS_RAPPORTS.md)** - Corrections v2.1

### Tests
Voir le dossier [`tests/`](tests/) pour les tests :

```bash
python tests/test_rapports_corriges.py
```

---

## 🎓 Compétences Développées

### Développement
- Architecture modulaire
- POO (8 classes)
- Gestion d'erreurs robuste
- Tests automatiques

### Data Science
- Analyse statistique
- Détection d'anomalies
- Visualisation de données
- Nettoyage de données

### Technologies
- Streamlit (web apps)
- Pandas & NumPy
- Plotly (viz interactives)
- ReportLab (PDF)
- python-docx (Word)

---

## 📈 Statistiques du Projet

- **Lignes de code** : ~3,000+
- **Modules Python** : 9
- **Fichiers de documentation** : 12
- **Tests automatiques** : 4+
- **Formats d'export** : 6
- **Types de visualisations** : 8+

---

## 🐛 Résolution de Problèmes

### Erreur : Module non trouvé
```bash
pip install -r requirements.txt
```

### Erreur : Port déjà utilisé
```bash
streamlit run app.py --server.port 8502
```

### Problèmes d'encodage
L'application détecte automatiquement l'encodage avec `chardet`.

---

## 🔄 Versions

- **v1.0** - Projet initial complet
- **v2.0** - Ajout rapports modernes (PDF, DOCX, HTML)
- **v2.1** - Corrections tableaux et emojis ✅ **Current**

---

## 🤝 Contribution

Ce projet fait partie du défi "50 Projets Python".

### Améliorations Possibles
- [ ] Export PowerPoint avec slides
- [ ] Graphiques intégrés dans PDF
- [ ] Templates personnalisables
- [ ] API REST
- [ ] Support bases de données SQL

---

## 📞 Support

### Documentation
- 📖 [Guide d'installation](docs/INSTALLATION_RAPIDE.md)
- 🔧 [Documentation technique](docs/DOCUMENTATION_TECHNIQUE.md)
- ✨ [Améliorations](docs/AMELIORATIONS.md)

### Tests
```bash
python tests/test_rapports_corriges.py
```

---

## 📄 License

MIT License - Voir le fichier LICENSE pour plus de détails.

---

## 🎉 Statut

**✅ Production-Ready** - Le projet est complet et prêt pour une utilisation professionnelle.

**Dernière mise à jour** : 27 octobre 2025  
**Version** : 2.1 (Corrections Appliquées)

---

**Fait avec ❤️ et Python** 🐍
