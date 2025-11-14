"""Endpoints d'authentification."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from shared.database import get_db, User, SocialAccount
from backend.app.auth.oauth import InstagramOAuth, TikTokOAuth

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/instagram/login")
async def instagram_login():
    """Rediriger vers l'authentification Instagram."""
    auth_url = InstagramOAuth.get_auth_url(state="instagram_auth")
    return RedirectResponse(url=auth_url)


@router.get("/instagram/callback")
async def instagram_callback(code: str, state: str = None, db: Session = Depends(get_db)):
    """Callback Instagram OAuth2."""
    try:
        # Échanger le code contre un token
        token_data = await InstagramOAuth.exchange_code_for_token(code)
        access_token = token_data.get("access_token")
        
        # Récupérer les infos utilisateur
        user_info = await InstagramOAuth.get_user_info(access_token)
        
        # Créer ou récupérer l'utilisateur
        user = db.query(User).filter(User.email == "demo@socialanalytics.com").first()
        if not user:
            user = User(email="demo@socialanalytics.com")
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Créer ou mettre à jour le compte Instagram
        instagram_accounts = user_info.get("accounts", {}).get("data", [])
        for account in instagram_accounts:
            ig_account = account.get("instagram_business_account")
            if ig_account:
                social_account = db.query(SocialAccount).filter(
                    SocialAccount.user_id == user.id,
                    SocialAccount.platform == "instagram",
                    SocialAccount.account_id == ig_account["id"]
                ).first()
                
                if not social_account:
                    social_account = SocialAccount(
                        user_id=user.id,
                        platform="instagram",
                        account_id=ig_account["id"],
                        username=ig_account["username"],
                        access_token=access_token,
                        is_active=True
                    )
                    db.add(social_account)
                else:
                    social_account.access_token = access_token
                    social_account.is_active = True
        
        db.commit()
        return {"message": "Instagram account connected successfully", "user_info": user_info}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Instagram authentication failed: {str(e)}")


@router.get("/tiktok/login")
async def tiktok_login():
    """Rediriger vers l'authentification TikTok."""
    auth_url = TikTokOAuth.get_auth_url(state="tiktok_auth")
    return RedirectResponse(url=auth_url)


@router.get("/tiktok/callback")
async def tiktok_callback(code: str, state: str = None, db: Session = Depends(get_db)):
    """Callback TikTok OAuth2."""
    try:
        # Échanger le code contre un token
        token_data = await TikTokOAuth.exchange_code_for_token(code)
        access_token = token_data.get("data", {}).get("access_token")
        
        # Récupérer les infos utilisateur
        user_info = await TikTokOAuth.get_user_info(access_token)
        
        # Créer ou récupérer l'utilisateur
        user = db.query(User).filter(User.email == "demo@socialanalytics.com").first()
        if not user:
            user = User(email="demo@socialanalytics.com")
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Créer ou mettre à jour le compte TikTok
        tiktok_data = user_info.get("data", {}).get("user", {})
        if tiktok_data:
            social_account = db.query(SocialAccount).filter(
                SocialAccount.user_id == user.id,
                SocialAccount.platform == "tiktok",
                SocialAccount.account_id == tiktok_data.get("open_id")
            ).first()
            
            if not social_account:
                social_account = SocialAccount(
                    user_id=user.id,
                    platform="tiktok",
                    account_id=tiktok_data.get("open_id"),
                    username=tiktok_data.get("display_name"),
                    access_token=access_token,
                    is_active=True
                )
                db.add(social_account)
            else:
                social_account.access_token = access_token
                social_account.is_active = True
        
        db.commit()
        return {"message": "TikTok account connected successfully", "user_info": user_info}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"TikTok authentication failed: {str(e)}")


@router.get("/status")
async def auth_status(db: Session = Depends(get_db)):
    """Vérifier le statut d'authentification."""
    user = db.query(User).filter(User.email == "demo@socialanalytics.com").first()
    if not user:
        return {"authenticated": False, "accounts": []}
    
    accounts = db.query(SocialAccount).filter(
        SocialAccount.user_id == user.id,
        SocialAccount.is_active == True
    ).all()
    
    return {
        "authenticated": True,
        "accounts": [
            {
                "platform": account.platform,
                "username": account.username,
                "connected_at": account.created_at
            }
            for account in accounts
        ]
    }