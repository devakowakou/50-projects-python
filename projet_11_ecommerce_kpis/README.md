# 🛒 Dashboard E-commerce KPIs

Dashboard interactif pour analyser les performances e-commerce avec les KPIs essentiels : CA, panier moyen, taux de conversion.

## 🎯 Fonctionnalités

### KPIs Principaux
- **💰 Chiffre d'Affaires** : Total et évolution
- **🛒 Panier Moyen** : Valeur moyenne par commande
- **📈 Taux de Conversion** : Visiteurs → Acheteurs
- **📦 Nombre de Commandes** : Volume total

### Analyses Avancées
- 📊 Évolution temporelle du CA
- 🏆 Top 10 produits par CA
- 🎯 Répartition CA par catégorie
- 🔄 Funnel de conversion
- 📱 Performance par canal marketing
- 📈 Comparaisons période vs période

### Filtres Interactifs
- 📅 Période : 7j, 30j, 90j, 1 an
- 📱 Canal : SEO, SEM, Social, Direct, Email
- 🎛️ Interface intuitive avec sidebar

## 🚀 Installation

```bash
# Cloner et naviguer
cd projet_11_ecommerce_kpis

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

## 📊 Données

Le dashboard génère automatiquement :
- **100 produits** répartis en 6 catégories
- **1000 clients** avec profils réalistes
- **5000 commandes** sur 12 mois
- **40000+ visiteurs** (taux conversion ~12%)

## 🛠️ Architecture

```
projet_11_ecommerce_kpis/
├── src/
│   ├── data_generator.py      # Génération données réalistes
│   ├── kpi_calculator.py      # Calculs des KPIs
│   └── visualizations.py     # Graphiques Plotly
├── data/                      # Données CSV générées
├── app.py                     # Application Streamlit
└── requirements.txt           # Dépendances
```

## 📈 KPIs Calculés

### Formules
- **CA** = Σ(prix_unitaire × quantité)
- **Panier moyen** = CA total / Nombre commandes
- **Taux conversion** = (Commandes / Visiteurs) × 100
- **CA/Visiteur** = CA total / Visiteurs

### Évolutions
- Comparaison période actuelle vs précédente
- Pourcentages d'évolution avec indicateurs visuels
- Métriques delta colorées (vert/rouge)

## 🎨 Visualisations

1. **Cards KPIs** : Métriques principales avec évolutions
2. **Ligne temporelle** : Évolution du CA
3. **Barres horizontales** : Top produits
4. **Camembert** : CA par catégorie
5. **Entonnoir** : Funnel de conversion
6. **Barres groupées** : Performance par canal

## 🔧 Technologies

- **Frontend** : Streamlit
- **Data Processing** : Pandas, NumPy
- **Visualisation** : Plotly
- **Génération données** : Faker
- **Caching** : Streamlit cache

## 📱 Interface

- **Layout responsive** : Colonnes adaptatives
- **Sidebar filtres** : Contrôles intuitifs
- **Métriques colorées** : Indicateurs visuels
- **Graphiques interactifs** : Zoom, hover, export
- **Tableaux détaillés** : Expandeurs pour plus d'infos

## 🎯 Cas d'Usage

- **E-commerce managers** : Suivi performance
- **Marketing teams** : ROI par canal
- **Data analysts** : Analyses approfondies
- **Business owners** : Vue d'ensemble KPIs

## 🚀 Évolutions Possibles

- 📊 Analyse de cohortes
- 🎯 Segmentation clients RFM
- 📈 Prédictions ML
- 🔔 Alertes automatiques
- 📤 Export rapports PDF
- 🔄 Connexion APIs réelles

---

**Stack** : Streamlit + Plotly + Pandas  
**Données** : 5000 commandes générées  
**KPIs** : 6 métriques principales  
**Visualisations** : 6 graphiques interactifs