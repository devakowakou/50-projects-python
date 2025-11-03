"""
Application principale - Stock Analysis Dashboard
"""

import dash
from dash import html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from datetime import datetime
import logging
import pandas as pd  # Ajouter cette ligne

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import des modules personnalisés
from database.crud import DatabaseManager
from database.models import Base
from src.core.data_manager import DataManager
from src.core.technical_engine import TechnicalEngine
from src.core.signals_engine import SignalsEngine
from src.components.charts import ChartBuilder
from src.layout.header import create_header
from src.layout.sidebar import create_sidebar
from src.layout.charts_layout import create_charts_layout

import config

# Initialisation de l'application Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    suppress_callback_exceptions=True
)

app.title = "Stock Analysis Dashboard"

# Initialisation des composants
db_manager = DatabaseManager(config.DATABASE_URL)
data_manager = DataManager()
technical_engine = TechnicalEngine()
signals_engine = SignalsEngine()
chart_builder = ChartBuilder()

# Layout principal de l'application
app.layout = dbc.Container([
    # Store pour la session utilisateur
    dcc.Store(id='user-session', data=None),
    dcc.Store(id='current-analysis', data=None),
    
    # Header
    create_header(),
    
    # Contenu principal
    dbc.Row([
        # Sidebar
        dbc.Col([
            create_sidebar()
        ], width=config.LAYOUT_CONFIG["sidebar_width"], id="sidebar-col"),
        
        # Zone principale
        dbc.Col([
            create_charts_layout()
        ], width=config.LAYOUT_CONFIG["main_width"], id="main-col")
    ], className="g-2"),
    
    # Intervalle de mise à jour
    dcc.Interval(id='update-interval', interval=60000, n_intervals=0),  # 1 minute
    
    # Callback context pour le debugging
    html.Div(id='callback-context', style={'display': 'none'})
    
], fluid=True, className="px-3")

# Callbacks principaux
@app.callback(
    [Output('user-session', 'data'),
     Output('symbol-info', 'children')],
    Input('analyze-btn', 'n_clicks'),
    [State('symbol-selector', 'value'),
     State('user-session', 'data')]
)
def initialize_analysis(n_clicks, symbol, current_session):
    """Initialise l'analyse et la session utilisateur"""
    if n_clicks is None:
        return current_session, "Sélectionnez un symbole et cliquez sur Analyser"
    
    # Création de la session si elle n'existe pas
    if not current_session:
        session_id = db_manager.create_user_session()
        current_session = {'session_id': session_id, 'created_at': datetime.utcnow().isoformat()}
    
    try:
        # Récupération des informations du symbole
        stock_info = data_manager.get_stock_info(symbol)
        
        info_card = dbc.Card([
            dbc.CardBody([
                html.H6(f"📊 {stock_info['name']}", className="card-title"),
                html.P(f"Secteur: {stock_info['sector']}", className="card-text mb-1"),
                html.P(f"Market Cap: {stock_info['market_cap']:,.0f} {stock_info['currency']}", 
                       className="card-text mb-1"),
                html.P(f"Symbole: {symbol}", className="card-text mb-0")
            ])
        ], color="light")
        
        return current_session, info_card
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        return current_session, dbc.Alert(f"Erreur: {str(e)}", color="danger")

