"""Application Streamlit principale pour l'analyse de sentiment."""

import streamlit as st
import pandas as pd
import sys
import os
from pathlib import Path

# Ajouter le chemin du projet
sys.path.append(str(Path(__file__).parent.parent))

from data.database import ReviewDatabase
from scrapers.amazon_scraper import AmazonScraper
from scrapers.trustpilot_scraper import TrustpilotScraper
from nlp.sentiment_analyzer import SentimentAnalyzer
from dashboard.components.charts import (
    create_sentiment_pie_chart, create_rating_histogram, 
    create_sentiment_by_rating, create_platform_comparison,
    create_confidence_scatter, create_wordcloud_image,
    create_metrics_cards, create_timeline_chart
)


# Configuration de la page
st.set_page_config(
    page_title="Sentiment Analysis Dashboard",
    page_icon="💭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .positive { border-left-color: #2E8B57 !important; }
    .negative { border-left-color: #DC143C !important; }
    .neutral { border-left-color: #FFD700 !important; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Charger les données depuis la base."""
    db = ReviewDatabase()
    reviews = db.get_recent_reviews_with_sentiment(limit=1000)
    sentiment_stats = db.get_sentiment_stats()
    return reviews, sentiment_stats


def main():
    """Application principale."""
    
    # Titre principal
    st.title("💭 Analyse de Sentiment - Reviews")
    st.markdown("Dashboard d'analyse des avis clients Amazon et Trustpilot")
    
    # Sidebar
    st.sidebar.title("🔧 Configuration")
    
    # Section de scraping
    st.sidebar.subheader("📥 Nouveau Scraping")
    
    platform = st.sidebar.selectbox("Plateforme", ["Amazon", "Trustpilot"])
    url_input = st.sidebar.text_input("URL du produit/entreprise")
    max_pages = st.sidebar.slider("Nombre de pages", 1, 5, 2)
    
    if st.sidebar.button("🚀 Lancer le Scraping"):
        if url_input:
            with st.spinner(f"Scraping {platform}..."):
                try:
                    if platform == "Amazon":
                        scraper = AmazonScraper()
                        reviews = scraper.scrape_product_reviews(url_input, max_pages)
                    else:
                        scraper = TrustpilotScraper()
                        reviews = scraper.scrape_company_reviews(url_input, max_pages)
                    
                    if reviews:
                        # Analyser les sentiments
                        analyzer = SentimentAnalyzer()
                        analyses = analyzer.analyze_reviews_batch(reviews)
                        
                        # Sauvegarder en base
                        from data.database import save_reviews_to_db
                        save_reviews_to_db(reviews, analyses)
                        
                        st.sidebar.success(f"✅ {len(reviews)} avis scrapés et analysés!")
                        st.experimental_rerun()
                    else:
                        st.sidebar.error("❌ Aucun avis trouvé")
                        
                except Exception as e:
                    st.sidebar.error(f"❌ Erreur: {str(e)}")
        else:
            st.sidebar.warning("⚠️ Veuillez entrer une URL")
    
    # Filtres
    st.sidebar.subheader("🔍 Filtres")
    platform_filter = st.sidebar.selectbox(
        "Filtrer par plateforme", 
        ["Toutes", "amazon", "trustpilot"]
    )
    
    # Charger les données
    reviews, sentiment_stats = load_data()
    
    if not reviews:
        st.warning("📭 Aucune donnée disponible. Commencez par scraper quelques avis!")
        st.info("💡 Utilisez la sidebar pour lancer un scraping.")
        return
    
    # Filtrer les données
    if platform_filter != "Toutes":
        reviews = [r for r in reviews if r.get("platform") == platform_filter]
        # Recalculer les stats pour le filtre
        db = ReviewDatabase()
        sentiment_stats = db.get_sentiment_stats(platform_filter)
    
    # Métriques principales
    st.subheader("📊 Métriques Principales")
    
    metrics = create_metrics_cards(sentiment_stats, len(reviews))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Avis", metrics["total_reviews"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card positive">', unsafe_allow_html=True)
        st.metric("Taux Positif", f"{metrics['positive_rate']:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card negative">', unsafe_allow_html=True)
        st.metric("Taux Négatif", f"{metrics['negative_rate']:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card neutral">', unsafe_allow_html=True)
        st.metric("Confiance Moy.", f"{metrics['avg_confidence']:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Graphiques principaux
    st.subheader("📈 Visualisations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique en camembert des sentiments
        fig_pie = create_sentiment_pie_chart(sentiment_stats)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Histogramme des notes
        fig_hist = create_rating_histogram(reviews)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Sentiment par note
        fig_rating = create_sentiment_by_rating(reviews)
        st.plotly_chart(fig_rating, use_container_width=True)
        
        # Comparaison plateformes
        fig_platform = create_platform_comparison(reviews)
        st.plotly_chart(fig_platform, use_container_width=True)
    
    # Graphiques avancés
    st.subheader("🔍 Analyses Avancées")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Confiance des prédictions
        fig_confidence = create_confidence_scatter(reviews)
        st.plotly_chart(fig_confidence, use_container_width=True)
    
    with col2:
        # Évolution temporelle
        fig_timeline = create_timeline_chart(reviews)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Nuage de mots
    st.subheader("☁️ Nuage de Mots")
    
    sentiment_filter = st.selectbox(
        "Sentiment pour le nuage de mots",
        ["Tous", "positive", "negative", "neutral"]
    )
    
    # Filtrer les textes selon le sentiment
    if sentiment_filter == "Tous":
        texts = [r.get("text", "") for r in reviews if r.get("text")]
    else:
        texts = [r.get("text", "") for r in reviews 
                if r.get("consensus_sentiment") == sentiment_filter and r.get("text")]
    
    if texts:
        wordcloud_img = create_wordcloud_image(texts)
        if wordcloud_img:
            st.markdown(f'<img src="{wordcloud_img}" style="width:100%">', 
                       unsafe_allow_html=True)
        else:
            st.info("Impossible de générer le nuage de mots")
    else:
        st.info("Aucun texte disponible pour ce filtre")
    
    # Tableau des avis récents
    st.subheader("📝 Avis Récents")
    
    if reviews:
        # Préparer les données pour le tableau
        df_display = pd.DataFrame([
            {
                "Plateforme": r.get("platform", "").title(),
                "Sentiment": r.get("consensus_sentiment", "N/A"),
                "Note": r.get("rating", "N/A"),
                "Confiance": f"{r.get('consensus_confidence', 0):.2f}",
                "Texte": r.get("text", "")[:100] + "..." if len(r.get("text", "")) > 100 else r.get("text", ""),
                "Auteur": r.get("author", "Anonyme"),
                "Date": r.get("created_at", "")[:10] if r.get("created_at") else ""
            }
            for r in reviews[:20]  # Limiter à 20 avis
        ])
        
        st.dataframe(df_display, use_container_width=True)
    
    # Export des données
    st.subheader("💾 Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Exporter CSV"):
            df_export = pd.DataFrame(reviews)
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="Télécharger CSV",
                data=csv,
                file_name="sentiment_analysis.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 Exporter Rapport"):
            # Créer un rapport simple
            report = f"""
# Rapport d'Analyse de Sentiment

## Résumé
- Total avis analysés: {len(reviews)}
- Taux positif: {metrics['positive_rate']:.1f}%
- Taux négatif: {metrics['negative_rate']:.1f}%
- Confiance moyenne: {metrics['avg_confidence']:.2f}

## Distribution des sentiments
"""
            for sentiment, stats in sentiment_stats.items():
                report += f"- {sentiment.title()}: {stats['count']} ({stats['percentage']:.1f}%)\n"
            
            st.download_button(
                label="Télécharger Rapport",
                data=report,
                file_name="rapport_sentiment.md",
                mime="text/markdown"
            )


if __name__ == "__main__":
    main()