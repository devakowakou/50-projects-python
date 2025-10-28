#!/bin/bash

# Script de lancement rapide pour le Budget Dashboard

echo "🚀 Lancement du Budget Dashboard..."
echo ""

# Vérifier si l'environnement virtuel existe
if [ ! -d ".venv" ]; then
    echo "  Environnement virtuel non trouvé"
    echo " Création de l'environnement virtuel..."
    python3 -m venv .venv
    
    echo "📥 Installation des dépendances..."
    source .venv/bin/activate
    pip install -r requirements.txt
else
    echo " Environnement virtuel trouvé"
    source .venv/bin/activate
fi

# Générer les données exemple si nécessaire
if [ ! -f "data/exemple_transactions.json" ]; then
    echo " Génération des données exemple..."
    python3 generate_example_data.py
fi

echo ""
echo " Ouverture de l'application..."
echo "📍 URL: http://localhost:8501"
echo ""
echo " Appuyez sur Ctrl+C pour arrêter l'application"
echo ""

# Lancer Streamlit
streamlit run app.py
