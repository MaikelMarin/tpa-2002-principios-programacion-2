"""
Ejercicio 1: Bubble Sort (Burbuja)
Dificultad: Básico

Principio: Comparar elementos adyacentes y cambiarlos si están en orden
incorrecto. Repetir hasta que no haya intercambios.

Complejidad:
- Mejor caso: O(n) — ya ordenado
- Promedio: O(n²)
- Peor caso: O(n²)

Propiedades: Estable, In-place, Adaptativo
"""

def bubble_sort(arr):
    """Ordena una lista usando Bubble Sort."""
    n = len(arr)
    for i in range(n):
        intercambios = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                intercambios = True
        if not intercambios:
            break
    return arr


if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {arr}")
    print(f"Ordenado: {bubble_sort(arr[:])}")

    assert bubble_sort([64, 34, 25, 12, 22, 11, 90]) == [11, 12, 22, 25, 34, 64, 90]
    assert bubble_sort([]) == []
    assert bubble_sort([1]) == [1]
    assert bubble_sort([1, 2, 3]) == [1, 2, 3]
    assert bubble_sort([3, 2, 1]) == [1, 2, 3]
    print("\n✓ Todas las pruebas pasaron")
