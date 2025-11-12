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
        # Converte a coluna 'size' para o tamanho real em bytes (necessário para a curva teórica)
        def size_to_bytes(s):
            s = s.lower().replace('kb', '*1024').replace('mb', '*1024*1024')
            return eval(s)
        
        df['size_bytes'] = df['size'].apply(size_to_bytes)
        return df

    # Leitura dos dados
    df_c = read_benchmark_csv(c_path)
    df_py = read_benchmark_csv(py_path)
    
    df_c = df_c.rename(columns={'mean_real_s': 'C_Real', 'mean_pior_s': 'C_Pior'})
    df_py = df_py.rename(columns={'mean_real_s': 'Python_Real', 'mean_pior_s': 'Python_Pior'})

    # Mescla os DataFrames pela coluna 'size'
    df_merged = pd.merge(df_c[['size', 'size_bytes', 'C_Real', 'C_Pior']], 
                         df_py[['size', 'Python_Real', 'Python_Pior']], 
                         on='size')
    
    return df_merged

# ----------------------------------------------------------------------
# GRÁFICO 1: ANÁLISE TEÓRICA (Curva O(N) vs Python)
# ----------------------------------------------------------------------

def plot_teorica_vs_pratica(df: pd.DataFrame):
    """Gera o gráfico comparando a curva O(N) com os dados práticos de Python (para prova teórica)."""
    
    df_plot = df[['size', 'size_bytes', 'Python_Pior']].copy()
    
    # 1. Geração da Curva Teórica O(N)
    N_max = df_plot['size_bytes'].max() 
    T_max = df_plot['Python_Pior'].max() 
    
    # Fator de escala k: ajusta a curva teórica para o ponto mais alto do dado prático
    k = T_max / N_max 
    df_plot['Teorica_ON'] = k * df_plot['size_bytes']

    # 2. Plotagem
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x_labels = df['size']
    x_ticks = np.arange(len(x_labels)) 
    
    ax.plot(x_ticks, df_plot['Python_Pior'], marker='s', label='Python (Pior Caso Medido)', linewidth=3, color='#c90000')
    ax.plot(x_ticks, df_plot['Teorica_ON'], linestyle='--', label='Curva Teórica O(N+M)', linewidth=2, color='darkgreen')

    ax.set_title('KMP: Análise Teórica vs. Prática (Foco em Python)', fontsize=16)
    ax.set_xlabel('Tamanho da Entrada (N)', fontsize=14)
    ax.set_ylabel('Tempo de Execução (Segundos)', fontsize=14)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels)
    ax.legend(fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    teorica_output_file = "analysis_teorica_vs_pratica.png"
    plt.savefig(teorica_output_file)
    print(f"Gráfico de Análise Teórica vs. Prática salvo como: {teorica_output_file}")

# ----------------------------------------------------------------------
# GRÁFICO 2: COMPARAÇÃO GERAL (C e Python Juntos - Escala Logarítmica)
# ----------------------------------------------------------------------

def plot_log_comparison(df: pd.DataFrame):
    """Gera um gráfico comparando C e Python em escala LOGARÍTMICA no eixo Y (Resolve crítica do professor)."""
    
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x_labels = df['size']
    x_ticks = np.arange(len(x_labels)) 
    
    # Plota os 4 cenários
    ax.plot(x_ticks, df['C_Real'], marker='o', label='C (Caso Real)', linewidth=2, color='#0077b6')
    ax.plot(x_ticks, df['C_Pior'], marker='x', label='C (Pior Caso)', linestyle='--', linewidth=1.5, color='#03045e')
    ax.plot(x_ticks, df['Python_Real'], marker='s', label='Python (Caso Real)', linewidth=2, color='#e90052')
    ax.plot(x_ticks, df['Python_Pior'], marker='d', label='Python (Pior Caso)', linestyle='--', linewidth=1.5, color='#b00020')

    # Escala Logarítmica no Eixo Y: essencial para ver C e Python no mesmo gráfico
    ax.set_yscale('log')
    
    ax.set_title('KMP: Comparação de Performance (C vs Python) - Escala Logarítmica', fontsize=16)
    ax.set_xlabel('Tamanho da Entrada (N)', fontsize=14)
    ax.set_ylabel('Tempo de Execução Médio (Segundos - Escala Log)', fontsize=14)
    
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels)
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.7, which='both') # which='both' mostra grades no eixo logarítmico
    
    plt.tight_layout()
    log_output_file = "comparison_log_scale.png"
    plt.savefig(log_output_file)
    print(f"Gráfico de Comparação Logarítmica salvo como: {log_output_file}")

# ----------------------------------------------------------------------
# FUNÇÃO PRINCIPAL
# ----------------------------------------------------------------------

def main():
    print("Iniciando a geração de gráficos de performance...")
    try:
        df = load_data()
        
        # 1. Gráfico Teórico (Prova a Complexidade)
        plot_teorica_vs_pratica(df) 
        
        # 2. Gráfico Logarítmico (Compara C e Python juntos)
        plot_log_comparison(df)
        
        print("\n*** Dois gráficos principais (Teórico e Logarítmico) foram gerados! ***")
        print("Verifique os arquivos 'analysis_teorica_vs_pratica.png' e 'comparison_log_scale.png'.")
    except Exception as e:
        print(f"\nOcorreu um erro durante a plotagem: {e}")
        print("Verifique se as bibliotecas 'pandas', 'matplotlib' e 'numpy' estão instaladas. (O numpy já está!)")


if __name__ == "__main__":
    main()