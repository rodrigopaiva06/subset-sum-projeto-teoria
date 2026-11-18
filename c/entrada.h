#ifndef ENTRADA_H
#define ENTRADA_H

#ifndef _WIN32
#define _POSIX_C_SOURCE 199309L
#endif

#include <stdio.h>
#include <stdlib.h>

#ifdef _WIN32
#include <windows.h>
#else
#include <time.h>
#endif

/* Le o arquivo. Devolve o vetor de numeros e preenche n e alvo.
   Devolve NULL se der erro. */
static int *ler_entrada(const char *caminho, int *n, long long *alvo) {
    FILE *f = fopen(caminho, "r");
    if (f == NULL) {
        fprintf(stderr, "erro: nao consegui abrir %s\n", caminho);
        return NULL;
    }
    
    char texto_alvo[32];
    if (fscanf(f, "%d %31s", n, texto_alvo) != 2 || *n < 0) {
        fprintf(stderr, "erro: primeira linha deve ser 'n alvo'\n");
        fclose(f);
        return NULL;
    }
    *alvo = strtoll(texto_alvo, NULL, 10);   /* converte o texto em numero */

    int *nums = malloc(sizeof(int) * (*n > 0 ? *n : 1));
    if (nums == NULL) {
        fclose(f);
        return NULL;
    }
    for (int i = 0; i < *n; i++) {
        if (fscanf(f, "%d", &nums[i]) != 1) {
            fprintf(stderr, "erro: faltam numeros no arquivo\n");
            free(nums);
            fclose(f);
            return NULL;
        }
    }
    fclose(f);
    return nums;
}

/* Cronometro: devolve o tempo atual em segundos.
   Windows usa um, Mac/Linux usa outro. */
static double agora(void) {
#ifdef _WIN32
    LARGE_INTEGER frequencia, contador;
    QueryPerformanceFrequency(&frequencia);
    QueryPerformanceCounter(&contador);
    return (double)contador.QuadPart / (double)frequencia.QuadPart;
#else
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec / 1e9;
#endif
}

#endif