@app.callback(
    [Output('price-chart', 'figure'),
     Output('technical-chart', 'figure'),
     Output('signals-display', 'children'),
     Output('current-analysis', 'data')],
    [Input('analyze-btn', 'n_clicks'),
     Input('update-interval', 'n_intervals')],
    [State('symbol-selector', 'value'),
     State('period-selector', 'value'),
     State('indicators-checklist', 'value'),
     State('user-session', 'data')]
)
def update_analysis(n_clicks, n_intervals, symbol, period, indicators, user_session):
    """Met à jour l'analyse technique"""
    if n_clicks is None and n_intervals == 0:
        # Retourne des figures vides au démarrage
        empty_fig = chart_builder.create_price_chart(pd.DataFrame(), symbol)
        return empty_fig, empty_fig, "Aucune analyse effectuée", None
    
    try:
        # Récupération des données
        stock_data = data_manager.get_stock_data(symbol, period=period)
        
        if stock_data.empty:
            raise ValueError(f"Aucune donnée disponible pour {symbol}")
        
        # Configuration des indicateurs
        indicator_config = {
            'sma_periods': config.INDICATOR_CONFIG['sma_periods'] if 'sma' in indicators else [],
            'ema_periods': config.INDICATOR_CONFIG['ema_periods'] if 'sma' in indicators else [],
            'rsi': 'rsi' in indicators,
            'macd': 'macd' in indicators,
            'bollinger': 'bollinger' in indicators
        }
        
        # Calcul des indicateurs techniques
        analyzed_data = technical_engine.add_all_indicators(stock_data, indicator_config)
        
        # Génération des signaux
        signals = signals_engine.generate_all_signals(analyzed_data)
        
        # Création des graphiques
        price_chart = chart_builder.create_price_chart(analyzed_data, symbol, 
                                                     [f'SMA_{p}' for p in indicator_config['sma_periods']])
        technical_chart = chart_builder.create_technical_chart(analyzed_data, symbol)
        
        # Affichage des signaux
        signals_display = create_signals_display(signals)
        
        # Sauvegarde de l'analyse
        analysis_data = {
            'symbol': symbol,
            'period': period,
            'signals': signals,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if user_session:
            db_manager.save_analysis(
                user_session['session_id'],
                symbol,
                period,
                indicator_config,
                signals,
                {'data_points': len(analyzed_data)}
            )
        
        return price_chart, technical_chart, signals_display, analysis_data
        
    except Exception as e:
        logger.error(f"Erreur dans update_analysis: {e}")
        error_fig = chart_builder.create_price_chart(pd.DataFrame(), symbol)
        error_msg = dbc.Alert(f"Erreur d'analyse: {str(e)}", color="danger")
        return error_fig, error_fig, error_msg, None

def create_signals_display(signals):
    """Crée l'affichage des signaux techniques"""
    if not signals:
        return dbc.Alert("🔍 Aucun signal détecté - Analyse en cours ou données insuffisantes", color="info")
    
    signal_cards = []
    
    # Signaux haussiers
    bullish_signals = []
    if signals.get('golden_cross'):
        bullish_signals.append("✅ Golden Cross (MA20 > MA50)")
    if signals.get('macd_bullish'):
        bullish_signals.append("✅ MACD Croisement haussier")
    
    # Signaux baissiers  
    bearish_signals = []
    if signals.get('death_cross'):
        bearish_signals.append("❌ Death Cross (MA20 < MA50)")
    if signals.get('macd_bearish'):
        bearish_signals.append("❌ MACD Croisement baissier")
    
    # Signaux RSI
    rsi_signals = []
    if signals.get('rsi_oversold'):
        rsi_signals.append("📉 RSI Survente (<30) - Potentiel rebond")
    if signals.get('rsi_overbought'):
        rsi_signals.append("📈 RSI Surachat (>70) - Potentielle correction")
    
    # Création des cartes de signaux
    if bullish_signals:
        signal_cards.append(
            dbc.Alert([
                html.H5("📈 Signaux Haussiers", className="alert-heading mb-2"),
                html.Ul([html.Li(signal, className="mb-1") for signal in bullish_signals], className="mb-0")
            ], color="success", className="mb-3")
        )
    
    if bearish_signals:
        signal_cards.append(
            dbc.Alert([
                html.H5("📉 Signaux Baissiers", className="alert-heading mb-2"),
                html.Ul([html.Li(signal, className="mb-1") for signal in bearish_signals], className="mb-0")
            ], color="danger", className="mb-3")
        )
    
    if rsi_signals:
        signal_cards.append(
            dbc.Alert([
                html.H5("⚡ Signaux RSI", className="alert-heading mb-2"),
                html.Ul([html.Li(signal, className="mb-1") for signal in rsi_signals], className="mb-0")
            ], color="warning", className="mb-3")
        )
    
    if not signal_cards:
        signal_cards.append(
            dbc.Alert("ℹ️ Aucun signal fort détecté - Marché neutre", color="info", className="mb-3")
        )
    
    return html.Div(signal_cards, className="alert-container")

# Lancement de l'application
if __name__ == '__main__':
    logger.info("🚀 Démarrage de l'application Stock Analysis Dashboard")
    app.run_server(debug=True, host='0.0.0.0', port=8050)