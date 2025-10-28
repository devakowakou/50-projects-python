"""
Budget Dashboard - Application Streamlit
Projet 2 du Challenge 50 Projets Python
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.dirname(__file__))

from src.data_manager import DataManager
from src.budget_analyzer import BudgetAnalyzer
from src.visualizer import Visualizer
import config

# Configuration de la page
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .alert-warning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        color: #856404;
        font-weight: 500;
    }
    .alert-danger {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        color: #721c24;
        font-weight: 500;
    }
    .success-message {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation du session state
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager(config.TRANSACTIONS_FILE)

if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = False

if 'show_edit_form' not in st.session_state:
    st.session_state.show_edit_form = False
    st.session_state.edit_transaction_id = None

# Initialiser les données exemple si fichier vide
def init_example_data():
    """Charge les données exemple si aucune transaction"""
    if not os.path.exists(config.TRANSACTIONS_FILE) or \
       len(st.session_state.data_manager.get_all_transactions()) == 0:
        
        if os.path.exists(config.EXAMPLE_FILE):
            import json
            with open(config.EXAMPLE_FILE, 'r', encoding='utf-8') as f:
                example_data = json.load(f)
            
            # Copier les données exemple
            for transaction in example_data:
                st.session_state.data_manager.add_transaction(transaction)
            
            return True
    return False


def show_metrics(metrics: dict):
    """Affiche les métriques principales"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Solde",
            value=f"{metrics['solde']:.2f}€",
            delta=f"{metrics['taux_epargne']:.1f}% d'épargne"
        )
    
    with col2:
        st.metric(
            label="Revenus",
            value=f"{metrics['revenus']:.2f}€",
            delta="Total période"
        )
    
    with col3:
        st.metric(
            label="Dépenses",
            value=f"{metrics['depenses']:.2f}€",
            delta="Total période"
        )
    
    with col4:
        st.metric(
            label="Économies",
            value=f"{metrics['economies']:.2f}€",
            delta=f"{metrics['taux_epargne']:.1f}% du revenu"
        )


def show_alerts(alerts: list):
    """Affiche les alertes"""
    if not alerts:
        st.success("Aucune alerte - Tous les budgets sont sous contrôle !")
        return
    
    st.warning(f"{len(alerts)} alerte(s) détectée(s)")
    
    for alert in alerts:
        if alert['level'] == 'danger':
            st.markdown(f"""
            <div class="alert-danger">
                {alert['message']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-warning">
                {alert['message']}
            </div>
            """, unsafe_allow_html=True)


def add_transaction_form():
    """Formulaire d'ajout de transaction"""
    st.subheader("Ajouter une Transaction")
    
    with st.form("add_transaction_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input(
                "Date",
                value=datetime.now(),
                max_value=datetime.now()
            )
            
            trans_type = st.selectbox(
                "Type",
                options=["depense", "revenu"],
                format_func=lambda x: "Dépense" if x == "depense" else "Revenu"
            )
            
            montant = st.number_input(
                "Montant (€)",
                min_value=0.01,
                step=0.01,
                format="%.2f"
            )
        
        with col2:
            # Sélection de catégorie selon le type
            if trans_type == "depense":
                categorie = st.selectbox("Catégorie", options=config.CATEGORIES_DEPENSES)
            else:
                categorie = st.selectbox("Catégorie", options=config.CATEGORIES_REVENUS)
            
            mode_paiement = st.selectbox("Mode de paiement", options=config.MODES_PAIEMENT)
            
            description = st.text_input("Description (optionnel)")
        
        submitted = st.form_submit_button("Enregistrer", use_container_width=True)
        
        if submitted:
            transaction = {
                "date": date.strftime("%Y-%m-%d"),
                "type": trans_type,
                "montant": float(montant),
                "categorie": categorie,
                "description": description,
                "mode_paiement": mode_paiement
            }
            
            transaction_id = st.session_state.data_manager.add_transaction(transaction)
            st.success(f"Transaction ajoutée avec succès ! (ID: {transaction_id[:8]}...)")
            st.rerun()


