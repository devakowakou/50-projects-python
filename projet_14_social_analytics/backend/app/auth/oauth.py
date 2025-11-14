"""Authentification OAuth2 pour Instagram et TikTok."""

from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
import httpx
from urllib.parse import urlencode
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from shared.config import settings, INSTAGRAM_SCOPES, TIKTOK_SCOPES


class InstagramOAuth:
    """Gestionnaire OAuth2 pour Instagram."""
    
    @staticmethod
    def get_auth_url(state: str = None) -> str:
        """Générer l'URL d'autorisation Instagram."""
        params = {
            "client_id": settings.INSTAGRAM_APP_ID,
            "redirect_uri": settings.INSTAGRAM_REDIRECT_URI,
            "scope": ",".join(INSTAGRAM_SCOPES),
            "response_type": "code"
        }
        if state:
            params["state"] = state
            
        return f"https://www.facebook.com/v18.0/dialog/oauth?{urlencode(params)}"
    
    @staticmethod
    async def exchange_code_for_token(code: str) -> dict:
        """Échanger le code d'autorisation contre un token."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://graph.facebook.com/v18.0/oauth/access_token",
                data={
                    "client_id": settings.INSTAGRAM_APP_ID,
                    "client_secret": settings.INSTAGRAM_APP_SECRET,
                    "redirect_uri": settings.INSTAGRAM_REDIRECT_URI,
                    "code": code
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to exchange code for token")
                
            return response.json()
    
    @staticmethod
    async def get_user_info(access_token: str) -> dict:
        """Récupérer les informations utilisateur Instagram."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://graph.facebook.com/v18.0/me",
                params={
                    "fields": "id,name,accounts{instagram_business_account{id,username}}",
                    "access_token": access_token
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get user info")
                
            return response.json()


class TikTokOAuth:
    """Gestionnaire OAuth2 pour TikTok."""
    
    @staticmethod
    def get_auth_url(state: str = None) -> str:
        """Générer l'URL d'autorisation TikTok."""
        params = {
            "client_key": settings.TIKTOK_CLIENT_KEY,
            "redirect_uri": settings.TIKTOK_REDIRECT_URI,
            "scope": ",".join(TIKTOK_SCOPES),
            "response_type": "code"
        }
        if state:
            params["state"] = state
            
        return f"https://www.tiktok.com/auth/authorize/?{urlencode(params)}"
    
    @staticmethod
    async def exchange_code_for_token(code: str) -> dict:
        """Échanger le code d'autorisation contre un token."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://open-api.tiktok.com/oauth/access_token/",
                json={
                    "client_key": settings.TIKTOK_CLIENT_KEY,
                    "client_secret": settings.TIKTOK_CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code"
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to exchange code for token")
                
            return response.json()
    
    @staticmethod
    async def get_user_info(access_token: str) -> dict:
        """Récupérer les informations utilisateur TikTok."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://open-api.tiktok.com/user/info/",
                json={
                    "access_token": access_token,
                    "fields": ["open_id", "union_id", "avatar_url", "display_name"]
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get user info")
                
            return response.json()