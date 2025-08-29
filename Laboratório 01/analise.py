import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- 1. Carregamento e Preparação dos Dados ---
print("Carregando e preparando os dados...")
CSV_FILE = 'top_1000_github_repos.csv'
df = pd.read_csv(CSV_FILE)

# Converte colunas de data para o formato datetime
df['createdAt'] = pd.to_datetime(df['createdAt'])
df['pushedAt'] = pd.to_datetime(df['pushedAt'])

# Calcula a idade do repositório em anos
df['repositoryAge'] = (pd.to_datetime('now', utc=True) - df['createdAt']).dt.days / 365.25

# Calcula os dias desde a última atualização
df['daysSinceLastPush'] = (pd.to_datetime('now', utc=True) - df['pushedAt']).dt.days

# Calcula o percentual de issues fechadas, tratando divisão por zero
df['closedIssuesPercentage'] = (df['closedIssues'] / df['totalIssues'] * 100).fillna(100)

print("Dados carregados e novas métricas calculadas com sucesso!")

# Cria um diretório para salvar os gráficos
import os
if not os.path.exists('graficos'):
    os.makedirs('graficos')

# --- 2. Geração dos Gráficos ---

# RQ01: Idade dos Repositórios (Histograma)
print("Gerando gráfico para RQ01 - Idade dos Repositórios...")
plt.figure(figsize=(10, 6))
sns.histplot(df['repositoryAge'], bins=20, kde=True)
plt.title('RQ01: Distribuição da Idade dos Repositórios Populares (em anos)')
plt.xlabel('Idade (Anos)')
plt.ylabel('Número de Repositórios')
plt.grid(True)
plt.savefig('graficos/rq01_idade_repositorios.png')
plt.close()

# RQ02: Pull Requests Aceitas (Box Plot)
print("Gerando gráfico para RQ02 - Pull Requests...")
plt.figure(figsize=(10, 6))
# Usando escala de log para melhor visualização devido a outliers
sns.boxplot(x=df['acceptedPullRequests'])
plt.xscale('log')
plt.title('RQ02: Distribuição de Pull Requests Aceitas (Escala Log)')
plt.xlabel('Número de Pull Requests Aceitas')
plt.grid(True)
plt.savefig('graficos/rq02_pull_requests.png')
plt.close()

# RQ03: Total de Releases (Box Plot)
print("Gerando gráfico para RQ03 - Releases...")
plt.figure(figsize=(10, 6))
# Usando escala de log e removendo repositórios com 0 releases para a visualização
sns.boxplot(x=df[df['totalReleases'] > 0]['totalReleases'])
plt.xscale('log')
plt.title('RQ03: Distribuição do Total de Releases (Repositórios com > 0 Releases)')
plt.xlabel('Número Total de Releases (Escala Log)')
plt.grid(True)
plt.savefig('graficos/rq03_releases.png')
plt.close()

# RQ04: Dias Desde a Última Atualização (Histograma)
print("Gerando gráfico para RQ04 - Atualização...")
plt.figure(figsize=(10, 6))
sns.histplot(df['daysSinceLastPush'], bins=30, kde=True)
plt.title('RQ04: Frequência de Atualizações (Dias desde o último push)')
plt.xlabel('Dias Desde a Última Atualização')
plt.ylabel('Número de Repositórios')
plt.xlim(0, df['daysSinceLastPush'].quantile(0.95)) # Foca nos 95% mais recentes
plt.grid(True)
plt.savefig('graficos/rq04_atualizacao.png')
plt.close()

# RQ05: Linguagens de Programação
print("Gerando gráficos para RQ05 - Linguagens...")
# Contagem das linguagens
language_counts = df['primaryLanguage'].value_counts()
# Agrupa as linguagens menos comuns em "Outras"
top_10_languages = language_counts.nlargest(10)
others_count = language_counts.nsmallest(len(language_counts) - 10).sum()
top_10_languages['Outras'] = others_count

# Gráfico de Pizza
plt.figure(figsize=(10, 8))
plt.pie(top_10_languages, labels=top_10_languages.index, autopct='%1.1f%%', startangle=140, pctdistance=0.85)
plt.title('RQ05: Distribuição das 10 Principais Linguagens de Programação')
plt.axis('equal')
plt.savefig('graficos/rq05_linguagens.png')
plt.close()

# Gráfico de Barras
plt.figure(figsize=(12, 7))
sns.barplot(x=top_10_languages.index, y=top_10_languages.values)
plt.title('RQ05: Contagem de Repositórios por Principal Linguagem de Programação')
plt.xlabel('Linguagem')
plt.ylabel('Número de Repositórios')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('graficos/rq05_linguagens_bar.png')
plt.close()

# RQ06: Percentual de Issues Fechadas (Histograma)
print("Gerando gráfico para RQ06 - Issues Fechadas...")
plt.figure(figsize=(10, 6))
sns.histplot(df['closedIssuesPercentage'], bins=20, kde=False)
plt.title('RQ06: Distribuição do Percentual de Issues Fechadas')
plt.xlabel('Percentual de Issues Fechadas (%)')
plt.ylabel('Número de Repositórios')
plt.grid(True)
plt.savefig('graficos/rq06_issues_fechadas.png')
plt.close()

# RQ07: Comparação de Métricas por Linguagem
print("Gerando gráficos para RQ07 - Comparação por Linguagem...")
# Filtra o DataFrame para incluir apenas as top 10 linguagens (sem "Outras")
top_10_names = top_10_languages.drop('Outras').index
df_top_lang = df[df['primaryLanguage'].isin(top_10_names)]

# Agrupa por linguagem e calcula a mediana das métricas
metrics_by_lang = df_top_lang.groupby('primaryLanguage').agg({
    'repositoryAge': 'median',
    'acceptedPullRequests': 'median',
    'totalReleases': 'median',
    'closedIssuesPercentage': 'median',
    'stars': 'median'
}).rename(columns={
    'repositoryAge': 'Idade Mediana (Anos)',
    'acceptedPullRequests': 'PRs Aceitas (Mediana)',
    'totalReleases': 'Releases (Mediana)',
    'closedIssuesPercentage': 'Issues Fechadas % (Mediana)',
    'stars': 'Estrelas (Mediana)'
}).sort_values(by='Estrelas (Mediana)', ascending=False)


# Heatmap com as métricas normalizadas para melhor comparação de cores
plt.figure(figsize=(12, 8))
# Normaliza os dados (escala de 0 a 1) para o heatmap
metrics_normalized = (metrics_by_lang - metrics_by_lang.min()) / (metrics_by_lang.max() - metrics_by_lang.min())
sns.heatmap(metrics_normalized, annot=True, cmap='viridis', fmt=".2f")
plt.title('RQ07: Métricas Normalizadas por Linguagem (Mediana)')
plt.xlabel('Métricas')
plt.ylabel('Linguagem de Programação')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('graficos/rq07_metricas_por_linguagem.png')
plt.close()

# Gráfico de Barras para Estrelas por Linguagem
plt.figure(figsize=(12, 7))
sns.barplot(x=metrics_by_lang.index, y=metrics_by_lang['Estrelas (Mediana)'], palette='viridis')
plt.title('RQ07: Mediana de Estrelas por Linguagem')
plt.xlabel('Linguagem')
plt.ylabel('Mediana de Estrelas')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('graficos/rq07_comparacao_linguagens.png')
plt.close()

print("\nTodos os gráficos foram gerados e salvos na pasta 'graficos'!")