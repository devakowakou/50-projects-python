"""
Modèles de données SQLAlchemy - VERSION CORRIGÉE
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class UserSession(Base):
    __tablename__ = 'user_sessions'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45))
    user_agent = Column(Text)

class StockAnalysis(Base):
    __tablename__ = 'stock_analyses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(36))
    symbol = Column(String(10), nullable=False)
    timeframe = Column(String(10))
    analysis_date = Column(DateTime, default=datetime.utcnow)
    indicators_config = Column(JSON)
    signals_detected = Column(JSON)
    chart_data = Column(JSON)
    analysis_metadata = Column(JSON)  # ✅ CORRIGÉ : changé de 'metadata' à 'analysis_metadata'

class Alert(Base):
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(36))
    symbol = Column(String(10))
    alert_type = Column(String(20))  # 'price', 'technical', 'crossover'
    condition = Column(JSON)
    is_active = Column(Boolean, default=True)
    triggered = Column(Boolean, default=False)
    trigger_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserPreferences(Base):
    __tablename__ = 'user_preferences'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(36), unique=True)
    default_symbols = Column(JSON)
    chart_settings = Column(JSON)
    indicator_defaults = Column(JSON)
    theme = Column(String(20), default='light')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)