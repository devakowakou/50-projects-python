from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.database import init_db
from backend.routes import logs_routes, stats_routes, analytics_routes

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Création de l'application
app = FastAPI(
    title="Server Log Dashboard API",
    description="API pour analyser et visualiser les logs serveur",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Événement de démarrage
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Démarrage de l'API...")
    init_db()
    logger.info("✅ Base de données prête")

# Inclusion des routes
app.include_router(logs_routes.router)
app.include_router(stats_routes.router)
app.include_router(analytics_routes.router)

# Route de santé
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "log-dashboard-api",
        "version": "1.0.0"
    }

@app.get("/")
def root():
    return {
        "message": "Server Log Dashboard API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
