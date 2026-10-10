"""
Ejercicio 4: Quick Sort
Dificultad: Intermedio

Principio (Divide y Vencerás):
1. Elegir un pivote
2. Particionar: menores a la izquierda, mayores a la derecha
3. Ordenar recursivamente cada partición

Historia: Tony Hoare lo inventó en 1960 en la Universidad de Moscú.

Complejidad:
- Mejor caso: O(n log n)
- Promedio: O(n log n)
- Peor caso: O(n²) — pivote mal elegido

Propiedades: No estable, In-place (en implementación eficiente)
"""

def quick_sort(arr):
    """Ordena una lista usando Quick Sort (versión simple con listas)."""
    if len(arr) <= 1:
        return arr
    pivote = arr[len(arr) // 2]
    izquierda = [x for x in arr if x < pivote]
    medio = [x for x in arr if x == pivote]
    derecha = [x for x in arr if x > pivote]
    return quick_sort(izquierda) + medio + quick_sort(derecha)


if __name__ == "__main__":
    arr = [3, 6, 8, 10, 1, 2, 1]
    print(f"Original: {arr}")
    print(f"Ordenado: {quick_sort(arr[:])}")

    assert quick_sort([3, 6, 8, 10, 1, 2, 1]) == [1, 1, 2, 3, 6, 8, 10]
    assert quick_sort([]) == []
    assert quick_sort([1]) == [1]
    assert quick_sort([3, 2, 1]) == [1, 2, 3]
    print("\n✓ Todas las pruebas pasaron")
