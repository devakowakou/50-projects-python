"""
Configuration centrale pour le Dashboard Budget
"""

# Catégories de dépenses prédéfinies
CATEGORIES_DEPENSES = [
    "Alimentation",
    "Logement",
    "Transport",
    "Factures",
    "Loisirs",
    "Shopping",
    "Santé",
    "Éducation",
    "Épargne",
    "Autres"
]

# Catégories de revenus prédéfinies
CATEGORIES_REVENUS = [
    "Salaire",
    "Prime/Bonus",
    "Freelance",
    "Investissements",
    "Autres"
]

# Modes de paiement
MODES_PAIEMENT = [
    "Carte Bancaire",
    "Espèces",
    "Virement",
    "Mobile Payment",
    "Prélèvement Automatique"
]

# Budgets par défaut par catégorie (mensuel)
BUDGETS_DEFAUT = {
    "Alimentation": 400,
    "Logement": 800,
    "Transport": 150,
    "Factures": 200,
    "Loisirs": 150,
    "Shopping": 100,
    "Santé": 100,
    "Éducation": 50,
    "Épargne": 300,
    "Autres": 100
}

# Seuils d'alerte (% du budget)
SEUIL_ALERTE_WARNING = 80  # Alerte à 80%
SEUIL_ALERTE_DANGER = 100   # Alerte à 100%

# Chemins des fichiers
DATA_DIR = "data"
TRANSACTIONS_FILE = f"{DATA_DIR}/transactions.json"
EXAMPLE_FILE = f"{DATA_DIR}/exemple_transactions.json"
OUTPUTS_DIR = "outputs"

# Couleurs pour les graphiques
COLORS = {
    "revenus": "#28a745",
    "depenses": "#dc3545",
    "solde": "#007bff",
    "budget": "#ffc107"
}

# Configuration Streamlit
PAGE_TITLE = "Budget Dashboard"
PAGE_ICON = "�"
LAYOUT = "wide"
