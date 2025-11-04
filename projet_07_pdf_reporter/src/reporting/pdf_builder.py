"""
Générateur de PDF avec ReportLab
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd

from config import PDF_CONFIG, OUTPUTS_DIR
from src.utils.logger import setup_logger
from src.reporting.formatters import format_currency, format_number, prepare_table_data

logger = setup_logger(__name__)

class PDFBuilder:
    """Classe pour construire des rapports PDF"""
    
    def __init__(self):
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
        kpis: Dict,
        charts: List[str],
        template_config: Dict,
        output_path: Optional[str] = None
    ) -> str:
        """
        Crée un rapport PDF complet
        
        Args:
            title: Titre du rapport
            data: DataFrame des données
            kpis: Dictionnaire des KPIs
            charts: Liste des chemins d'images
            template_config: Configuration du template
            output_path: Chemin de sortie (auto si None)
        
        Returns:
            Chemin du fichier PDF généré
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUTS_DIR / f"rapport_{timestamp}.pdf"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📄 Création du PDF: {output_path.name}")
        
        # Initialiser le document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        self.story = []
        
        # Construire le contenu
        self._add_header(title)
        self._add_metadata()
        
        # Traiter les sections du template
        for section in template_config.get("sections", []):
            section_type = section.get("type")
            
            if section_type == "header":
                self._add_section_header(section.get("content", ""))
            
            elif section_type == "kpi_grid":
                self._add_kpi_grid(kpis, section.get("kpis", []))
            
            elif section_type == "chart":
                if charts:
                    chart_path = charts.pop(0) if charts else None
                    if chart_path:
                        self._add_chart(chart_path, section.get("title", ""))
            
            elif section_type == "table":
                self._add_data_table(
                    data, 
                    section.get("title", "Données"),
                    max_rows=section.get("max_rows", 10)
                )
        
        # Footer
        self._add_footer(template_config.get("footer", ""))
        
        # Générer le PDF
        doc.build(self.story)
        
        logger.info(f"✅ PDF généré: {output_path}")
        return str(output_path)
    
    def _add_header(self, title: str):
        """Ajoute l'en-tête du rapport"""
        self.story.append(Paragraph(title, self.styles['CustomTitle']))
        self.story.append(Spacer(1, 0.5*cm))
    
    def _add_metadata(self):
        """Ajoute les métadonnées"""
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        meta = Paragraph(
            f"<i>Généré le {date_str}</i>",
            self.styles['Normal']
        )
        self.story.append(meta)
        self.story.append(Spacer(1, 1*cm))
    
    def _add_section_header(self, content: str):
        """Ajoute un titre de section"""
        self.story.append(Paragraph(content, self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.3*cm))
    
    def _add_kpi_grid(self, kpis: Dict, kpi_keys: List[str]):
        """Ajoute une grille de KPIs"""
        if not kpis:
            return
        
        # Filtrer les KPIs demandés
        selected_kpis = {k: v for k, v in kpis.items() if k in kpi_keys}
        
        if not selected_kpis:
            return
        
        # Créer la grille (3 colonnes)
        kpi_data = []
        row = []
        
        for key, value in selected_kpis.items():
            # Formater la valeur
            if isinstance(value, (int, float)):
                if "ca" in key.lower() or "credit" in key or "debit" in key:
                    formatted_value = format_currency(value)
                else:
                    formatted_value = format_number(value)
            else:
                formatted_value = str(value)
            
            # Formater le label
            label = key.replace("_", " ").title()
            
            cell_content = f"<b>{label}</b><br/><font size=14 color='#2ca02c'>{formatted_value}</font>"
            row.append(Paragraph(cell_content, self.styles['Normal']))
            
            if len(row) == 3:
                kpi_data.append(row)
                row = []
        
        # Ajouter la dernière ligne si incomplète
        if row:
            while len(row) < 3:
                row.append("")
            kpi_data.append(row)
        
        # Créer la table
        kpi_table = Table(kpi_data, colWidths=[6*cm, 6*cm, 6*cm])
        kpi_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.grey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        self.story.append(kpi_table)
        self.story.append(Spacer(1, 1*cm))
    
    def _add_chart(self, image_path: str, title: str):
        """Ajoute un graphique"""
        if not Path(image_path).exists():
            logger.warning(f"⚠️ Image introuvable: {image_path}")
            return
        
        if title:
            self.story.append(Paragraph(title, self.styles['CustomHeading']))
        
        img = Image(image_path, width=16*cm, height=10*cm)
        self.story.append(img)
        self.story.append(Spacer(1, 0.5*cm))
    
    def _add_data_table(self, data: pd.DataFrame, title: str, max_rows: int = 10):
        """Ajoute un tableau de données"""
        if data.empty:
            return
        
        self.story.append(Paragraph(title, self.styles['CustomHeading']))
        
        # Limiter les lignes
        df_subset = data.head(max_rows)
        
        # Préparer les données
        table_data = [list(df_subset.columns)]
        for _, row in df_subset.iterrows():
            table_data.append([str(x) for x in row.tolist()])
        
        # Calculer largeurs colonnes
        col_widths = [15*cm / len(df_subset.columns)] * len(df_subset.columns)
        
        # Créer la table
        data_table = Table(table_data, colWidths=col_widths)
        data_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003f5c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        
        self.story.append(data_table)
        self.story.append(Spacer(1, 0.5*cm))
    
    def _add_footer(self, footer_text: str):
        """Ajoute le pied de page"""
        if footer_text:
            self.story.append(Spacer(1, 1*cm))
            footer = Paragraph(
                f"<i>{footer_text}</i>",
                self.styles['Normal']
            )
            self.story.append(footer)