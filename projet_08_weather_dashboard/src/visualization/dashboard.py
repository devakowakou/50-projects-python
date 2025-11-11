import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.api.weather_api import WeatherAPI
from src.database.db_manager import DatabaseManager
from src.utils.config import Config
from src.visualization.charts import WeatherCharts
from src.utils.helpers import Cache, get_weather_emoji, format_wind_direction

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Météo",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

class WeatherDashboard:
    """Dashboard météo Streamlit"""
    
    def __init__(self):
        """Initialise le dashboard"""
        # Initialiser l'API et la DB
        try:
            Config.validate()
            self.api = WeatherAPI()
            self.db = DatabaseManager()
            self.charts = WeatherCharts()
        except ValueError as e:
            st.error(f"❌ {e}")
            st.stop()
        
        # Variables de session
        if 'selected_cities' not in st.session_state:
            st.session_state.selected_cities = ['Paris']
        if 'units' not in st.session_state:
            st.session_state.units = 'metric'
        if 'error_message' not in st.session_state:
            st.session_state.error_message = None
    
    def render_sidebar(self):
        """Affiche la barre latérale"""
        with st.sidebar:
            st.image("https://img.icons8.com/clouds/100/000000/sun.png", width=100)
            st.title("⚙️ Configuration")
            
            # Sélection de la ville
            st.subheader("📍 Ville")
            
            # Suggestions de villes populaires
            popular_cities = [
                'Paris', 'London', 'New York', 'Tokyo', 'Berlin',
                'Madrid', 'Rome', 'Amsterdam', 'Brussels', 'Lyon',
                'Marseille', 'Nice', 'Toulouse', 'Bordeaux'
            ]
            
            city_input = st.text_input(
                "Rechercher une ville",
                placeholder="Ex: London, Tokyo, New York...",
                help="Entrez le nom d'une ville en anglais"
            )
            
            # Afficher message d'erreur si présent
            if st.session_state.error_message:
                st.error(st.session_state.error_message)
                st.session_state.error_message = None
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔍 Rechercher", type="primary"):
                    if city_input:
                        # Vérifier que la ville existe avant de l'ajouter
                        test_weather = self.api.get_current_weather(city_input, st.session_state.units)
                        if test_weather:
                            if city_input not in st.session_state.selected_cities:
                                st.session_state.selected_cities.append(city_input)
                                st.success(f"✅ {city_input} ajoutée!")
                                st.rerun()
                            else:
                                st.warning(f"⚠️ {city_input} déjà dans la liste")
                        else:
                            st.session_state.error_message = f"❌ Ville '{city_input}' introuvable. Suggestions: {', '.join(popular_cities[:5])}"
                            st.rerun()
            
            with col2:
                # Bouton pour vider le champ
                if st.button("🗑️ Effacer"):
                    st.rerun()
            
            # Villes populaires en boutons
            with st.expander("🌍 Villes populaires"):
                for i in range(0, len(popular_cities), 3):
                    cols = st.columns(3)
                    for j, col in enumerate(cols):
                        if i + j < len(popular_cities):
                            city = popular_cities[i + j]
                            with col:
                                if st.button(city, key=f"pop_{city}", use_container_width=True):
                                    if city not in st.session_state.selected_cities:
                                        st.session_state.selected_cities.append(city)
                                        st.rerun()
            
            # Liste des villes sélectionnées
            st.subheader("🗺️ Villes suivies")
            if not st.session_state.selected_cities:
                st.info("Aucune ville sélectionnée")
            else:
                for city in st.session_state.selected_cities:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"• {city}")
                    with col2:
                        if st.button("❌", key=f"remove_{city}"):
                            st.session_state.selected_cities.remove(city)
                            st.rerun()
            
            # Unités
            st.subheader("🌡️ Unités")
            units_options = {
                'metric': 'Celsius (°C)',
                'imperial': 'Fahrenheit (°F)',
                'standard': 'Kelvin (K)'
            }
            st.session_state.units = st.selectbox(
                "Système",
                options=list(units_options.keys()),
                format_func=lambda x: units_options[x],
                index=0
            )
            
            # Historique
            st.subheader("📊 Historique")
            all_cities = self.db.get_all_cities()
            if all_cities:
                st.write(f"**{len(all_cities)}** villes en base")
                st.caption(", ".join(all_cities[:5]))
            else:
                st.info("Aucune donnée historique")
            
            # Actions
            st.subheader("🔧 Actions")
            
            # Informations sur le cache
            cache_size = Cache.size()
            if cache_size > 0:
                st.info(f"💾 Cache: {cache_size} entrée(s)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔄 Actualiser", use_container_width=True):
                    Cache.clear()
                    st.cache_data.clear()
                    st.success("✅ Cache vidé!")
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Nettoyer", use_container_width=True):
                    self.db.cleanup_old_data(days=30)
                    st.success("✅ Historique nettoyé!")
    
    def render_current_weather(self, city: str):
        """Affiche la météo actuelle pour une ville"""
        with st.spinner(f"Chargement météo pour {city}..."):
            weather = self.api.get_current_weather(city, st.session_state.units)
            
            if not weather:
                st.error(f"❌ Impossible de récupérer la météo pour **{city}**")
                st.warning("💡 Suggestions: Vérifiez l'orthographe ou essayez en anglais (ex: 'London' au lieu de 'Londres')")
                
                # Proposer de retirer la ville
                if st.button(f"Retirer {city} de la liste", key=f"remove_error_{city}"):
                    st.session_state.selected_cities.remove(city)
                    st.rerun()
                return
            
            # Sauvegarder en base
            self.db.save_current_weather(weather)
            
            # Affichage
            emoji = get_weather_emoji(weather['description'])
            st.markdown(f"### {emoji} {weather['city']}, {weather['country']}")
            
            # Icône météo
            icon_url = f"https://openweathermap.org/img/wn/{weather['icon']}@4x.png"
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.image(icon_url, width=150)
            
            with col2:
                st.metric(
                    label="Température",
                    value=f"{weather['temperature']}{weather['unit_symbol']}",
                    delta=f"Ressenti: {weather['feels_like']}{weather['unit_symbol']}"
                )
                st.caption(f"**{weather['description']}**")
            
            with col3:
                st.metric("Min", f"{weather['temp_min']}{weather['unit_symbol']}")
                st.metric("Max", f"{weather['temp_max']}{weather['unit_symbol']}")
            
            # Détails
            st.markdown("#### 📋 Détails")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💧 Humidité", f"{weather['humidity']}%")
            
            with col2:
                st.metric("🌪️ Pression", f"{weather['pressure']} hPa")
            
            with col3:
                wind_dir = format_wind_direction(weather['wind_deg'])
                st.metric("💨 Vent", f"{weather['wind_speed']} m/s {wind_dir}")
            
            with col4:
                st.metric("☁️ Nuages", f"{weather['clouds']}%")
            
            # Lever/coucher du soleil
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.caption(f"🌅 Lever: {weather['sunrise'].strftime('%H:%M')}")
            
            with col2:
                st.caption(f"🌇 Coucher: {weather['sunset'].strftime('%H:%M')}")
            
            with col3:
                st.caption(f"👁️ Visibilité: {weather['visibility']} km")
            
            st.caption(f"_Dernière mise à jour: {weather['timestamp'].strftime('%d/%m/%Y %H:%M')}_")
            
            # Badge de cache
            if Cache.get(f"get_current_weather_{city}_{st.session_state.units}"):
                st.caption("💾 _Données en cache_")
    
    def render_forecast_with_charts(self, city: str):
        """Affiche les prévisions avec graphiques"""
        with st.spinner(f"Chargement prévisions pour {city}..."):
            forecast = self.api.get_forecast(city, st.session_state.units)
            
            if not forecast:
                st.error(f"❌ Impossible de récupérer les prévisions pour **{city}**")
                st.warning("💡 Vérifiez que le nom de la ville est correct")
                return
            
            # Sauvegarder en base
            self.db.save_forecast(
                forecast['city'],
                forecast['country'],
                forecast['forecasts'],
                forecast['units']
            )
            
            st.markdown(f"### 📅 Prévisions - {forecast['city']}")
            
            # Graphique interactif des prévisions
            fig_forecast = self.charts.create_forecast_chart(
                forecast['forecasts'],
                forecast['city'],
                forecast['unit_symbol']
            )
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            # Grouper par jour
            forecasts_by_day = {}
            for f in forecast['forecasts']:
                day = f['timestamp'].date()
                if day not in forecasts_by_day:
                    forecasts_by_day[day] = []
                forecasts_by_day[day].append(f)
            
            # Afficher par jour avec expander
            st.markdown("#### 📆 Détails par jour")
            for day, day_forecasts in list(forecasts_by_day.items())[:5]:
                with st.expander(
                    f"📆 {day.strftime('%A %d %B %Y')}",
                    expanded=(day == datetime.now().date())
                ):
                    # Créer un DataFrame pour le tableau
                    df_data = []
                    for f in day_forecasts:
                        df_data.append({
                            'Heure': f['timestamp'].strftime('%H:%M'),
                            'Temp': f"{f['temperature']}{forecast['unit_symbol']}",
                            'Ressenti': f"{f['feels_like']}{forecast['unit_symbol']}",
                            'Description': f['description'],
                            'Pluie': f"{f['pop']}%",
                            'Vent': f"{f['wind_speed']} m/s",
                            'Humidité': f"{f['humidity']}%"
                        })
                    
                    df = pd.DataFrame(df_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Stats du jour
                    temps = [f['temperature'] for f in day_forecasts]
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("🌡️ Min", f"{min(temps)}{forecast['unit_symbol']}")
                    with col2:
                        st.metric("🌡️ Max", f"{max(temps)}{forecast['unit_symbol']}")
                    with col3:
                        st.metric("🌡️ Moy", f"{sum(temps)/len(temps):.1f}{forecast['unit_symbol']}")
                    with col4:
                        max_pop = max([f['pop'] for f in day_forecasts])
                        st.metric("🌧️ Pluie max", f"{max_pop}%")
    
    def render_statistics(self, city: str):
        """Affiche les statistiques historiques"""
        st.markdown(f"### 📈 Statistiques - {city}")
        
        # Période
        period_days = st.selectbox(
            "Période",
            options=[7, 14, 30],
            format_func=lambda x: f"{x} derniers jours",
            key=f"period_{city}"
        )
        
        # Récupérer les stats
        stats = self.db.get_temperature_stats(city, days=period_days)
        
        if not stats or not stats.get('min_temp'):
            st.info("📊 Pas assez de données historiques. Revenez plus tard!")
            return
        
        # Afficher les stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🥶 Température min", f"{stats['min_temp']}°C")
        
        with col2:
            st.metric("📊 Température moyenne", f"{stats['avg_temp']}°C")
        
        with col3:
            st.metric("🥵 Température max", f"{stats['max_temp']}°C")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("💧 Humidité moyenne", f"{stats['avg_humidity']}%")
        
        with col2:
            st.metric("🌪️ Pression moyenne", f"{stats['avg_pressure']} hPa")
        
        # Historique
        history = self.db.get_weather_history(city, days=period_days)
        
        if history:
            # Graphique température avec Plotly
            st.markdown("#### 🌡️ Évolution de la température")
            fig_temp = self.charts.create_temperature_line(history, city)
            st.plotly_chart(fig_temp, use_container_width=True)
            
            # Graphique humidité/pression
            st.markdown("#### 📊 Humidité et Pression")
            fig_hum_press = self.charts.create_humidity_pressure_chart(history, city)
            st.plotly_chart(fig_hum_press, use_container_width=True)
    
    def render_advanced_visualizations(self):
        """Affiche les visualisations avancées"""
        st.markdown("## 📊 Visualisations avancées")
        
        if len(st.session_state.selected_cities) == 0:
            st.info("👈 Sélectionnez des villes pour voir les visualisations")
            return
        
        # Récupérer les données actuelles pour les jauges
        if len(st.session_state.selected_cities) == 1:
            city = st.session_state.selected_cities[0]
            current = self.api.get_current_weather(city, st.session_state.units)
            
            if current:
                st.markdown(f"### 🎯 Métriques en temps réel - {city}")
                fig_gauges = self.charts.create_weather_metrics_gauge(current)
                st.plotly_chart(fig_gauges, use_container_width=True)
        
        # Comparaison multi-villes
        if len(st.session_state.selected_cities) > 1:
            st.markdown("### 🌍 Comparaison multi-villes")
            
            period = st.slider(
                "Période de comparaison (jours)",
                min_value=1,
                max_value=30,
                value=7,
                key="compare_period"
            )
            
            # Récupérer l'historique pour chaque ville
            cities_data = {}
            for city in st.session_state.selected_cities:
                history = self.db.get_weather_history(city, days=period)
                if history:
                    cities_data[city] = history
            
            if cities_data:
                fig_comparison = self.charts.create_multi_city_comparison(
                    cities_data,
                    Config.get_units_symbol(st.session_state.units)
                )
                st.plotly_chart(fig_comparison, use_container_width=True)
                
                # Tableau comparatif
                st.markdown("#### 📋 Tableau comparatif")
                
                comparison_data = []
                for city, history in cities_data.items():
                    df = pd.DataFrame(history)
                    comparison_data.append({
                        'Ville': city,
                        'Temp Min': f"{df['temperature'].min():.1f}°C",
                        'Temp Max': f"{df['temperature'].max():.1f}°C",
                        'Temp Moy': f"{df['temperature'].mean():.1f}°C",
                        'Humidité Moy': f"{df['humidity'].mean():.0f}%",
                        'Données': len(history)
                    })
                
                comparison_df = pd.DataFrame(comparison_data)
                st.dataframe(comparison_df, use_container_width=True, hide_index=True)
            else:
                st.warning("Pas assez de données pour la comparaison")
    
    def run(self):
        """Lance le dashboard"""
        # Header
        st.markdown('<h1 class="main-header">🌤️ Dashboard Météo</h1>', unsafe_allow_html=True)
        
        # Sidebar
        self.render_sidebar()
        
        # Contenu principal
        if not st.session_state.selected_cities:
            st.info("👈 Sélectionnez une ville dans la barre latérale")
            return
        
        # Onglets
        tabs = st.tabs([
            "🌍 Météo Actuelle",
            "📅 Prévisions",
            "📈 Statistiques",
            "📊 Visualisations"
        ])
        
        with tabs[0]:
            for city in st.session_state.selected_cities:
                with st.container():
                    self.render_current_weather(city)
                    st.divider()
        
        with tabs[1]:
            for city in st.session_state.selected_cities:
                with st.container():
                    self.render_forecast_with_charts(city)
                    st.divider()
        
        with tabs[2]:
            for city in st.session_state.selected_cities:
                with st.container():
                    self.render_statistics(city)
                    st.divider()
        
        with tabs[3]:
            self.render_advanced_visualizations()
