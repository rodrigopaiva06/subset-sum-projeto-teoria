#ifndef ENTRADA_H
#define ENTRADA_H

#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/* Le o arquivo. Devolve o vetor de numeros (alocado com malloc)
   e preenche n e alvo. Devolve NULL se der erro. */
static int *ler_entrada(const char *caminho, int *n, long long *alvo) {
    FILE *f = fopen(caminho, "r");
    if (f == NULL) {
        fprintf(stderr, "erro: nao consegui abrir %s\n", caminho);
        return NULL;
    }
    if (fscanf(f, "%d %lld", n, alvo) != 2 || *n < 0) {
        fprintf(stderr, "erro: primeira linha deve ser 'n alvo'\n");
        fclose(f);
        return NULL;
    }
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


static double agora(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec / 1e9;
}

#endif