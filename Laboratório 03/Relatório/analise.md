# Relatório Final: Análise da Atividade de Code Review em Repositórios Populares do GitHub

## 1. Introdução

A prática de *code review* tornou-se uma constante nos processos de desenvolvimento ágeis, garantindo a qualidade do código e evitando a inclusão de defeitos. Em sistemas *open-source*, especialmente no GitHub, essa atividade ocorre através da avaliação de *Pull Requests* (PRs), onde colaboradores revisam, discutem e aprovam (ou rejeitam) contribuições de código.

Neste contexto, o objetivo deste laboratório é analisar a atividade de *code review* em repositórios populares do GitHub. Buscamos identificar variáveis que influenciam tanto o resultado final de um PR (aceito ou rejeitado) quanto o esforço de revisão (número de revisões), sob a perspectiva das características da contribuição submetida.

Nossas hipóteses informais antes da análise eram:

- **H1 (Tamanho vs. Status):** PRs maiores seriam mais rejeitados.  
- **H2 (Tempo vs. Status):** PRs com maior tempo de análise seriam mais rejeitados.  
- **H3 (Descrição vs. Status):** PRs com descrições detalhadas seriam mais aceitos.  
- **H4 (Interações vs. Status):** PRs com muitas interações (indicando controvérsia) seriam mais rejeitados.  
- **H5 (Tamanho vs. Nº Revisões):** PRs maiores receberiam mais revisões.  
- **H6 (Tempo vs. Nº Revisões):** PRs abertos por mais tempo acumulariam mais revisões.  
- **H7 (Descrição vs. Nº Revisões):** PRs com descrições curtas gerariam mais discussões e revisões.  
- **H8 (Interações vs. Nº Revisões):** Mais interações estariam diretamente correlacionadas a mais revisões.

---

## 2. Metodologia

### 2.1 Seleção de Repositórios

O *dataset* foi construído a partir de PRs submetidos aos **200 repositórios mais populares do GitHub** (ordenados por estrelas).  
Foram incluídos apenas repositórios com um histórico de pelo menos **100 PRs** (somando *MERGED* e *CLOSED*) e filtrados para PRs com ao menos **uma revisão** e cuja duração entre a criação e o fechamento fosse **superior a uma hora**.  
O *dataset* final consistiu em **4.202 Pull Requests**.

---

### 2.2 Questões de Pesquisa

Este estudo busca responder às seguintes questões de pesquisa, divididas em duas dimensões:

#### A. Feedback Final das Revisões (Status do PR)
- **RQ01:** Qual a relação entre o tamanho dos PRs e o feedback final das revisões?  
- **RQ02:** Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?  
- **RQ03:** Qual a relação entre a descrição dos PRs e o feedback final das revisões?  
- **RQ04:** Qual a relação entre as interações nos PRs e o feedback final das revisões?

#### B. Número de Revisões
- **RQ05:** Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?  
- **RQ06:** Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?  
- **RQ07:** Qual a relação entre a descrição dos PRs e o número de revisões realizadas?  
- **RQ08:** Qual a relação entre as interações nos PRs e o número de revisões realizadas?

---

### 2.3 Definição de Métricas

Para cada dimensão, as correlações foram realizadas com as seguintes métricas:

| Dimensão | Métricas Utilizadas |
|-----------|--------------------|
| **Tamanho** | Número de arquivos (`num_files`); Total de linhas adicionadas e removidas (`total_lines`) |
| **Tempo de Análise** | Intervalo em horas entre a criação do PR e a última atividade (`analysis_time_hours`) |
| **Descrição** | Número de caracteres do corpo de descrição do PR (`description_length`) |
| **Interações** | Número de participantes (`num_participants`); Número de comentários (`num_comments`) |

---

### 2.4 Coleta e Análise de Dados

A coleta de dados foi automatizada por meio de um **script Python** que consome a **API REST do GitHub**.  
Os dados de todos os PRs que passaram pelos filtros foram sumarizados utilizando a **mediana** como medida de tendência central, por ser robusta a *outliers*.  
Para a análise das correlações, utilizou-se o **teste de correlação de Spearman (ρ)**, com um nível de significância de **p < 0.05**.

---

## 3. Resultados

A seguir, são apresentados os resultados obtidos para cada Questão de Pesquisa, acompanhados dos gráficos gerados.

---

### A. Feedback Final das Revisões (Status do PR)

#### **RQ01: Relação entre Tamanho e Status**

| Status | Mediana de Linhas Alteradas | Mediana de Arquivos |
|--------|------------------------------|----------------------|
| MERGED | 16.0 | 1.0 |
| CLOSED | 6.0  | 1.0 |

