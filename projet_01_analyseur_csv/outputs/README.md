# Dossier de Sortie

Ce dossier contient tous les fichiers générés par l'application.

---

## 📂 Structure

```
outputs/
├── reports/          # Rapports générés (PDF, DOCX, HTML)
│   ├── .gitkeep
│   └── (fichiers générés)
│
└── exports/          # Exports de données (CSV, JSON, Excel)
    ├── .gitkeep
    └── (fichiers générés)
```

---

##  reports/

### Description
Contient tous les rapports professionnels générés par l'application.

### Types de Fichiers
- **PDF** : Rapports professionnels pour clients/management
- **DOCX** : Documents Word éditables pour collaboration
- **HTML** : Pages web interactives pour partage web

### Exemple de Noms
```
rapport_analyse_2025-10-27_14-30-15.pdf
rapport_analyse_2025-10-27_14-30-15.docx
rapport_analyse_2025-10-27_14-30-15.html
test_rapport_corrige.pdf
```

### Taille Typique
- PDF : 4-20 KB
- DOCX : 20-50 KB
- HTML : 5-15 KB

---

##  exports/

### Description
Contient les exports de données dans différents formats.

### Types de Fichiers
- **CSV** : Données nettoyées ou transformées
- **JSON** : Statistiques et métadonnées
- **Excel** : Données avec formatage

### Exemple de Noms
```
donnees_nettoyees_2025-10-27_14-30-15.csv
statistiques_2025-10-27_14-30-15.json
export_analyse_2025-10-27_14-30-15.xlsx
```

### Taille Typique
- CSV : Variable selon le dataset
- JSON : 1-10 KB
- Excel : Variable selon le dataset

---

## 🔒 Gestion des Fichiers

### Nettoyage Automatique
Les fichiers générés sont **temporaires** et peuvent être supprimés sans risque.

### Commandes de Nettoyage

#### Supprimer tous les rapports
```bash
rm -f outputs/reports/*
# Garder .gitkeep
```

#### Supprimer tous les exports
```bash
rm -f outputs/exports/*
# Garder .gitkeep
```

#### Nettoyage complet
```bash
rm -f outputs/reports/* outputs/exports/*
# ou
make clean  # si Makefile disponible
```

---

##  Bonnes Pratiques

### Nommage des Fichiers
- Utiliser des timestamps : `rapport_2025-10-27_14-30-15.pdf`
- Éviter les espaces : utiliser `_` ou `-`
- Être descriptif : `analyse_ventes_Q4.pdf`

### Organisation
- Archiver les rapports importants ailleurs
- Nettoyer régulièrement les fichiers de test
- Sauvegarder les exports critiques

### Git
- Les fichiers générés sont **ignorés** par Git (.gitignore)
- Seuls les `.gitkeep` sont versionnés
- Ne pas commiter les rapports/exports

---

## Génération de Fichiers

### Via Streamlit
1. Lancer l'application
2. Charger des données
3. Onglet "Rapports" → Générer PDF/DOCX/HTML
4. Fichiers sauvegardés dans `outputs/reports/`

### Via Python
```python
from src.modern_report_generator import ModernReportGenerator

gen = ModernReportGenerator(df)
gen.generate_pdf_report(
    filepath="outputs/reports/mon_rapport.pdf"
)
```

---

##  Statistiques d'Utilisation

### Espace Disque
- Chaque rapport : ~50 KB max
- 100 rapports : ~5 MB
- Nettoyer si > 100 MB

### Performances
- Génération PDF : 1-2 secondes
- Génération DOCX : 0.5-1 seconde
- Génération HTML : 0.3 seconde

---

##  Important

### Ne Pas Commiter
-  Rapports générés
-  Exports de données
-  Fichiers temporaires
-  Seulement .gitkeep

### Sécurité
- Ne pas partager de données sensibles
- Vérifier le contenu avant distribution
- Respecter la confidentialité des données

---

## 🔧 Dépannage

### Le dossier n'existe pas
```bash
mkdir -p outputs/reports outputs/exports
touch outputs/reports/.gitkeep outputs/exports/.gitkeep
```

### Permission denied
```bash
chmod 755 outputs outputs/reports outputs/exports
```

### Espace disque plein
```bash
# Vérifier l'espace
du -sh outputs/

# Nettoyer
rm -f outputs/reports/* outputs/exports/*
```

---

**Note** : Ce dossier est créé automatiquement à l'installation si nécessaire.

**Dernière mise à jour** : 27 octobre 2025
