# 📊 Projet 07 - PDF Reporter

Générateur automatique de rapports PDF professionnels depuis fichiers Excel.

## 🚀 Installation

```bash
# Créer l'environnement virtuel
python3.11 -m venv .venv
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## 🎯 Utilisation

### Interface Streamlit

```bash
streamlit run app.py
```

### CLI (Batch)

```bash
python scripts/batch_generate.py --input data/samples/ --template commercial
```

## 📁 Structure

```
projet_07_pdf_reporter/
├── src/
│   ├── ingestion/      # Lecture Excel
│   ├── transformation/ # Traitement données
│   ├── visualization/  # Génération graphiques
│   ├── reporting/      # Création PDF
│   └── ui/            # Interface Streamlit
├── templates/         # Templates de rapports
├── outputs/          # PDFs générés
└── tests/           # Tests unitaires
```

## 🧪 Tests

```bash
pytest tests/ -v
pytest --cov=src tests/
```

## 📚 Templates disponibles

- **Commercial** : KPIs ventes, performances
- **Financier** : États financiers, ratios
- **Technique** : Métriques techniques

## 🔧 Configuration

Modifier `config.py` pour personnaliser :
- Chemins
- Styles PDF
- Configuration graphiques