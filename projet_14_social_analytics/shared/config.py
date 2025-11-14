"""Configuration globale du projet."""

import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application."""
    
    # App
    SECRET_KEY: str = "your-secret-key-change-in-production"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./social_analytics.db"
    
    # Instagram API
    INSTAGRAM_APP_ID: Optional[str] = None
    INSTAGRAM_APP_SECRET: Optional[str] = None
    INSTAGRAM_REDIRECT_URI: str = "http://localhost:8000/auth/instagram/callback"
    
    # TikTok API
    TIKTOK_CLIENT_KEY: Optional[str] = None
    TIKTOK_CLIENT_SECRET: Optional[str] = None
    TIKTOK_REDIRECT_URI: str = "http://localhost:8000/auth/tiktok/callback"
    
    # FastAPI
    API_HOST: str = "localhost"
    API_PORT: int = 8000
    
    # Dash
    DASH_HOST: str = "localhost"
    DASH_PORT: int = 8050
    
    # Scheduler
    FETCH_INTERVAL_HOURS: int = 24
    
    class Config:
        env_file = ".env"


# Instance globale des settings
settings = Settings()


# URLs des APIs
INSTAGRAM_API_BASE = "https://graph.instagram.com"
TIKTOK_API_BASE = "https://business-api.tiktok.com"

# Scopes OAuth2
INSTAGRAM_SCOPES = [
    "instagram_basic",
    "instagram_content_publish", 
    "pages_show_list",
    "pages_read_engagement"
]

TIKTOK_SCOPES = [
    "user.info.basic",
    "video.list",
    "video.insights"
]