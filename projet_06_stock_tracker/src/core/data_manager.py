"""
Gestionnaire de données boursières
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DataManager:
    def __init__(self):
        self.cache = {}
    
    def get_stock_data(self, symbol, period="1y", interval="1d"):
        """Récupère les données boursières"""
        try:
            cache_key = f"{symbol}_{period}_{interval}"
            
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                raise ValueError(f"Aucune donnée trouvée pour {symbol}")
            
            # Nettoyage des données
            data = data.reset_index()
            data['Date'] = pd.to_datetime(data['Date'])
            data = data.set_index('Date')
            
            self.cache[cache_key] = data
            return data
            
        except Exception as e:
            logger.error(f"Erreur récupération données {symbol}: {e}")
            raise e
    
    def get_multiple_stocks(self, symbols, period="1y", interval="1d"):
        """Récupère les données de plusieurs symboles"""
        data_dict = {}
        for symbol in symbols:
            try:
                data_dict[symbol] = self.get_stock_data(symbol, period, interval)
            except Exception as e:
                logger.warning(f"Impossible de récupérer {symbol}: {e}")
                continue
        return data_dict
    
    def get_stock_info(self, symbol):
        """Récupère les informations du symbole"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                'name': info.get('longName', symbol),
                'sector': info.get('sector', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'currency': info.get('currency', 'USD')
            }
        except Exception as e:
            logger.error(f"Erreur info {symbol}: {e}")
            return {'name': symbol, 'sector': 'N/A', 'market_cap': 0, 'currency': 'USD'}