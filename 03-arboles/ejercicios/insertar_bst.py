"""
Ejercicio 6: Inserción en BST
Dificultad: Intermedio

Inserta un nodo en un Árbol Binario de Búsqueda manteniendo la propiedad BST.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


def insertar(raiz, valor):
    """Inserta un valor en el BST recursivamente."""
    if raiz is None:
        return Nodo(valor)
    if valor < raiz.valor:
        raiz.izquierdo = insertar(raiz.izquierdo, valor)
    elif valor > raiz.valor:
        raiz.derecho = insertar(raiz.derecho, valor)
    return raiz


def insertar_iterativo(raiz, valor):
    """Versión iterativa de inserción en BST."""
    nuevo = Nodo(valor)
    if raiz is None:
        return nuevo
    actual = raiz
    while True:
        if valor < actual.valor:
            if actual.izquierdo is None:
                actual.izquierdo = nuevo
                break
            actual = actual.izquierdo
        elif valor > actual.valor:
            if actual.derecho is None:
                actual.derecho = nuevo
                break
            actual = actual.derecho
        else:
            break  # Valor ya existe
    return raiz


if __name__ == "__main__":
    raiz = None
    for val in [5, 3, 7, 1, 4, 6, 8]:
        raiz = insertar(raiz, val)

    print("BST construido con inserción recursiva")
    assert buscar(raiz, 5) == True
    assert buscar(raiz, 8) == True
    assert buscar(raiz, 10) == False

    raiz2 = None
    for val in [5, 3, 7, 1, 4, 6, 8]:
        raiz2 = insertar_iterativo(raiz2, val)

    print("BST construido con inserción iterativa")
    assert buscar(raiz2, 5) == True
    assert buscar(raiz2, 8) == True
    print("\n✓ Todas las pruebas pasaron")


def buscar(nodo, valor):
    if nodo is None:
        return False
    if nodo.valor == valor:
        return True
    if valor < nodo.valor:
        return buscar(nodo.izquierdo, valor)
    return buscar(nodo.derecho, valor)
