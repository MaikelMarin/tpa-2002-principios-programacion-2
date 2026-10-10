"""
Ejercicio 9: Mínimo y máximo en BST
Dificultad: Básico

El mínimo es el nodo más a la izquierda.
El máximo es el nodo más a la derecha.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


def encontrar_minimo(nodo):
    """Encuentra el valor mínimo en un BST."""
    while nodo.izquierdo:
        nodo = nodo.izquierdo
    return nodo.valor


def encontrar_maximo(nodo):
    """Encuentra el valor máximo en un BST."""
    while nodo.derecho:
        nodo = nodo.derecho
    return nodo.valor


def encontrar_minimo_recursivo(nodo):
    """Versión recursiva para encontrar el mínimo."""
    if nodo.izquierdo is None:
        return nodo.valor
    return encontrar_minimo_recursivo(nodo.izquierdo)


def encontrar_maximo_recursivo(nodo):
    """Versión recursiva para encontrar el máximo."""
    if nodo.derecho is None:
        return nodo.valor
    return encontrar_maximo_recursivo(nodo.derecho)


if __name__ == "__main__":
    raiz = Nodo(8)
    raiz.izquierdo = Nodo(3)
    raiz.derecho = Nodo(10)
    raiz.izquierdo.izquierdo = Nodo(1)
    raiz.izquierdo.derecho = Nodo(6)
    raiz.derecho.derecho = Nodo(14)

    print(f"Mínimo: {encontrar_minimo(raiz)}")
    print(f"Máximo: {encontrar_maximo(raiz)}")

    assert encontrar_minimo(raiz) == 1
    assert encontrar_maximo(raiz) == 14
    assert encontrar_minimo_recursivo(raiz) == 1
    assert encontrar_maximo_recursivo(raiz) == 14
    print("\n✓ Todas las pruebas pasaron")
