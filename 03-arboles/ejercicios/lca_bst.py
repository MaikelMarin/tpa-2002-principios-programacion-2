"""
Ejercicio 14: Ancestro común más bajo (LCA) en BST
Dificultad: Avanzado

El LCA de dos nodos es el nodo más bajo que tiene a ambos como descendientes.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


def lca_bst(raiz, p, q):
    """Encuentra el LCA de dos valores en un BST."""
    actual = raiz
    while actual:
        if p < actual.valor and q < actual.valor:
            actual = actual.izquierdo
        elif p > actual.valor and q > actual.valor:
            actual = actual.derecho
        else:
            return actual.valor
    return None


if __name__ == "__main__":
    raiz = Nodo(6)
    raiz.izquierdo = Nodo(2)
    raiz.derecho = Nodo(8)
    raiz.izquierdo.izquierdo = Nodo(0)
    raiz.izquierdo.derecho = Nodo(4)
    raiz.derecho.izquierdo = Nodo(7)
    raiz.derecho.derecho = Nodo(9)

    print(f"LCA(2, 8) = {lca_bst(raiz, 2, 8)}")
    print(f"LCA(2, 4) = {lca_bst(raiz, 2, 4)}")

    assert lca_bst(raiz, 2, 8) == 6
    assert lca_bst(raiz, 2, 4) == 2
    print("\n✓ Todas las pruebas pasaron")
