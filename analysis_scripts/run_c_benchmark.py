#!/usr/bin/env python3
import os
import subprocess
import re
import statistics
import sys

# Configuration
EXECUTABLE = "../c_implementation/kmp_c" if os.path.basename(os.getcwd()) == "analysis_scripts" else "c_implementation/kmp_c"
SIZES_TO_TEST = ["100kb", "500kb", "5mb", "10mb", "50mb"]
DATA_DIR = os.path.join("..", "data", "generated") if os.path.basename(os.getcwd()) == "analysis_scripts" else "data/generated"
NUM_RUNS = 5


def run_benchmark():
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
                
                cmd = [EXECUTABLE, filepath]
                try:
                    completed = subprocess.run(cmd, capture_output=True, text=True)
                except Exception as e:
                    print(f"Erro ao executar {cmd}: {e}")
                    continue

                if completed.returncode != 0:
                    print(f"Execução falhou (ret={completed.returncode}) para {cmd}: {completed.stderr.strip()}")
                    continue

                out = completed.stdout
                m = time_re.search(out)
                if not m:
                    print(f"Tempo não encontrado na saída do processo ({cmd}). Saída:\n{out}")
                    continue

                t = float(m.group(1))
                run_times.append(t)
                print(f"Progresso: {progress:.1f}% - {test_type} {size} (run {i+1}/{NUM_RUNS}): {t:.6f}s", end="\r")

            if run_times:
                avg_time = statistics.mean(run_times)
                results[test_type][size] = avg_time
                print(f"\nResultado {size} ({test_type}): média={avg_time:.6f}s, amostras={len(run_times)}")
            else:
                print(f"\nNenhuma execução bem-sucedida para {filename}")

    return results


def print_results_table(results):
    header = "Tamanho | Caso Real     | Pior Caso    | Diferença"
    sep =    "--------+---------------+--------------+-----------"
    print("\nResultados Finais:")
    print(header)
    print(sep)

    for size in SIZES_TO_TEST:
        real = results.get("real", {}).get(size)
        pior = results.get("pior_caso", {}).get(size)

        real_str = f"{real:.6f}s" if real is not None else "-"
        pior_str = f"{pior:.6f}s" if pior is not None else "-"
        
        if real is not None and pior is not None:
            diff = pior - real
            diff_str = f"{diff:+.6f}s"
        else:
            diff_str = "-"

        print(f"{size:7} | {real_str:13} | {pior_str:12} | {diff_str:9}")


if __name__ == "__main__":
    print("Iniciando benchmark KMP...")
    if not os.path.exists(DATA_DIR):
        print(f"Diretório de dados não encontrado: {DATA_DIR}")
        print("Execute primeiro: python gerar_dados.py")
        sys.exit(1)

    results = run_benchmark()
    print_results_table(results)
    print("\nBenchmark concluído!")
