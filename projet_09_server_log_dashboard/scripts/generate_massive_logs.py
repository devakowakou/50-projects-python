import random
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

URLS = [
    '/', '/home', '/login', '/dashboard', '/api/users', '/api/data', 
    '/api/products', '/api/orders', '/profile', '/settings',
    '/static/app.js', '/static/style.css', '/admin', '/logout',
    '/search', '/cart', '/checkout', '/payment', '/api/auth',
    '/api/recommendations', '/api/analytics', '/docs', '/help'
]

METHODS = {'GET': 0.7, 'POST': 0.2, 'PUT': 0.05, 'DELETE': 0.05}
STATUS_CODES = {200: 0.75, 201: 0.05, 304: 0.05, 400: 0.03, 401: 0.02, 404: 0.07, 500: 0.02, 503: 0.01}
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
    'curl/7.68.0',
    'Python-requests/2.28.0',
    'PostmanRuntime/7.29.0'
]

# Pool d'IPs réalistes (simule des utilisateurs récurrents)
IP_POOL = [f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}" 
           for _ in range(10000)]

def weighted_choice(choices: dict):
    return random.choices(list(choices.keys()), weights=list(choices.values()))[0]

def generate_log_batch(batch_size: int, start_time: datetime) -> list:
    """Génère un batch de logs"""
    logs = []
    for i in range(batch_size):
        ip = random.choice(IP_POOL)
        hours_ago = random.randint(0, 24 * 30)  # 30 jours de logs
        timestamp = start_time - timedelta(hours=hours_ago, minutes=random.randint(0,59), seconds=random.randint(0,59))
        ts_str = timestamp.strftime('%d/%b/%Y:%H:%M:%S +0000')
        method = weighted_choice(METHODS)
        url = random.choice(URLS)
        status = weighted_choice(STATUS_CODES)
        size = random.randint(100, 50000)
        ua = random.choice(USER_AGENTS)
        response_time = random.randint(10, 2000) if status != 500 else random.randint(2000, 10000)
        
        logs.append(f'{ip} - - [{ts_str}] "{method} {url} HTTP/1.1" {status} {size} "-" "{ua}" {response_time}\n')
    
    return logs

def write_batch(args):
    """Fonction pour écriture parallèle"""
    batch_num, batch_size, output_file, start_time = args
    logs = generate_log_batch(batch_size, start_time)
    
    with open(output_file, 'a') as f:
        f.writelines(logs)
    
    return len(logs)

def main():
    """Génère des millions de logs en parallèle"""
    output_path = Path(__file__).parent.parent / 'data' / 'raw_logs' / 'access_massive.log'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configuration
    TOTAL_LOGS = 2_000_000  # 2 MILLIONS de logs
    BATCH_SIZE = 10_000
    NUM_BATCHES = TOTAL_LOGS // BATCH_SIZE
    NUM_WORKERS = multiprocessing.cpu_count()
    
    print(f"🚀 Génération de {TOTAL_LOGS:,} logs avec {NUM_WORKERS} workers...")
    print(f"📦 {NUM_BATCHES} batches de {BATCH_SIZE:,} logs")
    
    # Vider le fichier existant
    if output_path.exists():
        output_path.unlink()
    
    start_time = datetime.now()
    
    # Génération parallèle
    args = [(i, BATCH_SIZE, output_path, start_time) for i in range(NUM_BATCHES)]
    
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        results = list(executor.map(write_batch, args))
        total_generated = sum(results)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n✅ {total_generated:,} logs générés en {duration:.2f}s")
    print(f"⚡ Vitesse: {total_generated/duration:,.0f} logs/seconde")
    print(f"📁 Fichier: {output_path}")
    print(f"💾 Taille: {output_path.stat().st_size / (1024*1024):.2f} MB")

if __name__ == '__main__':
    main()
