#!/usr/bin/env python3
"""Test rapide du setup du projet."""

import sys
import os

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Tester les imports principaux."""
    try:
        from shared.config import settings
        print("✅ Config importée")
        
        from shared.database import create_tables
        print("✅ Database importée")
        
        from shared.utils import calculate_engagement_rate
        print("✅ Utils importées")
        
        print(f"✅ Configuration: API sur {settings.API_HOST}:{settings.API_PORT}")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_database():
    """Tester la création de la base de données."""
    try:
        from shared.database import create_tables, SessionLocal
        create_tables()
        
        # Test de connexion
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        print("✅ Base de données créée et connectée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def main():
    """Test principal."""
    print("🧪 Test du setup du projet Social Analytics\n")
    
    success = True
    success &= test_imports()
    success &= test_database()
    
    if success:
        print("\n🎉 Setup OK ! Vous pouvez lancer:")
        print("   Backend: cd backend && python3 main.py")
        print("   Frontend: cd frontend && python3 app.py")
    else:
        print("\n❌ Des erreurs ont été détectées")
        print("   Installez les dépendances: pip3 install -r requirements.txt")

if __name__ == "__main__":
    main()