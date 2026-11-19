"""Gera todos os arquivos de entrada dos experimentos, sempre com a mesma semente.
Rodar de novo gera exatamente os mesmos arquivos.

Uso: python scripts/gerar_entradas.py
"""
import os
import random

from comum import PASTA_ENTRADAS, escrever_entrada

SEMENTE = 42

# Forca bruta: tamanhos n (o tempo cresce geometricamente: dobra a cada +1)
TAMANHOS_FB = [10, 12, 14, 16, 18, 20, 22, 24]

# Programacao dinamica: n fixo e alvo S dobrando a cada passo
N_PD = 50
ALVOS_PD = [1000, 2000, 4000, 8000, 16000, 32000, 64000]


def gerar_forca_bruta(rng):
    for n in TAMANHOS_FB:
        # PIOR CASO: todos os numeros pares e alvo impar -> nenhuma soma da certo,
        # entao a forca bruta e obrigada a testar os 2^n subconjuntos
        pares = [2 * rng.randint(1, 500) for _ in range(n)]
        alvo_impar = (sum(pares) // 2) | 1          # "| 1" garante que e impar
        escrever_entrada(os.path.join(PASTA_ENTRADAS, f"fb_pior_n{n}.txt"), pares, alvo_impar)

        # MELHOR CASO: o alvo e o primeiro numero -> acha logo na mascara 1 (2a tentativa)
        nums = [rng.randint(1, 1000) for _ in range(n)]
        escrever_entrada(os.path.join(PASTA_ENTRADAS, f"fb_melhor_n{n}.txt"), nums, nums[0])

        # CASO ALEATORIO: alvo = soma de um subconjunto sorteado (sempre tem resposta,
        # mas a posicao da resposta na enumeracao e aleatoria)
        nums = [rng.randint(1, 1000) for _ in range(n)]
        escolhidos = [x for x in nums if rng.random() < 0.5]
        escrever_entrada(os.path.join(PASTA_ENTRADAS, f"fb_aleatorio_n{n}.txt"), nums, sum(escolhidos))


def gerar_prog_dinamica(rng):
    for S in ALVOS_PD:
        # A PD sempre preenche a matriz inteira (n+1) x (S+1), entao o tempo
        # depende so de n e S, nao de ter ou nao resposta.
        nums = [rng.randint(1, S // 5) for _ in range(N_PD)]
        escrever_entrada(os.path.join(PASTA_ENTRADAS, f"pd_S{S}.txt"), nums, S)


def main():
    os.makedirs(PASTA_ENTRADAS, exist_ok=True)
    rng = random.Random(SEMENTE)
    gerar_forca_bruta(rng)
    gerar_prog_dinamica(rng)
    total = len([a for a in os.listdir(PASTA_ENTRADAS) if a.startswith(("fb_", "pd_"))])
    print(f"{total} arquivos gerados em {PASTA_ENTRADAS} (semente {SEMENTE})")


if __name__ == "__main__":
    main()