"""
Ejercicio 5: Merge Sort
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Divide y vencerás y Teorema Maestro (00-fundamentos §7.5): la
      recurrencia T(n) = 2T(n/2) + Θ(n) se resuelve por el caso 2.
    - Comprensiones de lista y slicing (00-fundamentos §10.3).

PROBLEMA
    Ordenar un arreglo de menor a mayor.

ESTRATEGIA (divide y vencerás)
    La diferencia con Quick Sort: aquí el trabajo difícil se hace al
    MEZCLAR, no al partir.

    1. DIVIDIR el arreglo en dos mitades por la mitad.
    2. Ordenar recursivamente cada mitad.
    3. MEZCLAR las dos mitades ordenadas en un solo arreglo ordenado.

    Particionar es trivial (cortar por la mitad). Todo el esfuerzo
    está en la mezcla, que compara las cabezas de ambas mitades y
    toma siempre la menor.

INVARIANTE DE LA MEZCLA
    En cada paso de la mezcla, `resultado` contiene los menores
    elementos ya vistos de ambas mitades, en orden.

TRAZA COMPLETA de merge_sort([38, 27, 43, 3])
    Dividir:
        [38, 27, 43, 3] → [38, 27] y [43, 3]
        [38, 27] → [38] y [27]
        [43, 3]  → [43] y [3]

    Mezclar (de abajo hacia arriba):
        merge([38], [27]):
            38 vs 27 → toma 27 → [27]
            38 vs (vacío) → toma 38 → [27, 38]
        merge([43], [3]):
            43 vs 3 → toma 3 → [3]
            43 vs (vacío) → toma 43 → [3, 43]
        merge([27,38], [3,43]):
            27 vs 3  → toma 3    → [3]
            27 vs 43 → toma 27   → [3, 27]
            38 vs 43 → toma 38   → [3, 27, 38]
            (izq vacía) → toma 43 → [3, 27, 38, 43]

    Resultado: [3, 27, 38, 43]

DETALLE CRÍTICO: POR QUÉ <= Y NO <
    En la comparación `izq[i] <= der[j]`, el `<=` es lo que hace el
    algoritmo ESTABLE.

    Si se usara `<` estricto, ante elementos iguales se tomaría
    primero de la derecha, invirtiendo el orden relativo original.
    Con `<=` se toma primero de la izquierda, preservándolo.

DEMOSTRACIÓN DE CORRECCIÓN
    Caso base: arreglo de ≤ 1 elemento, ya ordenado.

    Hipótesis: merge_sort ordena correctamente arreglos de tamaño < n.

    Paso: para tamaño n, se divide en dos partes de tamaño n/2, que
    por hipótesis quedan ordenadas. La mezcla produce una secuencia
    ordenada si y solo si ambas entradas están ordenadas (invariante
    de la mezcla: siempre se toma el menor de las dos cabezas). ∎

COMPLEJIDAD
    Recurrencia: T(n) = 2·T(n/2) + Θ(n)
    Teorema Maestro: a=2, b=2, c=1. f(n) = n = Θ(n^c) → caso 2.
    Resultado: Θ(n log n) en TODOS los casos (mejor, promedio, peor).

    Es la gran ventaja sobre Quick Sort: el rendimiento es predecible.
    No hay entrada patológica.

    Espacio: O(n) auxiliar para la mezcla. NO es in-place.

CUÁNDO USAR MERGE SORT EN VEZ DE QUICK SORT
    1. Se necesita ESTABILDAN garantizada.
    2. Se necesita la garantía de Θ(n log n) en el peor caso.
    3. Los datos NO caben en memoria (ordenamiento externo, tema 06):
       Merge Sort solo lee y escribe secuencialmente.
    4. La estructura es una lista enlazada: no requiere acceso
       aleatorio (ver merge_sort_lista_enlazada.py).

PROPIEDADES
    Estable: Sí (por el <=).
    In-place: No. O(n) de memoria auxiliar.
    Adaptativo: No. Siempre hace el mismo trabajo.

APLICACIÓN REAL
    - Python: `sorted()` y `list.sort()` usan TimSort, que es una
      evolución de Merge Sort con detección de corridas ordenadas.
    - Java: `Arrays.sort()` sobre objetos usa TimSort; sobre
      primitivos usa Dual-Pivot Quicksort.
    - C++: `std::stable_sort` es Merge Sort.
"""


def merge(izq, der):
    """Mezcla dos listas ordenadas en una sola ordenada.

    El `<=` (no `<`) es lo que garantiza estabilidad.
    """
    resultado = []
    i = j = 0

    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1

    # Al menos una de las dos quedó vacía; añadir el resto tal cual
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado


def merge_sort(arr):
    """Ordena con Merge Sort: Θ(n log n) siempre, estable, O(n) extra."""
    if len(arr) <= 1:
        return arr

    medio = len(arr) // 2
    izquierda = merge_sort(arr[:medio])     # ordenar mitad izquierda
    derecha = merge_sort(arr[medio:])       # ordenar mitad derecha
    return merge(izquierda, derecha)         # mezclar


if __name__ == "__main__":
    arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original: {arr}")
    print(f"Ordenado: {merge_sort(arr[:])}")

    # Casos variados
    assert merge_sort([38, 27, 43, 3, 9, 82, 10]) == [3, 9, 10, 27, 38, 43, 82]
    assert merge_sort([]) == []
    assert merge_sort([1]) == [1]
    assert merge_sort([3, 2, 1]) == [1, 2, 3]
    assert merge_sort(list(range(15))) == list(range(15))          # ya ordenado
    assert merge_sort(list(range(15, 0, -1))) == list(range(1, 16))  # inverso

    # El peor caso es igual que el mejor: Θ(n log n) siempre
    import time
    for n in [10000, 50000]:
        datos = list(range(n, 0, -1))
        inicio = time.time()
        merge_sort(datos[:])
        print(f"  n={n}: {(time.time()-inicio)*1000:.1f} ms (peor caso)")

    # Estabilidad verificada
    parejas = [(2, 'a'), (1, 'x'), (2, 'b'), (1, 'y')]
    ordenado = merge_sort([(k, v) for k, v in parejas])
    assert [v for k, v in ordenado if k == 1] == ['x', 'y']
    assert [v for k, v in ordenado if k == 2] == ['a', 'b']

    # Coincide con sorted() en todos los casos aleatorios
    import random
    random.seed(7)
    for _ in range(200):
        n = random.randint(0, 60)
        datos = [random.randint(-99, 99) for _ in range(n)]
        assert merge_sort(datos[:]) == sorted(datos)

    print("\n✓ Todas las pruebas pasaron")
