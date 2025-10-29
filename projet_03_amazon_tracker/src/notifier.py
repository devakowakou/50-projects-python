"""
Module de notification par email
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config


class EmailNotifier:
    """Gestionnaire des notifications par email"""
    
    def __init__(self):
        """Initialise le notifier"""
        self.email = config.SMTP_EMAIL
        self.password = config.SMTP_PASSWORD
        self.host = config.SMTP_HOST
        self.port = config.SMTP_PORT
    
    def send_price_alert(self, product_name, current_price, target_price, product_url):
        """
        Envoie une alerte par email
        
        Args:
            product_name: Nom du produit
            current_price: Prix actuel
            target_price: Prix cible
            product_url: URL du produit
            
        Returns:
            True si succès, False sinon
        """
        if not self.email or not self.password:
            print("⚠️  Configuration email manquante")
            return False
        
        try:
            # Calculer les économies
            savings = target_price - current_price
            
            # Créer le message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email
            msg['To'] = self.email  # Envoyer à soi-même pour MVP
            msg['Subject'] = config.EMAIL_SUBJECT.format(product_name=product_name)
            
            # Corps HTML
            html_body = config.EMAIL_TEMPLATE.format(
                product_name=product_name,
                current_price=f"{current_price:.2f}",
                target_price=f"{target_price:.2f}",
                savings=f"{savings:.2f}",
                product_url=product_url
            )
            
            # Attacher le corps HTML
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Envoyer l'email
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            print(f"✅ Email envoyé pour {product_name}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("❌ Erreur d'authentification email")
            return False
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi de l'email: {e}")
            return False
    
    def send_multiple_alerts(self, alerts):
        """
        Envoie plusieurs alertes groupées
        
        Args:
            alerts: Liste de dicts avec les infos des produits
            
        Returns:
            Nombre d'emails envoyés avec succès
        """
        success_count = 0
        
        for alert in alerts:
            if self.send_price_alert(
                alert['name'],
                alert['current_price'],
                alert['target_price'],
                alert['url']
            ):
                success_count += 1
        
        return success_count
    
    def test_connection(self):
        """
        Test la connexion au serveur SMTP
        
        Returns:
            True si connexion réussie, False sinon
        """
        if not self.email or not self.password:
            return False
        
        try:
            with smtplib.SMTP(self.host, self.port, timeout=5) as server:
                server.starttls()
                server.login(self.email, self.password)
            return True
        except Exception as e:
            print(f"❌ Test de connexion échoué: {e}")
            return False
