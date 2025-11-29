#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/*
 * Fornece clock_gettime e CLOCK_MONOTONIC no Windows usando
 * QueryPerformanceCounter ao compilar com MSVC/MinGW.
 */
#if defined(_WIN32) || defined(_WIN64)
#include <windows.h>
#ifndef CLOCK_MONOTONIC
#define CLOCK_MONOTONIC 0
#endif
/* Usa struct timespec fornecida pelo sistema quando disponível. */

static int clock_gettime_monotonic(struct timespec *tp)
{
    LARGE_INTEGER freq, counter;
    if (!QueryPerformanceFrequency(&freq))
        return -1;
    if (!QueryPerformanceCounter(&counter))
        return -1;
    tp->tv_sec = (time_t)(counter.QuadPart / freq.QuadPart);
    tp->tv_nsec = (long)((counter.QuadPart % freq.QuadPart) * 1000000000LL / freq.QuadPart);
    return 0;
}

/* Mapeia nome genérico para nossa implementação */
static int clock_gettime(int clk_id, struct timespec *tp)
{
    (void)clk_id; // apenas CLOCK_MONOTONIC é suportado aqui
    return clock_gettime_monotonic(tp);
}
#endif

// 1) Função de Array LPS (Iterativa)
// Calcula o array "Longest Prefix Suffix" (LPS) usado para pular caracteres no padrão
void computeLPSArray(char *pattern, int M, int *lps)
{
    int len = 0; // comprimento do prefixo mais longo anterior
    lps[0] = 0;  // lps[0] é sempre 0

    int i = 1;
    while (i < M)
    {
        if (pattern[i] == pattern[len])
        {
            len++;
            lps[i] = len;
            i++;
        }
        else
        {
            if (len != 0)
            {
                // Isso é complexo. Considere o exemplo AAACAAAA e i = 7.
                // Voltamos para o índice anterior no array LPS para tentar casar novamente
                len = lps[len - 1];
                // Note que não incrementamos i aqui
            }
            else
            {
                lps[i] = 0;
                i++;
            }
        }
    }
}

// 2) Função de Busca KMP (Iterativa)
// Realiza a busca do padrão no texto usando o array LPS para evitar comparações redundantes
int KMPSearch(char *pattern, int M, char *text, int N)
{
    if (!pattern || !text)
        return 0;
    if (M == 0 || N == 0 || M > N)
        return 0;

    // Aloca memória para o array LPS
    int *lps = (int *)malloc(sizeof(int) * M);
    if (!lps)
    {
        fprintf(stderr, "Falha ao alocar array lps de tamanho %d\n", M);
        return 0;
    }

    // Pré-processa o padrão para preencher o array LPS
    computeLPSArray(pattern, M, lps);

    int i = 0; // índice para text[]
    int j = 0; // índice para pattern[]
    int matches = 0;

    while (i < N)
    {
        if (pattern[j] == text[i])
        {
            i++;
            j++;
        }

        if (j == M)
        {
            matches++;
            // Após encontrar um match, continua buscando pelo próximo possível match
            // usando o valor LPS do último caractere casado
            j = lps[j - 1];
        }
        else if (i < N && pattern[j] != text[i])
        {
            // Incompatibilidade após j matches
            if (j != 0)
                // Não precisa voltar i, apenas ajusta j usando LPS
                j = lps[j - 1];
            else
                // Se j é 0, apenas avança no texto
                i++;
        }
    }

    free(lps);
    return matches;
}

// 3) Função Principal (Harness de Benchmark)
int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        fprintf(stderr, "Uso: %s <arquivo_entrada> <padrao>\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char *filename = argv[1];
    char *pattern = argv[2];
    FILE *fp = fopen(filename, "rb");
    if (!fp)
    {
        fprintf(stderr, "Erro ao abrir arquivo '%s'\n", filename);
        return EXIT_FAILURE;
    }

    // Determina o tamanho do arquivo
    if (fseek(fp, 0, SEEK_END) != 0)
    {
        fprintf(stderr, "Falha ao buscar no arquivo '%s'\n", filename);
        fclose(fp);
        return EXIT_FAILURE;
    }

    long fsize = ftell(fp);
    if (fsize < 0)
    {
        fprintf(stderr, "Falha ao obter tamanho do arquivo '%s'\n", filename);
        fclose(fp);
        return EXIT_FAILURE;
    }
    rewind(fp);

    // Aloca buffer para o conteúdo do arquivo mais o terminador nulo
    char *text = (char *)malloc((size_t)fsize + 1);
    if (!text)
    {
        fprintf(stderr, "Falha ao alocar buffer de tamanho %ld\n", fsize + 1);
        fclose(fp);
        return EXIT_FAILURE;
    }

    // Lê o arquivo inteiro para a memória
    size_t read_bytes = fread(text, 1, (size_t)fsize, fp);
    if (read_bytes != (size_t)fsize)
    {
        fprintf(stderr, "Aviso: esperado %ld bytes mas lido %zu bytes\n", fsize, read_bytes);
        // prossegue com o que foi lido
    }
    text[read_bytes] = '\0';

    fclose(fp);

    // Obtém comprimentos antes da cronometragem (strlen no padrão é rápido, N já sabemos)
    int M = (int)strlen(pattern);
    int N = (int)read_bytes;

    // Cronometragem: inicia logo antes do KMPSearch e termina logo depois
    struct timespec start, end;
    if (clock_gettime(CLOCK_MONOTONIC, &start) != 0)
    {
        perror("clock_gettime(start)");
        free(text);
        return EXIT_FAILURE;
    }

    int matches = KMPSearch(pattern, M, text, N);

    if (clock_gettime(CLOCK_MONOTONIC, &end) != 0)
    {
        perror("clock_gettime(end)");
        free(text);
        return EXIT_FAILURE;
    }

    // Calcula o tempo decorrido em segundos
    double elapsed = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    printf("Matches: %d\n", matches);
    printf("Time: %.6f seconds\n", elapsed);

    free(text);
    return EXIT_SUCCESS;
}
