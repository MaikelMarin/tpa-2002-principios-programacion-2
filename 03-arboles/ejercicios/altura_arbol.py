"""
Ejercicio 4: Altura de un árbol
Dificultad: Básico

La altura es el número máximo de aristas desde la raíz hasta una hoja.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


def altura(nodo):
    """Calcula la altura del árbol recursivamente."""
    if nodo is None:
        return -1
    return 1 + max(altura(nodo.izquierdo), altura(nodo.derecho))


def profundidad(nodo, valor, nivel=0):
    """Calcula la profundidad de un valor específico."""
    if nodo is None:
        return -1
    if nodo.valor == valor:
        return nivel
    izquierda = profundidad(nodo.izquierdo, valor, nivel + 1)
    if izquierda != -1:
        return izquierda
    return profundidad(nodo.derecho, valor, nivel + 1)


if __name__ == "__main__":
    # Crear árbol de ejemplo
    raiz = Nodo(1)
    raiz.izquierdo = Nodo(2)
    raiz.derecho = Nodo(3)
    raiz.izquierdo.izquierdo = Nodo(4)
    raiz.izquierdo.derecho = Nodo(5)
    raiz.derecho.derecho = Nodo(6)

    print(f"Altura del árbol: {altura(raiz)}")
    print(f"Profundidad de 4: {profundidad(raiz, 4)}")
    print(f"Profundidad de 6: {profundidad(raiz, 6)}")

    assert altura(raiz) == 2
    assert profundidad(raiz, 1) == 0
    assert profundidad(raiz, 4) == 2
    assert altura(None) == -1
    print("\n✓ Todas las pruebas pasaron")
