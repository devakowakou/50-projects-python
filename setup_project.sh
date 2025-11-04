#!/bin/bash

echo "🚀 Configuration du Projet 07 - PDF Reporter..."

# Couleurs pour les messages
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Création de la structure de base
echo -e "${BLUE}📁 Création de la structure de dossiers...${NC}"

mkdir -p projet_07_pdf_reporter/{data/samples,outputs,templates/{commercial,financier,technique},scripts,docs}
mkdir -p projet_07_pdf_reporter/src/{ingestion,transformation,visualization,reporting,ui,utils}
mkdir -p projet_07_pdf_reporter/tests/{unit,integration,fixtures/expected_outputs}

# Création des fichiers __init__.py
echo -e "${BLUE}📄 Création des fichiers __init__.py...${NC}"

touch projet_07_pdf_reporter/src/__init__.py
touch projet_07_pdf_reporter/src/ingestion/__init__.py
touch projet_07_pdf_reporter/src/transformation/__init__.py
touch projet_07_pdf_reporter/src/visualization/__init__.py
touch projet_07_pdf_reporter/src/reporting/__init__.py
touch projet_07_pdf_reporter/src/ui/__init__.py
touch projet_07_pdf_reporter/src/utils/__init__.py
touch projet_07_pdf_reporter/tests/__init__.py
touch projet_07_pdf_reporter/tests/unit/__init__.py
touch projet_07_pdf_reporter/tests/integration/__init__.py

# Création des fichiers principaux
echo -e "${BLUE}📝 Création des fichiers principaux...${NC}"

touch projet_07_pdf_reporter/app.py
touch projet_07_pdf_reporter/config.py
touch projet_07_pdf_reporter/requirements.txt
touch projet_07_pdf_reporter/README.md
touch projet_07_pdf_reporter/.gitignore

# Fichiers de données
touch projet_07_pdf_reporter/data/samples/.gitkeep
touch projet_07_pdf_reporter/outputs/.gitkeep

# Fichiers templates
touch projet_07_pdf_reporter/templates/commercial/template.json
touch projet_07_pdf_reporter/templates/commercial/styles.css
touch projet_07_pdf_reporter/templates/financier/template.json
touch projet_07_pdf_reporter/templates/financier/styles.css
touch projet_07_pdf_reporter/templates/technique/template.json
touch projet_07_pdf_reporter/templates/technique/styles.css

# Modules ingestion
touch projet_07_pdf_reporter/src/ingestion/excel_reader.py
touch projet_07_pdf_reporter/src/ingestion/validator.py

# Modules transformation
touch projet_07_pdf_reporter/src/transformation/transformer.py
touch projet_07_pdf_reporter/src/transformation/kpi_calculator.py

# Modules visualization
touch projet_07_pdf_reporter/src/visualization/chart_generator.py
touch projet_07_pdf_reporter/src/visualization/chart_config.py

# Modules reporting
touch projet_07_pdf_reporter/src/reporting/pdf_builder.py
touch projet_07_pdf_reporter/src/reporting/template_engine.py
touch projet_07_pdf_reporter/src/reporting/formatters.py

# Modules UI
touch projet_07_pdf_reporter/src/ui/components.py
touch projet_07_pdf_reporter/src/ui/pages.py
touch projet_07_pdf_reporter/src/ui/styles.py

# Modules utils
touch projet_07_pdf_reporter/src/utils/helpers.py
touch projet_07_pdf_reporter/src/utils/logger.py
touch projet_07_pdf_reporter/src/utils/constants.py

# Tests
touch projet_07_pdf_reporter/tests/conftest.py
touch projet_07_pdf_reporter/tests/unit/test_excel_reader.py
touch projet_07_pdf_reporter/tests/unit/test_transformer.py
touch projet_07_pdf_reporter/tests/unit/test_chart_generator.py
touch projet_07_pdf_reporter/tests/unit/test_pdf_builder.py
touch projet_07_pdf_reporter/tests/integration/test_pipeline.py
touch projet_07_pdf_reporter/tests/integration/test_templates.py
touch projet_07_pdf_reporter/tests/fixtures/sample_data.xlsx

# Scripts
touch projet_07_pdf_reporter/scripts/batch_generate.py
touch projet_07_pdf_reporter/scripts/migrate_templates.py

# Documentation
touch projet_07_pdf_reporter/docs/architecture.md
touch projet_07_pdf_reporter/docs/templates_guide.md
touch projet_07_pdf_reporter/docs/api_reference.md

echo -e "${GREEN}✅ Structure créée avec succès!${NC}"

# Création de l'environnement virtuel
echo -e "${BLUE}🐍 Création de l'environnement virtuel...${NC}"
cd projet_07_pdf_reporter
python3.11 -m venv .venv

echo -e "${GREEN}✅ Environnement virtuel créé!${NC}"

echo ""
echo -e "${GREEN}🎉 Projet configuré avec succès!${NC}"
echo ""
echo "Prochaines étapes:"
echo "1. cd projet_07_pdf_reporter"
echo "2. source .venv/bin/activate"
echo "3. pip install -r requirements.txt"
echo "4. streamlit run app.py"
echo ""