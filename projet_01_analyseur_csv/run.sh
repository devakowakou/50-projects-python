#!/bin/bash
# Script de lancement rapide pour l'analyseur CSV

echo "Lancement de l'Analyseur CSV Professionnel..."
echo ""

# Vérifier si l'environnement virtuel existe
if [ ! -d ".venv" ]; then
    echo " Création de l'environnement virtuel..."
    python3 -m venv .venv
    echo " Environnement virtuel créé"
    echo ""
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Installer/mettre à jour les dépendances
echo "📥 Installation des dépendances..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo " Installation terminée"
echo ""
echo " Lancement de l'application Streamlit..."
echo " L'application s'ouvrira dans votre navigateur"
echo ""

# Lancer l'application
streamlit run app.py
