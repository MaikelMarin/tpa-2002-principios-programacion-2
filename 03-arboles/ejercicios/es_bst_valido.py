"""
Ejercicio 8: Verificar si un árbol es BST válido
Dificultad: Intermedio

Un BST es válido si para cada nodo:
- Todos los valores del subárbol izquierdo son menores
- Todos los valores del subárbol derecho son mayores
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


def es_bst_valido(nodo, minimo=float('-inf'), maximo=float('inf')):
    """Verifica si un árbol es un BST válido usando límites."""
    if nodo is None:
        return True
    if nodo.valor <= minimo or nodo.valor >= maximo:
        return False
    return (es_bst_valido(nodo.izquierdo, minimo, nodo.valor) and
            es_bst_valido(nodo.derecho, nodo.valor, maximo))


def es_bst_valido_inorden(nodo):
    """Verificación usando recorrido inorden."""
    valores = []
    inorden(nodo, valores)
    return all(valores[i] < valores[i + 1] for i in range(len(valores) - 1))


def inorden(nodo, valores):
    if nodo:
        inorden(nodo.izquierdo, valores)
        valores.append(nodo.valor)
        inorden(nodo.derecho, valores)


if __name__ == "__main__":
    # BST válido
    raiz1 = Nodo(5)
    raiz1.izquierdo = Nodo(3)
    raiz1.derecho = Nodo(7)
    raiz1.izquierdo.izquierdo = Nodo(1)
    raiz1.izquierdo.derecho = Nodo(4)

    # BST inválido
    raiz2 = Nodo(5)
    raiz2.izquierdo = Nodo(3)
    raiz2.derecho = Nodo(7)
    raiz2.izquierdo.derecho = Nodo(6)  # 6 > 5, inválido

    print(f"Árbol 1 es BST válido: {es_bst_valido(raiz1)}")
    print(f"Árbol 2 es BST válido: {es_bst_valido(raiz2)}")

    assert es_bst_valido(raiz1) == True
    assert es_bst_valido(raiz2) == False
    assert es_bst_valido_inorden(raiz1) == True
    assert es_bst_valido_inorden(raiz2) == False
    print("\n✓ Todas las pruebas pasaron")
