"""
Ejercicio 2: Selection Sort (Selección)
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Sumatoria aritmética (00-fundamentos §5.2).
    - Análisis por número de escrituras, no solo de comparaciones.

PROBLEMA
    Ordenar un arreglo de menor a mayor.

ESTRATEGIA
    1. Buscar el MÍNIMO de la región no ordenada.
    2. Intercambiarlo con el primer elemento de esa región.
    3. Repetir para el resto del arreglo.

    Es el algoritmo más simple de "seleccionar": en cada pasada se
    SELECCIONA el siguiente elemento que va en su lugar.

INVARIANTE
    Tras la pasada i, los primeros i elementos del arreglo son los i
    menores de todos, y están ordenados.

    - Conservación: en la pasada i se busca el mínimo en arr[i..n-1] y
      se coloca en arr[i]. Como los i-1 anteriores ya eran los menores,
      el nuevo entra en su posición correcta al final.

TRAZA de seleccion([64, 25, 12, 22, 11])
    Pasada 0: buscar mínimo en [64,25,12,22,11] → 11 (índice 4)
               intercambiar arr[0] ↔ arr[4]  →  [11, 25, 12, 22, 64]
    Pasada 1: buscar mínimo en [25,12,22,64] → 12 (índice 2)
               intercambiar arr[1] ↔ arr[2]  →  [11, 12, 25, 22, 64]
    Pasada 2: buscar mínimo en [25,22,64] → 22 (índice 3)
               intercambiar arr[2] ↔ arr[3]  →  [11, 12, 22, 25, 64]
    Pasada 3: buscar mínimo en [25,64] → 25 (ya está)
               sin intercambio                →  [11, 12, 22, 25, 64]

    Resultado: [11, 12, 22, 25, 64]

COMPLEJIDAD: SIEMPRE Θ(n²), SIN EXCEPCIONES
    Comparaciones, contadas exactamente:
        pasada 0: n-1, pasada 1: n-2, ..., pasada n-2: 1
        total = (n-1) + (n-2) + ... + 1 = n(n-1)/2 = Θ(n²)

    A DIFERENCIA de Bubble Sort e Insertion Sort, este conteo NO
    depende del orden de entrada. Siempre se recorre toda la región
    no ordenada buscando el mínimo.

    Intercambios: exactamente n-1 como máximo (uno por pasada, salvo
    la última). Es el MÍNIMO número de escrituras posible entre los
    algoritmos de comparación elementales.

POR QUÉ ESTA PROPIEDAD IMPORTA (EL ÚNICO USO REAL)
    El costo de escritura puede ser MUCHO mayor que el de lectura:
      - Memoria flash y EEPROM: cada escritura desgasta físicamente
        la celda y tiene un límite de ciclos (~10,000 a 100,000).
      - Registros en disco: una escritura puede forzar una
        reorganización física si el registro no cabe en su sitio.
      - Estructuras con bloqueo: escribir requiere exclusión mutua.

    En esos escenarios, Selection Sort gana pese a hacer el mismo
    número de comparaciones, porque minimiza las ESCRITURAS a n-1.

PROPIEDADES
    Estable: NO. El intercambio a larga distancia puede mover un
            elemento por delante de otro igual. Ejemplo:
            [4a, 4b, 1] → mínimo es 1, se intercambia con 4a
            → [1, 4b, 4a]: el orden relativo de los 4 se invirtió.
    In-place: Sí. O(1) de memoria auxiliar.
    Adaptativo: NO. Ninguna optimización lo acelera con datos
                parcialmente ordenados.

COMPARACIÓN CON LOS OTROS DOS CUADRÁTICOS
    Algoritmo      Mejor caso   Intercambios   Escrituras   Uso real
    Burbuja        Θ(n)         O(inversiones) Alto          Docente
    Inserción      Θ(n)         O(inversiones) Medio         Arreglos
                                                           pequeños
    Selección      Θ(n²)        n-1            MÍNIMO        Flash/EEPROM

EJERCICIO RELACIONADO
    Ordenamiento hibrido (ordenamiento_hibrido.py) muestra cómo los
    algoritmos eficientes delegan en Insertion Sort, no en este.
"""


