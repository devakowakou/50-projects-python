"""
Script de test simplifié pour éviter les problèmes avec pytest-dash
"""

import sys
import os
import sqlite3
import pandas as pd
import numpy as np

# Ajouter le chemin source
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_database():
    """Test basique de la base de données"""
    print("🧪 Test de la base de données...")
    
    try:
        from database.crud import DatabaseManager
        
        # Test avec base de données mémoire
        db_manager = DatabaseManager("sqlite:///:memory:")
        
        # Test création session
        session_id = db_manager.create_user_session()
        assert session_id is not None
        print("✅ Session créée avec succès")
        
        # Test sauvegarde analyse
        analysis_id = db_manager.save_analysis(
            session_id=session_id,
            symbol="AAPL",
            timeframe="1d",
            indicators={"sma": [20, 50]},
            signals={"golden_cross": True},
            chart_data={"points": 100}
        )
        assert analysis_id is not None
        print("✅ Analyse sauvegardée avec succès")
        
        # Test récupération historique
        history = db_manager.get_analysis_history(session_id)
        assert len(history) == 1
        print("✅ Historique récupéré avec succès")
        
        print("🎉 Tous les tests base de données passés!")
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False
    
    return True

def test_technical_engine():
    """Test du moteur technique"""
    print("\n🧪 Test du moteur technique...")
    
    try:
        from src.core.technical_engine import TechnicalEngine
        
        # Créer des données de test
        dates = pd.date_range(start='2024-01-01', periods=50, freq='D')
        data = pd.DataFrame({
            'Open': 100 + np.cumsum(np.random.randn(50) * 0.5),
            'High': 100 + np.cumsum(np.random.randn(50) * 0.5) + 1,
            'Low': 100 + np.cumsum(np.random.randn(50) * 0.5) - 1,
            'Close': 100 + np.cumsum(np.random.randn(50) * 0.5),
            'Volume': np.random.randint(1000000, 5000000, 50)
        }, index=dates)
        
        engine = TechnicalEngine()
        
        # Test SMA
        sma_20 = engine.calculate_sma(data, 20)
        assert len(sma_20) == len(data)
        print("✅ SMA calculée")
        
        # Test RSI
        rsi = engine.calculate_rsi(data, 14)
        assert len(rsi) == len(data)
        print("✅ RSI calculé")
        
        # Test MACD
        macd_data = engine.calculate_macd(data)
        assert 'macd' in macd_data
        print("✅ MACD calculé")
        
        # Test indicateurs multiples
        config = {
            'sma_periods': [20, 50],
            'rsi': True,
            'macd': True
        }
        result = engine.add_all_indicators(data, config)
        assert 'SMA_20' in result.columns
        assert 'RSI' in result.columns
        print("✅ Tous les indicateurs calculés")
        
        print("🎉 Tous les tests techniques passés!")
        
    except Exception as e:
        print(f"❌ Erreur moteur technique: {e}")
        return False
    
    return True

def test_signals_engine():
    """Test du moteur de signaux"""
    print("\n🧪 Test du moteur de signaux...")
    
    try:
        from src.core.signals_engine import SignalsEngine
        
        # Créer des données avec signaux artificiels
        dates = pd.date_range(start='2024-01-01', periods=50, freq='D')
        data = pd.DataFrame({
            'Close': 100 + np.arange(50) * 0.5,
            'SMA_20': 100 + np.arange(50) * 0.6,  # SMA20 > SMA50 = tendance haussière
            'SMA_50': 100 + np.arange(50) * 0.4,
            'RSI': [45] * 50,
            'MACD': [0.1] * 50,
            'MACD_Signal': [0.05] * 50
        }, index=dates)
        
        # Simuler un golden cross
        data.loc[data.index[-2], 'SMA_20'] = data.loc[data.index[-2], 'SMA_50'] - 1
        data.loc[data.index[-1], 'SMA_20'] = data.loc[data.index[-1], 'SMA_50'] + 1
        
        engine = SignalsEngine()
        
        # Test golden cross
        golden_cross = engine.detect_golden_cross(data)
        assert golden_cross is True
        print("✅ Golden Cross détecté")
        
        # Test signaux RSI
        data['RSI'] = [25] * 50  # RSI survendu
        rsi_signals = engine.detect_rsi_signals(data)
        assert rsi_signals['rsi_oversold'] is True
        print("✅ Signaux RSI détectés")
        
        # Test tous les signaux
        all_signals = engine.generate_all_signals(data)
        assert isinstance(all_signals, dict)
        print("✅ Tous les signaux générés")
        
        print("🎉 Tous les tests signaux passés!")
        
    except Exception as e:
        print(f"❌ Erreur moteur signaux: {e}")
        return False
    
    return True

def test_data_manager():
    """Test du gestionnaire de données"""
    print("\n🧪 Test du gestionnaire de données...")
    
    try:
        from src.core.data_manager import DataManager
        
        manager = DataManager()
        
        # Test récupération info symbole (mock)
        stock_info = manager.get_stock_info("AAPL")
        assert stock_info is not None
        assert 'name' in stock_info
        print("✅ Informations symbole récupérées")
        
        print("🎉 Tous les tests données passés!")
        
    except Exception as e:
        print(f"❌ Erreur gestionnaire données: {e}")
        return False
    
    return True

def main():
    """Lance tous les tests"""
    print("🚀 Lancement des tests du Stock Analysis Dashboard...\n")
    
    tests = [
        test_database,
        test_technical_engine, 
        test_signals_engine,
        test_data_manager
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} a échoué: {e}")
            results.append(False)
    
    print(f"\n{'='*50}")
    print("📊 RÉSUMUM DES TESTS")
    print(f"{'='*50}")
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{i+1}. {test.__name__}: {status}")
    
    print(f"\n🎯 Résultat final: {passed}/{total} tests passés")
    
    if passed == total:
        print("🎉 Tous les tests sont passés! L'application est prête.")
        return True
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)