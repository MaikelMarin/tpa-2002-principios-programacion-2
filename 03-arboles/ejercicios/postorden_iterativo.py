"""
Ejercicio 13: Postorden iterativo
Dificultad: Avanzado

Recorrido postorden sin recursión, usando dos pilas.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


def postorden_iterativo(raiz):
    """Recorrido postorden iterativo usando dos pilas."""
    if not raiz:
        return []
    pila1, pila2 = [raiz], []
    while pila1:
        nodo = pila1.pop()
        pila2.append(nodo)
        if nodo.izquierdo:
            pila1.append(nodo.izquierdo)
        if nodo.derecho:
            pila1.append(nodo.derecho)
    return [n.valor for n in reversed(pila2)]


if __name__ == "__main__":
    raiz = Nodo(1)
    raiz.izquierdo = Nodo(2)
    raiz.derecho = Nodo(3)
    raiz.izquierdo.izquierdo = Nodo(4)
    raiz.izquierdo.derecho = Nodo(5)
    raiz.derecho.derecho = Nodo(6)

    print("Postorden iterativo:", postorden_iterativo(raiz))
    assert postorden_iterativo(raiz) == [4, 5, 2, 6, 3, 1]
    print("\n✓ Todas las pruebas pasaron")
