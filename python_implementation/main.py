import sys
import time

def compute_lps_array(pattern: str) -> list[int]:
    M = len(pattern)
    lps = [0] * M
    length = 0 
    i = 1

    while i < M:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:     
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(pattern: str, text: str) -> int:
    M = len(pattern)
    N = len(text)

    if not pattern or not text or M == 0 or N == 0 or M > N:
        return 0

    lps = compute_lps_array(pattern)

    matches = 0
    i = 0  
    j = 0 

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == M:
            matches += 1
            j = lps[j - 1]
        
        elif i < N and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
                
    return matches


def main():
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