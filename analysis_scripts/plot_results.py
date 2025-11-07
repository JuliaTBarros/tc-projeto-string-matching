import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Define os nomes dos arquivos CSV gerados pelos scripts de benchmark
C_CSV_FILE = "benchmark_results.csv"
PY_CSV_FILE = "benchmark_results_py.csv"
PLOT_OUTPUT_FILE = "performance_comparison.png"

def load_data():
    """Carrega e mescla os dados de C e Python dos arquivos CSV."""
    
    # Define o caminho completo dos arquivos
    script_dir = os.path.dirname(__file__)
    c_path = os.path.join(script_dir, C_CSV_FILE)
    py_path = os.path.join(script_dir, PY_CSV_FILE)

    if not os.path.exists(c_path) or not os.path.exists(py_path):
        print("Erro: Um ou ambos os arquivos CSV de resultados não foram encontrados.")
        print(f"Caminhos esperados: {c_path} e {py_path}")
        print("Certifique-se de ter rodado: python run_c_benchmark.py e python run_py_benchmark.py")
        sys.exit(1)

    # Função auxiliar para ler o CSV, pulando metadados
    def read_benchmark_csv(filepath):
        # O CSV tem linhas de metadados no início que começam com '#'
        # Pula as linhas que não são de dados, mantendo apenas o cabeçalho de dados e as linhas de dados
        df = pd.read_csv(filepath, comment='#')
        # Garante que as colunas de tempo sejam numéricas
        df['mean_real_s'] = pd.to_numeric(df['mean_real_s'])
        df['mean_pior_s'] = pd.to_numeric(df['mean_pior_s'])
        df['size'] = df['size'].str.replace('kb', '000').str.replace('mb', '000000').astype(int)
        return df

    # Leitura dos dados
    df_c = read_benchmark_csv(c_path)
    df_py = read_benchmark_csv(py_path)
    
    # Renomeia colunas para distinguir entre as linguagens
    df_c = df_c.rename(columns={'mean_real_s': 'C_Real', 'mean_pior_s': 'C_Pior'})
    df_py = df_py.rename(columns={'mean_real_s': 'Python_Real', 'mean_pior_s': 'Python_Pior'})

    # Mescla os DataFrames pela coluna 'size'
    df_merged = pd.merge(df_c[['size', 'C_Real', 'C_Pior']], 
                         df_py[['size', 'Python_Real', 'Python_Pior']], 
                         on='size')
    
    return df_merged

def plot_performance(df: pd.DataFrame):
    """Gera o gráfico de comparação de tempo de execução."""
    
    # 1. Configuração do Gráfico
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Define os rótulos do eixo X (tamanhos em texto)
    x_labels = ["100KB", "500KB", "5MB", "10MB", "50MB"]
    
    # 2. Plotagem dos Dados
    # Note que a complexidade O(N+M) do KMP é essencialmente O(N) para M muito pequeno e N grande.
    # O gráfico mostra a relação linear esperada para O(N).
    
    # Plotagem Caso Real
    ax.plot(df['size'], df['C_Real'], marker='o', label='C (Caso Real)', linewidth=2)
    ax.plot(df['size'], df['Python_Real'], marker='s', label='Python (Caso Real)', linewidth=2)
    
    # Plotagem Pior Caso
    ax.plot(df['size'], df['C_Pior'], marker='x', label='C (Pior Caso)', linestyle='--', linewidth=1.5)
    ax.plot(df['size'], df['Python_Pior'], marker='d', label='Python (Pior Caso)', linestyle='--', linewidth=1.5)

    # 3. Configuração de Rótulos e Título
    ax.set_title('Comparação de Performance KMP (C vs Python) - O(N+M)', fontsize=16)
    ax.set_xlabel('Tamanho da Entrada (N)', fontsize=14)
    ax.set_ylabel('Tempo de Execução Médio (Segundos)', fontsize=14)
    
    # Ajusta os ticks do eixo X
    ax.set_xticks(df['size'])
    ax.set_xticklabels(x_labels)
    
    ax.legend(fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Adiciona anotações de tempo para os 50MB (o ponto mais importante)
    for lang, case, color in [('C', 'Real', 'blue'), ('Python', 'Pior', 'red')]:
        y_val = df[f'{lang}_{case}'].iloc[-1]
        ax.annotate(f'{y_val:.3f}s', 
                    (df['size'].iloc[-1], y_val),
                    textcoords="offset points", 
                    xytext=(5, 5 if lang == 'C' else -10),
                    ha='center', fontsize=10, color=color)

    # 4. Salvar o Gráfico
    plt.tight_layout()
    plt.savefig(PLOT_OUTPUT_FILE)
    print(f"\nGráfico de comparação salvo como: {PLOT_OUTPUT_FILE}")


if __name__ == "__main__":
    print("Iniciando a geração de gráficos de performance...")
    try:
        df = load_data()
        plot_performance(df)
        print("\n*** Todos os dados e gráficos foram gerados! ***")
    except Exception as e:
        print(f"\nOcorreu um erro durante a plotagem: {e}")
        print("Verifique se as bibliotecas 'pandas' e 'matplotlib' estão instaladas.")