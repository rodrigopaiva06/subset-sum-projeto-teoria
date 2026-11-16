import sys
import time


def ler_entrada(caminho):
    with open(caminho) as f:
        n, alvo = map(int, f.readline().split())
        nums = list(map(int, f.read().split()))
    if len(nums) != n:
        raise ValueError("quantidade de numeros diferente de n")
    return nums, alvo


def forca_bruta(nums, alvo):
    n = len(nums)
    total = 1 << n                      # 2^n subconjuntos
    for mask in range(total):
        soma = 0                        # zera para cada subconjunto
        for i in range(n):
            if mask & (1 << i):         # o bit i esta ligado?
                soma += nums[i]
        if soma == alvo:
            return 1                    # achou: para na hora
    return 0                            # testou todos e nenhum deu


def main():
    if len(sys.argv) < 2:
        print(f"uso: python3 {sys.argv[0]} arquivo.txt [repeticoes]", file=sys.stderr)
        sys.exit(1)
    repeticoes = int(sys.argv[2]) if len(sys.argv) >= 3 else 1

    nums, alvo = ler_entrada(sys.argv[1])       # leitura fora do cronometro
    resposta = 0
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        resposta = forca_bruta(nums, alvo)
        fim = time.perf_counter()
        print(f"tempo_s {fim - inicio:.9f}")
    print(f"resposta {resposta}")


if __name__ == "__main__":
    main()