# Lab05S01: Desenho e Preparação do Experimento (GraphQL vs REST)

**Disciplina:** Laboratório de Experimentação de Software
**Experimento:** Comparação de Desempenho e Eficiência entre APIs REST e GraphQL

---

## 1. Desenho do Experimento

O objetivo deste experimento é avaliar quantitativamente os benefícios da adoção de GraphQL em comparação ao REST, focando especificamente em um cenário de consumo seletivo de dados (evitando *over-fetching*).

### A. Hipóteses

Para responder às perguntas de pesquisa, formulamos as seguintes hipóteses estatísticas, onde $\mu$ representa a média populacional:

**RQ1. Respostas às consultas GraphQL são mais rápidas que respostas às consultas REST?**
* **Hipótese Nula ($H_{0\_time}$):** $\mu_{GraphQL} \ge \mu_{REST}$
    * *Interpretação:* O tempo médio de resposta do GraphQL é igual ou maior (pior) que o do REST.
* **Hipótese Alternativa ($H_{1\_time}$):** $\mu_{GraphQL} < \mu_{REST}$
    * *Interpretação:* O tempo médio de resposta do GraphQL é estritamente menor (melhor) que o do REST.

**RQ2. Respostas às consultas GraphQL têm tamanho menor que respostas às consultas REST?**
* **Hipótese Nula ($H_{0\_size}$):** $\mu_{GraphQL} \ge \mu_{REST}$
    * *Interpretação:* O tamanho médio da resposta do GraphQL é igual ou maior que o do REST.
* **Hipótese Alternativa ($H_{1\_size}$):** $\mu_{GraphQL} < \mu_{REST}$
    * *Interpretação:* O tamanho médio da resposta do GraphQL é estritamente menor que o do REST.

### B. Variáveis

**Variável Independente (Fator):**
* **Tipo de API:** Categorical Nominal (`REST` ou `GraphQL`).

**Variáveis Dependentes (Métricas):**
1.  **Tempo de Resposta (`time_ms`):** Tempo decorrido (em milissegundos) entre o envio da requisição pelo cliente e o recebimento do último byte da resposta.
2.  **Tamanho da Resposta (`size_bytes`):** Tamanho total do corpo (payload) da resposta JSON (em bytes).

### C. Tratamentos

O experimento simula um cliente que necessita apenas de informações parciais de um recurso (Nome, Espécie e Status).

1.  **Tratamento REST (Controle):**
    * Requisição `GET` padrão para o endpoint do recurso.
    * O servidor retorna o objeto completo (Over-fetching).
2.  **Tratamento GraphQL (Experimental):**
    * Requisição `POST` enviando uma *query* específica.
    * Campos solicitados: `name`, `species`, `status`.
    * O servidor retorna apenas os campos solicitados (Exact-fetching).

### D. Objetos Experimentais

Utilizaremos a **Rick and Morty API**, uma API pública que fornece implementações espelhadas em ambas as tecnologias:

* **REST Endpoint:** `https://rickandmortyapi.com/api/character/{id}`
* **GraphQL Endpoint:** `https://rickandmortyapi.com/graphql`

### E. Tipo de Projeto Experimental

* **Tipo:** Experimento Controlado *In-vitro* (Simulado).
* **Design:** **Design Pareado (Paired Design)**.
    * Cada unidade experimental (um ID de personagem específico) será submetida a **ambos** os tratamentos.
    * Isso remove a variância que poderia ser causada por um personagem ter muito mais dados de histórico que outro, garantindo uma comparação direta.

### F. Quantidade de Medições

* **Tamanho da Amostra:** 50 personagens distintos (IDs 1 a 50).
* **Total de Observações:** 100 medições (50 REST + 50 GraphQL).
* **Justificativa:** $N > 30$ permite a aplicação do Teorema Central do Limite para análises estatísticas paramétricas (como o T-Test pareado).

### G. Ameaças à Validade

1.  **Latência de Rede (Validade Interna):** Flutuações na conexão de internet podem distorcer o tempo.
    * *Mitigação:* As requisições serão intercaladas (REST ID 1, GQL ID 1, REST ID 2...) para que condições de rede momentâneas afetem ambos igualmente.
2.  **Cold Start do Servidor (Validade Interna):** A primeira requisição pode ser mais lenta.
    * *Mitigação:* Execução de uma rodada de "aquecimento" (warm-up) descartável antes da coleta de dados.
3.  **Processamento do Cliente (Validade de Construto):** O tempo medido pode incluir o processamento do Python.
    * *Mitigação:* O cronômetro envolverá estritamente a chamada de I/O da biblioteca `requests`.
4.  **Generalização (Validade Externa):** Os resultados são específicos para a implementação da *Rick and Morty API*. Implementações ruins de GraphQL podem ser mais lentas que REST.

---

## 2. Preparação do Experimento

Para executar o desenho acima, foi desenvolvido um script em Python.

**Requisitos:**
* Python 3.x
* Bibliotecas: `requests`, `pandas`

**Estrutura do Script de Coleta (`experiment.py`):**
1.  **Setup:** Define URLs e cabeçalhos.
2.  **Warm-up:** Faz uma requisição simples para cada API para abrir conexões TCP/SSL.
3.  **Iteração:**
    * Loop de 1 a 50 (IDs dos personagens).
    * Mede o tempo e tamanho do `GET` (REST).
    * Mede o tempo e tamanho do `POST` (GraphQL) com a query `{ character(id: "x") { name, species, status } }`.
    * Armazena os dados em uma lista.
4.  **Output:** Salva os dados brutos em `experiment_results.csv` contendo as colunas: `id`, `type`, `time_ms`, `size_bytes`.

Este arquivo CSV será a entrada para a etapa de Análise de Resultados.