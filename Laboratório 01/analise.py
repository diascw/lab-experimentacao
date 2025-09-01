import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- 1. Carregamento e Preparação dos Dados ---
print("Carregando e preparando os dados...")
CSV_FILE = 'top_1000_github_repos.csv'
df = pd.read_csv(CSV_FILE)

# Converte colunas de data
df['createdAt'] = pd.to_datetime(df['createdAt'])
df['pushedAt'] = pd.to_datetime(df['pushedAt'])

# Calcula métricas derivadas
df['repositoryAge'] = (pd.to_datetime('now', utc=True) - df['createdAt']).dt.days / 365.25
df['daysSinceLastPush'] = (pd.to_datetime('now', utc=True) - df['pushedAt']).dt.days
df['closedIssuesPercentage'] = (df['closedIssues'] / df['totalIssues'] * 100).fillna(100)

print("Dados carregados e preparados!")

# Cria um diretório para salvar os gráficos (usando o mesmo nome 'graficos')
OUTPUT_DIR = 'graficos'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- Função para salvar tabelas como imagem ---
def save_df_as_image(df, title, filepath):
    """ Salva um DataFrame do Pandas como uma imagem de tabela. """
    fig, ax = plt.subplots(figsize=(8, max(2, len(df) * 0.5))) # Ajusta o tamanho dinamicamente
    ax.axis('off')
    ax.axis('tight')
    
    # Formata os números no DataFrame para melhor leitura
    df_display = df.copy()
    for col in df_display.select_dtypes(include=np.number).columns:
        df_display[col] = df_display[col].apply(lambda x: f'{x:,.2f}' if isinstance(x, float) else f'{x:,}')

    table = ax.table(cellText=df_display.values, colLabels=df_display.columns, rowLabels=df_display.index, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    
    plt.title(title, fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig(filepath, bbox_inches='tight', dpi=200)
    plt.close()

# --- 2. Geração dos Gráficos e Tabelas ---

# RQ01: Idade dos Repositórios (Gráfico de Pizza)
print("Gerando gráfico para RQ01 - Idade dos Repositórios...")
bins = [0, 5, 8, 10, 12, df['repositoryAge'].max()]
labels = ['0-5 anos', '5-8 anos', '8-10 anos', '10-12 anos', '12+ anos']
df['age_group'] = pd.cut(df['repositoryAge'], bins=bins, labels=labels, right=False)
age_dist = df['age_group'].value_counts()

plt.figure(figsize=(10, 8))
plt.pie(age_dist, labels=age_dist.index, autopct='%1.1f%%', startangle=140)
plt.title('RQ01: Proporção de Repositórios por Faixa de Idade')
plt.axis('equal')
plt.savefig(os.path.join(OUTPUT_DIR, 'rq01_idade_pizza.png'))
plt.close()

# RQ02 e RQ03: Pull Requests e Releases (Tabela de Estatísticas)
print("Gerando tabela para RQ02 e RQ03 - Contribuições e Releases...")
stats_df = df[['acceptedPullRequests', 'totalReleases']].describe().loc[['mean', '50%', '75%', 'max']]
stats_df.rename(index={'50%': 'mediana', '75%': 'quartil_superior'}, inplace=True)
stats_df.columns = ['Pull Requests Aceitas', 'Total de Releases']
save_df_as_image(stats_df, 'RQ02 & RQ03: Estatísticas de Contribuições e Releases', os.path.join(OUTPUT_DIR, 'rq02_rq03_estatisticas_tabela.png'))

# RQ04: Frequência de Atualizações (Gráfico de Pizza)
print("Gerando gráfico para RQ04 - Atualização...")
bins = [-1, 30, 90, 180, 365, df['daysSinceLastPush'].max()]
labels = ['Menos de 1 mês', '1-3 meses', '3-6 meses', '6-12 meses', 'Mais de 1 ano']
df['update_group'] = pd.cut(df['daysSinceLastPush'], bins=bins, labels=labels, right=True)
update_dist = df['update_group'].value_counts()

plt.figure(figsize=(10, 8))
plt.pie(update_dist, labels=update_dist.index, autopct='%1.1f%%', startangle=90)
plt.title('RQ04: Proporção por Tempo Desde a Última Atualização')
plt.axis('equal')
plt.savefig(os.path.join(OUTPUT_DIR, 'rq04_atualizacao_pizza.png'))
plt.close()


# RQ05: Linguagens de Programação (Pizza e Tabela)
print("Gerando gráficos para RQ05 - Linguagens...")
language_counts = df['primaryLanguage'].value_counts()
top_10_languages = language_counts.nlargest(10)
top_10_languages['Outras'] = language_counts.nsmallest(len(language_counts) - 10).sum()

# Gráfico de Pizza
plt.figure(figsize=(10, 8))
plt.pie(top_10_languages, labels=top_10_languages.index, autopct='%1.1f%%', startangle=140)
plt.title('RQ05: Distribuição das 10 Principais Linguagens')
plt.axis('equal')
plt.savefig(os.path.join(OUTPUT_DIR, 'rq05_linguagens_pizza.png'))
plt.close()

# Tabela
lang_df = top_10_languages.reset_index()
lang_df.columns = ['Linguagem', 'Nº de Repositórios']
lang_df.set_index('Linguagem', inplace=True)
save_df_as_image(lang_df, 'RQ05: Contagem de Repositórios por Linguagem', os.path.join(OUTPUT_DIR, 'rq05_linguagens_tabela.png'))

# RQ06: Percentual de Issues Fechadas (Gráfico de Pizza)
print("Gerando gráfico para RQ06 - Issues Fechadas...")
bins = [0, 80, 90, 95, 99, 100.1] # .1 para incluir o 100
labels = ['< 80%', '80-90%', '90-95%', '95-99%', '99-100%']
df['issues_group'] = pd.cut(df['closedIssuesPercentage'], bins=bins, labels=labels, right=False)
issues_dist = df['issues_group'].value_counts()

plt.figure(figsize=(10, 8))
plt.pie(issues_dist, labels=issues_dist.index, autopct='%1.1f%%', startangle=90)
plt.title('RQ06: Proporção por Faixa de Issues Fechadas')
plt.axis('equal')
plt.savefig(os.path.join(OUTPUT_DIR, 'rq06_issues_pizza.png'))
plt.close()

# RQ07: Comparação de Métricas por Linguagem (Tabela)
print("Gerando tabela para RQ07 - Comparação por Linguagem...")
top_10_names = top_10_languages.drop('Outras').index
df_top_lang = df[df['primaryLanguage'].isin(top_10_names)]
metrics_by_lang = df_top_lang.groupby('primaryLanguage').agg({
    'stars': 'median',
    'repositoryAge': 'median',
    'acceptedPullRequests': 'median',
}).rename(columns={
    'stars': 'Estrelas (Mediana)',
    'repositoryAge': 'Idade Mediana (Anos)',
    'acceptedPullRequests': 'PRs Aceitas (Mediana)',
}).sort_values(by='Estrelas (Mediana)', ascending=False)
save_df_as_image(metrics_by_lang, 'RQ07: Métricas por Linguagem (Mediana)', os.path.join(OUTPUT_DIR, 'rq07_comparacao_tabela.png'))

print(f"\nTodos os gráficos foram gerados e salvos na pasta '{OUTPUT_DIR}'!")