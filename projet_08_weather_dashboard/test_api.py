#!/usr/bin/env python3
"""Script de test pour l'API météo"""

from src.api.weather_api import WeatherAPI
from src.utils.config import Config

def main():
    print("🧪 Test de l'API OpenWeatherMap\n")
    print("=" * 50)
    
    # Valider la config
    try:
        Config.validate()
        print("✅ Configuration valide")
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    # Créer l'instance API
    api = WeatherAPI()
    
    # Test 1: Météo actuelle
    print("\n📍 Test 1: Météo actuelle pour Paris")
    print("-" * 50)
    current = api.get_current_weather('Paris')
    
    if current:
        print(f"✅ Ville: {current['city']}, {current['country']}")
        print(f"🌡️  Température: {current['temperature']}{current['unit_symbol']}")
        print(f"🤔 Ressenti: {current['feels_like']}{current['unit_symbol']}")
        print(f"☁️  Description: {current['description']}")
        print(f"💧 Humidité: {current['humidity']}%")
        print(f"💨 Vent: {current['wind_speed']} m/s")
    else:
        print("❌ Échec récupération météo actuelle")
        return
    
    # Test 2: Prévisions
    print("\n📅 Test 2: Prévisions pour Paris (5 jours)")
    print("-" * 50)
    forecast = api.get_forecast('Paris')
    
    if forecast:
        print(f"✅ Ville: {forecast['city']}, {forecast['country']}")
        print(f"📊 Nombre de prévisions: {len(forecast['forecasts'])}")
        
        # Afficher les 3 premières prévisions
        print("\n🔮 Premières prévisions:")
        for i, f in enumerate(forecast['forecasts'][:3], 1):
            print(f"\n  {i}. {f['timestamp'].strftime('%d/%m %H:%M')}")
            print(f"     Temp: {f['temperature']}{forecast['unit_symbol']} - {f['description']}")
            print(f"     Pluie: {f['pop']}% | Vent: {f['wind_speed']} m/s")
    else:
        print("❌ Échec récupération prévisions")
        return
    
    print("\n" + "=" * 50)
    print("✅ Tous les tests réussis! 🎉")
    print("\n💡 Prochaine étape: Créer la base de données pour l'historique")

if __name__ == "__main__":
    main()
