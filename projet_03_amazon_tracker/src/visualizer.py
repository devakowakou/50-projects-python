"""
Module de visualisation des données
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import config


class PriceVisualizer:
    """Générateur de graphiques pour l'analyse des prix"""
    
    @staticmethod
    def create_price_chart(df, product_name, target_price=None):
        """
        Crée un graphique d'évolution des prix
        
        Args:
            df: DataFrame avec colonnes 'checked_at' et 'price'
            product_name: Nom du produit
            target_price: Prix cible (optionnel)
            
        Returns:
            Figure Plotly
        """
        if df.empty:
            # Graphique vide
            fig = go.Figure()
            fig.add_annotation(
                text="Pas de données disponibles",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Convertir les dates en liste
        dates = df['checked_at'].tolist()
        prices = df['price'].tolist()
        
        fig = go.Figure()
        
        # Ligne de prix
        fig.add_trace(go.Scatter(
            x=dates,
            y=prices,
            mode='lines+markers',
            name='Prix',
            line=dict(color='#FF9900', width=2),
            marker=dict(size=8),
            hovertemplate='<b>%{y:.2f} €</b><br>%{x}<extra></extra>'
        ))
        
        # Ligne de prix cible si définie
        if target_price:
            fig.add_trace(go.Scatter(
                x=[dates[0], dates[-1]],
                y=[target_price, target_price],
                mode='lines',
                name='Prix cible',
                line=dict(color=config.COLOR_SUCCESS, width=2, dash='dash'),
                hovertemplate='<b>Cible: %{y:.2f} €</b><extra></extra>'
            ))
        
        fig.update_layout(
            title=f"Évolution du prix - {product_name}",
            xaxis_title="Date",
            yaxis_title="Prix (€)",
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_comparison_chart(products_df):
        """
        Crée un graphique de comparaison des produits
        
        Args:
            products_df: DataFrame avec les produits
            
        Returns:
            Figure Plotly
        """
        if products_df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="Aucun produit à afficher",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Limiter aux 10 premiers produits
        df = products_df.head(10).copy()
        
        # Calculer la différence avec le prix cible
        df['diff'] = df['current_price'] - df['target_price']
        df['status'] = df['diff'].apply(lambda x: 'Sous cible' if x <= 0 else 'Au-dessus')
        
        # Tronquer les noms longs
        df['name_short'] = df['name'].apply(lambda x: x[:40] + '...' if len(x) > 40 else x)
        
        fig = go.Figure()
        
        # Barres pour prix actuel
        fig.add_trace(go.Bar(
            y=df['name_short'],
            x=df['current_price'],
            name='Prix actuel',
            orientation='h',
            marker_color=config.COLOR_WARNING,
            text=df['current_price'].apply(lambda x: f"{x:.2f}€"),
            textposition='outside'
        ))
        
        # Barres pour prix cible
        fig.add_trace(go.Bar(
            y=df['name_short'],
            x=df['target_price'],
            name='Prix cible',
            orientation='h',
            marker_color=config.COLOR_SUCCESS,
            text=df['target_price'].apply(lambda x: f"{x:.2f}€"),
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Comparaison des produits suivis",
            xaxis_title="Prix (€)",
            yaxis_title="",
            barmode='group',
            template='plotly_white',
            height=max(400, len(df) * 60),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    @staticmethod
    def create_savings_gauge(current_price, target_price):
        """
        Crée une jauge d'économies potentielles
        
        Args:
            current_price: Prix actuel
            target_price: Prix cible
            
        Returns:
            Figure Plotly
        """
        if not current_price or not target_price:
            savings_percent = 0
        else:
            savings = target_price - current_price
            savings_percent = (savings / target_price) * 100
            savings_percent = max(-50, min(50, savings_percent))  # Limiter entre -50 et 50
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=current_price,
            delta={'reference': target_price, 'suffix': '€'},
            title={'text': "Prix actuel vs Prix cible"},
            gauge={
                'axis': {'range': [None, target_price * 1.5] if target_price else [0, 100]},
                'bar': {'color': config.COLOR_WARNING},
                'steps': [
                    {'range': [0, target_price], 'color': "lightgray"} if target_price else {},
                ],
                'threshold': {
                    'line': {'color': config.COLOR_SUCCESS, 'width': 4},
                    'thickness': 0.75,
                    'value': target_price or 0
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            template='plotly_white'
        )
        
        return fig
    
    @staticmethod
    def create_trend_indicator(trend, variation_percent):
        """
        Crée un indicateur visuel de tendance
        
        Args:
            trend: 'hausse' | 'baisse' | 'stable'
            variation_percent: Pourcentage de variation
            
        Returns:
            HTML string pour affichage
        """
        if trend == 'hausse':
            icon = "📈"
            color = config.COLOR_DANGER
            text = f"En hausse ({variation_percent:+.1f}%)"
        elif trend == 'baisse':
            icon = "📉"
            color = config.COLOR_SUCCESS
            text = f"En baisse ({variation_percent:+.1f}%)"
        else:
            icon = "➡️"
            color = "#808080"
            text = f"Stable ({variation_percent:+.1f}%)"
        
        return f'<span style="color: {color}; font-weight: bold;">{icon} {text}</span>'
