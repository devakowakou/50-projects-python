import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.api_client import APIClient

st.set_page_config(page_title="Insights & Recommandations", page_icon="💡", layout="wide")

st.title("💡 Insights & Recommandations Intelligentes")

api = APIClient()

hours = st.slider("Période d'analyse (heures)", 1, 168, 24)

if st.button("🔍 Générer les insights"):
    with st.spinner("Analyse en cours..."):
        try:
            data = api.get_insights(hours=hours)
            
            # Score de santé
            health_score = data['health_score']
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=health_score,
                    title={'text': "Score de Santé"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "red"},
                            {'range': [50, 75], 'color': "yellow"},
                            {'range': [75, 100], 'color': "green"}
                        ],
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("Total Requêtes", f"{data['total_requests']:,}")
                
                with col_b:
                    st.metric("Taux d'erreur", f"{data['error_rate']}%")
                
                with col_c:
                    st.metric("Requêtes lentes", f"{data['slow_requests_rate']}%")
            
            st.markdown("---")
            
            # Recommandations
            st.subheader("📢 Recommandations")
            
            if data.get('recommendations'):
                for rec in data['recommendations']:
                    if rec['type'] == 'CRITICAL':
                        st.error(f"🚨 **{rec['title']}**")
                    elif rec['type'] == 'WARNING':
                        st.warning(f"⚠️ **{rec['title']}**")
                    else:
                        st.info(f"ℹ️ **{rec['title']}**")
                    
                    st.write(f"**Description:** {rec['description']}")
                    st.write(f"**Action recommandée:** {rec['action']}")
                    st.markdown("---")
            else:
                st.success("✅ Aucune recommandation critique - Tout fonctionne normalement!")
            
            # Pages les plus lentes
            if data.get('slowest_pages'):
                st.subheader("🐌 Pages les plus lentes")
                slowest_df = pd.DataFrame(data['slowest_pages'])
                
                fig = px.bar(slowest_df, x='avg_time_ms', y='url',
                            orientation='h',
                            title="Temps de réponse moyen par page",
                            labels={'avg_time_ms': 'Temps (ms)', 'url': 'URL'})
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(slowest_df, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Erreur lors de la génération des insights: {e}")
