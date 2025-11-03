# 📚 Documentation Technique - Analyseur CSV Professionnel

## 🏗️ Architecture Détaillée

### Principes de Conception

L'application suit le principe de **Separation of Concerns (SoC)** avec une architecture modulaire où chaque module a une responsabilité unique et bien définie.

### Modules et Responsabilités

#### 1. `data_loader.py` - Chargement des Données
**Responsabilité**: Charger et valider les fichiers CSV/Excel

**Classe principale**: `DataLoader`

**Méthodes clés**:
- `detect_encoding()` : Détecte automatiquement l'encodage du fichier
- `load_from_upload()` : Charge depuis l'upload Streamlit
- `load_from_path()` : Charge depuis un chemin de fichier
- `validate_data()` : Valide la structure et la qualité
- `get_column_types()` : Identifie les types de colonnes

**Technologies**: pandas, chardet, io

---

#### 2. `data_cleaner.py` - Nettoyage des Données
**Responsabilité**: Prétraiter et nettoyer les données

**Classe principale**: `DataCleaner`

**Méthodes clés**:
- `get_missing_values_summary()` : Résumé des valeurs manquantes
- `handle_missing_values()` : Traite les NaN (5 stratégies)
- `remove_duplicates()` : Supprime les doublons
- `convert_column_type()` : Convertit les types
- `normalize_column_names()` : Normalise les noms
- `remove_outliers_iqr()` : Supprime les outliers
- `get_data_quality_report()` : Rapport de qualité

**Stratégies d'imputation**:
1. Drop : Suppression des lignes
2. Mean : Remplacement par la moyenne
3. Median : Remplacement par la médiane
4. Mode : Remplacement par le mode
5. Custom : Valeur personnalisée

---

#### 3. `statistical_analyzer.py` - Analyses Statistiques
**Responsabilité**: Calculer toutes les statistiques descriptives

**Classe principale**: `StatisticalAnalyzer`

**Méthodes clés**:
- `get_basic_statistics()` : Stats de base (mean, std, quartiles...)
- `get_advanced_statistics()` : Stats avancées (skewness, kurtosis...)
- `get_distribution_analysis()` : Tests de normalité
- `get_frequency_analysis()` : Analyse de fréquence
- `get_percentiles()` : Calcul de percentiles personnalisés
- `get_summary_by_category()` : Stats groupées

**Tests statistiques**:
- Shapiro-Wilk (normalité, n < 5000)
- Kolmogorov-Smirnov (normalité, tout n)

---

#### 4. `correlation_analyzer.py` - Analyse de Corrélation
**Responsabilité**: Analyser les relations entre variables

**Classe principale**: `CorrelationAnalyzer`

**Méthodes clés**:
- `get_correlation_matrix()` : Matrice complète
- `get_correlation_pairs()` : Paires fortement corrélées
- `test_correlation_significance()` : Tests statistiques
- `get_top_correlations()` : Top N corrélations
- `detect_multicollinearity()` : Détection de multicolinéarité
- `calculate_partial_correlation()` : Corrélation partielle

**Méthodes de corrélation**:
1. **Pearson** : Corrélation linéaire (r)
   - Mesure la relation linéaire
   - Sensible aux outliers
   - Assume normalité

2. **Spearman** : Corrélation de rang (ρ)
   - Non-paramétrique
   - Détecte relations monotones
   - Résistant aux outliers

3. **Kendall** : Tau de Kendall (τ)
   - Non-paramétrique
   - Basé sur concordance
   - Préféré pour petits échantillons

**Interprétation**:
- |r| ≥ 0.9 : Très forte
- |r| ≥ 0.7 : Forte
- |r| ≥ 0.5 : Modérée
- |r| ≥ 0.3 : Faible
- |r| < 0.3 : Très faible

---

#### 5. `anomaly_detector.py` - Détection d'Anomalies
**Responsabilité**: Identifier les valeurs aberrantes

**Classe principale**: `AnomalyDetector`

**Méthodes clés**:
- `detect_outliers_iqr()` : Méthode IQR
- `detect_outliers_zscore()` : Méthode Z-Score
- `detect_outliers_all_columns()` : Détection globale
- `get_multivariate_outliers()` : Mahalanobis
- `compare_methods()` : Comparaison des méthodes
- `suggest_treatment()` : Suggestions de traitement

**Méthode IQR (Interquartile Range)**:
```
Q1 = 25e percentile
Q3 = 75e percentile
IQR = Q3 - Q1

Outliers si:
  x < Q1 - 1.5×IQR  OU  x > Q3 + 1.5×IQR
  
Outliers extrêmes si:
  x < Q1 - 3×IQR  OU  x > Q3 + 3×IQR
```

**Méthode Z-Score**:
```
z = (x - μ) / σ

Outlier si: |z| > 3
```

**Distance de Mahalanobis** (multivarié):
```
D² = (x - μ)ᵀ Σ⁻¹ (x - μ)

Outlier si: D² > χ²(p, 0.95)
```

---

#### 6. `visualizer.py` - Visualisations
**Responsabilité**: Créer tous les graphiques interactifs

**Classe principale**: `Visualizer`

