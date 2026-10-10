"""
Ejercicio 7: Búsqueda binaria
Dificultad: Intermedio

Principio: Dividir el espacio de búsqueda a la mitad en cada paso.
Requiere lista ordenada.

Complejidad: O(log n)
"""

def busqueda_binaria(arr, objetivo):
    """Búsqueda binaria iterativa. Retorna el índice o -1."""
    izquierda, derecha = 0, len(arr) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if arr[medio] == objetivo:
            return medio
        elif arr[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1


def busqueda_binaria_recursiva(arr, objetivo, izquierda=0, derecha=None):
    """Búsqueda binaria recursiva."""
    if derecha is None:
        derecha = len(arr) - 1
    if izquierda > derecha:
        return -1
    medio = (izquierda + derecha) // 2
    if arr[medio] == objetivo:
        return medio
    elif arr[medio] < objetivo:
        return busqueda_binaria_recursiva(arr, objetivo, medio + 1, derecha)
    else:
        return busqueda_binaria_recursiva(arr, objetivo, izquierda, medio - 1)


if __name__ == "__main__":
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    print(f"Lista ordenada: {arr}")
    print(f"Buscar 23: índice {busqueda_binaria(arr, 23)}")
    print(f"Buscar 100: índice {busqueda_binaria(arr, 100)}")

    assert busqueda_binaria([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 23) == 5
    assert busqueda_binaria([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 100) == -1
    assert busqueda_binaria_recursiva([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 23) == 5
    assert busqueda_binaria_recursiva([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 100) == -1
    print("\n✓ Todas las pruebas pasaron")
