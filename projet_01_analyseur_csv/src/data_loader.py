"""
Module de chargement et validation des fichiers CSV
Responsabilité: Charger, détecter l'encodage et valider les données
Version 2.2 - Optimisée pour gros fichiers
"""

import pandas as pd
import streamlit as st
from typing import Optional, Tuple
import chardet
import io


class DataLoader:
    """Classe pour charger et valider les fichiers CSV (Version Optimisée)"""
    
    # Constantes d'optimisation
    SAMPLE_SIZE = 10000  # 10 KB pour détection encodage
    CHUNK_THRESHOLD = 10_000_000  # 10 MB - seuil pour chargement par chunks
    MAX_FILE_SIZE = 500_000_000  # 500 MB - taille maximale
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.file_info = {}
    
    def detect_encoding(self, file_bytes: bytes) -> str:
        """
        Détecte l'encodage du fichier (optimisé - échantillon seulement)
        
        Args:
            file_bytes: Contenu du fichier en bytes (ou échantillon)
            
        Returns:
            str: Encodage détecté
        """
        # Utiliser seulement un échantillon pour détecter l'encodage
        sample = file_bytes[:self.SAMPLE_SIZE] if len(file_bytes) > self.SAMPLE_SIZE else file_bytes
        result = chardet.detect(sample)
        return result['encoding'] or 'utf-8'
    
    def load_from_upload(self, uploaded_file) -> Tuple[bool, str]:
        """
        Charge un fichier depuis l'upload Streamlit (optimisé)
        
        Args:
            uploaded_file: Fichier uploadé par Streamlit
            
        Returns:
            Tuple[bool, str]: (Succès, Message)
        """
        try:
            # Vérifier la taille du fichier
            if uploaded_file.size > self.MAX_FILE_SIZE:
                return False, f" Fichier trop volumineux ({uploaded_file.size / 1_000_000:.1f} MB). Maximum: {self.MAX_FILE_SIZE / 1_000_000:.0f} MB"
            
            # Lire le contenu du fichier UNE SEULE FOIS
            file_bytes = uploaded_file.read()
            
            # Détecter l'encodage sur échantillon seulement
            encoding = self.detect_encoding(file_bytes)
            
            # Déterminer le type de fichier
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            # Créer un BytesIO pour éviter de relire
            file_io = io.BytesIO(file_bytes)
            
            # Chargement optimisé selon taille
            if file_extension == 'csv':
                if uploaded_file.size > self.CHUNK_THRESHOLD:
                    # Gros fichier : charger par chunks avec barre de progression
                    with st.spinner(f"Chargement d'un gros fichier ({uploaded_file.size / 1_000_000:.1f} MB)..."):
                        chunks = []
                        chunk_size = 50000  # 50K lignes par chunk
                        
                        for chunk in pd.read_csv(
                            file_io,
                            encoding=encoding,
                            encoding_errors='ignore',
                            chunksize=chunk_size
                        ):
                            chunks.append(chunk)
                        
                        self.df = pd.concat(chunks, ignore_index=True)
                else:
                    # Petit fichier : chargement normal
                    self.df = pd.read_csv(
                        file_io,
                        encoding=encoding,
                        encoding_errors='ignore'
                    )
            elif file_extension in ['xlsx', 'xls']:
                # Excel ne supporte pas chunksize
                if uploaded_file.size > self.CHUNK_THRESHOLD:
                    with st.spinner(f"Chargement d'un gros fichier Excel ({uploaded_file.size / 1_000_000:.1f} MB)..."):
                        self.df = pd.read_excel(file_io)
                else:
                    self.df = pd.read_excel(file_io)
            else:
                return False, f" Format non supporté: {file_extension}"
            
            # Stocker les informations du fichier
            self.file_info = {
                'nom': uploaded_file.name,
                'taille': f"{uploaded_file.size / 1024:.2f} KB",
                'encodage': encoding,
                'lignes': len(self.df),
                'colonnes': len(self.df.columns),
                'memoire': f"{self.df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
            }
            
            return True, " Fichier chargé avec succès"
            
        except MemoryError:
            return False, " Mémoire insuffisante pour charger ce fichier"
        except Exception as e:
            return False, f" Erreur lors du chargement: {str(e)}"
    
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
                return False, " Format non supporté"
            
            self.file_info = {
                'nom': file_path.split('/')[-1],
                'encodage': encoding,
                'lignes': len(self.df),
                'colonnes': len(self.df.columns)
            }
            
            return True, " Fichier chargé avec succès"
            
        except FileNotFoundError:
            return False, " Fichier introuvable"
        except Exception as e:
            return False, f" Erreur: {str(e)}"
    
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
            warnings.append(" Aucune colonne numérique détectée")
        
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
