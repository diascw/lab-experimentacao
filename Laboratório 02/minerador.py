import requests
import csv
import time

GITHUB_TOKEN = 'GITHUB_TOKEN'  
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}

API_URL = 'https://api.github.com/search/repositories'

PARAMS = {
    'q': 'language:java',
    'sort': 'stars',
    'order': 'desc',
    'per_page': 100  
}
repos = []
print("Buscando a primeira página...")

try:
    response = requests.get(API_URL, headers=HEADERS, params=PARAMS)
    response.raise_for_status()  # lança um erro para respostas HTTP > 400
    
    data = response.json()
    
    if 'items' in data:
        for item in data['items']:
            repos.append(item['full_name']) 
    else:
        print("Chave 'items' não encontrada na resposta.")

except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")
    print(f"Resposta da API: {response.text}")

print(f"Total de repositórios coletados na primeira página: {len(repos)}")
print(repos)

