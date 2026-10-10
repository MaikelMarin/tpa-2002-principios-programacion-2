"""
Ejercicio 10: Permutaciones recursivas
Dificultad: Avanzado

Genera todas las permutaciones de una lista de elementos.

Complejidad: O(n!) — factorial
"""

def permutaciones(lista):
    """Genera todas las permutaciones de una lista."""
    if len(lista) <= 1:
        return [lista]
    resultado = []
    for i, elemento in enumerate(lista):
        resto = lista[:i] + lista[i + 1:]
        for perm in permutaciones(resto):
            resultado.append([elemento] + perm)
    return resultado


def permutaciones_backtrack(lista):
    """Versión usando backtracking."""
    resultado = []
    n = len(lista)

    def backtrack(actual, usados):
        if len(actual) == n:
            resultado.append(actual[:])
            return
        for i in range(n):
            if not usados[i]:
                usados[i] = True
                actual.append(lista[i])
                backtrack(actual, usados)
                actual.pop()
                usados[i] = False

    backtrack([], [False] * n)
    return resultado


if __name__ == "__main__":
    lista = [1, 2, 3]
    print(f"Permutaciones de {lista}:")
    for perm in permutaciones(lista):
        print(f"  {perm}")

    print(f"\nTotal: {len(permutaciones(lista))} permutaciones")
    print(f"Esperado: {len(lista)}! = 6")

    perms = permutaciones([1, 2, 3])
    assert len(perms) == 6
    assert [1, 2, 3] in perms
    assert [3, 2, 1] in perms
    assert permutaciones_backtrack([1, 2, 3]) == permutaciones([1, 2, 3])
    print("\n✓ Todas las pruebas pasaron")
