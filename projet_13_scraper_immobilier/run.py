#!/usr/bin/env python3
"""
Script de lancement pour le Scraper Immobilier
"""

import subprocess
import sys
import os

def check_dependencies():
    """Vérifie les dépendances"""
    try:
        import streamlit, pandas, numpy, plotly, requests, bs4
        print("✅ Dépendances OK")
        return True
    except ImportError as e:
        print(f"❌ Manquant: {e}")
        print("📦 Installez: pip install -r requirements.txt")
        return False

def create_data_dir():
    """Crée le dossier data"""
    if not os.path.exists("data"):
        os.makedirs("data")
        print("📁 Dossier data créé")

def main():
    print("🏠 Scraper Immobilier - Lancement")
    print("=" * 40)
    
    if not check_dependencies():
        sys.exit(1)
    
    create_data_dir()
    
    print("🚀 Lancement Streamlit...")
    print("📱 URL: http://localhost:8501")
    print("⏹️  Ctrl+C pour arrêter")
    print("=" * 40)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Arrêté")

if __name__ == "__main__":
    main()