"""
Ejercicio 7: Eliminación en BST
Dificultad: Avanzado

Elimina un nodo de un BST manteniendo la propiedad BST.

Tres casos:
1. Nodo hoja: eliminar directamente
2. Nodo con un hijo: reemplazar con el hijo
3. Nodo con dos hijos: reemplazar con el sucesor inorden
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


def eliminar(raiz, valor):
    """Elimina un valor del BST."""
    if raiz is None:
        return raiz
    if valor < raiz.valor:
        raiz.izquierdo = eliminar(raiz.izquierdo, valor)
    elif valor > raiz.valor:
        raiz.derecho = eliminar(raiz.derecho, valor)
    else:
        # Caso 1: Nodo hoja o con un solo hijo
        if raiz.izquierdo is None:
            return raiz.derecho
        elif raiz.derecho is None:
            return raiz.izquierdo
        # Caso 2: Nodo con dos hijos
        sucesor = encontrar_minimo(raiz.derecho)
        raiz.valor = sucesor.valor
        raiz.derecho = eliminar(raiz.derecho, sucesor.valor)
    return raiz


def encontrar_minimo(nodo):
    """Encuentra el nodo con valor mínimo en un BST."""
    while nodo.izquierdo:
        nodo = nodo.izquierdo
    return nodo


def inorden(nodo):
    if nodo:
        inorden(nodo.izquierdo)
        print(nodo.valor, end=" ")
        inorden(nodo.derecho)


if __name__ == "__main__":
    raiz = None
    for val in [5, 3, 7, 1, 4, 6, 8]:
        raiz = insertar(raiz, val)

    print("BST original:")
    inorden(raiz)
    print()

    raiz = eliminar(raiz, 3)
    print("Después de eliminar 3:")
    inorden(raiz)
    print()

    raiz = eliminar(raiz, 5)
    print("Después de eliminar 5 (raíz):")
    inorden(raiz)
    print()

    assert buscar(raiz, 3) == False
    assert buscar(raiz, 5) == False
    assert buscar(raiz, 4) == True
    print("\n✓ Todas las pruebas pasaron")


def insertar(raiz, valor):
    if raiz is None:
        return Nodo(valor)
    if valor < raiz.valor:
        raiz.izquierdo = insertar(raiz.izquierdo, valor)
    elif valor > raiz.valor:
        raiz.derecho = insertar(raiz.derecho, valor)
    return raiz


def buscar(nodo, valor):
    if nodo is None:
        return False
    if nodo.valor == valor:
        return True
    if valor < nodo.valor:
        return buscar(nodo.izquierdo, valor)
    return buscar(nodo.derecho, valor)
