import random
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
URLS = [
    '/', '/home', '/login', '/dashboard', '/api/users', '/api/data', 
    '/api/products', '/api/orders', '/profile', '/settings',
    '/static/app.js', '/static/style.css', '/admin', '/logout'
]

METHODS = {
    'GET': 0.7,     # 70% GET
    'POST': 0.2,    # 20% POST
    'PUT': 0.05,    # 5% PUT
    'DELETE': 0.05  # 5% DELETE
}

STATUS_CODES = {
    200: 0.75,   # 75% success
    201: 0.05,
    304: 0.05,
    400: 0.03,
    401: 0.02,
    404: 0.07,   # 7% not found
    500: 0.02,   # 2% server error
    503: 0.01
}

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'curl/7.68.0',
    'Python-requests/2.28.0'
]

def weighted_choice(choices: dict):
    """Choix pondéré"""
    return random.choices(list(choices.keys()), weights=list(choices.values()))[0]

def generate_ip():
    """Génère une IP aléatoire"""
    return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

def generate_log_line(timestamp: datetime) -> str:
    """Génère une ligne de log Apache format"""
    ip = generate_ip()
    ts_str = timestamp.strftime('%d/%b/%Y:%H:%M:%S +0000')
    method = weighted_choice(METHODS)
    url = random.choice(URLS)
    status = weighted_choice(STATUS_CODES)
    size = random.randint(100, 50000)
    ua = random.choice(USER_AGENTS)
    response_time = random.randint(10, 2000) if status != 500 else random.randint(2000, 10000)
    
    return f'{ip} - - [{ts_str}] "{method} {url} HTTP/1.1" {status} {size} "-" "{ua}" {response_time}\n'

def main():
    """Génère des logs de test"""
    output_path = Path(__file__).parent.parent / 'data' / 'raw_logs' / 'access.log'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    num_logs = 5000  # Nombre de logs à générer
    now = datetime.now()
    
    print(f"🔄 Génération de {num_logs} logs...")
    
    with open(output_path, 'w') as f:
        for i in range(num_logs):
            # Distribution sur les 7 derniers jours
            hours_ago = random.randint(0, 24 * 7)
            timestamp = now - timedelta(hours=hours_ago)
            f.write(generate_log_line(timestamp))
            
            if (i + 1) % 1000 == 0:
                print(f"  ✓ {i + 1}/{num_logs} logs générés")
    
    print(f"✅ Fichier créé: {output_path}")
    print(f"📊 {num_logs} lignes de logs générées")

if __name__ == '__main__':
    main()
