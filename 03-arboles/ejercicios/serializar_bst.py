"""
Ejercicio 20: Serializar y deserializar BST
Dificultad: Experto

Convierte un BST a una cadena y viceversa.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


def serializar(raiz):
    """Serializa un BST a una cadena usando preorden."""
    def preorden(nodo):
        if not nodo:
            return
        valores.append(str(nodo.valor))
        preorden(nodo.izquierdo)
        preorden(nodo.derecho)

    valores = []
    preorden(raiz)
    return ",".join(valores)


def deserializar(datos):
    """Deserializa una cadena a un BST."""
    if not dados:
        return None
    valores = list(map(int, datos.split(",")))

    def construir(preorden):
        if not preorden:
            return None
        valor = preorden[0]
        nodo = Nodo(valor)
        i = 1
        while i < len(preorden) and preorden[i] < valor:
            i += 1
        nodo.izquierdo = construir(preorden[1:i])
        nodo.derecho = construir(preorden[i:])
        return nodo

    return construir(valores)


def inorden(nodo):
    if nodo:
        inorden(nodo.izquierdo)
        print(nodo.valor, end=" ")
        inorden(nodo.derecho)


if __name__ == "__main__":
    raiz = Nodo(5)
    raiz.izquierdo = Nodo(3)
    raiz.derecho = Nodo(7)
    raiz.izquierdo.izquierdo = Nodo(2)
    raiz.izquierdo.derecho = Nodo(4)

    serializado = serializar(raiz)
    print(f"Serializado: {serializado}")

    restaurado = deserializar(serializado)
    print("Restaurado (inorden):")
    inorden(restaurado)
    print()

    assert restaurado.valor == 5
    assert restaurado.izquierdo.valor == 3
    assert restaurado.derecho.valor == 7
    assert serializar(restaurado) == serializado
    print("\n✓ Todas las pruebas pasaron")
