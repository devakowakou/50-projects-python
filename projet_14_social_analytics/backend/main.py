"""Point d'entrée principal de l'API FastAPI."""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.database import create_tables, get_db
from shared.config import settings
from backend.app.api import auth, analytics

# Créer les tables au démarrage
create_tables()

# Initialiser FastAPI
app = FastAPI(
    title="Social Analytics API",
    description="API pour l'analyse d'audiences Instagram & TikTok",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8050"],  # Dashboard Dash
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ajouter les routers
app.include_router(auth.router)
app.include_router(analytics.router)


@app.get("/")
async def root():
    """Endpoint racine."""
    return {
        "message": "Social Analytics API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Vérification de santé de l'API."""
    try:
        # Test de connexion à la DB
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2025-10-29T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "database": "disconnected",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )