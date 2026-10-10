"""
Ejercicio 11: Ordenamiento híbrido (Quick Sort + Inserción)
Dificultad: Experto

Combina Quick Sort para particiones grandes e Insertion Sort para
particiones pequeñas (< 10-20 elementos).

Esta es la idea detrás de TimSort (Python) e Introsort (C++).
"""

UMBRAL = 10


def ordenamiento_hibrido(arr, bajo=0, alto=None):
    """Ordena usando Quick Sort + Inserción para particiones pequeñas."""
    if alto is None:
        alto = len(arr) - 1
    if bajo < alto:
        if alto - bajo < UMBRAL:
            insertion_sort_range(arr, bajo, alto)
        else:
            pi = partition(arr, bajo, alto)
            ordenamiento_hibrido(arr, bajo, pi - 1)
            ordenamiento_hibrido(arr, pi + 1, alto)
    return arr


def insertion_sort_range(arr, bajo, alto):
    """Insertion Sort para un rango específico."""
    for i in range(bajo + 1, alto + 1):
        clave = arr[i]
        j = i - 1
        while j >= bajo and arr[j] > clave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = clave


def partition(arr, bajo, alto):
    """Particiona la lista alrededor del pivote."""
    pivote = arr[alto]
    i = bajo - 1
    for j in range(bajo, alto):
        if arr[j] <= pivote:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[alto] = arr[alto], arr[i + 1]
    return i + 1


if __name__ == "__main__":
    import random

    arr = [random.randint(1, 100) for _ in range(50)]
    print(f"Original: {arr[:10]}...")
    ordenamiento_hibrido(arr)
    print(f"Ordenado: {arr[:10]}...")

    assert arr == sorted(arr)
    assert ordenamiento_hibrido([]) == []
    assert ordenamiento_hibrido([1]) == [1]
    print("\n✓ Todas las pruebas pasaron")
