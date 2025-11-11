"""
Pages de l'application Streamlit - VERSION FLEXIBLE
"""
import streamlit as st
import pandas as pd
import tempfile
import os

from src.ingestion.excel_reader import ExcelReader
from src.ingestion.validator import DataValidator
from src.transformation.transformer import Transformer
from src.transformation.kpi_calculator import KPICalculator
from src.visualization.chart_generator import ChartGenerator
from src.reporting.pdf_builder import PDFBuilder
from src.reporting.template_engine import TemplateEngine
from src.ui.components import (
    file_uploader_section, data_preview,
    validation_report, display_kpi_grid, progress_bar_section,
    success_download_button
)

from config import OUTPUTS_DIR

def generation_page():
    """Page principale de génération de rapports - VERSION FLEXIBLE"""
    
    st.header("📊 Nouvelle génération de rapport")
    st.markdown("---")
    
    # Upload du fichier D'ABORD
    uploaded_file = file_uploader_section()
    
    if uploaded_file is not None:
        
        # Validation du fichier
        if not uploaded_file.name.endswith(('.xlsx', '.xls')):
            st.error("❌ Format invalide. Seuls les fichiers Excel sont acceptés.")
            return
        
        # Sauvegarder temporairement
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                tmp.write(uploaded_file.getbuffer())
                tmp_path = tmp.name
        
            # Lecture du fichier
            reader = ExcelReader()
            df = reader.read_excel(tmp_path)
            
            st.success(f"✅ Fichier chargé: {uploaded_file.name}")
            
            # Aperçu des données
            data_preview(df)
            
            st.markdown("---")
            
            # DÉTECTION AUTOMATIQUE du type de données
            validator = DataValidator(template_type="auto")
            detected_type = validator.detect_data_type(df)
            
            st.info(f"🔍 Type de données détecté: **{detected_type.title()}**")
            
            # Template engine
            template_engine = TemplateEngine()
            available_templates = template_engine.get_available_templates()
            
            # Sélection du template (avec suggestion automatique)
            col1, col2 = st.columns([2, 1])
            with col1:
                selected_template = st.selectbox(
                    "📋 Type de rapport à générer",
                    options=list(available_templates.keys()),
                    index=list(available_templates.keys()).index(detected_type) if detected_type in available_templates else 0
                )
            
            with col2:
                auto_detect = st.checkbox("Détection auto", value=True)
            
            if auto_detect:
                selected_template = detected_type if detected_type in available_templates else "commercial"
            
            st.markdown("---")
            
            # Validation FLEXIBLE
            is_valid, errors, warnings = validator.validate(df)
            
            validation_report(is_valid, errors, warnings)
            
            st.markdown("---")
            
            # Options de transformation
            with st.expander("⚙️ Options de transformation"):
                col1, col2 = st.columns(2)
                
                with col1:
                    normalize = st.checkbox("Normaliser les données", value=True)
                    convert_dates = st.checkbox("Convertir les dates", value=True)
                
                with col2:
                    missing_strategy = st.selectbox(
                        "Gestion valeurs manquantes",
                        ["drop", "fill", "forward", "backward"]
                    )
            
            # Bouton de génération
            if st.button("🚀 Générer le rapport PDF", type="primary", use_container_width=True):
                
                if not is_valid:
                    st.error("❌ Données invalides, génération impossible")
                else:
                    generate_report(
                        df, 
                        selected_template, 
                        uploaded_file.name,
                        normalize,
                        convert_dates,
                        missing_strategy
                    )
        
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
            import traceback
            with st.expander("Détails de l'erreur"):
                st.code(traceback.format_exc())
        
        finally:
            # Nettoyage du fichier temporaire
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
    else:
        st.info("👆 Commencez par uploader un fichier Excel")

