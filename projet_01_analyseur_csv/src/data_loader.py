"""
Module de chargement et validation des fichiers CSV
Responsabilité: Charger, détecter l'encodage et valider les données
"""

import pandas as pd
import streamlit as st
from typing import Optional, Tuple
import chardet
import io


class DataLoader:
    """Classe pour charger et valider les fichiers CSV"""
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.file_info = {}
    
    def detect_encoding(self, file_bytes: bytes) -> str:
        """
        Détecte l'encodage du fichier
        
        Args:
            file_bytes: Contenu du fichier en bytes
            
        Returns:
            str: Encodage détecté
        """
        result = chardet.detect(file_bytes)
        return result['encoding'] or 'utf-8'
    
    def load_from_upload(self, uploaded_file) -> Tuple[bool, str]:
        """
        Charge un fichier depuis l'upload Streamlit
        
        Args:
            uploaded_file: Fichier uploadé par Streamlit
            
        Returns:
            Tuple[bool, str]: (Succès, Message)
        """
        try:
            # Lire le contenu du fichier
            file_bytes = uploaded_file.read()
            
            # Détecter l'encodage
            encoding = self.detect_encoding(file_bytes)
            
            # Réinitialiser le pointeur du fichier
            uploaded_file.seek(0)
            
            # Charger selon le type de fichier
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                self.df = pd.read_csv(
                    io.BytesIO(file_bytes),
                    encoding=encoding,
                    encoding_errors='ignore'
                )
            elif file_extension in ['xlsx', 'xls']:
                self.df = pd.read_excel(io.BytesIO(file_bytes))
            else:
                return False, f"❌ Format non supporté: {file_extension}"
            
            # Stocker les informations du fichier
            self.file_info = {
                'nom': uploaded_file.name,
                'taille': f"{uploaded_file.size / 1024:.2f} KB",
                'encodage': encoding,
                'lignes': len(self.df),
                'colonnes': len(self.df.columns)
            }
            
            return True, "✅ Fichier chargé avec succès"
            
        except Exception as e:
            return False, f"❌ Erreur lors du chargement: {str(e)}"
    
    def load_from_path(self, file_path: str, encoding: str = 'utf-8') -> Tuple[bool, str]:
        """
        Charge un fichier depuis un chemin
        
        Args:
            file_path: Chemin du fichier
            encoding: Encodage du fichier
            
        Returns:
            Tuple[bool, str]: (Succès, Message)
        """
        try:
            if file_path.endswith('.csv'):
                self.df = pd.read_csv(file_path, encoding=encoding)
            elif file_path.endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(file_path)
            else:
                return False, "❌ Format non supporté"
            
            self.file_info = {
                'nom': file_path.split('/')[-1],
                'encodage': encoding,
                'lignes': len(self.df),
                'colonnes': len(self.df.columns)
            }
            
            return True, "✅ Fichier chargé avec succès"
            
        except FileNotFoundError:
            return False, "❌ Fichier introuvable"
        except Exception as e:
            return False, f"❌ Erreur: {str(e)}"
    
    def validate_data(self) -> Tuple[bool, list]:
        """
        Valide les données chargées
        
        Returns:
            Tuple[bool, list]: (Valide, Liste des avertissements)
        """
        warnings = []
        
        if self.df is None:
            return False, ["Aucune donnée chargée"]
        
        if self.df.empty:
            return False, ["Le fichier est vide"]
        
        # Vérifier les colonnes vides
        empty_cols = self.df.columns[self.df.isnull().all()].tolist()
        if empty_cols:
            warnings.append(f"Colonnes entièrement vides: {', '.join(empty_cols)}")
        
        # Vérifier le pourcentage de valeurs manquantes
        missing_percent = (self.df.isnull().sum() / len(self.df) * 100)
        high_missing = missing_percent[missing_percent > 50].index.tolist()
        if high_missing:
            warnings.append(f"Colonnes avec >50% de valeurs manquantes: {', '.join(high_missing)}")
        
        # Vérifier les colonnes numériques
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        if len(numeric_cols) == 0:
            warnings.append("⚠️ Aucune colonne numérique détectée")
        
        return True, warnings
    
    def get_data(self) -> Optional[pd.DataFrame]:
        """Retourne le DataFrame chargé"""
        return self.df
    
    def get_file_info(self) -> dict:
        """Retourne les informations du fichier"""
        return self.file_info
    
    def get_column_types(self) -> dict:
        """
        Retourne les types de colonnes détectés
        
        Returns:
            dict: Dictionnaire avec les types de colonnes
        """
        if self.df is None:
            return {}
        
        return {
            'numeriques': self.df.select_dtypes(include=['number']).columns.tolist(),
            'categoriques': self.df.select_dtypes(include=['object', 'category']).columns.tolist(),
            'dates': self.df.select_dtypes(include=['datetime']).columns.tolist(),
            'autres': self.df.select_dtypes(exclude=['number', 'object', 'category', 'datetime']).columns.tolist()
        }
