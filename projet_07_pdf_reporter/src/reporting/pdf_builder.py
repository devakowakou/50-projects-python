"""
Générateur de PDF avec ReportLab
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd

from config import PDF_CONFIG, OUTPUTS_DIR
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class PDFBuilder:
    """Classe pour construire des rapports PDF"""
    
    def __init__(self, output_dir: Path = None):
        """
        Initialise le générateur de PDF
        
        Args:
            output_dir: Dossier de sortie (défaut: OUTPUTS_DIR)
        """
        self.output_dir = Path(output_dir) if output_dir else Path(OUTPUTS_DIR)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.story = []
    
    def _setup_custom_styles(self):
        """Configure des styles personnalisés"""
        
        # Titre principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#003f5c'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Sous-titre
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#58508d'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # KPI
        self.styles.add(ParagraphStyle(
            name='KPI',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#2ca02c'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
    
    def create_report(
        self,
        title: str,
        data: pd.DataFrame,
        kpis: Dict[str, Any],
        charts: List[str],
        template_config: Dict[str, Any]
    ) -> str:
        """
        Crée un rapport PDF complet
        
        Args:
            title: Titre du rapport
            data: DataFrame des données
            kpis: Dictionnaire des KPIs
            charts: Liste des chemins vers les graphiques
            template_config: Configuration du template
            
        Returns:
            Chemin du fichier PDF généré
        """
        # Créer le document
        filename = f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output_path = self.output_dir / filename
        
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Construire le contenu
        story = []
        
        # Page de titre
        story.extend(self._create_title_page(title, template_config))
        story.append(PageBreak())
        
        # Sections du rapport
        sections = template_config.get('sections', ['synthese', 'donnees', 'analyse'])
        
        for section in sections:
            # Gérer sections sous forme de string ou de dict
            if isinstance(section, str):
                section_name = section
                section_dict = {"type": section, "title": section.title()}
            else:
                section_name = section.get("type", "unknown")
                section_dict = section
            
            if section_name == "synthese":
                story.extend(self._create_kpi_section(kpis, template_config))
            elif section_name == "donnees":
                story.extend(self._create_data_section(data))
            elif section_name == "graphiques" and charts:
                story.extend(self._create_charts_section(charts))
            elif section_name == "analyse":
                story.extend(self._create_analysis_section(data, kpis))
            
            story.append(Spacer(1, 0.5*cm))
        
        # Générer le PDF
        doc.build(story)
        
        return str(output_path)
    
    def _create_title_page(self, title: str, template_config: Dict) -> List:
        """Crée la page de titre"""
        elements = []
        
        # Titre principal
        elements.append(Spacer(1, 3*cm))
        elements.append(Paragraph(title, self.styles['CustomTitle']))
        elements.append(Spacer(1, 1*cm))
        
        # Sous-titre
        template_name = template_config.get('name', 'Rapport')
        elements.append(Paragraph(template_name, self.styles['Heading2']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Date
        date_str = datetime.now().strftime('%d/%m/%Y %H:%M')
        elements.append(Paragraph(f"Généré le {date_str}", self.styles['Normal']))
        
        return elements
    
    def _create_kpi_section(self, kpis: Dict, template_config: Dict) -> List:
        """Crée la section des KPIs"""
        elements = []
        
        elements.append(Paragraph("Indicateurs Clés", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.5*cm))
        
        if not kpis:
            elements.append(Paragraph("Aucun KPI disponible", self.styles['Normal']))
            return elements
        
        # Créer un tableau des KPIs
        data_table = [['Indicateur', 'Valeur']]
        
        for key, value in kpis.items():
            key_formatted = key.replace('_', ' ').title()
            data_table.append([key_formatted, str(value)])
        
        table = Table(data_table, colWidths=[8*cm, 6*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_data_section(self, data: pd.DataFrame) -> List:
        """Crée la section des données"""
        elements = []
        
        elements.append(Paragraph("Aperçu des Données", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Statistiques de base
        stats_text = f"""
        <b>Lignes:</b> {len(data)}<br/>
        <b>Colonnes:</b> {len(data.columns)}<br/>
        <b>Colonnes numériques:</b> {len(data.select_dtypes(include=['number']).columns)}
        """
        elements.append(Paragraph(stats_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Échantillon de données (5 premières lignes)
        sample_data = data.head(5)
        
        # Limiter le nombre de colonnes affichées
        max_cols = 5
        if len(sample_data.columns) > max_cols:
            sample_data = sample_data.iloc[:, :max_cols]
        
        # Créer le tableau
        table_data = [list(sample_data.columns)]
        for _, row in sample_data.iterrows():
            table_data.append([str(val)[:20] for val in row.values])
        
        col_width = 14 / len(table_data[0])
        table = Table(table_data, colWidths=[col_width*cm] * len(table_data[0]))
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_charts_section(self, charts: List[str]) -> List:
        """Crée la section des graphiques"""
        elements = []
        
        elements.append(Paragraph("Visualisations", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.5*cm))
        
        for chart_path in charts:
            if Path(chart_path).exists():
                try:
                    img = Image(chart_path, width=15*cm, height=9*cm)
                    elements.append(img)
                    elements.append(Spacer(1, 0.5*cm))
                except Exception as e:
                    elements.append(Paragraph(f"Erreur chargement graphique: {e}", self.styles['Normal']))
        
        return elements
    
    def _create_analysis_section(self, data: pd.DataFrame, kpis: Dict) -> List:
        """Crée la section d'analyse"""
        elements = []
        
        elements.append(Paragraph("Analyse", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.5*cm))
        
        # Analyse simple basée sur les KPIs
        analysis_text = f"""
        Le rapport contient {len(data)} enregistrements avec {len(data.columns)} colonnes.<br/>
        <br/>
        <b>Principales observations:</b><br/>
        - {len(kpis)} indicateurs clés ont été calculés<br/>
        - Les données couvrent {len(data.select_dtypes(include=['number']).columns)} colonnes numériques<br/>
        """
        
        elements.append(Paragraph(analysis_text, self.styles['Normal']))
        
        return elements