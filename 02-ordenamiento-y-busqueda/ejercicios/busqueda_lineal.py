"""
Ejercicio 6: Búsqueda lineal
Dificultad: Básico

Principio: Revisar cada elemento en orden hasta encontrar el objetivo.

Complejidad: O(n)
"""

def busqueda_lineal(arr, objetivo):
    """Busca un elemento en una lista. Retorna el índice o -1."""
    for i, elemento in enumerate(arr):
        if elemento == objetivo:
            return i
    return -1


if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Lista: {arr}")
    print(f"Buscar 22: índice {busqueda_lineal(arr, 22)}")
    print(f"Buscar 100: índice {busqueda_lineal(arr, 100)}")

    assert busqueda_lineal([64, 34, 25, 12, 22, 11, 90], 22) == 4
    assert busqueda_lineal([64, 34, 25, 12, 22, 11, 90], 100) == -1
    assert busqueda_lineal([], 5) == -1
    assert busqueda_lineal([5], 5) == 0
    print("\n✓ Todas las pruebas pasaron")
