"""
Gestionnaire de données pour les transactions
Gère le CRUD (Create, Read, Update, Delete) en JSON
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import uuid
import pandas as pd

class DataManager:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Crée le fichier s'il n'existe pas"""
        if not os.path.exists(self.data_file):
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            self._save_data([])
    
    def _load_data(self) -> List[Dict]:
        """Charge les transactions depuis le JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_data(self, data: List[Dict]):
        """Sauvegarde les transactions dans le JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_transaction(self, transaction: Dict) -> str:
        """
        Ajoute une nouvelle transaction
        Returns: ID de la transaction
        """
        data = self._load_data()
        
        # Générer un ID unique si non fourni
        if 'id' not in transaction:
            transaction['id'] = str(uuid.uuid4())
        
        # Ajouter timestamp de création
        transaction['created_at'] = datetime.now().isoformat()
        
        data.append(transaction)
        self._save_data(data)
        return transaction['id']
    
    def get_all_transactions(self) -> List[Dict]:
        """Récupère toutes les transactions"""
        return self._load_data()
    
    def get_transaction(self, transaction_id: str) -> Optional[Dict]:
        """Récupère une transaction par ID"""
        data = self._load_data()
        for transaction in data:
            if transaction.get('id') == transaction_id:
                return transaction
        return None
    
    def update_transaction(self, transaction_id: str, updated_data: Dict) -> bool:
        """
        Met à jour une transaction
        Returns: True si succès, False sinon
        """
        data = self._load_data()
        for i, transaction in enumerate(data):
            if transaction.get('id') == transaction_id:
                # Garder l'ID et la date de création
                updated_data['id'] = transaction_id
                updated_data['created_at'] = transaction.get('created_at')
                updated_data['updated_at'] = datetime.now().isoformat()
                data[i] = updated_data
                self._save_data(data)
                return True
        return False
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """
        Supprime une transaction
        Returns: True si succès, False sinon
        """
        data = self._load_data()
        initial_length = len(data)
        data = [t for t in data if t.get('id') != transaction_id]
        
        if len(data) < initial_length:
            self._save_data(data)
            return True
        return False
    
    def get_transactions_dataframe(self) -> pd.DataFrame:
        """Retourne les transactions sous forme de DataFrame Pandas"""
        data = self._load_data()
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        
        # Convertir la date en datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date', ascending=False)
        
        # Convertir le montant en float
        if 'montant' in df.columns:
            df['montant'] = pd.to_numeric(df['montant'], errors='coerce')
        
        return df
    
    def import_from_csv(self, csv_file_path: str) -> int:
        """
        Importe des transactions depuis un CSV
        Returns: Nombre de transactions importées
        """
        try:
            df = pd.read_csv(csv_file_path)
            required_columns = ['date', 'type', 'montant', 'categorie']
            
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Le CSV doit contenir les colonnes: {required_columns}")
            
            count = 0
            for _, row in df.iterrows():
                transaction = {
                    'date': str(row['date']),
                    'type': str(row['type']),
                    'montant': float(row['montant']),
                    'categorie': str(row['categorie']),
                    'description': str(row.get('description', '')),
                    'mode_paiement': str(row.get('mode_paiement', 'Carte Bancaire'))
                }
                self.add_transaction(transaction)
                count += 1
            
            return count
        except Exception as e:
            raise Exception(f"Erreur lors de l'import CSV: {str(e)}")
    
    def export_to_csv(self, output_path: str) -> str:
        """
        Exporte les transactions vers un CSV
        Returns: Chemin du fichier créé
        """
        df = self.get_transactions_dataframe()
        if df.empty:
            raise ValueError("Aucune transaction à exporter")
        
        # Sélectionner les colonnes à exporter
        export_columns = ['date', 'type', 'montant', 'categorie', 'description', 'mode_paiement']
        df_export = df[[col for col in export_columns if col in df.columns]]
        
        df_export.to_csv(output_path, index=False, encoding='utf-8')
        return output_path
    
    def export_to_json(self, output_path: str) -> str:
        """
        Exporte les transactions vers un JSON
        Returns: Chemin du fichier créé
        """
        data = self._load_data()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return output_path
    
    def clear_all_transactions(self) -> bool:
        """Supprime toutes les transactions"""
        self._save_data([])
        return True
