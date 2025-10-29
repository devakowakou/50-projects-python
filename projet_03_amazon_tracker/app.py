"""
Amazon Price Tracker - Application Streamlit
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.append(str(Path(__file__).parent))

import config
from src.database import DatabaseManager
from src.scraper import AmazonScraper
from src.analyzer import PriceAnalyzer
from src.visualizer import PriceVisualizer
from src.notifier import EmailNotifier


# Configuration de la page
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Charger le CSS personnalisé
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Initialiser les gestionnaires (avec cache)
@st.cache_resource
def init_managers():
    """Initialise les gestionnaires (cached)"""
    db = DatabaseManager()
    scraper = AmazonScraper()
    analyzer = PriceAnalyzer(db)
    visualizer = PriceVisualizer()
    notifier = EmailNotifier()
    return db, scraper, analyzer, visualizer, notifier


db, scraper, analyzer, visualizer, notifier = init_managers()


def show_header():
    """Affiche l'en-tête de l'application"""
    st.markdown('''
        <div class="main-header">
            <h1>🛒 Amazon Price Tracker</h1>
            <p>Suivez les prix, économisez malin !</p>
        </div>
    ''', unsafe_allow_html=True)


def show_dashboard():
    """Affiche le dashboard principal"""
    show_header()
    
    # Métriques globales
    st.markdown("## 📊 Vue d'ensemble")
    
    col1, col2, col3, col4 = st.columns(4)
    
    product_count = db.get_product_count()
    alerts = analyzer.check_alerts()
    savings = analyzer.calculate_savings_potential()
    
    with col1:
        st.metric("Produits suivis", product_count, f"Max: {config.MAX_PRODUCTS}")
    
    with col2:
        st.metric("Alertes actives", len(alerts))
    
    with col3:
        st.metric("Économies potentielles", f"{savings['total_savings']:.2f} €")
    
    with col4:
        st.metric("Économie moyenne", f"{savings['average_savings']:.2f} €")
    
    # Afficher les alertes
    if alerts:
        st.markdown("### 🔔 Alertes de Prix")
        for alert in alerts:
            st.markdown(f'''
                <div class="alert-success">
                    <strong>{alert['name']}</strong><br>
                    Prix actuel: <strong>{alert['current_price']:.2f} €</strong> 
                    | Prix cible: {alert['target_price']:.2f} € 
                    | Économie: <strong style="color: {config.COLOR_SUCCESS}">
                    {alert['savings']:.2f} € ({alert['savings_percent']:.1f}%)</strong>
                </div>
            ''', unsafe_allow_html=True)
    
    # Graphique de comparaison
    st.markdown("## 📈 Comparaison des Produits")
    products_df = db.get_all_products()
    
    if not products_df.empty:
        # Filtrer les produits avec prix cible
        products_with_target = products_df[products_df['target_price'].notna()].copy()
        
        if not products_with_target.empty:
            fig = visualizer.create_comparison_chart(products_with_target)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Définissez des prix cibles pour voir la comparaison")
    else:
        st.info("Aucun produit suivi. Ajoutez-en un pour commencer !")


def show_add_product():
    """Page d'ajout de produit"""
    show_header()
    
    st.markdown("## ➕ Ajouter un Produit")
    
    # Vérifier la limite
    product_count = db.get_product_count()
    if product_count >= config.MAX_PRODUCTS:
        st.error(f"Limite atteinte ! Maximum {config.MAX_PRODUCTS} produits pour la version MVP.")
        return
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.info(f"Produits suivis: {product_count}/{config.MAX_PRODUCTS}")
    
    with col2:
        if st.button("🎭 Mode Démo", use_container_width=True, help="Ajouter 5 produits de test"):
            with st.spinner("Génération des produits de démo..."):
                db.add_demo_products()
            st.success("✅ 5 produits de démo ajoutés !")
            st.balloons()
            st.rerun()
    
    # Formulaire
    with st.form("add_product_form"):
        st.warning("⚠️ **Note:** Le scraping Amazon peut être bloqué. Utilisez le **Mode Démo** pour tester l'interface avec des données simulées.")
        
        url = st.text_input(
            "URL du produit Amazon",
            placeholder="https://www.amazon.fr/dp/XXXXXXXXXX",
            help="Collez l'URL complète du produit Amazon"
        )
        
        target_price = st.number_input(
            "Prix cible (€)",
            min_value=0.0,
            step=0.01,
            help="Vous serez alerté quand le prix atteint ou descend sous ce montant"
        )
        
        submit = st.form_submit_button("🔍 Ajouter au suivi")
        
        if submit:
            if not url:
                st.error("Veuillez entrer une URL")
                return
            
            # Valider l'URL
            if not scraper.validate_url(url):
                st.error(f"URL invalide ! Doit être une URL {config.AMAZON_DOMAIN} valide")
                return
            
            # Scraper le produit
            with st.spinner("🔍 Récupération des informations du produit..."):
                product_data = scraper.scrape_product(url)
            
            if not product_data:
                st.error("Impossible de récupérer les informations. Vérifiez l'URL ou réessayez plus tard.")
                return
            
            # Prévisualisation
            st.success("✅ Produit trouvé !")
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if product_data['image_url']:
                    st.image(product_data['image_url'], width=150)
            
            with col2:
                st.markdown(f"**Nom:** {product_data['name']}")
                st.markdown(f"**Prix actuel:** {product_data['price']:.2f} €")
                st.markdown(f"**ASIN:** {product_data['asin']}")
                st.markdown(f"**Disponibilité:** {product_data['availability']}")
            
            # Ajouter à la base de données
            product_id = db.add_product(
                url=url,
                name=product_data['name'],
                price=product_data['price'],
                target_price=target_price if target_price > 0 else None,
                asin=product_data['asin'],
                image_url=product_data['image_url']
            )
            
            if product_id:
                st.success(f"✅ Produit ajouté avec succès ! (ID: {product_id})")
                st.balloons()
            else:
                st.warning("Ce produit est déjà dans votre liste de suivi")


