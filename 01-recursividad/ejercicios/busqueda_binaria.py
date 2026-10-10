"""
Ejercicio 11: Búsqueda binaria recursiva
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Divide y vencerás: cada llamada descarta la mitad del espacio
      de búsqueda, y de ahí el O(log n).
    - Invariantes de bucle (00-fundamentos §6.4): la corrección se
      demuestra con el invariante, no con un seguimiento paso a paso.
    - Arreglo ordenado: es una PRECONDICIÓN, no una opción.

PROBLEMA
    Buscar un valor en una lista ORDENADA devolviendo su índice.

FONDO MATEMÁTICO
    Si la lista está ordenada, comparar con el elemento del medio
    permite descartar la mitad entera:
      - Si el objetivo es menor, solo puede estar en la mitad izquierda.
      - Si es mayor, solo en la mitad derecha.

    ¿Cuántas veces se puede dividir n a la mitad hasta llegar a 1?
    Exactamente ⌊log₂ n⌋. Esa es la profundidad de la recursión.

    Precondición indispensable: la lista DEBE estar ordenada. Si no lo
    está, el algoritmo puede devolver -1 aunque el valor exista. No
    valida el orden (sería O(n) y anularía la ventaja).

ESTRATEGIA
    1. Si izq > der, el rango está vacío → no encontrado (-1).
    2. Calcular medio = (izq + der) // 2.
    3. Si arr[medio] == objetivo → encontrado, devolver medio.
    4. Si arr[medio] < objetivo → buscar en [medio+1, der].
    5. Si arr[medio] > objetivo → buscar en [izq, medio-1].

TRAZA DE busqueda_binaria([2,5,8,12,16,23], 16)
    Llamada        izq der  medio  arr[medio]  Acción
    bb(arr,0,5)     0   5    2      8          8<16 → der. [3,5]
    bb(arr,3,5)     3   5    4      16         ¡encontrado! retorna 4

    Solo 2 comparaciones para 6 elementos. La búsqueda lineal
    necesitaría 5.

INVARIANTE (la clave de la corrección)
    Al inicio de cada llamada con rango [izq, der]:
        si el objetivo está en el arreglo, entonces está en arr[izq..der].

    - Inicialización: el primer rango es todo el arreglo. Se cumple.
    - Conservación: si arr[medio] < objetivo, el valor (si existe)
      está a la derecha, y el nuevo rango lo conserva. Análogo para
      el otro caso.
    - Terminación: el rango se reduce estrictamente; cuando se vacía,
      por el invariante el objetivo no estaba.

DEMOSTRACIÓN DE CORRECCIÓN
    Se sigue directamente del invariante: si la función devuelve un
    índice i, entonces arr[i] == objetivo (se retorna justo cuando
    se verifica la igualdad). Si devuelve -1, el rango se vació sin
    encontrar el valor, y por el invariante el valor no está. ∎

COMPLEJIDAD
    Recurrencia: T(n) = T(n/2) + O(1)
    Teorema Maestro (a=1, b=2, c=0, f=1=Θ(n^0)): caso 2.
    Tiempo: O(log n)
    Espacio: O(log n) de pila. La versión iterativa usa O(1).

IMPACTO PRÁCTICO
    n              Lineal      Binaria
    1,000             1,000           10
    1,000,000     1,000,000           20
    1,000,000,000  10^9               30

    Un factor de 50 millones para mil millones de elementos. Es la
    razón por la que los índices de bases de datos existen.

CASOS LÍMITE
    - Lista vacía: izq=0, der=-1, izq>der → retorna -1.
    - Objetivo menor que todo: se va siempre a la izquierda → -1.
    - Objetivo mayor que todo: se va siempre a la derecha → -1.
    - Lista de un elemento: se compara y listo.
    - Valores duplicados: devuelve EL que encuentra primero, no
      necesariamente el primero de la lista. Si se necesita el
      primer o el último, hay que seguir buscando (variante).

VARIANTE: LISTA ROTADA
    Una lista ordenada rotada ([4,5,6,7,0,1,2]) NO está ordenada, así
    que la búsqueda binaria estándar falla. Pero siempre se puede
    determinar qué mitad está ordenada y buscar allí. Es el ejercicio
    binaria_rotada.py del tema 02.
"""


def busqueda_binaria_recursiva(arr, objetivo, izquierda=0, derecha=None):
    """Búsqueda binaria recursiva. Requiere lista ordenada.

    Devuelve el índice del objetivo, o -1 si no está.
    """
    if derecha is None:
        derecha = len(arr) - 1

    # Caso base: rango vacío
    if izquierda > derecha:
        return -1

    medio = (izquierda + derecha) // 2

    if arr[medio] == objetivo:
        return medio                      # encontrado
    elif arr[medio] < objetivo:
        return busqueda_binaria_recursiva(arr, objetivo, medio + 1, derecha)
    else:
        return busqueda_binaria_recursiva(arr, objetivo, izquierda, medio - 1)


def busqueda_binaria_iterativa(arr, objetivo):
    """Versión iterativa: O(1) de espacio en vez de O(log n)."""
    izquierda, derecha = 0, len(arr) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if arr[medio] == objetivo:
            return medio
        elif arr[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1


def busqueda_lineal(arr, objetivo):
    """Búsqueda lineal: O(n). Se incluye para comparar resultados."""
    for i, elemento in enumerate(arr):
        if elemento == objetivo:
            return i
    return -1


if __name__ == "__main__":
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

    print(f"Lista ordenada: {arr}")
    print(f"Buscar 23: índice {busqueda_binaria_recursiva(arr, 23)}")
    print(f"Buscar 2:  índice {busqueda_binaria_recursiva(arr, 2)}")
    print(f"Buscar 91: índice {busqueda_binaria_recursiva(arr, 91)}")
    print(f"Buscar 100: índice {busqueda_binaria_recursiva(arr, 100)}")

    # Caso base y casos generales
    assert busqueda_binaria_recursiva(arr, 23) == 5
    assert busqueda_binaria_recursiva(arr, 100) == -1
    assert busqueda_binaria_recursiva([], 5) == -1, "lista vacía"
    assert busqueda_binaria_recursiva([5], 5) == 0, "un elemento"
    assert busqueda_binaria_recursiva([5], 3) == -1, "un elemento ausente"

    # Las tres versiones coinciden para todo valor buscado
    for objetivo in range(-5, 100):
        r = busqueda_binaria_recursiva(arr, objetivo)
        i = busqueda_binaria_iterativa(arr, objetivo)
        l = busqueda_lineal(arr, objetivo)
        assert r == i == l, f"discrepancia buscando {objetivo}"

    # La media del invariante: con duplicados, devuelve uno válido
    con_dups = [1, 2, 2, 2, 3]
    idx = busqueda_binaria_recursiva(con_dups, 2)
    assert con_dups[idx] == 2

    print("\n✓ Todas las pruebas pasaron")
