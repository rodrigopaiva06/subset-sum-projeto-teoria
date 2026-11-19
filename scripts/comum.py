"""Funcoes usadas por varios scripts: caminhos, compilacao do C e execucao dos programas."""
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_C = os.path.join(RAIZ, "c")
PASTA_PY = os.path.join(RAIZ, "python")
PASTA_ENTRADAS = os.path.join(RAIZ, "entradas")
PASTA_MEDICOES = os.path.join(RAIZ, "medicoes")
PASTA_GRAFICOS = os.path.join(RAIZ, "graficos")

FLAGS_GCC = ["-O2", "-Wall"]
EXT = ".exe" if os.name == "nt" else ""   # no Windows o gcc gera .exe

# (algoritmo, linguagem) -> comando para rodar (sem o arquivo de entrada)
PROGRAMAS = {
    ("forca_bruta", "C"): [os.path.join(PASTA_C, "forca_bruta" + EXT)],
    ("prog_dinamica", "C"): [os.path.join(PASTA_C, "prog_dinamica" + EXT)],
    ("forca_bruta", "Python"): [sys.executable, os.path.join(PASTA_PY, "forca_bruta.py")],
    ("prog_dinamica", "Python"): [sys.executable, os.path.join(PASTA_PY, "prog_dinamica.py")],
}


def compilar_c():
    """Compila os dois programas em C com as mesmas flags sempre."""
    for nome in ["forca_bruta", "prog_dinamica"]:
        fonte = os.path.join(PASTA_C, nome + ".c")
        saida = os.path.join(PASTA_C, nome + EXT)
        cmd = ["gcc"] + FLAGS_GCC + ["-o", saida, fonte]
        print("compilando:", " ".join(cmd))
        subprocess.run(cmd, check=True)


def rodar(algoritmo, linguagem, arquivo, repeticoes=1, timeout=None):
    """Roda um programa sobre um arquivo de entrada.
    Devolve (lista de tempos em segundos, resposta)."""
    cmd = PROGRAMAS[(algoritmo, linguagem)] + [arquivo, str(repeticoes)]
    saida = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=timeout).stdout
    tempos, resposta = [], None
    for linha in saida.splitlines():
        partes = linha.split()
        if partes and partes[0] == "tempo_s":
            tempos.append(float(partes[1]))
        elif partes and partes[0] == "resposta":
            resposta = int(partes[1])
    return tempos, resposta


def escrever_entrada(caminho, nums, alvo):
    """Grava no formato combinado: 'n alvo' na 1a linha, numeros na 2a."""
    with open(caminho, "w") as f:
        f.write(f"{len(nums)} {alvo}\n")
        f.write(" ".join(map(str, nums)) + "\n")