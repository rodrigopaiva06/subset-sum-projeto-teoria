"""Descobre o maior n que a forca bruta resolve em ate 60 segundos (pior caso),
em C e em Python. Aumenta n de 1 em 1 ate uma execucao passar de 60 s.
Demora alguns minutos. Resultado em medicoes/limite_60s.csv.

Uso: python scripts/limite.py
"""
import csv
import os
import random
import subprocess
import tempfile

from comum import PASTA_MEDICOES, compilar_c, escrever_entrada, rodar

LIMITE_S = 60
N_INICIAL = {"C": 22, "Python": 18}


def main():
    os.makedirs(PASTA_MEDICOES, exist_ok=True)
    compilar_c()
    linhas = []
    with tempfile.TemporaryDirectory() as pasta:
        for linguagem in ["C", "Python"]:
            n = N_INICIAL[linguagem]
            maior_ok, tempo_ok = None, None
            while True:
                rng = random.Random(n)
                pares = [2 * rng.randint(1, 500) for _ in range(n)]
                arquivo = os.path.join(pasta, f"n{n}.txt")
                escrever_entrada(arquivo, pares, (sum(pares) // 2) | 1)   # pior caso
                try:
                    tempos, _ = rodar("forca_bruta", linguagem, arquivo, 1, timeout=LIMITE_S)
                except subprocess.TimeoutExpired:
                    print(f"{linguagem} n={n}: passou de {LIMITE_S} s")
                    break
                print(f"{linguagem} n={n}: {tempos[0]:.2f} s")
                maior_ok, tempo_ok = n, tempos[0]
                if tempos[0] > LIMITE_S:
                    break
                n += 1
            linhas.append([linguagem, maior_ok, f"{tempo_ok:.3f}" if tempo_ok else ""])
    with open(os.path.join(PASTA_MEDICOES, "limite_60s.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["linguagem", "maior_n_ate_60s", "tempo_s"])
        w.writerows(linhas)
    for linguagem, n, t in linhas:
        print(f"{linguagem}: maior n em ate {LIMITE_S} s = {n} ({t} s)")


if __name__ == "__main__":
    main()