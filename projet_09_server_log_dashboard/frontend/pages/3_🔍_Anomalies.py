import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.api_client import APIClient

st.set_page_config(page_title="Détection d'Anomalies", page_icon="🔍", layout="wide")

st.title("🔍 Détection d'Anomalies par Machine Learning")

api = APIClient()

col1, col2 = st.columns(2)

with col1:
    hours = st.slider("Période d'analyse (heures)", 1, 168, 24)

with col2:
    retrain = st.checkbox("Ré-entraîner le modèle", value=False)

if st.button("🤖 Détecter les anomalies"):
    with st.spinner("Analyse ML en cours..."):
        try:
            data = api.detect_anomalies(hours=hours, retrain=retrain)
            
            alert_level = data['alert_level']
            
            if alert_level == 'HIGH':
                st.error(f"🚨 ALERTE HAUTE: {data['anomalies_detected']} anomalies détectées!")
            elif alert_level == 'MEDIUM':
                st.warning(f"⚠️ ALERTE MOYENNE: {data['anomalies_detected']} anomalies détectées")
            else:
                st.success(f"✅ Niveau bas: {data['anomalies_detected']} anomalies détectées")
            
            st.metric("Logs analysés", data['total_logs_analyzed'])
            
            st.markdown("---")
            
            if data.get('anomalies'):
                st.subheader("🔴 Anomalies détectées")
                
                for idx, anomaly in enumerate(data['anomalies'][:10], 1):
                    with st.expander(f"Anomalie #{idx} - Sévérité: {anomaly['severity']}"):
                        st.write(f"**Description:** {anomaly['description']}")
                        st.write(f"**Score:** {anomaly['score']:.3f}")
                        st.json(anomaly['features'])
            else:
                st.info("Aucune anomalie majeure détectée")
            
        except Exception as e:
            st.error(f"❌ Erreur lors de la détection: {e}")
