#  Budget Dashboard - Projet 2

> Application web de suivi de budget personnel avec analyses et visualisations

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/Status-MVP-success)](.)

---

##  Description

Application web interactive pour gérer son budget personnel :
- Suivi des revenus et dépenses
- Visualisations interactives (graphiques Plotly)
- Alertes de dépassement de budget
- Export des données (CSV, JSON)
- Interface intuitive Streamlit

## ✨ Fonctionnalités MVP

###  Gestion des Transactions
-  Ajouter revenus/dépenses
-  Historique complet
-  Filtres par période/catégorie
-  Import/Export CSV et JSON

###  Dashboard
-  4 métriques clés (Solde, Revenus, Dépenses, Économies)
-  Graphique d'évolution temporelle
-  Répartition par catégorie (camembert)
-  État des budgets (barres + seuils)
-  Top 10 des dépenses

###  Système d'Alertes
-  Alerte à 80% du budget (warning)
-  Alerte à 100% du budget (danger)
-  Recommandations automatiques

###  Analyses
-  Statistiques par période
-  Comparaisons temporelles
-  Taux d'épargne
-  Budgets par catégorie

---

## 📂 Structure du Projet

```
projet_02_budget_dashboard/
├── app.py                          # Application Streamlit
├── config.py                       # Configuration
├── requirements.txt                # Dépendances
├── run.sh                          # Script de lancement
├── generate_example_data.py        # Génération données test
│
├── src/                            # Modules
│   ├── data_manager.py             # CRUD transactions (JSON)
│   ├── budget_analyzer.py          # Analyses et calculs
│   └── visualizer.py               # Graphiques Plotly
│
├── data/                           # Données
│   ├── transactions.json           # Base principale
│   └── exemple_transactions.json   # Données de démo
│
└── outputs/                        # Exports
```

---

## 🚀 Installation & Lancement

### Prérequis
- Python 3.9+
- pip

### Installation

```bash
# Naviguer vers le projet
cd projet_02_budget_dashboard

# Créer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Générer les données exemple
python3 generate_example_data.py
```

### Lancement

```bash
# Méthode 1 : Script automatique
./run.sh

# Méthode 2 : Commande directe
streamlit run app.py
```

L'application s'ouvre sur **http://localhost:8501**

---

## 🎨 Interface

### Pages disponibles

1. ** Dashboard** : Vue d'ensemble avec métriques et graphiques
2. ** Ajouter Transaction** : Formulaire d'ajout
3. ** Historique** : Liste complète avec filtres
4. ** Paramètres** : Configuration budgets et alertes

### Catégories Prédéfinies

**Dépenses** :
-  Alimentation
-  Logement
-  Transport
-  Factures
-  Loisirs
-  Shopping
-  Santé
-  Éducation
-  Épargne
-  Autres

**Revenus** :
-  Salaire
-  Prime/Bonus
-  Freelance
-  Investissements
-  Autres

---

##  Données Exemple

Le projet inclut un générateur de 100 transactions réalistes :
- 85% dépenses / 15% revenus
- Montants et fréquences réalistes
- Distribution sur 90 jours

```bash
python3 generate_example_data.py
```

---

## 🛠️ Stack Technique

| Technologie | Usage |
|-------------|-------|
| **Streamlit** | Interface web |
| **Pandas** | Manipulation données |
| **Plotly** | Visualisations interactives |
| **JSON** | Stockage simple |

---

##  Prochaines Améliorations (v2.0)

-  Export rapports PDF
-  Transactions récurrentes
-  Prévisions basées sur l'historique
- 💾 Support SQLite
- 👥 Multi-utilisateurs
-  Version mobile optimisée

---

##  Licence

Projet libre - Challenge 50 Projets Python

---

## 👨‍💻 Auteur

Projet 2 du Challenge 50 Projets Python
Date : 28 octobre 2025
