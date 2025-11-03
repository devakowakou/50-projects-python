"""
Tests pour les composants
"""

import pytest
import pandas as pd
from src.components.charts import ChartBuilder
from src.components.indicators import create_indicator_summary

class TestComponents:
    @pytest.fixture
    def sample_data(self):
        """Données de test pour les graphiques"""
        dates = pd.date_range(start='2024-01-01', periods=50, freq='D')
        
        data = pd.DataFrame({
            'Open': [100 + i*0.5 for i in range(50)],
            'High': [102 + i*0.5 for i in range(50)],
            'Low': [98 + i*0.5 for i in range(50)],
            'Close': [101 + i*0.5 for i in range(50)],
            'Volume': [1000000 + i*10000 for i in range(50)],
            'SMA_20': [100 + i*0.45 for i in range(50)],
            'SMA_50': [100 + i*0.4 for i in range(50)],
            'RSI': [45 + i*0.5 for i in range(50)],
            'MACD': [0.1 + i*0.01 for i in range(50)],
            'MACD_Signal': [0.05 + i*0.01 for i in range(50)],
            'MACD_Histogram': [0.05 + i*0.005 for i in range(50)]
        }, index=dates)
        
        return data
    
    @pytest.fixture
    def chart_builder(self):
        return ChartBuilder()
    
    def test_create_price_chart(self, chart_builder, sample_data):
        """Test de création du graphique de prix"""
        fig = chart_builder.create_price_chart(sample_data, "AAPL", ["SMA_20", "SMA_50"])
        
        assert fig is not None
        # Vérifier que la figure a des données
        assert len(fig.data) > 0
        # Vérifier la structure des subplots
        assert hasattr(fig, 'layout')
        assert 'xaxis' in fig.layout
        assert 'yaxis' in fig.layout
    
    def test_create_technical_chart(self, chart_builder, sample_data):
        """Test de création du graphique technique"""
        fig = chart_builder.create_technical_chart(sample_data, "TSLA")
        
        assert fig is not None
        assert len(fig.data) > 0
        # Vérifier qu'il y a 3 subplots
        assert hasattr(fig, 'layout')
        assert 'xaxis3' in fig.layout  # Troisième subplot
    
    def test_indicator_summary(self, sample_data):
        """Test du résumé des indicateurs"""
        # Tester avec des données complètes
        summary = create_indicator_summary(sample_data)
        assert summary is not None
        
        # Tester avec des données partielles
        partial_data = sample_data[['Close', 'RSI']].copy()
        summary_partial = create_indicator_summary(partial_data)
        assert summary_partial is not None
        
        # Tester avec des données vides
        empty_summary = create_indicator_summary({})
        assert empty_summary is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])