from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from database import init_db
from routes import logs_routes, stats_routes, analytics_routes

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Server Log Dashboard API",
    description="API pour analyser et visualiser les logs serveur",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Démarrage de l'API...")
    init_db()
    logger.info("✅ Base de données prête")

app.include_router(logs_routes.router)
app.include_router(stats_routes.router)
app.include_router(analytics_routes.router)

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
