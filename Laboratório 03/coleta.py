import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv 

import pandas as pd
import requests
from tqdm import tqdm

load_dotenv()  


GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

REPOSITORIES = [
    "freeCodeCamp/freeCodeCamp", "vuejs/vue", "facebook/react", "tensorflow/tensorflow",
    "EbookFoundation/free-programming-books", "sindresorhus/awesome", "jwasham/coding-interview-university",
    "kamranahmedse/developer-roadmap", "public-apis/public-apis", "github/gitignore", "torvalds/linux",
    "getify/You-Dont-Know-JS", "ohmyzsh/ohmyzsh", "airbnb/javascript", "donnemartin/system-design-primer",
    "TheAlgorithms/Python", "microsoft/vscode", "facebook/react-native", "flutter/flutter", "kubernetes/kubernetes",
    "DefinitelyTyped/DefinitelyTyped", "twbs/bootstrap", "microsoft/TypeScript", "ant-design/ant-design",
    "golang/go"
]

HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

OUTPUT_CSV_FILE = 'github_prs_dataset.csv'
MAX_PRS_PER_REPO = 500  



def get_api_data(url: str):
    """
    Faz uma requisição GET à API do GitHub com tratamento de limite de taxa (rate limit).
    """
    while True:
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403 and 'rate limit' in response.text.lower():
                reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 60))
                sleep_duration = max(reset_time - time.time() + 5, 1) 
                tqdm.write(f"Rate limit atingido. Aguardando por {sleep_duration:.0f} segundos.")
                time.sleep(sleep_duration)
            elif response.status_code == 404:
                tqdm.write(f"Recurso não encontrado (404): {url}")
                return None
            else:
                tqdm.write(f"Erro ao acessar a API (Status {response.status_code}) para a URL: {url}")
                return None
        except requests.exceptions.RequestException as e:
            tqdm.write(f"Erro de conexão: {e}. Tentando novamente em 30 segundos.")
            time.sleep(30)


def parse_iso_datetime(date_str: str):
    """
    Converte uma string de data no formato ISO 8601 para um objeto datetime.
    """
    if date_str:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    return None

def get_pull_requests(repo_owner: str, repo_name: str):
    """
    Busca Pull Requests (merged e closed) de um repositório, com paginação.
    """
    prs = []
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls?state=closed&per_page=100"
    
    max_pages = MAX_PRS_PER_REPO // 100
    
    for page in range(1, max_pages + 1):
        paginated_url = f"{base_url}&page={page}"
        data = get_api_data(paginated_url)
        if not data:
            break
        prs.extend(data)
        time.sleep(1) 
    
    return prs


def main():
    """
    Função principal para orquestrar a coleta e processamento dos dados.
    """
    if not GITHUB_TOKEN:
        print("ERRO: A variável de ambiente 'GITHUB_TOKEN' não está definida.")
        print("Por favor, defina a variável com seu token de acesso pessoal do GitHub e tente novamente.")
        return

    all_prs_data = []

    print("Iniciando a coleta de dados dos Pull Requests...")
    
    for repo_full_name in tqdm(REPOSITORIES, desc="Progresso dos Repositórios"):
        owner, name = repo_full_name.split('/')
        
        pull_requests = get_pull_requests(owner, name)

        if len(pull_requests) < 100:
            tqdm.write(f"Repositório '{repo_full_name}' ignorado (possui menos de 100 PRs fechados).")
            continue

        for pr in tqdm(pull_requests, desc=f"Analisando PRs de '{name}'", leave=False):
            created_at = parse_iso_datetime(pr['created_at'])
            closed_at = parse_iso_datetime(pr.get('closed_at'))

            if not closed_at: continue

            if (closed_at - created_at) <= timedelta(hours=1):
                continue

            reviews_url = pr['_links']['self']['href'] + '/reviews'
            reviews_data = get_api_data(reviews_url)

            if not reviews_data or len(reviews_data) == 0:
                continue
            
            pr_details_url = pr['url']
            pr_details = get_api_data(pr_details_url)
            
            if not pr_details:
                continue

          
            status = 'MERGED' if pr_details.get('merged') else 'CLOSED'
            
            num_files = pr_details.get('changed_files', 0)
            lines_added = pr_details.get('additions', 0)
            lines_removed = pr_details.get('deletions', 0)
            
            last_activity_at = parse_iso_datetime(pr['updated_at'])
            analysis_time_hours = (last_activity_at - created_at).total_seconds() / 3600 if last_activity_at else 0
            
            description_length = len(pr_details.get('body') or '')
            
            comments_data = get_api_data(pr_details['_links']['comments']['href'])
            participants = {pr_details['user']['login']}
            
            if comments_data:
                for comment in comments_data:
                    if comment.get('user'): participants.add(comment['user']['login'])
            
            for review in reviews_data:
                if review.get('user'): participants.add(review['user']['login'])
            
            num_participants = len(participants)
            num_comments = pr_details.get('comments', 0) + pr_details.get('review_comments', 0)
            
  
            num_reviews = len(reviews_data)

            all_prs_data.append({
                'repo': repo_full_name,
                'pr_number': pr['number'],
                'status': status,
                'num_files': num_files,
                'lines_added': lines_added,
                'lines_removed': lines_removed,
                'analysis_time_hours': round(analysis_time_hours, 2),
                'description_length': description_length,
                'num_participants': num_participants,
                'num_comments': num_comments,
                'num_reviews': num_reviews,
                'created_at': created_at.isoformat(),
                'closed_at': closed_at.isoformat()
            })

    if not all_prs_data:
        print("\nNenhum Pull Request atendeu a todos os critérios de coleta.")
        return

    df = pd.DataFrame(all_prs_data)
    df.to_csv(OUTPUT_CSV_FILE, index=False, encoding='utf-8')
    print(f"\nColeta finalizada com sucesso!")
    print(f"{len(df)} Pull Requests foram coletados e salvos em '{OUTPUT_CSV_FILE}'.")


if __name__ == '__main__':
    main()