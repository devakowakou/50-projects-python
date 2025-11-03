"""
Moteur de génération de signaux
"""

import pandas as pd
from typing import Dict, List

class SignalsEngine:
    def __init__(self):
        pass
    
    def detect_golden_cross(self, data: pd.DataFrame) -> bool:
        """Détecte un Golden Cross (MA20 > MA50)"""
        if 'SMA_20' not in data.columns or 'SMA_50' not in data.columns:
            return False
        
        latest = data.iloc[-1]
        prev = data.iloc[-2] if len(data) > 1 else latest
        
        # Vérifie si MA20 vient de franchir MA50 à la hausse
        cross_up = (prev['SMA_20'] <= prev['SMA_50']) and (latest['SMA_20'] > latest['SMA_50'])
        return cross_up
    
    def detect_death_cross(self, data: pd.DataFrame) -> bool:
        """Détecte un Death Cross (MA20 < MA50)"""
        if 'SMA_20' not in data.columns or 'SMA_50' not in data.columns:
            return False
        
        latest = data.iloc[-1]
        prev = data.iloc[-2] if len(data) > 1 else latest
        
        # Vérifie si MA20 vient de franchir MA50 à la baisse
        cross_down = (prev['SMA_20'] >= prev['SMA_50']) and (latest['SMA_20'] < latest['SMA_50'])
        return cross_down
    
    def detect_rsi_signals(self, data: pd.DataFrame) -> Dict[str, bool]:
        """Détecte les signaux RSI"""
        if 'RSI' not in data.columns:
            return {}
        
        latest_rsi = data['RSI'].iloc[-1]
        
        return {
            'rsi_oversold': latest_rsi < 30,
            'rsi_overbought': latest_rsi > 70
        }
    
    def detect_macd_signals(self, data: pd.DataFrame) -> Dict[str, bool]:
        """Détecte les signaux MACD"""
        if 'MACD' not in data.columns or 'MACD_Signal' not in data.columns:
            return {}
        
        latest = data.iloc[-1]
        prev = data.iloc[-2] if len(data) > 1 else latest
        
        macd_cross_up = (prev['MACD'] <= prev['MACD_Signal']) and (latest['MACD'] > latest['MACD_Signal'])
        macd_cross_down = (prev['MACD'] >= prev['MACD_Signal']) and (latest['MACD'] < latest['MACD_Signal'])
        
        return {
            'macd_bullish': macd_cross_up,
            'macd_bearish': macd_cross_down
        }
    
    def generate_all_signals(self, data: pd.DataFrame) -> Dict:
        """Génère tous les signaux techniques"""
        signals = {}
        
        # Signaux de croisement
        signals['golden_cross'] = self.detect_golden_cross(data)
        signals['death_cross'] = self.detect_death_cross(data)
        
        # Signaux RSI
        signals.update(self.detect_rsi_signals(data))
        
        # Signaux MACD
        signals.update(self.detect_macd_signals(data))
        
        return signals