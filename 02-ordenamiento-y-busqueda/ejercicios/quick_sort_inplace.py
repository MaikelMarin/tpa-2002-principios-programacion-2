"""
Ejercicio 8: Quick Sort in-place
Dificultad: Avanzado

CONOCIMIENTO PREVIO NECESARIO
    - Quick Sort funcional (ejercicio quick_sort.py).
    - Arreglos y swap (00-fundamentos §8.2).
    - Localidad de caché (§9.3): por qué esta versión es más rápida.

PROBLEMA
    Ordenar un arreglo usando Quick Sort SIN crear listas nuevas.

¿POR QUÉ EXISTE ESTA VERSIÓN?
    La versión funcional es clara, pero tiene dos costos ocultos:
      1. Memoria: crea tres listas nuevas en CADA nivel de recursión.
         Para n elementos, eso es O(n log n) de asignaciones totales.
      2. Caché: los datos nuevos no son contiguos, así que cada
         acceso tiene peor localidad.

    La versión in-place mueve los elementos DENTRO del mismo arreglo.
    Resultado: menos memoria, mejor caché, y unos 2-3x más rápida en
    la práctica pese a tener la misma complejidad.

ESTRATEGIA: PARTICIÓN DE LOMUTO
    La idea es mantener una "frontera" que separa los menores del
    pivote de los mayores:

        [ menores o iguales | mayores | pivote | sin examinar ]
                              ↑
                          frontera i

    Recorriendo j de izquierda a derecha:
      - Si arr[j] <= pivote: avanzar la frontera i e intercambiar
        arr[i] ↔ arr[j]. El elemento entra en la región de menores.
      - Si arr[j] > pivote: no hacer nada; j avanza.

    Al final, colocar el pivote justo tras la frontera (i+1), que es
    su posición definitiva.

```python
def partition(arr, bajo, alto):
    pivote = arr[alto]          # pivote = último elemento
    i = bajo - 1                # frontera (aún vacía)
    for j in range(bajo, alto):
        if arr[j] <= pivote:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[alto] = arr[alto], arr[i + 1]
    return i + 1                # posición final del pivote
```

INVARIANTE DE LA PARTICIÓN
    En cada iteración del bucle con índice j:
      1. arr[bajo..i]   contiene elementos <= pivote
      2. arr[i+1..j-1]  contiene elementos > pivote
      3. arr[j..alto-1] son los elementos sin examinar
      4. arr[alto] es el pivote

    - Inicialización: i = bajo-1 (región 1 vacía), j = bajo.
    - Conservación: si arr[j] <= pivote, se incrementa i y se
      intercambia, moviendo el elemento a la región 1. j siempre
      avanza. Si arr[j] > pivote, la región 2 se expande sola.
    - Al terminar: se coloca el pivote tras la región 1, y queda
      rodeado de menores a la izquierda y mayores a la derecha.

TRAZA de partition([8, 3, 7, 1, 9, 2], 0, 5) con pivote=2
    Inicio: i=-1, pivote=2
    j=0: arr[0]=8 > 2 → nada
    j=1: arr[1]=3 > 2 → nada
    j=2: arr[2]=7 > 2 → nada
    j=3: arr[3]=1 <= 2 → i=0, swap arr[0]↔arr[3] → [1,3,7,8,9,2]
    j=4: arr[4]=9 > 2 → nada
    Fin: swap arr[i+1=1] ↔ arr[5] → [1,2,7,8,9,3]
    Retorna 1 (posición final del pivote)

    Verificación: a la izquierda del pivote [1] todo es <= 2 ✓
                  a la derecha [7,8,9,3] todo es > 2 ✓

COMPLEJIDAD
    Partición: Θ(n) — un solo recorrido, cada elemento se compara
    una vez con el pivote.

    Recurrencias (igual que la versión funcional):
      - Pivote equilibrado: T(n) = 2T(n/2) + Θ(n) → Θ(n log n)
      - Pivote extremo:     T(n) = T(n-1) + Θ(n) → Θ(n²)

    DIFERENCIA CON LA VERSIÓN FUNCIONAL:
      Espacio auxiliar: O(1) aquí vs O(n) por nivel allí.
      Pila de recursión: O(log n) promedio, O(n) peor caso.

    OPTIMIZACIÓN DE ESPACIO: recursión por la cola. Siempre se hace
    recursión sobre la partición MÁS PEQUEÑA y se itera sobre la más
    grande. Eso garantiza que la profundidad de pila sea O(log n)
    incluso en el peor caso.

RIESGO DEL PIVOTE FIJO
    Esta implementación toma arr[alto] como pivote. Si el arreglo ya
    está ORDENADO, cada partición separa un solo elemento → Θ(n²).
    Es un fallo real documentado en sistemas de producción.

    Soluciones (no implementadas aquí, pero usadas en la práctica):
      - Pivote aleatorio: intercambiar arr[alto] con uno aleatorio.
      - Mediana de tres: tomar la mediana de arr[bajo], arr[medio],
        arr[alto].
      - IntroSort: si la profundidad supera 2·log(n), cambiar a
        Heap Sort. Garantiza Θ(n log n) siempre. Es std::sort.

PROPIEDADES
    Estable: NO (los intercambios a larga distancia reordenan).
    In-place: SÍ. Es la principal razón de usar esta versión.
    Adaptativo: NO.
"""