def show_transactions_history():
    """Affiche l'historique des transactions"""
    st.subheader("Historique des Transactions")
    
    df = st.session_state.data_manager.get_transactions_dataframe()
    
    if df.empty:
        st.info("Aucune transaction enregistrée")
        return
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_type = st.multiselect(
            "Filtrer par type",
            options=["depense", "revenu"],
            default=["depense", "revenu"],
            format_func=lambda x: "Dépenses" if x == "depense" else "Revenus"
        )
    
    with col2:
        all_categories = df['categorie'].unique().tolist()
        filter_categories = st.multiselect(
            "Filtrer par catégorie",
            options=all_categories,
            default=all_categories
        )
    
    with col3:
        date_range = st.date_input(
            "Période",
            value=(df['date'].min().date(), df['date'].max().date()),
            max_value=datetime.now()
        )
    
    # Appliquer les filtres
    df_filtered = df[
        (df['type'].isin(filter_type)) &
        (df['categorie'].isin(filter_categories))
    ]
    
    if len(date_range) == 2:
        df_filtered = df_filtered[
            (df_filtered['date'].dt.date >= date_range[0]) &
            (df_filtered['date'].dt.date <= date_range[1])
        ]
    
    # Afficher le tableau
    st.dataframe(
        df_filtered[['date', 'type', 'categorie', 'description', 'montant', 'mode_paiement']],
        use_container_width=True,
        height=400,
        hide_index=True
    )
    
    # Options d'actions
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Supprimer toutes les transactions", type="secondary"):
            if st.session_state.data_manager.clear_all_transactions():
                st.success("Toutes les transactions ont été supprimées")
                st.rerun()
    
    with col2:
        if st.button("Exporter en CSV", type="secondary"):
            try:
                output_path = f"{config.OUTPUTS_DIR}/export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                os.makedirs(config.OUTPUTS_DIR, exist_ok=True)
                st.session_state.data_manager.export_to_csv(output_path)
                st.success(f"Exporté vers {output_path}")
            except Exception as e:
                st.error(f"Erreur: {str(e)}")
    
    with col3:
        if st.button("Exporter en JSON", type="secondary"):
            try:
                output_path = f"{config.OUTPUTS_DIR}/export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                os.makedirs(config.OUTPUTS_DIR, exist_ok=True)
                st.session_state.data_manager.export_to_json(output_path)
                st.success(f"Exporté vers {output_path}")
            except Exception as e:
                st.error(f"Erreur: {str(e)}")


