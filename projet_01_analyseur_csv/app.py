"""
Application Streamlit - Analyseur CSV Professionnel
Point d'entrée principal de l'application
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

# Ajouter le dossier src au path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.statistical_analyzer import StatisticalAnalyzer
from src.correlation_analyzer import CorrelationAnalyzer
from src.anomaly_detector import AnomalyDetector
from src.visualizer import Visualizer
from src.report_generator import ReportGenerator
from src.modern_report_generator import ModernReportGenerator

import config

# Configuration de la page
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.APP_LAYOUT,
    initial_sidebar_state="expanded"
)

# CSS personnalisé
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialiser les états de session
if 'df' not in st.session_state:
    st.session_state.df = None
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None
if 'file_info' not in st.session_state:
    st.session_state.file_info = {}

# ============= HEADER =============
st.title(f"{config.APP_ICON} Analyseur CSV Professionnel")
st.markdown("### Statistiques descriptives, corrélations et détection d'anomalies")
st.markdown("---")

# ============= SIDEBAR =============
with st.sidebar:
    st.header(" Configuration")
    
    # Section Upload
    st.subheader(" Charger les données")
    
    upload_option = st.radio(
        "Source des données",
        ["Upload fichier", "Fichier exemple"]
    )
    
    loader = DataLoader()
    
    if upload_option == "Upload fichier":
        uploaded_file = st.file_uploader(
            "Choisir un fichier",
            type=config.SUPPORTED_FORMATS,
            help=f"Formats supportés: {', '.join(config.SUPPORTED_FORMATS)}"
        )
        
        if uploaded_file:
            with st.spinner("Chargement du fichier..."):
                success, message = loader.load_from_upload(uploaded_file)
                
                if success:
                    st.success(message)
                    st.session_state.df = loader.get_data()
                    st.session_state.file_info = loader.get_file_info()
                else:
                    st.error(message)
    
    else:  # Fichier exemple
        if st.button("📂 Charger fichier exemple"):
            example_path = "data/exemple_ventes.csv"
            success, message = loader.load_from_path(example_path)
            
            if success:
                st.success(message)
                st.session_state.df = loader.get_data()
                st.session_state.file_info = loader.get_file_info()
            else:
                st.error(message)
    
    # Informations du fichier
    if st.session_state.df is not None:
        st.markdown("---")
        st.subheader(" Informations")
        info = st.session_state.file_info
        st.metric("Lignes", info.get('lignes', 0))
        st.metric("Colonnes", info.get('colonnes', 0))
        if 'taille' in info:
            st.metric("Taille", info['taille'])

# ============= MAIN CONTENT =============
if st.session_state.df is None:
    # Page d'accueil
    st.info("👈 Veuillez charger un fichier CSV pour commencer l'analyse")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ###  Statistiques
        - Moyenne, médiane, écart-type
        - Distribution et normalité
        - Quartiles et percentiles
        """)
    
    with col2:
        st.markdown("""
        ###  Corrélations
        - Matrice de corrélation
        - Tests de significativité
        - Visualisations interactives
        """)
    
    with col3:
        st.markdown("""
        ###  Anomalies
        - Détection d'outliers (IQR, Z-Score)
        - Analyse multivariée
        - Recommandations
        """)

