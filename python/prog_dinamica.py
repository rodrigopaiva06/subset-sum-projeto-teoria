import sys
import time


def ler_entrada(caminho):
    with open(caminho) as f:
        n, alvo = map(int, f.readline().split())
        nums = list(map(int, f.read().split()))
    if len(nums) != n:
        raise ValueError("quantidade de numeros diferente de n")
    return nums, alvo


def prog_dinamica(nums, alvo):
    if alvo < 0:
        return 0
    # so funciona com numeros >= 0: com negativo, j - numero sai da tabela
    for x in nums:
        if x < 0:
            return -1

    n = len(nums)
    # n+1 linhas, cada uma com alvo+1 colunas, tudo com 0
    tabela = [bytearray(alvo + 1) for _ in range(n + 1)]

    # sem usar nenhum numero, so da para somar 0
    tabela[0][0] = 1

    for i in range(1, n + 1):
        numero = nums[i - 1]            # o numero novo desta linha
        de_cima = tabela[i - 1]
        atual = tabela[i]
        for j in range(alvo + 1):
            #1: nao pego o numero novo -> copio da linha de cima
            if de_cima[j] == 1:
                atual[j] = 1
            #pego o numero novo -> precisava ter somado j - numero antes
            if j >= numero and de_cima[j - numero] == 1:
                atual[j] = 1

    return tabela[n][alvo]


def main():
    if len(sys.argv) < 2:
        print(f"uso: python3 {sys.argv[0]} arquivo.txt [repeticoes]", file=sys.stderr)
        sys.exit(1)
    repeticoes = int(sys.argv[2]) if len(sys.argv) >= 3 else 1

    nums, alvo = ler_entrada(sys.argv[1])

    resposta = 0
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        resposta = prog_dinamica(nums, alvo)
        fim = time.perf_counter()
        print(f"tempo_s {fim - inicio:.9f}")
    print(f"resposta {resposta}")


if __name__ == "__main__":
    main()