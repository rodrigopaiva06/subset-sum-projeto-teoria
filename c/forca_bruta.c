#include "entrada.h"

int forca_bruta(const int nums[], int n, long long alvo) {
    if (n > 62) {
        return -1;                       /* 2^63 nao cabe na mascara */
    }
    unsigned long long total = 1ULL << n;        /* quantidade de subconjuntos: 2^n */

    for (unsigned long long mask = 0; mask < total; mask++) {
        long long soma = 0;                      /* zera para cada subconjunto */
        for (int i = 0; i < n; i++) {
            if (mask & (1ULL << i)) {            /* o bit i esta ligado? */
                soma += nums[i];                 /* entao nums[i] entra na soma */
            }
        }
        if (soma == alvo) return 1;              /* achou: para na hora */
    }
    return 0;                                    /* testou todos e nenhum deu */
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "uso: %s arquivo.txt [repeticoes]\n", argv[0]);
        return 1;
    }
    int repeticoes = (argc >= 3) ? atoi(argv[2]) : 1;

    int n;
    long long alvo;
    int *nums = ler_entrada(argv[1], &n, &alvo);   /* leitura fora do cronometro */
    if (nums == NULL) return 1;

    int resposta = 0;
    for (int r = 0; r < repeticoes; r++) {
        double inicio = agora();
        resposta = forca_bruta(nums, n, alvo);
        double fim = agora();
        printf("tempo_s %.9f\n", fim - inicio);
    }
    printf("resposta %d\n", resposta);

    free(nums);
    return 0;
}