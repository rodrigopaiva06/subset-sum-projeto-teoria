#include <stdio.h>
#include <stdlib.h>

int prog_dinamica(int nums[], int n, int alvo) {
    int i, j;          /* i = linha (quantos numeros ja usei), j = coluna (qual soma) */
    int resposta;      /* guarda o valor final, tabela[n][alvo] */

    if (alvo < 0 || n < 0) return 0;

        /* cria a matriz: n+1 linhas, cada uma com alvo+1 colunas, tudo com 0 */
    char **tabela = calloc(n + 1, sizeof(char *));

    for (i = 0; i <= n; i++) tabela[i] = calloc(alvo + 1, sizeof(char));

    /* sem usar nenhum numero, so da para somar 0 */
    tabela[0][0] = 1;

    /* preenche linha por linha */
    for (i = 1; i <= n; i++) {

        int numero = nums[i - 1]; /* o numero novo desta linha */

        for (j = 0; j <= alvo; j++) {

            /* opcao 1: nao pego o numero novo -> copio da linha de cima */
            if (tabela[i - 1][j] == 1) tabela[i][j] = 1;

            /* opcao 2: pego o numero novo -> precisava ter somado j - numero antes */
            if (j >= numero && tabela[i - 1][j - numero] == 1) tabela[i][j] = 1;
        }
    }

    /* guarda a resposta antes de apagar a matriz */
    resposta = tabela[n][alvo];

    /* apaga a matriz: primeiro cada linha, depois a lista de linhas */
    for (i = 0; i <= n; i++) free(tabela[i]);

    free(tabela);

    return resposta;
}

int main(void) {
    int nums[] = {3, 7, 2};
    int n = 3;

    printf("alvo 9:  %d\n", prog_dinamica(nums, n, 9));   /* esperado 1 (7+2) */
    printf("alvo 20: %d\n", prog_dinamica(nums, n, 20));  /* esperado 0 */
    printf("alvo 12: %d\n", prog_dinamica(nums, n, 12));  /* esperado 1 (3+7+2) */
    return 0;
}