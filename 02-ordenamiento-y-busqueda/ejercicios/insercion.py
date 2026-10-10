"""
Ejercicio 3: Insertion Sort (Inserción)
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Número de inversiones: el costo de este algoritmo es
      proporcional a cuántos pares están en orden inverso.
    - Comprensión de "casi ordenado" como entrada favorable.

PROBLEMA
    Ordenar un arreglo de menor a mayor.

ESTRATEGIA
    Como ordenar cartas en la mano:
      1. Empezar con el primer elemento como "mano ordenada".
      2. Tomar el siguiente elemento (la "clave").
      3. Desplazar hacia la derecha todos los elementos de la mano
         que sean MAYORES que la clave.
      4. Insertar la clave en el hueco que queda.

    A diferencia de Selection Sort (que busca el mínimo de toda la
    región), aquí solo se compara con la región ya ordenada.

INVARIANTE
    Tras la iteración i, el subarreglo arr[0..i] está ordenado.

    - Inicialización: arr[0] solo, trivialmente ordenado.
    - Conservación: al insertar arr[i] en su posición correcta dentro
      de arr[0..i-1] (que ya está ordenado), arr[0..i] queda ordenado.

TRAZA de insercion([5, 2, 4, 6, 1, 3])
    i=1: clave=2. Desplazar 5. Insertar.   [2, 5, 4, 6, 1, 3]
    i=2: clave=4. Desplazar 5. Insertar.   [2, 4, 5, 6, 1, 3]
    i=3: clave=6. Nada que desplazar.      [2, 4, 5, 6, 1, 3]
    i=4: clave=1. Desplazar 6,5,4,2.       [1, 2, 4, 5, 6, 3]
            Insertar al inicio.
    i=5: clave=3. Desplazar 6,5,4.         [1, 2, 3, 4, 5, 6]
            Insertar tras el 2.

    Observe la última fila: 3 desplaza tres elementos. En total el
    número de desplazamientos es el número de INVERSIONES del arreglo.

COMPLEJIDAD, MEDIDA POR INVERSIONES
    Una inversión es un par (i, j) con i < j pero arr[i] > arr[j].

    Teorema: el número de desplazamientos (y por tanto el costo de
    Insertion Sort) es exactamente el número de inversiones.

    - Mejor caso (ordenado): 0 inversiones → Θ(n) comparaciones.
    - Peor caso (inverso): n(n-1)/2 inversiones → Θ(n²).
    - Promedio: n(n-1)/4 inversiones → Θ(n²), la mitad del peor.

    De aquí sale la ADAPTATIVIDAD: si el arreglo tiene k inversiones,
    el costo es O(n + k). Datos casi ordenados (k pequeño) se ordenan
    casi gratis.

PROPIEDADES
    Estable: Sí. Se desplazan solo los elementos ESTRICTAMENTE mayores
            que la clave, así que los iguales no se cruzan.
    In-place: Sí. O(1) de memoria auxiliar.
    Adaptativo: Sí. O(n + k) donde k = número de inversiones.
    Online: Sí. Puede ordenar elementos a medida que llegan.

POR QUÉ ES EL MÁS IMPORTANTE DE LOS TRES
    Es el mejor algoritmo para arreglos PEQUEÑOS (n ≲ 20), porque:
      1. Overhead mínimo: un solo bucle, sin llamadas a función.
      2. Excelente localidad de caché.
      3. Es estable.

    Por eso Quick Sort y Merge Sort "híbridos" delegan en él: cuando
    una partición baja del umbral, se ordena con Insertion Sort.
    TimSort (Python) e Introsort (C++) hacen exactamente eso.

APLICACIÓN REAL
    - Python: `sorted()` cambia a un método de inserción para
      corridas cortas ya ordenadas.
    - C++: `std::sort` usa Insertion Sort para particiones < 16.
    - Corrección de datos levemente desordenados: el caso de uso ideal.

EJERCICIO RELACIONADO
    ordenamiento_hibrido.py implementa Quick Sort + Insertion Sort.
"""


