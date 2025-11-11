import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import json
from io import StringIO

sys.path.append(str(Path(__file__).parent.parent))

from utils.api_client import APIClient

st.set_page_config(page_title="Export de Rapports", page_icon="📥", layout="wide")

st.title("📥 Export de Rapports")

api = APIClient()

st.info("📊 Exportez vos analyses en format CSV/JSON pour traitement externe (sans limite de volume)")

col1, col2 = st.columns(2)

with col1:
    hours = st.number_input("Période (heures)", 1, 720, 24, help="Max 30 jours (720h)")

with col2:
    export_format = st.selectbox("Format", ["CSV", "JSON"])

if st.button("🚀 Générer le rapport", type="primary"):
    with st.spinner("📦 Génération en cours..."):
        try:
            # Appeler l'API d'export
            data = api.export_logs(hours=hours, format=export_format.lower())
            
            if export_format == "CSV":
                # data est déjà le contenu CSV
                filename = f"rapport_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                
                st.download_button(
                    label="⬇️ Télécharger le rapport CSV",
                    data=data,
                    file_name=filename,
                    mime="text/csv"
                )
                
                # Compter les lignes
                lines = data.strip().split('\n')
                total = len(lines) - 1  # -1 pour le header
                
                st.success(f"✅ {total:,} logs exportés avec succès !")
                
                # Preview
                st.subheader("👀 Aperçu des données (20 premières lignes)")
                df = pd.read_csv(StringIO(data))
                st.dataframe(df.head(20), use_container_width=True)
                
                # Stats rapides
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Total lignes", f"{len(df):,}")
                with col_b:
                    st.metric("IPs uniques", f"{df['ip'].nunique():,}")
                with col_c:
                    st.metric("Période", f"{hours}h")
            
            else:  # JSON
                # data est un dict
                json_str = json.dumps(data, indent=2)
                filename = f"rapport_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                
                st.download_button(
                    label="⬇️ Télécharger le rapport JSON",
                    data=json_str,
                    file_name=filename,
                    mime="application/json"
                )
                
                st.success(f"✅ {data['total']:,} logs exportés avec succès !")
                
                # Métadonnées
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Total logs", f"{data['total']:,}")
                with col_b:
                    st.metric("Période", f"{data['period_hours']}h")
                with col_c:
                    st.metric("Date export", data['export_date'][:10])
                
                # Preview JSON (5 premiers logs)
                st.subheader("👀 Aperçu JSON (5 premiers logs)")
                st.json(data['logs'][:5])
            
        except Exception as e:
            st.error(f"❌ Erreur lors de l'export: {e}")
            st.exception(e)

st.markdown("---")

st.markdown("""
### 📋 Informations sur l'export

- **CSV** : Format tabulaire, idéal pour Excel/Pandas
- **JSON** : Format structuré, idéal pour API/scripts
- **Volume** : Aucune limite stricte, tous les logs de la période
- **Performance** : Optimisé pour gros volumes via requêtes SQL directes

### 💡 Cas d'usage

1. **Analyse externe** : Import dans Excel, Tableau, Power BI
2. **Archivage** : Sauvegarde périodique des logs
3. **Machine Learning** : Datasets pour entraînement de modèles
4. **Audit** : Génération de rapports de conformité
""")