def show_dashboard():
    """Page principale du dashboard"""
    st.markdown('<h1 class="main-header">Dashboard Budget Personnel</h1>', unsafe_allow_html=True)
    
    # Charger les données
    df = st.session_state.data_manager.get_transactions_dataframe()
    
    if df.empty:
        st.info("Bienvenue ! Commencez par ajouter des transactions ou charger les données exemple.")
        
        if st.button("Charger les données exemple", type="primary"):
            if init_example_data():
                st.success("Données exemple chargées !")
                st.rerun()
        return
    
    # Créer l'analyseur
    analyzer = BudgetAnalyzer(df)
    
    # Filtres de période
    st.sidebar.subheader("Période d'analyse")
    period_option = st.sidebar.radio(
        "Choisir une période",
        ["Tout", "Mois actuel", "30 derniers jours", "90 derniers jours", "Personnalisé"]
    )
    
    # Filtrer selon la période
    df_filtered = df.copy()
    
    if period_option == "Mois actuel":
        today = datetime.now()
        df_filtered = df[
            (df['date'].dt.year == today.year) &
            (df['date'].dt.month == today.month)
        ]
    elif period_option == "30 derniers jours":
        cutoff_date = datetime.now() - timedelta(days=30)
        df_filtered = df[df['date'] >= cutoff_date]
    elif period_option == "90 derniers jours":
        cutoff_date = datetime.now() - timedelta(days=90)
        df_filtered = df[df['date'] >= cutoff_date]
    elif period_option == "Personnalisé":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input("De", value=df['date'].min().date())
        with col2:
            end_date = st.date_input("À", value=df['date'].max().date())
        
        df_filtered = df[
            (df['date'].dt.date >= start_date) &
            (df['date'].dt.date <= end_date)
        ]
    
    # Recréer l'analyseur avec les données filtrées
    analyzer = BudgetAnalyzer(df_filtered)
    metrics = analyzer.get_summary_metrics()
    
    # Afficher les métriques
    show_metrics(metrics)
    
    st.markdown("---")
    
    # Alertes
    alerts = analyzer.get_alerts(config.BUDGETS_DEFAUT, config.SEUIL_ALERTE_WARNING, config.SEUIL_ALERTE_DANGER)
    show_alerts(alerts)
    
    st.markdown("---")
    
    # Visualisations
    visualizer = Visualizer(config.COLORS)
    
    # Tendance temporelle
    st.subheader("Évolution du Budget")
    trend_data = analyzer.get_daily_trend()
    if not trend_data.empty:
        fig_trend = visualizer.create_trend_chart(trend_data)
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Pas assez de données pour afficher la tendance")
    
    # Deux colonnes pour les graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Répartition des Dépenses")
        spending_by_cat = analyzer.get_spending_by_category()
        if not spending_by_cat.empty:
            fig_pie = visualizer.create_pie_chart(
                spending_by_cat,
                values_col='Montant',
                names_col='Catégorie',
                title=""
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Aucune dépense enregistrée")
    
    with col2:
        st.subheader("Sources de Revenus")
        income_by_cat = analyzer.get_income_by_category()
        if not income_by_cat.empty:
            fig_income = visualizer.create_pie_chart(
                income_by_cat,
                values_col='Montant',
                names_col='Catégorie',
                title=""
            )
            st.plotly_chart(fig_income, use_container_width=True)
        else:
            st.info("Aucun revenu enregistré")
    
    # État des budgets
    st.subheader("État des Budgets par Catégorie")
    budget_status = analyzer.get_budget_status(config.BUDGETS_DEFAUT)
    if not budget_status.empty:
        fig_budget = visualizer.create_budget_status_chart(budget_status)
        st.plotly_chart(fig_budget, use_container_width=True)
        
        # Tableau détaillé
        with st.expander("Détails des budgets"):
            st.dataframe(budget_status, use_container_width=True, hide_index=True)
    
    # Top dépenses
    st.subheader("Top 10 des Plus Grandes Dépenses")
    top_transactions = analyzer.get_top_transactions(n=10, transaction_type='depense')
    if not top_transactions.empty:
        st.dataframe(top_transactions, use_container_width=True, hide_index=True)


def main():
    """Fonction principale"""
    
    # Sidebar - Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choisir une page",
        ["Dashboard", "Ajouter Transaction", "Historique", "Paramètres"]
    )
    
    st.sidebar.markdown("---")
    
    # Informations
    st.sidebar.info("""
    **Budget Dashboard v1.0**
    
    Application de suivi de budget personnel.
    
    Projet 2 du Challenge 50 Projets Python
    """)
    
    # Routing
    if page == "Dashboard":
        show_dashboard()
    
    elif page == "Ajouter Transaction":
        add_transaction_form()
    
    elif page == "Historique":
        show_transactions_history()
    
    elif page == "Paramètres":
        st.subheader("Paramètres")
        
        st.markdown("### Budgets par Catégorie")
        st.info("Configuration des budgets mensuels par catégorie")
        
        # Afficher les budgets configurés
        budget_df = pd.DataFrame([
            {"Catégorie": cat, "Budget Mensuel (€)": budget}
            for cat, budget in config.BUDGETS_DEFAUT.items()
        ])
        st.dataframe(budget_df, use_container_width=True, hide_index=True)
        
        st.markdown("### Seuils d'Alerte")
        st.info(f"""
        - **Alerte Warning**: {config.SEUIL_ALERTE_WARNING}% du budget
        - **Alerte Danger**: {config.SEUIL_ALERTE_DANGER}% du budget
        """)
        
        st.markdown("### Fichiers")
        st.info(f"""
        - **Transactions**: `{config.TRANSACTIONS_FILE}`
        - **Exports**: `{config.OUTPUTS_DIR}/`
        """)


if __name__ == "__main__":
    main()
