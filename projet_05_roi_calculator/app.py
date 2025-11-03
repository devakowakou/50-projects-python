"""
Application principale - Calculateur de ROI Marketing
Interface Streamlit améliorée
"""

import streamlit as st
from src.calculator import ROICalculator
from src.converter import MetricConverter
from src.simulator import ScenarioSimulator
from src.visualizer import MarketingVisualizer

# Configuration de la page
st.set_page_config(
    page_title="Calculateur de ROI Marketing",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour améliorer le design
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
    }
    .positive-roi {
        color: #2ca02c;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .negative-roi {
        color: #d62728;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .stButton button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #1668a6;
    }
</style>
""", unsafe_allow_html=True)

# En-tête amélioré
st.markdown('<h1 class="main-header"> Calculateur de ROI Marketing</h1>', unsafe_allow_html=True)
st.markdown("**Projet 5/50 - 50 Jours, 50 Projets Python**")

st.markdown("---")

# Initialisation des classes
calculator = ROICalculator()
converter = MetricConverter()
simulator = ScenarioSimulator()
visualizer = MarketingVisualizer()

# Sidebar améliorée
with st.sidebar:
    st.markdown("###  Navigation")
    st.markdown("---")
    
    app_mode = st.radio(
        "**Choisissez un module :**",
        [" Tableau de Bord", " Calculateur ROI", "Convertisseur Métriques", 
         " Simulateur Scénarios", " Rapports Détaillés"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("###  Astuces")
    st.info("""
    - **ROI > 0%** = Campagne rentable
    - **ROI > 100%** = Excellente performance  
    - Utilisez le simulateur pour tester différents scénarios
    """)

# Section Tableau de Bord (nouvelle page d'accueil)
if app_mode == " Tableau de Bord":
    st.header(" Tableau de Bord Marketing")
    
    # Métriques rapides en haut
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="ROI Moyen Industrie", 
            value="45%", 
            delta="+5%"
        )
    
    with col2:
        st.metric(
            label="CPC Moyen", 
            value="€2.50", 
            delta="-€0.30"
        )
    
    with col3:
        st.metric(
            label="CTR Standard", 
            value="3.2%", 
            delta="+0.4%"
        )
    
    with col4:
        st.metric(
            label="Seuil Rentabilité", 
            value="250 units", 
            delta="-15"
        )
    
    st.markdown("---")
    
    # Section calculateur rapide
    st.subheader("Calculateur Rapide ROI")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        quick_col1, quick_col2 = st.columns(2)
        with quick_col1:
            quick_revenue = st.number_input(
                "**Revenu généré (€)**", 
                min_value=0.0, 
                value=10000.0,
                step=1000.0,
                key="quick_revenue"
            )
        with quick_col2:
            quick_cost = st.number_input(
                "**Coût de la campagne (€)**", 
                min_value=0.0, 
                value=5000.0,
                step=500.0,
                key="quick_cost"
            )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        calculate_quick = st.button("** Calculer ROI Rapide**", type="primary", use_container_width=True)
        
        if calculate_quick:
            result = calculator.calculate_roi(quick_revenue, quick_cost)
            
            if 'error' not in result:
                roi_class = "positive-roi" if result['roi_percentage'] >= 0 else "negative-roi"
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="margin-top: 0;"> Résultats Rapides :</h3>
                    <p><strong>ROI :</strong> <span class="{roi_class}">{result['roi_percentage']}%</span></p>
                    <p><strong>Profit Net :</strong> €{result['net_profit']:,.2f}</p>
                    <p><strong>Ratio ROI :</strong> {result['roi_ratio']:.1f}:1</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Feedback visuel supplémentaire
                if result['roi_percentage'] > 100:
                    st.success("🎉 **Excellente performance !** Votre campagne est très rentable.")
                elif result['roi_percentage'] > 0:
                    st.info("✅ **Performance positive !** Votre campagne est rentable.")
                else:
                    st.warning("⚠️ **Attention :** Votre campagne n'est pas rentable.")
            else:
                st.error(f"❌ {result['error']}")

# Section Calculateur ROI améliorée
elif app_mode == " Calculateur ROI":
    st.header(" Calculateur de ROI Complet")
    
    # Layout en colonnes
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 Paramètres d'Entrée")
        
        with st.form("roi_calculator_form"):
            st.markdown("**Données de Base**")
            
            revenue = st.number_input(
                "Revenu généré par la campagne (€)",
                min_value=0.0,
                value=10000.0,
                step=1000.0,
                help="Chiffre d'affaires généré par la campagne"
            )
            
            cost = st.number_input(
                "Coût total de la campagne (€)",
                min_value=0.0,
                value=5000.0,
                step=500.0,
                help="Investissement total dans la campagne"
            )
            
            # Options avancées
            with st.expander("⚙️ Options avancées"):
                campaign_duration = st.number_input(
                    "Durée de la campagne (jours)",
                    min_value=1,
                    value=30,
                    step=1,
                    help="Durée en jours de la campagne"
                )
                
                campaign_type = st.selectbox(
                    "Type de campagne",
                    ["Publicité digitale", "Email marketing", "Réseaux sociaux", "Traditionnel", "Autre"]
                )
            
            # BOUTON SUBMIT
            submitted = st.form_submit_button("Calculer le ROI Détaillé", type="primary", use_container_width=True)
    
    with col2:
        st.subheader(" Résultats")
        
        if submitted:
            if cost == 0:
                st.error("❌ **Erreur :** Le coût ne peut pas être zéro pour calculer le ROI")
            else:
                with st.spinner("Calcul en cours..."):
                    result = calculator.calculate_roi(revenue, cost)
                
                if 'error' not in result:
                    # Affichage des métriques principales
                    st.success("✅ **Calcul terminé avec succès !**")
                    
                    roi_col1, roi_col2, roi_col3 = st.columns(3)
                    
                    with roi_col1:
                        st.metric(
                            label="**ROI**", 
                            value=f"{result['roi_percentage']}%",
                            delta=f"{result['roi_percentage']}%",
                            delta_color="normal" if result['roi_percentage'] >= 0 else "inverse"
                        )
                    
                    with roi_col2:
                        st.metric(
                            label="**Profit Net**", 
                            value=f"€{result['net_profit']:,.2f}",
                            delta=f"€{result['net_profit']:,.0f}"
                        )
                    
                    with roi_col3:
                        st.metric(
                            label="**Ratio ROI**", 
                            value=f"{result['roi_ratio']:.1f}:1",
                            help="Pour chaque € investi, retour généré"
                        )
                    
                    # Graphique ROI
                    st.subheader(" Visualisation du ROI")
                    try:
                        fig = visualizer.create_roi_gauge(result['roi_percentage'])
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.warning("⚠️ Le graphique n'est pas disponible pour le moment")
                    
                    # Analyse détaillée
                    with st.expander("🔍 Analyse Détaillée", expanded=True):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.markdown("###  Performance")
                            if result['roi_percentage'] > 100:
                                st.success("**🎉 Excellente performance**\n\nVotre campagne est très rentable avec un ROI supérieur à 100%.")
                            elif result['roi_percentage'] > 0:
                                st.info("**✅ Performance positive**\n\nVotre campagne est rentable avec un ROI positif.")
                            else:
                                st.warning("**⚠️ Performance négative**\n\nVotre campagne n'est pas rentable avec un ROI négatif.")
                        
                        with col_b:
                            st.markdown("###  Recommandations")
                            if result['roi_percentage'] < 0:
                                st.error("""
                                **Actions recommandées :**
                                - Réduire les coûts de campagne
                                - Améliorer le taux de conversion  
                                - Revoir le public cible
                                - Tester de nouveaux canaux
                                """)
                            elif result['roi_percentage'] < 50:
                                st.warning("""
                                **Optimisations possibles :**
                                - Optimiser les canaux performants
                                - Tester de nouvelles approches créatives
                                - Améliorer le ciblage
                                - Négocier les coûts publicitaires
                                """)
                            else:
                                st.success("""
                                **Stratégies de croissance :**
                                - Augmenter le budget sur cette campagne
                                - Répliquer la stratégie sur d'autres canaux
                                - Automatiser les processus
                                - Scalez votre audience
                                """)
                else:
                    st.error(f"❌ **Erreur de calcul :** {result['error']}")

# Sections autres modules
elif app_mode == "Convertisseur Métriques":
    st.header("Convertisseur de Métriques Marketing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚙️ Paramètres de Conversion")
        conversion_type = st.selectbox(
            "Type de conversion",
            ["CPC → CPM", "CPM → CPC", "CPA → CPC", "CTR → Taux de Conversion"]
        )
        
        # Exemple pour CPC → CPM
        if conversion_type == "CPC → CPM":
            cpc = st.number_input("Coût Par Clic (CPC €)", min_value=0.01, value=2.0, step=0.1)
            ctr = st.number_input("Click-Through Rate (CTR %)", min_value=0.1, value=3.0, step=0.1)
            
            if st.button("Convertir", type="primary", use_container_width=True):
                result = converter.cpc_to_cpm(cpc, ctr)
                if 'error' not in result:
                    st.success(f"**✅ Résultat : CPM = €{result['cpm']:.2f}**")
                    st.info(f"**Détails :** CPC €{cpc:.2f} × CTR {ctr}% × 10 = €{result['cpm']:.2f}")
                else:
                    st.error(f"❌ {result['error']}")
    
    with col2:
        st.subheader("📚 Explications")
        st.info("""
        ** Formules utilisées :**
        
        **CPM → CPC**
        ```
        CPM = CPC × CTR × 10
        ```
        
        **CPC → CPM**  
        ```
        CPC = CPM ÷ (CTR × 10)
        ```
        
        **CPA**
        ```
        CPA = Coût total ÷ Conversions
        ```
        
        **CTR**
        ```
        CTR = (Clics ÷ Impressions) × 100
        ```
        """)

elif app_mode == " Simulateur Scénarios":
    st.header(" Simulateur de Scénarios")
    
    st.info("""
    **🔬 Testez l'impact de différents scénarios sur votre ROI :**
    - Augmentation/réduction du budget
    - Changement du taux de conversion
    - Variation du prix de vente
    - Modification des coûts
    """)
    
    # Interface simulateur basique
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(" Scénario de Base")
        base_revenue = st.number_input("Revenu de base (€)", value=10000.0, step=1000.0)
        base_cost = st.number_input("Coût de base (€)", value=5000.0, step=500.0)
        
        st.subheader("🎛️ Modifications")
        revenue_change = st.slider("Changement revenu (%)", -50, 200, 10)
        cost_change = st.slider("Changement coût (%)", -50, 200, 5)
    
    with col2:
        st.subheader(" Résultats du Scénario")
        if st.button(" Simuler le scénario", type="primary", use_container_width=True):
            scenario = simulator.simulate_roi_scenario(
                base_revenue, base_cost, revenue_change, cost_change
            )
            
            st.metric(
                "Nouveau ROI", 
                f"{scenario['new_roi']}%", 
                delta=f"{scenario['roi_change']}%"
            )
            st.metric(
                "Nouveau Profit Net", 
                f"€{scenario['new_revenue'] - scenario['new_cost']:,.2f}"
            )
            
            # Analyse du scénario
            st.info(f"""
            ** Analyse du scénario :**
            - Revenu : €{base_revenue:,.2f} → €{scenario['new_revenue']:,.2f}
            - Coût : €{base_cost:,.2f} → €{scenario['new_cost']:,.2f}
            - ROI : {scenario['original_roi']}% → {scenario['new_roi']}%
            """)

elif app_mode == " Rapports Détaillés":
    st.header(" Rapports et Analytics")
    
    st.warning("🚧 **Module en cours de développement...**")
    st.info("""
    ** Fonctionnalités à venir :**
    -  Rapports PDF détaillés
    -  Historique des calculs
    - Comparaisons multi-campagnes
    - 📱 Export des données
    - 🎨 Dashboard avancé
    """)
    
    # Placeholder pour les futures fonctionnalités
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Export des Données")
        st.button("📄 Générer rapport PDF", disabled=True)
        st.button(" Exporter en CSV", disabled=True)
    
    with col2:
        st.subheader(" Analytics")
        st.button(" Voir l'historique", disabled=True)
        st.button("Comparer campagnes", disabled=True)

# Footer amélioré
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 1])
with footer_col1:
    st.markdown("**🔗 Projet 5/50** - 50 Jours, 50 Projets Python")
with footer_col2:
    st.markdown("**Version :** 1.0.0")
with footer_col3:
    st.markdown("** Dernière mise à jour :** Octobre 2024")

# Message de debug (optionnel - à enlever en production)
if st.sidebar.checkbox("🐛 Mode Debug", value=False):
    st.sidebar.write("**Debug Info:**")
    st.sidebar.write(f"Module actuel: {app_mode}")
    st.sidebar.write("Classes initialisées avec succès")