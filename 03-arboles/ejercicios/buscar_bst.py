"""
Ejercicio 5: Búsqueda en BST
Dificultad: Intermedio

Búsqueda en un Árbol Binario de Búsqueda (BST).
Complejidad: O(h) donde h es la altura.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


def buscar(nodo, valor):
    """Busca un valor en un BST recursivamente."""
    if nodo is None:
        return False
    if nodo.valor == valor:
        return True
    if valor < nodo.valor:
        return buscar(nodo.izquierdo, valor)
    return buscar(nodo.derecho, valor)


def buscar_iterativo(nodo, valor):
    """Versión iterativa de búsqueda en BST."""
    actual = nodo
    while actual:
        if actual.valor == valor:
            return True
        elif valor < actual.valor:
            actual = actual.izquierdo
        else:
            actual = actual.derecho
    return False


if __name__ == "__main__":
    # Crear BST
    raiz = Nodo(8)
    raiz.izquierdo = Nodo(3)
    raiz.derecho = Nodo(10)
    raiz.izquierdo.izquierdo = Nodo(1)
    raiz.izquierdo.derecho = Nodo(6)
    raiz.derecho.derecho = Nodo(14)

    print("Búsquedas en BST:")
    print(f"  Buscar 6: {buscar(raiz, 6)}")
    print(f"  Buscar 14: {buscar(raiz, 14)}")
    print(f"  Buscar 5: {buscar(raiz, 5)}")

    assert buscar(raiz, 6) == True
    assert buscar(raiz, 14) == True
    assert buscar(raiz, 5) == False
    assert buscar_iterativo(raiz, 6) == True
    assert buscar_iterativo(raiz, 5) == False
    print("\n✓ Todas las pruebas pasaron")
