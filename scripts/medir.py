"""Mede o tempo das 4 implementacoes sobre os arquivos de entradas/.

- compila o C antes (sempre com -O2 -Wall)
- cada programa mede SO o algoritmo (a leitura do arquivo fica fora do cronometro)
- a primeira execucao de cada serie e descartada (aquecimento)
- salva os tempos brutos, a media/desvio e o ambiente em medicoes/

Uso: python scripts/medir.py            (15 repeticoes, alguns minutos)
     python scripts/medir.py --rapido   (3 repeticoes, so para testar o script)
"""
import csv
import os
import platform
import re
import statistics
import subprocess
import sys

from comum import PASTA_ENTRADAS, PASTA_MEDICOES, FLAGS_GCC, compilar_c, rodar

REPETICOES = 3 if "--rapido" in sys.argv else 15

# A forca bruta em Python e cerca de 20x mais lenta que em C;
# acima deste n ela levaria minutos por tamanho, entao paramos aqui.
MAX_N_FB_PYTHON = 20


def ler_cabecalho(arquivo):
    with open(arquivo) as f:
        n, alvo = f.readline().split()
    return int(n), int(alvo)


def experimentos():
    """Lista (algoritmo, linguagem, caso, arquivo) de tudo que sera medido."""
    lista = []
    for nome in sorted(os.listdir(PASTA_ENTRADAS)):
        caminho = os.path.join(PASTA_ENTRADAS, nome)
        m = re.match(r"fb_(pior|melhor|aleatorio)_n(\d+)\.txt$", nome)
        if m:
            caso, n = m.group(1), int(m.group(2))
            for linguagem in ["C", "Python"]:
                if linguagem == "Python" and n > MAX_N_FB_PYTHON:
                    continue
                lista.append(("forca_bruta", linguagem, caso, caminho))
            if caso == "pior":
                # a PD roda nas mesmas entradas para comparar algoritmo x algoritmo
                for linguagem in ["C", "Python"]:
                    lista.append(("prog_dinamica", linguagem, caso, caminho))
        elif re.match(r"pd_S\d+\.txt$", nome):
            for linguagem in ["C", "Python"]:
                lista.append(("prog_dinamica", linguagem, "pd", caminho))
    return lista


def salvar_ambiente():
    linhas = [
        f"sistema: {platform.system()} {platform.release()} ({platform.machine()})",
        f"processador: {platform.processor() or 'nao informado'}",
        f"python: {platform.python_version()}",
        f"flags do gcc: {' '.join(FLAGS_GCC)}",
        f"repeticoes por entrada: {REPETICOES} (+1 de aquecimento descartada)",
    ]
    try:
        gcc = subprocess.run(["gcc", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
        linhas.append(f"gcc: {gcc}")
    except (OSError, IndexError):
        linhas.append("gcc: nao encontrado")
    linhas.append("memoria RAM: preencher manualmente no relatorio")
    with open(os.path.join(PASTA_MEDICOES, "ambiente.txt"), "w") as f:
        f.write("\n".join(linhas) + "\n")
    print("\n".join(linhas))


def main():
    os.makedirs(PASTA_MEDICOES, exist_ok=True)
    compilar_c()
    salvar_ambiente()

    lista = experimentos()
    brutos, resumo = [], []
    for k, (algoritmo, linguagem, caso, arquivo) in enumerate(lista, 1):
        n, alvo = ler_cabecalho(arquivo)
        tempos, resposta = rodar(algoritmo, linguagem, arquivo, REPETICOES + 1)
        tempos = tempos[1:]                      # descarta o aquecimento
        media = statistics.mean(tempos)
        desvio = statistics.stdev(tempos) if len(tempos) > 1 else 0.0
        nome = os.path.basename(arquivo)
        print(f"[{k}/{len(lista)}] {algoritmo:13} {linguagem:6} {nome:22} media={media:.6f}s desvio={desvio:.6f}s resposta={resposta}")
        for r, t in enumerate(tempos, 1):
            brutos.append([algoritmo, linguagem, caso, n, alvo, nome, r, f"{t:.9f}"])
        resumo.append([algoritmo, linguagem, caso, n, alvo, nome, len(tempos),
                       f"{media:.9f}", f"{desvio:.9f}", resposta])

    with open(os.path.join(PASTA_MEDICOES, "tempos_brutos.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["algoritmo", "linguagem", "caso", "n", "alvo", "arquivo", "repeticao", "tempo_s"])
        w.writerows(brutos)
    with open(os.path.join(PASTA_MEDICOES, "resumo.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["algoritmo", "linguagem", "caso", "n", "alvo", "arquivo", "repeticoes",
                    "media_s", "desvio_s", "resposta"])
        w.writerows(resumo)
    print(f"\nresultados salvos em {PASTA_MEDICOES}")


if __name__ == "__main__":
    main()