# 📊 Projet 14 : Analyse d'Audiences Instagram & TikTok

**Status**: 🚧 EN COURS | **Date début**: 29 oct 2025

Application complète d'analyse et visualisation des performances de comptes Instagram et TikTok avec dashboard interactif.

## 🎯 Objectif

Analyser et visualiser les performances de comptes Instagram et TikTok :
- Evolution des followers
- Reach et impressions  
- Taux d'engagement global et par post
- Meilleurs contenus et formats
- Meilleures heures de publication
- Recommandations automatisées

## 🔧 Stack Technique

| Composant | Technologie |
|-----------|-------------|
| **Backend** | Python + FastAPI |
| **Frontend/Dashboard** | Python + Dash/Plotly |
| **Authentification** | OAuth2 (Meta/TikTok) |
| **Base de données** | PostgreSQL/SQLite |
| **APIs** | Instagram Graph API, TikTok Business API |
| **Tâches automatiques** | APScheduler |
| **Visualisations** | Dash Core Components, Plotly Charts |

## 📊 Données Collectées

### Instagram
- Followers, Reach, Impressions
- Likes, commentaires, partages, sauvegardes
- Engagement par post, top posts
- Reels : vues et engagement

### TikTok  
- Followers, vues par vidéo
- Likes, commentaires, partages
- Watch time, completion rate
- Audience insights, top vidéos

## 📐 Métriques Calculées

### Taux d'engagement par post
```
ER = (likes + comments + shares + saves) / followers × 100
```

### Taux d'engagement global
```
ER_global = total_interactions / total_followers × 100
```

### Reach rate
```
Reach_rate = reach / followers × 100
```

### Croissance audience
```
Growth = (followers_today - followers_yesterday) / followers_yesterday × 100
```

## 🏗️ Architecture

```
projet_14_social_analytics/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # Endpoints API
│   │   ├── auth/              # OAuth2 Instagram/TikTok
│   │   ├── models/            # Modèles de données
│   │   ├── services/          # Logique métier
│   │   └── database/          # Configuration DB
│   ├── main.py                # Point d'entrée FastAPI
│   └── requirements.txt
│
├── frontend/                   # Dash Dashboard
│   ├── components/            # Composants Dash
│   ├── layouts/               # Layouts des pages
│   ├── callbacks/             # Callbacks interactifs
│   └── app.py                 # Application Dash
│
├── shared/                     # Code partagé
│   ├── config.py              # Configuration
│   ├── database.py            # Modèles DB
│   └── utils.py               # Utilitaires
│
├── scripts/                    # Scripts automatiques
│   ├── fetch_instagram.py     # Collecte données IG
│   ├── fetch_tiktok.py        # Collecte données TikTok
│   └── scheduler.py           # Planificateur
│
├── tests/                      # Tests unitaires
├── docs/                       # Documentation
├── requirements.txt            # Dépendances globales
└── README.md                   # Ce fichier
```

## 🚀 Fonctionnalités

### ✅ Niveau Basique
- [ ] Connexion compte Instagram/TikTok
- [ ] Dashboard followers, likes, vues
- [ ] Engagement par post

### 🔄 Niveau Intermédiaire  
- [ ] Top posts/vidéos
- [ ] Meilleures heures pour publier
- [ ] Croissance & reach par période

### 🎯 Niveau Avancé
- [ ] Recommandations de contenu
- [ ] Analyse du format le plus performant
- [ ] Prévision de performance (ML)
- [ ] Export PDF/CSV des rapports

## 📍 Roadmap

### Phase 1: Setup & Auth (Semaine 1)
- [x] Structure du projet
- [ ] Configuration FastAPI
- [ ] OAuth2 Instagram & TikTok
- [ ] Base de données SQLite

### Phase 2: Backend API (Semaine 2)
- [ ] Endpoints de collecte de données
- [ ] Modèles de données
- [ ] Scripts de fetch automatique
- [ ] Calcul des métriques

### Phase 3: Frontend Dashboard (Semaine 3)
- [ ] Layout Dash principal
- [ ] Graphiques Plotly interactifs
- [ ] Filtres et contrôles
- [ ] Tables de données

### Phase 4: Analyses Avancées (Semaine 4)
- [ ] Recommandations automatiques
- [ ] Export de rapports
- [ ] Optimisations et tests
- [ ] Documentation finale

## 🔑 Configuration Requise

### APIs Nécessaires
1. **Meta for Developers** (Instagram)
   - Créer une app Facebook
   - Activer Instagram Graph API
   - Obtenir les tokens d'accès

2. **TikTok for Business** 
   - Créer une app TikTok Business
   - Activer Marketing API
   - Configuration OAuth2

### Variables d'Environnement
```bash
# Instagram
INSTAGRAM_APP_ID=your_app_id
INSTAGRAM_APP_SECRET=your_app_secret
INSTAGRAM_REDIRECT_URI=http://localhost:8000/auth/instagram/callback

# TikTok
TIKTOK_CLIENT_KEY=your_client_key
TIKTOK_CLIENT_SECRET=your_client_secret
TIKTOK_REDIRECT_URI=http://localhost:8000/auth/tiktok/callback

# Database
DATABASE_URL=sqlite:///./social_analytics.db

# App
SECRET_KEY=your_secret_key
```

## 🚀 Installation & Lancement

### 1. Cloner et installer
```bash
cd projet_14_social_analytics
pip install -r requirements.txt
```

### 2. Configuration
```bash
cp .env.example .env
# Éditer .env avec vos clés API
```

### 3. Lancer le backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 4. Lancer le dashboard
```bash
cd frontend  
python app.py
```

### 5. Accéder à l'application
- **API Documentation**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8050

## 📈 Métriques de Succès

- [ ] Connexion réussie aux 2 plateformes
- [ ] Collecte automatique quotidienne
- [ ] Dashboard responsive et interactif
- [ ] Calculs de métriques précis
- [ ] Export de rapports fonctionnel

## 🎯 Objectifs d'Apprentissage

### Techniques
- [ ] Maîtriser FastAPI et Dash
- [ ] OAuth2 avec APIs sociales
- [ ] Architecture backend/frontend séparée
- [ ] Planification de tâches automatiques

### Data Science
- [ ] Métriques d'engagement social media
- [ ] Analyse de performance de contenu
- [ ] Visualisations interactives avancées
- [ ] Recommandations basées sur les données

## 📚 Ressources

### Documentation APIs
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/)
- [TikTok Marketing API](https://business-api.tiktok.com/portal/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Dash Documentation](https://dash.plotly.com/)

### Guides OAuth2
- [Meta OAuth Flow](https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow)
- [TikTok OAuth Guide](https://developers.tiktok.com/doc/login-kit-web)

---

## 📊 Progression

**Phase actuelle**: Setup & Architecture ✅  
**Prochaine étape**: Configuration FastAPI et OAuth2  
**Avancement global**: 5%

---

*Projet créé le 29 octobre 2025 dans le cadre du Challenge 50 Projets Python*