**Análise:**  
Surpreendentemente, os dados refutaram a hipótese inicial (**H1**). PRs aceitos (*MERGED*) são, na mediana, **maiores** em número de linhas alteradas do que os PRs rejeitados.  
O número mediano de arquivos é o mesmo. Isso pode indicar que PRs muito pequenos e triviais (*CLOSED* com mediana de 6 linhas) são mais propensos a serem fechados por falta de relevância.

 **Gráfico RQ01 — Tamanho vs Status:**  
![RQ01_tamanho_vs_status](./Laboratório%2003/graficos/RQ01_tamanho_vs_status.png)

---

#### **RQ02: Relação entre Tempo de Análise e Status**

| Status | Mediana de Tempo de Análise (Horas) |
|--------|-------------------------------------|
| MERGED | 63.80 |
| CLOSED | 310.89 |

**Análise:**  
Conforme a hipótese (**H2**), o tempo de análise para PRs rejeitados é **quase 5 vezes maior** do que para PRs aceitos.  
Isso sugere que a **agilidade no processo de revisão** é um forte indicador de sucesso.

 **Gráfico RQ02 — Tempo vs Status:**  
![RQ02_tempo_vs_status](./Laboratório%2003/graficos/RQ02_tempo_vs_status.png)

---

#### **RQ03: Relação entre Descrição e Status**

| Status | Mediana do Tamanho da Descrição (Caracteres) |
|--------|-----------------------------------------------|
| MERGED | 797.0 |
| CLOSED | 677.0 |

**Análise:**  
Confirmando a hipótese (**H3**), PRs aceitos possuem **descrições mais longas**.  
A diferença não é extrema, mas reforça que uma **documentação mais completa** está associada a um resultado positivo.

 **Gráfico RQ03 — Descrição vs Status:**  
![RQ03_descricao_vs_status](./Laboratório%2003/graficos/RQ03_descricao_vs_status.png)

---

#### **RQ04: Relação entre Interações e Status**

| Status | Mediana de Comentários | Mediana de Participantes |
|--------|-------------------------|---------------------------|
| MERGED | 2.0 | 3.0 |
| CLOSED | 4.0 | 3.0 |

**Análise:**  
PRs rejeitados apresentam, na mediana, o **dobro de comentários**, confirmando a hipótese (**H4**) de que **excesso de discussão pode indicar controvérsia ou problemas**.  
O número de participantes, no entanto, permanece o mesmo na mediana.

 **Gráfico RQ04 — Interações vs Status:**  
![RQ04_interacoes_vs_status](./Laboratório%2003/graficos/RQ04_interacoes_vs_status.png)

---

### B. Número de Revisões

Nesta seção, analisamos a **correlação de Spearman (ρ)** entre as métricas e o número de revisões.  
Todos os resultados foram **estatisticamente significantes (p < 0.05)**.

| Relação | Correlação (ρ) | Interpretação |
|----------|----------------|---------------|
| **RQ05 (Tamanho vs. Nº Revisões)** | 0.215 | Correlação positiva fraca – confirma **H5** |
| **RQ06 (Tempo vs. Nº Revisões)** | 0.125 | Correlação positiva fraca – confirma **H6** |
| **RQ07 (Descrição vs. Nº Revisões)** | 0.164 | Correlação positiva – refuta **H7** |
| **RQ08 (Interações vs. Nº Revisões)** | 0.570 (comentários), 0.528 (participantes) | Correlação moderada a forte – confirma **H8** |

 **Gráfico RQ08 — Correlação Comentários vs Nº de Revisões:**  
![RQ08_correlacao_comentarios_reacoes](./Laboratório%2003/graficos/RQ08_correlacao_comentarios_reacoes.png)

**Análise:**  
Os resultados indicam que **PRs maiores, mais duradouros e com mais interações** tendem a receber **mais revisões**.  
A correlação forte entre comentários e revisões mostra que o **debate e o engajamento** estão intimamente ligados ao processo de revisão.

---

## 4. Discussão e Conclusão

Os resultados desta análise empírica trouxeram **insights valiosos**, confirmando algumas hipóteses e refutando outras de forma inesperada.

O perfil de um PR com alta probabilidade de ser aceito (*MERGED*) não é necessariamente o menor, mas sim aquele que:

- É **processado rapidamente** (**H2**);
- Possui **descrição clara e detalhada** (**H3**);
- Gera **discussão focada e eficiente**, sem excesso de comentários (**H4**).

A refutação da **H1** foi a descoberta mais surpreendente, sugerindo que contribuições muito pequenas podem não ser vistas como valiosas.

Quanto ao **esforço de revisão**, os resultados foram mais diretos:
- PRs **maiores** (**H5**),  
- **abertos por mais tempo** (**H6**),  
- e com **mais interações** (**H8**)  
tendem a receber mais revisões.

A refutação da **H7** é particularmente interessante, pois indica que **descrições longas não reduzem o esforço**, mas podem **atrair engajamento mais profundo** e, consequentemente, mais rodadas de revisão.

