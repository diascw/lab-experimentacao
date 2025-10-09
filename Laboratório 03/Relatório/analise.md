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
