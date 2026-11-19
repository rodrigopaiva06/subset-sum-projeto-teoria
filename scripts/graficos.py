"""Gera os graficos a partir de medicoes/resumo.csv.
Uso: python scripts/graficos.py   (precisa do matplotlib: pip install matplotlib)
"""
import csv
import os
import statistics

import matplotlib
matplotlib.use("Agg")                       # salva em arquivo, sem abrir janela
import matplotlib.pyplot as plt

from comum import PASTA_GRAFICOS, PASTA_MEDICOES

COR = {"C": "#2a78d6", "Python": "#eb6834", "melhor": "#1baf7a",
       "aleatorio": "#eda100", "pior": "#e34948"}
plt.rcParams.update({"axes.grid": True, "grid.alpha": 0.3,
                     "axes.spines.top": False, "axes.spines.right": False})


def ler_resumo():
    with open(os.path.join(PASTA_MEDICOES, "resumo.csv")) as f:
        linhas = list(csv.DictReader(f))
    for l in linhas:
        l["n"], l["alvo"], l["media_s"] = int(l["n"]), int(l["alvo"]), float(l["media_s"])
    return linhas


def filtrar(linhas, algoritmo, linguagem, caso):
    sel = [l for l in linhas if (l["algoritmo"], l["linguagem"], l["caso"]) == (algoritmo, linguagem, caso)]
    return sorted(sel, key=lambda l: (l["n"], l["alvo"]))


def f_fb(l):
    return 2 ** l["n"] * l["n"]              # teorico da forca bruta: 2^n * n


def f_pd(l):
    return l["n"] * l["alvo"]                # teorico da prog. dinamica: n * S


def constante(dados, f):
    """c tal que tempo = c * f: mediana das razoes tempo / f."""
    return statistics.median(d["media_s"] / f(d) for d in dados)


def salvar(nome, titulo, xlabel, ylabel="tempo médio (s)"):
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    plt.savefig(os.path.join(PASTA_GRAFICOS, nome), dpi=150, bbox_inches="tight")
    plt.close()
    print("salvo:", nome)


def teorico_x_medido(linhas, algoritmo, caso, eixo_x, f, nome, titulo, xlabel, loglog):
    """Curva medida de C e Python + curva teorica (tracejada) ajustada a cada uma."""
    plt.figure(figsize=(7, 4.5))
    for ling in ["C", "Python"]:
        d = filtrar(linhas, algoritmo, ling, caso)
        x = [l[eixo_x] for l in d]
        plt.plot(x, [l["media_s"] for l in d], "o-", color=COR[ling], label=f"{ling} (medido)")
        c = constante(d, f)
        plt.plot(x, [c * f(l) for l in d], "--", color="gray")
    plt.plot([], [], "--", color="gray", label="teórico")
    plt.yscale("log")
    if loglog:
        plt.xscale("log")
    salvar(nome, titulo, xlabel, "tempo médio (s, escala log)")


def razao(linhas):
    """T / f normalizado: perto de 1 = a complexidade teorica esta certa."""
    plt.figure(figsize=(7, 4.5))
    for ling, marcador in [("C", "o-"), ("Python", "s-")]:
        d = filtrar(linhas, "forca_bruta", ling, "pior")
        c = constante(d, f_fb)
        plt.plot([l["n"] for l in d], [l["media_s"] / f_fb(l) / c for l in d],
                 marcador, color=COR[ling], label=f"{ling}: T(n) / (2ⁿ·n)")
    plt.axhline(1, color="gray", linestyle="--")
    plt.ylim(0, 2)
    salvar("3_razao_T_sobre_f.png", "Força bruta: razão T(n) / f(n)", "n", "razão normalizada (ideal = 1)")


def algoritmo_x_algoritmo(linhas):
    """Mesmas entradas (pior caso da forca bruta) nos dois algoritmos."""
    plt.figure(figsize=(7, 4.5))
    for ling in ["C", "Python"]:
        for alg, estilo, nome in [("forca_bruta", "o-", "força bruta"), ("prog_dinamica", "o--", "prog. dinâmica")]:
            d = filtrar(linhas, alg, ling, "pior")
            plt.plot([l["n"] for l in d], [l["media_s"] for l in d], estilo, color=COR[ling], label=f"{ling}, {nome}")
    plt.yscale("log")
    salvar("4_algoritmo_x_algoritmo.png", "Força bruta × programação dinâmica", "n", "tempo médio (s, escala log)")


def casos(linhas):
    """Forca bruta em C: melhor, medio e pior caso."""
    plt.figure(figsize=(7, 4.5))
    for caso, nome in [("pior", "pior (sem solução)"), ("aleatorio", "médio (aleatório)"), ("melhor", "melhor (alvo = 1º número)")]:
        d = filtrar(linhas, "forca_bruta", "C", caso)
        plt.plot([l["n"] for l in d], [l["media_s"] for l in d], "o-", color=COR[caso], label=nome)
    plt.yscale("log")
    salvar("5_forca_bruta_casos.png", "Força bruta em C: melhor × médio × pior caso", "n", "tempo médio (s, escala log)")


def main():
    linhas = ler_resumo()
    teorico_x_medido(linhas, "forca_bruta", "pior", "n", f_fb, "1_forca_bruta_teorico.png",
                     "Força bruta (pior caso): medido × teórico 2ⁿ·n", "n", loglog=False)
    teorico_x_medido(linhas, "prog_dinamica", "pd", "alvo", f_pd, "2_prog_dinamica_teorico.png",
                     "Programação dinâmica: medido × teórico n·S (log-log)", "S (alvo), com n = 50", loglog=True)
    razao(linhas)
    algoritmo_x_algoritmo(linhas)
    casos(linhas)


if __name__ == "__main__":
    main()