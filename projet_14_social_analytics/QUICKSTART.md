# 🚀 Quick Start - Social Analytics

## 📦 Installation Rapide

```bash
# 1. Aller dans le projet
cd projet_14_social_analytics

# 2. Installer les dépendances
pip3 install -r requirements.txt

# 3. Tester le setup
python3 test_setup.py

# 4. Générer des données de démo
python3 scripts/demo_data.py
```

## 🏃‍♂️ Lancement

### Terminal 1 - Backend API
```bash
cd backend
python3 main.py
```
**➡️ API disponible sur:** http://localhost:8000/docs

### Terminal 2 - Dashboard
```bash
cd frontend  
python3 app.py
```
**➡️ Dashboard disponible sur:** http://localhost:8050

## 🎯 Fonctionnalités Disponibles

### ✅ **Implémenté**
- **Backend FastAPI** avec endpoints d'analyse
- **Dashboard Dash** avec 7 graphiques interactifs
- **OAuth2** Instagram & TikTok (structure prête)
- **Base de données** SQLAlchemy avec modèles complets
- **Données de démo** (30 jours d'insights + posts)

### 📊 **Graphiques Dashboard**
1. **Métriques principales** (followers, engagement, reach)
2. **Évolution followers** dans le temps
3. **Engagement quotidien** par plateforme
4. **Indicateur de croissance** (gauge)
5. **Meilleures heures** de publication
6. **Top posts** par engagement
7. **Performance par type** de contenu
8. **Comparaison plateformes** Instagram vs TikTok

### 🔗 **Endpoints API**
- `GET /analytics/metrics` - Métriques principales
- `GET /analytics/followers-evolution` - Évolution followers
- `GET /analytics/engagement-analysis` - Analyse engagement
- `GET /analytics/top-posts` - Meilleurs posts
- `GET /analytics/best-times` - Meilleures heures
- `GET /analytics/content-performance` - Performance contenu
- `GET /auth/status` - Statut connexion
- `GET /auth/instagram/login` - Connexion Instagram
- `GET /auth/tiktok/login` - Connexion TikTok

## 🔧 Configuration APIs (Optionnel)

Pour connecter de vraies données Instagram/TikTok :

### 1. Instagram (Meta for Developers)
```bash
# .env
INSTAGRAM_APP_ID=your_app_id
INSTAGRAM_APP_SECRET=your_app_secret
```

### 2. TikTok (TikTok for Business)  
```bash
# .env
TIKTOK_CLIENT_KEY=your_client_key
TIKTOK_CLIENT_SECRET=your_client_secret
```

## 🎮 Test Rapide

1. **Lancer le test**: `python3 test_setup.py`
2. **Générer données**: `python3 scripts/demo_data.py`  
3. **Démarrer backend**: `cd backend && python3 main.py`
4. **Démarrer dashboard**: `cd frontend && python3 app.py`
5. **Ouvrir**: http://localhost:8050

## 📈 Résultat Attendu

Le dashboard affiche :
- **15,420 followers** avec croissance +2.3%
- **Graphiques interactifs** avec données des 30 derniers jours
- **Top 5 posts** avec engagement détaillé
- **Recommandations automatiques** basées sur les performances
- **Filtres** par plateforme (Instagram/TikTok/Toutes)

---

**🎯 Projet fonctionnel en 5 minutes !**