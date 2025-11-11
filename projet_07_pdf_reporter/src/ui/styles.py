"""
Styles CSS personnalisés pour Streamlit
"""

CUSTOM_CSS = """
<style>
    /* Style général */
    .main {
        padding-top: 2rem;
    }
    
    /* Cartes KPI */
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Boutons */
    .stButton>button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 600;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Dataframes */
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* Messages */
    .stAlert {
        border-radius: 0.5rem;
    }
</style>
"""

def inject_custom_css():
    """Injecte le CSS personnalisé"""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)