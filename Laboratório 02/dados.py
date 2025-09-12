import pandas as pd
from datetime import datetime


ARQUIVO_GITHUB = 'dados_repositorios_java.csv'
ARQUIVO_CK = 'metricas_qualidade_sumarizadas.csv'
ARQUIVO_FINAL = 'dataset_final.csv'

print(f"Carregando dados de '{ARQUIVO_GITHUB}'...")
df_github = pd.read_csv(ARQUIVO_GITHUB)
print(f"  -> Encontrados {len(df_github)} registros.")

print(f"Carregando dados de '{ARQUIVO_CK}'...")
df_ck = pd.read_csv(ARQUIVO_CK)
print(f"  -> Encontrados {len(df_ck)} registros.")


print("\nUnindo os dois datasets...")
df_final = pd.merge(df_github, df_ck, on='full_name', how='inner')
print(f"  -> Dataset final possui {len(df_final)} registros após a união.")


df_final['created_at'] = pd.to_datetime(df_final['created_at'])

hoje = datetime.now()
df_final['idade_dias'] = (hoje - df_final['created_at']).dt.days

# Converte a idade de dias para anos
df_final['idade_anos'] = df_final['idade_dias'] / 365.25

# Vamos arredondar para 2 casas decimais e remover colunas que não precisamos mais
df_final['idade_anos'] = df_final['idade_anos'].round(2)
df_final = df_final.drop(columns=['created_at', 'idade_dias'])

print("  -> Métrica 'idade_anos' calculada com sucesso.")


# --- 5. SALVAR O DATASET FINAL ---
df_final.to_csv(ARQUIVO_FINAL, index=False, encoding='utf-8')
print(f"\n Dataset final salvo com sucesso em '{ARQUIVO_FINAL}'!")
print("Colunas do arquivo final:", df_final.columns.tolist())