# Projeto de Teoria da Computação: Análise de Algoritmos de Busca de Padrão

## Visão Geral

Este repositório contém o desenvolvimento do projeto para a disciplina de **Teoria da Computação** da **CESAR School**, ministrada pelo Prof. Daniel Bezerra.

O objetivo do projeto é realizar uma análise teórica e prática detalhada sobre a complexidade de tempo de um algoritmo sorteado. O algoritmo designado para esta equipe foi o **KMP ou Rabin-Karp**, para busca de padrões em strings.

As implementações foram realizadas em **C** e **Python** para comparar a performance e analisar o comportamento do algoritmo em diferentes cenários.

## Equipe

* Antônio Augusto de Arruda Laprovitera
* Henrique Figuêiredo Tefile
* Julia Torres de Barros
* Maria Cláudia Rodrigues Corrêa de Oliveira Andrade

## Objetivos do Projeto

1.  **Descrição do Algoritmo:** Apresentar o problema resolvido, a lógica geral e o pseudocódigo.
2.  **Classificação Assintótica:** Realizar a análise de complexidade usando as notações Big-Ο, Big-Ω e Big-Θ.
3.  **Análise de Casos:** Estudar o melhor caso, pior caso e caso médio de execução.
4.  **Simulação Prática:** Executar o algoritmo com entradas de diferentes tamanhos (pequenas, médias, grandes) e coletar métricas de tempo de execução (média e desvio padrão).
5.  **Análise Comparativa:** Gerar gráficos e tabelas para comparar os resultados práticos com a complexidade teórica esperada e a performance entre as linguagens C e Python.
6.  **Reflexão Final:** Discutir se o algoritmo pertence à classe P e analisar problemas semelhantes no contexto de NP-completude.

## Estrutura do Repositório

```
.
├── c_implementation/           # Código-fonte da implementação em C
├── python_implementation/      # Código-fonte da implementação em Python
├── analysis_scripts/          # Scripts para automação de testes e geração de gráficos
│   ├── benchmark_results.csv  # Resultados dos benchmarks em C
│   ├── benchmark_results_py.csv # Resultados dos benchmarks em Python
│   ├── plot_results.py       # Script para gerar gráficos comparativos
│   ├── run_c_benchmark.py    # Script para executar testes em C
│   └── run_py_benchmark.py   # Script para executar testes em Python
├── data/                     # Diretório de dados para testes
│   ├── base.txt             # Arquivo base para geração de casos de teste
│   └── generated/           # Arquivos de teste gerados
└── README.md                # Este arquivo
```

## Como Executar

### Pré-requisitos

* Compilador C (GCC ou Clang)
* Python 3.x
* Bibliotecas Python:
  * matplotlib
  * pandas (para análise de dados)
  * numpy (para cálculos estatísticos)

### Implementação em C

1.  Navegue até o diretório `c_implementation`:
    ```bash
    cd c_implementation
    ```
2.  Compile o programa (exemplo usando GCC):
    ```bash
    gcc -o kmp_c main.c -O2
    ```
3.  Execute o programa:
    ```bash
    ./kmp_c <arquivo_texto> <padrao_busca>
    ```

### Implementação em Python

1.  Navegue até o diretório `python_implementation`:
    ```bash
    cd python_implementation
    ```
2.  (Opcional, mas recomendado) Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Execute o script:
    ```bash
    python main.py <arquivo_texto> <padrão_busca>
    ```

## Entregas

* **Entrega 1 (Definição da Equipe):** 24/10/2025
* **Entrega 2 (Projeto Final):** 30/11/2025
* **Apresentações:** 01 e 10 de Dezembro de 2025
