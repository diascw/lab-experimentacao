# Análise dos 1000 Repositórios Mais Populares do GitHub

## Resumo

Este estudo analisa os 1000 repositórios mais populares do GitHub, classificados pelo número de estrelas, para identificar padrões em seis áreas principais: idade, contribuições externas, frequência de releases, regularidade de atualizações, linguagens de programação e gerenciamento de *issues*. Os resultados mostram que os repositórios populares são tipicamente projetos maduros, com manutenção ativa e desenvolvidos predominantemente em linguagens como Python, TypeScript e JavaScript.

---

## 1. Introdução

Neste laboratório, investigamos os 1000 repositórios mais estrelados do GitHub para identificar características comuns que contribuem para seu sucesso e sustentabilidade. A análise busca validar um conjunto de hipóteses sobre maturidade, colaboração, manutenção e tecnologia.

### Questões de Pesquisa e Hipóteses

As hipóteses formuladas no início do projeto foram:
* **H1 (Idade):** Repositórios populares tendem a ser projetos maduros (mais antigos).
* **H2 (Contribuições):** Repositórios populares recebem muitas contribuições externas.
* **H3 (Releases):** Repositórios populares lançam novas versões (*releases*) frequentemente.
* **H4 (Atualizações):** Repositórios populares são atualizados com regularidade.
* **H5 (Linguagens):** As linguagens mais comuns são *mainstream* como JavaScript e Python.
* **H6 (Manutenção):** Repositórios populares possuem uma boa taxa de resolução de *issues*.

---

## 2. Metodologia

### Coleta e Análise dos Dados
Os dados foram coletados da API GraphQL do GitHub através de um *script* em Python, focando em métricas como data de criação, *pull requests* aceitas, *releases*, última atualização e *issues*. Os dados brutos, armazenados em formato CSV e JSON, foram processados para calcular a idade dos repositórios, o tempo desde a última atualização e o percentual de *issues* fechadas. A análise utilizou medianas para dados numéricos e distribuições de frequência para dados categóricos (linguagens).

### Visualização
Para apresentar os resultados, foram gerados histogramas, *box plots* e gráficos de pizza e de barras, utilizando as bibliotecas `matplotlib` e `seaborn` em Python, o que permitiu uma visualização clara dos padrões encontrados.

---

## 3. Resultados e Discussão

A seguir, cada hipótese é confrontada com os dados analisados.

### H1: Repositórios populares são projetos maduros (mais antigos)
* **Resultado:** A idade mediana dos repositórios é de aproximadamente **9,3 anos**.
* **Conclusão:** A grande maioria dos projetos populares é madura, com um pico de concentração entre 8 e 12 anos de existência.
* **Hipótese:** **Confirmada.** A popularidade está fortemente correlacionada com o tempo, que permite a construção de uma comunidade sólida e a consolidação do projeto.

<br>
<div align="center">

| ![Gráfico da distribuição de idade dos repositórios.](graficos/rq01_idade_repositorios.png) |
|:---:|
| **Figura 1:** Distribuição da Idade dos Repositórios (em anos). A maioria concentra-se na faixa de 8 a 12 anos, indicando que a maturidade é um fator comum entre projetos populares. |

</div>
<br>

### H2: Repositórios populares recebem muitas contribuições externas
* **Resultado:** A mediana de *pull requests* (PRs) aceitas é de **929**.
* **Conclusão:** Repositórios populares atraem um número significativo de contribuições externas. A escala logarítmica do gráfico evidencia que, embora a mediana seja alta, existem *outliers* com dezenas de milhares de PRs.
* **Hipótese:** **Confirmada.** A visibilidade desses projetos incentiva a colaboração da comunidade.

<br>
<div align="center">

| ![Gráfico da distribuição de pull requests aceitas.](graficos/rq02_pull_requests.png) |
|:---:|
| **Figura 2:** Distribuição de Pull Requests Aceitas. O box plot em escala logarítmica mostra uma mediana elevada e a presença de projetos com altíssimo engajamento. |

</div>
<br>

### H3: Repositórios populares lançam releases frequentemente
* **Resultado:** A mediana de *releases* é de **45**.
* **Conclusão:** Muitos projetos, especialmente ferramentas e *frameworks*, adotam um ciclo de *releases* formais. No entanto, o número é bastante variável, e muitos repositórios (como listas de conteúdo) não utilizam esse recurso.
* **Hipótese:** **Parcialmente confirmada.** O uso de *releases* depende da natureza do projeto, não sendo um indicador universal de popularidade.

