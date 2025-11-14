"""
Tests pour le dashboard e-commerce KPIs
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.data_generator import EcommerceDataGenerator
from src.kpi_calculator import EcommerceKPICalculator

def test_data_generation():
    """Test de génération des données"""
    print("🧪 Test génération des données...")
    
    generator = EcommerceDataGenerator()
    
    # Test produits
    products = generator.generate_products(10)
    assert len(products) == 10
    assert 'product_id' in products.columns
    assert 'price' in products.columns
    print("✅ Génération produits OK")
    
    # Test clients
    customers = generator.generate_customers(50)
    assert len(customers) == 50
    assert 'customer_id' in customers.columns
    print("✅ Génération clients OK")
    
    # Test commandes
    orders, order_items, visitors = generator.generate_orders(products, customers, 100)
    assert len(orders) == 100
    assert len(order_items) > 0
    assert len(visitors) > len(orders)  # Plus de visiteurs que de commandes
    print("✅ Génération commandes OK")
    
    return products, customers, orders, order_items, visitors

def test_kpi_calculations():
    """Test des calculs de KPIs"""
    print("\n🧪 Test calculs KPIs...")
    
    # Générer des données de test
    generator = EcommerceDataGenerator()
    products = generator.generate_products(20)
    customers = generator.generate_customers(100)
    orders, order_items, visitors = generator.generate_orders(products, customers, 200)
    
    # Initialiser le calculateur
    calc = EcommerceKPICalculator(orders, order_items, visitors, products)
    
    # Test KPIs principaux
    kpis = calc.calculate_main_kpis()
    
    assert kpis['total_revenue'] > 0
    assert kpis['total_orders'] == 200
    assert kpis['avg_order_value'] > 0
    assert kpis['total_visitors'] > 200
    assert 0 <= kpis['conversion_rate'] <= 100
    print("✅ KPIs principaux OK")
    
    # Test évolution
    evolution = calc.calculate_evolution(30)
    assert 'total_revenue_evolution' in evolution
    print("✅ Calcul évolution OK")
    
    # Test CA par période
    revenue_by_period = calc.get_revenue_by_period('D', 30)
    assert len(revenue_by_period) > 0
    print("✅ CA par période OK")
    
    # Test top produits
    top_products = calc.get_top_products(5, 30)
    assert len(top_products) <= 5
    print("✅ Top produits OK")
    
    # Test CA par catégorie
    revenue_by_category = calc.get_revenue_by_category(30)
    assert len(revenue_by_category) > 0
    print("✅ CA par catégorie OK")
    
    # Test conversion par canal
    conversion_by_channel = calc.get_conversion_by_channel(30)
    assert len(conversion_by_channel) > 0
    print("✅ Conversion par canal OK")
    
    return kpis

def test_data_consistency():
    """Test de cohérence des données"""
    print("\n🧪 Test cohérence des données...")
    
    generator = EcommerceDataGenerator()
    products = generator.generate_products(10)
    customers = generator.generate_customers(20)
    orders, order_items, visitors = generator.generate_orders(products, customers, 50)
    
    # Vérifier que tous les produits dans order_items existent
    product_ids_in_orders = set(order_items['product_id'].unique())
    product_ids_available = set(products['product_id'].unique())
    assert product_ids_in_orders.issubset(product_ids_available)
    print("✅ Cohérence produits OK")
    
    # Vérifier que tous les clients dans orders existent
    customer_ids_in_orders = set(orders['customer_id'].unique())
    customer_ids_available = set(customers['customer_id'].unique())
    assert customer_ids_in_orders.issubset(customer_ids_available)
    print("✅ Cohérence clients OK")
    
    # Vérifier que tous les order_ids dans order_items existent dans orders
    order_ids_in_items = set(order_items['order_id'].unique())
    order_ids_available = set(orders['order_id'].unique())
    assert order_ids_in_items.issubset(order_ids_available)
    print("✅ Cohérence commandes OK")

def test_edge_cases():
    """Test des cas limites"""
    print("\n🧪 Test cas limites...")
    
    # Test avec données vides
    empty_df = pd.DataFrame()
    products = pd.DataFrame({'product_id': ['P1'], 'name': ['Test'], 'category': ['Test'], 'price': [10], 'cost': [5]})
    
    try:
        calc = EcommerceKPICalculator(empty_df, empty_df, empty_df, products)
        kpis = calc.calculate_main_kpis()
        assert kpis['total_revenue'] == 0
        assert kpis['total_orders'] == 0
        assert kpis['conversion_rate'] == 0
        print("✅ Gestion données vides OK")
    except Exception as e:
        print(f"❌ Erreur données vides: {e}")
    
    # Test avec une seule commande
    generator = EcommerceDataGenerator()
    products = generator.generate_products(5)
    customers = generator.generate_customers(5)
    orders, order_items, visitors = generator.generate_orders(products, customers, 1)
    
    calc = EcommerceKPICalculator(orders, order_items, visitors, products)
    kpis = calc.calculate_main_kpis()
    assert kpis['total_orders'] == 1
    print("✅ Une seule commande OK")

def run_performance_test():
    """Test de performance avec beaucoup de données"""
    print("\n🧪 Test performance...")
    
    import time
    start_time = time.time()
    
    generator = EcommerceDataGenerator()
    products = generator.generate_products(500)
    customers = generator.generate_customers(2000)
    orders, order_items, visitors = generator.generate_orders(products, customers, 10000)
    
    generation_time = time.time() - start_time
    print(f"⏱️ Génération 10k commandes: {generation_time:.2f}s")
    
    start_time = time.time()
    calc = EcommerceKPICalculator(orders, order_items, visitors, products)
    kpis = calc.calculate_main_kpis()
    
    calculation_time = time.time() - start_time
    print(f"⏱️ Calcul KPIs: {calculation_time:.2f}s")
    
    if generation_time < 10 and calculation_time < 2:
        print("✅ Performance acceptable")
    else:
        print("⚠️ Performance à optimiser")

def main():
    """Exécute tous les tests"""
    print("🚀 Lancement des tests du dashboard e-commerce\n")
    
    try:
        # Tests principaux
        products, customers, orders, order_items, visitors = test_data_generation()
        kpis = test_kpi_calculations()
        test_data_consistency()
        test_edge_cases()
        
        # Test de performance (optionnel)
        run_performance_test()
        
        print("\n🎉 Tous les tests sont passés avec succès!")
        print(f"\n📊 Exemple de KPIs calculés:")
        print(f"   💰 CA: {kpis['total_revenue']:,.2f} €")
        print(f"   🛒 Panier moyen: {kpis['avg_order_value']:.2f} €")
        print(f"   📈 Conversion: {kpis['conversion_rate']:.2f}%")
        print(f"   📦 Commandes: {kpis['total_orders']:,}")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()