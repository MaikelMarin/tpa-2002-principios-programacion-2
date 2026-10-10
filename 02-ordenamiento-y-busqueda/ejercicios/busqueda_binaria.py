"""
Ejercicio 7: Búsqueda binaria
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Logaritmos (00-fundamentos §4): por qué log n pasos.
    - Invariantes de bucle (§6.4): la corrección se demuestra con el
      invariante, no con un seguimiento paso a paso.
    - Divide y vencerás: cada llamada descarta la mitad.

PROBLEMA
    Buscar un valor en una lista ORDENADA, devolviendo su índice.

PRECONDICIÓN OBLIGATORIA
    La lista DEBE estar ordenada ascendentemente.

    Si no lo está, el algoritmo puede devolver -1 aunque el valor
    exista. No lanza error: da un resultado SILENCIOSAMENTE incorrecto.
    Esta es una de las fuentes de bugs más peligrosas en programación,
    porque no hay síntoma visible.

ESTRATEGIA
    Comparar con el elemento del medio:
      - Si es el objetivo → encontrado.
      - Si el objetivo es menor → buscar solo en la mitad izquierda.
      - Si es mayor → buscar solo en la mitad derecha.

    ¿Por qué se puede descartar la mitad? Porque la lista está
    ordenada: si arr[medio] < objetivo, TODOS los elementos a la
    izquierda de medio también son menores. Ese razonamiento es
    válido solo gracias a la precondición.

INVARIANTE (la clave de la corrección)
    Al inicio de cada iteración con rango [izq, der]:
        si el objetivo está en el arreglo, entonces está en arr[izq..der]

    - Inicialización: el primer rango es todo el arreglo. Se cumple.
    - Conservación: si arr[medio] < objetivo, el valor solo puede
      estar a la derecha; el nuevo rango [medio+1, der] lo conserva.
      Análogo para el otro caso.
    - Terminación: cuando izq > der el rango está vacío; por el
      invariante el objetivo no está.

TRAZA de busqueda_binaria([2,5,8,12,16,23,38], 16)
    izq=0, der=6
    medio=3, arr[3]=12. 12 < 16 → izq = 4
    izq=4, der=6
    medio=5, arr[5]=23. 23 > 16 → der = 4
    izq=4, der=4
    medio=4, arr[4]=16. ¡IGUAL! → retorna 4

    3 comparaciones. La búsqueda lineal habría necesitado 5.

COMPLEJIDAD
    Recurrencia: T(n) = T(n/2) + O(1)
    Teorema Maestro: a=1, b=2, c=0, f(n)=1=Θ(n^0) → caso 2.
    Resultado: Θ(log n)

    Espacio: O(1) en la versión iterativa (solo dos variables).
             La versión recursiva usa O(log n) de pila.

IMPACTO CUANTIFICADO
    n              Lineal      Binaria
    10                  10           3
    1,000            1,000          10
    1,000,000    1,000,000          20
    1,000,000,000   10⁹             30

    Para mil millones de elementos, la diferencia es 50 millones de
    veces. Es la razón por la que existen los índices en las bases
    de datos: mantener los datos ordenados para poder buscar en
    O(log n) en vez de O(n).

EL COSTE DE ORDENAR ANTES DE BUSCAR
    Ordenar cuesta O(n log n) UNA vez. Después cada búsqueda cuesta
    O(log n).

    - k búsquedas sin ordenar: k × O(n)
    - k búsquedas ordenando primero: O(n log n) + k × O(log n)

    Ordenar conviene cuando:
        n log n + k log n < k n
        ⇔ aproximadamente k > log n

    Para n = 1,000,000 eso son unas 20 búsquedas. Es decir: si va a
    buscar MÁS DE ~20 VECES en el mismo conjunto, ordénelo primero.

CASOS LÍMITE
    - Lista vacía: izq=0, der=-1, izq>der → retorna -1 inmediatamente.
    - Objetivo menor que todo: siempre va a la izquierda → -1.
    - Objetivo mayor que todo: siempre va a la derecha → -1.
    - Lista de un elemento: una comparación y resuelto.
    - Valores duplicados: devuelve EL que encuentra, que puede no ser
      el primero ni el último. Si se necesita el primero, hay que
      seguir buscando hacia la izquierda (variante lower bound).

VARIANTES ÚTILES
    - Lower bound: primer índice i con arr[i] >= objetivo. También da
      la posición de insercción que mantiene el orden.
    - Upper bound: primer índice i con arr[i] > objetivo.
    - Búsqueda en lista rotada (ver binaria_rotada.py).
    - Búsqueda exponencial: para flujos infinitos o de tamaño
      desconocido; primero acota el rango duplicando, luego busca
      binario dentro.
"""


