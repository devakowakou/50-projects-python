# 🏗️ Architecture du Dashboard E-commerce KPIs

## 📋 Vue d'ensemble

Dashboard professionnel d'analyse des performances e-commerce avec 5 KPIs essentiels, conçu avec une architecture modulaire et scalable.

## 🎯 Objectifs Business

- **Analyser les performances** d'un site e-commerce
- **Suivre 5 KPIs critiques** : CA, panier moyen, conversion, performance par source/catégorie
- **Visualiser les tendances** avec des graphiques interactifs
- **Exporter les données** pour analyses externes

## 🏗️ Architecture Technique

### Structure Modulaire

```
projet_11_ecommerce_kpis/
├── 📱 app.py                    # Interface Streamlit principale
├── ⚙️  config.py                # Configuration business
├── 🚀 run.py                    # Script de lancement
├── 🧪 test_architecture.py      # Tests d'architecture
├── 📦 requirements.txt          # Dépendances
├── 📚 README.md                 # Documentation utilisateur
├── 🏗️ ARCHITECTURE.md           # Cette documentation
├── 📊 data/                     # Données générées
│   ├── transactions.json        # 10K transactions
│   └── sessions.json            # 30K sessions
└── 🔧 src/                      # Modules métier
    ├── data_generator.py        # Génération données réalistes
    ├── kpi_calculator.py        # Calculs des 5 KPIs
    ├── visualizations.py       # 6 graphiques spécialisés
    └── utils.py                 # Utilitaires (chargement, filtres, export)
```

### Séparation des Responsabilités

| Module | Responsabilité | Dépendances |
|--------|---------------|-------------|
| `config.py` | Configuration business | Aucune |
| `data_generator.py` | Génération données réalistes | `random`, `datetime` |
| `kpi_calculator.py` | Calculs KPIs et analyses | `pandas`, `numpy` |
| `visualizations.py` | Graphiques interactifs | `plotly` |
| `utils.py` | Chargement, filtres, export | `pandas`, `streamlit` |
| `app.py` | Interface utilisateur | Tous les modules |

## 📊 Modèle de Données

### Transaction (10,000 records)
```python
{
    "id": "TXN_00001",           # Identifiant unique
    "date": "2025-01-15",        # Date transaction
    "customer_id": "CUST_1234",  # ID client
    "amount": 89.99,             # Montant €
    "category": "Electronics",   # Catégorie produit (10 au total)
    "source": "organic",         # Source trafic (4 sources)
    "products_count": 2          # Nombre produits
}
```

### Session (30,000 records)
```python
{
    "id": "SESS_000001",         # Identifiant unique
    "date": "2025-01-15",        # Date session
    "source": "organic",         # Source trafic
    "converted": True,           # Conversion (True/False)
    "pages_viewed": 5            # Pages vues
}
```

## 🎯 KPIs Implémentés

### 1. 💰 Chiffre d'Affaires Total
- **Calcul** : `sum(transactions.amount)`
- **Affichage** : Métrique principale + graphique évolution
- **Filtres** : Par période, source, catégorie

### 2. 🛒 Panier Moyen (AOV)
- **Calcul** : `CA_total / nombre_transactions`
- **Affichage** : Métrique principale + analyse par segment
- **Insights** : Évolution temporelle, par source

### 3. 🎯 Taux de Conversion
- **Calcul** : `(sessions_converties / total_sessions) * 100`
- **Affichage** : Métrique principale + graphique évolution
- **Segmentation** : Par source de trafic

### 4. 📈 CA par Source de Trafic
- **Sources** : organic (40%), paid (30%), social (20%), email (10%)
- **Taux conversion** : email (5.5%) > paid (4.5%) > organic (3.5%) > social (2.5%)
- **Visualisation** : Graphique barres + tableau détaillé

### 5. 🏷️ CA par Catégorie
- **10 catégories** : Electronics, Fashion, Home, Books, Sports, Beauty, Toys, Food, Health, Automotive
- **Gammes prix** : Réalistes par catégorie (Books: €10-50, Electronics: €50-1500)
- **Visualisation** : Camembert + tableau performance

## 🎨 Interface Utilisateur

### Layout Dashboard
```
┌─────────────────────────────────────────────────┐
│  🛒 Dashboard E-commerce KPIs                   │
├─────────────────────────────────────────────────┤
│  📊 MÉTRIQUES CLÉS (4 colonnes)                │
│  [CA Total] [Panier Moy] [Conv Rate] [Trans]   │
├─────────────────────────────────────────────────┤
│  📈 ÉVOLUTIONS TEMPORELLES (2 colonnes)        │
│  [Graphique CA]        [Graphique Conversion]  │
├─────────────────────────────────────────────────┤
│  🔍 ANALYSES PAR SEGMENT (2 colonnes)          │
│  [CA par Source]       [Top Catégories]        │
├─────────────────────────────────────────────────┤
│  🎯 ANALYSE CONVERSION                          │
│  [Conversion par Source - Graphique barres]    │
├─────────────────────────────────────────────────┤
│  📋 DONNÉES DÉTAILLÉES (3 onglets)             │
│  [CA par Source] [CA par Catégorie] [Conv]     │
└─────────────────────────────────────────────────┘
```

