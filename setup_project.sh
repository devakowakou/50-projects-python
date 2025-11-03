#!/bin/bash

echo "🚀 Configuration du projet Stock Analysis Dashboard..."

# Création de la structure de dossiers
echo "📁 Création de la structure de dossiers..."
mkdir -p projet_06_stock_tracker/{database,src/{layout,core,components,utils},tests/integration,assets,migrations}

# Création des fichiers principaux
echo "📄 Création des fichiers principaux..."

# Fichiers racine
touch projet_06_stock_tracker/app.py
touch projet_06_stock_tracker/requirements.txt
touch projet_06_stock_tracker/config.py
touch projet_06_stock_tracker/README.md
touch projet_06_stock_tracker/.gitignore
touch projet_06_stock_tracker/setup.py

# Database
touch projet_06_stock_tracker/database/__init__.py
touch projet_06_stock_tracker/database/models.py
touch projet_06_stock_tracker/database/crud.py
touch projet_06_stock_tracker/database/session.py

# Source
touch projet_06_stock_tracker/src/__init__.py
touch projet_06_stock_tracker/src/layout/__init__.py
touch projet_06_stock_tracker/src/layout/header.py
touch projet_06_stock_tracker/src/layout/sidebar.py
touch projet_06_stock_tracker/src/layout/charts_layout.py
touch projet_06_stock_tracker/src/core/__init__.py
touch projet_06_stock_tracker/src/core/data_manager.py
touch projet_06_stock_tracker/src/core/technical_engine.py
touch projet_06_stock_tracker/src/core/signals_engine.py
touch projet_06_stock_tracker/src/components/__init__.py
touch projet_06_stock_tracker/src/components/charts.py
touch projet_06_stock_tracker/src/components/indicators.py
touch projet_06_stock_tracker/src/utils/__init__.py
touch projet_06_stock_tracker/src/utils/helpers.py

# Tests
touch projet_06_stock_tracker/tests/__init__.py
touch projet_06_stock_tracker/tests/test_database.py
touch projet_06_stock_tracker/tests/test_core.py
touch projet_06_stock_tracker/tests/test_components.py
touch projet_06_stock_tracker/tests/integration/__init__.py
touch projet_06_stock_tracker/tests/integration/test_dashboard.py

# Assets
touch projet_06_stock_tracker/assets/style.css

echo "✅ Structure de dossiers créée!"

# Création de l'environnement virtuel
echo "🐍 Création de l'environnement virtuel Python 3.11..."
cd projet_06_stock_tracker
python3.11 -m venv .venv

echo "✅ Environnement virtuel créé!"

# Activation de l'environnement
echo "🔧 Activation de l'environnement..."
source .venv/bin/activate

# Installation des packages
echo "📦 Installation des packages..."
pip install --upgrade pip

cat > requirements.txt << 'EOF'
dash==2.14.0
dash-bootstrap-components==1.5.0
plotly==5.15.0
pandas==2.1.0
numpy==1.24.0
yfinance==0.2.18
sqlalchemy==2.0.23
python-dateutil==2.8.2
pytest==7.4.0
pytest-dash==2.1.0
selenium==4.15.0
gunicorn==21.2.0
EOF

pip install -r requirements.txt

echo "✅ Packages installés!"

# Création des fichiers de configuration
echo "⚙️ Création des fichiers de configuration..."

# .gitignore
cat > .gitignore << 'EOF'
# Environment
.venv/
.env
.env.local

# Database
*.db
*.sqlite3

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.so

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp

# Data cache
data/cache/
EOF

# Fichier de configuration
cat > config.py << 'EOF'
"""
Configuration de l'application Stock Analysis Dashboard
"""

import os

# Configuration de la base de données
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'stock_analysis.db')}"

# Configuration des données boursières
DEFAULT_SYMBOLS = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "NFLX"]
DEFAULT_TIMEFRAME = "6mo"
DEFAULT_PERIOD = "1y"

# Configuration des indicateurs techniques
INDICATOR_CONFIG = {
    "sma_periods": [20, 50, 200],
    "ema_periods": [12, 26],
    "rsi_period": 14,
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,
    "bollinger_period": 20,
    "bollinger_std": 2
}

# Configuration de l'interface
CHART_CONFIG = {
    "height": 600,
    "template": "plotly_white",
    "colors": {
        "primary": "#1f77b4",
        "secondary": "#ff7f0e", 
        "success": "#2ca02c",
        "danger": "#d62728",
        "warning": "#ffbb78",
        "info": "#17a2b8"
    }
}

# Configuration du layout
LAYOUT_CONFIG = {
    "sidebar_width": 2,
    "main_width": 10,
    "header_height": "60px"
}
EOF

# Création du dossier data
mkdir -p data

echo "✅ Configuration créée!"

# Message final
echo ""
echo "🎉 Projet configuré avec succès!"
echo ""
echo "Prochaines étapes:"
echo "1. cd projet_06_stock_tracker"
echo "2. source .venv/bin/activate"
echo "3. python app.py"
echo ""
echo "🚀 Prêt pour le développement!"
