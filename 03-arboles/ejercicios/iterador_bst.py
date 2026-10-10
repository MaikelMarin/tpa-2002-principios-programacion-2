"""
Ejercicio 15: Iterador para BST
Dificultad: Experto

Implementa un iterador que recorre un BST en inorden.
Debe soportar next() y hasNext() con complejidad O(1) amortizado.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


class IteradorBST:
    def __init__(self, raiz):
        self.pila = []
        self._apilar_izquierdos(raiz)

    def _apilar_izquierdos(self, nodo):
        while nodo:
            self.pila.append(nodo)
            nodo = nodo.izquierdo

    def next(self):
        """Retorna el siguiente elemento en inorden."""
        nodo = self.pila.pop()
        self._apilar_izquierdos(nodo.derecho)
        return nodo.valor

    def hasNext(self):
        """Verifica si hay más elementos."""
        return len(self.pila) > 0


if __name__ == "__main__":
    raiz = Nodo(7)
    raiz.izquierdo = Nodo(3)
    raiz.derecho = Nodo(15)
    raiz.izquierdo.izquierdo = Nodo(1)
    raiz.izquierdo.derecho = Nodo(5)
    raiz.derecho.izquierdo = Nodo(10)
    raiz.derecho.derecho = Nodo(20)

    iterador = IteradorBST(raiz)
    resultado = []
    while iterador.hasNext():
        resultado.append(iterador.next())

    print("Recorrido con iterador:", resultado)
    assert resultado == [1, 3, 5, 7, 10, 15, 20]
    print("\n✓ Todas las pruebas pasaron")
