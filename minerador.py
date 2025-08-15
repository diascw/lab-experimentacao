import os
import requests
import pandas as pd
import json
from dotenv import load_dotenv
import time

# carrega variáveis de ambiente
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise ValueError("Token não encontrado! Verifique seu arquivo .env.")

API_URL = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"bearer {GITHUB_TOKEN}"}

TOTAL_REPOS = 100
BATCH_SIZE = 3  # menor batch para evitar 502 e Response ended prematurely
CSV_FILE = "top_100_github_repos.csv"
JSON_FILE = "laboratorio-01_data.json"

GRAPHQL_QUERY = """
query GetTopRepositories($cursor: String) {
  search(query: "stars:>1 sort:stars-desc", type: REPOSITORY, first: %d, after: $cursor) {
    repositoryCount
    pageInfo {
      endCursor
      hasNextPage
    }
    nodes {
      ... on Repository {
        nameWithOwner
        stargazers { totalCount }
        createdAt
        pushedAt
        primaryLanguage { name }
        releases { totalCount }
        pullRequests(states: MERGED) { totalCount }
        issues { totalCount }
        closedIssues: issues(states: CLOSED) { totalCount }
      }
    }
  }
}
""" % BATCH_SIZE

def run_query(query, variables):
    """executa a query com retry progressivo e timeout longo."""
    for attempt in range(8):
        try:
            response = requests.post(API_URL, json={'query': query, 'variables': variables}, headers=HEADERS, timeout=60)
            if response.status_code == 200:
                data = response.json()
                if "errors" in data:
                    print(f"erro retornado pela API: {data['errors']}")
                    time.sleep(min(60, 5 * 2**attempt))
                    continue
                return data
            elif response.status_code == 401:
                raise Exception("401 Unauthorized - verifique seu token.")
            else:
                print(f"erro {response.status_code}. tentando novamente em {min(60, 5 * 2**attempt)}s...")
        except requests.exceptions.RequestException as e:
            print(f"erro de conexão: {e}. tentando novamente em {min(60, 5 * 2**attempt)}s...")
        time.sleep(min(60, 5 * 2**attempt))
    raise Exception("falha após várias tentativas.")

def load_existing_data():
    """carrega dados existentes de CSV ou JSON para continuar."""
    if os.path.exists(CSV_FILE):
        print(f"{CSV_FILE} existe. Continuando de onde parou...")
        df_existing = pd.read_csv(CSV_FILE)
        return df_existing.to_dict('records')
    elif os.path.exists(JSON_FILE):
        print(f"{JSON_FILE} existe. Continuando de onde parou...")
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(all_repos_data):
    """salva CSV e JSON incrementalmente no mesmo arquivo."""
    # atualiza CSV completo
    pd.DataFrame(all_repos_data).to_csv(CSV_FILE, index=False)
    
    # salva JSON completo
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_repos_data, f, ensure_ascii=False, indent=2)

def mine_repositories():
    all_repos_data = load_existing_data()
    cursor = None

    print(f"iniciando mineração...\n")

    while len(all_repos_data) < TOTAL_REPOS:
        variables = {"cursor": cursor}
        result = run_query(GRAPHQL_QUERY, variables)
        data = result['data']['search']
        repos = data['nodes']

        if not repos:
            print("nenhum repositório retornado, saindo...")
            break

        for repo in repos:
            primary_language_name = repo['primaryLanguage']['name'] if repo['primaryLanguage'] else 'N/A'
            repo_data = {
                'name': repo['nameWithOwner'],
                'stars': repo['stargazers']['totalCount'],
                'createdAt': repo['createdAt'],
                'pushedAt': repo['pushedAt'],
                'primaryLanguage': primary_language_name,
                'totalReleases': repo['releases']['totalCount'],
                'acceptedPullRequests': repo['pullRequests']['totalCount'],
                'totalIssues': repo['issues']['totalCount'],
                'closedIssues': repo['closedIssues']['totalCount'],
            }
            all_repos_data.append(repo_data)

        # limita a quantidade total
        if len(all_repos_data) > TOTAL_REPOS:
            all_repos_data = all_repos_data[:TOTAL_REPOS]

        # salva CSV + JSON incremental
        save_data(all_repos_data)
        print(f"coletados {len(all_repos_data)}/{TOTAL_REPOS} repositórios...\n")

        page_info = data['pageInfo']
        if not page_info['hasNextPage']:
            print("não há mais páginas para buscar.")
            break

        cursor = page_info['endCursor']
        time.sleep(5)  # pausa entre páginas

    print("mineração concluída!")
    print(f"arquivos finais salvos em '{CSV_FILE}' e '{JSON_FILE}'")
    return pd.DataFrame(all_repos_data)

if __name__ == "__main__":
    mine_repositories()
