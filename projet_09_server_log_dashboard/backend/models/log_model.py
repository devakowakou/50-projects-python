from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class LogEntryBase(BaseModel):
    """Schéma de base pour une entrée de log"""
    ip: str = Field(..., description="Adresse IP du client")
    timestamp: datetime = Field(..., description="Date et heure de la requête")
    method: str = Field(..., description="Méthode HTTP (GET, POST, etc.)")
    url: str = Field(..., description="URL demandée")
    status_code: int = Field(..., ge=100, le=599, description="Code de statut HTTP")
    response_time: Optional[float] = Field(None, description="Temps de réponse en ms")
    user_agent: str = Field(..., description="User-Agent du navigateur")

class LogEntryCreate(LogEntryBase):
    """Schéma pour créer un log"""
    pass

class LogEntryResponse(LogEntryBase):
    """Schéma de réponse incluant l'ID"""
    id: int
    
    class Config:
        from_attributes = True

class StatsOverview(BaseModel):
    """Statistiques globales"""
    total_requests: int
    unique_ips: int
    errors_4xx: int
    errors_5xx: int
    error_rate: float
    avg_response_time: Optional[float]
    date_range: dict
