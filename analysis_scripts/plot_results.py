import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import numpy as np

# Define os nomes dos arquivos CSV gerados pelos scripts de benchmark
C_CSV_FILE = "benchmark_results.csv"
PY_CSV_FILE = "benchmark_results_py.csv"

def load_data():
    """Carrega e mescla os dados de C e Python dos arquivos CSV."""
    
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
            s = s.lower().replace('kb', '*1024').replace('mb', '*1024*1024')
            return eval(s)
        
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
        df_c[['size', 'size_bytes', 'C_Real', 'C_Pior', 'stdev_real_s_c', 'stdev_pior_s_c']], 
        df_py[['size', 'Python_Real', 'Python_Pior', 'stdev_real_s_py', 'stdev_pior_s_py']], 
        on='size'
    )
    
    return df_merged

# ----------------------------------------------------------------------
# GRÁFICO 1: ANÁLISE TEÓRICA (Curva O(N) vs Python e C)
# ----------------------------------------------------------------------

def plot_teorica_vs_pratica(df):
    """
    Gera o gráfico de análise da complexidade teórica (Python e C) com barras de erro.
    
    O algoritmo KMP tem complexidade O(N+M), que é dominada pelo tamanho do texto (N).
    A curva teórica é plotada como C * N, onde C é uma constante ARBITRÁRIA.
    """
    
    # 1. Definição da Curva Teórica - CONSTANTE ARBITRÁRIA (NÃO ajustada aos dados)
    # Esta constante deve ser escolhida de forma independente dos dados medidos
    # Vamos usar uma constante que represente um processamento ideal hipotético
    CONSTANTE_ESCALA_TEORICA = 5.0e-8  # 50 nanossegundos por byte (arbitrário)
    curva_teorica = df['size_bytes'] * CONSTANTE_ESCALA_TEORICA 
    
    # 2. Definição da Figura e Eixos
    fig, ax = plt.subplots(figsize=(12, 7))
    x_labels = df['size']
    x_bytes = df['size_bytes']
    
    # 3. Plotagem do Pior Caso Medido (Python) com Barras de Erro
    ax.errorbar(
        x_bytes, 
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
        x_bytes, 
        curva_teorica, 
        '--', 
        color='green',
        linewidth=2.5,
        label='Complexidade Teórica $O(N)$'
    )

    # 5. Decisão sobre plotar C no mesmo gráfico ou separado
    c_max = df['C_Pior'].max()
    py_min = df['Python_Pior'].min()
    
    # Se C for muito menor (menos de 5% do mínimo de Python), fazer gráfico separado
    if c_max < py_min * 0.05:
        print("\n[INFO] C é muito mais rápido que Python. Gerando gráfico teórico C em separado.")
        plot_teorica_vs_pratica_c(df, CONSTANTE_ESCALA_TEORICA)
        ax.text(0.98, 0.02, 
                'Nota: Dados de C plotados em gráfico separado\ndevido à diferença de escala',
                transform=ax.transAxes,
                fontsize=10,
                verticalalignment='bottom',
                horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    else:
        # Plota C no mesmo gráfico
        ax.errorbar(
            x_bytes, 
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
    
    # 6. Configuração Final
    ax.set_title('Análise Teórica vs. Prática (Pior Caso)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Tamanho da Entrada (N em Bytes)', fontsize=14)
    ax.set_ylabel('Tempo de Execução (Segundos)', fontsize=14)
    
    ax.set_xticks(x_bytes)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("analysis_teorica_vs_pratica.png", dpi=300)
    print("\nGráfico de Análise Teórica (Python) salvo como: analysis_teorica_vs_pratica.png")

def plot_teorica_vs_pratica_c(df, constante_escala):
    """
    Gera um gráfico separado para C e Teórico, pois C é muito mais rápido que Python.
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    x_labels = df['size']
    x_bytes = df['size_bytes']
    
    # Curva Teórica (usando a mesma constante de escala)
    curva_teorica = df['size_bytes'] * constante_escala
    
    ax.plot(
        x_bytes, 
        curva_teorica, 
        '--',
        color='green',
        linewidth=2.5,
        label='Complexidade Teórica $O(N)$'
    )
    
    # Pior Caso Medido (C) com Barras de Erro
    ax.errorbar(
        x_bytes, 
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

    ax.set_title('Análise Teórica vs. Prática para C (Pior Caso)', 
                 fontsize=16, fontweight='bold')
    ax.set_xlabel('Tamanho da Entrada (N em Bytes)', fontsize=14)
    ax.set_ylabel('Tempo de Execução (Segundos)', fontsize=14)
    
    ax.set_xticks(x_bytes)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("analysis_teorica_vs_pratica_C_separado.png", dpi=300)
    print("Gráfico de Análise Teórica (C separado) salvo como: analysis_teorica_vs_pratica_C_separado.png")

# ----------------------------------------------------------------------
# GRÁFICO 2: COMPARAÇÃO GERAL (C e Python Juntos - Escala Logarítmica)
# ----------------------------------------------------------------------

def plot_log_comparison(df: pd.DataFrame):
    """Gera um gráfico comparando C e Python em escala LOGARÍTMICA com barras de erro."""
    
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
    ax.set_ylabel('Tempo de Execução Médio (Segundos - Escala Log)', fontsize=14)
    
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
    print("Iniciando a geração de gráficos de performance...")
    try:
        df = load_data()
        
        print("\n=== Dados carregados ===")
        print(df[['size', 'C_Pior', 'Python_Pior', 'stdev_pior_s_c', 'stdev_pior_s_py']])
        
        # 1. Gráfico Teórico (Prova a Complexidade)
        plot_teorica_vs_pratica(df) 
        
        # 2. Gráfico Logarítmico (Compara C e Python juntos)
        plot_log_comparison(df)
        
        print("\n*** Gráficos gerados com sucesso! ***")
        print("Verifique os arquivos:")
        print("  - analysis_teorica_vs_pratica.png")
        print("  - comparison_log_scale.png")
        if df['C_Pior'].max() < df['Python_Pior'].min() * 0.05:
            print("  - analysis_teorica_vs_pratica_C_separado.png")
            
    except Exception as e:
        print(f"\nOcorreu um erro durante a plotagem: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()