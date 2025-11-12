import os
import subprocess
import re
import statistics
import sys
import csv
import datetime


if os.path.basename(os.getcwd()) == "analysis_scripts":
    PY_SCRIPT_PATH = os.path.join("..", "python_implementation", "main.py")
    DATA_DIR = os.path.join("..", "data", "generated")
else:
    PY_SCRIPT_PATH = os.path.join("python_implementation", "main.py")
    DATA_DIR = os.path.join("data", "generated")

EXECUTABLE = [sys.executable, PY_SCRIPT_PATH]

SIZES_TO_TEST = ["100kb", "500kb", "5mb", "10mb", "50mb"]
NUM_RUNS = 30
CSV_OUTPUT_FILE = "benchmark_results_py.csv" 


def run_benchmark():
    if not os.path.exists(EXECUTABLE[1]):
        print(f"Erro: script Python não encontrado: {EXECUTABLE[1]}")
        print("Certifique-se que 'python_implementation/main.py' existe.")
        sys.exit(1)

    results = {"real": {}, "pior_caso": {}}
    time_re = re.compile(r"Time: (\d+\.\d+) seconds")
    total_runs = len(SIZES_TO_TEST) * 2 * NUM_RUNS  
    current_run = 0

    for test_type in ["real", "pior_caso"]:
        if test_type == "real":
            needle = "Call me Ishmael. Some years ago--never mind how long"
        else:
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
                
                cmd = [*EXECUTABLE, filepath, needle]
                
                try:
                    completed = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
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
                # CALCULA O DESVIO-PADRÃO: Adicionado
                stdev_time = statistics.stdev(run_times) if len(run_times) > 1 else 0.0

                # ARMAZENA MEAN E STDEV: Modificado
                results[test_type][size] = {"mean": avg_time, "stdev": stdev_time}
                
                print(f"\nResultado {size} ({test_type}): média={avg_time:.6f}s, stdev={stdev_time:.6f}s, amostras={len(run_times)}")
            else:
                print(f"\nNenhuma execução bem-sucedida para {filename}")

    return results


def print_results_table(results):
    header = "Tamanho | Caso Real (M/D)    | Pior Caso (M/D)   | Diferença"
    sep =    "--------+--------------------+-------------------+-----------"
    print("\nResultados Finais (Python):")
    print(header)
    print(sep)

    for size in SIZES_TO_TEST:
        real = results.get("real", {}).get(size)
        pior = results.get("pior_caso", {}).get(size)

        # Extrai a média (M) e o desvio-padrão (D)
        real_m = real.get('mean') if real else None
        real_d = real.get('stdev') if real else None
        pior_m = pior.get('mean') if pior else None
        pior_d = pior.get('stdev') if pior else None
        
        # Formata a string de saída
        real_str = f"{real_m:.4f}±{real_d:.4f}s" if real_m is not None else "-"
        pior_str = f"{pior_m:.4f}±{pior_d:.4f}s" if pior_m is not None else "-"
        
        if real is not None and pior is not None:
            diff = pior_m - real_m
            diff_str = f"{diff:+.6f}s"
        else:
            diff_str = "-"

        print(f"{size:7} | {real_str:19} | {pior_str:17} | {diff_str:9}")


if __name__ == "__main__":
    print("Iniciando benchmark KMP (Python)...")
    if not os.path.exists(DATA_DIR):
        print(f"Diretório de dados não encontrado: {DATA_DIR}")
        print("Execute primeiro: python gerar_dados.py")
        sys.exit(1)

    results = run_benchmark()
    print_results_table(results)
    
    try:
        script_dir = os.path.dirname(__file__) if __file__ else '.'
        csv_path = os.path.join(script_dir, CSV_OUTPUT_FILE)
        timestamp = datetime.datetime.now().isoformat()
        
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["# Generated", timestamp])
            writer.writerow(["# Executable", " ".join(EXECUTABLE)])
            writer.writerow(["# NumRuns", NUM_RUNS])
            writer.writerow([])
            writer.writerow(["size", "mean_real_s", "stdev_real_s", "mean_pior_s", "stdev_pior_s", "diff_s"])
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
                writer.writerow([size, real_v, real_s_v, pior_v, pior_s_v, diff_v])
                
        print(f"CSV salvo em: {csv_path}")
    except Exception as e:
        print(f"Falha ao salvar CSV: {e}")
        
    print("\nBenchmark (Python) concluído!")