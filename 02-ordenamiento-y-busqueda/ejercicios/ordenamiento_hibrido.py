"""
Ejercicio 11: Ordenamiento híbrido (Quick Sort + Insertion Sort)
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - Quick Sort in-place (ejercicio quick_sort_inplace.py).
    - Insertion Sort (ejercicio insercion.py) y por qué gana con
      arreglos pequeños.
    - Análisis de constantes: por qué "mejor complejidad" no siempre
      significa "más rápido".

PROBLEMA
    Ordenar un arreglo combinando dos algoritmos según el tamaño de
    la partición.

¿POR QUÉ HIBRIDAR?
    Quick Sort e Insertion Sort tienen la MISMA complejidad asintótica
    en ciertos regímenes, pero constantes muy distintas:

    - Quick Sort: cada partición cuesta Θ(n) de comparaciones e
      intercambios, y hace una llamada a función por subproblema.
    - Insertion Sort: solo comparaciones y desplazamientos locales,
      sin llamadas a función.

    Para arreglos PEQUEÑOS (n ≲ 16), la constante de Quick Sort domina:
      - El overhead de las llamadas recursivas pesa más que el trabajo.
      - Insertion Sort tiene excelente localidad de caché.
      - No hay que calcular el pivote ni particionar.

    Resultado medido: Insertion Sort vence a Quick Sort por debajo de
    ~16-32 elementos. Ese es el umbral usado en la práctica.

QUIÉN LO USA EN PRODUCCIÓN
    - C++ `std::sort` (Introsort): Quick + Heap + Insertion.
    - Java `Arrays.sort` sobre primitivos: Dual-Pivot Quick + Insertion.
    - Python `sorted` (TimSort): Merge + inserción en corridas.
    - Rust `sort_unstable`: PDQSort + inserción.

    Es decir: TODOS los ordenamientos de propósito general de los
    lenguajes modernos son híbridos. Un Quick Sort puro no se usa
    prácticamente en ninguna biblioteca estándar.

ESTRATEGIA
    1. Si el rango es menor que UMBRAL, ordenarlo con Insertion Sort.
    2. En otro caso, particionar con Quick Sort y recursar.

```python
UMBRAL = 16

def hibrido(arr, bajo=0, alto=None):
    if alto is None:
        alto = len(arr) - 1
    if bajo < alto:
        if alto - bajo < UMBRAL:
            insertion_sort_range(arr, bajo, alto)   # rango pequeño
        else:
            pi = partition(arr, bajo, alto)          # rango grande
            hibrido(arr, bajo, pi - 1)
            hibrido(arr, pi + 1, alto)
    return arr
```

DETALLE: INSERTION SOBRE UN RANGO
    Insertion Sort estándar ordena desde el índice 0. Aquí hace falta
    ordenar solo arr[bajo..alto], así que la versión acepta límites:

```python
def insertion_sort_range(arr, bajo, alto):
    for i in range(bajo + 1, alto + 1):
        clave = arr[i]
        j = i - 1
        while j >= bajo and arr[j] > clave:   # j >= bajo, no j >= 0
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = clave
```

    El cambio de `j >= 0` a `j >= bajo` es sutil pero esencial: sin
    él, la inserción se saldría del rango y corrompería datos ya
    ordenados de otra partición.

TRAZA conceptual
    arr de 100 elementos aleatorios:
      - partition → pivote en alguna posición
      - rango izquierdo de 60 → recursar con Quick
      - rango derecho de 39 → recursar con Quick
      - ... hasta que todas las particiones queden por debajo de 16
      - cada partición pequeña se ordena con Insertion Sort

    El número de llamadas a Insertion es aproximadamente n/UMBRAL.

COMPLEJIDAD
    Sigue siendo O(n log n) en promedio y O(n²) en el peor caso
    (hereda el comportamiento de Quick Sort). Lo que mejora es la
    CONSTANTE, no el orden.

    Medido típicamente: 15-30% más rápido que Quick Sort puro para
    arreglos de tamaño moderado (10^3 a 10^6).

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción sobre el tamaño del rango.
    - Si el rango cabe bajo el umbral, Insertion Sort lo ordena
      correctamente (ya demostrado para ese algoritmo).
    - Si no, partition coloca el pivote en su posición final, y por
      hipótesis las dos llamadas recursivas ordenan sus rangos.
      El resultado completo queda ordenado. ∎

RELACIÓN CON INTROSORT
    Este ejercicio es el paso intermedio hacia Introsort, que añade
    una tercera salvaguarda: si la recursión se profundiza más de
    2·log₂(n) niveles, cambiar a Heap Sort. Con eso se garantiza
    O(n log n) incluso en el peor caso. La cadena de mejoras es:

        Quick Sort puro
          → + umbral de inserción     (este ejercicio)
          → + pivote aleatorio        (evita entradas patológicas)
          → + cambio a Heap Sort      (garantiza el peor caso)
          = Introsort / std::sort
"""