def insertion_sort(arr):
    """Ordena con Insertion Sort. Modifica arr in-place.

    Costo: O(n + k) donde k es el número de inversiones.
    """
    for i in range(1, len(arr)):
        clave = arr[i]                 # elemento a insertar
        j = i - 1
        # Desplazar hacia la derecha los mayores que la clave
        while j >= 0 and arr[j] > clave:
            arr[j + 1] = arr[j]
            j -= 1
        # Insertar en el hueco
        arr[j + 1] = clave
    return arr


def contar_inversiones(arr):
    """Cuenta las inversiones por fuerza bruta: O(n²).

    Sirve para verificar que el costo de Insertion Sort coincide con
    el número de inversiones.
    """
    n = len(arr)
    inversiones = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                inversiones += 1
    return inversiones


def insertion_sort_ordenado_parcial(arr):
    """Mide cuántos desplazamientos hace el algoritmo.

    Debe coincidir con el número de inversiones.
    """
    desplazamientos = 0
    for i in range(1, len(arr)):
        clave = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > clave:
            arr[j + 1] = arr[j]
            j -= 1
            desplazamientos += 1
        arr[j + 1] = clave
    return desplazamientos


if __name__ == "__main__":
    arr = [5, 2, 4, 6, 1, 3]
    print(f"Original: {arr}")
    print(f"Ordenado: {insertion_sort(arr[:])}")

    # Casos variados
    assert insertion_sort([5, 2, 4, 6, 1, 3]) == [1, 2, 3, 4, 5, 6]
    assert insertion_sort([]) == []
    assert insertion_sort([1]) == [1]
    assert insertion_sort([3, 2, 1]) == [1, 2, 3]
    assert insertion_sort([1, 2, 3, 4]) == [1, 2, 3, 4], "ya ordenado"
    assert insertion_sort([5, 5, 5, 5]) == [5, 5, 5, 5], "todos iguales"

    # Verificación: desplazamientos == número de inversiones
    print("\nVerificación de adaptatividad (desplazamientos = inversiones):")
    for datos in [[3, 1, 2], [4, 3, 2, 1], list(range(10, 0, -1)), [1, 5, 2, 6, 3]]:
        inv = contar_inversiones(datos[:])
        desp = insertion_sort_ordenado_parcial(datos[:])
        marca = "✓" if inv == desp else "✗"
        print(f"  {marca} {datos}: {inv} inversiones, {desp} desplazamientos")
        assert inv == desp

    # Mejor vs peor caso: la diferencia real de tiempos
    import time
    n = 5000                                  # 5000 (no 20000) para que
    ordenado = list(range(n))                 # el test corra rápido
    inverso = list(range(n, 0, -1))

    inicio = time.time()
    insertion_sort(ordenado[:])
    t_ordenado = time.time() - inicio

    inicio = time.time()
    insertion_sort(inverso[:])
    t_inverso = time.time() - inicio

    print(f"\nMejor caso (ordenado, n={n}): {t_ordenado*1000:.1f} ms")
    print(f"Peor caso  (inverso, n={n}): {t_inverso*1000:.1f} ms")
    print(f"Diferencia: {t_inverso/t_ordenado:,.0f}x — es la adaptatividad")

    # El ordenado debe ser muchísimo más rápido: Θ(n) vs Θ(n²)
    assert t_inverso > t_ordenado * 10, "el peor caso debe dominar"

    # Estabilidad
    parejas = [(2, 'a'), (1, 'x'), (2, 'b'), (1, 'y')]
    resultado = insertion_sort([(k, v) for k, v in parejas])
    assert [v for k, v in resultado if k == 1] == ['x', 'y']
    assert [v for k, v in resultado if k == 2] == ['a', 'b']

    # Coincide con sorted()
    import random
    random.seed(11)
    for _ in range(200):
        n = random.randint(0, 40)
        datos = [random.randint(-50, 50) for _ in range(n)]
        assert insertion_sort(datos[:]) == sorted(datos)

    print("\n✓ Todas las pruebas pasaron")
