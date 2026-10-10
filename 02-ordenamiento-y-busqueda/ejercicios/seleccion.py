"""
Ejercicio 2: Selection Sort (Selección)
Dificultad: Básico

Principio: Encontrar el elemento mínimo y colocarlo en su posición
correcta. Repetir para el resto.

Complejidad: Siempre O(n²)
Propiedades: No estable, In-place, No adaptativo
"""

def selection_sort(arr):
    """Ordena una lista usando Selection Sort."""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


if __name__ == "__main__":
    arr = [64, 25, 12, 22, 11]
    print(f"Original: {arr}")
    print(f"Ordenado: {selection_sort(arr[:])}")

    assert selection_sort([64, 25, 12, 22, 11]) == [11, 12, 22, 25, 64]
    assert selection_sort([]) == []
    assert selection_sort([1]) == [1]
    assert selection_sort([3, 2, 1]) == [1, 2, 3]
    print("\n✓ Todas las pruebas pasaron")
