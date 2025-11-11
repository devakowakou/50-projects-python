import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.api_client import APIClient

st.set_page_config(page_title="Analyse de Sessions", page_icon="👥", layout="wide")

st.title("👥 Analyse de Sessions Utilisateur")

api = APIClient()

hours = st.slider("Période d'analyse (heures)", 1, 168, 24)

if st.button("🔄 Analyser les sessions"):
    with st.spinner("Analyse en cours..."):
        try:
            data = api.get_sessions_analysis(hours=hours)
            
            st.success(f"✅ {data['total_logs_analyzed']} logs analysés")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Sessions", data['total_sessions'])
            
            with col2:
                st.metric("Durée moyenne", f"{data['avg_duration']:.1f}s")
            
            with col3:
                st.metric("Pages/Session", f"{data['avg_pages_per_session']:.1f}")
            
            with col4:
                st.metric("Taux de rebond", f"{data['bounce_rate']:.1f}%")
            
            st.markdown("---")
            
            st.subheader("🛤️ Parcours clients les plus fréquents")
            if data.get('conversion_paths'):
                paths_df = pd.DataFrame(data['conversion_paths'])
                st.dataframe(paths_df, use_container_width=True)
            else:
                st.info("Aucun parcours client détecté")
            
            st.markdown("---")
            
            st.subheader("📊 Détails des sessions")
            if data.get('session_details'):
                sessions_df = pd.DataFrame(data['session_details'])
                st.dataframe(sessions_df, use_container_width=True, height=400)
            
        except Exception as e:
            st.error(f"❌ Erreur lors de l'analyse: {e}")
