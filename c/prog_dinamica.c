#include "entrada.h"

int prog_dinamica(const int nums[], int n, long long alvo) {
    int i;
    long long j;       
    int resposta;

    if (alvo < 0 || n < 0) return 0;

    for (i = 0; i < n; i++) {
        if (nums[i] < 0) return -1;
    }

    /* cria a matriz: n+1 linhas, cada uma com alvo+1 colunas, tudo com 0 */
    char **tabela = calloc(n + 1, sizeof(char *));
    if (tabela == NULL) {
        return -1;               
    }

    for (i = 0; i <= n; i++) {
        tabela[i] = calloc((size_t)alvo + 1, sizeof(char));
        if (tabela[i] == NULL) {                 
            for (int k = 0; k < i; k++) free(tabela[k]);   
            free(tabela);
            return -1;
        }
    }

    /* sem usar nenhum numero, so da para somar 0 */
    tabela[0][0] = 1;

    /* preenche linha por linha */
    for (i = 1; i <= n; i++) {
        int numero = nums[i - 1];              

        for (j = 0; j <= alvo; j++) {
            /* opcao 1: nao pego o numero novo -> copio da linha de cima */
            if (tabela[i - 1][j] == 1) tabela[i][j] = 1;

            /* opcao 2: pego o numero novo -> precisava ter somado j - numero antes */
            if (j >= numero && tabela[i - 1][j - numero] == 1) tabela[i][j] = 1;
        }
    }

    resposta = tabela[n][alvo];

    /* apaga a matriz: primeiro cada linha, depois a lista de linhas */
    for (i = 0; i <= n; i++) free(tabela[i]);
    free(tabela);

    return resposta;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "uso: %s arquivo.txt [repeticoes]\n", argv[0]);
        return 1;
    }
    int repeticoes = (argc >= 3) ? atoi(argv[2]) : 1;

    int n;
    long long alvo;
    int *nums = ler_entrada(argv[1], &n, &alvo);
    if (nums == NULL) return 1;

    int resposta = 0;
    for (int r = 0; r < repeticoes; r++) {
        double inicio = agora();
        resposta = prog_dinamica(nums, n, alvo);
        double fim = agora();
        printf("tempo_s %.9f\n", fim - inicio);
    }
    printf("resposta %d\n", resposta);

    free(nums);
    return 0;
}