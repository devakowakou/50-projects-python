"""
Utilitaires pour le dashboard e-commerce
"""

import json
import pandas as pd
from typing import Dict, List, Tuple
import streamlit as st
from datetime import datetime, timedelta


class DataLoader:
    """Chargeur de données avec cache"""
    
    @staticmethod
    @st.cache_data
    def load_transactions(file_path: str = "data/transactions.json") -> pd.DataFrame:
        """Charge les transactions avec cache Streamlit"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            df['amount'] = pd.to_numeric(df['amount'])
            return df
        except FileNotFoundError:
            st.error(f"❌ Fichier {file_path} non trouvé. Générez d'abord les données.")
            return pd.DataFrame()
    
    @staticmethod
    @st.cache_data
    def load_sessions(file_path: str = "data/sessions.json") -> pd.DataFrame:
        """Charge les sessions avec cache Streamlit"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            st.error(f"❌ Fichier {file_path} non trouvé. Générez d'abord les données.")
            return pd.DataFrame()


class DateFilter:
    """Gestionnaire de filtres temporels"""
    
    @staticmethod
    def create_date_filter(df: pd.DataFrame) -> Tuple[datetime, datetime]:
        """Crée un filtre de dates dans la sidebar"""
        if df.empty:
            return datetime.now() - timedelta(days=30), datetime.now()
        
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        
        st.sidebar.subheader("📅 Filtres Temporels")
        
        date_range = st.sidebar.date_input(
            "Période d'analyse",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            return pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        else:
            return pd.to_datetime(min_date), pd.to_datetime(max_date)
    
    @staticmethod
    def filter_dataframe_by_date(df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Filtre un DataFrame par période"""
        if df.empty:
            return df
        return df[(df['date'] >= start_date) & (df['date'] <= end_date)]


class MetricFormatter:
    """Formateur de métriques pour l'affichage"""
    
    @staticmethod
    def format_currency(value: float) -> str:
        """Formate une valeur monétaire"""
        if value >= 1_000_000:
            return f"€{value/1_000_000:.1f}M"
        elif value >= 1_000:
            return f"€{value/1_000:.0f}K"
        else:
            return f"€{value:.0f}"
    
    @staticmethod
    def format_percentage(value: float) -> str:
        """Formate un pourcentage"""
        return f"{value:.1f}%"
    
    @staticmethod
    def format_number(value: int) -> str:
        """Formate un nombre avec séparateurs"""
        return f"{value:,}".replace(",", " ")
    
    @staticmethod
    def calculate_delta(current: float, previous: float) -> Tuple[float, str]:
        """Calcule la variation entre deux valeurs"""
        if previous == 0:
            return 0, "0%"
        
        delta = ((current - previous) / previous) * 100
        delta_str = f"{delta:+.1f}%"
        return delta, delta_str


class ExportUtils:
    """Utilitaires d'export de données"""
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filename: str) -> str:
        """Exporte un DataFrame en CSV"""
        csv = df.to_csv(index=False)
        return csv
    
    @staticmethod
    def create_pdf_report(kpis: Dict, revenue_by_source: pd.DataFrame, 
                         revenue_by_category: pd.DataFrame) -> bytes:
        """Crée un rapport PDF avec reportlab"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from io import BytesIO
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Titre
            title = Paragraph("RAPPORT E-COMMERCE KPIs", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Date
            date = Paragraph(f"Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal'])
            story.append(date)
            story.append(Spacer(1, 12))
            
            # Métriques principales
            metrics_title = Paragraph("MÉTRIQUES PRINCIPALES", styles['Heading2'])
            story.append(metrics_title)
            
            metrics = [
                f"• Chiffre d'Affaires Total: €{kpis['total_revenue']:,.0f}",
                f"• Panier Moyen: €{kpis['average_order_value']:.0f}",
                f"• Taux de Conversion: {kpis['conversion_rate']:.1f}%",
                f"• Nombre de Transactions: {kpis['total_transactions']:,}",
                f"• Nombre de Sessions: {kpis['total_sessions']:,}"
            ]
            
            for metric in metrics:
                story.append(Paragraph(metric, styles['Normal']))
            
            story.append(Spacer(1, 12))
            
            # Top sources
            sources_title = Paragraph("TOP 3 SOURCES DE TRAFIC", styles['Heading2'])
            story.append(sources_title)
            
            for i, (source, data) in enumerate(revenue_by_source.head(3).iterrows(), 1):
                source_text = f"{i}. {source}: €{data['total_revenue']:,.0f}"
                story.append(Paragraph(source_text, styles['Normal']))
            
            story.append(Spacer(1, 12))
            
            # Top catégories
            categories_title = Paragraph("TOP 3 CATÉGORIES", styles['Heading2'])
            story.append(categories_title)
            
            for i, (category, data) in enumerate(revenue_by_category.head(3).iterrows(), 1):
                category_text = f"{i}. {category}: €{data['total_revenue']:,.0f}"
                story.append(Paragraph(category_text, styles['Normal']))
            
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
            
        except ImportError:
            # Fallback vers texte si reportlab pas disponible
            report_text = f"""
RAPPORT E-COMMERCE KPIs
======================
Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M')}

MÉTRIQUES PRINCIPALES
--------------------
• Chiffre d'Affaires Total: €{kpis['total_revenue']:,.0f}
• Panier Moyen: €{kpis['average_order_value']:.0f}
• Taux de Conversion: {kpis['conversion_rate']:.1f}%
• Nombre de Transactions: {kpis['total_transactions']:,}
• Nombre de Sessions: {kpis['total_sessions']:,}

TOP 3 SOURCES DE TRAFIC
-----------------------
"""
            
            for i, (source, data) in enumerate(revenue_by_source.head(3).iterrows(), 1):
                report_text += f"{i}. {source}: €{data['total_revenue']:,.0f}\n"
            
            report_text += "\nTOP 3 CATÉGORIES\n----------------\n"
            for i, (category, data) in enumerate(revenue_by_category.head(3).iterrows(), 1):
                report_text += f"{i}. {category}: €{data['total_revenue']:,.0f}\n"
            
            return report_text.encode('utf-8')
    
    @staticmethod
    def create_summary_report(kpis: Dict, revenue_by_source: pd.DataFrame, 
                            revenue_by_category: pd.DataFrame) -> str:
        """Crée un rapport de synthèse"""
        report = f"""
# Rapport E-commerce KPIs
Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Métriques Principales
- Chiffre d'Affaires Total: €{kpis['total_revenue']:,.0f}
- Panier Moyen: €{kpis['average_order_value']:.0f}
- Taux de Conversion: {kpis['conversion_rate']:.1f}%
- Nombre de Transactions: {kpis['total_transactions']:,}
- Nombre de Sessions: {kpis['total_sessions']:,}

## Top 3 Sources de Trafic
"""
        for i, (source, data) in enumerate(revenue_by_source.head(3).iterrows(), 1):
            report += f"{i}. {source}: €{data['total_revenue']:,.0f}\n"
        
        report += "\n## Top 3 Catégories\n"
        for i, (category, data) in enumerate(revenue_by_category.head(3).iterrows(), 1):
            report += f"{i}. {category}: €{data['total_revenue']:,.0f}\n"
        
        return report