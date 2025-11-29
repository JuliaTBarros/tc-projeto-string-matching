"""
Implementação do algoritmo Knuth-Morris-Pratt (KMP) em Python.

Este script implementa o algoritmo de busca de padrões KMP, que realiza a busca
de ocorrências de uma string (padrão) dentro de um texto maior com complexidade
de tempo linear O(N + M), onde N é o tamanho do texto e M é o tamanho do padrão.
"""

import sys
import time


def compute_lps_array(pattern: str) -> list[int]:
    """
    Calcula o array LPS (Longest Prefix Suffix) para o padrão dado.

    O array LPS armazena, para cada posição i do padrão, o comprimento do maior
    prefixo próprio do padrão[0...i] que também é um sufixo de padrão[0...i].
    Isso permite que o algoritmo pule comparações desnecessárias.

    Args:
        pattern (str): O padrão para o qual o array LPS será calculado.

    Returns:
        list[int]: Uma lista de inteiros representando o array LPS.
    """
    M = len(pattern)
    lps = [0] * M
    length = 0  # Comprimento do prefixo sufixo anterior mais longo
    i = 1

    while i < M:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            # Se houver incompatibilidade
            if length != 0:
                # Tenta um prefixo menor que também é sufixo
                length = lps[length - 1]
            else:
                # Se não houver prefixo sufixo, lps[i] é 0
                lps[i] = 0
                i += 1
    return lps


def kmp_search(pattern: str, text: str) -> int:
    """
    Realiza a busca do padrão no texto usando o algoritmo KMP.

    Args:
        pattern (str): O padrão a ser buscado.
        text (str): O texto onde a busca será realizada.

    Returns:
        int: O número total de ocorrências do padrão encontradas no texto.
    """
    M = len(pattern)
    N = len(text)

    # Verificações básicas de validade
    if not pattern or not text or M == 0 or N == 0 or M > N:
        return 0

    # Pré-processamento do padrão
    lps = compute_lps_array(pattern)

    matches = 0
    i = 0  # Índice para o texto
    j = 0  # Índice para o padrão

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == M:
            # Encontrou uma ocorrência completa
            matches += 1
            # Prepara para buscar a próxima ocorrência usando o LPS
            j = lps[j - 1]

        elif i < N and pattern[j] != text[i]:
            # Incompatibilidade após j matches
            if j != 0:
                # Usa o array LPS para pular caracteres no padrão
                j = lps[j - 1]
            else:
                # Se j é 0, apenas avança no texto
                i += 1

    return matches


def main():
    """
    Função principal para execução via linha de comando.

    Lê o arquivo de texto e o padrão fornecidos como argumentos, executa a busca
    KMP e imprime o número de ocorrências e o tempo de execução.
    """
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input_file> <needle>", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]
    pattern = sys.argv[2]

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado '{filename}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}", file=sys.stderr)
        sys.exit(1)

    start_time = time.monotonic()

    matches = kmp_search(pattern, text)

    end_time = time.monotonic()

    elapsed = end_time - start_time

    print(f"Matches: {matches}")
    print(f"Time: {elapsed:.6f} seconds")


if __name__ == "__main__":
    main()
