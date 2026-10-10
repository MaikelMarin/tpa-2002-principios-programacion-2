"""
Ejercicio 1: Bubble Sort (Burbuja)
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Sumatoria aritmética (00-fundamentos §5.2): el conteo de
      comparaciones se resuelve con n(n-1)/2.
    - Invariantes de bucle (§6.4): la corrección se demuestra con un
      invariante, no con un seguimiento paso a paso.
    - Arreglos (§8.2): acceso O(1) por índice es la premisa.

PROBLEMA
    Ordenar un arreglo de menor a mayor.

ESTRATEGIA
    Comparar elementos adyacentes e intercambiarlos si están en orden
    inverso. Repetir hasta que una pasada completa no haga ningún
    intercambio.

    La idea intuitiva: los elementos "flotan" hacia su posición como
    burbujas de agua, de ahí el nombre. El elemento más grande siempre
    termina al final de cada pasada.

INVARIANTE
    Tras completar la pasada i, los i últimos elementos del arreglo
    están en su posición final y son los i mayores de todos.

    - Inicialización: antes de la pasada 0, ningún elemento está fijo.
      (Invariante vacío, se cumple.)
    - Conservación: durante la pasada i, el máximo de la región
      arr[0..n-i-1] se compara y desplaza hasta llegar a arr[n-i-1].
      Queda fijo en su posición correcta.
    - Al terminar la pasada n-1, todos los elementos están fijos.

TRAZA de burbuja([5, 3, 8, 1])
    Pasada 0 (i=0), compara hasta j=2:
      5 vs 3 → intercambio    [3, 5, 8, 1]
      5 vs 8 → no             [3, 5, 8, 1]
      8 vs 1 → intercambio    [3, 5, 1, 8]
      → el 8 quedó fijo al final
    Pasada 1 (i=1), compara hasta j=1:
      3 vs 5 → no             [3, 5, 1, 8]
      5 vs 1 → intercambio    [3, 1, 5, 8]
      → el 5 quedó fijo
    Pasada 2 (i=2), compara hasta j=0:
      3 vs 1 → intercambio    [1, 3, 5, 8]
      → el 3 quedó fijo
    Resultado: [1, 3, 5, 8]

OPTIMIZACIÓN: BANDERA DE INTERCAMBIO
    Si una pasada completa no hace ningún intercambio, el arreglo ya
    está ordenado y se puede terminar. Sin esta optimización, incluso
    un arreglo ordenado costaría Θ(n²).

    Con la bandera, el mejor caso baja a Θ(n). Es lo que hace que
    Bubble Sort sea "adaptativo".

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción sobre el número de pasadas, usando el invariante.
    Si tras la pasada i los i mayores están en su posición final,
    tras la pasada n-1 los n mayores están fijos, es decir, todo el
    arreglo está ordenado. ∎

COMPLEJIDAD
    Comparaciones, contadas exactamente:
        pasada 0: n-1, pasada 1: n-2, ..., pasada n-1: 0
        total = (n-1) + (n-2) + ... + 0 = n(n-1)/2

    Mejor caso (ordenado): Θ(n)      (una pasada, 0 intercambios)
    Promedio:             Θ(n²)
    Peor caso (inverso):  Θ(n²)

    Intercambios: exactamente uno por cada inversión del arreglo.
    Espacio: O(1) auxiliar (in-place).

PROPIEDADES
    Estable: Sí. Solo se intercambia cuando arr[j] > arr[j+1] (estricto),
    así que elementos iguales nunca se cruzan.
    In-place: Sí.
    Adaptativo: Sí, con la bandera de intercambio.

VEREDICTO
    Nunca se usa en producción. Su valor es didáctico: es el algoritmo
    más simple de analizar cuantitativamente, y por eso abre el tema.

APLICACIÓN REAL DE LA MISMA IDEA
    Detectar si un arreglo está ordenado: una pasada sin intercambios
    lo confirma en O(n). Eso sí es útil en la práctica.
"""


def bubble_sort(arr):
    """Ordena un arreglo con Bubble Sort. Modifica arr in-place.

    Recurrencia: peor caso Θ(n²), mejor caso Θ(n) con bandera.
    """
    n = len(arr)
    for i in range(n):
        intercambios = False
        # Los i últimos elementos ya están en su posición final,
        # por eso el límite es n - i - 1.
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                intercambios = True
        if not intercambios:
            break                   # ya está ordenado
    return arr


def contar_operaciones(arr):
    """Cuenta comparaciones e intercambios. Sirve para verificar
    experimentalmente que el número de comparaciones es n(n-1)/2."""
    n = len(arr)
    comparaciones = 0
    intercambios = 0
    for i in range(n):
        intercambio = False
        for j in range(0, n - i - 1):
            comparaciones += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                intercambios += 1
                intercambio = True
        if not intercambio:
            break
    return comparaciones, intercambios


def esta_ordenado(arr):
    """Detecta si un arreglo está ordenado en una sola pasada: O(n).

    Uso práctico real de la idea de Bubble Sort.
    """
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {arr}")
    print(f"Ordenado: {bubble_sort(arr[:])}")

    # Casos variados
    assert bubble_sort([64, 34, 25, 12, 22, 11, 90]) == [11, 12, 22, 25, 34, 64, 90]
    assert bubble_sort([]) == []
    assert bubble_sort([1]) == [1]
    assert bubble_sort([1, 2, 3]) == [1, 2, 3]          # ya ordenado
    assert bubble_sort([3, 2, 1]) == [1, 2, 3]          # inverso
    assert bubble_sort([5, 5, 5, 5]) == [5, 5, 5, 5]    # todos iguales

    # Estabilidad: elementos iguales no cambian de orden relativo
    parejas = [(2, 'a'), (1, 'x'), (2, 'b'), (1, 'y')]
    ordenado = bubble_sort([(k, v) for k, v in parejas])
    # Agrupar por clave y verificar que 'a' sigue antes que 'b'
    claves_1 = [v for k, v in ordenado if k == 1]
    claves_2 = [v for k, v in ordenado if k == 2]
    assert claves_1 == ['x', 'y'], "perdió estabilidad en clave 1"
    assert claves_2 == ['a', 'b'], "perdió estabilidad en clave 2"

    # Verificación cuantitativa: comparaciones = n(n-1)/2 en el peor caso
    arr_inverso = list(range(30, 0, -1))
    comps, swaps = contar_operaciones(arr_inverso[:])
    print(f"\nArreglo inverso de 30 elementos:")
    print(f"  Comparaciones: {comps}  (esperado 30·29/2 = {30*29//2})")
    print(f"  Intercambios:  {swaps}  (= número de inversiones)")
    assert comps == 30 * 29 // 2

    # Arreglo ordenado: una sola pasada con bandera
    comps_ord, _ = contar_operaciones(list(range(50)))
    print(f"  Ordenado de 50: {comps_ord} comparaciones (Θ(n), no Θ(n²))")
    assert comps_ord == 49, "la bandera debe cortar en la primera pasada"

    # Detección de orden en O(n)
    assert esta_ordenado([1, 2, 3, 4]) is True
    assert esta_ordenado([1, 3, 2]) is False

    print("\n✓ Todas las pruebas pasaron")
