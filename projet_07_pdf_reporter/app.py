"""
Application Streamlit - Générateur de rapports PDF
"""
import streamlit as st
from src.ui.pages import generation_page, history_page, config_page
from src.ui.components import sidebar_info
from src.ui.styles import inject_custom_css

# Configuration de la page
st.set_page_config(
    page_title="PDF Reporter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injection du CSS
inject_custom_css()

def main():
    """Point d'entrée principal de l'application"""
    
    st.title("📊 Générateur de Rapports PDF")
    st.markdown("---")
    
    # Sidebar pour navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Choisir une page",
            ["📊 Génération", "📚 Historique", "⚙️ Configuration"],
            label_visibility="collapsed"
        )
        
        sidebar_info()
    
    # Routing
    if page == "📊 Génération":
        generation_page()
        
    elif page == "📚 Historique":
        history_page()
        
    elif page == "⚙️ Configuration":
        config_page()

if __name__ == "__main__":
    main()