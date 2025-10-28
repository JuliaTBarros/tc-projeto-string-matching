# Projeto de Teoria da Computação: Análise de Algoritmos de Busca de Padrão

## Visão Geral

[cite_start]Este repositório contém o desenvolvimento do projeto para a disciplina de **Teoria da Computação** [cite: 3] [cite_start]da **CESAR School** [cite: 1, 2][cite_start], ministrada pelo Prof. Daniel Bezerra[cite: 4].

[cite_start]O objetivo do projeto é realizar uma análise teórica e prática detalhada sobre a complexidade de tempo de um algoritmo sorteado[cite: 8, 9]. [cite_start]O algoritmo designado para esta equipe foi o **KMP ou Rabin-Karp**, para busca de padrões em strings[cite: 29].

[cite_start]As implementações foram realizadas em **C** e **Python** para comparar a performance e analisar o comportamento do algoritmo em diferentes cenários[cite: 9].

## Equipe

* [Nome do Integrante 1]
* [Nome do Integrante 2]
* [Nome do Integrante 3]
* [Nome do Integrante 4]

## Objetivos do Projeto

[cite_start]Conforme a descrição do projeto[cite: 7], os principais objetivos são:

1.  [cite_start]**Descrição do Algoritmo:** Apresentar o problema resolvido, a lógica geral e o pseudocódigo[cite: 10].
2.  [cite_start]**Classificação Assintótica:** Realizar a análise de complexidade usando as notações Big-Ο, Big-Ω e Big-Θ[cite: 11].
3.  [cite_start]**Análise de Casos:** Estudar o melhor caso, pior caso e caso médio de execução[cite: 16].
4.  [cite_start]**Simulação Prática:** Executar o algoritmo com entradas de diferentes tamanhos (pequenas, médias, grandes) e coletar métricas de tempo de execução (média e desvio padrão)[cite: 13, 14].
5.  [cite_start]**Análise Comparativa:** Gerar gráficos e tabelas para comparar os resultados práticos com a complexidade teórica esperada e a performance entre as linguagens C e Python[cite: 15].
6.  [cite_start]**Reflexão Final:** Discutir se o algoritmo pertence à classe P e analisar problemas semelhantes no contexto de NP-completude[cite: 17].

## Estrutura do Repositório

```
.
├── c_implementation/           # Código-fonte da implementação em C
├── python_implementation/      # Código-fonte da implementação em Python
├── analysis_scripts/           # Scripts para automação de testes e geração de gráficos
├── report/                     # Relatório final em PDF e materiais de apoio
├── presentation/               # Slides da apresentação final
└── README.md                   # Este arquivo
```

## Como Executar

### Pré-requisitos

* Compilador C (GCC ou Clang)
* Python 3.x
* Bibliotecas Python (ex: `matplotlib`, `pandas` - a serem especificadas)

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

* [cite_start]**Entrega 1 (Definição da Equipe):** 24/10/2025 [cite: 34]
* [cite_start]**Entrega 2 (Projeto Final):** 30/11/2025 [cite: 37]
* [cite_start]**Apresentações:** 01 e 10 de Dezembro de 2025 [cite: 43]