<br>
<div align="center">

| ![Gráfico da distribuição do total de releases.](graficos/rq03_releases.png) |
|:---:|
| **Figura 3:** Distribuição do Total de Releases. O gráfico mostra que a maioria dos repositórios que utilizam releases possui menos de 200 versões publicadas. |

</div>
<br>

### H4: Repositórios populares são atualizados com regularidade
* **Resultado:** O tempo mediano desde a última atualização (*push*) é de apenas **7 dias**.
* **Conclusão:** A grande maioria dos repositórios populares está em desenvolvimento ativo, com atualizações ocorrendo semanalmente.
* **Hipótese:** **Confirmada.** Manutenção constante é uma característica chave de projetos relevantes e populares.

<br>
<div align="center">

| ![Gráfico da frequência de atualizações.](graficos/rq04_atualizacao.png) |
|:---:|
| **Figura 4:** Frequência de Atualizações (Dias desde o último push). O histograma mostra uma forte concentração de projetos atualizados em menos de 100 dias. |

</div>
<br>

### H5: Repositórios populares utilizam linguagens mainstream
* **Resultado:** As linguagens mais comuns são **Python** (20.9%), **TypeScript** (18.3%) e **JavaScript** (14.2%).
* **Conclusão:** As três principais linguagens somam mais da metade dos repositórios analisados, refletindo as tendências atuais no mercado.
* **Hipótese:** **Confirmada.** A popularidade das linguagens está diretamente ligada à sua presença nos projetos mais estrelados.

<br>
<div align="center">

| ![Gráfico de pizza com a distribuição das linguagens de programação.](graficos/rq05_linguagens.png) |
|:---:|
| **Figura 5:** Distribuição das 10 Principais Linguagens de Programação. Python, TypeScript e JavaScript dominam, confirmando sua popularidade no ecossistema open-source. |

</div>
<br>

### H6: Repositórios populares possuem boa manutenção
* **Resultado:** A mediana do percentual de *issues* fechadas é de **93.8%**.
* **Conclusão:** Os repositórios mais populares demonstram uma capacidade muito alta de gerenciar e resolver os problemas reportados pela comunidade.
* **Hipótese:** **Confirmada.** Uma boa manutenção, refletida na alta taxa de resolução de *issues*, é um pilar dos projetos de sucesso.

<br>
<div align="center">

| ![Gráfico da distribuição do percentual de issues fechadas.](graficos/rq06_issues_fechadas.png) |
|:---:|
| **Figura 6:** Distribuição do Percentual de Issues Fechadas. O histograma mostra que a grande maioria dos repositórios resolve mais de 80% das issues abertas. |

</div>
<br>

### Análise Comparativa por Linguagem (Bônus)

Ao analisar as métricas por linguagem, observamos padrões interessantes:
* **Rust** se destaca com a maior mediana de estrelas, indicando projetos de alto impacto.
* Projetos em **JavaScript** e **C++** tendem a ser mais antigos, enquanto os em **Rust** são, em média, mais recentes.
* A taxa de resolução de *issues* é alta em todas as linguagens, com **HTML** e **JavaScript** liderando.

<br>
<div align="center">

| ![Gráfico de calor com métricas normalizadas por linguagem.](graficos/rq07_metricas_por_linguagem.png) |
|:---:|
| **Figura 7:** Métricas Normalizadas por Linguagem. O heatmap compara a performance mediana de cada linguagem, revelando os pontos fortes de cada ecossistema. |

</div>
<br>

---

## 4. Conclusão

A análise confirma que a popularidade no GitHub é resultado de um conjunto de características observáveis. Projetos populares são, em sua maioria, **maduros, ativamente mantidos e com forte engajamento comunitário**. A escolha de tecnologias consolidadas como Python, TypeScript e JavaScript também desempenha um papel fundamental.

Os principais achados reforçam que, para um projeto de código aberto prosperar, ele precisa não apenas de uma base técnica sólida, mas também de uma comunidade ativa e de mantenedores responsivos, capazes de gerenciar contribuições e resolver problemas de forma eficiente.
