#!/usr/bin/env python3
"""
Script de lancement pour la Calculatrice A/B Test
"""

import subprocess
import sys
import os

def check_dependencies():
    """Vérifie les dépendances"""
    try:
        import streamlit, pandas, numpy, scipy, plotly
        print("✅ Dépendances OK")
        return True
    except ImportError as e:
        print(f"❌ Manquant: {e}")
        print("📦 Installez: pip install -r requirements.txt")
        return False

def main():
    print("📊 A/B Test Calculator - Lancement")
    print("=" * 40)
    
    if not check_dependencies():
        sys.exit(1)
    
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