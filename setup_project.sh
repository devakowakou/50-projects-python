#!/bin/bash

# Nom du projet
PROJECT_NAME="projet_10_api_extractor"

# Création de la structure principale
echo "Création du projet : $PROJECT_NAME ..."
mkdir -p $PROJECT_NAME/{data/{raw,processed},src/{api_clients,processing,dashboard,utils},tests}

# Création des fichiers
touch $PROJECT_NAME/data/raw/{twitter_raw.json,reddit_raw.json}
touch $PROJECT_NAME/data/processed/cleaned_data.csv
touch $PROJECT_NAME/src/api_clients/{__init__.py,twitter_client.py,reddit_client.py}
touch $PROJECT_NAME/src/processing/{__init__.py,clean_data.py,sentiment_analysis.py,trends_extraction.py}
touch $PROJECT_NAME/src/dashboard/{__init__.py,app.py}
touch $PROJECT_NAME/src/utils/{__init__.py,config.py}
touch $PROJECT_NAME/tests/{__init__.py,test_twitter_client.py,test_reddit_client.py}
touch $PROJECT_NAME/{requirements.txt,.env.example,.gitignore,README.md,main.py}

# Message de fin
echo "✅ Structure du projet '$PROJECT_NAME' créée avec succès !"
tree $PROJECT_NAME
