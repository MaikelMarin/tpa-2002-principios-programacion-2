"""
Ejercicio 10: Búsqueda binaria en lista rotada
Dificultad: Experto

Una lista rotada es una lista ordenada que ha sido rotada un número
desconocido de veces. Ejemplo: [4, 5, 6, 7, 0, 1, 2]

Complejidad: O(log n)
"""

def busqueda_binaria_rotada(arr, objetivo):
    """Busca en una lista ordenada rotada."""
    izquierda, derecha = 0, len(arr) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if arr[medio] == objetivo:
            return medio
        # Determinar qué mitad está ordenada
        if arr[izquierda] <= arr[medio]:
            # Mitad izquierda ordenada
            if arr[izquierda] <= objetivo < arr[medio]:
                derecha = medio - 1
            else:
                izquierda = medio + 1
        else:
            # Mitad derecha ordenada
            if arr[medio] < objetivo <= arr[derecha]:
                izquierda = medio + 1
            else:
                derecha = medio - 1
    return -1


if __name__ == "__main__":
    arr = [4, 5, 6, 7, 0, 1, 2]
    print(f"Lista rotada: {arr}")
    print(f"Buscar 0: índice {busqueda_binaria_rotada(arr, 0)}")
    print(f"Buscar 3: índice {busqueda_binaria_rotada(arr, 3)}")

    assert busqueda_binaria_rotada([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert busqueda_binaria_rotada([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert busqueda_binaria_rotada([1], 1) == 0
    assert busqueda_binaria_rotada([1, 3], 3) == 1
    print("\n✓ Todas las pruebas pasaron")
