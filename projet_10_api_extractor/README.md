# 📊 Extracteur de données depuis APIs publiques

Un outil Python pour collecter, analyser et visualiser des données depuis Twitter/X et Reddit.

## 🚀 Installation

```bash
# Cloner le projet
cd project10_api_extractor

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API
```

## 🔑 Configuration des APIs

### Twitter/X API
1. Créer un compte développeur : https://developer.twitter.com
2. Créer une application et récupérer les clés

### Reddit API
1. Aller sur : https://www.reddit.com/prefs/apps
2. Créer une application "script" et récupérer les identifiants

## 📖 Usage

```bash
# Lancer le dashboard
streamlit run src/dashboard/app.py

# Ou utiliser le script principal
python main.py --source twitter --query "python programming" --limit 100
```

## 🧪 Tests

```bash
pytest tests/
```

## 📂 Structure

- `data/` : Données brutes et traitées
- `src/api_clients/` : Clients pour Twitter et Reddit
- `src/processing/` : Nettoyage et analyse
- `src/dashboard/` : Interface Streamlit
- `tests/` : Tests unitaires
