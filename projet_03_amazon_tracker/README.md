# 🛒 Amazon Price Tracker

Suivez l'évolution des prix de vos produits Amazon favoris et recevez des alertes lorsqu'ils atteignent votre prix cible.

## 📋 Description

Amazon Price Tracker est une application web interactive qui permet de :
- 🔍 Surveiller les prix de produits Amazon
- 📊 Visualiser l'historique des prix
- 🔔 Recevoir des alertes email quand le prix atteint votre cible
- 📈 Analyser les tendances et obtenir des recommandations d'achat

## ✨ Fonctionnalités MVP

### 1. Ajout de produits
- Ajoutez des produits via leur URL Amazon
- Définissez un prix cible personnalisé
- Prévisualisation instantanée (nom, prix, image)

### 2. Suivi des prix
- Liste complète de vos produits suivis
- Rafraîchissement manuel des prix
- Alertes visuelles pour les produits en dessous du prix cible

### 3. Historique et analyse
- Graphique d'évolution des prix sur 30 jours
- Statistiques détaillées (min, max, moyenne)
- Indicateur de tendance (hausse/baisse/stable)
- Recommandations d'achat intelligentes

### 4. Notifications
- Alertes par email (SMTP)
- Template HTML professionnel
- Envoi automatique lors du refresh des prix

## 🛠️ Technologies

- **Python 3.9+**
- **Streamlit** - Interface web
- **BeautifulSoup4** - Web scraping
- **SQLite** - Base de données
- **Pandas** - Manipulation de données
- **Plotly** - Visualisations interactives
- **SMTP** - Notifications email

## 📦 Installation

### 1. Cloner le projet
```bash
cd projet_03_amazon_tracker
```

### 2. Créer un environnement virtuel (si pas déjà fait)
```bash
python3 -m venv ../.venv
source ../.venv/bin/activate  # Linux/Mac
# ou
..\.venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration email
Créez un fichier `.env` à partir de `.env.example` :
```bash
cp .env.example .env
```

Éditez `.env` et configurez vos paramètres email :
```env
SMTP_EMAIL=votre.email@gmail.com
SMTP_PASSWORD=votre_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
AMAZON_DOMAIN=amazon.fr
```

**⚠️ Important pour Gmail :**
- Vous devez générer un "App Password" (pas votre mot de passe normal)
- Allez dans : Compte Google → Sécurité → Validation en deux étapes → Mots de passe des applications

## 🚀 Utilisation

### Lancer l'application
```bash
bash run.sh
# ou directement
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

### Workflow typique

1. **Ajouter un produit**
   - Copiez l'URL d'un produit Amazon
   - Définissez votre prix cible
   - Cliquez sur "Ajouter au suivi"

2. **Suivre les prix**
   - Consultez la liste de vos produits
   - Cliquez sur "Rafraîchir tous les prix"
   - Les produits sous le prix cible apparaissent en vert

3. **Analyser l'historique**
   - Sélectionnez un produit
   - Visualisez le graphique d'évolution
   - Consultez les recommandations d'achat

4. **Recevoir les alertes**
   - Configurez votre email dans `.env`
   - Les alertes sont envoyées automatiquement lors du refresh

## 📁 Structure du Projet

```
projet_03_amazon_tracker/
├── app.py                      # Application Streamlit
├── config.py                   # Configuration
├── requirements.txt            # Dépendances
├── run.sh                      # Script de lancement
├── .env                        # Variables d'environnement (à créer)
├── .env.example                # Template de configuration
├── .gitignore
│
├── data/
│   └── tracker.db              # Base SQLite (créée auto)
│
├── src/
│   ├── __init__.py
│   ├── database.py             # Gestion SQLite
│   ├── scraper.py              # Scraping Amazon
│   ├── analyzer.py             # Analyse des prix
│   ├── visualizer.py           # Graphiques Plotly
│   └── notifier.py             # Alertes email
│
└── assets/
    └── style.css               # Styles personnalisés
```

## ⚙️ Configuration

### Paramètres dans `config.py`

- **AMAZON_DOMAIN** : `amazon.fr` ou `amazon.com`
- **MAX_PRODUCTS** : Limite de produits (défaut: 20)
- **REQUEST_DELAY** : Délai entre requêtes (défaut: 2s)
- **DEFAULT_HISTORY_DAYS** : Historique par défaut (défaut: 30j)

### Sélecteurs CSS personnalisables

Si Amazon change sa structure HTML, vous pouvez ajuster les sélecteurs dans `config.py` :
- `PRICE_SELECTORS`
- `NAME_SELECTORS`
- `IMAGE_SELECTORS`

## 🔒 Sécurité & Bonnes Pratiques

- ✅ Fichier `.env` dans `.gitignore` (ne jamais commit les credentials)
- ✅ User-Agent aléatoire pour éviter la détection de bot
- ✅ Délai entre requêtes (2-3 secondes)
- ✅ Limite de produits pour éviter le scraping intensif
- ✅ Retry logic en cas d'erreur réseau

## 🚨 Limitations MVP

- Scraping **manuel** uniquement (bouton à cliquer)
- Pas de scraping automatique en arrière-plan
- Email envoyé uniquement lors du refresh manuel
- Maximum 20 produits suivis
- Historique limité à 30 jours
- Support Amazon.fr uniquement (facilement extensible)

## 🔄 Évolutions Futures (Version Complète)

- [ ] Scraping automatique avec scheduler (APScheduler)
- [ ] Support multi-sites (eBay, Cdiscount)
- [ ] Notifications Telegram/Discord
- [ ] Authentification multi-utilisateurs
- [ ] Prédictions ML pour meilleur moment d'achat
- [ ] Export PDF des rapports
- [ ] Déploiement cloud (Streamlit Cloud)
- [ ] API REST
- [ ] Intégration CamelCamelCamel/Keepa

## 🐛 Résolution de Problèmes

### Le scraping ne fonctionne pas
- Vérifiez que l'URL est bien une URL Amazon valide
- Amazon peut bloquer temporairement → attendez quelques minutes
- Essayez avec un autre produit

### Les emails ne partent pas
- Vérifiez la configuration `.env`
- Pour Gmail, utilisez un "App Password", pas votre mot de passe
- Testez la connexion SMTP

### Erreurs de parsing
- Amazon change régulièrement sa structure HTML
- Ajustez les sélecteurs CSS dans `config.py`
- Ouvrez une issue GitHub si le problème persiste

## 📝 Notes

- **Respect du robots.txt** : Ce projet est à usage personnel/éducatif
- **Rate limiting** : Évitez de scraper trop fréquemment
- **Terms of Service** : Respectez les CGU d'Amazon

## 📄 Licence

MIT License - Projet éducatif dans le cadre du challenge "50 Projects Python"

## 👨‍💻 Auteur

Projet réalisé dans le cadre du challenge **50 projets Python en 25 jours**

---

**⭐ Si ce projet vous est utile, n'hésitez pas à le star !**
