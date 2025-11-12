#!/usr/bin/env python3
"""
Script de lancement pour le Dashboard E-commerce KPIs
"""

import subprocess
import sys
import os

def check_dependencies():
    """Vérifie si les dépendances sont installées"""
    try:
        import streamlit
        import pandas
        import plotly
        import numpy
        print("✅ Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("📦 Installez les dépendances avec: pip install -r requirements.txt")
        return False

def generate_data_if_needed():
    """Génère les données si elles n'existent pas"""
    if not os.path.exists("data/transactions.json") or not os.path.exists("data/sessions.json"):
        print("🔄 Génération des données e-commerce...")
        from src.data_generator import generate_sample_data
        generate_sample_data()
        print("✅ Données générées avec succès!")
    else:
        print("✅ Données déjà présentes")

def main():
    """Fonction principale"""
    print("🛒 Dashboard E-commerce KPIs - Lancement")
    print("=" * 50)
    
    # Vérification des dépendances
    if not check_dependencies():
        sys.exit(1)
    
    # Génération des données si nécessaire
    generate_data_if_needed()
    
    # Lancement de Streamlit
    print("🚀 Lancement du dashboard Streamlit...")
    print("📱 Ouvrez votre navigateur sur: http://localhost:8501")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard arrêté")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du lancement: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()  