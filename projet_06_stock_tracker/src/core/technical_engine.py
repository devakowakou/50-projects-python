"""
Moteur d'analyse technique
"""

import pandas as pd
import numpy as np
from typing import Dict, List

class TechnicalEngine:
    def __init__(self):
        pass
    
    def calculate_sma(self, data: pd.DataFrame, period: int) -> pd.Series:
        """Calcule la moyenne mobile simple"""
        return data['Close'].rolling(window=period).mean()
    
    def calculate_ema(self, data: pd.DataFrame, period: int) -> pd.Series:
        """Calcule la moyenne mobile exponentielle"""
        return data['Close'].ewm(span=period, adjust=False).mean()
    
    def calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calcule le RSI"""
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        """Calcule le MACD"""
        ema_12 = self.calculate_ema(data, 12)
        ema_26 = self.calculate_ema(data, 26)
        macd_line = ema_12 - ema_26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def calculate_bollinger_bands(self, data: pd.DataFrame, period: int = 20, std: int = 2) -> Dict[str, pd.Series]:
        """Calcule les bandes de Bollinger"""
        sma = self.calculate_sma(data, period)
        std_dev = data['Close'].rolling(window=period).std()
        
        upper_band = sma + (std_dev * std)
        lower_band = sma - (std_dev * std)
        
        return {
            'upper': upper_band,
            'middle': sma,
            'lower': lower_band
        }
    
    def add_all_indicators(self, data: pd.DataFrame, config: Dict) -> pd.DataFrame:
        """Ajoute tous les indicateurs techniques aux données"""
        df = data.copy()
        
        # Moyennes mobiles
        if 'sma_periods' in config:
            for period in config['sma_periods']:
                df[f'SMA_{period}'] = self.calculate_sma(df, period)
        
        if 'ema_periods' in config:
            for period in config['ema_periods']:
                df[f'EMA_{period}'] = self.calculate_ema(df, period)
        
        # RSI
        if config.get('rsi', True):
            df['RSI'] = self.calculate_rsi(df)
        
        # MACD
        if config.get('macd', True):
            macd_data = self.calculate_macd(df)
            df['MACD'] = macd_data['macd']
            df['MACD_Signal'] = macd_data['signal']
            df['MACD_Histogram'] = macd_data['histogram']
        
        # Bollinger Bands
        if config.get('bollinger', True):
            bb_data = self.calculate_bollinger_bands(df)
            df['BB_Upper'] = bb_data['upper']
            df['BB_Middle'] = bb_data['middle']
            df['BB_Lower'] = bb_data['lower']
        
        return df