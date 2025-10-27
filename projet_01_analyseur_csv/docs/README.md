# 📊 Projet 1 : Analyseur CSV Professionnel

## 🎯 Description

Application web interactive pour l'analyse approfondie de fichiers CSV avec statistiques descriptives, analyse de corrélations, détection d'anomalies et visualisations dynamiques.

## ✨ Fonctionnalités

### 📥 Chargement des Données
- Upload de fichiers CSV, XLSX, XLS
- Détection automatique de l'encodage
- Support de fichiers jusqu'à 200 MB
- Validation automatique des données

### 🧹 Nettoyage des Données
- Traitement des valeurs manquantes (suppression, imputation)
- Détection et suppression des duplicatas
- Conversion de types de colonnes
- Normalisation des noms de colonnes
- Détection et traitement des outliers

### 📊 Analyses Statistiques
- **Statistiques descriptives** : moyenne, médiane, écart-type, variance
- **Mesures de position** : quartiles, percentiles, min, max
- **Mesures de forme** : skewness, kurtosis
- **Tests de normalité** : Shapiro-Wilk, Kolmogorov-Smirnov
- **Analyses par catégorie** : groupement et agrégation

### 🔗 Analyse de Corrélations
- Matrices de corrélation (Pearson, Spearman, Kendall)
- Tests de significativité statistique
- Identification des variables fortement corrélées
- Détection de multicolinéarité
- Corrélations partielles

### 🚨 Détection d'Anomalies
- **Méthode IQR** (Interquartile Range)
- **Méthode Z-Score**
- Détection d'outliers multivariés (distance de Mahalanobis)
- Comparaison des méthodes
- Suggestions de traitement

### 📈 Visualisations Interactives (Plotly)
- Histogrammes avec courbe de distribution
- Box plots pour détection d'outliers
- Scatter plots avec lignes de tendance
- Heatmaps de corrélation
- Violin plots
- Bar charts et Pie charts
- Graphiques personnalisables

### 📄 Génération de Rapports
- Export CSV des données nettoyées
- Export JSON des statistiques
- Rapports Markdown formatés
- Rapports Excel multi-feuilles

## 🏗️ Architecture

```
projet_01_analyseur_csv/
├── src/                          # Code source modulaire
│   ├── data_loader.py           # Chargement et validation
│   ├── data_cleaner.py          # Nettoyage et preprocessing
│   ├── statistical_analyzer.py  # Analyses statistiques
│   ├── correlation_analyzer.py  # Analyse de corrélations
│   ├── anomaly_detector.py      # Détection d'anomalies
│   ├── visualizer.py            # Visualisations Plotly
│   └── report_generator.py      # Génération de rapports
├── app.py                       # Application Streamlit
├── config.py                    # Configuration globale
├── requirements.txt             # Dépendances
├── data/                        # Fichiers d'exemple
│   └── exemple_ventes.csv
└── assets/                      # Ressources CSS
    └── style.css
```

## 🛠️ Technologies Utilisées

- **Frontend** : Streamlit (interface utilisateur)
- **Data Processing** : Pandas & NumPy
- **Visualisation** : Plotly (graphiques interactifs)
- **Analyse Statistique** : SciPy
- **Gestion des fichiers** : openpyxl, chardet

## 📦 Installation

### 1. Cloner le projet
```bash
cd projet_01_analyseur_csv
```

### 2. Créer un environnement virtuel (recommandé)
```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

### Lancer l'application
```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse : `http://localhost:8501`

### Guide d'utilisation

1. **Charger un fichier**
   - Cliquez sur "Upload fichier" dans la sidebar
   - Ou utilisez le fichier d'exemple fourni

2. **Explorer les données**
   - Onglet "Aperçu" : vue d'ensemble des données
   - Vérifiez les types de colonnes et les métriques de base

3. **Nettoyer les données**
   - Onglet "Nettoyage" : traiter les valeurs manquantes
   - Choisir une stratégie d'imputation

4. **Analyser**
   - Onglet "Statistiques" : statistiques descriptives complètes
   - Onglet "Corrélations" : matrice de corrélation et paires significatives
   - Onglet "Anomalies" : détecter les outliers avec IQR ou Z-Score

5. **Visualiser**
   - Onglet "Visualisations" : graphiques interactifs
   - Choisir le type de graphique adapté à vos besoins

6. **Exporter**
   - Onglet "Rapports" : télécharger les résultats
   - CSV, JSON, Markdown disponibles

## 📊 Exemple de Données

Le fichier `data/exemple_ventes.csv` contient des données de ventes avec :
- Dates de transaction
- Produits et catégories
- Quantités et prix
- Vendeurs et régions

Parfait pour tester toutes les fonctionnalités !

## 🎨 Captures d'écran

*(L'application génère automatiquement des visualisations interactives)*

## 🧪 Tests

Pour tester l'application avec vos propres données :
1. Préparez un fichier CSV avec des colonnes numériques et catégoriques
2. Lancez l'application
3. Uploadez votre fichier
4. Explorez les différents onglets

## 📝 Fonctionnalités Avancées

### Détection d'Anomalies
- **IQR** : Détecte les valeurs hors de [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
- **Z-Score** : Détecte les valeurs avec |z| > 3
- **Multivarié** : Distance de Mahalanobis pour anomalies complexes

### Analyse de Corrélation
- **Pearson** : Corrélation linéaire
- **Spearman** : Corrélation de rang (non-linéaire)
- **Kendall** : Corrélation tau de Kendall

### Statistiques Avancées
- Tests de normalité
- Intervalles de confiance
- Coefficient de variation
- Skewness et Kurtosis

## 🤝 Contribution

Ce projet fait partie du défi "50 Projets Python". Suggestions et améliorations bienvenues !

## 📚 Ressources

- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation Plotly](https://plotly.com/python/)
- [Documentation Pandas](https://pandas.pydata.org/)
- [Documentation SciPy](https://docs.scipy.org/)

## 📄 Licence

MIT License - Libre d'utilisation et de modification

## 👨‍💻 Auteur

Projet 1/50 du défi Python

---

**Fait avec ❤️ et Python** 🐍