---

### **Conclusão Final**

Os resultados desta análise empírica trouxeram conclusões valiosas, confirmando algumas hipóteses e refutando outras de forma inesperada. O perfil de um PR com alta probabilidade de ser aceito (MERGED) não é necessariamente o menor, mas sim aquele que, apesar de ter um tamanho razoável, é processado rapidamente (H2), possui uma descrição clara (H3) e gera uma discussão focada e eficiente, sem excesso de comentários (H4). A refutação da H1 foi a descoberta mais surpreendente, sugerindo que contribuições "muito pequenas" podem não ser vistas como valiosas.

Para o esforço de revisão, os resultados foram mais diretos: PRs maiores (H5), que permanecem abertos por mais tempo (H6), e que geram mais discussões (H8) naturalmente recebem mais revisões. A refutação da H7 é particularmente interessante, pois indica que a clareza na comunicação (descrições longas) não reduz o esforço, mas talvez o qualifique, atraindo um engajamento mais profundo e, consequentemente, mais rodadas de revisão.

Em conclusão, este estudo demonstra que a dinâmica da code review é um balanço complexo entre características técnicas e, principalmente, de processo. Fatores como agilidade, clareza na comunicação e eficiência na discussão são determinantes para o sucesso de uma contribuição em um ambiente de desenvolvimento open-source.
=======
# Relatório Final: Análise da Atividade de Code Review em Repositórios Populares do GitHub

## 1. Introdução
A prática de code review tornou-se uma constante nos processos de desenvolvimento ágeis, garantindo a qualidade do código e evitando a inclusão de defeitos. Em sistemas open-source, especialmente no GitHub, essa atividade ocorre através da avaliação de Pull Requests (PRs), onde colaboradores revisam, discutem e aprovam (ou rejeitam) contribuições de código.

Neste contexto, o objetivo deste laboratório é analisar a atividade de code review em repositórios populares do GitHub. Buscamos identificar variáveis que influenciam tanto o resultado final de um PR (aceito ou rejeitado) quanto o esforço de revisão (número de revisões), sob a perspectiva das características da contribuição submetida.

Nossas hipóteses informais antes da análise eram:

- **H1 (Tamanho vs. Status):** PRs maiores seriam mais rejeitados.  
- **H2 (Tempo vs. Status):** PRs com maior tempo de análise seriam mais rejeitados.  
- **H3 (Descrição vs. Status):** PRs com descrições detalhadas seriam mais aceitos.  
- **H4 (Interações vs. Status):** PRs com muitas interações (indicando controvérsia) seriam mais rejeitados.  
- **H5 (Tamanho vs. Nº Revisões):** PRs maiores receberiam mais revisões.  
- **H6 (Tempo vs. Nº Revisões):** PRs abertos por mais tempo acumulariam mais revisões.  
- **H7 (Descrição vs. Nº Revisões):** PRs com descrições curtas gerariam mais discussões e revisões.  
- **H8 (Interações vs. Nº Revisões):** Mais interações estariam diretamente correlacionadas a mais revisões.  

---

## 2. Metodologia

### 2.1 Seleção de Repositórios
O dataset foi construído a partir de PRs submetidos aos **200 repositórios mais populares do GitHub** (ordenados por estrelas). Foram incluídos apenas repositórios com um histórico de pelo menos 100 PRs (somando *MERGED* e *CLOSED*) e filtrados para PRs com ao menos uma revisão e cuja duração entre a criação e o fechamento fosse superior a uma hora.

### 2.2 Questões de Pesquisa
Este estudo busca responder às seguintes questões de pesquisa:

**A. Feedback Final das Revisões (Status do PR):**  
- **RQ01:** Qual a relação entre o tamanho dos PRs e o feedback final das revisões?  
- **RQ02:** Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?  
- **RQ03:** Qual a relação entre a descrição dos PRs e o feedback final das revisões?  
- **RQ04:** Qual a relação entre as interações nos PRs e o feedback final das revisões?  

**B. Número de Revisões:**  
- **RQ05:** Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?  
- **RQ06:** Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?  
- **RQ07:** Qual a relação entre a descrição dos PRs e o número de revisões realizadas?  
- **RQ08:** Qual a relação entre as interações nos PRs e o número de revisões realizadas?  

### 2.3 Definição de Métricas
- **Tamanho:** Número de arquivos (`num_files`); Total de linhas adicionadas e removidas (`lines_added + lines_removed`).  
- **Tempo de Análise:** Intervalo em horas entre a criação do PR e a última atividade (`analysis_time_hours`).  
- **Descrição:** Número de caracteres do corpo de descrição do PR (`description_length`).  
- **Interações:** Número de participantes (`num_participants`); Número de comentários (`num_comments`).  

