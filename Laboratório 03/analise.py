# -*- coding: utf-8 -*-
"""
Script de Análise e Visualização de Dados para o Lab03.

Este script processa o dataset 'github_prs_dataset.csv' para responder
às questões de pesquisa sobre a atividade de code review.

Ele calcula estatísticas descritivas (medianas), realiza testes de correlação
(Spearman) e gera visualizações (boxplots e scatter plots).
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr
import os

# --- CONFIGURAÇÃO ---
DATASET_FILE = 'github_prs_dataset.csv'
OUTPUT_DIR = 'graficos'

def main():
    """
    Função principal que orquestra a análise e visualização dos dados.
    """
    # Criar o diretório para salvar os gráficos, se não existir
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # --- CARREGAMENTO E PREPARAÇÃO DOS DADOS ---
    try:
        df = pd.read_csv(DATASET_FILE)
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{DATASET_FILE}' não foi encontrado.")
        print("Certifique-se de que o script de coleta foi executado com sucesso e o dataset está na mesma pasta.")
        return

    # Adicionar uma coluna 'total_lines' para a métrica de tamanho
    df['total_lines'] = df['lines_added'] + df['lines_removed']

    print("--- Análise de Dados Iniciada ---")
    print(f"Total de PRs no dataset: {len(df)}")
    print("\n")

    # ==============================================================================
    # A. FEEDBACK FINAL DAS REVISÕES (STATUS DO PR)
    # ==============================================================================
    print("--- PARTE A: Análise do Status do PR (MERGED vs. CLOSED) ---")

    # --- RQ01: Relação entre o Tamanho e o Status ---
    print("\n[RQ01: Tamanho vs. Status]")
    median_size = df.groupby('status')[['total_lines', 'num_files']].median()
    print("Valores Medianos:")
    print(median_size)
    
    plt.figure(figsize=(12, 6))
    plt.suptitle('RQ01: Relação entre Tamanho do PR e Status Final', fontsize=16)
    plt.subplot(1, 2, 1)
    sns.boxplot(x='status', y='total_lines', data=df, showfliers=False, order=['MERGED', 'CLOSED'], palette="pastel")
    plt.title('Total de Linhas Alteradas')
    plt.ylabel('Mediana de Linhas (Adicionadas + Removidas)')
    plt.xlabel('Status do PR')

    plt.subplot(1, 2, 2)
    sns.boxplot(x='status', y='num_files', data=df, showfliers=False, order=['MERGED', 'CLOSED'], palette="pastel")
    plt.title('Número de Arquivos Modificados')
    plt.ylabel('Mediana de Arquivos')
    plt.xlabel('Status do PR')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(OUTPUT_DIR, 'RQ01_tamanho_vs_status.png'))
    plt.close()

    print("\n[RQ02: Tempo de Análise vs. Status]")
    median_time = df.groupby('status')['analysis_time_hours'].median()
    print("Valores Medianos (Horas):")
    print(median_time)
    
    plt.figure(figsize=(7, 6))
    sns.boxplot(x='status', y='analysis_time_hours', data=df, showfliers=False, order=['MERGED', 'CLOSED'], palette="pastel")
    plt.title('RQ02: Relação entre Tempo de Análise e Status Final', fontsize=14)
    plt.ylabel('Mediana do Tempo de Análise (Horas)')
    plt.xlabel('Status do PR')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'RQ02_tempo_vs_status.png'))
    plt.close()

    print("\n[RQ03: Descrição vs. Status]")
    median_desc = df.groupby('status')['description_length'].median()
    print("Valores Medianos (Nº de Caracteres):")
    print(median_desc)

    plt.figure(figsize=(7, 6))
    sns.boxplot(x='status', y='description_length', data=df, showfliers=False, order=['MERGED', 'CLOSED'], palette="pastel")
    plt.title('RQ03: Relação entre Tamanho da Descrição e Status Final', fontsize=14)
    plt.ylabel('Mediana do Nº de Caracteres na Descrição')
    plt.xlabel('Status do PR')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'RQ03_descricao_vs_status.png'))
    plt.close()

    print("\n[RQ04: Interações vs. Status]")
    median_interactions = df.groupby('status')[['num_comments', 'num_participants']].median()
    print("Valores Medianos:")
    print(median_interactions)

    plt.figure(figsize=(12, 6))
    plt.suptitle('RQ04: Relação entre Interações no PR e Status Final', fontsize=16)
    plt.subplot(1, 2, 1)
    sns.boxplot(x='status', y='num_comments', data=df, showfliers=False, order=['MERGED', 'CLOSED'], palette="pastel")
    plt.title('Número de Comentários')
    plt.ylabel('Mediana de Comentários')
    plt.xlabel('Status do PR')

    plt.subplot(1, 2, 2)
    sns.boxplot(x='status', y='num_participants', data=df, showfliers=False, order=['MERGED', 'CLOSED'], palette="pastel")
    plt.title('Número de Participantes')
    plt.ylabel('Mediana de Participantes')
    plt.xlabel('Status do PR')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(OUTPUT_DIR, 'RQ04_interacoes_vs_status.png'))
    plt.close()


    print("\n\n--- PARTE B: Análise do Número de Revisões ---")

    corr_size, p_size = spearmanr(df['total_lines'], df['num_reviews'])
    print(f"\n[RQ05: Tamanho vs. Nº Revisões] | Correlação de Spearman: {corr_size:.3f}, p-valor: {p_size:.3g}")

    corr_time, p_time = spearmanr(df['analysis_time_hours'], df['num_reviews'])
    print(f"[RQ06: Tempo vs. Nº Revisões] | Correlação de Spearman: {corr_time:.3f}, p-valor: {p_time:.3g}")

    corr_desc, p_desc = spearmanr(df['description_length'], df['num_reviews'])
    print(f"[RQ07: Descrição vs. Nº Revisões] | Correlação de Spearman: {corr_desc:.3f}, p-valor: {p_desc:.3g}")

    # --- RQ08: Relação entre as Interações e o Número de Revisões ---
    corr_comm, p_comm = spearmanr(df['num_comments'], df['num_reviews'])
    corr_part, p_part = spearmanr(df['num_participants'], df['num_reviews'])
    print(f"[RQ08: Comentários vs. Nº Revisões] | Correlação de Spearman: {corr_comm:.3f}, p-valor: {p_comm:.3g}")
    print(f"[RQ08: Participantes vs. Nº Revisões] | Correlação de Spearman: {corr_part:.3f}, p-valor: {p_part:.3g}")

    plt.figure(figsize=(8, 6))
    sample_df = df.sample(n=min(len(df), 2000), random_state=42)
    sns.regplot(x='num_comments', y='num_reviews', data=sample_df,
                scatter_kws={'alpha':0.3, 's':25},
                line_kws={'color':'red', 'linewidth':2})
    plt.title(f'RQ08: Comentários vs. Número de Revisões\n(Correlação Spearman: {corr_comm:.2f})', fontsize=14)
    plt.xlabel('Número de Comentários')
    plt.ylabel('Número de Revisões')
    plt.xscale('log')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'RQ08_correlacao_comentarios_revisoes.png'))
    plt.close()

    print(f"\n--- Análise Finalizada ---\nGráficos salvos na pasta: '{OUTPUT_DIR}'")

if __name__ == '__main__':
    main()