**Méthodes clés**:
- `create_histogram()` : Distribution avec courbe normale
- `create_boxplot()` : Box plots pour outliers
- `create_correlation_heatmap()` : Heatmap de corrélation
- `create_scatter_plot()` : Scatter avec tendance
- `create_bar_chart()` : Fréquences catégoriques
- `create_pie_chart()` : Répartition en camembert
- `create_violin_plot()` : Distribution détaillée
- `create_missing_values_chart()` : Visualisation des NaN

**Technologies**: Plotly (graphiques interactifs)

**Avantages de Plotly**:
- Interactivité (zoom, hover, sélection)
- Responsive design
- Export PNG/SVG
- Thèmes personnalisables

---

#### 7. `report_generator.py` - Génération de Rapports
**Responsabilité**: Exporter les résultats

**Classe principale**: `ReportGenerator`

**Méthodes clés**:
- `export_to_csv()` : Export CSV
- `export_statistics_to_json()` : Stats en JSON
- `generate_markdown_report()` : Rapport formaté
- `export_cleaned_data()` : Données nettoyées
- `create_excel_report()` : Rapport Excel multi-feuilles

**Formats supportés**:
- CSV (données)
- JSON (statistiques)
- Markdown (rapport lisible)
- Excel (rapport complet)

---

### Flux de Données

```
1. Upload CSV
   ↓
2. DataLoader → Validation
   ↓
3. DataCleaner → Nettoyage (optionnel)
   ↓
4. Analyse parallèle:
   ├─ StatisticalAnalyzer → Statistiques
   ├─ CorrelationAnalyzer → Corrélations
   └─ AnomalyDetector → Anomalies
   ↓
5. Visualizer → Graphiques
   ↓
6. ReportGenerator → Export
```

---

## 🎨 Interface Streamlit

### Structure de l'Application

**Sidebar**:
- Configuration
- Upload de fichiers
- Métadonnées du fichier

**Main Content (Tabs)**:
1. Aperçu : Vue d'ensemble
2. Nettoyage : Traitement des données
3. Statistiques : Analyses descriptives
4. Corrélations : Relations entre variables
5. Anomalies : Détection d'outliers
6. Visualisations : Graphiques interactifs
7. Rapports : Export des résultats

### Session State

Variables de session Streamlit:
- `df` : DataFrame original
- `df_cleaned` : DataFrame nettoyé
- `file_info` : Métadonnées du fichier

---

## 🔧 Configuration (`config.py`)

### Paramètres Modifiables

**Application**:
- `APP_TITLE` : Titre de l'app
- `APP_LAYOUT` : "wide" ou "centered"
- `MAX_FILE_SIZE_MB` : Taille max des fichiers

**Statistiques**:
- `CONFIDENCE_LEVEL` : Niveau de confiance (défaut: 0.95)
- `IQR_MULTIPLIER` : Multiplicateur IQR (défaut: 1.5)
- `Z_SCORE_THRESHOLD` : Seuil Z-Score (défaut: 3)

**Corrélation**:
- `CORRELATION_THRESHOLD` : Seuil significatif (défaut: 0.7)

**Visualisation**:
- `PLOTLY_THEME` : Thème Plotly
- `COLOR_PALETTE` : Palette de couleurs

---

##  Cas d'Usage

### 1. Analyse de Ventes
```python
# Charger les données
# Statistiques par région, par produit
# Corrélations prix-quantité
# Détection de ventes anormales
```

### 2. Contrôle Qualité
```python
# Charger mesures de production
# Identifier les outliers
# Analyser la distribution
# Générer rapport de conformité
```

### 3. Analyse de Marketing
```python
# Données de campagnes
# Corrélations budget-conversions
# Identifier segments performants
# Visualiser KPIs
```

---

##  Tests et Validation

### Tests Manuels

1. **Test de Chargement**
   - Fichier vide
   - Encodage incorrect
   - Format non supporté
   - Fichier très volumineux

2. **Test de Nettoyage**
   - 100% valeurs manquantes
   - Aucune valeur manquante
   - Tous duplicatas

3. **Test de Statistiques**
   - Aucune colonne numérique
   - Distribution normale
   - Distribution asymétrique

4. **Test de Corrélation**
   - Moins de 2 colonnes numériques
   - Corrélation parfaite (1.0)
   - Aucune corrélation

---

## Optimisations Futures

### Performance
- [ ] Lazy loading pour gros fichiers
- [ ] Cache des calculs lourds
- [ ] Parallélisation des analyses

### Fonctionnalités
- [ ] Analyse de séries temporelles
- [ ] Machine Learning (clustering, PCA)
- [ ] Support de bases de données
- [ ] API REST

### UX/UI
- [ ] Mode sombre
- [ ] Templates de rapports
- [ ] Comparaison de datasets
- [ ] Historique des analyses

---

## 📚 Références

### Documentation
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [SciPy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Plotly Python](https://plotly.com/python/)
- [Streamlit API](https://docs.streamlit.io/library/api-reference)

### Concepts Statistiques
- Tests de normalité
- Corrélation vs Causalité
- Détection d'outliers
- Intervalles de confiance

---

**Dernière mise à jour**: 2025-10-27
