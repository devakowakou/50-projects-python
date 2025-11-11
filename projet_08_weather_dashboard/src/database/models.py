"""
Modèles de données pour la base de données météo
"""

# Structure de la table weather_history
WEATHER_HISTORY_SCHEMA = """
CREATE TABLE IF NOT EXISTS weather_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    country TEXT,
    timestamp DATETIME NOT NULL,
    temperature REAL NOT NULL,
    feels_like REAL,
    temp_min REAL,
    temp_max REAL,
    pressure INTEGER,
    humidity INTEGER,
    description TEXT,
    icon TEXT,
    wind_speed REAL,
    wind_deg INTEGER,
    clouds INTEGER,
    visibility REAL,
    units TEXT DEFAULT 'metric',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(city, timestamp)
)
"""

# Structure de la table forecast_history
FORECAST_HISTORY_SCHEMA = """
CREATE TABLE IF NOT EXISTS forecast_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    country TEXT,
    forecast_timestamp DATETIME NOT NULL,
    temperature REAL NOT NULL,
    feels_like REAL,
    temp_min REAL,
    temp_max REAL,
    pressure INTEGER,
    humidity INTEGER,
    description TEXT,
    icon TEXT,
    wind_speed REAL,
    clouds INTEGER,
    pop INTEGER,
    units TEXT DEFAULT 'metric',
    saved_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

# Index pour améliorer les performances
INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_weather_city ON weather_history(city)",
    "CREATE INDEX IF NOT EXISTS idx_weather_timestamp ON weather_history(timestamp)",
    "CREATE INDEX IF NOT EXISTS idx_forecast_city ON forecast_history(city)",
    "CREATE INDEX IF NOT EXISTS idx_forecast_timestamp ON forecast_history(forecast_timestamp)"
]
