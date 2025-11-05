from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Remplacer la valeur par défaut PostgreSQL par SQLite local si non défini
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./data/logs.db')

# Détecter SQLite pour ajouter les bons connect_args
if DATABASE_URL.startswith("sqlite"):
    # pour SQLite avec SQLAlchemy + FastAPI (threading), désactiver check_same_thread
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
        echo=False
    )
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LogRecord(Base):
    """Modèle SQLAlchemy pour les logs"""
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String(45), index=True, nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    method = Column(String(10), nullable=False)
    url = Column(String(2048), index=True, nullable=False)
    status_code = Column(Integer, index=True, nullable=False)
    response_time = Column(Float, nullable=True)
    user_agent = Column(String(512), nullable=False)
    
    __table_args__ = (
        Index('idx_timestamp_status', 'timestamp', 'status_code'),
        Index('idx_ip_timestamp', 'ip', 'timestamp'),
    )

def init_db():
    """Crée toutes les tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données initialisée")

def get_db():
    """Générateur de session pour FastAPI Depends"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    init_db()