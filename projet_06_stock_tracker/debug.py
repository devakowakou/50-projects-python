#!/usr/bin/env python3
"""
Script de debug pour tester les composants
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.crud import DatabaseManager
from src.core.data_manager import DataManager
from src.core.technical_engine import TechnicalEngine
import config

def test_components():
    print("🧪 Test des composants...")
    
    try:
        # Test base de données
        print("1. Test base de données...")
        db = DatabaseManager(config.DATABASE_URL)
        session_id = db.create_user_session()
        print(f"   ✅ Session créée: {session_id}")
        
        # Test data manager
        print("2. Test data manager...")
        dm = DataManager()
        data = dm.get_stock_data("AAPL", period="1mo")
        print(f"   ✅ Données récupérées: {len(data)} points")
        
        # Test technical engine
        print("3. Test technical engine...")
        te = TechnicalEngine()
        analyzed_data = te.add_all_indicators(data, config.INDICATOR_CONFIG)
        print(f"   ✅ Indicateurs calculés: {len(analyzed_data.columns)} colonnes")
        
        print("🎉 Tous les tests passent!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_components()