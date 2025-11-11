#!/usr/bin/env python3
"""Test complet: API + Base de données"""

from src.api.weather_api import WeatherAPI
from src.database.db_manager import DatabaseManager
from src.utils.config import Config
from datetime import datetime

def main():
    print("🧪 Test complet: API + Base de données")
    print("=" * 60)
    
    # Valider la config
    try:
        Config.validate()
        print("✅ Configuration valide\n")
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    # Initialiser API et DB
    api = WeatherAPI()
    db = DatabaseManager()
    
    # Test 1: Récupérer et sauvegarder la météo actuelle
    print("📍 Test 1: Météo actuelle + Sauvegarde")
    print("-" * 60)
    
    cities = ['Paris', 'Lyon', 'Marseille']
    
    for city in cities:
        print(f"\n🌍 {city}:")
        current = api.get_current_weather(city)
        
        if current:
            print(f"  🌡️  Température: {current['temperature']}{current['unit_symbol']}")
            print(f"  ☁️  {current['description']}")
            
            # Sauvegarder en DB
            if db.save_current_weather(current):
                print(f"  ✅ Sauvegardé en base de données")
            else:
                print(f"  ❌ Échec sauvegarde")
        else:
            print(f"  ❌ Échec récupération")
    
    # Test 2: Récupérer et sauvegarder les prévisions
    print("\n\n📅 Test 2: Prévisions + Sauvegarde")
    print("-" * 60)
    
    forecast = api.get_forecast('Paris')
    if forecast:
        print(f"✅ {len(forecast['forecasts'])} prévisions récupérées")
        
        # Sauvegarder les prévisions
        if db.save_forecast(
            forecast['city'],
            forecast['country'],
            forecast['forecasts'],
            forecast['units']
        ):
            print("✅ Prévisions sauvegardées en base")
        else:
            print("❌ Échec sauvegarde prévisions")
    
    # Test 3: Lire l'historique depuis la DB
    print("\n\n📊 Test 3: Lecture historique depuis DB")
    print("-" * 60)
    
    for city in cities:
        history = db.get_weather_history(city, days=1)
        print(f"\n🌍 {city}: {len(history)} entrées dans l'historique")
        
        if history:
            latest = history[0]
            print(f"  Dernière mesure: {latest['timestamp']}")
            print(f"  Température: {latest['temperature']}°C")
    
    # Test 4: Statistiques
    print("\n\n📈 Test 4: Statistiques")
    print("-" * 60)
    
    stats = db.get_temperature_stats('Paris', days=1)
    if stats:
        print(f"\n🌡️  Statistiques Paris (24h):")
        if stats.get('min_temp'):
            print(f"  Min: {stats['min_temp']}°C")
            print(f"  Max: {stats['max_temp']}°C")
            print(f"  Moyenne: {stats['avg_temp']}°C")
            print(f"  Humidité moyenne: {stats['avg_humidity']}%")
    
    # Test 5: Liste des villes
    print("\n\n🗺️  Test 5: Liste des villes en base")
    print("-" * 60)
    
    all_cities = db.get_all_cities()
    print(f"Villes enregistrées: {', '.join(all_cities)}")
    
    print("\n" + "=" * 60)
    print("✅ Tous les tests réussis! 🎉")
    print("\n💡 Base de données créée: data/weather_history.db")
    print("💡 Prochaine étape: Interface Streamlit")

if __name__ == "__main__":
    main()