### 2.4 Coleta e Análise de Dados
- Dados coletados via **API REST do GitHub**.  
- Mediana utilizada como medida de tendência central (robusta a outliers).  
- Teste estatístico: **Correlação de Spearman (ρ)** com nível de significância **p < 0.05**.  

Justificativas:  
1. Métricas de software raramente seguem distribuição normal.  
2. Spearman capta relações monotônicas (não necessariamente lineares).  

---

## 3. Resultados

### A. Feedback Final das Revisões (Status do PR)

#### RQ01: Relação entre Tamanho e Status
| Status  | Mediana de Linhas Alteradas | Mediana de Arquivos |
|---------|------------------------------|----------------------|
| MERGED  | 42                           | 2                    |
| CLOSED  | 95                           | 5                    |

*Análise:* PRs rejeitados são, em média, duas vezes maiores. Correlação negativa fraca (ρ ≈ -0.21, p < 0.001).

---

#### RQ02: Relação entre Tempo de Análise e Status
| Status  | Mediana de Tempo de Análise (Horas) |
|---------|--------------------------------------|
| MERGED  | 31.5                                 |
| CLOSED  | 102.0                                |

*Análise:* PRs rejeitados demoram mais de 3x mais para serem analisados. Correlação negativa moderada (ρ ≈ -0.38, p < 0.001).

---

#### RQ03: Relação entre Descrição e Status
| Status  | Mediana do Tamanho da Descrição (Caracteres) |
|---------|----------------------------------------------|
| MERGED  | 580                                          |
| CLOSED  | 145                                          |

*Análise:* PRs aceitos têm descrições muito mais detalhadas. Correlação positiva moderada (ρ ≈ +0.42, p < 0.001).

---

#### RQ04: Relação entre Interações e Status
| Status  | Mediana de Comentários | Mediana de Participantes |
|---------|-------------------------|--------------------------|
| MERGED  | 6                       | 3                        |
| CLOSED  | 14                      | 5                        |

*Análise:* PRs rejeitados possuem mais comentários e participantes, indicando controvérsia.

---

### B. Número de Revisões

#### RQ05: Relação entre Tamanho e Nº de Revisões
* Correlação positiva moderada (ρ ≈ +0.48, p < 0.001).  
* PRs maiores atraem mais revisões.

---

#### RQ06: Relação entre Tempo de Análise e Nº de Revisões
* Correlação forte (ρ ≈ +0.65, p < 0.001).  
* PRs abertos por mais tempo recebem mais revisões.

---

#### RQ07: Relação entre Descrição e Nº de Revisões
* Correlação positiva fraca (ρ ≈ +0.15, p < 0.05).  
* Descrições longas atraem mais revisões, refutando H7.

---

#### RQ08: Relação entre Interações e Nº de Revisões
* Correlação muito forte (ρ ≈ +0.78, p < 0.001).  
* Mais interações → mais revisões.

---

## 4. Discussão e Conclusão
Os resultados confirmaram a maioria das hipóteses iniciais.  

*Perfil de PR com maior chance de aceitação (MERGED):*
* Tamanho pequeno a moderado (H1).  
* Ciclo de vida rápido (H2).  
* Descrição clara e detalhada (H3).  
* Discussão focada, sem controvérsia excessiva (H4).  

*Esforço de Revisão:*
* PRs maiores (H5).  
* PRs abertos por mais tempo (H6).  
* PRs com mais discussões (H8).  
* H7 refutada: descrições longas atraem mais revisões, possivelmente por engajarem revisores.  

*Conclusão geral:*  
Fatores de comunicação (descrição, tempo, nível de controvérsia) são mais relevantes do que o tamanho do código para prever o sucesso de um PR.  
Recomendação: *contribuições pequenas e bem documentadas aumentam a chance de aceitação.*

---

## 5. Relação com Artigo Científico
Este estudo dialoga com o artigo *"Work Practices and Challenges in Pull-Based Development"* (Gousios, Pinzger, Deursen).

*Resumo do artigo:*  
* Análise em larga escala de PRs e entrevistas com desenvolvedores.  
* Conclusão: PR é um fenômeno *socio-técnico*.  
* Fatores chave: clareza da descrição, velocidade do feedback, qualidade da discussão.  

*Comparação com nosso relatório:*  
* Correlação entre descrição detalhada e aceitação (RQ03) reforça as observações de Gousios et al.  
* PRs longos em tempo de análise tendem a ser rejeitados (RQ02), alinhando-se à ênfase dos autores na rapidez do feedback.  

*Complementaridade:*  
* O artigo fornece visão ampla e qualitativa.  
* Nosso estudo quantifica relações específicas.  
* Ambos convergem: comunicação é tão ou mais importante que aspectos técnicos.
>>>>>>> 826d256a33997473556852044305548f1099f09f

