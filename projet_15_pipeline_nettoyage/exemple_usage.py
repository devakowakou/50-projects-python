"""Exemple d'utilisation du pipeline de nettoyage."""

from src.pipeline import DataCleaningPipeline
from pathlib import Path

def exemple_basique():
    """Exemple d'utilisation basique du pipeline."""
    
    # Initialiser le pipeline
    pipeline = DataCleaningPipeline()
    
    # Fichiers d'entrée et de sortie
    input_file = "data/raw/sample_messy_data.csv"
    output_file = "data/cleaned/sample_clean_data.csv"
    
    # Traitement avec stratégies personnalisées
    result = pipeline.process_file(
        input_path=input_file,
        output_path=output_file,
        strategies={
            'missing_values': 'median',  # Imputation par médiane
            'outliers': 'iqr',          # Détection par IQR
            'duplicates': True,         # Supprimer les doublons
            'standardize': True         # Standardiser les formats
        }
    )
    
    # Affichage du résumé
    if result['success']:
        print(f"\n✅ Traitement réussi !")
        print(f"📊 Lignes : {result['summary']['original_rows']:,} → {result['summary']['final_rows']:,}")
        print(f"🎯 Qualité : {result['summary']['quality_before']:.1f}% → {result['summary']['quality_after']:.1f}%")
        print(f"⏱️ Temps : {result['processing_time']:.2f}s")
        print(f"📁 Fichier nettoyé : {result['output_file']}")
    else:
        print(f"❌ Erreur : {result['error']}")

def exemple_dossier():
    """Exemple de traitement d'un dossier complet."""
    
    pipeline = DataCleaningPipeline()
    
    # Traiter tous les fichiers d'un dossier
    result = pipeline.process_directory(
        input_dir="data/raw/",
        output_dir="data/cleaned/"
    )
    
    print(f"\n📁 Traitement de dossier terminé :")
    print(f"├── Fichiers traités : {result['total_files']}")
    print(f"├── Succès : {result['successful']}")
    print(f"├── Échecs : {result['failed']}")
    print(f"└── Temps total : {result['total_processing_time']:.2f}s")

def exemple_configuration_avancee():
    """Exemple avec configuration avancée."""
    
    # Configuration personnalisée
    config_avancee = {
        'missing_values': {
            'strategy': 'mean',
            'fill_value': 0,
            'drop_threshold': 0.8  # Supprimer colonnes avec >80% manquant
        },
        'outliers': {
            'method': 'zscore',
            'zscore_threshold': 2.5  # Plus strict
        },
        'duplicates': {
            'keep': 'last',  # Garder le dernier doublon
            'subset': ['nom', 'email']  # Doublons basés sur nom+email
        },
        'standardization': {
            'text_lowercase': True,
            'text_strip': True,
            'date_format': '%Y-%m-%d',
            'normalize_spaces': True
        }
    }
    
    # Pipeline avec config personnalisée
    pipeline = DataCleaningPipeline(config=config_avancee)
    
    result = pipeline.process_file(
        input_path="data/raw/sample_messy_data.csv",
        output_path="data/cleaned/sample_advanced_clean.csv"
    )
    
    print(f"\n🔧 Configuration avancée appliquée")
    print(f"Résultat : {'✅ Succès' if result['success'] else '❌ Échec'}")

if __name__ == "__main__":
    print("🧹 EXEMPLES D'UTILISATION DU PIPELINE DE NETTOYAGE")
    print("=" * 60)
    
    # Créer les dossiers nécessaires
    Path("data/cleaned").mkdir(parents=True, exist_ok=True)
    
    # Exemples
    print("\n1️⃣ Exemple basique")
    exemple_basique()
    
    print("\n2️⃣ Exemple dossier")
    exemple_dossier()
    
    print("\n3️⃣ Exemple configuration avancée")
    exemple_configuration_avancee()
    
    print("\n🎉 Tous les exemples terminés !")
    print("📁 Vérifiez le dossier 'data/cleaned/' pour les résultats")
    print("📋 Les rapports sont générés automatiquement")