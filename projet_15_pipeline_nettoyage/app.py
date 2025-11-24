"""Interface Streamlit pour le pipeline de nettoyage de données."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import tempfile
import json
from io import StringIO

from src.pipeline import DataCleaningPipeline
from config import CLEANING_CONFIG

# Configuration de la page
st.set_page_config(
    page_title="Pipeline de Nettoyage de Données",
    page_icon="🧹",
    layout="wide"
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
.success-card {
    background-color: #d4edda;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #28a745;
}
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🧹 Pipeline de Nettoyage Automatique de Données")
    st.markdown("**Nettoyez et standardisez vos datasets automatiquement**")
    
    # Sidebar pour configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Stratégies de nettoyage
        st.subheader("Valeurs manquantes")
        missing_strategy = st.selectbox(
            "Stratégie",
            ["median", "mean", "mode", "drop", "ffill", "bfill"],
            help="Comment traiter les valeurs manquantes"
        )
        
        st.subheader("Outliers")
        outlier_method = st.selectbox(
            "Méthode de détection",
            ["iqr", "zscore", "percentile"],
            help="Méthode pour détecter les valeurs aberrantes"
        )
        
        if outlier_method == "iqr":
            iqr_threshold = st.slider("Seuil IQR", 1.0, 3.0, 1.5, 0.1)
        elif outlier_method == "zscore":
            zscore_threshold = st.slider("Seuil Z-Score", 2.0, 4.0, 3.0, 0.1)
        
        st.subheader("Autres options")
        remove_duplicates = st.checkbox("Supprimer les doublons", True)
        standardize_text = st.checkbox("Standardiser le texte", True)
    
    # Interface principale
    tab1, tab2, tab3 = st.tabs(["📁 Upload & Nettoyage", "📊 Analyse", "📋 Rapports"])
    
    with tab1:
        st.header("Upload de fichier")
        
        uploaded_file = st.file_uploader(
            "Choisissez un fichier",
            type=['csv', 'xlsx', 'xls', 'json'],
            help="Formats supportés : CSV, Excel, JSON"
        )
        
        if uploaded_file is not None:
            # Sauvegarde temporaire
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_path = tmp_file.name
            
            # Initialisation du pipeline
            pipeline = DataCleaningPipeline()
            
            # Configuration personnalisée
            custom_config = CLEANING_CONFIG.copy()
            custom_config['missing_values']['strategy'] = missing_strategy
            custom_config['outliers']['method'] = outlier_method
            
            if outlier_method == "iqr":
                custom_config['outliers']['threshold'] = iqr_threshold
            elif outlier_method == "zscore":
                custom_config['outliers']['zscore_threshold'] = zscore_threshold
            
            pipeline.set_config(custom_config)
            
            # Chargement et profilage initial
            try:
                df_original, load_metadata = pipeline.loader.load_file(temp_path)
                initial_profile = pipeline.profiler.profile_dataframe(df_original)
                
                # Affichage des données originales
                st.subheader("📊 Aperçu des données originales")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Lignes", f"{len(df_original):,}")
                with col2:
                    st.metric("Colonnes", len(df_original.columns))
                with col3:
                    st.metric("Valeurs manquantes", f"{df_original.isnull().sum().sum():,}")
                with col4:
                    st.metric("Doublons", f"{df_original.duplicated().sum():,}")
                
                # Échantillon des données
                st.dataframe(df_original.head(10), use_container_width=True)
                
                # Bouton de nettoyage
                if st.button("🧹 Lancer le nettoyage", type="primary"):
                    with st.spinner("Nettoyage en cours..."):
                        # Nettoyage
                        df_cleaned, cleaning_report = pipeline.cleaner.clean_dataframe(df_original)
                        final_profile = pipeline.profiler.profile_dataframe(df_cleaned)
                        
                        # Stockage dans session state
                        st.session_state.df_original = df_original
                        st.session_state.df_cleaned = df_cleaned
                        st.session_state.cleaning_report = cleaning_report
                        st.session_state.initial_profile = initial_profile
                        st.session_state.final_profile = final_profile
                        st.session_state.load_metadata = load_metadata
                    
                    st.success("✅ Nettoyage terminé !")
                    st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erreur lors du chargement : {e}")
    
    with tab2:
        if 'df_cleaned' in st.session_state:
            st.header("📊 Analyse Comparative")
            
            df_original = st.session_state.df_original
            df_cleaned = st.session_state.df_cleaned
            initial_profile = st.session_state.initial_profile
            final_profile = st.session_state.final_profile
            
            # Métriques de comparaison
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(
                    "Lignes",
                    f"{len(df_cleaned):,}",
                    delta=f"{len(df_cleaned) - len(df_original):,}"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(
                    "Valeurs manquantes",
                    f"{df_cleaned.isnull().sum().sum():,}",
                    delta=f"{df_cleaned.isnull().sum().sum() - df_original.isnull().sum().sum():,}"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(
                    "Doublons",
                    f"{df_cleaned.duplicated().sum():,}",
                    delta=f"{df_cleaned.duplicated().sum() - df_original.duplicated().sum():,}"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                quality_before = pipeline.profiler.get_quality_score(initial_profile)
                quality_after = pipeline.profiler.get_quality_score(final_profile)
                st.markdown('<div class="success-card">', unsafe_allow_html=True)
                st.metric(
                    "Score Qualité",
                    f"{quality_after:.1f}%",
                    delta=f"{quality_after - quality_before:+.1f}%"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Graphiques de comparaison
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Valeurs manquantes par colonne")
                
                missing_before = df_original.isnull().sum()
                missing_after = df_cleaned.isnull().sum()
                
                comparison_df = pd.DataFrame({
                    'Avant': missing_before,
                    'Après': missing_after
                }).reset_index()
                comparison_df.columns = ['Colonne', 'Avant', 'Après']
                comparison_df = comparison_df[comparison_df['Avant'] > 0]
                
                if not comparison_df.empty:
                    fig = px.bar(
                        comparison_df.melt(id_vars='Colonne', var_name='État', value_name='Valeurs manquantes'),
                        x='Colonne', y='Valeurs manquantes', color='État',
                        title="Comparaison des valeurs manquantes"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Aucune valeur manquante détectée")
            
            with col2:
                st.subheader("Distribution des types de données")
                
                types_before = df_original.dtypes.value_counts()
                types_after = df_cleaned.dtypes.value_counts()
                
                fig = go.Figure()
                fig.add_trace(go.Bar(name='Avant', x=types_before.index.astype(str), y=types_before.values))
                fig.add_trace(go.Bar(name='Après', x=types_after.index.astype(str), y=types_after.values))
                fig.update_layout(title="Types de données", barmode='group')
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Aperçu des données nettoyées
            st.subheader("📋 Données nettoyées")
            st.dataframe(df_cleaned.head(10), use_container_width=True)
            
        else:
            st.info("👆 Uploadez et nettoyez d'abord un fichier dans l'onglet précédent")
    
    with tab3:
        if 'cleaning_report' in st.session_state:
            st.header("📋 Rapport de Nettoyage")
            
            cleaning_report = st.session_state.cleaning_report
            
            # Résumé des opérations
            st.subheader("🔧 Opérations effectuées")
            for i, operation in enumerate(cleaning_report['operations'], 1):
                st.write(f"{i}. {operation}")
            
            # Téléchargements
            st.subheader("💾 Téléchargements")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # CSV nettoyé
                csv_data = st.session_state.df_cleaned.to_csv(index=False)
                st.download_button(
                    "📄 Télécharger CSV nettoyé",
                    csv_data,
                    file_name="donnees_nettoyees.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Rapport JSON
                report_data = {
                    'metadata': st.session_state.load_metadata,
                    'initial_profile': st.session_state.initial_profile,
                    'final_profile': st.session_state.final_profile,
                    'cleaning_report': cleaning_report
                }
                
                st.download_button(
                    "📊 Télécharger rapport JSON",
                    json.dumps(report_data, indent=2, default=str),
                    file_name="rapport_nettoyage.json",
                    mime="application/json"
                )
            
            with col3:
                # Échantillon
                sample_data = st.session_state.df_cleaned.sample(
                    n=min(100, len(st.session_state.df_cleaned))
                ).to_csv(index=False)
                
                st.download_button(
                    "🎯 Télécharger échantillon",
                    sample_data,
                    file_name="echantillon_100_lignes.csv",
                    mime="text/csv"
                )
            
        else:
            st.info("👆 Effectuez d'abord un nettoyage pour générer un rapport")

if __name__ == "__main__":
    main()