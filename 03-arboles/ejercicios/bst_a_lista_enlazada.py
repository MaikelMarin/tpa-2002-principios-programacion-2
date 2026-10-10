"""
Ejercicio 17: BST a lista enlazada
Dificultad: Experto

Convierte un BST en una lista enlazada ordenada (in-place).
"""

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


class NodoLista:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


def bst_a_lista_enlazada(raiz):
    """Convierte un BST en una lista enlazada ordenada."""
    cabeza = [None]
    anterior = [None]

    def inorden(nodo):
        if not nodo:
            return
        inorden(nodo.izquierdo)
        nuevo = NodoLista(nodo.valor)
        if anterior[0]:
            anterior[0].siguiente = nuevo
        else:
            cabeza[0] = nuevo
        anterior[0] = nuevo
        inorden(nodo.derecho)

    inorden(raiz)
    return cabeza[0]


def imprimir_lista(cabeza):
    actual = cabeza
    while actual:
        print(actual.valor, end=" → " if actual.siguiente else "\n")
        actual = actual.siguiente


if __name__ == "__main__":
    raiz = Nodo(4)
    raiz.izquierdo = Nodo(2)
    raiz.derecho = Nodo(5)
    raiz.izquierdo.izquierdo = Nodo(1)
    raiz.izquierdo.derecho = Nodo(3)

    cabeza = bst_a_lista_enlazada(raiz)
    print("Lista enlazada desde BST:")
    imprimir_lista(cabeza)
    assert cabeza.valor == 1
    assert cabeza.siguiente.valor == 2
    assert cabeza.siguiente.siguiente.valor == 3
    print("\n✓ Todas las pruebas pasaron")
