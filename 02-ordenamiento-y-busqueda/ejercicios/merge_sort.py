"""
Ejercicio 5: Merge Sort
Dificultad: Intermedio

Principio (Divide y Vencerás):
1. Dividir la lista en dos mitades
2. Ordenar recursivamente cada mitad
3. Mezclar (merge) las dos mitades ordenadas

Historia: John von Neumann lo describió en 1945.

Complejidad: Siempre O(n log n)
Propiedades: Estable, No in-place (usa O(n) extra)
"""

def merge_sort(arr):
    """Ordena una lista usando Merge Sort."""
    if len(arr) <= 1:
        return arr
    medio = len(arr) // 2
    izquierda = merge_sort(arr[:medio])
    derecha = merge_sort(arr[medio:])
    return merge(izquierda, derecha)


def merge(izquierda, derecha):
    """Mezcla dos listas ordenadas en una sola lista ordenada."""
    resultado = []
    i = j = 0
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado


if __name__ == "__main__":
    arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original: {arr}")
    print(f"Ordenado: {merge_sort(arr[:])}")

    assert merge_sort([38, 27, 43, 3, 9, 82, 10]) == [3, 9, 10, 27, 38, 43, 82]
    assert merge_sort([]) == []
    assert merge_sort([1]) == [1]
    assert merge_sort([3, 2, 1]) == [1, 2, 3]
    print("\n✓ Todas las pruebas pasaron")