def generate_report(
    df: pd.DataFrame, 
    template_type: str, 
    filename: str,
    normalize: bool,
    convert_dates: bool,
    missing_strategy: str
):
    """
    Génère le rapport PDF
    
    Args:
        df: DataFrame
        template_type: Type de template
        filename: Nom du fichier original
        normalize: Normaliser les données
        convert_dates: Convertir les dates
        missing_strategy: Stratégie valeurs manquantes
    """
    progress = progress_bar_section("Génération en cours...")
    chart_paths = []
    chart_gen = None
    charts = []
    
    try:
        # Transformation
        progress.progress(20)
        transformer = Transformer()
        
        if normalize:
            df = transformer.normalize(df)
        
        if convert_dates:
            df = transformer.convert_dates(df)
        
        df = transformer.handle_missing_values(df, strategy=missing_strategy)
        
        # Calcul KPIs
        progress.progress(40)
        kpi_calc = KPICalculator(template_type=template_type)
        kpis = kpi_calc.calculate(df)
        formatted_kpis = kpi_calc.format_kpis_for_display()
        
        st.subheader("📈 KPIs calculés")
        display_kpi_grid(formatted_kpis)
        
        # Génération graphiques
        progress.progress(60)
        chart_gen = ChartGenerator(template_type=template_type)
        
        # Détecter colonnes pour graphiques
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        if date_cols and numeric_cols:
            chart_path = chart_gen.plot_timeseries(
                df, 
                date_cols[0], 
                numeric_cols[0],
                title=f"Évolution de {numeric_cols[0]}"
            )
            chart_paths.append(chart_path)
            charts.append(chart_path)
            st.image(chart_path, caption="Graphique généré")
        
        # Charger template
        progress.progress(80)
        template_engine = TemplateEngine()
        
        try:
            template_config = template_engine.load_template(template_type)
            st.info(f"📋 Template chargé: {template_config.get('name', template_type)}")
        except Exception as e:
            st.warning(f"⚠️ Erreur chargement template: {str(e)}")
            st.info("📋 Utilisation de la configuration par défaut")
            template_config = {
                "name": f"Rapport {template_type.title()}",
                "description": "Rapport généré avec configuration par défaut",
                "sections": ["synthese", "donnees", "analyse"]
            }
        
        # Génération PDF
        pdf_builder = PDFBuilder()
        output_path = pdf_builder.create_report(
            title=f"Rapport {template_type.title()} - {filename}",
            data=df,
            kpis=kpis,
            charts=charts,
            template_config=template_config
        )
        
        progress.progress(100)
        
        st.success("✅ Rapport généré avec succès!")
        
        # Bouton de téléchargement
        success_download_button(output_path)
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la génération: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
    
    finally:
        # Cleanup garanti
        try:
            if chart_gen:
                chart_gen.cleanup()
            # Supprimer les fichiers de graphiques temporaires
            for chart_path in chart_paths:
                if os.path.exists(chart_path):
                    os.unlink(chart_path)
        except Exception:
            pass

def history_page():
    """Page d'historique des rapports"""
    
    st.header("📚 Historique des rapports")
    st.markdown("---")
    
    # Lister les PDFs générés
    pdf_files = list(OUTPUTS_DIR.glob("*.pdf"))
    
    if not pdf_files:
        st.info("Aucun rapport généré pour le moment")
        return
    
    st.write(f"**{len(pdf_files)} rapport(s) généré(s)**")
    
    # Afficher la liste
    for pdf_file in sorted(pdf_files, reverse=True):
        with st.expander(f"📄 {pdf_file.name}"):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**Taille:** {pdf_file.stat().st_size / 1024:.2f} Ko")
            
            with col2:
                from datetime import datetime
                modified = datetime.fromtimestamp(pdf_file.stat().st_mtime)
                st.write(f"**Créé:** {modified.strftime('%d/%m/%Y %H:%M')}")
            
            with col3:
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        "📥 Télécharger",
                        data=f.read(),
                        file_name=pdf_file.name,
                        mime="application/pdf",
                        key=f"download_{pdf_file.name}"
                    )

def config_page():
    """Page de configuration"""
    
    st.header("⚙️ Configuration")
    st.markdown("---")
    
    st.subheader("📋 Templates disponibles")
    
    template_engine = TemplateEngine()
    templates = template_engine.get_available_templates()
    
    for name, description in templates.items():
        with st.expander(f"**{name.title()}**"):
            st.write(description)
            
            # Charger la config
            try:
                config = template_engine.load_template(name)
                st.json(config)
            except Exception as e:
                st.error(f"Erreur chargement: {e}")
    
    st.markdown("---")
    
    st.subheader("📊 Statistiques globales")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pdf_count = len(list(OUTPUTS_DIR.glob("*.pdf")))
        st.metric("Rapports générés", pdf_count)
    
    with col2:
        st.metric("Templates disponibles", len(templates))
    
    with col3:
        total_size = sum(f.stat().st_size for f in OUTPUTS_DIR.glob("*.pdf"))
        st.metric("Espace utilisé", f"{total_size / (1024*1024):.2f} Mo")