"""Dashboard Streamlit pour visualiser les données collectées."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Ajouter le dossier parent au path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.api_clients.twitter_client import TwitterClient
from src.api_clients.reddit_client import RedditClient
from src.processing.clean_data import DataCleaner
from src.processing.sentiment_analysis import SentimentAnalyzer


st.set_page_config(
    page_title="API Data Extractor",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Extracteur de données depuis APIs publiques")
st.markdown("---")

# Sidebar pour la configuration
st.sidebar.header("⚙️ Configuration")

source = st.sidebar.selectbox(
    "Source de données",
    ["Twitter/X", "Reddit"]
)

if source == "Twitter/X":
    query = st.sidebar.text_input("Requête de recherche", "python programming")
    max_results = st.sidebar.slider("Nombre de tweets", 10, 100, 50)
    
    if st.sidebar.button("🔍 Collecter les données"):
        with st.spinner("Collecte en cours..."):
            try:
                client = TwitterClient()
                tweets = client.search_tweets(query, max_results)
                
                if tweets:
                    df = DataCleaner.clean_twitter_data(tweets)
                    df = SentimentAnalyzer.add_sentiment_to_df(df)
                    
                    st.session_state['df'] = df
                    st.session_state['source'] = 'twitter'
                    st.success(f"✅ {len(df)} tweets collectés !")
                else:
                    st.warning("Aucun tweet trouvé")
            except Exception as e:
                st.error(f"❌ Erreur: {e}")

else:  # Reddit
    subreddit = st.sidebar.text_input("Subreddit", "python")
    query_reddit = st.sidebar.text_input("Recherche (optionnel)", "")
    limit = st.sidebar.slider("Nombre de posts", 10, 100, 50)
    
    if st.sidebar.button("🔍 Collecter les données"):
        with st.spinner("Collecte en cours..."):
            try:
                client = RedditClient()
                posts = client.search_subreddit(
                    subreddit, 
                    query_reddit if query_reddit else None, 
                    limit
                )
                
                if posts:
                    df = DataCleaner.clean_reddit_data(posts)
                    df = SentimentAnalyzer.add_sentiment_to_df(df, 'title_clean')
                    
                    st.session_state['df'] = df
                    st.session_state['source'] = 'reddit'
                    st.success(f"✅ {len(df)} posts collectés !")
                else:
                    st.warning("Aucun post trouvé")
            except Exception as e:
                st.error(f"❌ Erreur: {e}")

# Affichage des résultats
if 'df' in st.session_state:
    df = st.session_state['df']
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Total de posts", len(df))
    
    with col2:
        avg_engagement = df['engagement'].mean()
        st.metric("💬 Engagement moyen", f"{avg_engagement:.1f}")
    
    with col3:
        positive_pct = (df['sentiment_category'] == 'positive').sum() / len(df) * 100
        st.metric("😊 Sentiment positif", f"{positive_pct:.1f}%")
    
    with col4:
        negative_pct = (df['sentiment_category'] == 'negative').sum() / len(df) * 100
        st.metric("😞 Sentiment négatif", f"{negative_pct:.1f}%")
    
    st.markdown("---")
    
    # Visualisations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribution du sentiment")
        sentiment_counts = df['sentiment_category'].value_counts()
        fig = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            color=sentiment_counts.index,
            color_discrete_map={
                'positive': '#28a745',
                'neutral': '#ffc107',
                'negative': '#dc3545'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Top 10 auteurs")
        if st.session_state['source'] == 'twitter':
            top_authors = df['author_username'].value_counts().head(10)
        else:
            top_authors = df['author'].value_counts().head(10)
        
        fig = px.bar(
            x=top_authors.values,
            y=top_authors.index,
            orientation='h',
            labels={'x': 'Nombre de posts', 'y': 'Auteur'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Timeline
    st.subheader("📅 Timeline des publications")
    date_col = 'created_at' if st.session_state['source'] == 'twitter' else 'created_utc'
    if date_col in df.columns:
        df_timeline = df.set_index(date_col).resample('H').size().reset_index(name='count')
        fig = px.line(df_timeline, x=date_col, y='count', title="Publications par heure")
        st.plotly_chart(fig, use_container_width=True)
    
    # Tableau de données
    st.subheader("📋 Données brutes")
    st.dataframe(df.head(50), use_container_width=True)
    
    # Export
    st.download_button(
        label="💾 Télécharger en CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name=f"{st.session_state['source']}_data.csv",
        mime="text/csv"
    )

else:
    st.info("👈 Configurez les paramètres dans la barre latérale et cliquez sur 'Collecter les données'")
