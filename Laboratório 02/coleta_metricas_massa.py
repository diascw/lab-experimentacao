import pandas as pd
import subprocess
import os
import shutil
import stat
import time

REPOSITORIES_CSV = 'repositories.csv'
CK_JAR_PATH = os.path.join('ck', 'target', 'ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar')
CLONE_DIR = 'temp_repo'
# O CK gera os resultados em um subdiretório com o nome do projeto, então apontamos para um diretório pai.
OUTPUT_DIR_BASE = 'resultados_ck_massa'
RESULTADO_FINAL_CSV = 'todas_metricas_classe.csv'

# --- Função de ajuda para a limpeza ---
def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

# --- Lógica Principal do Script ---
def coletar_metricas_em_massa():
    # 1. Ler o CSV com a lista de repositórios
    try:
        df_repos = pd.read_csv(REPOSITORIES_CSV)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{REPOSITORIES_CSV}' não encontrado!")
        return

    # Lista para armazenar todos os DataFrames de métricas de classe
    lista_dfs_metricas = []

    # 2. Loop por cada repositório no DataFrame
    for index, repo_info in df_repos.iterrows():
        repo_url = repo_info['url']
        repo_name = repo_info['name']
        repo_owner = repo_info['owner']
        full_repo_name = f"{repo_owner}_{repo_name}" # Nome único para a pasta de resultados

        print(f"\n--- Processando Repositório {index + 1}/{len(df_repos)}: {repo_name} ---")

        try:
            # 3. Clonar o repositório
            if os.path.exists(CLONE_DIR):
                shutil.rmtree(CLONE_DIR, onerror=remove_readonly)
            
            print(f"Clonando {repo_url}...")
            subprocess.run(['git', 'clone', '--depth', '1', repo_url, CLONE_DIR], check=True, capture_output=True, text=True)
            print("Clone concluído. ✅")

            # 4. Executar a ferramenta CK
            caminho_repo_clonado = os.path.abspath(CLONE_DIR)
            caminho_saida_ck = os.path.abspath(os.path.join(OUTPUT_DIR_BASE))

            if not os.path.exists(caminho_saida_ck):
                os.makedirs(caminho_saida_ck)
                
            print("Executando CK...")
            comando_ck = [
                'java', '-jar', CK_JAR_PATH, caminho_repo_clonado, 'true', '0', caminho_saida_ck, full_repo_name
            ]
            subprocess.run(comando_ck, check=True, capture_output=True, text=True)

            # 5. Ler o resultado e adicioná-lo à lista
            # O CK salva o resultado em OUTPUT_DIR_BASE/full_repo_name/class.csv
            caminho_csv_resultado = os.path.join(caminho_saida_ck, full_repo_name, 'class.csv')
            
            if os.path.exists(caminho_csv_resultado):
                df_metricas_repo = pd.read_csv(caminho_csv_resultado)
                # Adiciona uma coluna para identificar o repositório em cada linha de métrica
                df_metricas_repo['repository'] = repo_name 
                # Adiciona as informações do repositório original (estrelas, etc.)
                for col in repo_info.index:
                    df_metricas_repo[col] = repo_info[col]

                lista_dfs_metricas.append(df_metricas_repo)
                print(f"Métricas de '{repo_name}' coletadas e adicionadas. ✅")
            else:
                print(f"AVISO: Arquivo class.csv não encontrado para o repositório '{repo_name}'.")

        except Exception as e:
            print(f"!!!!!! ERRO ao processar o repositório {repo_name}: {e} !!!!!!")
            print("Continuando para o próximo...")
            continue # Pula para o próximo repositório em caso de erro

        finally:
            # 6. Limpar
            if os.path.exists(CLONE_DIR):
                shutil.rmtree(CLONE_DIR, onerror=remove_readonly)

    # 7. Juntar todos os resultados em um único DataFrame e salvar
    if lista_dfs_metricas:
        df_final = pd.concat(lista_dfs_metricas, ignore_index=True)
        df_final.to_csv(RESULTADO_FINAL_CSV, index=False)
        print(f"\nProcesso finalizado! Todas as métricas foram salvas em '{RESULTADO_FINAL_CSV}'.")
    else:
        print("\nNenhuma métrica foi coletada.")


if __name__ == "__main__":
    coletar_metricas_em_massa()