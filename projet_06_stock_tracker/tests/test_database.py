"""
Tests pour la base de données
"""

import pytest
import os
from datetime import datetime
from database.crud import DatabaseManager
from database.session import SessionManager

class TestDatabase:
    @pytest.fixture
    def db_manager(self):
        """Fixture pour le gestionnaire de base de données"""
        test_db_url = "sqlite:///test_stock_analysis.db"
        manager = DatabaseManager(test_db_url)
        yield manager
        # Nettoyage après les tests
        if os.path.exists("test_stock_analysis.db"):
            os.remove("test_stock_analysis.db")
    
    @pytest.fixture
    def session_manager(self):
        """Fixture pour le gestionnaire de sessions"""
        test_db_url = "sqlite:///test_sessions.db"
        manager = SessionManager(test_db_url)
        yield manager
        # Nettoyage après les tests
        if os.path.exists("test_sessions.db"):
            os.remove("test_sessions.db")
    
    def test_create_user_session(self, db_manager):
        """Test la création d'une session utilisateur"""
        session_id = db_manager.create_user_session("127.0.0.1", "test-agent")
        assert session_id is not None
        assert isinstance(session_id, str)
        assert len(session_id) == 36  # UUID length
    
    def test_save_analysis(self, db_manager):
        """Test la sauvegarde d'une analyse"""
        session_id = db_manager.create_user_session()
        
        analysis_id = db_manager.save_analysis(
            session_id=session_id,
            symbol="AAPL",
            timeframe="1d",
            indicators={"sma": [20, 50], "rsi": True},
            signals={"golden_cross": True, "rsi_oversold": False},
            chart_data={"data_points": 100}
        )
        
        assert analysis_id is not None
        assert isinstance(analysis_id, int)
    
    def test_get_analysis_history(self, db_manager):
        """Test la récupération de l'historique des analyses"""
        session_id = db_manager.create_user_session()
        
        # Créer plusieurs analyses
        for i in range(3):
            db_manager.save_analysis(
                session_id=session_id,
                symbol=f"TEST{i}",
                timeframe="1d",
                indicators={},
                signals={},
                chart_data={}
            )
        
        history = db_manager.get_analysis_history(session_id, limit=5)
        assert len(history) == 3
        assert history[0].symbol == "TEST2"  # Dernier en premier
    
    def test_create_alert(self, db_manager):
        """Test la création d'une alerte"""
        session_id = db_manager.create_user_session()
        
        alert_id = db_manager.create_alert(
            session_id=session_id,
            symbol="TSLA",
            alert_type="price",
            condition={"operator": ">", "value": 200}
        )
        
        assert alert_id is not None
        assert isinstance(alert_id, int)
    
    def test_user_preferences(self, db_manager):
        """Test la gestion des préférences utilisateur"""
        session_id = db_manager.create_user_session()
        
        # Récupération des préférences par défaut
        prefs = db_manager.get_user_preferences(session_id)
        assert prefs is not None
        assert prefs.default_symbols == ["AAPL", "TSLA", "MSFT"]
        
        # Mise à jour des préférences
        db_manager.update_user_preferences(
            session_id,
            theme="dark",
            chart_settings={"height": 700}
        )
        
        prefs_updated = db_manager.get_user_preferences(session_id)
        assert prefs_updated.theme == "dark"
        assert prefs_updated.chart_settings["height"] == 700
    
    def test_session_management(self, session_manager):
        """Test la gestion des sessions"""
        session_id = session_manager.create_session("192.168.1.1", "test-browser")
        
        session = session_manager.get_session(session_id)
        assert session is not None
        assert session.ip_address == "192.168.1.1"
        
        # Test mise à jour activité
        session_manager.update_session_activity(session_id)
        updated_session = session_manager.get_session(session_id)
        assert updated_session.last_activity is not None
    
    def test_cleanup_sessions(self, session_manager):
        """Test le nettoyage des anciennes sessions"""
        # Créer une session "ancienne"
        old_session_id = session_manager.create_session()
        old_session = session_manager.get_session(old_session_id)
        
        # Simuler une session vieille de 8 jours
        from datetime import timedelta
        old_session.last_activity = datetime.utcnow() - timedelta(days=8)
        
        cleaned_count = session_manager.cleanup_old_sessions(days=7)
        assert cleaned_count >= 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])