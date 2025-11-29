"""
Script para geração de dados de teste para o benchmark do algoritmo KMP.

Este script gera dois tipos de arquivos de teste em diferentes tamanhos:
1. Pior Caso: Arquivos contendo repetições de um caractere 'A', projetados para
   maximizar o número de comparações no algoritmo KMP quando buscado um padrão
   como 'AA...AB'.
2. Caso Real: Arquivos gerados a partir de um texto base real (ex: livro),
   truncados ou repetidos para atingir os tamanhos desejados.

Tamanhos gerados: 100KB, 500KB, 5MB, 10MB, 50MB.
"""

import os

SIZES = [
    ("100kb", 100 * 1024),
    ("500kb", 500 * 1024),
    ("5mb", 5 * 1024 * 1024),
    ("10mb", 10 * 1024 * 1024),
    ("50mb", 50 * 1024 * 1024),
]

REAL_DATA_SOURCE = "data/base.txt"

OUTPUT_DIR = "data/generated"


def gerar_arquivos_pior_caso():
    """
    Gera arquivos de teste para o cenário de pior caso.

    O conteúdo consiste em repetições do caractere 'A'. Isso é utilizado em conjunto
    com um padrão do tipo 'AA...AB' para forçar o algoritmo KMP a realizar muitas
    comparações e falhas parciais, testando sua eficiência no pior cenário teórico.
    """
    print("Gerando arquivos de Pior Caso (sintético)...")

    chunk_size = 1024 * 1024
    chunk = 'A' * chunk_size

    for name, size in SIZES:
        filepath = os.path.join(OUTPUT_DIR, f"pior_caso_{name}.txt")
        print(f"  -> Criando {filepath} ({size} bytes)")

        bytes_escritos = 0
        with open(filepath, 'w', encoding='utf-8') as f:
            while bytes_escritos < size:
                bytes_restantes = size - bytes_escritos
                if bytes_restantes >= chunk_size:
                    f.write(chunk)
                    bytes_escritos += chunk_size
                else:
                    f.write('A' * bytes_restantes)
                    bytes_escritos += bytes_restantes


def gerar_arquivos_caso_real():
    """
    Gera arquivos de teste para o cenário de caso real.

    Lê um arquivo de texto base (definido em REAL_DATA_SOURCE) e cria arquivos
    de teste com os tamanhos especificados. Se o arquivo base for menor que o
    tamanho desejado, seu conteúdo é repetido até preencher o tamanho.
    """
    print("\nGerando arquivos de Caso Real (baseado em texto)...")

    if not os.path.exists(REAL_DATA_SOURCE):
        print(f"ERRO: Arquivo base '{REAL_DATA_SOURCE}' não encontrado.")
        print("Por favor, baixe um arquivo .txt (ex: Moby Dick) e salve-o nesse caminho.")
        return

    with open(REAL_DATA_SOURCE, 'r', encoding='utf-8') as f:
        base_content = f.read()

    base_content_size = len(base_content)
    if base_content_size == 0:
        print("ERRO: O arquivo base está vazio.")
        return

    print(
        f"Arquivo base '{REAL_DATA_SOURCE}' lido ({base_content_size} bytes).")

    for name, size in SIZES:
        filepath = os.path.join(OUTPUT_DIR, f"real_{name}.txt")
        print(f"  -> Criando {filepath} ({size} bytes)")

        with open(filepath, 'w', encoding='utf-8') as f:
            if size <= base_content_size:
                f.write(base_content[:size])
            else:
                bytes_escritos = 0
                while bytes_escritos < size:
                    bytes_restantes = size - bytes_escritos
                    if bytes_restantes >= base_content_size:
                        f.write(base_content)
                        bytes_escritos += base_content_size
                    else:
                        f.write(base_content[:bytes_restantes])
                        bytes_escritos += bytes_restantes


def main():
    """
    Função principal que orquestra a geração dos arquivos de dados.
    Cria o diretório de saída se não existir e chama as funções geradoras.
    """
    print("Iniciando script de geração de dados...")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Pasta de saída: '{OUTPUT_DIR}'")

    gerar_arquivos_pior_caso()

    gerar_arquivos_caso_real()

    print("\nConcluído! Todos os 10 arquivos de teste foram gerados.")


if __name__ == "__main__":
    main()
