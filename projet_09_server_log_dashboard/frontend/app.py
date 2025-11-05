import streamlit as st
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="Analyseur de Logs Web Avancé",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    .stAlert {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🎯 Navigation")

pages = {
    "🏠 Dashboard Principal": "pages/1_dashboard.py",
    "👥 Analyse de Sessions": "pages/2_sessions.py",
    "🔍 Détection d'Anomalies": "pages/3_anomalies.py",
    "📊 Benchmarking": "pages/4_benchmark.py",
    "💡 Insights & Recommandations": "pages/5_insights.py"
}

# Header
st.markdown('<h1 class="main-header">📊 Analyseur de Logs Web Avancé</h1>', unsafe_allow_html=True)

st.markdown("""
### 🚀 Plateforme d'Analytics Professionnelle

Transformez vos logs serveur en insights stratégiques avec :
- 📈 **Analyse en temps réel** du trafic et des performances
- 👤 **Détection automatique** des sessions et parcours clients
- 🤖 **Machine Learning** pour identifier les anomalies
- 🌐 **Benchmarking** de plateformes concurrentes
- 💡 **Recommandations intelligentes** pour optimiser votre site

---
""")

# Quick stats preview
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🟢 Statut API", "En ligne", delta="Opérationnel")

with col2:
    st.metric("📊 Pages", "5", delta="Multi-pages")

with col3:
    st.metric("🤖 ML", "Actif", delta="Anomaly Detection")

with col4:
    st.metric("🌐 Benchmark", "Ready", delta="Web Scraping")

st.info("👈 **Utilisez la barre latérale pour naviguer entre les différentes analyses**")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🔒 Projet 9/50 - Stack: Streamlit + FastAPI + PostgreSQL + Scikit-learn + Plotly</p>
</div>
""", unsafe_allow_html=True)
