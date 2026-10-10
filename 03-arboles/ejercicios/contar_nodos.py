"""
Ejercicio 3: Contar nodos recursivamente
Dificultad: Básico

Cuenta el número total de nodos en un árbol binario.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


def contar_nodos(nodo):
    """Cuenta recursivamente todos los nodos del árbol."""
    if nodo is None:
        return 0
    return 1 + contar_nodos(nodo.izquierdo) + contar_nodos(nodo.derecho)


def contar_hojas(nodo):
    """Cuenta solo las hojas (nodos sin hijos)."""
    if nodo is None:
        return 0
    if nodo.izquierdo is None and nodo.derecho is None:
        return 1
    return contar_hojas(nodo.izquierdo) + contar_hojas(nodo.derecho)


if __name__ == "__main__":
    # Crear árbol de ejemplo
    raiz = Nodo(1)
    raiz.izquierdo = Nodo(2)
    raiz.derecho = Nodo(3)
    raiz.izquierdo.izquierdo = Nodo(4)
    raiz.izquierdo.derecho = Nodo(5)
    raiz.derecho.derecho = Nodo(6)

    print(f"Total de nodos: {contar_nodos(raiz)}")
    print(f"Total de hojas: {contar_hojas(raiz)}")

    assert contar_nodos(raiz) == 6
    assert contar_hojas(raiz) == 3
    assert contar_nodos(None) == 0
    print("\n✓ Todas las pruebas pasaron")
