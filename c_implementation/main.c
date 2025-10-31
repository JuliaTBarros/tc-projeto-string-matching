#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/*
 * Provide clock_gettime and CLOCK_MONOTONIC on Windows using
 * QueryPerformanceCounter when building on MSVC/MinGW.
 */
#if defined(_WIN32) || defined(_WIN64)
#include <windows.h>
#ifndef CLOCK_MONOTONIC
#define CLOCK_MONOTONIC 0
#endif
/* Use system provided struct timespec when available. */

static int clock_gettime_monotonic(struct timespec* tp) {
    LARGE_INTEGER freq, counter;
    if (!QueryPerformanceFrequency(&freq)) return -1;
    if (!QueryPerformanceCounter(&counter)) return -1;
    tp->tv_sec = (time_t)(counter.QuadPart / freq.QuadPart);
    tp->tv_nsec = (long)((counter.QuadPart % freq.QuadPart) * 1000000000LL / freq.QuadPart);
    return 0;
}

/* Map generic name to our implementation */
static int clock_gettime(int clk_id, struct timespec* tp) {
    (void)clk_id; // only CLOCK_MONOTONIC is supported here
    return clock_gettime_monotonic(tp);
}
#endif

// 1) LPS Array Function (Iterative)
void computeLPSArray(char* pattern, int M, int* lps) {
    int len = 0; // length of the previous longest prefix suffix
    lps[0] = 0;  // lps[0] is always 0

    int i = 1;
    while (i < M) {
        if (pattern[i] == pattern[len]) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0) {
                // This is tricky. Consider the example AAACAAAA and i = 7.
                len = lps[len - 1];
                // Also, note that we do not increment i here
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }
}

// 2) KMP Search Function (Iterative)
int KMPSearch(char* pattern, int M, char* text, int N) {
    if (!pattern || !text) return 0;
    if (M == 0 || N == 0 || M > N) return 0;

    int* lps = (int*)malloc(sizeof(int) * M);
    if (!lps) {
        fprintf(stderr, "Failed to allocate lps array of size %d\n", M);
        return 0;
    }

    computeLPSArray(pattern, M, lps);

    int i = 0; // index for text[]
    int j = 0; // index for pattern[]
    int matches = 0;

    while (i < N) {
        if (pattern[j] == text[i]) {
            i++;
            j++;
        }

        if (j == M) {
            matches++;
            // After a match, continue searching for next possible match
            j = lps[j - 1];
        } else if (i < N && pattern[j] != text[i]) {
            if (j != 0)
                j = lps[j - 1];
            else
                i++;
        }
    }

    free(lps);
    return matches;
}

// 3) Main Function (Benchmark Harness)
int main(int argc, char* argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <input_file> <needle>\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char* filename = argv[1];
    char* pattern = argv[2];
    FILE* fp = fopen(filename, "rb");
    if (!fp) {
        fprintf(stderr, "Error opening file '%s'\n", filename);
        return EXIT_FAILURE;
    }

    if (fseek(fp, 0, SEEK_END) != 0) {
        fprintf(stderr, "Failed to seek in file '%s'\n", filename);
        fclose(fp);
        return EXIT_FAILURE;
    }

    long fsize = ftell(fp);
    if (fsize < 0) {
        fprintf(stderr, "Failed to tell file size for '%s'\n", filename);
        fclose(fp);
        return EXIT_FAILURE;
    }
    rewind(fp);

    // Allocate buffer for file content plus null terminator
    char* text = (char*)malloc((size_t)fsize + 1);
    if (!text) {
        fprintf(stderr, "Failed to allocate buffer of size %ld\n", fsize + 1);
        fclose(fp);
        return EXIT_FAILURE;
    }

    size_t read_bytes = fread(text, 1, (size_t)fsize, fp);
    if (read_bytes != (size_t)fsize) {
        fprintf(stderr, "Warning: expected %ld bytes but read %zu bytes\n", fsize, read_bytes);
        // proceed with what we've got
    }
    text[read_bytes] = '\0';

    fclose(fp);

    // Get lengths before timing (strlen on pattern is fast, N we already know)
    int M = (int)strlen(pattern);
    int N = (int)read_bytes;

    // Timing: start just before KMPSearch and end right after
    struct timespec start, end;
    if (clock_gettime(CLOCK_MONOTONIC, &start) != 0) {
        perror("clock_gettime(start)");
        free(text);
        return EXIT_FAILURE;
    }

    int matches = KMPSearch(pattern, M, text, N);

    if (clock_gettime(CLOCK_MONOTONIC, &end) != 0) {
        perror("clock_gettime(end)");
        free(text);
        return EXIT_FAILURE;
    }

    double elapsed = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    printf("Matches: %d\n", matches);
    printf("Time: %.6f seconds\n", elapsed);

    free(text);
    return EXIT_SUCCESS;
}
