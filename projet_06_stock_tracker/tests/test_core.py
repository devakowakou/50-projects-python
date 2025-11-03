"""
Tests pour les modules core
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from src.core.data_manager import DataManager
from src.core.technical_engine import TechnicalEngine
from src.core.signals_engine import SignalsEngine

class TestCoreModules:
    @pytest.fixture
    def sample_data(self):
        """Données de test pour les indicateurs techniques"""
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        
        # Créer des données avec une tendance haussière
        np.random.seed(42)
        base_price = 100
        returns = np.random.normal(0.001, 0.02, 100)  # Rendements journaliers
        prices = base_price * (1 + returns).cumprod()
        
        df = pd.DataFrame({
            'Open': prices * 0.99,
            'High': prices * 1.01,
            'Low': prices * 0.98,
            'Close': prices,
            'Volume': np.random.randint(1000000, 5000000, 100)
        }, index=dates)
        
        return df
    
    @pytest.fixture
    def data_manager(self):
        return DataManager()
    
    @pytest.fixture
    def technical_engine(self):
        return TechnicalEngine()
    
    @pytest.fixture
    def signals_engine(self):
        return SignalsEngine()
    
    def test_sma_calculation(self, technical_engine, sample_data):
        """Test du calcul de la moyenne mobile simple"""
        sma_20 = technical_engine.calculate_sma(sample_data, 20)
        
        assert sma_20 is not None
        assert len(sma_20) == len(sample_data)
        assert sma_20.iloc[-1] == pytest.approx(sample_data['Close'].tail(20).mean(), rel=1e-10)
        # Les 19 premières valeurs doivent être NaN (fenêtre incomplète)
        assert pd.isna(sma_20.iloc[18])
        assert not pd.isna(sma_20.iloc[19])
    
    def test_ema_calculation(self, technical_engine, sample_data):
        """Test du calcul de la moyenne mobile exponentielle"""
        ema_12 = technical_engine.calculate_ema(sample_data, 12)
        
        assert ema_12 is not None
        assert len(ema_12) == len(sample_data)
        # L'EMA doit être plus réactive que la SMA
        sma_12 = technical_engine.calculate_sma(sample_data, 12)
        recent_volatility = abs(ema_12.iloc[-1] - sma_12.iloc[-1])
        assert recent_volatility > 0
    
    def test_rsi_calculation(self, technical_engine, sample_data):
        """Test du calcul du RSI"""
        rsi = technical_engine.calculate_rsi(sample_data, 14)
        
        assert rsi is not None
        assert len(rsi) == len(sample_data)
        # RSI doit être entre 0 et 100
        assert 0 <= rsi.iloc[-1] <= 100
        # Les 13 premières valeurs doivent être NaN
        assert pd.isna(rsi.iloc[13])
        assert not pd.isna(rsi.iloc[14])
    
    def test_macd_calculation(self, technical_engine, sample_data):
        """Test du calcul du MACD"""
        macd_data = technical_engine.calculate_macd(sample_data)
        
        assert 'macd' in macd_data
        assert 'signal' in macd_data
        assert 'histogram' in macd_data
        
        macd_line = macd_data['macd']
        signal_line = macd_data['signal']
        histogram = macd_data['histogram']
        
        assert len(macd_line) == len(sample_data)
        assert len(signal_line) == len(sample_data)
        assert len(histogram) == len(sample_data)
        
        # Vérifier que histogram = MACD - Signal
        assert histogram.iloc[-1] == pytest.approx(macd_line.iloc[-1] - signal_line.iloc[-1], rel=1e-10)
    
    def test_bollinger_bands_calculation(self, technical_engine, sample_data):
        """Test du calcul des bandes de Bollinger"""
        bb_data = technical_engine.calculate_bollinger_bands(sample_data, 20, 2)
        
        assert 'upper' in bb_data
        assert 'middle' in bb_data
        assert 'lower' in bb_data
        
        upper = bb_data['upper']
        middle = bb_data['middle']
        lower = bb_data['lower']
        
        # La bande du milieu doit être la SMA
        sma_20 = technical_engine.calculate_sma(sample_data, 20)
        assert middle.iloc[-1] == pytest.approx(sma_20.iloc[-1], rel=1e-10)
        
        # Vérifier l'écart type
        assert upper.iloc[-1] > middle.iloc[-1]
        assert lower.iloc[-1] < middle.iloc[-1]
    
    def test_add_all_indicators(self, technical_engine, sample_data):
        """Test de l'ajout de tous les indicateurs"""
        config = {
            'sma_periods': [20, 50],
            'ema_periods': [12, 26],
            'rsi': True,
            'macd': True,
            'bollinger': True
        }
        
        result_df = technical_engine.add_all_indicators(sample_data, config)
        
        # Vérifier que les colonnes ont été ajoutées
        expected_columns = ['SMA_20', 'SMA_50', 'EMA_12', 'EMA_26', 'RSI', 
                          'MACD', 'MACD_Signal', 'MACD_Histogram',
                          'BB_Upper', 'BB_Middle', 'BB_Lower']
        
        for col in expected_columns:
            assert col in result_df.columns
    
    def test_golden_cross_detection(self, signals_engine, sample_data):
        """Test de la détection du Golden Cross"""
        # Créer des données avec un Golden Cross artificiel
        df = sample_data.copy()
        df['SMA_20'] = [95 + i*0.1 for i in range(len(df))]
        df['SMA_50'] = [100 + i*0.05 for i in range(len(df))]
        
        # Simuler un croisement à la hausse
        df.loc[df.index[-2], 'SMA_20'] = df.loc[df.index[-2], 'SMA_50'] - 1
        df.loc[df.index[-1], 'SMA_20'] = df.loc[df.index[-1], 'SMA_50'] + 1
        
        golden_cross = signals_engine.detect_golden_cross(df)
        assert golden_cross is True
    
    def test_death_cross_detection(self, signals_engine, sample_data):
        """Test de la détection du Death Cross"""
        # Créer des données avec un Death Cross artificiel
        df = sample_data.copy()
        df['SMA_20'] = [105 - i*0.1 for i in range(len(df))]
        df['SMA_50'] = [100 - i*0.05 for i in range(len(df))]
        
        # Simuler un croisement à la baisse
        df.loc[df.index[-2], 'SMA_20'] = df.loc[df.index[-2], 'SMA_50'] + 1
        df.loc[df.index[-1], 'SMA_20'] = df.loc[df.index[-1], 'SMA_50'] - 1
        
        death_cross = signals_engine.detect_death_cross(df)
        assert death_cross is True
    
    def test_rsi_signals(self, signals_engine, sample_data):
        """Test des signaux RSI"""
        df = sample_data.copy()
        
        # Test RSI survendu
        df['RSI'] = [25] * len(df)
        rsi_signals_oversold = signals_engine.detect_rsi_signals(df)
        assert rsi_signals_oversold['rsi_oversold'] is True
        assert rsi_signals_oversold['rsi_overbought'] is False
        
        # Test RSI suracheté
        df['RSI'] = [75] * len(df)
        rsi_signals_overbought = signals_engine.detect_rsi_signals(df)
        assert rsi_signals_overbought['rsi_oversold'] is False
        assert rsi_signals_overbought['rsi_overbought'] is True
    
    def test_macd_signals(self, signals_engine, sample_data):
        """Test des signaux MACD"""
        df = sample_data.copy()
        
        # Simuler un croisement haussier
        df['MACD'] = [0.1] * len(df)
        df['MACD_Signal'] = [0.2] * len(df)
        df.loc[df.index[-1], 'MACD'] = 0.3  # MACD dépasse le signal
        
        macd_signals = signals_engine.detect_macd_signals(df)
        assert macd_signals['macd_bullish'] is True
        assert macd_signals['macd_bearish'] is False

if __name__ == "__main__":
    pytest.main([__file__, "-v"])