def busqueda_binaria(arr, objetivo):
    """Búsqueda binaria iterativa. Requiere arr ordenado.

    Devuelve el índice del objetivo, o -1 si no está.
    """
    izquierda, derecha = 0, len(arr) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2

        if arr[medio] == objetivo:
            return medio                      # encontrado
        elif arr[medio] < objetivo:
            izquierda = medio + 1             # descartar mitad izquierda
        else:
            derecha = medio - 1               # descartar mitad derecha

    return -1


def busqueda_binaria_recursiva(arr, objetivo, izquierda=0, derecha=None):
    """Versión recursiva: O(log n) tiempo y O(log n) espacio (pila)."""
    if derecha is None:
        derecha = len(arr) - 1
    if izquierda > derecha:
        return -1

    medio = (izquierda + derecha) // 2
    if arr[medio] == objetivo:
        return medio
    elif arr[medio] < objetivo:
        return busqueda_binaria_recursiva(arr, objetivo, medio + 1, derecha)
    else:
        return busqueda_binaria_recursiva(arr, objetivo, izquierda, medio - 1)


def lower_bound(arr, objetivo):
    """Primer índice i tal que arr[i] >= objetivo.

    Si todos los elementos son menores, devuelve len(arr). También
    indica dónde insertar para mantener el orden.
    """
    izquierda, derecha = 0, len(arr)
    while izquierda < derecha:
        medio = (izquierda + derecha) // 2
        if arr[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio
    return izquierda


if __name__ == "__main__":
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

    print(f"Lista ordenada: {arr}")
    print(f"Buscar 23: índice {busqueda_binaria(arr, 23)}")
    print(f"Buscar 2:  índice {busqueda_binaria(arr, 2)}")
    print(f"Buscar 91: índice {busqueda_binaria(arr, 91)}")
    print(f"Buscar 100: índice {busqueda_binaria(arr, 100)}")

    # Casos y valores conocidos
    assert busqueda_binaria(arr, 23) == 5
    assert busqueda_binaria(arr, 2) == 0, "primer elemento"
    assert busqueda_binaria(arr, 91) == 9, "último elemento"
    assert busqueda_binaria(arr, 100) == -1, "no encontrado"
    assert busqueda_binaria([], 5) == -1, "lista vacía"
    assert busqueda_binaria([5], 5) == 0, "un elemento"
    assert busqueda_binaria([5], 3) == -1, "un elemento ausente"

    # Las tres versiones coinciden siempre
    for objetivo in range(-5, 100):
        assert busqueda_binaria(arr, objetivo) == \
               busqueda_binaria_recursiva(arr, objetivo), f"discrepancia en {objetivo}"

    # lower_bound
    assert lower_bound(arr, 5) == 1, "5 está en índice 1"
    assert lower_bound(arr, 6) == 2, "6 iría entre 5 y 8"
    assert lower_bound(arr, 0) == 0, "menor que todo"
    assert lower_bound(arr, 999) == len(arr), "mayor que todo"

    # Verificación cuantitativa: comparaciones ≈ log2(n)
    def contar_iteraciones(arr, objetivo):
        izq, der = 0, len(arr) - 1
        pasos = 0
        while izq <= der:
            medio = (izq + der) // 2
            pasos += 1
            if arr[medio] == objetivo:
                return pasos
            elif arr[medio] < objetivo:
                izq = medio + 1
            else:
                der = medio - 1
        return pasos

    import math
    grande = list(range(0, 1000000, 2))               # 500,000 elementos
    pasos = contar_iteraciones(grande, grande[-1])    # peor caso aprox
    print(f"\nPeor caso con n={len(grande):,}: {pasos} comparaciones")
    print(f"log₂(n) = {math.log2(len(grande)):.1f}")
    assert pasos <= math.ceil(math.log2(len(grande))) + 1

    # Con duplicados devuelve un índice VÁLIDO (no necesariamente el 1º)
    con_dups = [1, 2, 2, 2, 3]
    idx = busqueda_binaria(con_dups, 2)
    assert con_dups[idx] == 2, "debe apuntar a un 2"

    print("\n✓ Todas las pruebas pasaron")
