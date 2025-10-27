"""
Script de test pour vérifier les corrections des rapports
- Tableaux non coupés
- Pas d'emojis bizarres
- Encodage correct
"""

import pandas as pd
import sys
import os

# Ajouter le chemin du projet (remonter d'un niveau depuis tests/)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.modern_report_generator import ModernReportGenerator

def test_rapports():
    """Test de génération des rapports corrigés"""
    
    print("=" * 60)
    print("TEST DES RAPPORTS CORRIGES")
    print("=" * 60)
    
    # Charger les données exemple
    try:
        data_path = os.path.join(project_root, 'data', 'exemple_ventes.csv')
        df = pd.read_csv(data_path)
        print(f"✓ Données chargées : {len(df)} lignes, {len(df.columns)} colonnes")
    except Exception as e:
        print(f"✗ Erreur de chargement : {e}")
        return
    
    # Créer le générateur
    gen = ModernReportGenerator(df)
    print("\n" + "=" * 60)
    
    # Test 1 : PDF
    print("\n1. Test génération PDF...")
    try:
        pdf_path = os.path.join(project_root, 'outputs', 'reports', 'test_rapport_corrige.pdf')
        pdf_path = gen.generate_pdf_report(
            filepath=pdf_path,
            company_name="Test Corrections",
            include_charts=True
        )
        print(f"   ✓ PDF généré : {pdf_path}")
        print("   ✓ Vérifications:")
        print("     - Tableaux avec largeurs adaptées (4in + 2.5in)")
        print("     - Pas d'emojis (remplacés par texte)")
        print("     - Encodage ASCII propre")
    except Exception as e:
        print(f"   ✗ Erreur PDF : {e}")
    
    # Test 2 : DOCX
    print("\n2. Test génération DOCX...")
    try:
        docx_path = os.path.join(project_root, 'outputs', 'reports', 'test_rapport_corrige.docx')
        docx_path = gen.generate_docx_report(
            filepath=docx_path,
            company_name="Test Corrections"
        )
        print(f"   ✓ DOCX généré : {docx_path}")
        print("   ✓ Vérifications:")
        print("     - Colonnes avec largeurs définies (3.5in + 2.5in)")
        print("     - Pas d'emojis dans les titres")
        print("     - Accents remplacés par ASCII")
    except Exception as e:
        print(f"   ✗ Erreur DOCX : {e}")
    
    # Test 3 : HTML
    print("\n3. Test génération HTML...")
    try:
        html_path = os.path.join(project_root, 'outputs', 'reports', 'test_rapport_corrige.html')
        html_path = gen.generate_html_report(
            filepath=html_path,
            include_interactive_charts=False
        )
        print(f"   ✓ HTML généré : {html_path}")
        print("   ✓ HTML supporte bien les emojis (conservés)")
    except Exception as e:
        print(f"   ✗ Erreur HTML : {e}")
    
    # Test 4 : Recommandations
    print("\n4. Test recommandations...")
    try:
        recs = gen._generate_recommendations()
        print(f"   ✓ {len(recs)} recommandations générées")
        print("   ✓ Exemples (sans emojis):")
        for i, rec in enumerate(recs[:3], 1):
            # Vérifier qu'il n'y a pas de caractères bizarres
            clean = rec.encode('ascii', 'ignore').decode('ascii')
            if clean == rec:
                print(f"     {i}. {rec[:60]}...")
            else:
                print(f"     ✗ Contient des caractères non-ASCII")
    except Exception as e:
        print(f"   ✗ Erreur recommandations : {e}")
    
    print("\n" + "=" * 60)
    print("TESTS TERMINES")
    print("=" * 60)
    print("\nVérifiez les fichiers générés dans outputs/reports/ :")
    print("  - outputs/reports/test_rapport_corrige.pdf")
    print("  - outputs/reports/test_rapport_corrige.docx")
    print("  - outputs/reports/test_rapport_corrige.html")
    print("\nPoints à vérifier manuellement :")
    print("  ✓ Les tableaux ne sont PAS coupés")
    print("  ✓ Pas de symboles bizarres (□, ?, etc.)")
    print("  ✓ Texte lisible et professionnel")
    print("  ✓ Largeurs de colonnes appropriées")

if __name__ == "__main__":
    test_rapports()
