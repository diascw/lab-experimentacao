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
    response.raise_for_status()  # Lança um erro para respostas HTTP > 400
    
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
with open('lista_repositorios_java.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['repositorio']) 
    for repo in repos:
        writer.writerow([repo])

print("Lista de repositórios salva em 'lista_repositorios_java.csv'")
