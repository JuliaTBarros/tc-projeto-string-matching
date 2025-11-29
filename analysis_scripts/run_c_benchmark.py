#!/usr/bin/env python3
"""
Script de automação para benchmark da implementação em C do algoritmo KMP.

Este script realiza as seguintes tarefas:
1. Compila o código C (se necessário).
2. Executa o binário compilado contra os arquivos de teste gerados.
3. Coleta métricas de tempo de execução para múltiplos testes (runs).
4. Calcula estatísticas (média e desvio padrão).
5. Exibe os resultados em uma tabela no console.
6. Salva os resultados detalhados em um arquivo CSV para análise posterior.
"""

import os
import subprocess
import re
import statistics
import sys
import csv
import datetime

# Configuration
EXECUTABLE = "../c_implementation/kmp_c" if os.path.basename(
    os.getcwd()) == "analysis_scripts" else "c_implementation/kmp_c"
SIZES_TO_TEST = ["100kb", "500kb", "5mb", "10mb", "50mb"]
DATA_DIR = os.path.join("..", "data", "generated") if os.path.basename(
    os.getcwd()) == "analysis_scripts" else "data/generated"
NUM_RUNS = 30


def run_benchmark():
    """
    Executa o benchmark completo para a implementação em C.

    Itera sobre os tipos de teste (real e pior caso) e tamanhos de arquivo.
    Para cada combinação, executa o programa C múltiplas vezes (NUM_RUNS)
    e coleta os tempos de execução.

    Returns:
        dict: Um dicionário aninhado contendo os resultados estatísticos
              (média e desvio padrão) para cada caso de teste.
    """
    # Verify executable exists and compile if needed
    if not os.path.exists(EXECUTABLE):
        print(f"Erro: executável não encontrado: {EXECUTABLE}")
        print("Compilando o programa C...")
        try:
            compile_cmd = ["gcc", "-std=c11", "-O2", "-o", EXECUTABLE,
                           os.path.join(os.path.dirname(EXECUTABLE), "main.c")]
            subprocess.run(compile_cmd, check=True)
            print("Compilação concluída com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao compilar: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Erro inesperado ao compilar: {e}")
            sys.exit(1)

    results = {"real": {}, "pior_caso": {}}
    time_re = re.compile(r"Time: (\d+\.\d+) seconds")
    total_runs = len(SIZES_TO_TEST) * 2 * NUM_RUNS  # 2 for real and pior_caso
    current_run = 0

    for test_type in ["real", "pior_caso"]:
        # Define the needle pattern based on test type
        if test_type == "real":
            # NOTE: This must be 50 chars and exist in the 'base.txt'
            needle = "Call me Ishmael. Some years ago--never mind how long"
        else:
            # 50 chars: 49 'A's followed by 1 'B'
            needle = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB"

        for size in SIZES_TO_TEST:
            filename = f"{test_type}_{size}.txt"
            filepath = os.path.join(DATA_DIR, filename)

            if not os.path.exists(filepath):
                print(f"Aviso: arquivo não encontrado, pulando: {filepath}")
                continue

            run_times = []

            for i in range(NUM_RUNS):
                current_run += 1
                progress = (current_run / total_runs) * 100

                cmd = [EXECUTABLE, filepath, needle]
                try:
                    completed = subprocess.run(
                        cmd, capture_output=True, text=True)
                except Exception as e:
                    print(f"Erro ao executar {cmd}: {e}")
                    continue

                if completed.returncode != 0:
                    print(
                        f"Execução falhou (ret={completed.returncode}) para {cmd}: {completed.stderr.strip()}")
                    continue

                out = completed.stdout
                m = time_re.search(out)
                if not m:
                    print(
                        f"Tempo não encontrado na saída do processo ({cmd}). Saída:\n{out}")
                    continue

                t = float(m.group(1))
                run_times.append(t)
                print(
                    f"Progresso: {progress:.1f}% - {test_type} {size} (run {i+1}/{NUM_RUNS}): {t:.6f}s", end="\r")

            if run_times:
                avg_time = statistics.mean(run_times)
                stdev_time = statistics.stdev(
                    run_times) if len(run_times) > 1 else 0.0
                results[test_type][size] = {
                    "mean": avg_time, "stdev": stdev_time}
                print(
                    f"\nResultado {size} ({test_type}): média={avg_time:.6f}s, stdev={stdev_time:.6f}s, amostras={len(run_times)}")
            else:
                print(f"\nNenhuma execução bem-sucedida para {filename}")

    return results


