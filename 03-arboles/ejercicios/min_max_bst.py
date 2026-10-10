r"""
Ejercicio 9: Mínimo y máximo en BST
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Invariante BST (teoria.md §4.1).
    - Búsqueda descendente (ejercicio buscar_bst.py).

PROBLEMA
    Encontrar el valor mínimo y máximo de un BST.

ESTRATEGIA (por qué es trivial en un BST)
    La invariante BST convierte esto en un recorrido directo, sin
    necesidad de explorar todo el árbol:

      - El MÍNIMO está en el extremo izquierdo: bajando siempre por
        hijo.izquierdo hasta que ya no haya.
      - El MÁXIMO está en el extremo derecho: bajando siempre por
        hijo.derecho hasta que ya no haya.

    ¿Por qué? Porque el invariante garantiza que todo el subárbol
    izquierdo es menor que la raíz. Entonces el mínimo de todo el
    árbol es el mínimo del subárbol izquierdo, y recursivamente llega
    al nodo más a la izquierda posible.

    Compare con un árbol NO ordenado, donde habría que visitar los n
    nodos (O(n)). Aquí es O(h).

TRAZA de encontrar_minimo(8) sobre:
            8
           / \
          3   10
         / \    \
        1   6    14

    partimos en 8 → hay izquierdo, bajamos
    partimos en 3 → hay izquierdo, bajamos
    partimos en 1 → NO hay izquierdo → este es el mínimo

    Solo 3 pasos (la altura), no 7 (el número de nodos).

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción sobre la altura.
    Caso base: nodo sin hijo izquierdo. Por la invariante BST, todo
    su subárbol izquierdo está vacío, así que él es el menor de su
    subárbol. Pero hay que argumentar que también es el menor de TODO
    el árbol: eso se sigue de que sus ancestros lo dejaron como
    mínimo del rango que les corresponde (se bajó por la izquierda en
    cada paso, así que el nodo es menor que todos sus ancestros).
    Paso: si hay hijo izquierdo, el mínimo global está en él (todo el
    subárbol izquierdo es menor que el nodo actual), y por hipótesis
    la recursión lo encuentra. ∎

COMPLEJIDAD
    Tiempo: O(h). Balanceado O(log n), degenerado O(n).
    Espacio: O(1) en la versión iterativa.

COMPARACIÓN CON OTRAS ESTRUCTURAS
    Estructura       Mínimo/máximo
    Arreglo ordenado O(1) (los extremos)
    Heap             O(1) (la raíz)
    BST              O(h)
    Árbol no ordenado O(n)
    Tabla hash       O(n) (no hay orden)

    El BST no es la mejor estructura para esta operación: para eso
    está el heap. Pero el BST sí permite MÁS operaciones (búsqueda,
    recorrido ordenado, rango), y eso es lo que lo justifica.

RELACIÓN CON OTROS TEMAS
    - El sucesor inorden de un nodo ES el mínimo de su subárbol
      derecho: es exactamente esta función, y es lo que se usa al
      eliminar un nodo con dos hijos (ejercicio eliminar_bst.py).
    - En grafos (tema 04), Dijkstra extrae repetidamente el vértice
      de menor distancia: esa es una operación de mínimo sobre un
      conjunto, resuelta con un heap.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def encontrar_minimo(nodo):
    """Mínimo del BST: bajar siempre por la izquierda."""
    while nodo.izquierdo:
        nodo = nodo.izquierdo
    return nodo.valor


def encontrar_maximo(nodo):
    """Máximo del BST: bajar siempre por la derecha."""
    while nodo.derecho:
        nodo = nodo.derecho
    return nodo.valor


def encontrar_minimo_recursivo(nodo):
    """Versión recursiva: O(h) de pila."""
    if nodo.izquierdo is None:
        return nodo.valor
    return encontrar_minimo_recursivo(nodo.izquierdo)


def encontrar_maximo_recursivo(nodo):
    """Versión recursiva: O(h) de pila."""
    if nodo.derecho is None:
        return nodo.valor
    return encontrar_maximo_recursivo(nodo.derecho)


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

    print(f"Mínimo: {encontrar_minimo(raiz)}")
    print(f"Máximo: {encontrar_maximo(raiz)}")

    assert encontrar_minimo(raiz) == 1
    assert encontrar_maximo(raiz) == 14

    # Las versiones recursivas coinciden
    assert encontrar_minimo_recursivo(raiz) == 1
    assert encontrar_maximo_recursivo(raiz) == 14

    # Caso base: un solo nodo
    solo = insertar(None, 42)
    assert encontrar_minimo(solo) == 42
    assert encontrar_maximo(solo) == 42

    # El mínimo/máximo coinciden con min/max de Python
    import random
    random.seed(23)
    for _ in range(100):
        n = random.randint(1, 25)
        valores = random.sample(range(-100, 101), n)
        arbol = None
        for v in valores:
            arbol = insertar(arbol, v)
        assert encontrar_minimo(arbol) == min(valores)
        assert encontrar_maximo(arbol) == max(valores)

    # El coste es O(h), no O(n): medido con un árbol degenerado
    deg = None
    for v in range(1, 101):                # degenerado a la derecha
        deg = insertar(deg, v)

    pasos = [0]
    def minimo_contando(n):
        while n.izquierdo:
            pasos[0] += 1
            n = n.izquierdo
        return n.valor
    minimo_contando(deg)
    print(f"\nDegenerado (100 nodos a la derecha): mínimo en {pasos[0]} pasos")
    assert pasos[0] == 0, "el mínimo es la raíz: 0 pasos"

    pasos = [0]
    def maximo_contando(n):
        while n.derecho:
            pasos[0] += 1
            n = n.derecho
        return n.valor
    maximo_contando(deg)
    print(f"Degenerado: máximo en {pasos[0]} pasos (=h=99, no n)")
    assert pasos[0] == 99

    # En un árbol BALANCEADO la altura es log n.
    # OJO: insertar 1..256 en orden da un árbol DEGENERADO (altura n-1),
    # no balanceado. Hay que insertar en orden equilibrado.
    import math

    def construir_balanceado(valores):
        """Construye un BST balanceado desde una lista ordenada."""
        if not valores:
            return None
        medio = len(valores) // 2
        nodo = Nodo(valores[medio])
        nodo.izquierdo = construir_balanceado(valores[:medio])
        nodo.derecho = construir_balanceado(valores[medio + 1:])
        return nodo

    bal = construir_balanceado(list(range(1, 257)))     # 256 nodos
    h_bal = altura(bal)
    print(f"Balanceado: altura {h_bal}, log₂(256) = {math.log2(256)}")
    assert h_bal == 8, f"altura {h_bal}, esperaba 8 (log2(257)≈8.01)"
    assert encontrar_minimo(bal) == 1
    assert encontrar_maximo(bal) == 256

    # Contraste: el mismo rango insertado en orden → degenerado
    deg_bal = None
    for v in range(1, 257):
        deg_bal = insertar(deg_bal, v)
    print(f"Mismo rango insertado en orden: altura {altura(deg_bal)} (degenerado)")
    assert altura(deg_bal) == 255

    print("\n✓ Todas las pruebas pasaron")
