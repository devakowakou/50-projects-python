import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.api_client import APIClient

st.set_page_config(page_title="Dashboard Principal", page_icon="📊", layout="wide")

st.title("📊 Dashboard Principal")

api = APIClient()

try:
    health = api.get_health()
    if health.get('status') == 'healthy':
        st.success("✅ API connectée")
    else:
        st.error("❌ API non disponible")
        st.stop()
except Exception as e:
    st.error(f"❌ Impossible de se connecter à l'API: {e}")
    st.stop()

st.markdown("---")

# Statistiques principales
try:
    stats = api.get_overview_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Requêtes", f"{stats['total_requests']:,}")
    
    with col2:
        st.metric("IPs Uniques", f"{stats['unique_ips']:,}")
    
    with col3:
        st.metric("Taux d'erreur", f"{stats['error_rate']}%", 
                 delta=f"-{stats['error_rate']}%" if stats['error_rate'] < 5 else f"+{stats['error_rate']}%",
                 delta_color="inverse")
    
    with col4:
        if stats['avg_response_time']:
            st.metric("Temps de réponse moyen", f"{stats['avg_response_time']:.0f}ms")
        else:
            st.metric("Temps de réponse moyen", "N/A")
    
except Exception as e:
    st.error(f"Erreur lors du chargement des stats: {e}")

st.markdown("---")

# Graphiques
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Timeline des requêtes")
    try:
        timeline_data = api.get_requests_timeline(days=7)
        if timeline_data:
            df_timeline = pd.DataFrame(timeline_data)
            fig = px.line(df_timeline, x='hour', y='count', 
                         title="Requêtes par heure (7 derniers jours)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée de timeline disponible")
    except Exception as e:
        st.error(f"Erreur timeline: {e}")

with col_right:
    st.subheader("🎯 Distribution des codes HTTP")
    try:
        status_dist = api.get_status_distribution()
        if status_dist:
            df_status = pd.DataFrame(status_dist)
            fig = px.pie(df_status, values='count', names='status',
                        title="Répartition des codes de statut")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée de distribution disponible")
    except Exception as e:
        st.error(f"Erreur distribution: {e}")

st.markdown("---")

# Top URLs
st.subheader("🔝 Top 10 URLs les plus visitées")
try:
    top_urls = api.get_top_urls(limit=10)
    if top_urls:
        df_urls = pd.DataFrame(top_urls)
        fig = px.bar(df_urls, x='count', y='url', orientation='h',
                    title="URLs par nombre de requêtes")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée d'URLs disponible")
except Exception as e:
    st.error(f"Erreur top URLs: {e}")

st.markdown("---")

# Logs récents
st.subheader("📋 Logs Récents")
try:
    recent_logs = api.get_recent_logs(limit=20)
    if recent_logs:
        df_logs = pd.DataFrame(recent_logs)
        st.dataframe(df_logs, use_container_width=True, height=400)
    else:
        st.info("Aucun log récent disponible")
except Exception as e:
    st.error(f"Erreur logs récents: {e}")
