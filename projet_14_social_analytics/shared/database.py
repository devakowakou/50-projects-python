"""Modèles de base de données SQLAlchemy."""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .config import settings

# Configuration de la base de données
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    """Utilisateur de l'application."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    social_accounts = relationship("SocialAccount", back_populates="user")


class SocialAccount(Base):
    """Compte social media lié à un utilisateur."""
    __tablename__ = "social_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    platform = Column(String)  # "instagram" ou "tiktok"
    account_id = Column(String)  # ID du compte sur la plateforme
    username = Column(String)
    access_token = Column(Text)
    refresh_token = Column(Text, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="social_accounts")
    insights = relationship("SocialInsight", back_populates="account")
    posts = relationship("Post", back_populates="account")


class SocialInsight(Base):
    """Métriques d'audience pour un compte social."""
    __tablename__ = "social_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("social_accounts.id"))
    date = Column(DateTime)
    
    # Métriques communes
    followers_count = Column(Integer)
    following_count = Column(Integer, nullable=True)
    posts_count = Column(Integer, nullable=True)
    
    # Métriques Instagram
    reach = Column(Integer, nullable=True)
    impressions = Column(Integer, nullable=True)
    profile_views = Column(Integer, nullable=True)
    website_clicks = Column(Integer, nullable=True)
    
    # Métriques TikTok
    video_views = Column(Integer, nullable=True)
    likes_count = Column(Integer, nullable=True)
    comments_count = Column(Integer, nullable=True)
    shares_count = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    account = relationship("SocialAccount", back_populates="insights")


class Post(Base):
    """Post/Vidéo sur les réseaux sociaux."""
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("social_accounts.id"))
    platform_post_id = Column(String)  # ID du post sur la plateforme
    
    # Informations du post
    caption = Column(Text, nullable=True)
    media_type = Column(String)  # "IMAGE", "VIDEO", "CAROUSEL_ALBUM"
    media_url = Column(String, nullable=True)
    permalink = Column(String, nullable=True)
    timestamp = Column(DateTime)
    
    # Métriques d'engagement
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    saves_count = Column(Integer, default=0, nullable=True)  # Instagram uniquement
    
    # Métriques de portée
    reach = Column(Integer, nullable=True)
    impressions = Column(Integer, nullable=True)
    
    # Métriques TikTok spécifiques
    video_views = Column(Integer, nullable=True)
    play_time = Column(Float, nullable=True)
    completion_rate = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    account = relationship("SocialAccount", back_populates="posts")


def create_tables():
    """Créer toutes les tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Obtenir une session de base de données."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()