else:
    df = st.session_state.df
    
    # Onglets principaux
    tabs = st.tabs([
        " Aperçu",
        " Nettoyage",
        " Statistiques",
        " Corrélations",
        " Anomalies",
        " Visualisations",
        " Rapports"
    ])
    
    # ============= ONGLET 1: APERÇU =============
    with tabs[0]:
        st.header(" Aperçu des Données")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(" Lignes", len(df))
        with col2:
            st.metric(" Colonnes", len(df.columns))
        with col3:
            missing_pct = (df.isnull().sum().sum() / df.size * 100)
            st.metric(" Valeurs Manquantes", f"{missing_pct:.1f}%")
        with col4:
            st.metric(" Duplicatas", df.duplicated().sum())
        
        st.markdown("---")
        
        # Aperçu des données
        st.subheader(" Aperçu des données")
        n_rows = st.slider("Nombre de lignes à afficher", 5, 100, 10)
        st.dataframe(df.head(n_rows), use_container_width=True)
        
        # Types de colonnes
        st.subheader(" Types de colonnes")
        
        # Calculer les types directement depuis df
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Colonnes Numériques:**")
            st.write(numeric_cols if numeric_cols else "Aucune")
        with col2:
            st.write("**Colonnes Catégoriques:**")
            st.write(categorical_cols if categorical_cols else "Aucune")
    
    # ============= ONGLET 2: NETTOYAGE =============
    with tabs[1]:
        st.header(" Nettoyage des Données")
        
        cleaner = DataCleaner(df)
        
        # Résumé des valeurs manquantes
        st.subheader(" Valeurs Manquantes")
        missing_summary = cleaner.get_missing_values_summary()
        
        if len(missing_summary) > 0:
            st.dataframe(missing_summary, use_container_width=True)
            
            # Options de traitement
            st.markdown("---")
            st.subheader("🔧 Traiter les valeurs manquantes")
            
            strategy = st.selectbox(
                "Stratégie",
                list(config.MISSING_VALUE_STRATEGIES.keys())
            )
            
            if st.button("Appliquer le nettoyage"):
                strategy_value = config.MISSING_VALUE_STRATEGIES[strategy]
                cleaner.handle_missing_values(strategy=strategy_value)
                st.session_state.df_cleaned = cleaner.get_cleaned_data()
                st.success(" Nettoyage appliqué !")
                st.rerun()
        else:
            st.success(" Aucune valeur manquante !")
        
        # Rapport de qualité
        st.markdown("---")
        st.subheader(" Rapport de Qualité")
        quality_report = cleaner.get_data_quality_report()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Complétude", f"{quality_report['pourcentage_completude']:.1f}%")
        with col2:
            st.metric("Duplicatas", quality_report['duplicatas'])
        with col3:
            st.metric("Mémoire", quality_report['memoire_utilise'])
    
    # ============= ONGLET 3: STATISTIQUES =============
    with tabs[2]:
        st.header(" Analyse Statistique")
        
        analyzer = StatisticalAnalyzer(df)
        
        # Résumé complet
        summary = analyzer.get_complete_summary()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Colonnes Numériques", summary['dimensions']['colonnes_numeriques'])
        with col2:
            st.metric("Colonnes Catégoriques", summary['dimensions']['colonnes_categoriques'])
        with col3:
            st.metric("Complétude", f"{summary['qualite_donnees']['pourcentage_completude']:.1f}%")
        with col4:
            st.metric("Mémoire", summary['memoire'])
        
        st.markdown("---")
        
        # Statistiques descriptives
        st.subheader(" Statistiques Descriptives")
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) > 0:
            selected_col = st.selectbox("Sélectionner une colonne", numeric_cols)
            
            # Statistiques de base
            stats_df = analyzer.get_basic_statistics(selected_col)
            st.dataframe(stats_df, use_container_width=True)
            
            # Statistiques avancées
            with st.expander(" Statistiques Avancées"):
                advanced_stats = analyzer.get_advanced_statistics(selected_col)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Skewness", f"{advanced_stats['skewness']:.4f}")
                    st.metric("Kurtosis", f"{advanced_stats['kurtosis']:.4f}")
                with col2:
                    if advanced_stats['mode'] is not None:
                        st.metric("Mode", f"{advanced_stats['mode']:.2f}")
                    if advanced_stats['coef_variation'] is not None:
                        st.metric("CV (%)", f"{advanced_stats['coef_variation']:.2f}")
        else:
            st.warning(" Aucune colonne numérique à analyser")
    
    # ============= ONGLET 4: CORRÉLATIONS =============
    with tabs[3]:
        st.header(" Analyse de Corrélation")
        
        corr_analyzer = CorrelationAnalyzer(df)
        
        # Méthode de corrélation
        method = st.selectbox(
            "Méthode de corrélation",
            config.CORRELATION_METHODS
        )
        
        # Matrice de corrélation
        corr_matrix = corr_analyzer.get_correlation_matrix(method=method)
        
        if not corr_matrix.empty:
            # Résumé
            summary = corr_analyzer.get_correlation_summary(method=method)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Variables", summary['nombre_variables'])
            with col2:
                st.metric("Corrélation Moyenne", f"{summary['correlation_moyenne']:.3f}")
            with col3:
                st.metric("Fortes Corrélations", summary['paires_fortement_correlees'])
            
            st.markdown("---")
            
            # Heatmap
            st.subheader(" Matrice de Corrélation")
            visualizer = Visualizer(df)
            fig = visualizer.create_correlation_heatmap(corr_matrix, method)
            st.plotly_chart(fig, use_container_width=True)
            
            # Paires corrélées
            st.markdown("---")
            st.subheader(" Paires Fortement Corrélées")
            threshold = st.slider("Seuil de corrélation", 0.0, 1.0, 0.7, 0.05)
            pairs = corr_analyzer.get_correlation_pairs(threshold=threshold, method=method)
            
            if pairs:
                pairs_df = pd.DataFrame(pairs)
                st.dataframe(pairs_df, use_container_width=True)
            else:
                st.info("Aucune paire avec corrélation supérieure au seuil")
        else:
            st.warning(" Pas assez de colonnes numériques pour calculer les corrélations")
    
    # ============= ONGLET 5: ANOMALIES =============
    with tabs[4]:
        st.header(" Détection d'Anomalies")
        
        detector = AnomalyDetector(df)
        
        # Méthode de détection
        col1, col2 = st.columns(2)
        with col1:
            method = st.selectbox("Méthode", ["IQR", "Z-Score"])
        with col2:
            if method == "IQR":
                threshold = st.slider("Multiplicateur IQR", 1.0, 3.0, 1.5, 0.5)
            else:
                threshold = st.slider("Seuil Z-Score", 2.0, 4.0, 3.0, 0.5)
        
        if st.button(" Détecter les anomalies"):
            with st.spinner("Détection en cours..."):
                outliers_summary = detector.detect_outliers_all_columns(
                    method=method,
                    threshold=threshold
                )
                
                st.subheader(" Résumé des Anomalies")
                st.dataframe(outliers_summary, use_container_width=True)
                
                # Sélection pour visualisation
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                selected_col = st.selectbox("Colonne à visualiser", numeric_cols)
                
                # Box plot
                visualizer = Visualizer(df)
                fig = visualizer.create_boxplot([selected_col])
                st.plotly_chart(fig, use_container_width=True)
                
                # Suggestions
                st.markdown("---")
                st.subheader(" Suggestions de Traitement")
                suggestions = detector.suggest_treatment(selected_col)
                st.write(f"**Recommandation:** {suggestions['recommandation']}")
                st.write("**Autres options:**")
                for suggestion in suggestions['suggestions']:
                    st.write(f"- {suggestion}")
    
    # ============= ONGLET 6: VISUALISATIONS =============
    with tabs[5]:
        st.header(" Visualisations Interactives")
        
        visualizer = Visualizer(df, theme=config.PLOTLY_THEME)
        
        viz_type = st.selectbox(
            "Type de visualisation",
            [
                "Histogramme",
                "Box Plot",
                "Scatter Plot",
                "Bar Chart",
                "Pie Chart",
                "Violin Plot",
                "Valeurs Manquantes"
            ]
        )
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if viz_type == "Histogramme" and numeric_cols:
            col = st.selectbox("Colonne", numeric_cols)
            nbins = st.slider("Nombre de bins", 10, 100, 30)
            fig = visualizer.create_histogram(col, nbins=nbins)
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Box Plot" and numeric_cols:
            cols = st.multiselect("Colonnes", numeric_cols, default=numeric_cols[:3])
            if cols:
                fig = visualizer.create_boxplot(cols)
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Scatter Plot" and len(numeric_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("Axe X", numeric_cols)
            with col2:
                y_col = st.selectbox("Axe Y", [c for c in numeric_cols if c != x_col])
            
            color_col = st.selectbox("Couleur (optionnel)", [None] + categorical_cols)
            fig = visualizer.create_scatter_plot(x_col, y_col, color_col=color_col)
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Bar Chart" and categorical_cols:
            col = st.selectbox("Colonne", categorical_cols)
            top_n = st.slider("Top N", 5, 20, 10)
            fig = visualizer.create_bar_chart(col, top_n=top_n)
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Pie Chart" and categorical_cols:
            col = st.selectbox("Colonne", categorical_cols)
            top_n = st.slider("Top N", 5, 15, 10)
            fig = visualizer.create_pie_chart(col, top_n=top_n)
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Violin Plot" and numeric_cols:
            col = st.selectbox("Colonne numérique", numeric_cols)
            by_col = st.selectbox("Grouper par (optionnel)", [None] + categorical_cols)
            fig = visualizer.create_violin_plot(col, by=by_col)
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Valeurs Manquantes":
            fig = visualizer.create_missing_values_chart()
            st.plotly_chart(fig, use_container_width=True)
    
    # ============= ONGLET 7: RAPPORTS =============
    with tabs[6]:
        st.header(" Génération de Rapports Professionnels")
        
        # Configuration du rapport
        with st.expander(" Configuration du Rapport", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                company_name = st.text_input("Nom de l'entreprise/projet", "Analyse de Données")
            with col2:
                include_charts = st.checkbox("Inclure les graphiques", value=True)
        
        st.markdown("---")
        
        # Générateurs de rapports
        report_gen = ReportGenerator(df)
        modern_gen = ModernReportGenerator(df)
        
        # Section 1: Exports de données
        st.subheader("� Export des Données")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("� CSV", use_container_width=True):
                with st.spinner("Génération du fichier CSV..."):
                    filepath = report_gen.export_to_csv()
                    st.success(f" Fichier créé")
                    with open(filepath, 'rb') as f:
                        st.download_button(
                            " Télécharger CSV",
                            f,
                            file_name=f"donnees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime='text/csv',
                            use_container_width=True
                        )
        
        with col2:
            if st.button(" JSON", use_container_width=True):
                with st.spinner("Génération du fichier JSON..."):
                    analyzer = StatisticalAnalyzer(df)
                    summary = analyzer.get_complete_summary()
                    filepath = report_gen.export_statistics_to_json(summary)
                    st.success(f" Fichier créé")
                    with open(filepath, 'rb') as f:
                        st.download_button(
                            " Télécharger JSON",
                            f,
                            file_name=f"statistiques_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime='application/json',
                            use_container_width=True
                        )
        
        with col3:
            if st.button(" Excel", use_container_width=True):
                with st.spinner("Génération du fichier Excel..."):
                    analyzer = StatisticalAnalyzer(df)
                    stats_df = {
                        'Statistiques': analyzer.get_basic_statistics(),
                        'Résumé': pd.DataFrame([analyzer.get_complete_summary()['dimensions']])
                    }
                    filepath = report_gen.create_excel_report(stats_df)
                    st.success(f" Fichier créé")
                    with open(filepath, 'rb') as f:
                        st.download_button(
                            " Télécharger Excel",
                            f,
                            file_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                            use_container_width=True
                        )
        
        st.markdown("---")
        
        # Section 2: Rapports professionnels
        st.subheader(" Rapports Professionnels")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(" PDF", use_container_width=True, type="primary"):
                with st.spinner("Génération du rapport PDF professionnel..."):
                    try:
                        filepath = modern_gen.generate_pdf_report(
                            company_name=company_name,
                            include_charts=include_charts
                        )
                        st.success(f" Rapport PDF créé !")
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                " Télécharger PDF",
                                f,
                                file_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime='application/pdf',
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f" Erreur: {str(e)}")
                        st.info(" Installez les dépendances: pip install reportlab")
        
        with col2:
            if st.button(" DOCX (Word)", use_container_width=True, type="primary"):
                with st.spinner("Génération du rapport Word..."):
                    try:
                        filepath = modern_gen.generate_docx_report(company_name=company_name)
                        st.success(f" Rapport DOCX créé !")
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                " Télécharger DOCX",
                                f,
                                file_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                                mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f" Erreur: {str(e)}")
                        st.info(" Installez les dépendances: pip install python-docx")
        
        with col3:
            if st.button(" HTML", use_container_width=True, type="primary"):
                with st.spinner("Génération du rapport HTML interactif..."):
                    try:
                        filepath = modern_gen.generate_html_report(
                            include_interactive_charts=include_charts
                        )
                        st.success(f" Rapport HTML créé !")
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                " Télécharger HTML",
                                f,
                                file_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                                mime='text/html',
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f" Erreur: {str(e)}")
        
        st.markdown("---")
        
        # Section 3: Aperçu du rapport
        st.subheader(" Aperçu du Rapport")
        
        tab1, tab2 = st.tabs([" Markdown", " Recommandations"])
        
        with tab1:
            analyzer = StatisticalAnalyzer(df)
            summary = analyzer.get_complete_summary()
            report_preview = report_gen.generate_markdown_report(summary)
            st.markdown(report_preview)
        
        with tab2:
            recommendations = modern_gen._generate_recommendations()
            for i, rec in enumerate(recommendations, 1):
                if "" in rec:
                    st.success(f"{i}. {rec}")
                elif "" in rec:
                    st.warning(f"{i}. {rec}")
                else:
                    st.info(f"{i}. {rec}")

# ============= FOOTER =============
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    " Analyseur CSV Professionnel | Projet 1/50 | Fait avec ❤️ et Streamlit"
    "</div>",
    unsafe_allow_html=True
)
