import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.api_client import APIClient

st.set_page_config(page_title="Benchmarking Web", page_icon="🌐", layout="wide")

st.title("🌐 Benchmarking de Plateformes Web")

api = APIClient()

st.info("⚠️ Maximum 10 URLs - L'analyse peut prendre quelques secondes par site")

urls_input = st.text_area(
    "Entrez les URLs à analyser (une par ligne)",
    "https://akowakou-amour.vercel.app\nhttps://google.com\nhttps://github.com",
    height=150
)

if st.button("🚀 Lancer le benchmark"):
    urls = [url.strip() for url in urls_input.split('\n') if url.strip()]
    
    if not urls:
        st.error("Veuillez entrer au moins une URL")
    elif len(urls) > 10:
        st.error("Maximum 10 URLs autorisées")
    else:
        with st.spinner(f"Analyse de {len(urls)} sites en cours..."):
            try:
                data = api.benchmark_websites(urls)
                
                st.success(f"✅ {data['successful']}/{data['total_analyzed']} sites analysés avec succès")
                
                if data.get('ranking'):
                    st.subheader("🏆 Classement par performance")
                    ranking_df = pd.DataFrame(data['ranking'])
                    
                    fig = px.bar(ranking_df, x='url', y='score',
                                title="Score de performance (0-100)",
                                color='score',
                                color_continuous_scale='RdYlGn')
                    st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                
                st.subheader("📊 Résultats détaillés")
                for result in data['results']:
                    with st.expander(f"{result['url']} - {result['status']}"):
                        if result['status'] == 'success':
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Score", f"{result['performance_score']}/100")
                            
                            with col2:
                                st.metric("Temps de chargement", f"{result['load_time_ms']:.0f}ms")
                            
                            with col3:
                                st.metric("Taille page", f"{result['page_size_kb']:.1f}KB")
                            
                            st.json(result)
                        else:
                            st.error(f"Erreur: {result.get('error', 'Inconnu')}")
                
            except Exception as e:
                st.error(f"❌ Erreur lors du benchmark: {e}")
