"""
Script para geração de gráficos comparativos de performance do algoritmo KMP.

Este script lê os arquivos CSV gerados pelos benchmarks de C e Python e gera
visualizações gráficas para análise de desempenho. Ele produz dois gráficos principais:
1. Análise Teórica vs Prática: Compara o tempo de execução medido com a curva
   teórica O(N).
2. Comparação Logarítmica: Compara o desempenho das implementações em C e Python
   em escala logarítmica.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import numpy as np

# Define os nomes dos arquivos CSV gerados pelos scripts de benchmark
C_CSV_FILE = "benchmark_results.csv"
PY_CSV_FILE = "benchmark_results_py.csv"


def load_data():
    """
    Carrega e mescla os dados de benchmark de C e Python dos arquivos CSV.

    Lê os arquivos CSV, converte os tamanhos de string (ex: '100kb') para bytes,
    renomeia colunas para padronização e mescla os dados em um único DataFrame.

    Returns:
        pd.DataFrame: DataFrame contendo os dados mesclados de C e Python.
    """

    script_dir = os.path.dirname(__file__)
    c_path = os.path.join(script_dir, C_CSV_FILE)
    py_path = os.path.join(script_dir, PY_CSV_FILE)

    if not os.path.exists(c_path) or not os.path.exists(py_path):
        print("Erro: Um ou ambos os arquivos CSV de resultados não foram encontrados.")
        print("Certifique-se de ter rodado: python run_c_benchmark.py e python run_py_benchmark.py")
        sys.exit(1)

    # Função auxiliar para ler o CSV, pulando metadados
    def read_benchmark_csv(filepath):
        df = pd.read_csv(filepath, comment='#')
        # Converte a coluna 'size' para o tamanho real em bytes

        def size_to_bytes(s):
            s_lower = s.lower().strip()
            if s_lower.endswith('mb'):
                return int(s_lower[:-2]) * 1024 * 1024
            elif s_lower.endswith('kb'):
                return int(s_lower[:-2]) * 1024
            else:
                return int(s_lower)
        df['size_bytes'] = df['size'].apply(size_to_bytes)
        return df

    # Leitura dos dados
    df_c = read_benchmark_csv(c_path)
    df_py = read_benchmark_csv(py_path)

    # Renomeia colunas para facilitar identificação
    df_c = df_c.rename(columns={
        'mean_real_s': 'C_Real',
        'mean_pior_s': 'C_Pior',
        'stdev_real_s': 'stdev_real_s_c',
        'stdev_pior_s': 'stdev_pior_s_c'
    })

    df_py = df_py.rename(columns={
        'mean_real_s': 'Python_Real',
        'mean_pior_s': 'Python_Pior',
        'stdev_real_s': 'stdev_real_s_py',
        'stdev_pior_s': 'stdev_pior_s_py'
    })

    # Mescla os DataFrames pela coluna 'size'
    df_merged = pd.merge(
        df_c[['size', 'size_bytes', 'C_Real', 'C_Pior',
              'stdev_real_s_c', 'stdev_pior_s_c']],
        df_py[['size', 'Python_Real', 'Python_Pior',
               'stdev_real_s_py', 'stdev_pior_s_py']],
        on='size'
    )

    return df_merged

# ----------------------------------------------------------------------
# GRÁFICO 1: ANÁLISE TEÓRICA (Curva O(N) vs Python e C)
# ----------------------------------------------------------------------


def plot_teorica_vs_pratica(df):
    """
    Gera o gráfico de análise da complexidade teórica (Python e C) com barras de erro.
    Utiliza escala logarítmica para melhor visualização de C.

    O algoritmo KMP tem complexidade O(N+M), que é dominada pelo tamanho do texto (N).
    A curva teórica é plotada como C * N, onde C é uma constante ARBITRÁRIA.
    """

    # 1. Definição da Curva Teórica - CONSTANTE ARBITRÁRIA (NÃO ajustada aos dados)
    # Esta constante deve ser escolhida de forma independente dos dados medidos
    CONSTANTE_ESCALA_TEORICA = 5.0e-8  # 50 nanossegundos por byte (arbitrário)
    curva_teorica = df['size_bytes'] * CONSTANTE_ESCALA_TEORICA

    # 2. Definição da Figura e Eixos
    fig, ax = plt.subplots(figsize=(12, 7))
    x_labels = df['size']
    x_ticks = np.arange(len(x_labels))  # Posições numéricas para o eixo X

    # 3. Plotagem do Pior Caso Medido (Python) com Barras de Erro
    ax.errorbar(
        x_ticks,
        df['Python_Pior'],
        yerr=df['stdev_pior_s_py'],
        fmt='-o',
        color='#e90052',
        capsize=5,
        markersize=8,
        linewidth=2,
        elinewidth=1.5,
        label='Python - Pior Caso Medido'
    )

    # 4. Plotagem da Curva Teórica (Com a constante arbitrária)
    ax.plot(
        x_ticks,
        curva_teorica,
        '--',
        color='green',
        linewidth=2.5,
        label='Complexidade Teórica $O(N)$'
    )

    # 5. Plotagem de C com Barras de Erro
    ax.errorbar(
        x_ticks,
        df['C_Pior'],
        yerr=df['stdev_pior_s_c'],
        fmt='-^',
        color='#0077b6',
        capsize=5,
        markersize=8,
        linewidth=2,
        elinewidth=1.5,
        label='C - Pior Caso Medido'
    )

    # 6. Escala Logarítmica no Eixo Y (para visualizar C adequadamente)
    ax.set_yscale('log')

    # 7. Configuração Final
    ax.set_title('Análise Teórica vs. Prática (Pior Caso) - Escala Logarítmica',
                 fontsize=16, fontweight='bold')
    ax.set_xlabel('Tamanho da Entrada (N)', fontsize=14)
    ax.set_ylabel('Tempo de Execução (Segundos - Escala Log)', fontsize=14)

    # Configuração do eixo X com labels corretos
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')

    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.7,
            which='both')  # Grid para escala log
    plt.tight_layout()
    plt.savefig("analysis_teorica_vs_pratica.png", dpi=300)
    print("\nGráfico de Análise Teórica salvo como: analysis_teorica_vs_pratica.png")
    print("[INFO] Todas as curvas (C, Python, Teórica) estão no mesmo gráfico com escala logarítmica.")

# ----------------------------------------------------------------------
# GRÁFICO 2: COMPARAÇÃO GERAL (C e Python Juntos - Escala Logarítmica)
# ----------------------------------------------------------------------


def plot_log_comparison(df: pd.DataFrame):
    """
    Gera um gráfico comparando C e Python em escala LOGARÍTMICA com barras de erro.

    Este gráfico permite visualizar a diferença de ordem de grandeza entre as
    implementações em C e Python, mantendo a visibilidade dos dados de C que
    são muito mais rápidos.
    """

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(12, 7))

    x_labels = df['size']
    x_ticks = np.arange(len(x_labels))

    # Plota os 4 cenários COM BARRAS DE ERRO
    ax.errorbar(x_ticks, df['C_Real'], yerr=df['stdev_real_s_c'],
                marker='o', label='C (Caso Real)', linewidth=2,
                color='#0077b6', capsize=4, elinewidth=1.5)

    ax.errorbar(x_ticks, df['C_Pior'], yerr=df['stdev_pior_s_c'],
                marker='x', label='C (Pior Caso)', linestyle='--',
                linewidth=1.5, color='#03045e', capsize=4, elinewidth=1.5)

    ax.errorbar(x_ticks, df['Python_Real'], yerr=df['stdev_real_s_py'],
                marker='s', label='Python (Caso Real)', linewidth=2,
                color='#e90052', capsize=4, elinewidth=1.5)

    ax.errorbar(x_ticks, df['Python_Pior'], yerr=df['stdev_pior_s_py'],
                marker='d', label='Python (Pior Caso)', linestyle='--',
                linewidth=1.5, color='#b00020', capsize=4, elinewidth=1.5)

    # Escala Logarítmica no Eixo Y
    ax.set_yscale('log')

    ax.set_title('KMP: Comparação de Performance (C vs Python) - Escala Logarítmica',
                 fontsize=16, fontweight='bold')
    ax.set_xlabel('Tamanho da Entrada (N)', fontsize=14)
    ax.set_ylabel(
        'Tempo de Execução Médio (Segundos - Escala Log)', fontsize=14)

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels)
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.7, which='both')

    plt.tight_layout()
    log_output_file = "comparison_log_scale.png"
    plt.savefig(log_output_file, dpi=300)
    print(f"Gráfico de Comparação Logarítmica salvo como: {log_output_file}")

# ----------------------------------------------------------------------
# FUNÇÃO PRINCIPAL
# ----------------------------------------------------------------------


def main():
    """
    Função principal que orquestra a geração dos gráficos.
    Carrega os dados, gera os gráficos e salva os arquivos de imagem.
    """
    print("Iniciando a geração de gráficos de performance...")
    try:
        df = load_data()

        print("\n=== Dados carregados ===")
        print(df[['size', 'C_Pior', 'Python_Pior',
              'stdev_pior_s_c', 'stdev_pior_s_py']])

        # 1. Gráfico Teórico (Prova a Complexidade) - AGORA COM ESCALA LOG
        plot_teorica_vs_pratica(df)

        # 2. Gráfico Logarítmico (Compara C e Python juntos)
        plot_log_comparison(df)

        print("\n*** Gráficos gerados com sucesso! ***")
        print("Verifique os arquivos:")
        print("  - analysis_teorica_vs_pratica.png (Escala Logarítmica)")
        print("  - comparison_log_scale.png")

    except Exception as e:
        print(f"\nOcorreu um erro durante a plotagem: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
