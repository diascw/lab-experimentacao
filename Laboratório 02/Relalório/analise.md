# Relatório Final: Um Estudo das Características de Qualidade de Sistemas Java

**Autor(a):** Wanessa Dias Costa
**Data:** 19 de Setembro de 2025

## 1. Introdução

No processo de desenvolvimento de sistemas open-source, em que diversos desenvolvedores contribuem em partes diferentes do código, um dos riscos a serem gerenciados diz respeito à evolução dos seus atributos de qualidade interna. Isto é, ao se adotar uma abordagem colaborativa, corre-se o risco de tornar vulnerável aspectos como modularidade, manutenibilidade, ou legibilidade do software produzido. Para tanto, diversas abordagens modernas buscam aperfeiçoar tal processo, através da adoção de práticas relacionadas à revisão de código ou à análise estática através de ferramentas de CI/CD.

Neste contexto, o objetivo deste laboratório é analisar aspectos da qualidade de repositórios desenvolvidos na linguagem Java, correlacionando-os com características do seu processo de desenvolvimento, sob a perspectiva de métricas de produto calculadas através da ferramenta CK.

Nossas **hipóteses informais** antes da análise eram:
- **H1 (Popularidade):** Repositórios mais populares teriam *melhor* qualidade (menor CBO e LCOM).
- **H2 (Maturidade):** Repositórios mais maduros (antigos) teriam *pior* qualidade (maior CBO), refletindo o acúmulo de débito técnico.
- **H3 (Atividade):** Repositórios mais ativos (com mais releases) teriam *melhor* qualidade.
- **H4 (Tamanho):** Repositórios maiores (com mais linhas de código) teriam *pior* qualidade (maior CBO).

## 2. Metodologia

O processo para responder às questões de pesquisa foi executado sobre o universo dos 1.000 repositórios Java mais populares do GitHub. A metodologia consistiu em:
1.  **Mineração de Dados:** Utilizou-se a API REST do GitHub para coletar metadados dos repositórios.
2.  **Extração de Métricas:** A ferramenta de análise estática **CK** foi empregada através de um script de automação para clonar cada repositório e extrair as métricas de qualidade (CBO, DIT, LCOM) e tamanho (LOC).
3.  **Agregação e Análise:** Os dados foram agregados por repositório utilizando a **mediana** como medida de tendência central. A relação entre as variáveis foi investigada visualmente através de **gráficos de dispersão**.

## 3. Resultados

A seguir, são apresentados os resultados para cada Questão de Pesquisa.

### RQ01: Relação entre Popularidade e Qualidade

![Popularidade vs. CBO](graficos/RQ01_Popularidade_cbo_median.png)
![Popularidade vs. DIT](graficos/RQ01_Popularidade_dit_median.png)
![Popularidade vs. LCOM](graficos/RQ01_Popularidade_lcom_median.png)

**Análise:** A análise visual dos gráficos que comparam a popularidade com as métricas de qualidade não revela correlações fortes. As linhas de regressão são quase horizontais, indicando que um aumento na popularidade não está associado a uma mudança clara na qualidade do código.

---

### RQ02: Relação entre Maturidade e Qualidade

![Maturidade vs. CBO](graficos/RQ02_Maturidade_cbo_median.png)
![Maturidade vs. DIT](graficos/RQ02_Maturidade_dit_median.png)
![Maturidade vs. LCOM](graficos/RQ02_Maturidade_lcom_median.png)

**Análise:** A relação entre a maturidade (idade) e a qualidade do código também se mostrou fraca. Para CBO e LCOM, as linhas de regressão são praticamente planas. Para o DIT, observa-se uma tendência positiva extremamente sutil, mas a grande variabilidade dos dados torna a relação pouco confiável.

---

### RQ03: Relação entre Atividade e Qualidade

![Atividade vs. CBO](graficos/RQ03_Atividade_cbo_median.png)
![Atividade vs. DIT](graficos/RQ03_Atividade_dit_median.png)
![Atividade vs. LCOM](graficos/RQ03_Atividade_lcom_median.png)

**Análise:** A atividade, medida pelo número de releases, também não demonstrou ser um forte preditor de qualidade. A grande maioria dos projetos possui um número baixo de releases, e não é possível identificar qualquer padrão ou tendência clara que relacione a atividade com a qualidade do código.

---

### RQ04: Relação entre Tamanho e Qualidade

![Tamanho vs. CBO](graficos/RQ04_Tamanho_cbo_median.png)
![Tamanho vs. DIT](graficos/RQ04_Tamanho_dit_median.png)
![Tamanho vs. LCOM](graficos/RQ04_Tamanho_lcom_median.png)

**Análise:** Contrariando a hipótese inicial, mesmo o tamanho do projeto (LOC Total) não apresentou uma correlação forte com as métricas de qualidade. As linhas de regressão para CBO, LCOM e DIT são quase perfeitamente planas, indicando uma correlação muito fraca ou inexistente.

## 4. Discussão e Conclusão

Os resultados obtidos através da análise visual refutaram a maioria das hipóteses informais. Fatores externos como **popularidade (H1)**, **maturidade (H2)**, **atividade (H3)** e **tamanho (H4)** não mostraram correlações fortes com as métricas de qualidade interna analisadas.

A ausência generalizada de correlações lineares sugere que a qualidade de software, medida por CBO, DIT e LCOM, é um fenômeno complexo, provavelmente influenciado por fatores não medidos neste estudo, como a cultura da equipe de desenvolvimento e a rigidez dos processos de revisão de código.

Em conclusão, este estudo empírico demonstrou que as características de processo de um projeto de software são preditores fracos de sua qualidade estrutural interna. A qualidade parece ser um atributo intrínseco, governado por fatores mais complexos do que seus metadados externos.