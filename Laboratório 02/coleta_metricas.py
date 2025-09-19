import pandas as pd
import subprocess
import os
import shutil  # Módulo para remover a pasta do repositório de forma segura
import stat    # Módulo necessário para alterar permissões de arquivos
import time    # Módulo para adicionar um pequeno delay antes da limpeza

# --- Configurações ---
# Nome do arquivo CSV com a lista de repositórios
REPOSITORIES_CSV = 'repositories.csv'

# Caminho para o arquivo .jar da ferramenta CK
CK_JAR_PATH = os.path.join('ck', 'target', 'ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar')

# Pasta onde os repositórios serão clonados temporariamente
CLONE_DIR = 'temp_repo'

# Pasta onde os resultados do CK serão salvos
OUTPUT_DIR = 'resultados_ck'

# --- Função de ajuda para a limpeza ---

# Função para lidar com erros de permissão em arquivos somente leitura (comum no .git do Windows)
def remove_readonly(func, path, excinfo):
    """
    Esta função de tratamento de erro é chamada por shutil.rmtree quando encontra um erro.
    Ela remove o atributo 'somente leitura' do arquivo e tenta novamente a operação original.
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)

# --- Lógica Principal do Script ---

def coletar_metricas():
    # 1. Certifique-se de que o diretório de saída existe
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Diretório '{OUTPUT_DIR}' criado.")

    # 2. Ler o arquivo CSV com os repositórios
    try:
        df = pd.read_csv(REPOSITORIES_CSV)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{REPOSITORIES_CSV}' não encontrado! Execute o minerador.py primeiro.")
        return

    # 3. Escolher um repositório para analisar (aqui, pegamos o primeiro da lista)
    if df.empty:
        print("Arquivo CSV está vazio. Nada para analisar.")
        return
    
    # Pegamos as informações do primeiro repositório (índice 0)
    repo_info = df.iloc[0]
    repo_url = repo_info['url']
    repo_name = repo_info['name']
    
    print(f"Iniciando análise do repositório: {repo_name}")

    # 4. Clonar o repositório
    # Primeiro, removemos o diretório se ele já existir de uma execução anterior
    if os.path.exists(CLONE_DIR):
        print(f"Removendo diretório antigo '{CLONE_DIR}'...")
        # Usamos o handler de erro caso a pasta antiga também tenha problemas de permissão
        shutil.rmtree(CLONE_DIR, onerror=remove_readonly)

    print(f"Clonando {repo_url} para a pasta '{CLONE_DIR}'...")
    try:
        # Usamos o subprocess para executar o comando 'git clone'
        subprocess.run(['git', 'clone', repo_url, CLONE_DIR], check=True, capture_output=True, text=True)
        print("Repositório clonado com sucesso! ")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao clonar o repositório: {e.stderr}")
        return

    # 5. Executar a ferramenta CK para coletar as métricas
    print("Executando a ferramenta CK para coletar as métricas...")
    caminho_repo_clonado = os.path.abspath(CLONE_DIR)
    caminho_saida_ck = os.path.abspath(OUTPUT_DIR)

    try:
        # Comando: java -jar ck.jar <caminho_do_repo> <use_jit> <max_files_per_commit> <output_dir>
        comando_ck = [
            'java', '-jar',
            CK_JAR_PATH,
            caminho_repo_clonado,
            'true', # use_jit
            '0',    # max_files (0 para ilimitado)
            caminho_saida_ck
        ]
        
        print(f"Comando CK: {' '.join(comando_ck)}")
        subprocess.run(comando_ck, check=True, capture_output=True, text=True)
        
        print(f"Métricas coletadas com sucesso! Resultados salvos em '{OUTPUT_DIR}'.")
        # O CK gera arquivos como 'class.csv', 'method.csv', etc. dentro do diretório de saída.

    except FileNotFoundError:
        print("Erro: 'java' não foi encontrado. Certifique-se de que o Java está instalado e no PATH do sistema.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o CK: {e.stdout}{e.stderr}")
    finally:
        # 6. Limpar a pasta do repositório clonado
        print(f"Limpando e removendo a pasta '{CLONE_DIR}'...")
        # Adiciona um pequeno delay para garantir que nenhum processo (como antivírus) esteja usando os arquivos
        time.sleep(1)
        # Chama a remoção com a função de tratamento de erro para lidar com arquivos somente leitura
        shutil.rmtree(CLONE_DIR, onerror=remove_readonly)
        print("Limpeza concluída. ")


if __name__ == "__main__":
    coletar_metricas()