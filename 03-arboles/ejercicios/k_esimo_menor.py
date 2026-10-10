"""
Ejercicio 19: K-ésimo elemento menor en BST
Dificultad: Avanzado

Encuentra el k-ésimo elemento más pequeño en un BST.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.tamano_izquierdo = 0  # Tamaño del subárbol izquierdo


def k_esimo_menor(raiz, k):
    """Encuentra el k-ésimo elemento más pequeño en un BST."""
    actual = raiz
    while actual:
        tamano_izq = actual.tamano_izquierdo
        if k == tamano_izq + 1:
            return actual.valor
        elif k <= tamano_izq:
            actual = actual.izquierdo
        else:
            k -= tamano_izq + 1
            actual = actual.derecho
    return None


def k_esimo_menor_inorden(raiz, k):
    """Versión usando recorrido inorden."""
    pila = []
    actual = raiz
    contador = 0
    while actual or pila:
        while actual:
            pila.append(actual)
            actual = actual.izquierdo
        actual = pila.pop()
        contador += 1
        if contador == k:
            return actual.valor
        actual = actual.derecho
    return None


def calcular_tamano(nodo):
    """Calcula el tamaño de cada subárbol."""
    if nodo is None:
        return 0
    nodo.tamano_izquierdo = calcular_tamano(nodo.izquierdo)
    return 1 + nodo.tamano_izquierdo + calcular_tamano(nodo.derecho)


if __name__ == "__main__":
    raiz = Nodo(5)
    raiz.izquierdo = Nodo(3)
    raiz.derecho = Nodo(7)
    raiz.izquierdo.izquierdo = Nodo(2)
    raiz.izquierdo.derecho = Nodo(4)
    raiz.derecho.derecho = Nodo(8)

    calcular_tamano(raiz)

    print("K-ésimo menor en BST:")
    for k in range(1, 7):
        print(f"  {k}º menor: {k_esimo_menor(raiz, k)}")

    assert k_esimo_menor(raiz, 1) == 2
    assert k_esimo_menor(raiz, 3) == 4
    assert k_esimo_menor(raiz, 6) == 8
    assert k_esimo_menor_inorden(raiz, 3) == 4
    print("\n✓ Todas las pruebas pasaron")
