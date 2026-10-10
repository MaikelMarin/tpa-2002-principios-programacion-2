"""
Ejercicio 6: Recorrido recursivo de matriz
Dificultad: Intermedio

Recorre una matriz (lista de listas) de forma recursiva.
"""

def recorrer_matriz(matriz, fila=0, col=0):
    """Recorre una matriz recursivamente en orden fila por fila."""
    if fila >= len(matriz):
        return
    if col >= len(matriz[0]):
        recorrer_matriz(matriz, fila + 1, 0)
        return
    print(matriz[fila][col], end=" ")
    recorrer_matriz(matriz, fila, col + 1)


def suma_matriz(matriz, fila=0, col=0):
    """Suma todos los elementos de una matriz recursivamente."""
    if fila >= len(matriz):
        return 0
    if col >= len(matriz[0]):
        return suma_matriz(matriz, fila + 1, 0)
    return matriz[fila][col] + suma_matriz(matriz, fila, col + 1)


def buscar_matriz(matriz, objetivo, fila=0, col=0):
    """Busca un elemento en una matriz recursivamente. Retorna (fila, col) o None."""
    if fila >= len(matriz):
        return None
    if col >= len(matriz[0]):
        return buscar_matriz(matriz, objetivo, fila + 1, 0)
    if matriz[fila][col] == objetivo:
        return (fila, col)
    return buscar_matriz(matriz, objetivo, fila, col + 1)


if __name__ == "__main__":
    matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    print("Recorrido: ", end="")
    recorrer_matriz(matriz)
    print()

    print(f"Suma total: {suma_matriz(matriz)}")
    print(f"Buscar 5: {buscar_matriz(matriz, 5)}")
    print(f"Buscar 10: {buscar_matriz(matriz, 10)}")

    assert suma_matriz(matriz) == 45
    assert buscar_matriz(matriz, 5) == (1, 1)
    assert buscar_matriz(matriz, 1) == (0, 0)
    assert buscar_matriz(matriz, 9) == (2, 2)
    assert buscar_matriz(matriz, 10) is None
    print("\n✓ Todas las pruebas pasaron")