### Sidebar
- **📅 Filtres temporels** : Sélection période personnalisée
- **📊 Informations** : Nombre transactions/sessions, période
- **📥 Export** : Rapports Markdown et CSV

## 🎨 Visualisations

### 6 Types de Graphiques Spécialisés

1. **📈 Évolution CA** : Graphique linéaire avec tendance
2. **📊 Évolution Conversion** : Suivi taux de conversion
3. **📊 CA par Source** : Barres comparatives par canal
4. **🥧 Top Catégories** : Camembert des performances
5. **🎯 Conversion par Source** : Efficacité par canal
6. **📊 KPIs Résumé** : Indicateurs synthétiques

### Caractéristiques Graphiques
- **Interactivité** : Hover, zoom, sélection
- **Responsive** : Adaptation écran
- **Couleurs** : Palette cohérente business
- **Tooltips** : Informations détaillées

## ⚙️ Configuration Business

### Sources de Trafic (4)
```python
TRAFFIC_SOURCES = ["organic", "paid", "social", "email"]

SOURCE_WEIGHTS = {
    "organic": 0.4,    # 40% du trafic
    "paid": 0.3,       # 30% du trafic  
    "social": 0.2,     # 20% du trafic
    "email": 0.1       # 10% du trafic
}

CONVERSION_RATES = {
    "organic": 0.035,   # 3.5%
    "paid": 0.045,      # 4.5%
    "social": 0.025,    # 2.5%
    "email": 0.055      # 5.5%
}
```

### Catégories Produits (10)
```python
PRODUCT_CATEGORIES = [
    "Electronics", "Fashion", "Home", "Books", "Sports",
    "Beauty", "Toys", "Food", "Health", "Automotive"
]

CATEGORY_PRICE_RANGES = {
    "Electronics": (50, 1500),    # High-ticket
    "Fashion": (20, 300),         # Medium range
    "Books": (10, 50),            # Low-ticket
    # ... etc
}
```

## 🚀 Performance & Scalabilité

### Optimisations Implémentées
- **Cache Streamlit** : `@st.cache_data` pour chargement données
- **Calculs optimisés** : Pandas groupby pour agrégations
- **Génération efficace** : Données réalistes avec distributions pondérées
- **Mémoire** : Structures de données optimales

### Métriques Performance
- **Génération données** : 10K transactions + 30K sessions en ~5 secondes
- **Chargement dashboard** : < 2 secondes avec cache
- **Calculs KPIs** : < 1 seconde pour tous les KPIs
- **Graphiques** : Rendu interactif instantané

## 🧪 Tests & Validation

### Tests d'Architecture (7 tests)
1. **Génération données** : Volume et structure
2. **KPI Calculator** : Import et structure
3. **Visualisations** : Import modules graphiques
4. **Utilitaires** : Fonctions helper
5. **Configuration** : Constantes business
6. **Structure fichiers** : Présence fichiers requis
7. **Calculs KPIs** : Validation logique métier

### Validation Données
- **Volume** : 10,000 transactions, 30,000 sessions
- **Cohérence** : Dates, montants, catégories
- **Réalisme** : Distributions pondérées, taux conversion
- **Intégrité** : Pas de valeurs manquantes

## 🔧 Extensibilité

### Ajouts Faciles
- **Nouvelles métriques** : Ajouter dans `kpi_calculator.py`
- **Graphiques** : Nouvelles visualisations dans `visualizations.py`
- **Sources données** : Adapter `data_generator.py`
- **Filtres** : Étendre `utils.py`

### Architecture Modulaire
- **Découplage** : Modules indépendants
- **Interfaces claires** : APIs bien définies
- **Configuration centralisée** : `config.py`
- **Tests unitaires** : Validation par module

## 📚 Documentation

### Niveaux Documentation
1. **README.md** : Guide utilisateur complet
2. **ARCHITECTURE.md** : Cette documentation technique
3. **Docstrings** : Documentation inline du code
4. **Comments** : Explications logique métier

### Standards Code
- **PEP 8** : Style guide Python
- **Type hints** : Annotations de types
- **Error handling** : Gestion robuste erreurs
- **Logging** : Messages informatifs

## 🎯 Résultats Attendus

### KPIs Typiques
- **CA Total** : ~€2.3M (sur 10K transactions)
- **Panier Moyen** : ~€235
- **Taux Conversion** : ~3.5%
- **Top Source** : Organic (~40% CA)
- **Top Catégorie** : Electronics (~20-25% CA)

### Insights Business
- **Email** : Meilleur taux conversion (5.5%) mais faible volume
- **Paid** : Bon équilibre volume/conversion (4.5%)
- **Social** : Volume correct mais conversion faible (2.5%)
- **Electronics** : Catégorie la plus rentable (panier élevé)

---

## 🏆 Points Forts Architecture

✅ **Modulaire** : Séparation claire des responsabilités  
✅ **Scalable** : Facilement extensible  
✅ **Testable** : Architecture testée et validée  
✅ **Performant** : Optimisations cache et calculs  
✅ **Réaliste** : Données business cohérentes  
✅ **Professionnel** : Interface moderne et intuitive  
✅ **Documenté** : Documentation complète  

Cette architecture garantit un dashboard robuste, maintenable et évolutif pour l'analyse des performances e-commerce.