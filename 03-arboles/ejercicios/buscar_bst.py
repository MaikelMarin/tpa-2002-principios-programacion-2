r"""
Ejercicio 5: Búsqueda en BST
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Invariante BST: izquierdo < raíz < derecho (teoria.md §4.1).
    - Logaritmos: por qué la búsqueda es O(log n) si está balanceado.
    - Comparación con búsqueda binaria sobre arreglos (tema 02).

PROBLEMA
    Buscar un valor en un BST devolviendo el nodo que lo contiene.

ESTRATEGIA
    La invariante BST permite DESCARTAR la mitad del árbol en cada
    comparación:

        si valor < nodo.valor  →  solo puede estar en el izquierdo
        si valor > nodo.valor  →  solo puede estar en el derecho
        si valor == nodo.valor →  encontrado

    Es exactamente la búsqueda binaria del tema 02, pero sobre una
    estructura con punteros en vez de con índices.

    La diferencia práctica: en un arreglo se accede al medio en O(1)
    (índice), aquí hay que bajar por los punteros. Por eso el BST
    gana cuando hay INSERCIONES frecuentes: insertar en un arreglo
    ordenado cuesta O(n) por el desplazamiento, y en un BST O(h).

TRAZA de buscar(8, valor=6) sobre:
            8               6 < 8 → bajar a la izquierda
           / \
          3   10            6 > 3 → bajar a la derecha
         / \    \
        1   6    14        ¡6 encontrado!

    3 comparaciones. En el peor caso (recorrer toda la altura), h.

DEMOSTRACIÓN DE CORRECCIÓN
    Invariante: al entrar en la llamada con subárbol T, si el valor
    está en el árbol ORIGINAL, está en T.

    - Inicialización: T es el árbol completo. Se cumple.
    - Conservación: si valor < T.raiz, por la invariante BST todo el
      subárbol derecho es mayor, así que el valor solo puede estar en
      el izquierdo. El nuevo T lo preserva. Análogo al otro lado.
    - Terminación: el subárbol se reduce en cada paso; si no se
      encuentra el valor, se llega a None, y por el invariante el
      valor no estaba.

    Si devuelve un nodo, es porque nodo.valor == valor. ∎

COMPLEJIDAD
    Tiempo: O(h).
        - BST balanceado:  h = O(log n) → O(log n)
        - BST degenerado:  h = O(n)     → O(n)
    Espacio: O(h) recursivo, O(1) iterativo.

    ¡OJO! El BST no garantiza O(log n) por sí solo. Solo lo garantiza
    si está balanceado (ver ejercicio 16). Es la diferencia entre
    "prometedor" y "garantizado".

COMPARACIÓN: BST vs ARREGLO ORDENADO
                        Arreglo ordenado    BST
    Búsqueda            O(log n)            O(h)
    Inserción           O(n) (desplaza)     O(h)
    Eliminación         O(n)                O(h)
    Mínimo/máximo       O(1) (extremos)     O(h)
    Recorrer en orden   O(n) secuencial     O(n) con pila O(h)

    El BST gana en inserciones y eliminaciones. El arreglo gana en
    localidad de caché (los datos son contiguos, §9.3), por lo que
    en la práctica la búsqueda binaria sobre arreglo suele ser más
    rápida a igualdad de complejidad.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def buscar(nodo, valor):
    """Busca en el BST. Devuelve el nodo o None."""
    if nodo is None or nodo.valor == valor:
        return nodo
    if valor < nodo.valor:
        return buscar(nodo.izquierdo, valor)
    return buscar(nodo.derecho, valor)


def buscar_iterativo(nodo, valor):
    """Versión iterativa: O(1) de espacio en vez de O(h)."""
    actual = nodo
    while actual:
        if actual.valor == valor:
            return actual
        elif valor < actual.valor:
            actual = actual.izquierdo
        else:
            actual = actual.derecho
    return None


def insertar(raiz, valor):
    """Inserta en el BST (para construir los árboles de prueba)."""
    if raiz is None:
        return Nodo(valor)
    if valor < raiz.valor:
        raiz.izquierdo = insertar(raiz.izquierdo, valor)
    elif valor > raiz.valor:
        raiz.derecho = insertar(raiz.derecho, valor)
    return raiz


def altura(nodo):
    if nodo is None:
        return -1
    return 1 + max(altura(nodo.izquierdo), altura(nodo.derecho))


if __name__ == "__main__":
    raiz = None
    for val in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        raiz = insertar(raiz, val)

    print("Búsquedas en BST:")
    for v in [6, 14, 1, 8, 99]:
        n = buscar(raiz, v)
        print(f"  Buscar {v}: {'encontrado' if n else 'no encontrado'}")

    assert buscar(raiz, 6) is not None
    assert buscar(raiz, 14) is not None
    assert buscar(raiz, 1) is not None
    assert buscar(raiz, 8) is not None, "hallar la raíz"
    assert buscar(raiz, 99) is None, "no insertado"

    # Ambas versiones coinciden
    for v in range(-5, 25):
        assert (buscar(raiz, v) is None) == (buscar_iterativo(raiz, v) is None)

    # Casos base
    assert buscar(None, 5) is None, "árbol vacío"
    solo = insertar(None, 5)
    assert buscar(solo, 5) is not None
    assert buscar(solo, 3) is None

    # El nodo devuelto contiene el valor buscado
    n = buscar(raiz, 4)
    assert n.valor == 4 and n.izquierdo is None, "4 es hoja izquierda"

    # BST balanceado: búsqueda eficiente
    bal = None
    for val in [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]:
        bal = insertar(bal, val)
    h_bal = altura(bal)
    import math
    print(f"\nBST balanceado: 16 valores, altura {h_bal} (log₂16 = 4)")
    assert h_bal == 3, f"altura {h_bal}, esperaba 3"

    # Búsqueda en el balanceado: nunca más de h+1 comparaciones
    def pasos(nodo, valor):
        c = 0
        while nodo:
            c += 1
            if nodo.valor == valor:
                return c
            nodo = nodo.izquierdo if valor < nodo.valor else nodo.derecho
        return c
    peor = max(pasos(bal, v) for v in range(1, 16))
    print(f"Peor caso medido: {peor} comparaciones (h+1 = {h_bal + 1})")
    assert peor <= h_bal + 1

    # BST degenerado: búsqueda O(n)
    deg = None
    for v in range(1, 101):
        deg = insertar(deg, v)
    h_deg = altura(deg)
    print(f"BST degenerado: 100 valores, altura {h_deg}")
    assert h_deg == 99
    assert pasos(deg, 100) == 100, "recorrió todo: O(n)"

    print("\n✓ Todas las pruebas pasaron")
