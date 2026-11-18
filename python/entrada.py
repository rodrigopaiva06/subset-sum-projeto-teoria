def ler_entrada(caminho):
    """Le o arquivo de entrada.
    1a linha: n e alvo. 2a linha: os n numeros.
    Devolve a lista de numeros e o alvo."""
    with open(caminho) as f:
        n, alvo = map(int, f.readline().split())
        nums = list(map(int, f.read().split()))
    if len(nums) != n:
        raise ValueError("quantidade de numeros diferente de n")
    return nums, alvo