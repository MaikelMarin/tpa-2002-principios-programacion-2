r"""
Ejercicio 4: Altura de un árbol
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Logaritmos (00-fundamentos §4): por qué la altura importa.
    - Inducción estructural.
    - Diferencia entre altura y número de nodos.

PROBLEMA
    Calcular la altura de un árbol binario en ARISTAS (no en nodos).

FONDO MATEMÁTICO
    La altura de un árbol con n nodos está acotada:
        ⌊log₂ n⌋ ≤ altura ≤ n − 1

    El mínimo se da en un árbol perfecto (2^(h+1) − 1 nodos). El
    máximo, en un árbol degenerado (un solo nodo por nivel).

    La altura es la métrica que gobierna el coste de TODAS las
    operaciones de un BST: O(h). De ahí que el balanceo sea el tema
    central del resto del curso.

CONVENCIÓN: ARISTAS, NO NODOS
    Este proyecto usa la convención de aristas:
        - Árbol vacío:      altura = −1
        - Árbol de 1 nodo:  altura = 0
    La convención alternativa (contar nodos en el camino) daría 0 y 1
    respectivamente. Ambas son válidas; hay que ser CONSISTENTE, y
    documentar cuál se usa. Cormen usa nodos; nosotros usamos aristas
    porque hace que las fórmulas de balance (BF = h(izq) − h(der))
    salgan limpias.

ESTRATEGIA
    Combinar con MÁXIMO, no con suma (ese es el error clásico del
    ejercicio 3):

        altura(nodo) = 1 + max(altura(izq), altura(der))
        altura(None) = -1

    El −1 del caso base hace que una hoja devuelva
    1 + max(−1, −1) = 0. Correcto.

    También se calcula la PROFUNDIDAD de un valor concreto (cuántas
    aristas hay desde la raíz hasta él), que es una operación distinta.

TRAZA de altura() sobre:
            1          altura = 0
           / \
          2   3        altura = 1
         /
        4              altura = 2

    altura(1) = 1 + max(altura(2), altura(3))
    altura(2) = 1 + max(altura(4), altura(None))
              = 1 + max(0, −1) = 1
    altura(3) = 1 + max(−1, −1) = 0
    altura(1) = 1 + max(1, 0) = 2

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción estructural.
    Caso base: altura(None) = −1. Un árbol vacío no tiene nodos, así
    que su "número de aristas en el camino más largo" es −1 por
    convención (camino vacío).
    Hipótesis: altura() correcta para subárboles menores.
    Paso: el camino más largo desde n pasa por el subárbol más alto,
    más la arista que conecta n con ese subárbol. De ahí
    1 + max(...). ∎

COMPLEJIDAD
    Tiempo: Θ(n). Visita todos los nodos.
    Espacio: Θ(h) de pila — irónicamente, la profundidad de la
    recursión es la altura del árbol.

    Se puede calcular en O(1) de espacio con un recorrido iterativo
    por niveles (BFS contando niveles), a cambio de O(w) para la cola.

RELACIÓN CON OTROS TEMAS
    - BST balanceado: altura O(log n) → operaciones O(log n).
    - BST degenerado: altura O(n) → operaciones O(n).
    - AVL (ejercicio 16): garantiza altura ≤ 1.44·log₂(n).
    - La recursión de esta función es T(n) = T(n/2) + T(n/2) + O(1)
      en árbol balanceado → Θ(n).
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def altura(nodo):
    """Altura en aristas. Árbol vacío = −1, un solo nodo = 0."""
    if nodo is None:
        return -1
    return 1 + max(altura(nodo.izquierdo), altura(nodo.derecho))


def altura_por_niveles(raiz):
    """Altura por BFS: O(1) de espacio de recursión, O(w) de cola.

    Alternativa cuando el árbol es muy alto y se quiere evitar la
    recursión profunda.
    """
    from collections import deque

    if not raiz:
        return -1

    cola = deque([(raiz, 0)])
    maxima = 0
    while cola:
        nodo, nivel = cola.popleft()
        maxima = max(maxima, nivel)
        if nodo.izquierdo:
            cola.append((nodo.izquierdo, nivel + 1))
        if nodo.derecho:
            cola.append((nodo.derecho, nivel + 1))
    return maxima


def profundidad(raiz, valor, nivel=0):
    """Profundidad de un valor concreto: aristas desde la raíz."""
    if raiz is None:
        return -1
    if raiz.valor == valor:
        return nivel
    izq = profundidad(raiz.izquierdo, valor, nivel + 1)
    if izq != -1:
        return izq
    return profundidad(raiz.derecho, valor, nivel + 1)


if __name__ == "__main__":
    # Árbol de referencia
    raiz = Nodo(1)
    raiz.izquierdo = Nodo(2)
    raiz.derecho = Nodo(3)
    raiz.izquierdo.izquierdo = Nodo(4)
    raiz.izquierdo.derecho = Nodo(5)
    raiz.derecho.derecho = Nodo(6)

    print(f"Altura (aristas):  {altura(raiz)}")
    print(f"Altura (niveles):  {altura_por_niveles(raiz)}")
    print(f"Profundidad de 4:  {profundidad(raiz, 4)}")
    print(f"Profundidad de 6:  {profundidad(raiz, 6)}")

    assert altura(raiz) == 2
    assert altura_por_niveles(raiz) == 2, "ambas versiones deben coincidir"

    # Casos base
    assert altura(None) == -1, "árbol vacío"
    solo = Nodo(7)
    assert altura(solo) == 0, "un solo nodo"
    assert altura_por_niveles(solo) == 0

    # Profundidad
    assert profundidad(raiz, 1) == 0, "la raíz está a profundidad 0"
    assert profundidad(raiz, 4) == 2
    assert profundidad(raiz, 6) == 2
    assert profundidad(raiz, 99) == -1, "valor ausente"

    # Cota inferior: ⌊log₂ n⌋ para árbol perfecto
    import math
    pleno = Nodo(1)
    pleno.izquierdo = Nodo(2)
    pleno.derecho = Nodo(3)
    pleno.izquierdo.izquierdo = Nodo(4)
    pleno.izquierdo.derecho = Nodo(5)
    pleno.derecho.izquierdo = Nodo(6)
    pleno.derecho.derecho = Nodo(7)
    n = 7
    print(f"\nÁrbol perfecto de {n} nodos: altura {altura(pleno)}")
    print(f"Cota inferior ⌊log₂ n⌋ = {math.floor(math.log2(n))}")
    assert altura(pleno) == math.floor(math.log2(n)), "perfecto alcanza la cota"

    # Cota superior: n − 1 para árbol degenerado
    deg = Nodo(1)
    actual = deg
    for v in [2, 3, 4, 5]:
        actual.derecho = Nodo(v)
        actual = actual.derecho
    n_deg = 5
    print(f"Árbol degenerado de {n_deg} nodos: altura {altura(deg)}")
    assert altura(deg) == n_deg - 1, "degenerado alcanza la cota superior"

    # Relación entre nodos y altura: n ≤ 2^(h+1) − 1
    def contar(n):
        if n is None:
            return 0
        return 1 + contar(n.izquierdo) + contar(n.derecho)
    for arbol in [raiz, pleno, deg]:
        n_arbol = contar(arbol)
        h = altura(arbol)
        assert n_arbol <= 2 ** (h + 1) - 1, f"violó la cota: n={n_arbol}, h={h}"
        print(f"  n={n_arbol}, h={h}: n ≤ 2^(h+1)−1 = {2**(h+1)-1} ✓")

    print("\n✓ Todas las pruebas pasaron")
