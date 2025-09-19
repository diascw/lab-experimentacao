import requests
import os
import subprocess
import pandas as pd
import shutil
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
import stat 

# Bibliotecas para a análise
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr

# --- FUNÇÕES AUXILIARES ---

def find_best_java_source_directory(root_path):
    """Tenta encontrar o melhor diretório de código-fonte Java em um projeto."""
    print(f"Buscando código-fonte em '{root_path}'...")
    standard_path_suffix = os.path.join("src", "main", "java")
    for dirpath, _, _ in os.walk(root_path):
        if dirpath.endswith(standard_path_suffix):
            print(f"Diretório padrão encontrado: '{dirpath}'")
            return dirpath, -1

    best_path, max_java_files = root_path, 0
    for dirpath, _, filenames in os.walk(root_path):
        if os.path.sep + '.' in dirpath: continue
        
        java_files_count = sum(1 for f in filenames if f.endswith('.java'))
        if java_files_count > max_java_files:
            max_java_files = java_files_count
            best_path = dirpath
            
    if max_java_files > 0:
        print(f"Diretório com mais arquivos Java: '{best_path}' ({max_java_files} arquivos).")
    else:
        print("Nenhum arquivo .java encontrado no projeto.")
        
    return best_path, max_java_files

def remove_readonly(func, path, exc_info):
    """Função para tratar erros de permissão no Windows ao apagar o repositório."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

# --- FUNÇÃO DE ANÁLISE E VISUALIZAÇÃO ---

def perform_analysis_and_visualization(final_df):
    """Realiza a análise final e gera todos os gráficos para o relatório."""
    print("\n--- INICIANDO ANÁLISE E GERAÇÃO DE GRÁFICOS ---")
    if not os.path.exists("graficos"):
        os.makedirs("graficos")

    rq_map = {
        "RQ01_Popularidade": {"metric": "stars", "label": "Popularidade (Estrelas)"},
        "RQ02_Maturidade": {"metric": "age_years", "label": "Maturidade (Anos)"},
        "RQ03_Atividade": {"metric": "releases_count", "label": "Atividade (Nº de Releases)"},
        "RQ04_Tamanho": {"metric": "loc_total", "label": "Tamanho (LOC Total)"}
    }
    
    quality_metrics = ["cbo_median", "dit_median", "lcom_median"]

    for rq_name, rq_data in rq_map.items():
        for quality_metric in quality_metrics:
            print(f"\nAnalisando: {rq_name} vs. {quality_metric}")
            analysis_df = final_df[[rq_data["metric"], quality_metric]].dropna()
            
            if len(analysis_df) < 2:
                print("Dados insuficientes para análise.")
                continue

            corr, p_value = spearmanr(analysis_df[rq_data["metric"]], analysis_df[quality_metric])
            print(f"Correlação de Spearman: {corr:.3f} (p-valor: {p_value:.3f})")
            
            plt.figure(figsize=(10, 6))
            sns.regplot(data=analysis_df, x=rq_data["metric"], y=quality_metric, line_kws={"color": "red"})
            plt.title(f'{rq_name}: {rq_data["label"]} vs. {quality_metric.replace("_", " ").upper()}')
            plt.xlabel(rq_data["label"])
            plt.ylabel(quality_metric.replace("_", " ").upper())
            plt.grid(True)
            
            filename = f"graficos/{rq_name}_{quality_metric}.png"
            plt.savefig(filename)
            plt.close()
            print(f"Gráfico salvo em: {filename}")

# --- FUNÇÃO PRINCIPAL ---

def main():
    # --- CONFIGURAÇÕES ---
    NUM_REPOS_TO_ANALYZE = 1000
    REPOS_PER_PAGE = 100
    FINAL_CSV_PATH = "analise_final_repositorios.csv"
    CK_JAR_FILENAME = "ck.jar"

    load_dotenv()
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    if not GITHUB_TOKEN:
        print("ERRO: GITHUB_TOKEN não encontrado no arquivo .env")
        return
        
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    
    if os.path.exists(FINAL_CSV_PATH):
        os.remove(FINAL_CSV_PATH)
        print(f"Arquivo de resultados antigo '{FINAL_CSV_PATH}' removido.")

    all_repos = []
    num_pages_needed = (NUM_REPOS_TO_ANALYZE + REPOS_PER_PAGE - 1) // REPOS_PER_PAGE
    for page in range(1, num_pages_needed + 1):
        api_url = f"https://api.github.com/search/repositories?q=language:java&sort=stars&order=desc&per_page={REPOS_PER_PAGE}&page={page}"
        try:
            print(f"\nBuscando página {page}/{num_pages_needed} de repositórios...")
            response = requests.get(api_url, timeout=60, headers=headers)
            response.raise_for_status()
            all_repos.extend(response.json().get('items', []))
        except requests.exceptions.RequestException as e:
            print(f"Erro fatal ao acessar a API do GitHub: {e}"); return
    
    repos_to_process = all_repos[:NUM_REPOS_TO_ANALYZE]

    for i, repo_data in enumerate(repos_to_process):
        repo_name = repo_data['name']
        clone_url = repo_data['clone_url']
        print(f"\n--- Processando Repositório {i + 1}/{len(repos_to_process)}: {repo_name} ---")

        releases_url = repo_data.get('releases_url', '').replace('{/id}', '')
        releases_count = 0
        try:
            releases_response = requests.get(f"{releases_url}?per_page=1", headers=headers, timeout=30)
            if 'Link' in releases_response.headers:
                link_header = releases_response.headers['Link']
                if 'last' in link_header:
                    releases_count = int(link_header.split('page=')[-1].split('>')[0])
                else:
                    releases_count = len(requests.get(releases_url, headers=headers, timeout=30).json())
            elif releases_response.ok:
                 releases_count = len(releases_response.json())
        except Exception:
            print("Aviso: Falha ao buscar contagem de releases.")

        repo_metrics = {
            "repo_name": repo_name,
            "stars": repo_data.get('stargazers_count', 0),
            "age_years": (datetime.now(timezone.utc) - pd.to_datetime(repo_data.get('created_at'))).days / 365.25 if repo_data.get('created_at') else 0,
            "releases_count": releases_count,
            "cbo_median": None, "dit_median": None, "lcom_median": None, "loc_total": None
        }

        try:
            if os.path.exists(repo_name): shutil.rmtree(repo_name, onerror=remove_readonly)
            subprocess.run(["git", "clone", "--depth", "1", clone_url, repo_name], check=True, capture_output=True, text=True, timeout=300)

            source_path, file_count = find_best_java_source_directory(repo_name)
            
            if file_count != 0:
                subprocess.run(["java", "-jar", CK_JAR_FILENAME, source_path], check=True, capture_output=True, text=True, timeout=300)
                
                if os.path.exists("class.csv"):
                    df = pd.read_csv("class.csv")
                    if not df.empty:
                        repo_metrics.update({
                            "cbo_median": df['cbo'].median(),
                            "dit_median": df['dit'].median(),
                            "lcom_median": df['lcom'].median(),
                            "loc_total": df['loc'].sum()
                        })
                        print("Métricas do CK calculadas.")
        except Exception as e:
            print(f"ERRO: Falha no processamento do repositório {repo_name}. Erro: {e}")
        finally:
            df_to_append = pd.DataFrame([repo_metrics])
            file_exists = os.path.exists(FINAL_CSV_PATH)
            df_to_append.to_csv(FINAL_CSV_PATH, mode='a', header=not file_exists, index=False)
            print(f"Dados do repositório salvos em {FINAL_CSV_PATH}")

            if os.path.exists("class.csv"): os.remove("class.csv")
            if os.path.exists("method.csv"): os.remove("method.csv")
            if os.path.exists(repo_name): shutil.rmtree(repo_name, onerror=remove_readonly)
            
    print(f"\n--- COLETA DE DADOS CONCLUÍDA! ---")

    if os.path.exists(FINAL_CSV_PATH):
        final_df = pd.read_csv(FINAL_CSV_PATH)
        if not final_df.empty:
            perform_analysis_and_visualization(final_df)
    else:
        print("Arquivo de análise final não encontrado.")

if __name__ == "__main__":
    main()