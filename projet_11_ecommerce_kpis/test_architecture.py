#!/usr/bin/env python3
"""
Test de l'architecture du Dashboard E-commerce KPIs
"""

import json
import os
from datetime import datetime

def test_data_generation():
    """Test de la génération de données"""
    print("🧪 Test 1: Génération de données")
    
    # Import et génération
    from src.data_generator import generate_sample_data
    transactions, sessions = generate_sample_data()
    
    # Vérifications
    assert len(transactions) == 10000, f"Expected 10000 transactions, got {len(transactions)}"
    assert len(sessions) == 30000, f"Expected 30000 sessions, got {len(sessions)}"
    
    # Vérification structure transaction
    tx = transactions[0]
    required_fields = ['id', 'date', 'customer_id', 'amount', 'category', 'source', 'products_count']
    for field in required_fields:
        assert field in tx, f"Missing field {field} in transaction"
    
    # Vérification structure session
    sess = sessions[0]
    required_fields = ['id', 'date', 'source', 'converted', 'pages_viewed']
    for field in required_fields:
        assert field in sess, f"Missing field {field} in session"
    
    print("   ✅ Génération de données OK")
    return transactions, sessions

def test_kpi_calculator():
    """Test du calculateur KPIs (sans pandas)"""
    print("🧪 Test 2: Calculateur KPIs (structure)")
    
    # Test de l'import
    try:
        from src.kpi_calculator import EcommerceKPICalculator
        print("   ✅ Import KPI Calculator OK")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    return True

def test_visualizations():
    """Test du module visualisations"""
    print("🧪 Test 3: Module visualisations (structure)")
    
    try:
        from src.visualizations import EcommerceCharts
        print("   ✅ Import Visualizations OK")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    return True

def test_utils():
    """Test du module utilitaires"""
    print("🧪 Test 4: Module utilitaires (structure)")
    
    try:
        from src.utils import DataLoader, DateFilter, MetricFormatter, ExportUtils
        print("   ✅ Import Utils OK")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    return True

def test_config():
    """Test de la configuration"""
    print("🧪 Test 5: Configuration")
    
    try:
        import config
        
        # Vérification des constantes
        assert hasattr(config, 'DATA_CONFIG'), "Missing DATA_CONFIG"
        assert hasattr(config, 'TRAFFIC_SOURCES'), "Missing TRAFFIC_SOURCES"
        assert hasattr(config, 'PRODUCT_CATEGORIES'), "Missing PRODUCT_CATEGORIES"
        
        # Vérification des valeurs
        assert len(config.TRAFFIC_SOURCES) == 4, f"Expected 4 traffic sources, got {len(config.TRAFFIC_SOURCES)}"
        assert len(config.PRODUCT_CATEGORIES) == 10, f"Expected 10 categories, got {len(config.PRODUCT_CATEGORIES)}"
        
        print("   ✅ Configuration OK")
        return True
    except Exception as e:
        print(f"   ❌ Config test failed: {e}")
        return False

def test_file_structure():
    """Test de la structure des fichiers"""
    print("🧪 Test 6: Structure des fichiers")
    
    required_files = [
        'app.py',
        'config.py', 
        'requirements.txt',
        'README.md',
        'src/data_generator.py',
        'src/kpi_calculator.py',
        'src/visualizations.py',
        'src/utils.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"   ❌ Fichiers manquants: {missing_files}")
        return False
    
    print("   ✅ Structure des fichiers OK")
    return True

def calculate_basic_kpis(transactions, sessions):
    """Calcul basique des KPIs sans pandas"""
    print("🧪 Test 7: Calcul KPIs basique")
    
    # CA Total
    total_revenue = sum(tx['amount'] for tx in transactions)
    
    # Panier moyen
    avg_order_value = total_revenue / len(transactions)
    
    # Taux de conversion
    converted_sessions = sum(1 for sess in sessions if sess['converted'])
    conversion_rate = (converted_sessions / len(sessions)) * 100
    
    print(f"   💰 CA Total: €{total_revenue:,.0f}")
    print(f"   🛒 Panier Moyen: €{avg_order_value:.0f}")
    print(f"   🎯 Taux Conversion: {conversion_rate:.1f}%")
    print(f"   📦 Transactions: {len(transactions):,}")
    print(f"   👥 Sessions: {len(sessions):,}")
    print("   ✅ Calculs KPIs basiques OK")
    
    return True

def main():
    """Test principal"""
    print("🛒 Test Architecture Dashboard E-commerce KPIs")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 7
    
    try:
        # Test 1: Génération de données
        transactions, sessions = test_data_generation()
        tests_passed += 1
        
        # Test 2: KPI Calculator
        if test_kpi_calculator():
            tests_passed += 1
        
        # Test 3: Visualisations
        if test_visualizations():
            tests_passed += 1
        
        # Test 4: Utils
        if test_utils():
            tests_passed += 1
        
        # Test 5: Config
        if test_config():
            tests_passed += 1
        
        # Test 6: Structure fichiers
        if test_file_structure():
            tests_passed += 1
        
        # Test 7: KPIs basiques
        if calculate_basic_kpis(transactions, sessions):
            tests_passed += 1
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
    
    # Résultats
    print("=" * 60)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 Tous les tests sont passés ! Architecture validée !")
        print("🚀 Vous pouvez lancer: python run.py")
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()