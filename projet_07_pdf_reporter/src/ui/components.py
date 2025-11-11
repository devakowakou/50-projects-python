"""
Composants UI réutilisables pour Streamlit
"""
from pathlib import Path
import streamlit as st
import pandas as pd
from typing import Dict, List, Optional
from src.utils.constants import STATUS

def display_kpi_card(label: str, value: str, delta: Optional[str] = None):
    """
    Affiche une carte KPI
    
    Args:
        label: Label du KPI
        value: Valeur principale
        delta: Variation (optionnel)
    """
    col1, col2 = st.columns([3, 1])
    with col1:
        st.metric(label=label, value=value, delta=delta)

def display_kpi_grid(kpis: Dict):
    """
    Affiche une grille de KPIs
    
    Args:
        kpis: Dictionnaire {label: value}
    """
    if not kpis:
        st.warning("Aucun KPI disponible")
        return
    
    # Créer 3 colonnes
    cols = st.columns(3)
    
    for idx, (key, value) in enumerate(kpis.items()):
        col_idx = idx % 3
        with cols[col_idx]:
            label = key.replace("_", " ").title()
            st.metric(label=label, value=value)

def file_uploader_section():
    """
    Section d'upload de fichier
    
    Returns:
        Fichier uploadé ou None
    """
    st.subheader("📁 Importer un fichier Excel")
    
    uploaded_file = st.file_uploader(
        "Choisir un fichier",
        type=["xlsx", "xls"],
        help="Formats supportés: .xlsx, .xls"
    )
    
    return uploaded_file

def template_selector(templates: Dict) -> str:
    """
    Sélecteur de template
    
    Args:
        templates: Dictionnaire des templates disponibles
    
    Returns:
        Nom du template sélectionné
    """
    st.subheader("📋 Choisir un template")
    
    template_options = {
        name: f"{name.title()} - {desc}"
        for name, desc in templates.items()
    }
    
    selected = st.selectbox(
        "Type de rapport",
        options=list(template_options.keys()),
        format_func=lambda x: template_options[x]
    )
    
    return selected

def data_preview(df: pd.DataFrame, max_rows: int = 5):
    """
    Affiche un aperçu des données
    
    Args:
        df: DataFrame à afficher
        max_rows: Nombre de lignes max
    """
    st.subheader("👀 Aperçu des données")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Lignes", len(df))
    with col2:
        st.metric("Colonnes", len(df.columns))
    with col3:
        missing = df.isnull().sum().sum()
        st.metric("Valeurs manquantes", missing)
    
    st.dataframe(df.head(max_rows), use_container_width=True)

def validation_report(is_valid: bool, errors: List[str], warnings: List[str]):
    """
    Affiche le rapport de validation
    
    Args:
        is_valid: Validation réussie
        errors: Liste d'erreurs
        warnings: Liste d'avertissements
    """
    st.subheader("✅ Validation des données")
    
    if is_valid:
        st.success(f"{STATUS['success']} Validation réussie!")
    else:
        st.error(f"{STATUS['error']} Validation échouée")
    
    if errors:
        with st.expander(f"❌ Erreurs ({len(errors)})"):
            for error in errors:
                st.error(error)
    
    if warnings:
        with st.expander(f"⚠️ Avertissements ({len(warnings)})"):
            for warning in warnings:
                st.warning(warning)

def progress_bar_section(message: str):
    """
    Affiche une barre de progression
    
    Args:
        message: Message à afficher
    
    Returns:
        Objet progress bar
    """
    st.info(f"{STATUS['loading']} {message}")
    return st.progress(0)

def success_download_button(file_path: str, button_label: str = "📥 Télécharger le PDF"):
    """
    Bouton de téléchargement du PDF
    
    Args:
        file_path: Chemin du fichier PDF
        button_label: Label du bouton
    """
    with open(file_path, "rb") as f:
        pdf_bytes = f.read()
    
    st.download_button(
        label=button_label,
        data=pdf_bytes,
        file_name=Path(file_path).name,
        mime="application/pdf"
    )

def sidebar_info():
    """Affiche les informations dans la sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Statistiques")
    st.sidebar.info(
        """
        **Templates disponibles:** 3  
        **Formats supportés:** Excel  
        **Export:** PDF
        """
    )