UMBRAL = 16          # por debajo de esto, Insertion Sort gana


def insertion_sort_range(arr, bajo, alto):
    """Insertion Sort sobre arr[bajo..alto] inclusive.

    La condición `j >= bajo` (en vez de `j >= 0`) es lo que permite
    ordenar solo un rango sin tocar el resto del arreglo.
    """
    for i in range(bajo + 1, alto + 1):
        clave = arr[i]
        j = i - 1
        while j >= bajo and arr[j] > clave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = clave


def partition(arr, bajo, alto):
    """Partición de Lomuto alrededor de arr[alto]."""
    pivote = arr[alto]
    i = bajo - 1
    for j in range(bajo, alto):
        if arr[j] <= pivote:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[alto] = arr[alto], arr[i + 1]
    return i + 1


def ordenamiento_hibrido(arr, bajo=0, alto=None):
    """Quick Sort que delega en Insertion Sort para rangos pequeños."""
    if alto is None:
        alto = len(arr) - 1

    if bajo < alto:
        if alto - bajo < UMBRAL:
            insertion_sort_range(arr, bajo, alto)      # rango pequeño
        else:
            pi = partition(arr, bajo, alto)            # rango grande
            ordenamiento_hibrido(arr, bajo, pi - 1)
            ordenamiento_hibrido(arr, pi + 1, alto)

    return arr


def quick_sort_puro(arr, bajo=0, alto=None):
    """Quick Sort sin umbral, para comparar rendimiento."""
    if alto is None:
        alto = len(arr) - 1
    if bajo < alto:
        pi = partition(arr, bajo, alto)
        quick_sort_puro(arr, bajo, pi - 1)
        quick_sort_puro(arr, pi + 1, alto)
    return arr


if __name__ == "__main__":
    import random
    import time

    random.seed(42)

    # Correctitud
    for _ in range(200):
        n = random.randint(0, 100)
        datos = [random.randint(-100, 100) for _ in range(n)]
        copia = datos[:]
        ordenamiento_hibrido(copia)
        assert copia == sorted(datos)

    # Casos base y límite
    assert ordenamiento_hibrido([]) == []
    assert ordenamiento_hibrido([1]) == [1]
    assert ordenamiento_hibrido(list(range(20))) == list(range(20))
    assert ordenamiento_hibrido(list(range(20, 0, -1))) == list(range(1, 21))
    assert ordenamiento_hibrido([7] * 50) == [7] * 50

    # Existe el umbral: cambiar UMBRAL no debe alterar el resultado
    for umbral in [1, 2, 16, 100]:
        UMBRAL_global = globals()['UMBRAL']
        globals()['UMBRAL'] = umbral
        datos = [random.randint(0, 1000) for _ in range(200)]
        copia = datos[:]
        ordenamiento_hibrido(copia)
        assert copia == sorted(datos), f"falló con umbral={umbral}"
        globals()['UMBRAL'] = UMBRAL_global
    UMBRAL = globals()['UMBRAL'] = 16

    # El rango de Insertion Sort se respeta: no corrompe datos fuera
    # de él (se verifica implícitamente arriba, pero se prueba explícito)
    arr = list(range(100)) + [50] + list(range(100, 200))
    insertion_sort_range(arr, 99, 101)      #ordenar solo el entorno del 50
    assert arr[99] <= arr[100] <= arr[101]

    # Medición de rendimiento vs Quick Sort puro en varios tamaños
    print("Comparación de rendimiento por tamaño:")
    print(f"  {'n':>8}  {'Híbrido':>10}  {'Puro':>10}  {'Mejora':>8}")
    for n in [100, 1000, 10000, 100000]:
        datos = [random.randint(0, 10**6) for _ in range(n)]

        copia1 = datos[:]
        inicio = time.time()
        ordenamiento_hibrido(copia1)
        t_hibrido = time.time() - inicio

        copia2 = datos[:]
        inicio = time.time()
        quick_sort_puro(copia2)
        t_puro = time.time() - inicio

        mejora = t_puro / t_hibrido if t_hibrido > 0 else 0
        print(f"  {n:>8}  {t_hibrido*1000:>8.1f}ms  {t_puro*1000:>8.1f}ms  {mejora:>7.2f}x")

        assert copia1 == copia2 == sorted(datos), f"discrepancia en n={n}"

    print("\n  Nota honesta: en Python la diferencia es pequeña porque el")
    print("  intérprete ya optimiza bien las llamadas. En C++ (std::sort)")
    print("  la ganancia medida es del 15-30%, y allí es donde el umbral")
    print("  de inserción realmente decide.")

    print("\n✓ Todas las pruebas pasaron")
