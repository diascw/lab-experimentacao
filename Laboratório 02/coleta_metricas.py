import os
import csv
import subprocess
import pandas as pd
import shutil


CK_JAR_PATH = 'ck.jar' 
REPO_LIST_FILE = 'lista_repositorios_java.csv'
CLONE_DIR = 'cloned_repos'
CK_RESULTS_DIR = 'ck_results'
FINAL_RESULTS_FILE = 'metricas_sumarizadas.csv'


def criar_diretorios():
    """Cria os diretórios necessários para o script, se não existirem."""
    print("Criando diretórios necessários...")
    os.makedirs(CLONE_DIR, exist_ok=True)
    os.makedirs(CK_RESULTS_DIR, exist_ok=True)

def ler_lista_repositorios():
    """Lê o arquivo CSV com a lista de repositórios."""
    try:
        with open(REPO_LIST_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  
            repos = [row[0] for row in reader]
            print(f"Encontrados {len(repos)} repositórios na lista.")
            return repos
    except FileNotFoundError:
        print(f"Erro: Arquivo '{REPO_LIST_FILE}' não encontrado.")
        return []

def clonar_repositorio(repo_full_name):
    """Clona um repositório do GitHub, limpando o diretório antigo se existir."""
    repo_name = repo_full_name.split('/')[-1]
    repo_path = os.path.join(CLONE_DIR, repo_name)
    
    if os.path.exists(repo_path):
        print(f"Repositório '{repo_full_name}' já existe. Removendo para garantir uma clonagem limpa...")
        shutil.rmtree(repo_path)
    
    print(f"Clonando '{repo_full_name}' para '{repo_path}'...")
    try:
        subprocess.run(
            ['git', 'clone', f'https://github.com/{repo_full_name}.git', repo_path, '--depth', '1'],
            check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore'
        )
        print("Clone concluído com sucesso.")
        return repo_path
    except subprocess.CalledProcessError as e:
        print(f"### ERRO AO CLONAR O REPOSITÓRIO '{repo_full_name}'. ###")
        print(f"Erro: {e.stderr}")
        return None

def executar_ck(repo_path):
    """Executa a ferramenta CK com os parâmetros corretos e captura erros."""
    repo_name = os.path.basename(repo_path)
    output_path = os.path.join(CK_RESULTS_DIR, repo_name)
    
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)
    
    print(f"\nExecutando o CK para o repositório '{repo_name}'...")
    try:
        command = [
            'java', '-jar', CK_JAR_PATH,
            repo_path,    
            'false',        
            '0',          
            'false',       
            output_path     
        ]
        
        print(f"Comando executado: {' '.join(command)}")
        
        subprocess.run(
            command,
            check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore'
        )
        
        print(f"CK executado com sucesso. Resultados salvos em '{output_path}'.")
        return output_path
        
    except subprocess.CalledProcessError as e:
        print(f"### ERRO AO EXECUTAR O CK no repositório '{repo_name}'. ###")
        print(f"--- Mensagem de erro do CK (stderr): ---\n{e.stderr}\n------------------------------------------")
        return None
    except FileNotFoundError:
        print(f"### ERRO CRÍTICO ###")
        print(f"Comando 'java' não foi encontrado ou o arquivo '{CK_JAR_PATH}' não existe nesta pasta.")
        print("Verifique se o JDK está instalado e se o nome do arquivo .jar está correto na variável CK_JAR_PATH.")
        return None

def sumarizar_metricas(ck_output_path, repo_full_name):
    """Lê os resultados do CK e calcula média, mediana e desvio padrão."""
    class_metrics_file = os.path.join(ck_output_path, 'class.csv')
    
    if not os.path.exists(class_metrics_file):
        print(f"\nERRO FINAL: Arquivo 'class.csv' não foi gerado em '{ck_output_path}'.")
        print("Isso pode acontecer se o repositório não tiver código Java ou se o CK encontrou um erro fatal.")
        return None

    print("\nSumarizando métricas (CBO, DIT, LCOM)...")
    try:
        df = pd.read_csv(class_metrics_file)
        
        metricas = ['cbo', 'dit', 'lcom']
        sumario = {'repositorio': repo_full_name}
        
        for metrica in metricas:
            sumario[f'{metrica}_media'] = df[metrica].mean()
            sumario[f'{metrica}_mediana'] = df[metrica].median()
            sumario[f'{metrica}_desvio_padrao'] = df[metrica].std()
                
        return sumario
    except Exception as e:
        print(f"Erro ao processar o arquivo '{class_metrics_file}': {e}")
        return None


def main():
    """Função principal que orquestra todo o processo."""
    criar_diretorios()
    repositorios = ler_lista_repositorios()
    
    if not repositorios:
        return

    primeiro_repo = repositorios[0]
    
    caminho_repo_clonado = clonar_repositorio(primeiro_repo)
    
    if caminho_repo_clonado:
        caminho_resultado_ck = executar_ck(caminho_repo_clonado)
        
        if caminho_resultado_ck:
            dados_sumarizados = sumarizar_metricas(caminho_resultado_ck, primeiro_repo)
            
            if dados_sumarizados:
                print(f"\nSalvando resultados sumarizados em '{FINAL_RESULTS_FILE}'...")
                
                df_final = pd.DataFrame([dados_sumarizados])
                df_final.to_csv(FINAL_RESULTS_FILE, index=False, mode='w', header=True)
                    
                print(f"\nPROCESSO CONCLUÍDO COM SUCESSO!")
                print(f"O resultado para '{primeiro_repo}' foi salvo em '{FINAL_RESULTS_FILE}'.")

if __name__ == '__main__':
    main()