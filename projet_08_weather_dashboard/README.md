# 🌤️ Dashboard Météo - Projet 8

> Dashboard météo interactif professionnel avec historiques, prévisions et visualisations avancées.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

![Dashboard Preview](https://img.shields.io/badge/Status-Production_Ready-success)

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Architecture](#-architecture)
- [API & Limites](#-api--limites)
- [Dépannage](#-dépannage)
- [Contribution](#-contribution)

## 🎯 Fonctionnalités

### 🌍 Météo en temps réel
- ✅ Température actuelle et ressentie
- ✅ Min/Max quotidiens
- ✅ Humidité, pression, vent
- ✅ Lever/coucher du soleil
- ✅ Visibilité et couverture nuageuse

### 📅 Prévisions
- ✅ Prévisions sur 5 jours
- ✅ Détails par tranche de 3h
- ✅ Probabilité de précipitations
- ✅ Graphiques interactifs Plotly

### 📊 Historique & Statistiques
- ✅ Sauvegarde automatique SQLite
- ✅ Statistiques sur 7/14/30 jours
- ✅ Graphiques d'évolution
- ✅ Comparaison multi-villes

### 🎨 Interface
- ✅ Design moderne et responsive
- ✅ Multi-villes simultanées
- ✅ 3 systèmes d'unités (°C/°F/K)
- ✅ Cache intelligent (10min)
- ✅ Gestion d'erreurs robuste

## 🚀 Installation

### Prérequis
- Python 3.11 ou supérieur
- pip ou poetry
- Clé API OpenWeatherMap (gratuite)

### Installation rapide

```bash
# Cloner ou naviguer vers le projet
cd /home/dev-akw/Documents/Coding/data/50-projects-python/projet_08_weather_dashboard

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Dépendances

```txt
streamlit>=1.28.0      # Interface web
requests>=2.31.0       # Appels API
pandas>=2.1.0          # Manipulation données
plotly>=5.17.0         # Graphiques interactifs
python-dotenv>=1.0.0   # Variables d'environnement
```

## ⚙️ Configuration

### 1. Obtenir une clé API

1. Créez un compte sur [OpenWeatherMap](https://openweathermap.org/api)
2. Allez dans **API Keys**
3. Copiez votre clé (activée sous ~2h)

### 2. Configurer l'application

```bash
# Copier le template
cp .env.example .env

# Éditer avec votre clé
nano .env
```

Contenu du fichier `.env` :

```env
# API OpenWeatherMap
OPENWEATHER_API_KEY=votre_cle_ici

# Configuration par défaut
DEFAULT_CITY=Paris
DEFAULT_UNITS=metric  # metric, imperial, standard
```

### 3. Vérifier la configuration

```bash
python test_api.py
```

## 🎮 Utilisation

### Lancer le dashboard

```bash
streamlit run app.py
```

Le dashboard s'ouvre sur `http://localhost:8501`

### Tests

```bash
# Test API seule
python test_api.py

# Test complet (API + DB)
python test_complete.py
```

### Commandes utiles

```bash
# Nettoyer le cache
rm -rf data/*.db
rm -rf __pycache__ src/**/__pycache__

# Réinstaller les dépendances
pip install -r requirements.txt --upgrade
```

## 📁 Architecture

````

