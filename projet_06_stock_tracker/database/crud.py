"""
Opérations CRUD pour la base de données - VERSION CORRIGÉE
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, UserSession, StockAnalysis, Alert, UserPreferences
from datetime import datetime, timedelta
import json

class DatabaseManager:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_user_session(self, ip_address=None, user_agent=None):
        """Crée une nouvelle session utilisateur"""
        session = self.Session()
        try:
            user_session = UserSession(
                ip_address=ip_address,
                user_agent=user_agent
            )
            session.add(user_session)
            session.commit()
            
            # Crée les préférences par défaut
            default_prefs = UserPreferences(
                session_id=user_session.id,
                default_symbols=["AAPL", "TSLA", "MSFT"],
                chart_settings={"theme": "light", "height": 600},
                indicator_defaults={"sma": [20, 50], "rsi": True}
            )
            session.add(default_prefs)
            session.commit()
            
            return user_session.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def save_analysis(self, session_id, symbol, timeframe, indicators, signals, chart_data=None):
        """Sauvegarde une analyse technique"""
        session = self.Session()
        try:
            analysis = StockAnalysis(
                session_id=session_id,
                symbol=symbol,
                timeframe=timeframe,
                indicators_config=indicators,
                signals_detected=signals,
                chart_data=chart_data,
                analysis_metadata={"saved_at": datetime.utcnow().isoformat()}  # ✅ CORRIGÉ
            )
            session.add(analysis)
            session.commit()
            return analysis.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_analysis_history(self, session_id, limit=10):
        """Récupère l'historique des analyses"""
        session = self.Session()
        try:
            analyses = session.query(StockAnalysis)\
                .filter(StockAnalysis.session_id == session_id)\
                .order_by(StockAnalysis.analysis_date.desc())\
                .limit(limit)\
                .all()
            return analyses
        finally:
            session.close()
    
    def create_alert(self, session_id, symbol, alert_type, condition):
        """Crée une nouvelle alerte"""
        session = self.Session()
        try:
            alert = Alert(
                session_id=session_id,
                symbol=symbol,
                alert_type=alert_type,
                condition=condition
            )
            session.add(alert)
            session.commit()
            return alert.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_user_preferences(self, session_id):
        """Récupère les préférences utilisateur"""
        session = self.Session()
        try:
            prefs = session.query(UserPreferences)\
                .filter(UserPreferences.session_id == session_id)\
                .first()
            return prefs
        finally:
            session.close()
    
    def update_user_preferences(self, session_id, **updates):
        """Met à jour les préférences utilisateur"""
        session = self.Session()
        try:
            prefs = session.query(UserPreferences)\
                .filter(UserPreferences.session_id == session_id)\
                .first()
            
            if prefs:
                for key, value in updates.items():
                    if hasattr(prefs, key):
                        setattr(prefs, key, value)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()