# run_c_benchmark.py: Função print_results_table

def print_results_table(results):
    """
    Imprime os resultados em formato de tabela no console.

    Args:
        results (dict): Dicionário com os resultados coletados (médias e desvios padrão).
    """
    header = "Tamanho | Caso Real (M/D)     | Pior Caso (M/D)   | Diferença"
    sep = "--------+---------------------+-------------------+-----------"
    print("\nResultados Finais (M=Média, D=Desvio-Padrão):")
    print(header)
    print(sep)

    for size in SIZES_TO_TEST:
        real_data = results.get("real", {}).get(size)
        pior_data = results.get("pior_caso", {}).get(size)

        # Extrai a média (M) e o desvio-padrão (D) do dicionário
        real_m = real_data.get('mean') if real_data else None
        real_d = real_data.get('stdev') if real_data else None
        pior_m = pior_data.get('mean') if pior_data else None
        pior_d = pior_data.get('stdev') if pior_data else None

        # Formata a string de saída usando as variáveis M e D (que são floats)
        real_str = f"{real_m:.4f}±{real_d:.4f}s" if real_m is not None else "-"
        pior_str = f"{pior_m:.4f}±{pior_d:.4f}s" if pior_m is not None else "-"

        diff_str = "-"
        if real_m is not None and pior_m is not None:
            diff = pior_m - real_m
            diff_str = f"{diff:+.6f}s"

        print(f"{size:7} | {real_str:19} | {pior_str:17} | {diff_str:9}")


if __name__ == "__main__":
    print("Iniciando benchmark KMP...")
    if not os.path.exists(DATA_DIR):
        print(f"Diretório de dados não encontrado: {DATA_DIR}")
        print("Execute primeiro: python gerar_dados.py")
        sys.exit(1)

    results = run_benchmark()
    print_results_table(results)
    # write CSV results for inclusion in reports
    try:
        script_dir = os.path.dirname(__file__)
        csv_path = os.path.join(script_dir, "benchmark_results.csv")
        timestamp = datetime.datetime.now().isoformat()
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # metadata rows
            writer.writerow(["# Generated", timestamp])
            writer.writerow(["# Executable", EXECUTABLE])
            writer.writerow(["# NumRuns", NUM_RUNS])
            writer.writerow([])
            # data header
            writer.writerow(["size", "mean_real_s", "stdev_real_s",
                            "mean_pior_s", "stdev_pior_s", "diff_s"])
            for size in SIZES_TO_TEST:
                real = results.get("real", {}).get(size)
                pior = results.get("pior_caso", {}).get(size)
                if real is None and pior is None:
                    continue
                # Extrai média e stdev do novo formato de dicionário
                real_m = real['mean'] if real is not None else None
                real_s = real['stdev'] if real is not None else None
                pior_m = pior['mean'] if pior is not None else None
                pior_s = pior['stdev'] if pior is not None else None

                real_v = f"{real_m:.6f}" if real_m is not None else ""
                real_s_v = f"{real_s:.6f}" if real_s is not None else ""
                pior_v = f"{pior_m:.6f}" if pior_m is not None else ""
                pior_s_v = f"{pior_s:.6f}" if pior_s is not None else ""

                diff_v = ""
                if real_m is not None and pior_m is not None:
                    diff_v = f"{(pior_m - real_m):.6f}"

                # Escreve a linha de dados: MODIFICADO para incluir 4 colunas de tempo
                writer.writerow(
                    [size, real_v, real_s_v, pior_v, pior_s_v, diff_v])
        print(f"CSV salvo em: {csv_path}")
    except Exception as e:
        print(f"Falha ao salvar CSV: {e}")
    print("\nBenchmark concluído!")
