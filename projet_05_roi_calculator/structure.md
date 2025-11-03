# 📁 Structure du Projet - ROI Marketing Calculator

```
projet_05_roi_calculator/
│
├── 📄 app.py                           # Application Streamlit principale
├── 📄 config.py                        # Configuration et constantes
├── 📄 requirements.txt                 # Dépendances Python
├── 📄 README.md                        # Documentation du projet
├── 📄 .gitignore                       # Fichiers à ignorer par Git
├── 📄 setup.py                         # Configuration du package
│
├── 📁 src/                             # Code source principal
│   ├── 📄 __init__.py                  # Init package
│   ├── 📄 calculator.py                # Calculs ROI et métriques
│   ├── 📄 converter.py                 # Conversions entre métriques
│   ├── 📄 simulator.py                 # Simulations de scénarios
│   ├── 📄 visualizer.py                # Graphiques et visualisations
│   └── 📄 utils.py                     # Fonctions utilitaires
│
├── 📁 tests/                           # Tests unitaires
│   ├── 📄 __init__.py
│   ├── 📄 test_calculator.py
│   ├── 📄 test_converter.py
│   ├── 📄 test_simulator.py
│   └── 📄 test_visualizer.py
│
├── 📁 data/                            # Données et exports
│   ├── 📄 .gitkeep
│   ├── 📁 exports/                     # Exports PDF/CSV
│   └── 📁 history/                     # Historique des calculs
│
├── 📁 assets/                          # Ressources (images, styles)
│   ├── 📄 styles.css                   # Styles personnalisés
│   └── 📁 images/                      # Images et icônes
│
└── 📁 docs/                            # Documentation
    ├── 📄 formulas.md                  # Documentation des formules
    └── 📄 user_guide.md                # Guide utilisateur
```

##  Organisation par Responsabilité

### **Core Business Logic** (`src/`)
- `calculator.py` : Tous les calculs métier (ROI, CPA, etc.)
- `converter.py` : Conversions entre métriques
- `simulator.py` : Simulations et analyses de scénarios
- `visualizer.py` : Génération de graphiques et rapports
- `utils.py` : Fonctions helpers (validation, formatage)

### **Tests** (`tests/`)
- Tests unitaires avec `pytest`
- Coverage > 80%
- Tests d'intégration

### **Interface** (`app.py`)
- Interface Streamlit moderne
- Multi-pages / onglets
- Responsive design

### **Configuration** (`config.py`)
- Constantes globales
- Formules
- Paramètres par défaut

## 📦 Prochaines Étapes

1. ✅ **Structure créée**
2. 🔄 **config.py** - Configuration et constantes
3. 🔄 **calculator.py** - Logique de calcul
4. 🔄 **converter.py** - Conversions
5. 🔄 **visualizer.py** - Graphiques
6. 🔄 **simulator.py** - Simulations
7. 🔄 **utils.py** - Utilitaires
8. 🔄 **Tests unitaires**
9. 🔄 **app.py** - Interface Streamlit
10. 🔄 **Documentation**

## 🎨 Design Principles

- **Clean Code** : PEP 8,type hints, docstrings
- **Modulaire** : Séparation des responsabilités
- **Testable** : Couverture de tests élevée
- **Maintenable** : Documentation complète
- **User-friendly** : Interface intuitive