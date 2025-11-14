# 📊 Projet 12 : Calculateur de Tests A/B

**Status**: ✅ TERMINÉ | **Date**: Novembre 2025

Application web complète pour l'analyse statistique de tests A/B avec interface intuitive et visualisations interactives.

## 🎯 Objectifs

- **Analyse statistique** : Tests t, tests Z, intervalles de confiance
- **Calcul de puissance** : Taille d'échantillon optimale
- **Visualisations** : Graphiques interactifs des résultats
- **Export** : Rapports JSON et Markdown

## 🛠️ Stack Technique

- **Frontend** : Streamlit
- **Calculs** : SciPy, NumPy
- **Visualisation** : Plotly
- **Data Processing** : Pandas

## ⚡ Fonctionnalités

### 📈 Analyse de Données
- ✅ Import CSV avec validation
- ✅ Tests t pour moyennes
- ✅ Tests Z pour proportions
- ✅ Intervalles de confiance
- ✅ Calcul taille d'effet (Cohen's d, h de Cohen)

### 🧮 Calculateur Manuel
- ✅ Interface pour saisie manuelle
- ✅ Simulation de données
- ✅ Tests statistiques en temps réel

### 📏 Taille d'Échantillon
- ✅ Calcul basé sur puissance statistique
- ✅ Courbes de puissance interactives
- ✅ Recommandations personnalisées

### 🎲 Générateur de Données
- ✅ Génération de données de test
- ✅ Contrôle du bruit et des paramètres
- ✅ Export CSV

### 📊 Visualisations
- ✅ Histogrammes des distributions
- ✅ Intervalles de confiance
- ✅ Comparaisons de proportions
- ✅ Courbes de puissance

## 🚀 Installation & Lancement

```bash
# Installation
pip install -r requirements.txt

# Lancement
streamlit run app.py
# ou
python run.py
```

## 📱 Interface

L'application propose 4 onglets principaux :

1. **📈 Analyse de Données** : Import et analyse de fichiers CSV
2. **🧮 Calculateur Manuel** : Saisie manuelle des paramètres
3. **📏 Taille d'Échantillon** : Calcul de la taille optimale
4. **🎲 Générateur** : Création de données de test

## 🔬 Tests Statistiques Supportés

### T-Test (Moyennes)
- Comparaison de deux moyennes
- Calcul de Cohen's d
- Intervalles de confiance

### Z-Test (Proportions)
- Comparaison de taux de conversion
- Calcul de h de Cohen
- Tests de significativité

## 📊 Métriques Calculées

- **P-value** : Probabilité d'erreur de type I
- **Statistique de test** : T ou Z selon le test
- **Taille d'effet** : Cohen's d ou h
- **Intervalle de confiance** : À 90%, 95% ou 99%
- **Changement relatif** : Pourcentage d'amélioration

## 💾 Export des Résultats

- **JSON** : Données structurées pour intégration
- **Markdown** : Rapports lisibles
- **CSV** : Données générées

## 📁 Structure du Projet

```
projet_12_ab_test_calculator/
├── app.py                    # Application Streamlit principale
├── run.py                    # Script de lancement
├── config.py                 # Configuration
├── requirements.txt          # Dépendances
├── README.md                 # Documentation
├── src/
│   ├── statistical_tests.py  # Tests statistiques
│   ├── utils.py              # Utilitaires
│   └── visualizations.py     # Graphiques
├── data/
│   └── example_ab_test.csv   # Données d'exemple
└── tests/                    # Tests unitaires
```

## 🧪 Exemple d'Utilisation

### Test de Conversion
```python
# Groupe A: 1000 visiteurs, 50 conversions (5%)
# Groupe B: 1000 visiteurs, 65 conversions (6.5%)

# Résultat: Amélioration de +30% significative (p < 0.05)
```

### Test de Revenus
```python
# Groupe A: Moyenne 100€, écart-type 20€
# Groupe B: Moyenne 105€, écart-type 20€

# Résultat: Amélioration de +5% avec Cohen's d = 0.25
```

## 📈 Statistiques du Projet

| Métrique | Valeur |
|----------|--------|
| Lignes de code | ~400 |
| Modules | 4 |
| Tests statistiques | 2 |
| Types de visualisations | 4 |
| Formats d'export | 3 |

## 🎓 Compétences Développées

### Statistiques
- ✅ Tests d'hypothèses
- ✅ Calcul de puissance statistique
- ✅ Tailles d'effet
- ✅ Intervalles de confiance

### Développement
- ✅ Architecture modulaire
- ✅ Interface utilisateur avancée
- ✅ Visualisations interactives
- ✅ Export de données

## 🔄 Améliorations Futures

- [ ] Tests non-paramétriques (Mann-Whitney)
- [ ] Tests multivariés (ANOVA)
- [ ] Correction de Bonferroni
- [ ] Tests séquentiels
- [ ] API REST

## 📚 Ressources

- [SciPy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [A/B Testing Guide](https://www.optimizely.com/optimization-glossary/ab-testing/)
- [Statistical Power](https://en.wikipedia.org/wiki/Statistical_power)

---

**🎯 Projet 12/50 terminé** | **Progression**: 24% | **Prochaine étape**: Projet 13