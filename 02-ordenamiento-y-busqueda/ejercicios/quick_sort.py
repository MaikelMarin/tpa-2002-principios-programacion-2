"""
Ejercicio 4: Quick Sort (versión funcional)
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Divide y vencerás y Teorema Maestro (00-fundamentos §7.5).
    - Comprensiones de lista (00-fundamentos §10.3).
    - Localidad de caché (§9.3): por qué esta versión "clara" es más
      lenta que la in-place pese a tener la misma complejidad.

PROBLEMA
    Ordenar un arreglo de menor a mayor.

ESTRATEGIA (divide y vencerás)
    1. Elegir un PIVOTE del arreglo.
    2. PARTICIONAR: separar en tres grupos
         - menores que el pivote
         - iguales al pivote
         - mayores que el pivote
    3. Ordenar recursivamente los grupos de menores y mayores.
    4. Concatenar: menores + iguales + mayores.

    Observe que al terminar la partición, el pivote YA está en su
    posición final: todos los que quedan a la izquierda son menores y
    todos los de la derecha son mayores. Por eso la recursión no
    necesita volver a tocar el pivote.

¿POR QUÉ TRES GRUPOS Y NO DOS?
    Agrupar aparte los elementos iguales al pivote (partición de tres
    vías) evita el desastre con datos que tienen muchos duplicados.
    Con dos grupos y un arreglo de todos elementos iguales, la
    partición no divide nada y el algoritmo degrada a Θ(n²).
    Con tres grupos, los duplicados se resuelven de una vez.

TRAZA de quick_sort([3, 6, 1, 8, 2, 9, 4])
    quick_sort([3,6,1,8,2,9,4])
      pivote = arr[3] = 8
      menores = [3,6,1,2,4]   iguales = [8]   mayores = [9]
      → quick_sort([3,6,1,2,4]) + [8] + quick_sort([9])

    quick_sort([3,6,1,2,4])
      pivote = arr[2] = 1
      menores = []   iguales = [1]   mayores = [3,6,2,4]
      → [] + [1] + quick_sort([3,6,2,4])

    ...y así sucesivamente hasta arreglos de tamaño ≤ 1.

COMPLEJIDAD
    Recurrencia (caso equilibrado):
        T(n) = 2·T(n/2) + O(n)
    Teorema Maestro: a=2, b=2, c=1, f(n)=n=Θ(n^c) → caso 2.
    Resultado: Θ(n log n).

    Recurrencia (pivote siempre mínimo o máximo):
        T(n) = T(n-1) + O(n)
    Resultado: Θ(n²).

    Promedio sobre entradas aleatorias: Θ(n log n).

EL PIVOTE ES LA DECISIÓN CRÍTICA
    Con esta implementación el pivote es el del MEDIO, que ya evita el
    peor caso de los arreglos ordenados (donde el último elemento
    sería siempre el máximo).

    Otras estrategias:
      - Aleatorio: elimina el peor caso para entradas patológicas.
      - Mediana de tres: probar primero, medio y último; tomar la
        mediana. Mejora el equilibrio sin costo de rendimiento.
      - Introsort: si la recursión se vuelve demasiado profunda,
        cambiar a Heap Sort para garantizar O(n log n) siempre.

PROPIEDADES DE ESTA VERSIÓN
    NO estable: la partición puede reordenar elementos iguales.
    NO in-place: crea listas nuevas en cada llamada.
    Más clara, pero más lenta que la versión in-place, por dos razones:
      1. Asigna memoria nueva en cada nivel (sobrecoste del
         recolector de basura).
      2. Peor localidad de caché: los datos nuevos no están contiguos.

    La versión quick_sort_inplace.py resuelve ambos problemas.

COMPARACIÓN DE VERSIONES
    Versión              Memoria extra   Estabilidad   Claridad
    Ésta (funcional)     O(n) por nivel  No            Alta
    In-place (Lomuto)    O(log n) pila   No            Media
    Con 3 vías + Insertion O(1) aprox.   No            Baja (pero la
                                                         más rápida)
"""


def quick_sort(arr):
    """Quick Sort funcional (no in-place).

    Crea listas nuevas en cada nivel: más claro, pero usa más memoria
    y es más lento que la versión in-place.
    """
    if len(arr) <= 1:
        return arr

    # Pivote: el del medio. Evita el peor caso en arreglos ordenados.
    pivote = arr[len(arr) // 2]

    # Partición de tres vías (incluye los iguales al pivote)
    izquierda = [x for x in arr if x < pivote]
    medio = [x for x in arr if x == pivote]
    derecha = [x for x in arr if x > pivote]

    return quick_sort(izquierda) + medio + quick_sort(derecha)


if __name__ == "__main__":
    arr = [3, 6, 8, 10, 1, 2, 1]
    print(f"Original: {arr}")
    print(f"Ordenado: {quick_sort(arr[:])}")

    # Casos variados
    assert quick_sort([3, 6, 8, 10, 1, 2, 1]) == [1, 1, 2, 3, 6, 8, 10]
    assert quick_sort([]) == []
    assert quick_sort([1]) == [1]
    assert quick_sort([3, 2, 1]) == [1, 2, 3]
    assert quick_sort([5, 5, 5, 5, 5]) == [5, 5, 5, 5, 5], "muchos duplicados"
    assert quick_sort(list(range(20, 0, -1))) == list(range(1, 21)), "orden inverso"
    assert quick_sort(list(range(20))) == list(range(20)), "ya ordenado"

    # La partición de tres vías manejaduplicados sin degradar a Θ(n²)
    todos_iguales = [7] * 500
    assert quick_sort(todos_iguales) == [7] * 500

    # Coincide con el sorted() del lenguaje
    import random
    for _ in range(100):
        n = random.randint(0, 40)
        datos = [random.randint(-50, 50) for _ in range(n)]
        assert quick_sort(datos[:]) == sorted(datos)

    print("\n✓ Todas las pruebas pasaron")
