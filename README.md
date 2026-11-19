# Subset Sum - Projeto de Teoria da Computação

Projeto da disciplina de Teoria da Computação. Implementamos o problema
Subset Sum com força bruta e programação dinâmica, em C e em Python, e medimos o tempo
de cada versão para comparar com a complexidade teórica.

## Pastas

- `c/` e `python/`: os dois algoritmos em cada linguagem
- `entradas/`: arquivos de entrada (gerados pelo script)
- `scripts/`: gerar entradas, testar, medir e fazer os gráficos
- `medicoes/` e `graficos/`: resultados

Todos os programas leem o mesmo formato de arquivo:

```
n alvo
x1 x2 ... xn
```

## O que precisa

- gcc
- Python 3
- matplotlib (`pip install matplotlib`), só para os gráficos

## Como rodar

Na pasta principal do projeto:

```
python scripts/gerar_entradas.py
python scripts/testes.py
python scripts/medir.py
python scripts/limite.py
python scripts/graficos.py
```

O `medir.py` já compila o C sozinho com `-O2 -Wall`. O `limite.py` demora alguns
minutos, porque procura o maior n que a força bruta resolve em até 60 segundos.

No Mac/Linux, troque `python` por `python3`.

Para rodar um programa sozinho:

```
gcc -O2 -Wall -o c/forca_bruta c/forca_bruta.c
./c/forca_bruta entradas/exemplo.txt 15
python python/forca_bruta.py entradas/exemplo.txt 15
```

O número no final é a quantidade de repetições. No Windows, use `.\c\forca_bruta.exe`.