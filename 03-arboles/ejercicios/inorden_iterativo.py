"""
Ejercicio 10: Inorden iterativo (con pila)
Dificultad: Intermedio

Recorrido inorden sin recursión, usando una pila explícita.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


def inorden_iterativo(raiz):
    """Recorrido inorden iterativo usando una pila."""
    pila = []
    actual = raiz
    resultado = []
    while actual or pila:
        while actual:
            pila.append(actual)
            actual = actual.izquierdo
        actual = pila.pop()
        resultado.append(actual.valor)
        actual = actual.derecho
    return resultado


if __name__ == "__main__":
    raiz = Nodo(1)
    raiz.izquierdo = Nodo(2)
    raiz.derecho = Nodo(3)
    raiz.izquierdo.izquierdo = Nodo(4)
    raiz.izquierdo.derecho = Nodo(5)
    raiz.derecho.derecho = Nodo(6)

    print("Inorden iterativo:", inorden_iterativo(raiz))
    assert inorden_iterativo(raiz) == [4, 2, 5, 1, 3, 6]
    print("\n✓ Todas las pruebas pasaron")
