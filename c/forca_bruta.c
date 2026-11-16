#include <stdio.h>

/* Devolve 1 se existe um subconjunto de nums[i..n-1] que, somado a soma_atual,
   dá exatamente o alvo. Devolve 0 caso contrário. */
int forca_bruta(int nums[], int n, int i, long long soma_atual, long long alvo) {
    if (i == n) {                      /* chegou numa folha: decidiu todos os números */
        return soma_atual == alvo;
    }
    /* escolha 1: pega o número nums[i] */
    if (forca_bruta(nums, n, i + 1, soma_atual + nums[i], alvo)) {
        return 1;
    }
    /* escolha 2: não pega o número nums[i] */
    return forca_bruta(nums, n, i + 1, soma_atual, alvo);
}

int main(void) {
    int nums[] = {3, 7, 2};
    int n = 3;

    printf("alvo 9:  %d\n", forca_bruta(nums, n, 0, 0, 9));   /* esperado 1 (7+2) */
    printf("alvo 20: %d\n", forca_bruta(nums, n, 0, 0, 20));  /* esperado 0 */
    printf("alvo 12: %d\n", forca_bruta(nums, n, 0, 0, 12));  /* esperado 1 (3+7+2) */
    return 0;
}