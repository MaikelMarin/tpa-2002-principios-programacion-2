"""
Ejercicio 6: Búsqueda lineal
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Notación asintótica (00-fundamentos §2): por qué Θ(n).
    - Enumeración de listas (`enumerate`).

PROBLEMA
    Determinar si un valor está en una lista y en qué posición.

ESTRATEGIA
    Revisar cada elemento en orden hasta encontrar el objetivo.
    Si se termina la lista sin encontrarlo, no está.

    Es el único algoritmo de búsqueda que funciona en listas
    DESORDENADAS. No requiere ninguna precondición, y esa es
    precisamente su virtud y su límite.

TRAZA de busqueda_lineal([64,34,25,12], 25)
    i=0: 64 == 25? No
    i=1: 34 == 25? No
    i=2: 25 == 25? Sí → retorna 2

    3 comparaciones de 4 elementos.

COMPLEJIDAD
    Sea n el tamaño de la lista.
    Mejor caso (objetivo en la posición 0):      Θ(1)
    Peor caso (objetivo al final o ausente):     Θ(n)
    Promedio (objetivo en posición aleatoria):   Θ(n/2) = Θ(n)

    En todos los casos ≢ Ω(n) en el peor caso, porque hay que
    confirmar la ausencia recorriendo todo.

DEMOSTRACIÓN DE CORRECCIÓN
    Si el algoritmo devuelve i, entonces arr[i] == objetivo (se
    retorna justo tras verificar la igualdad).
    Si devuelve -1, se examinaron los n elementos y ninguno coincidió,
    luego el objetivo no está. ∎

CUÁNDO USARLA
    SÍ:
      - La lista no está ordenada.
      - Solo se busca UNA vez (ordenar costaría más).
      - La estructura no permite acceso por índice.
      - n es pequeño.

    NO:
      - La lista está ordenada → búsqueda binaria (O(log n)).
      - Se busca MUCHAS veces → ordenar una vez y buscar binario.
      - Los datos son grandes y estáticos → tabla hash o índice.

COMPARACIÓN CON BÚSQUEDA BINARIA
    n              Lineal          Binaria (requiere orden)
    1,000             1,000               10
    1,000,000     1,000,000               20
    10⁹              10⁹                  30

    La binaria es absurdamente mejor, pero exige ordenar primero
    (O(n log n) una vez). Ver el análisis de costo en busqueda_binaria.py.

RELACIÓN CON OTROS TEMAS
    - El recorrido de un árbol o grafo (temas 03 y 04) es una
      generalización de esta idea: visitar cada nodo una vez.
    - El análisis de "visitar cada elemento una vez" da complejidad
      O(n) que aparece en todos los recorridos del proyecto.
"""


def busqueda_lineal(arr, objetivo):
    """Busca objetivo en arr. Devuelve el índice o -1.

    Funciona en listas ordenadas y desordenadas.
    """
    for i, elemento in enumerate(arr):
        if elemento == objetivo:
            return i
    return -1


def contar_comparaciones(arr, objetivo):
    """Cuenta comparaciones para verificar el análisis asintótico."""
    for i, elemento in enumerate(arr):
        if elemento == objetivo:
            return i + 1                 # comparaciones hasta encontrarlo
    return len(arr)                      # se recorrió todo


if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Lista: {arr}")
    print(f"Buscar 22: índice {busqueda_lineal(arr, 22)}")
    print(f"Buscar 100: índice {busqueda_lineal(arr, 100)}")

    # Caso base
    assert busqueda_lineal([], 5) == -1, "lista vacía"
    assert busqueda_lineal([5], 5) == 0, "un elemento, encontrado"
    assert busqueda_lineal([5], 3) == -1, "un elemento, no encontrado"

    # Caso general
    assert busqueda_lineal([64, 34, 25, 12, 22, 11, 90], 22) == 4
    assert busqueda_lineal([64, 34, 25, 12, 22, 11, 90], 100) == -1

    # Funciona en lista DESORDENADA (a diferencia de la binaria)
    desordenada = [9, 3, 7, 1, 5, 8]
    assert busqueda_lineal(desordenada, 7) == 2
    assert busqueda_lineal(desordenada, 4) == -1

    # Devuelve la PRIMERA aparición, no cualquiera
    con_dups = [5, 3, 5, 3, 5]
    assert busqueda_lineal(con_dups, 5) == 0, "primera aparición"

    # Verificación cuantitativa del análisis
    print("\nComparaciones según posición del objetivo:")
    for pos in [0, len(arr) // 2, len(arr) - 1]:
        comps = contar_comparaciones(arr, arr[pos])
        print(f"  Posición {pos}: {comps} comparaciones")
    comps_ausente = contar_comparaciones(arr, 999)
    print(f"  Ausente: {comps_ausente} comparaciones (recorre todo)")
    assert comps_ausente == len(arr)

    # Mejor caso: Θ(1). Peor caso: Θ(n).
    assert contar_comparaciones(arr, arr[0]) == 1, "mejor caso es 1 comparación"
    assert contar_comparaciones(arr, arr[-1]) == len(arr), "peor caso es n"

    # Coincide con list.index cuando el elemento existe
    import random
    random.seed(5)
    for _ in range(100):
        n = random.randint(1, 30)
        datos = [random.randint(0, 20) for _ in range(n)]
        obj = random.choice(datos)
        assert busqueda_lineal(datos, obj) == datos.index(obj)

    print("\n✓ Todas las pruebas pasaron")
