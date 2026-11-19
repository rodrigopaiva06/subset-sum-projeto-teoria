"""Teste de corretude: as 4 implementacoes (forca bruta e PD, em C e Python)
precisam dar a mesma resposta, e essa resposta precisa bater com uma
verificacao independente feita aqui mesmo (itertools).

Uso: python scripts/testes.py
"""
import itertools
import os
import random
import sys
import tempfile

from comum import PROGRAMAS, compilar_c, escrever_entrada, rodar

SEMENTE = 2026
QUANTIDADE = 150


def resposta_esperada(nums, alvo):
    """Verificacao independente: testa todas as combinacoes com itertools."""
    for tamanho in range(len(nums) + 1):
        for combo in itertools.combinations(nums, tamanho):
            if sum(combo) == alvo:
                return 1
    return 0


def casos_de_teste(rng):
    # casos de borda escolhidos a mao
    yield [], 0            # lista vazia, alvo 0 -> 1 (subconjunto vazio)
    yield [], 5            # lista vazia, alvo 5 -> 0
    yield [3, 7, 2], 9     # o exemplo do relatorio -> 1
    yield [3, 7, 2], 20    # maior que a soma total -> 0
    yield [5], 5           # um numero so, igual ao alvo -> 1
    yield [0, 0, 4], 4     # zeros na lista
    yield [2, 4, 6, 8], 7  # todos pares, alvo impar -> 0 (pior caso)
    yield [1, 1, 1, 1], 3  # numeros repetidos
    # casos aleatorios pequenos
    for _ in range(QUANTIDADE):
        n = rng.randint(1, 12)
        nums = [rng.randint(0, 30) for _ in range(n)]
        alvo = rng.randint(0, sum(nums) + 5)
        yield nums, alvo


def main():
    compilar_c()
    rng = random.Random(SEMENTE)
    falhas = 0
    total = 0
    with tempfile.TemporaryDirectory() as pasta:
        arquivo = os.path.join(pasta, "caso.txt")
        for nums, alvo in casos_de_teste(rng):
            total += 1
            escrever_entrada(arquivo, nums, alvo)
            esperado = resposta_esperada(nums, alvo)
            respostas = {prog: rodar(*prog, arquivo)[1] for prog in PROGRAMAS}
            if any(r != esperado for r in respostas.values()):
                falhas += 1
                print(f"FALHOU: nums={nums} alvo={alvo} esperado={esperado} obtido={respostas}")
    if falhas == 0:
        print(f"OK: {total} casos, as 4 implementacoes concordam entre si e com a verificacao independente")
    else:
        print(f"{falhas} de {total} casos falharam")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()