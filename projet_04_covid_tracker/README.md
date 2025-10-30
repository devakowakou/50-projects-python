# 🦠 Projet 04 - COVID-19 Global Tracker

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)
![License](https://img.shields.io/badge/License-MIT-green)

**Projet #4 du Challenge 50 Projets Python en 25 jours**

Application web interactive de suivi et d'analyse de la pandémie COVID-19 à l'échelle mondiale avec données en temps réel.

---

## 📋 Table des matières

- [Description](#-description)
- [Fonctionnalités](#-fonctionnalités)
- [Technologies utilisées](#-technologies-utilisées)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Architecture](#-architecture)
- [Source des données](#-source-des-données)
- [Captures d'écran](#-captures-décran)
- [Auteur](#-auteur)

---

## 📖 Description

COVID-19 Global Tracker est une application de visualisation et d'analyse des données mondiales sur la pandémie COVID-19. Elle permet de suivre l'évolution des cas, des décès et des vaccinations pour plus de 200 pays avec des graphiques interactifs et des métriques en temps réel.

**Points forts :**
- 📊 Données actualisées quotidiennement (Our World in Data)
- 🌍 Suivi de 200+ pays
- 📈 Graphiques interactifs avec Plotly
- 💾 Système de cache intelligent (24h)
- 🔍 Comparaison multi-pays
- 📉 Moyennes mobiles sur 7 jours
- 🚨 Niveaux d'alerte automatiques

---

## ✨ Fonctionnalités

### 1. **Dashboard principal**
- 4 KPI clés en temps réel (cas, décès, vaccinations, niveau d'alerte)
- Sélection de pays et de période
- Métriques par million d'habitants

### 2. **Évolution temporelle**
- Graphiques de tendance avec moyennes mobiles
- Choix entre nouveaux cas/décès ou totaux cumulés
- Identification des pics épidémiques
- Statistiques détaillées par période

### 3. **Comparaison internationale**
- Comparaison jusqu'à 8 pays simultanément
- Graphiques temporels et barres comparatives
- Tableau de métriques comparatives
- Analyse des différences entre pays

### 4. **Vaccination**
- Diagramme circulaire de l'état vaccinal
- Taux de vaccination complet/partiel
- Métriques détaillées par pays

### 5. **Système intelligent**
- Cache local de données (24h) pour performances optimales
- Rafraîchissement manuel des données
- Téléchargement automatique (~90 MB)
- Gestion d'erreurs robuste

---

## 🛠️ Technologies utilisées

| Technologie | Version | Usage |
|-------------|---------|-------|
| **Python** | 3.9+ | Langage principal |
| **Streamlit** | 1.28.0 | Interface web interactive |
| **Pandas** | 2.0.0 | Manipulation de données |
| **Plotly** | 5.17.0 | Visualisations interactives |
| **Requests** | 2.31.0 | Téléchargement de données |
| **NumPy** | 1.24.0 | Calculs numériques |

---

## 📦 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/VOTRE_USERNAME/50-projects-python.git
cd 50-projects-python/projet_04_covid_tracker
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

**Note :** Premier lancement télécharge ~90 MB de données (une seule fois, ensuite cache 24h).

---

## 🚀 Utilisation

### Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur à `http://localhost:8501`

### Première utilisation

1. **Chargement initial** : Patience pendant le téléchargement des données (1-2 min)
2. **Sélectionner un pays** : Utilisez la sidebar pour choisir le pays à analyser
3. **Choisir une période** : 7 jours, 30 jours, 6 mois, 1 an ou tout l'historique
4. **Explorer les onglets** :
   - **Évolution** : Graphiques temporels d'un pays
   - **Comparaison** : Analyse multi-pays
   - **Vaccination** : État vaccinal détaillé

### Fonctionnalités avancées

- **Rafraîchir les données** : Bouton "🔄 Rafraîchir" dans la sidebar
- **Comparer jusqu'à 8 pays** : Sélection multiple dans l'onglet "Comparaison"
- **Changer de métrique** : Cas, décès, vaccinations au choix
- **Zoom/Pan** : Interactions natives sur les graphiques Plotly

---

## 🏗️ Architecture

```
projet_04_covid_tracker/
│
├── app.py                      # Application Streamlit principale
├── config.py                   # Configuration centralisée
├── requirements.txt            # Dépendances Python
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Téléchargement et cache
│   ├── analyzer.py             # Calculs et statistiques
│   └── visualizer.py           # Génération de graphiques
│
└── data/
    └── covid_data_cache.csv    # Cache local (généré)
```

### Modules clés

**`data_loader.py`** (159 lignes)
- Téléchargement depuis Our World in Data
- Système de cache 24h
- Nettoyage et validation des données

**`analyzer.py`** (185 lignes)
- Calcul de 12 métriques clés
- Moyennes mobiles sur 7 jours
- Comparaisons multi-pays
- Niveaux d'alerte automatiques

**`visualizer.py`** (249 lignes)
- 4 types de graphiques Plotly
- Timeline avec moyennes mobiles
- Comparaisons temporelles
- Diagrammes circulaires vaccination

---

## 📊 Source des données

**Our World in Data - COVID-19 Dataset**

- **URL** : https://github.com/owid/covid-19-data
- **Format** : CSV (~90 MB)
- **Mise à jour** : Quotidienne
- **Couverture** : 200+ pays depuis janvier 2020
- **Variables** : 60+ colonnes (cas, décès, tests, vaccinations, hospitalisations)

**Colonnes utilisées (14) :**
- `location`, `date`, `population`
- `total_cases`, `new_cases`
- `total_deaths`, `new_deaths`
- `total_vaccinations`, `people_vaccinated`, `people_fully_vaccinated`
- `total_cases_per_million`, `total_deaths_per_million`
- `reproduction_rate`, `icu_patients`

**Attribution :**
> Hannah Ritchie, Edouard Mathieu, Lucas Rodés-Guirao, Cameron Appel, Charlie Giattino, Esteban Ortiz-Ospina, Joe Hasell, Bobbie Macdonald, Diana Beltekian and Max Roser (2020) - "Coronavirus Pandemic (COVID-19)". Published online at OurWorldInData.org. Retrieved from: 'https://ourworldindata.org/coronavirus'

---

## 📸 Captures d'écran

### Dashboard principal
![Dashboard](docs/screenshots/dashboard.png)
*Vue d'ensemble avec métriques clés et niveau d'alerte*

### Évolution temporelle
![Evolution](docs/screenshots/evolution.png)
*Graphique avec moyenne mobile sur 7 jours*

### Comparaison pays
![Comparison](docs/screenshots/comparison.png)
*Analyse comparative de 4 pays*

### État vaccination
![Vaccination](docs/screenshots/vaccination.png)
*Diagramme circulaire du taux de vaccination*

---

## 👤 Auteur

**Votre Nom**
- GitHub : [@VOTRE_USERNAME](https://github.com/VOTRE_USERNAME)
- LinkedIn : [Votre Profil](https://linkedin.com/in/VOTRE_PROFIL)
- Email : votre.email@example.com

---

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 🙏 Remerciements

- **Our World in Data** pour les données COVID-19
- **Streamlit** pour le framework web
- **Plotly** pour les visualisations interactives
- Communauté Python pour les librairies open-source

---

## 🚀 Projets suivants

Ce projet fait partie du **Challenge 50 Projets Python en 25 jours** :

- ✅ Projet 01 : Analyseur CSV avancé
- ✅ Projet 02 : Budget Dashboard
- ✅ Projet 03 : Amazon Price Tracker
- 🔄 **Projet 04 : COVID-19 Global Tracker** *(actuel)*
- ⏳ Projet 05 : À venir...

Suivez l'avancement sur [LinkedIn](https://linkedin.com) avec #50ProjectsPython

---

**⭐ N'oubliez pas de mettre une étoile si ce projet vous a plu !**
