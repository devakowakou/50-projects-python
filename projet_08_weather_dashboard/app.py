#!/usr/bin/env python3
"""
Dashboard Météo - Application Streamlit
Lance avec: streamlit run app.py
"""

from src.visualization.dashboard import WeatherDashboard

if __name__ == "__main__":
    dashboard = WeatherDashboard()
    dashboard.run()
