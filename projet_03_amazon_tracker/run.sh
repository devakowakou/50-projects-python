#!/bin/bash

# Script de lancement du Amazon Price Tracker

echo "🚀 Démarrage du Amazon Price Tracker..."

# Vérifier si le virtual environment existe
if [ ! -d "../.venv" ]; then
    echo "❌ Virtual environment non trouvé dans ../.venv"
    echo "Créez-le avec: python3 -m venv ../.venv"
    exit 1
fi

# Activer le virtual environment
source ../.venv/bin/activate

# Installer les dépendances si nécessaire
echo "📦 Vérification des dépendances..."
pip install -q -r requirements.txt

# Vérifier si .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Fichier .env non trouvé"
    echo "Copiez .env.example vers .env et configurez vos paramètres"
    echo ""
fi

# Lancer l'application
echo "✅ Lancement de Streamlit..."
streamlit run app.py