def partition(arr, bajo, alto):
    """Particiona arr[bajo..alto] alrededor de arr[alto] (Lomuto).

    Devuelve la posición final del pivote.
    """
    pivote = arr[alto]
    i = bajo - 1                        # frontera de los <= pivote

    for j in range(bajo, alto):
        if arr[j] <= pivote:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # Colocar el pivote justo tras la frontera
    arr[i + 1], arr[alto] = arr[alto], arr[i + 1]
    return i + 1


def quick_sort_inplace(arr, bajo=0, alto=None):
    """Quick Sort in-place. Modifica arr.

    Memoria auxiliar O(1); pila de recursión O(log n) promedio.
    """
    if alto is None:
        alto = len(arr) - 1

    if bajo < alto:
        pi = partition(arr, bajo, alto)
        quick_sort_inplace(arr, bajo, pi - 1)     # menores
        quick_sort_inplace(arr, pi + 1, alto)     # mayores

    return arr


if __name__ == "__main__":
    import random
    import time

    arr = [10, 7, 8, 9, 1, 5]
    print(f"Original: {arr}")
    quick_sort_inplace(arr)
    print(f"Ordenado: {arr}")
    assert arr == [1, 5, 7, 8, 9, 10]

    # Casos variados
    for datos in [[], [1], [3, 2, 1], list(range(15)), list(range(15, 0, -1)), [5] * 10]:
        copia = datos[:]
        quick_sort_inplace(copia)
        assert copia == sorted(datos), f"falló con {datos}"

    # Verificación exhaustiva aleatoria
    random.seed(13)
    for _ in range(300):
        n = random.randint(0, 50)
        datos = [random.randint(-100, 100) for _ in range(n)]
        copia = datos[:]
        quick_sort_inplace(copia)
        assert copia == sorted(datos)

    # Medición de rendimiento vs la versión funcional
    def quick_sort_funcional(a):
        if len(a) <= 1:
            return a
        p = a[len(a) // 2]
        return (quick_sort_funcional([x for x in a if x < p])
                + [x for x in a if x == p]
                + quick_sort_funcional([x for x in a if x > p]))

    datos = [random.randint(0, 10000) for _ in range(50000)]

    inicio = time.time()
    quick_sort_inplace(datos[:])
    t_ip = time.time() - inicio

    inicio = time.time()
    quick_sort_funcional(datos[:])
    t_fn = time.time() - inicio

    print(f"\nn=50,000 elementos:")
    print(f"  In-place:  {t_ip*1000:.1f} ms")
    print(f"  Funcional: {t_fn*1000:.1f} ms")
    print(f"  Diferencia: {t_fn/t_ip:.2f}x más rápida la in-place")

    # El pivote fijo en el último elemento degrada con datos ordenados
    print("\nAdvertencia demostrada: pivote fijo + arreglo ordenado")
    print("  (n limitado a 800 porque más allá Python agota su pila:")
    print("   ¡el propio límite de recursión es parte de la lección!)")

    import time
    for n in [400, 800]:
        ordenado = list(range(n))
        inicio = time.time()
        quick_sort_inplace(ordenado[:])
        t = time.time() - inicio
        print(f"  n={n}: {t*1000:.0f} ms (tiende a n², no a n log n)")

    # El crecimiento es cuadrático, no lineal-logarítmico:
    # duplicar n cuadruplica el tiempo (aprox), en vez de multiplicarlo
    # por ~2.2 como correspondería a n log n.
    t400 = None
    for n in [400, 800]:
        ordenado = list(range(n))
        inicio = time.time()
        quick_sort_inplace(ordenado[:])
        t = time.time() - inicio
        if n == 400:
            t400 = t
    ratio = t / t400 if t400 else 0
    print(f"  Razón 800/400 = {ratio:.1f}x (n log n daría ~2.3x; n² da 4x)")

    print("\n✓ Todas las pruebas pasaron")
