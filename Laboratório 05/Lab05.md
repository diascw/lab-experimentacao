# Lab05S01: Desenho e Preparação do Experimento (GraphQL vs REST)

**Disciplina:** Laboratório de Experimentação de Software  
**Experimento:** Comparação de Desempenho e Eficiência entre APIs REST e GraphQL

## 1. Desenho do Experimento

O objetivo é avaliar quantitativamente os benefícios da adoção de GraphQL em comparação ao REST, focando em um cenário de consumo seletivo de dados (evitando over‑fetching).

### A. Hipóteses

Seja μ a média populacional.

- RQ1. Respostas às consultas GraphQL são mais rápidas que respostas às consultas REST?
  - H0_time: μ_GraphQL ≥ μ_REST (GraphQL não é mais rápido que REST)
  - H1_time: μ_GraphQL < μ_REST (GraphQL é mais rápido que REST)

- RQ2. Respostas às consultas GraphQL têm tamanho menor que respostas às consultas REST?
  - H0_size: μ_GraphQL ≥ μ_REST (GraphQL não é menor que REST)
  - H1_size: μ_GraphQL < μ_REST (GraphQL é menor que REST)

### B. Variáveis

- Independente (fator): Tipo de API (REST vs GraphQL)
- Dependentes (métricas):
  1. Tempo de resposta (time_ms)
  2. Tamanho da resposta (size_bytes)

### C. Tratamentos

- REST (controle): GET do recurso completo (over‑fetching)
- GraphQL (experimental): POST com query solicitando apenas `name`, `species`, `status` (exact‑fetching)

### D. Objetos Experimentais

- REST: https://rickandmortyapi.com/api/character/{id}
- GraphQL: https://rickandmortyapi.com/graphql

### E. Tipo de Projeto Experimental

- Experimento controlado in‑vitro com design pareado: cada ID é consultado em ambos os tratamentos.

### F. Quantidade de Medições

- Amostra: 50 personagens (IDs 1..50) → 100 observações (50 REST + 50 GraphQL)

### G. Ameaças à Validade e Mitigações

1. Latência de rede: intercalar tratamentos e embaralhar IDs (seed fixa).  
2. Cold start: rodada de warm‑up descartada.  
3. Processamento no cliente: medir apenas a chamada de I/O (time.perf_counter envolvendo requests).  
4. Generalização: resultados válidos para a API escolhida; outras implementações podem diferir.

## 2. Preparação do Experimento

- Linguagem: Python 3.x  
- Bibliotecas: requests, pandas, (matplotlib, seaborn para S03), opcionalmente SciPy.  
- Scripts:
  - lab05_experiment.py → coleta e gera `experiment_results.csv`  
  - lab05_analyze_dashboard.py → análise, testes e gráficos  
- Ambiente (preencher ao executar): CPU, SO, rede, data/hora, local.

## 3. Como Executar

1. Coleta:  
   ```bash
   python lab05_experiment.py --trials 50 --seed 42 --out experiment_results.csv
   ```
2. Análise e dashboard:  
   ```bash
   python lab05_analyze_dashboard.py --csv experiment_results.csv
   ```

Saídas esperadas: `experiment_results.csv`, `lab05_report.md`, `dashboard_boxplots.png`, `paired_time.png`, `paired_size.png`.
