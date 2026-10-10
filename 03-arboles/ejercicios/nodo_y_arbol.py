"""
Ejercicio 1: Nodo y Árbol Binario
Dificultad: Básico

Implementación básica de un árbol binario con inserción recursiva.
"""

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


class ArbolBinario:
    def __init__(self, raiz=None):
        self.raiz = raiz

    def insertar(self, valor):
        """Inserta un valor en el árbol."""
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        if valor < nodo.valor:
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.izquierdo, valor)
        else:
            if nodo.derecho is None:
                nodo.derecho = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.derecho, valor)

    def buscar(self, valor):
        """Busca un valor en el árbol."""
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return False
        if nodo.valor == valor:
            return True
        if valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierdo, valor)
        return self._buscar_recursivo(nodo.derecho, valor)

    def __repr__(self):
        return f"ArbolBinario(raiz={self.raiz})"


if __name__ == "__main__":
    arbol = ArbolBinario()
    for val in [5, 3, 7, 1, 4, 6, 8]:
        arbol.insertar(val)

    print(f"Árbol: {arbol}")
    print(f"Buscar 4: {arbol.buscar(4)}")
    print(f"Buscar 10: {arbol.buscar(10)}")

    assert arbol.buscar(5) == True
    assert arbol.buscar(1) == True
    assert arbol.buscar(8) == True
    assert arbol.buscar(10) == False
    print("\n✓ Todas las pruebas pasaron")
