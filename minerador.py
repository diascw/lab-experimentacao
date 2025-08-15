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

