# 🧹 Projet 15 : Pipeline de Nettoyage Automatique de Datasets

**Status**: 🚧 EN DÉVELOPPEMENT | **Date**: 29 oct 2025

## 🎯 Objectif

Pipeline automatisé pour nettoyer et standardiser des datasets bruts :
- Import multi-formats (CSV, Excel, JSON)
- Détection et correction des valeurs manquantes
- Standardisation des formats (dates, texte, nombres)
- Gestion des doublons et outliers
- Export de datasets propres avec rapport détaillé

## 🔧 Stack Technique

- **Langage**: Python 3.x
- **Data Processing**: Pandas, NumPy
- **Validation**: Pandera
- **Logging**: Rich (interface moderne)
- **Visualisation**: Plotly
- **Export**: CSV, Parquet, JSON

## 📊 Fonctionnalités

### ✅ Niveau Basique
- ✅ Import multi-formats (CSV, Excel, JSON)
- ✅ Profilage automatique des données
- ✅ Nettoyage des valeurs manquantes (5 stratégies)
- ✅ Détection et suppression des doublons
- ✅ Standardisation des formats (dates, texte)
- ✅ Export avec rapport de nettoyage

### 🔄 Niveau Intermédiaire
- ✅ Détection d'outliers (Z-score, IQR)
- ✅ Validation automatisée des types
- ✅ Rapport synthétique avant/après
- ✅ Interface Streamlit interactive

### 🚀 Niveau Avancé
- 🔄 Pipeline batch pour dossiers multiples
- 🔄 Transformations avancées
- 🔄 Notifications et logging détaillé

## 🏗️ Architecture

```
projet_15_pipeline_nettoyage/
├── src/
│   ├── data_loader.py      # Import multi-formats
│   ├── data_profiler.py    # Profilage initial
│   ├── data_cleaner.py     # Nettoyage principal
│   ├── data_validator.py   # Validation et contraintes
│   ├── data_exporter.py    # Export et rapports
│   └── pipeline.py         # Orchestration complète
├── app.py                  # Interface Streamlit
├── config.py              # Configuration
├── requirements.txt       # Dépendances
└── data/
    ├── raw/              # Datasets bruts
    ├── cleaned/          # Datasets nettoyés
    └── reports/          # Rapports de nettoyage
```

## 🚀 Quick Start

```bash
# Installation
pip install -r requirements.txt

# Lancer l'interface
streamlit run app.py

# Ou utiliser le pipeline en CLI
python -m src.pipeline --input data/raw/dataset.csv --output data/cleaned/
```

## 📈 Métriques de Nettoyage

Le pipeline génère automatiquement :
- **Avant/Après** : Lignes, colonnes, types
- **Valeurs manquantes** : Détectées et corrigées
- **Doublons** : Nombre supprimé
- **Outliers** : Détectés par méthode
- **Standardisation** : Formats corrigés
- **Temps d'exécution** : Performance

## 🎨 Interface Streamlit

1. **Upload** : Glisser-déposer vos fichiers
2. **Configuration** : Choisir les stratégies de nettoyage
3. **Aperçu** : Voir les données avant/après
4. **Nettoyage** : Lancer le pipeline automatique
5. **Export** : Télécharger le dataset propre + rapport

## 📋 Stratégies de Nettoyage

### Valeurs Manquantes
- **Suppression** : Lignes ou colonnes
- **Imputation** : Moyenne, médiane, mode
- **Forward/Backward Fill** : Propagation
- **Valeur par défaut** : Personnalisée

### Outliers
- **Z-Score** : |z| > 3
- **IQR** : Q1 - 1.5*IQR ou Q3 + 1.5*IQR
- **Percentiles** : 1er et 99e percentile

### Standardisation
- **Dates** : Format ISO (YYYY-MM-DD)
- **Texte** : Minuscules, trim, normalisation
- **Nombres** : Conversion de types

## 🔍 Exemple d'Utilisation

```python
from src.pipeline import DataCleaningPipeline

# Initialiser le pipeline
pipeline = DataCleaningPipeline()

# Charger et nettoyer
result = pipeline.process_file(
    input_path="data/raw/messy_data.csv",
    output_path="data/cleaned/clean_data.csv",
    strategies={
        'missing_values': 'median',
        'outliers': 'iqr',
        'duplicates': True,
        'standardize': True
    }
)

# Rapport automatique
print(f"Nettoyage terminé : {result.summary}")
```

## 📊 Rapport de Nettoyage

```
🧹 RAPPORT DE NETTOYAGE - dataset.csv
═══════════════════════════════════════

📊 RÉSUMÉ
├── Lignes : 10,000 → 9,847 (-153)
├── Colonnes : 15 → 15 (=)
├── Valeurs manquantes : 1,247 → 0 (-1,247)
├── Doublons : 89 → 0 (-89)
└── Outliers : 64 → 12 (-52)

🔧 OPÉRATIONS EFFECTUÉES
├── ✅ Imputation par médiane (colonnes numériques)
├── ✅ Suppression des doublons complets
├── ✅ Détection outliers par IQR
├── ✅ Standardisation des dates
└── ✅ Normalisation du texte

⏱️ PERFORMANCE
└── Temps d'exécution : 2.34 secondes
```

## 🧪 Tests et Validation

- **Tests unitaires** : Chaque module testé
- **Datasets de test** : Données corrompues volontairement
- **Validation** : Contraintes et types vérifiés
- **Performance** : Benchmarks sur gros datasets

## 📚 Documentation Technique

### Modules Principaux

- **DataLoader** : Import intelligent multi-formats
- **DataProfiler** : Analyse exploratoire automatique
- **DataCleaner** : Nettoyage avec stratégies configurables
- **DataValidator** : Validation et contraintes
- **DataExporter** : Export avec métadonnées

### Configuration

```python
CLEANING_CONFIG = {
    'missing_values': {
        'strategy': 'median',  # mean, median, mode, drop, fill
        'fill_value': None
    },
    'outliers': {
        'method': 'iqr',  # zscore, iqr, percentile
        'threshold': 1.5
    },
    'duplicates': {
        'keep': 'first',  # first, last, False
        'subset': None
    }
}
```

## 🎯 Prochaines Étapes

1. **Pipeline Batch** : Traitement de dossiers complets
2. **Règles Métier** : Validation personnalisée
3. **ML Integration** : Préparation pour modélisation
4. **API REST** : Service de nettoyage
5. **Monitoring** : Qualité des données en temps réel

---

**🧹 Dataset propre = Analyse fiable !**