# 📊 ROI Marketing Calculator

> Calculez votre retour sur investissement et convertissez vos métriques marketing en quelques clics

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](tests/)

## 🎯 Fonctionnalités

### ✅ MVP (Version de Base)
- **Calculateur de ROI** : Calcul automatique du retour sur investissement
- **Convertisseur de métriques** : Conversion entre CPC, CPM, CPA, CTR
- **Seuil de rentabilité** : Détermination du point d'équilibre
- **Interface intuitive** : Dashboard Streamlit moderne et responsive

### 🚀 Fonctionnalités Avancées
- **Simulateur de scénarios** : Testez différentes hypothèses
- **Visualisations interactives** : Graphiques dynamiques avec Plotly
- **Export de rapports** : PDF et CSV
- **Historique des calculs** : Sauvegarde de vos simulations
- **Benchmarks sectoriels** : Comparez-vous aux standards du marché

## 📦 Installation

### Prérequis
- Python 3.10 ou supérieur
- pip

### Installation rapide

```bash
# Cloner le repository
git clone https://github.com/votre-username/roi-marketing-calculator.git
cd roi-marketing-calculator

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur macOS/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## 🚀 Utilisation

### Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

### Utilisation comme bibliothèque Python

```python
from src.calculator import ROICalculator
from src.converter import MetricConverter

# Calculer le ROI
calc = ROICalculator()
roi = calc.calculate_roi(revenue=15000, cost=10000)
print(f"ROI: {roi}%")  # ROI: 50.0%

# Convertir CPC en CPM
converter = MetricConverter()
cpm = converter.cpc_to_cpm(cpc=2.50, ctr=2.0)
print(f"CPM: ${cpm:.2f}")  # CPM: $50.00
```

## 📖 Documentation des Métriques

### ROI (Return on Investment)
```
ROI = (Revenu - Coût) / Coût × 100
```
Mesure la rentabilité d'un investissement en pourcentage.

### ROAS (Return on Ad Spend)
```
ROAS = Revenu / Coût
```
Indique combien de revenus vous générez pour chaque euro dépensé.

### CPC (Cost Per Click)
```
CPC = Coût Total / Nombre de Clics
```
Coût moyen par clic sur vos annonces.

### CPM (Cost Per Mille)
```
CPM = (Coût Total / Impressions) × 1000
```
Coût pour 1000 impressions de votre annonce.

### CPA (Cost Per Acquisition)
```
CPA = Coût Total / Conversions
```
Coût pour acquérir un nouveau client.

### CTR (Click Through Rate)
```
CTR = (Clics / Impressions) × 100
```
Pourcentage de personnes qui cliquent après avoir vu votre annonce.

## 🧪 Tests

### Lancer les tests

```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=src --cov-report=html

# Tests spécifiques
pytest tests/test_calculator.py
```

### Structure des tests

```
tests/
├── test_calculator.py      # Tests des calculs
├── test_converter.py       # Tests des conversions
├── test_simulator.py       # Tests des simulations
└── test_visualizer.py      # Tests des visualisations
```

## 📁 Structure du Projet

```
roi-marketing-calculator/
├── app.py                  # Application Streamlit
├── config.py               # Configuration
├── requirements.txt        # Dépendances
├── src/
│   ├── calculator.py       # Logique de calcul
│   ├── converter.py        # Conversions
│   ├── simulator.py        # Simulations
│   ├── visualizer.py       # Graphiques
│   └── utils.py            # Utilitaires
├── tests/                  # Tests unitaires
├── data/                   # Données et exports
└── docs/                   # Documentation
```

## 🎨 Captures d'écran

### Dashboard Principal
![Dashboard](docs/images/dashboard.png)

### Simulateur de Scénarios
![Simulator](docs/images/simulator.png)

### Rapport d'Export
![Report](docs/images/report.png)

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment participer :

1. Forkez le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add: amazing feature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Standards de code

- Suivre PEP 8
- Ajouter des docstrings
- Écrire des tests unitaires
- Maintenir la couverture > 80%

## 📝 Roadmap

- [ ] Intégration avec Google Ads API
- [ ] Intégration avec Meta Ads API
- [ ] Calcul de LTV (Lifetime Value)
- [ ] Analyse de cohortes
- [ ] Modèles prédictifs ML
- [ ] Mode multi-campagnes
- [ ] Dashboard temps réel

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Auteurs

- **Votre Nom** - *Développeur principal* - [@votre-github](https://github.com/votre-username)

## 🙏 Remerciements

- Streamlit pour le framework d'interface
- Plotly pour les visualisations
- La communauté Python

## 📞 Support

- 📧 Email: support@exemple.com
- 💬 Discord: [Serveur Discord](https://discord.gg/exemple)
- 🐦 Twitter: [@votre_compte](https://twitter.com/votre_compte)

---

⭐ **Si ce projet vous aide, n'hésitez pas à mettre une étoile !** ⭐