import pandas as pd
import subprocess
import os
import shutil
import stat
import time

# --- Configurações ---
REPOSITORIES_CSV = 'repositories.csv'
CK_JAR_PATH = os.path.join('ck', 'target', 'ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar')
CLONE_DIR = 'temp_repo'
OUTPUT_DIR = '.' # Salva os resultados na pasta atual (Laboratório 02)

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def coletar_metricas_em_massa():
    try:
        df_repos = pd.read_csv(REPOSITORIES_CSV)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{REPOSITORIES_CSV}' não encontrado! Execute o minerador.py primeiro.")
        return

    print(f"Iniciando a coleta de métricas para {len(df_repos)} repositórios...")
    
    for index, repo_info in df_repos.iterrows():
        repo_url = repo_info['url']
        repo_name = repo_info['name']
        repo_owner = repo_info['owner']
        full_repo_name = f"{repo_owner}_{repo_name}"

        print(f"\n--- Processando Repositório {index + 1}/{len(df_repos)}: {repo_name} ---")

        try:
            if os.path.exists(CLONE_DIR):
                shutil.rmtree(CLONE_DIR, onerror=remove_readonly)
            
            print(f"Clonando {repo_url}...")
            subprocess.run(
                ['git', 'clone', '--depth', '1', repo_url, CLONE_DIR], 
                check=True, capture_output=True, text=True, timeout=300
            )
            print("Clone concluído.")

            caminho_repo_clonado = os.path.abspath(CLONE_DIR)
            caminho_saida_ck = os.path.abspath(OUTPUT_DIR)
            
            print("Executando CK...")
            comando_ck = [
                'java', '-jar', CK_JAR_PATH, caminho_repo_clonado, 'true', '0', caminho_saida_ck, full_repo_name
            ]
            resultado_processo = subprocess.run(comando_ck, capture_output=True, text=True, timeout=300)

            if resultado_processo.returncode != 0:
                 print(f"AVISO: O CK retornou um código de erro ({resultado_processo.returncode}) para o repo {repo_name}")
                 print(f"Mensagem de erro do CK:\n{resultado_processo.stderr}")

            print(f"Processamento de '{repo_name}' finalizado.")

        except Exception as e:
            print(f"!!!!!! ERRO GERAL ao processar o repositório {repo_name}: {e} !!!!!!")
            print("Continuando para o próximo...")
            continue 

        finally:
            if os.path.exists(CLONE_DIR):
                print(f"Limpando e removendo '{CLONE_DIR}'...")
                shutil.rmtree(CLONE_DIR, onerror=remove_readonly)
    
    print("\n--- Processo de coleta de métricas em massa CONCLUÍDO! ---")


if __name__ == "__main__":
    print("AVISO: Este processo analisará 1000 repositórios e pode levar MUITAS horas.")
    time.sleep(5)
    coletar_metricas_em_massa()