def show_products_list():
    """Page de liste des produits"""
    show_header()
    
    st.markdown("## 📋 Mes Produits Suivis")
    
    # Bouton de rafraîchissement
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🔄 Rafraîchir tous les prix", use_container_width=True):
            refresh_all_prices()
    
    # Récupérer les produits
    products_df = db.get_all_products()
    
    if products_df.empty:
        st.info("Aucun produit suivi. Ajoutez-en un dans la page 'Ajouter un produit' !")
        return
    
    # Afficher les produits
    for idx, product in products_df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([1, 5, 2])
            
            with col1:
                if product['image_url']:
                    st.image(product['image_url'], width=100)
            
            with col2:
                st.markdown(f"### {product['name'][:60]}{'...' if len(product['name']) > 60 else ''}")
                
                # Prix et tendance
                price_col1, price_col2, price_col3 = st.columns(3)
                
                with price_col1:
                    st.markdown(f"**Prix actuel:** {product['current_price']:.2f} €")
                
                with price_col2:
                    if pd.notna(product['target_price']):
                        st.markdown(f"**Prix cible:** {product['target_price']:.2f} €")
                        
                        # Alerte si sous le prix cible
                        if product['current_price'] <= product['target_price']:
                            st.markdown(f"<span style='color: {config.COLOR_SUCCESS}; font-weight: bold;'>🎯 Prix atteint !</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("**Prix cible:** Non défini")
                
                with price_col3:
                    # Tendance
                    trend = analyzer.get_price_trend(product['id'])
                    if trend:
                        stats = analyzer.get_price_stats(product['id'])
                        if stats:
                            trend_html = visualizer.create_trend_indicator(trend, stats['variation_percent'])
                            st.markdown(trend_html, unsafe_allow_html=True)
                
                st.markdown(f"*Dernière vérification: {product['last_checked'] or 'Jamais'}*")
            
            with col3:
                if st.button(f"📈 Historique", key=f"hist_{product['id']}"):
                    st.session_state['selected_product'] = product['id']
                    st.rerun()
                
                if st.button(f"🗑️ Supprimer", key=f"del_{product['id']}"):
                    db.delete_product(product['id'])
                    st.success("Produit supprimé")
                    st.rerun()
            
            st.divider()


def show_product_history():
    """Page d'historique d'un produit"""
    show_header()
    
    st.markdown("## 📈 Historique des Prix")
    
    # Sélection du produit
    products_df = db.get_all_products()
    
    if products_df.empty:
        st.info("Aucun produit suivi")
        return
    
    # Créer un dict pour le selectbox
    product_options = {f"{row['name'][:50]}..." if len(row['name']) > 50 else row['name']: row['id'] 
                      for idx, row in products_df.iterrows()}
    
    selected_name = st.selectbox("Sélectionnez un produit", list(product_options.keys()))
    product_id = product_options[selected_name]
    
    # Récupérer les infos du produit
    product = db.get_product_by_id(product_id)
    
    if not product:
        st.error("Produit introuvable")
        return
    
    # Afficher les infos
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if product['image_url']:
            st.image(product['image_url'], width=200)
    
    with col2:
        st.markdown(f"### {product['name']}")
        st.markdown(f"**Prix actuel:** {product['current_price']:.2f} €")
        if product['target_price']:
            st.markdown(f"**Prix cible:** {product['target_price']:.2f} €")
        st.markdown(f"[Voir sur Amazon]({product['url']})")
    
    with col3:
        # Recommandation
        best_price = analyzer.get_best_price_info(product_id)
        if best_price:
            st.markdown("### 💡 Recommandation")
            st.markdown(best_price['recommendation'])
    
    st.divider()
    
    # Statistiques
    st.markdown("### 📊 Statistiques (30 derniers jours)")
    
    stats = analyzer.get_price_stats(product_id)
    
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Prix minimum", f"{stats['min']:.2f} €")
        
        with col2:
            st.metric("Prix maximum", f"{stats['max']:.2f} €")
        
        with col3:
            st.metric("Prix moyen", f"{stats['mean']:.2f} €")
        
        with col4:
            delta_text = f"{stats['variation_percent']:+.1f}%"
            st.metric("Variation", delta_text, delta_text)
    
    # Graphique d'évolution
    st.markdown("### 📈 Évolution du Prix")
    
    history_df = db.get_price_history(product_id, config.DEFAULT_HISTORY_DAYS)
    
    if not history_df.empty:
        fig = visualizer.create_price_chart(
            history_df,
            product['name'],
            product['target_price']
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pas encore d'historique disponible")


def refresh_all_prices():
    """Rafraîchit les prix de tous les produits"""
    products_df = db.get_all_products()
    
    if products_df.empty:
        st.warning("Aucun produit à rafraîchir")
        return
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    success_count = 0
    alerts_to_send = []
    
    for idx, product in products_df.iterrows():
        status_text.text(f"Rafraîchissement {idx + 1}/{len(products_df)}: {product['name'][:40]}...")
        
        # Scraper le prix
        product_data = scraper.scrape_product(product['url'])
        
        if product_data:
            # Mettre à jour le prix
            db.update_price(
                product['id'],
                product_data['price'],
                product_data['availability']
            )
            success_count += 1
            
            # Vérifier si alerte nécessaire
            if product['target_price'] and product_data['price'] <= product['target_price']:
                if product['current_price'] is None or product_data['price'] < product['current_price']:
                    # Nouveau prix sous la cible
                    alerts_to_send.append({
                        'name': product['name'],
                        'url': product['url'],
                        'current_price': product_data['price'],
                        'target_price': product['target_price']
                    })
        
        progress_bar.progress((idx + 1) / len(products_df))
    
    progress_bar.empty()
    status_text.empty()
    
    # Envoyer les alertes
    if alerts_to_send and config.SMTP_EMAIL:
        with st.spinner("📧 Envoi des alertes email..."):
            sent_count = notifier.send_multiple_alerts(alerts_to_send)
            if sent_count > 0:
                st.success(f"✅ {sent_count} alerte(s) envoyée(s) par email")
    
    st.success(f"✅ Rafraîchissement terminé ! {success_count}/{len(products_df)} produits mis à jour")
    st.rerun()


def show_settings():
    """Page des paramètres"""
    show_header()
    
    st.markdown("## ⚙️ Paramètres")
    
    # Configuration email
    st.markdown("### 📧 Configuration Email")
    
    if config.SMTP_EMAIL:
        st.success(f"✅ Email configuré: {config.SMTP_EMAIL}")
        
        if st.button("Tester la connexion"):
            with st.spinner("Test de connexion..."):
                if notifier.test_connection():
                    st.success("✅ Connexion réussie !")
                else:
                    st.error("❌ Échec de la connexion. Vérifiez vos paramètres dans .env")
    else:
        st.warning("⚠️ Email non configuré. Les alertes ne seront pas envoyées.")
        st.info("Configurez vos paramètres email dans le fichier .env")
    
    st.divider()
    
    # Informations système
    st.markdown("### 📊 Informations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Domaine Amazon:** {config.AMAZON_DOMAIN}")
        st.markdown(f"**Produits max:** {config.MAX_PRODUCTS}")
        st.markdown(f"**Délai entre requêtes:** {config.REQUEST_DELAY}s")
    
    with col2:
        st.markdown(f"**Historique par défaut:** {config.DEFAULT_HISTORY_DAYS} jours")
        st.markdown(f"**Tentatives max:** {config.MAX_RETRIES}")
        st.markdown(f"**Timeout:** {config.REQUEST_TIMEOUT}s")
    
    st.divider()
    
    # Base de données
    st.markdown("### 🗄️ Base de Données")
    
    st.markdown(f"**Chemin:** `{config.DB_PATH}`")
    
    product_count = db.get_product_count()
    st.markdown(f"**Produits actifs:** {product_count}")


def main():
    """Fonction principale de l'application"""
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    page = st.sidebar.radio(
        "Menu",
        ["Dashboard", "Ajouter un produit", "Mes produits", "Historique", "Paramètres"]
    )
    
    # Afficher la page sélectionnée
    if page == "Dashboard":
        show_dashboard()
    elif page == "Ajouter un produit":
        show_add_product()
    elif page == "Mes produits":
        show_products_list()
    elif page == "Historique":
        show_product_history()
    elif page == "Paramètres":
        show_settings()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📖 À propos")
    st.sidebar.info(
        "**Amazon Price Tracker v1.0**\n\n"
        "Projet 3 du challenge 50 Projects Python\n\n"
        "🔗 [Documentation](README.md)"
    )


if __name__ == "__main__":
    main()
