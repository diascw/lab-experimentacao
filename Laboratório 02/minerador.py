import os
import requests
import csv
import time
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}

API_URL = 'https://api.github.com/search/repositories'

BASE_PARAMS = {
    'q': 'language:java',
    'sort': 'stars',
    'order': 'desc',
    'per_page': 100
}

repos = []
response = None

print("Buscando até 1000 repositórios em várias páginas...")

try:
    for page in range(1, 11):
        print(f"  Buscando página {page}...")
        params = BASE_PARAMS.copy()
        params['page'] = page

        response = requests.get(API_URL, headers=HEADERS, params=params)
        response.raise_for_status()

        data = response.json()

        if 'items' in data:
            for item in data['items']:
                repos.append(item['full_name'])
        else:
            print("  Chave 'items' não encontrada na resposta. Interrompendo.")
            break

        time.sleep(2)

except requests.exceptions.RequestException as e:
    print(f"\n[ERRO] Ocorreu um erro na requisição: {e}")
    if response is not None:
        print(f"  Resposta da API (status {response.status_code}): {response.text}")

print(f"\nTotal de repositórios coletados: {len(repos)}")

output_file = 'lista_repositorios_java.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['repositorio'])  
    for repo in repos:
        writer.writerow([repo])

print(f"Lista de repositórios salva com sucesso em '{output_file}'")