# Projeto de Teoria da Computação: Análise de Algoritmos de Busca de Padrão

## Visão Geral

Este repositório contém o desenvolvimento do projeto para a disciplina de **Teoria da Computação** da **CESAR School**, ministrada pelo Prof. Daniel Bezerra.

O objetivo do projeto é realizar uma análise teórica e prática detalhada sobre a complexidade de tempo de um algoritmo sorteado. O algoritmo designado para esta equipe foi o **KMP**, para busca de padrões em strings.

As implementações foram realizadas em **C** e **Python** para comparar a performance e analisar o comportamento do algoritmo em diferentes cenários.

## Equipe

- Antônio Augusto de Arruda Laprovitera
- Henrique Figuêiredo Tefile
- Julia Torres de Barros
- Maria Cláudia Rodrigues Corrêa de Oliveira Andrade

## Objetivos do Projeto

1. **Descrição do Algoritmo:** Apresentar o problema resolvido, a lógica geral e o pseudocódigo.
2. **Classificação Assintótica:** Realizar a análise de complexidade usando as notações Big-Ο, Big-Ω e Big-Θ.
3. **Análise de Casos:** Estudar o melhor caso, pior caso e caso médio de execução.
4. **Simulação Prática:** Executar o algoritmo com entradas de diferentes tamanhos (pequenas, médias, grandes) e coletar métricas de tempo de execução (média e desvio padrão).
5. **Análise Comparativa:** Gerar gráficos e tabelas para comparar os resultados práticos com a complexidade teórica esperada e a performance entre as linguagens C e Python.
6. **Reflexão Final:** Discutir se o algoritmo pertence à classe P e analisar problemas semelhantes no contexto de NP-completude.

## Estrutura do Repositório

```bash
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

- Compilador C (GCC ou Clang)
- Python 3.x
- Bibliotecas Python:
  - matplotlib
  - pandas (para análise de dados)
  - numpy (para cálculos estatísticos)

### 1. Geração de Dados de Teste

Antes de executar qualquer benchmark, é necessário gerar os arquivos de dados. O script `gerar_dados.py` está localizado na raiz do repositório.

1. **Crie o arquivo base (`data/base.txt`):**
   O script precisa de um arquivo de texto inicial para gerar os casos de teste do tipo "Caso Real".

   - Crie um arquivo chamado `base.txt` dentro da pasta `data/`.
   - O arquivo deve ser texto puro (UTF-8) e ter algum conteúdo (alguns parágrafos de Lorem Ipsum ou um livro de domínio público funcionam bem).
   - Exemplo rápido de criação (se não tiver um arquivo pronto):
     Crie o arquivo `data/base.txt` e cole o seguinte texto repetidas vezes até ter alguns KB:
     > "Call me Ishmael. Some years ago--never mind how long precisely--having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world."

2. **Execute o script gerador:**
   A partir da raiz do projeto, execute:

   ```bash
   python gerar_dados.py
   ```

   Isso criará a pasta `data/generated` com arquivos de teste de 100KB a 50MB.

### 2. Implementação em C

1. Navegue até o diretório `c_implementation`:

   ```bash
   cd c_implementation
   ```

2. Compile o programa (exemplo usando GCC):

   ```bash
   gcc -o kmp_c main.c -O2
   ```

   _Nota: No Windows, isso gerará um arquivo `kmp_c.exe`._

3. Execute o programa manualmente (teste unitário):

   - **Linux/macOS:**

     ```bash
     ./kmp_c ../data/base.txt "padrao"
     ```

   - **Windows (CMD/PowerShell):**

     ```cmd
     kmp_c.exe ..\data\base.txt "padrao"
     ```

### 3. Implementação em Python

1. Navegue até o diretório `python_implementation`:

   ```bash
   cd python_implementation
   ```

2. (Opcional, mas recomendado) Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute o script manualmente:

   ```bash
   python main.py <arquivo_texto> <padrão_busca>
   ```

### 4. Execução dos Benchmarks e Análise

Para reproduzir os resultados e gerar os gráficos:

1. Navegue até a pasta de scripts:

   ```bash
   cd analysis_scripts
   ```

2. Execute o benchmark da implementação em C:

   ```bash
   python run_c_benchmark.py
   ```

   _Isso gerará o arquivo `benchmark_results.csv`._

3. Execute o benchmark da implementação em Python:

   ```bash
   python run_py_benchmark.py
   ```

   _Isso gerará o arquivo `benchmark_results_py.csv`._

4. Gere os gráficos comparativos:

   ```bash
   python plot_results.py
   ```

   _Isso gerará as imagens `analysis_teorica_vs_pratica.png` e `comparison_log_scale.png`._

## Entregas

- **Entrega 1 (Definição da Equipe):** 24/10/2025
- **Entrega 2 (Projeto Final):** 30/11/2025
- **Apresentações:** 01 e 10 de Dezembro de 2025
