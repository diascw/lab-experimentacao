# RELATÓRIO DE ANÁLISE DOS 1000 REPOSITÓRIOS MAIS POPULARES DO GITHUB

## 1. INTRODUÇÃO

Este relatório apresenta uma análise inicial sobre as características dos 1000 repositórios open-source mais populares do GitHub, definidos pelo número de estrelas. O objetivo é compreender padrões de desenvolvimento, manutenção e popularidade desses projetos, a partir da coleta de dados via API GraphQL.

### Hipóteses Informais

•⁠ ⁠H1: Repositórios populares tendem a ser projetos maduros (mais antigos).  
•⁠ ⁠H2: Repositórios populares recebem muitas contribuições externas (alto número de pull requests aceitas).  
•⁠ ⁠H3: Repositórios populares lançam releases frequentemente.  
•⁠ ⁠H4: Repositórios populares são atualizados com regularidade (última atualização recente).  
•⁠ ⁠H5: Repositórios populares utilizam linguagens mainstream (JavaScript, Python, Java, TypeScript).  
•⁠ ⁠H6: Repositórios populares possuem boa manutenção (alto percentual de issues fechadas).

---

## 2. METODOLOGIA

Os dados foram coletados por meio da API GraphQL do GitHub, utilizando um script em Python desenvolvido especificamente para este trabalho.

### Métricas Extraídas

•⁠ ⁠Data de criação (para medir idade/maturidade)  
•⁠ ⁠Data da última atualização (para medir atividade recente)  
•⁠ ⁠Número de pull requests aceitas (colaboração externa)  
•⁠ ⁠Número total de releases (frequência de versões formais)  
•⁠ ⁠Linguagem primária do repositório  
•⁠ ⁠Número total de issues e issues fechadas (qualidade da manutenção)

### Procedimento

1.⁠ ⁠Consulta GraphQL com paginação até alcançar os 1000 repositórios mais estrelados.  
2.⁠ ⁠Armazenamento dos dados em formatos CSV e JSON para análise posterior.  
3.⁠ ⁠Definição das hipóteses preliminares com base em expectativas teóricas.  
4.⁠ ⁠A análise estatística detalhada (medianas, distribuições, comparação por linguagens) será realizada no Laboratório 3.

---

## 3. RESULTADOS PRELIMINARES

Como esta é a fase de coleta, ainda não foram realizadas análises numéricas detalhadas. Entretanto, espera-se que os resultados indiquem:

•⁠ ⁠RQ01 – Idade: a maioria dos projetos populares seja relativamente madura, com anos de existência.  
•⁠ ⁠RQ02 – Contribuição externa: sistemas grandes (ex.: VS Code, TensorFlow) apresentem milhares de PRs aceitas, mas a mediana seja moderada.  
•⁠ ⁠RQ03 – Releases: nem todos os projetos utilizam releases formais, o que pode reduzir a mediana.  
•⁠ ⁠RQ04 – Atualizações: muitos projetos tenham sido atualizados recentemente, indicando atividade ativa.  
•⁠ ⁠RQ05 – Linguagens: prevalência de linguagens populares (JavaScript, TypeScript, Python, Go, Java).  
•⁠ ⁠RQ06 – Issues fechadas: um percentual significativo de issues fechadas, refletindo manutenção constante.

---

## 4. DISCUSSÃO

•⁠ ⁠H1: Projetos antigos provavelmente dominam, pois tiveram tempo para acumular estrelas.  
•⁠ ⁠H2: A colaboração externa deve ser relevante, mas varia de acordo com a governança.  
•⁠ ⁠H3: Pode ser parcialmente refutada, pois releases não são sempre usadas como forma de distribuição.  
•⁠ ⁠H4: Confirmada preliminarmente, visto que projetos populares costumam ter commits recentes.  
•⁠ ⁠H5: Confirmada, linguagens mainstream devem dominar o ranking.  
•⁠ ⁠H6: Deve se confirmar, indicando boa taxa de resolução de issues.

---

## 5. CONCLUSÃO

Nesta etapa (Lab01S02), foi realizada a coleta completa dos 1000 repositórios mais populares do GitHub e definida a estrutura inicial de análise com hipóteses informais.  
Os dados já estão armazenados em CSV e JSON para permitir a próxima fase de análise estatística (Lab01S03), quando serão apresentados os resultados quantitativos e comparações entre linguagens.
