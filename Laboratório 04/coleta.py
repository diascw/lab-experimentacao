import os
import requests
import pandas as pd
import time
from dotenv import load_dotenv  

load_dotenv() 


GITHUB_TOKEN = os.getenv('GITHUB_TOKEN') 
if not GITHUB_TOKEN:
    raise EnvironmentError("Variável de ambiente GITHUB_TOKEN não configurada. Verifique seu arquivo .env")

HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

API_URL = 'https://api.github.com/search/repositories'


TOPICOS_DE_BUSCA = {
    'Awesome List': 'topic:awesome-list',
    'Education': 'topic:education'
}


PAGINAS_POR_TOPICO = 10
RESULTADOS_POR_PAGINA = 100

dados_finais = []

print("Iniciando a coleta de dados da API do GitHub...")


for categoria, query in TOPICOS_DE_BUSCA.items():
    
    print(f"\nBuscando categoria: '{categoria}' (Query: '{query}')")
    
    for page_num in range(1, PAGINAS_POR_TOPICO + 1):
        
        params = {
            'q': query,
            'sort': 'stars',  
            'order': 'desc',
            'per_page': RESULTADOS_POR_PAGINA,
            'page': page_num
        }
        
        try:
            response = requests.get(API_URL, headers=HEADERS, params=params)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                
                if not items:
                    print(f"  Página {page_num}: Não encontrou mais resultados. Terminando este tópico.")
                    break  
                
                print(f"  Página {page_num}: Coletando {len(items)} repositórios...")
                
                for repo in items:
                    dados_repo = {
                        'categoria': categoria,
                        'nome_repo': repo.get('name'),
                        'url': repo.get('html_url'),
                        'stargazers_count': repo.get('stargazers_count'),
                        'forks_count': repo.get('forks_count'),
                        'open_issues_count': repo.get('open_issues_count'),
                        'language': repo.get('language'),
                        'license_name': repo.get('license', {}).get('name') if repo.get('license') else None,
                        'created_at': repo.get('created_at'),
                        'pushed_at': repo.get('pushed_at')
                    }
                    dados_finais.append(dados_repo)
                
               
                time.sleep(2.5) 
                
            elif response.status_code == 403:
                print(f"  Erro 403: Atingiu o Rate Limit da API. Aguardando 60 segundos...")
                print(f"  Mensagem do GitHub: {response.json().get('message')}")
                print(f"  Headers de limite: {response.headers.get('X-RateLimit-Remaining')} restantes.")
                time.sleep(60)
            else:
                print(f"  Erro ao buscar página {page_num}. Status: {response.status_code}")
                print(f"  Mensagem: {response.text}")
                break 

        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro de rede ou conexão: {e}")
            print("Aguardando 30 segundos antes de tentar novamente...")
            time.sleep(30)
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            break


if dados_finais:
    df = pd.DataFrame(dados_finais)
    
    nome_arquivo = 'github_dataset_alternativo.csv'
    df.to_csv(nome_arquivo, index=False, encoding='utf-8')
    
    print(f"\nColeta concluída! {len(df)} registros salvos em '{nome_arquivo}'.")
else:
    print("\nColeta concluída, mas nenhum dado foi salvo.")