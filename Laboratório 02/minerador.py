import os
import requests
import csv
import time

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}

API_URL = 'https://api.github.com/search/repositories'

# parâmetros fixos da busca
BASE_PARAMS = {
    'q': 'language:java',
    'sort': 'stars',
    'order': 'desc',
    'per_page': 100  
}

repos = []

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
            print(" Chave 'items' não encontrada na resposta.")
            break

        time.sleep(2)

except requests.exceptions.RequestException as e:
    print(f" Erro na requisição: {e}")
    if response is not None:
        print(f"Resposta da API: {response.text}")

print(f"\n Total de repositórios coletados: {len(repos)}")

# salva no CSV
with open('lista_repositorios_java.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['repositorio'])
    for repo in repos:
        writer.writerow([repo])

print(" Lista de repositórios salva em 'lista_repositorios_java.csv'")
