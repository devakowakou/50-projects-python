# 🚀 Guide de Configuration - Social Analytics

## 📋 Prérequis

### Système
- Python 3.8+
- pip ou conda
- Git

### Comptes Développeur Requis
1. **Meta for Developers** (Instagram)
2. **TikTok for Business** (TikTok)

---

## 🔧 Installation

### 1. Cloner le projet
```bash
git clone <your-repo-url>
cd 50-projects-python/projet_14_social_analytics
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration
```bash
cp .env.example .env
# Éditer .env avec vos clés API
```

---

## 🔑 Configuration des APIs

### Instagram (Meta for Developers)

#### 1. Créer une App Facebook
1. Aller sur [developers.facebook.com](https://developers.facebook.com)
2. Créer une nouvelle app → "Consumer"
3. Ajouter le produit "Instagram Graph API"

#### 2. Configuration OAuth2
```
App ID: Votre App ID Facebook
App Secret: Votre App Secret Facebook
Redirect URI: http://localhost:8000/auth/instagram/callback
```

#### 3. Permissions requises
- `instagram_basic`
- `instagram_content_publish`
- `pages_show_list`
- `pages_read_engagement`

#### 4. Variables d'environnement
```bash
INSTAGRAM_APP_ID=your_app_id
INSTAGRAM_APP_SECRET=your_app_secret
INSTAGRAM_REDIRECT_URI=http://localhost:8000/auth/instagram/callback
```

### TikTok (TikTok for Business)

#### 1. Créer une App TikTok
1. Aller sur [developers.tiktok.com](https://developers.tiktok.com)
2. Créer une nouvelle app
3. Activer "Marketing API"

#### 2. Configuration OAuth2
```
Client Key: Votre Client Key TikTok
Client Secret: Votre Client Secret TikTok
Redirect URI: http://localhost:8000/auth/tiktok/callback
```

#### 3. Scopes requis
- `user.info.basic`
- `video.list`
- `video.insights`

#### 4. Variables d'environnement
```bash
TIKTOK_CLIENT_KEY=your_client_key
TIKTOK_CLIENT_SECRET=your_client_secret
TIKTOK_REDIRECT_URI=http://localhost:8000/auth/tiktok/callback
```

---

## 🗄️ Base de Données

### SQLite (Développement)
```bash
# La DB sera créée automatiquement
DATABASE_URL=sqlite:///./social_analytics.db
```

### PostgreSQL (Production)
```bash
# Installer PostgreSQL
sudo apt install postgresql postgresql-contrib  # Ubuntu
brew install postgresql                         # macOS

# Créer la base
createdb social_analytics

# Configuration
DATABASE_URL=postgresql://user:password@localhost/social_analytics
```

---

## 🚀 Lancement

### Mode Développement

#### 1. Générer des données de démo
```bash
python scripts/demo_data.py
```

#### 2. Lancer le backend (Terminal 1)
```bash
cd backend
uvicorn main:app --reload --port 8000
```

#### 3. Lancer le dashboard (Terminal 2)
```bash
cd frontend
python app.py
```

#### 4. Accéder aux applications
- **API Documentation**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8050

### Mode Production

#### 1. Configuration
```bash
# .env
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@localhost/social_analytics
```

#### 2. Lancement avec Gunicorn
```bash
# Backend
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Dashboard
gunicorn frontend.app:server -w 2 --bind 0.0.0.0:8050
```

---

## 🧪 Tests

### Lancer les tests
```bash
pytest tests/ -v
```

### Tests de couverture
```bash
pytest --cov=backend --cov=frontend tests/
```

---

## 🔍 Vérification

### 1. Santé de l'API
```bash
curl http://localhost:8000/health
```

### 2. Endpoints disponibles
```bash
curl http://localhost:8000/docs
```

### 3. Dashboard accessible
Ouvrir http://localhost:8050 dans le navigateur

---

## 🐛 Dépannage

### Erreurs communes

#### "Module not found"
```bash
# Vérifier l'environnement virtuel
which python
pip list

# Réinstaller les dépendances
pip install -r requirements.txt
```

#### "Database connection failed"
```bash
# Vérifier la DB
python -c "from shared.database import engine; print(engine.url)"

# Recréer les tables
python -c "from shared.database import create_tables; create_tables()"
```

#### "OAuth2 redirect mismatch"
```bash
# Vérifier les URLs dans .env
echo $INSTAGRAM_REDIRECT_URI
echo $TIKTOK_REDIRECT_URI

# Vérifier la configuration des apps
```

### Logs de débogage

#### Backend
```bash
# Logs détaillés
uvicorn main:app --log-level debug
```

#### Frontend
```bash
# Mode debug Dash
python app.py --debug
```

---

## 📚 Ressources

### Documentation APIs
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/)
- [TikTok Marketing API](https://business-api.tiktok.com/portal/docs)

### Frameworks
- [FastAPI](https://fastapi.tiangolo.com/)
- [Dash](https://dash.plotly.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)

### OAuth2
- [Meta OAuth](https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow)
- [TikTok OAuth](https://developers.tiktok.com/doc/login-kit-web)

---

## 🆘 Support

### Issues communes
1. **Tokens expirés**: Réimplémenter le refresh automatique
2. **Rate limiting**: Implémenter un système de queue
3. **Données manquantes**: Vérifier les permissions des apps

### Contact
- GitHub Issues: [Lien vers issues]
- Documentation: [Lien vers docs]

---

*Guide créé le 29 octobre 2025*