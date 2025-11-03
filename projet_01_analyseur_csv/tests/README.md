#  Tests du Projet

Ce dossier contient tous les scripts de test pour l'Analyseur CSV.

---

##  Fichiers de Test

### test_rapports_corriges.py

**Description** : Script de test complet pour valider les corrections v2.1

**Objectif** :
- Vérifier la génération des rapports PDF, DOCX, HTML
- Valider que les tableaux ne sont pas coupés
- Confirmer l'absence d'emojis bizarres
- Tester les recommandations automatiques

**Utilisation** :
```bash
cd /chemin/vers/projet_01_analyseur_csv
python tests/test_rapports_corriges.py
```

**Résultats attendus** :
```
============================================================
TEST DES RAPPORTS CORRIGES
============================================================
✓ Données chargées : 36 lignes, 8 colonnes

1. Test génération PDF...
   ✓ PDF généré : outputs/reports/test_rapport_corrige.pdf
   
2. Test génération DOCX...
   ✓ DOCX généré : outputs/reports/test_rapport_corrige.docx
   
3. Test génération HTML...
   ✓ HTML généré : outputs/reports/test_rapport_corrige.html
   
4. Test recommandations...
   ✓ 4 recommandations générées
   
============================================================
TESTS TERMINES - 100% REUSSIS
============================================================
```

---

##  Tests à Effectuer

### Tests Automatiques
- [x] Génération PDF sans erreur
- [x] Génération DOCX sans erreur
- [x] Génération HTML sans erreur
- [x] Recommandations sans emojis
- [x] Nettoyage ASCII des colonnes

### Tests Manuels (Validation Visuelle)
- [ ] Ouvrir PDF → Vérifier tableaux complets
- [ ] Ouvrir DOCX → Vérifier largeurs colonnes
- [ ] Ouvrir HTML → Vérifier design moderne
- [ ] Vérifier absence de caractères bizarres (□, ?, �)

---

## Lancer les Tests

### Méthode 1 : Script Direct
```bash
python tests/test_rapports_corriges.py
```

### Méthode 2 : Avec l'environnement virtuel
```bash
source .venv/bin/activate
python tests/test_rapports_corriges.py
```

### Méthode 3 : Depuis le dossier racine
```bash
cd projet_01_analyseur_csv
python -m tests.test_rapports_corriges
```

---

##  Fichiers Générés

Les tests génèrent des fichiers dans `outputs/reports/` :

```
outputs/reports/
├── test_rapport_corrige.pdf      (4.4 KB)
├── test_rapport_corrige.docx    (37 KB)
└── test_rapport_corrige.html     (5.0 KB)
```

---

##  Critères de Réussite

### PDF
-  Fichier généré sans erreur
-  Tableaux avec largeurs adaptées (4in + 2.5in)
-  Pas d'emojis (texte ASCII)
-  Recommandations lisibles

### DOCX
-  Fichier généré sans erreur
-  Colonnes avec largeurs définies (3.5in + 2.5in)
-  Pas d'emojis dans les titres
-  Éditable dans Word

### HTML
-  Fichier généré sans erreur
-  Design moderne
-  Emojis conservés (supportés en HTML)
-  Responsive

---

##  En Cas d'Échec

### Erreur : Module non trouvé
```bash
# Installer les dépendances
pip install -r requirements.txt
```

### Erreur : Fichier de données manquant
```bash
# Vérifier la présence du fichier
ls data/exemple_ventes.csv
```

### Erreur : Permission denied
```bash
# Rendre le script exécutable
chmod +x tests/test_rapports_corriges.py
```

---

##  Ajouter de Nouveaux Tests

Pour créer un nouveau test :

1. Créer un fichier `test_nouvelle_fonctionnalite.py`
2. Suivre la structure :
```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_ma_fonctionnalite():
    """Description du test"""
    # Code du test
    assert resultat == attendu
    
if __name__ == "__main__":
    test_ma_fonctionnalite()
```

---

##  Tests Futurs Prévus

- [ ] Test de performance (grands datasets)
- [ ] Test d'intégration complète
- [ ] Test des graphiques Plotly
- [ ] Test de nettoyage de données
- [ ] Test de détection d'anomalies
- [ ] Test de l'interface Streamlit

---

**Dernière mise à jour** : 27 octobre 2025  
**Version** : 2.1