def selection_sort(arr):
    """Ordena con Selection Sort. Modifica arr in-place.

    Peor caso = mejor caso = Θ(n²) comparaciones.
    Intercambios: como máximo n-1.
    """
    n = len(arr)
    for i in range(n):
        # Suponer que el mínimo está en la posición i
        minimo = i
        # Buscar si hay uno menor en el resto
        for j in range(i + 1, n):
            if arr[j] < arr[minimo]:
                minimo = j
        # Colocar el mínimo encontrado en su posición
        arr[i], arr[minimo] = arr[minimo], arr[i]
    return arr


def contar_operaciones(arr):
    """Cuenta comparaciones e intercambios para verificar el análisis."""
    n = len(arr)
    comparaciones = 0
    intercambios = 0
    for i in range(n):
        minimo = i
        for j in range(i + 1, n):
            comparaciones += 1
            if arr[j] < arr[minimo]:
                minimo = j
        if minimo != i:
            arr[i], arr[minimo] = arr[minimo], arr[i]
            intercambios += 1
    return comparaciones, intercambios


if __name__ == "__main__":
    arr = [64, 25, 12, 22, 11]
    print(f"Original: {arr}")
    print(f"Ordenado: {selection_sort(arr[:])}")

    # Casos variados
    assert selection_sort([64, 25, 12, 22, 11]) == [11, 12, 22, 25, 64]
    assert selection_sort([]) == []
    assert selection_sort([1]) == [1]
    assert selection_sort([3, 2, 1]) == [1, 2, 3]
    assert selection_sort([5, 5, 5]) == [5, 5, 5]
    assert selection_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5], "ya ordenado"

    # Verificación cuantitativa: comparaciones SIEMPRE n(n-1)/2
    for n in [5, 10, 20]:
        comps, swaps = contar_operaciones(list(range(n, 0, -1)))
        assert comps == n * (n - 1) // 2, f"n={n}: {comps} comparaciones"

    # El orden de entrada NO cambia el número de comparaciones
    comps_ord, swaps_ord = contar_operaciones(list(range(20)))
    comps_inv, swaps_inv = contar_operaciones(list(range(20, 0, -1)))
    print(f"\nComparaciones (ordenado):    {comps_ord}")
    print(f"Comparaciones (inverso):     {comps_inv}")
    assert comps_ord == comps_inv, "no debe depender del orden"
    assert comps_ord == 20 * 19 // 2

    # Intercambios: máximo n-1
    assert swaps_inv <= 19, "como máximo n-1 intercambios"

    # Verificar que NO es estable, comparando SOLO por la primera componente
    # (no por la tupla completa, que rompería el empate artificialmente)
    def solo_clave(par):
        return par[0]

    def selection_sort_por_clave(arr):
        n = len(arr)
        for i in range(n):
            minimo = i
            for j in range(i + 1, n):
                if solo_clave(arr[j]) < solo_clave(arr[minimo]):
                    minimo = j
            arr[i], arr[minimo] = arr[minimo], arr[i]
        return arr

    parejas = [(4, 'a'), (4, 'b'), (1, 'x')]
    resultado = selection_sort_por_clave(parejas[:])
    claves_4 = [v for k, v in resultado if k == 4]
    print(f"Orden de los '4' tras ordenar: {claves_4}")
    print("  (Selection Sort NO es estable: los 4 quedan invertidos)")
    assert claves_4 == ['b', 'a'], "Selection Sort debería invertir los iguales"

    # Comparar con Insertion Sort, que SÍ es estable
    def insertion_sort_por_clave(arr):
        for i in range(1, len(arr)):
            clave = arr[i]
            j = i - 1
            while j >= 0 and solo_clave(arr[j]) > solo_clave(clave):
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = clave
        return arr

    resultado_i = insertion_sort_por_clave(parejas[:])
    claves_4_i = [v for k, v in resultado_i if k == 4]
    assert claves_4_i == ['a', 'b'], "Insertion Sort debería ser estable"
    print(f"Insertion Sort, mismos datos: {claves_4_i} (estable ✓)")

    # Coincide con sorted() en valores, no en estabilidad
    import random
    random.seed(3)
    for _ in range(100):
        n = random.randint(0, 30)
        datos = [random.randint(-50, 50) for _ in range(n)]
        assert selection_sort(datos[:]) == sorted(datos)

    print("\n✓ Todas las pruebas pasaron")
