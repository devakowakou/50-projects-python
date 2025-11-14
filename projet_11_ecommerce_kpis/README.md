# 🛒 Projet 11 : Dashboard E-commerce KPIs

**Status**: ✅ TERMINÉ | **Date**: 29 octobre 2025 | **Durée**: ~90 minutes

Dashboard complet d'analyse des performances e-commerce avec 5 KPIs essentiels et visualisations interactives.

## 🎯 Objectifs

Créer un dashboard professionnel pour analyser les performances d'un site e-commerce avec :
- **5 KPIs principaux** : CA, panier moyen, conversion, performance par source/catégorie
- **10,000 transactions** et **30,000 sessions** simulées
- **Visualisations interactives** avec Plotly
- **Filtres temporels** et export de rapports

## 📊 KPIs Implémentés

### KPIs Principaux
1. **💰 Chiffre d'Affaires Total** : Revenus globaux sur la période
2. **🛒 Panier Moyen (AOV)** : Montant moyen par transaction
3. **🎯 Taux de Conversion** : % de sessions qui convertissent
4. **📈 CA par Source** : Performance par canal d'acquisition
5. **🏷️ CA par Catégorie** : Revenus par segment produit

### Métriques Secondaires
- Évolution temporelle (jour/semaine/mois)
- Conversion par source de trafic
- Top catégories performantes
- Nombre de transactions et sessions

## 🏗️ Architecture

### Structure Modulaire
```
projet_11_ecommerce_kpis/
├── src/
│   ├── data_generator.py      # Génération 10K transactions réalistes
│   ├── kpi_calculator.py      # Calculs des 5 KPIs + analyses
│   ├── visualizations.py     # 6 types de graphiques spécialisés
│   └── utils.py              # Chargement, filtres, export
├── app.py                     # Dashboard Streamlit principal
├── config.py                  # Configuration business (10 catégories, 4 sources)
├── requirements.txt           # Dépendances minimales
├── data/                      # Données JSON générées
└── README.md                  # Cette documentation
```

### Modèle de Données
```python
# Transaction (10,000 records)
{
    "id": "TXN_00001",
    "date": "2025-01-15",
    "customer_id": "CUST_1234",
    "amount": 89.99,
    "category": "Electronics",  # 10 catégories
    "source": "organic",        # organic, paid, social, email
    "products_count": 2
}

# Session (30,000 records)
{
    "id": "SESS_000001",
    "date": "2025-01-15",
    "source": "organic",
    "converted": True,
    "pages_viewed": 5
}
```

## 🛠️ Stack Technique

### Core Technologies
- **Frontend** : Streamlit (dashboard interactif)
- **Data Processing** : Pandas (manipulation données)
- **Visualisation** : Plotly (graphiques business)
- **Calculs** : NumPy (métriques mathématiques)

### Fonctionnalités
- **Génération de données** : 10K transactions réalistes avec Faker
- **Cache intelligent** : Streamlit cache pour performances
- **Filtres temporels** : Analyse par période personnalisée
- **Export** : Rapports Markdown et CSV
- **Responsive** : Interface adaptative

## 🚀 Installation & Utilisation

### Installation
```bash
cd projet_11_ecommerce_kpis
pip install -r requirements.txt
```

### Lancement
```bash
streamlit run app.py
```

### Première utilisation
1. **Génération automatique** : Les données sont générées au premier lancement
2. **Filtres** : Utilisez la sidebar pour filtrer par période
3. **Export** : Téléchargez rapports et données via la sidebar

## 📈 Fonctionnalités Détaillées

### Dashboard Principal
- **4 métriques clés** en temps réel (CA, panier, conversion, transactions)
- **Graphiques d'évolution** temporelle (CA et conversion)
- **Analyses par segment** (source et catégorie)
- **Tableaux détaillés** avec données complètes

### Visualisations
1. **Évolution CA** : Graphique linéaire avec tendance
2. **Évolution Conversion** : Suivi du taux de conversion
3. **CA par Source** : Barres comparatives par canal
4. **Top Catégories** : Camembert des meilleures performances
5. **Conversion par Source** : Efficacité par canal
6. **KPIs Résumé** : Indicateurs synthétiques

