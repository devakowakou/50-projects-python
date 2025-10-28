# 🚀 Installation Rapide - Analyseur CSV Professionnel

## ⏱️ Installation en 3 minutes

### Étape 1 : Cloner et Naviguer

```bash
cd /home/dev-akw/Documents/Coding/data/50-projects-python/projet_01_analyseur_csv
```

### Étape 2 : Installer les Dépendances

```bash
# Activer l'environnement virtuel
source ../.venv/bin/activate

# Installer toutes les dépendances
pip install -r requirements.txt
```

### Étape 3 : Lancer l'Application

```bash
# Méthode 1 : Script automatique
./run.sh

# Méthode 2 : Commande manuelle
streamlit run app.py
```

---

##  Dépendances Installées

### Core
-  streamlit==1.28.0
-  pandas==2.1.1
-  numpy==1.25.2
-  plotly==5.17.0
-  scipy==1.11.3

### Utilitaires
-  chardet==5.2.0 (détection encodage)
-  openpyxl==3.1.2 (Excel)

### Rapports Modernes
-  reportlab==4.4.4 (PDF)
-  python-docx==1.2.0 (Word)
-  python-pptx==1.0.2 (PowerPoint)
-  pillow==10.4.0 (Images)
-  kaleido==1.1.0 (Export graphiques)

---

##  Premier Test

### Charger le Fichier Exemple

1. Lancer l'application
2. Aller sur http://localhost:8501
3. Dans l'onglet "Aperçu", cliquer sur "Charger exemple"
4. Explorer les 7 onglets

### Générer un Rapport PDF

1. Naviguer vers l'onglet **"Rapports"**
2. Entrer le nom de votre entreprise
3. Cliquer sur **" Générer Rapport PDF"**
4. Télécharger le fichier généré

---

##  Résolution de Problèmes

### Erreur : Module chardet non trouvé
```bash
pip install chardet==5.2.0
```

### Erreur : Module reportlab non trouvé
```bash
pip install reportlab python-docx python-pptx pillow kaleido
```

### Port 8501 déjà utilisé
```bash
streamlit run app.py --server.port 8502
```

---

##  Formats Supportés

### Import
-  CSV (tous encodages)
-  Excel (.xlsx, .xls)

### Export
-  CSV
-  JSON
-  Excel
-  PDF ⭐ NOUVEAU
-  DOCX ⭐ NOUVEAU
-  HTML ⭐ NOUVEAU

---

##  Checklist Post-Installation

- [ ] Application se lance sans erreur
- [ ] Fichier exemple se charge
- [ ] Statistiques s'affichent
- [ ] Graphiques s'affichent
- [ ] Export PDF fonctionne
- [ ] Export DOCX fonctionne
- [ ] Export HTML fonctionne

---

##  Documentation Complète

- 📖 [README.md](README.md) - Vue d'ensemble
- 🔧 [DOCUMENTATION_TECHNIQUE.md](DOCUMENTATION_TECHNIQUE.md) - Architecture
-  [PROGRESSION.md](PROGRESSION.md) - Historique du projet
- ✨ [AMELIORATIONS.md](AMELIORATIONS.md) - Nouvelles fonctionnalités

---

**🚀 Vous êtes prêt ! Bon analyse !**
