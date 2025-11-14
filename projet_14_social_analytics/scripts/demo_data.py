"""Script pour générer des données de démonstration."""

import sys
import os
from datetime import datetime, timedelta
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.database import SessionLocal, User, SocialAccount, SocialInsight, Post, create_tables


def generate_demo_data():
    """Générer des données de démonstration."""
    
    # Créer les tables
    create_tables()
    
    db = SessionLocal()
    
    try:
        # Créer un utilisateur de démo
        demo_user = User(email="demo@socialanalytics.com")
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        
        # Créer des comptes sociaux
        instagram_account = SocialAccount(
            user_id=demo_user.id,
            platform="instagram",
            account_id="demo_instagram_123",
            username="demo_instagram",
            access_token="demo_token_instagram",
            is_active=True
        )
        
        tiktok_account = SocialAccount(
            user_id=demo_user.id,
            platform="tiktok", 
            account_id="demo_tiktok_456",
            username="demo_tiktok",
            access_token="demo_token_tiktok",
            is_active=True
        )
        
        db.add(instagram_account)
        db.add(tiktok_account)
        db.commit()
        db.refresh(instagram_account)
        db.refresh(tiktok_account)
        
        # Générer des insights quotidiens (30 derniers jours)
        base_date = datetime.now() - timedelta(days=30)
        
        for i in range(30):
            current_date = base_date + timedelta(days=i)
            
            # Instagram insights
            instagram_insight = SocialInsight(
                account_id=instagram_account.id,
                date=current_date,
                followers_count=15000 + i * 20 + random.randint(-10, 30),
                following_count=1200 + random.randint(-5, 10),
                posts_count=150 + i,
                reach=8000 + random.randint(1000, 3000),
                impressions=12000 + random.randint(2000, 5000),
                profile_views=500 + random.randint(50, 200),
                website_clicks=25 + random.randint(0, 15)
            )
            
            # TikTok insights
            tiktok_insight = SocialInsight(
                account_id=tiktok_account.id,
                date=current_date,
                followers_count=8500 + i * 15 + random.randint(-8, 25),
                posts_count=80 + i,
                video_views=45000 + random.randint(5000, 15000),
                likes_count=2200 + random.randint(200, 800),
                comments_count=180 + random.randint(20, 100),
                shares_count=95 + random.randint(10, 50)
            )
            
            db.add(instagram_insight)
            db.add(tiktok_insight)
        
        # Générer des posts Instagram
        instagram_posts = [
            {
                "caption": "Belle journée pour une photo ! 📸 #photography #lifestyle",
                "media_type": "IMAGE",
                "likes": 1250, "comments": 85, "shares": 25, "saves": 45
            },
            {
                "caption": "Nouveau reel en ligne ! 🎬 Qu'est-ce que vous en pensez ?",
                "media_type": "VIDEO", 
                "likes": 1850, "comments": 120, "shares": 65, "saves": 80
            },
            {
                "caption": "Carousel de mes photos préférées 📷✨",
                "media_type": "CAROUSEL_ALBUM",
                "likes": 980, "comments": 62, "shares": 18, "saves": 35
            },
            {
                "caption": "Story highlights mis à jour ! 💫",
                "media_type": "IMAGE",
                "likes": 720, "comments": 45, "shares": 12, "saves": 28
            },
            {
                "caption": "Collaboration avec @brand 🤝 #sponsored",
                "media_type": "VIDEO",
                "likes": 1100, "comments": 78, "shares": 22, "saves": 42
            }
        ]
        
        for i, post_data in enumerate(instagram_posts):
            post_date = datetime.now() - timedelta(days=random.randint(1, 15))
            
            post = Post(
                account_id=instagram_account.id,
                platform_post_id=f"ig_post_{i+1}",
                caption=post_data["caption"],
                media_type=post_data["media_type"],
                timestamp=post_date,
                likes_count=post_data["likes"],
                comments_count=post_data["comments"],
                shares_count=post_data["shares"],
                saves_count=post_data["saves"],
                reach=post_data["likes"] * 3,
                impressions=post_data["likes"] * 5
            )
            db.add(post)
        
        # Générer des vidéos TikTok
        tiktok_videos = [
            {
                "caption": "Danse tendance du moment ! 💃 #dance #trending",
                "likes": 2100, "comments": 150, "shares": 85, "views": 25000
            },
            {
                "caption": "Astuce du jour 💡 #tips #lifehack",
                "likes": 1650, "comments": 95, "shares": 45, "views": 18000
            },
            {
                "caption": "Réaction à la nouvelle tendance 😂",
                "likes": 3200, "comments": 220, "shares": 120, "views": 42000
            },
            {
                "caption": "Behind the scenes 🎬 #bts",
                "likes": 890, "comments": 65, "shares": 25, "views": 12000
            },
            {
                "caption": "Collaboration TikTok 🤝 #collab",
                "likes": 1450, "comments": 88, "shares": 55, "views": 20000
            }
        ]
        
        for i, video_data in enumerate(tiktok_videos):
            video_date = datetime.now() - timedelta(days=random.randint(1, 12))
            
            video = Post(
                account_id=tiktok_account.id,
                platform_post_id=f"tt_video_{i+1}",
                caption=video_data["caption"],
                media_type="VIDEO",
                timestamp=video_date,
                likes_count=video_data["likes"],
                comments_count=video_data["comments"],
                shares_count=video_data["shares"],
                video_views=video_data["views"],
                play_time=random.uniform(15.0, 45.0),
                completion_rate=random.uniform(0.6, 0.9)
            )
            db.add(video)
        
        db.commit()
        print("✅ Données de démonstration générées avec succès !")
        print(f"👤 Utilisateur créé: {demo_user.email}")
        print(f"📱 Comptes sociaux: Instagram (@{instagram_account.username}), TikTok (@{tiktok_account.username})")
        print(f"📊 30 jours d'insights générés")
        print(f"📝 {len(instagram_posts)} posts Instagram et {len(tiktok_videos)} vidéos TikTok créés")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération des données: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    generate_demo_data()