### Filtres & Export
- **Filtre temporel** : Sélection de période personnalisée
- **Rapport Markdown** : Synthèse des KPIs principaux
- **Export CSV** : Données filtrées pour analyse externe

## 📊 Configuration Business

### 10 Catégories Produits
- Electronics, Fashion, Home, Books, Sports
- Beauty, Toys, Food, Health, Automotive

### 4 Sources de Trafic
- **Organic** (40%) : Taux conversion 3.5%
- **Paid** (30%) : Taux conversion 4.5%
- **Social** (20%) : Taux conversion 2.5%
- **Email** (10%) : Taux conversion 5.5%

### Gammes de Prix
- Electronics: €50-1500 | Fashion: €20-300
- Home: €30-800 | Books: €10-50
- Sports: €25-400 | Beauty: €15-150
- Toys: €10-100 | Food: €5-80
- Health: €20-200 | Automotive: €40-1000

## 🎯 Métriques de Performance

### Données Générées
- **10,000 transactions** sur 90 jours
- **30,000 sessions** (ratio 3:1 réaliste)
- **~5,000 clients uniques**
- **Distribution réaliste** par source et catégorie

### KPIs Typiques Attendus
- **CA Total** : ~€500K-800K
- **Panier Moyen** : ~€50-120
- **Taux Conversion** : ~3-4%
- **Top Source** : Organic (~40% du CA)
- **Top Catégorie** : Electronics (~20-25% du CA)

## 🔧 Personnalisation

### Modifier les Catégories
```python
# config.py
PRODUCT_CATEGORIES = [
    "Votre_Categorie_1", "Votre_Categorie_2", ...
]
```

### Ajuster les Prix
```python
# config.py
CATEGORY_PRICE_RANGES = {
    "Votre_Categorie": (prix_min, prix_max),
}
```

### Changer les Sources
```python
# config.py
TRAFFIC_SOURCES = ["source1", "source2", ...]
CONVERSION_RATES = {"source1": 0.035, ...}
```

## 📚 Apprentissages

### Techniques
- **Architecture modulaire** : Séparation claire des responsabilités
- **Cache Streamlit** : Optimisation des performances
- **Plotly avancé** : Graphiques business interactifs
- **Pandas groupby** : Agrégations complexes efficaces

### Business
- **KPIs e-commerce** : Métriques essentielles du retail
- **Analyse de conversion** : Optimisation par canal
- **Segmentation** : Performance par catégorie/source
- **Reporting** : Export et synthèse automatisés

## 🚀 Extensions Possibles

### Court Terme
- [ ] Analyse de cohortes clients
- [ ] Prédiction de tendances (Prophet)
- [ ] Alertes sur seuils KPIs
- [ ] Dashboard temps réel

### Moyen Terme
- [ ] Intégration base de données
- [ ] API REST pour données
- [ ] Machine Learning (churn, recommandations)
- [ ] A/B testing framework

## 📊 Statistiques du Projet

| Métrique | Valeur |
|----------|--------|
| Lignes de code | ~400 |
| Modules | 5 |
| Fonctions | 25+ |
| Graphiques | 6 types |
| KPIs | 5 principaux |
| Temps développement | ~90 min |
| Technologies | 4 |

## 🏆 Résultats

### Fonctionnalités Livrées
- ✅ Dashboard complet avec 5 KPIs
- ✅ 10,000 transactions réalistes générées
- ✅ 6 types de visualisations interactives
- ✅ Filtres temporels avancés
- ✅ Export rapports et données
- ✅ Interface responsive et intuitive
- ✅ Architecture modulaire et maintenable

### Performance
- ⚡ Chargement instantané (cache)
- 📊 Graphiques fluides et interactifs
- 🔄 Filtrage temps réel
- 💾 Export rapide

---

## 🤝 Utilisation

Ce dashboard peut servir de :
- **Template** pour projets e-commerce
- **Outil d'analyse** pour données réelles
- **Base d'apprentissage** pour KPIs business
- **Démo** pour présentations clients

---

**🛒 Dashboard E-commerce KPIs - Projet 11/50 Complété !**

*Prochaine étape : Projet 12 - Calculatrice de significativité statistique pour A/B test*