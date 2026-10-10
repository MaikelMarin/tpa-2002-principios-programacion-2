"""
Ejercicio 12: Árbol balanceado
Dificultad: Avanzado

Un árbol es balanceado si la altura de los subárboles izquierdo y derecho
de cada nodo difiere en máximo 1.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


def es_balanceado(nodo):
    """Verifica si un árbol está balanceado. Retorna (balanceado, altura)."""
    if nodo is None:
        return True, -1
    izquierda_bal, altura_izq = es_balanceado(nodo.izquierdo)
    if not izquierda_bal:
        return False, 0
    derecha_bal, altura_der = es_balanceado(nodo.derecho)
    if not derecha_bal:
        return False, 0
    if abs(altura_izq - altura_der) > 1:
        return False, 0
    return True, 1 + max(altura_izq, altura_der)


if __name__ == "__main__":
    # Árbol balanceado
    raiz1 = Nodo(1)
    raiz1.izquierdo = Nodo(2)
    raiz1.derecho = Nodo(3)
    raiz1.izquierdo.izquierdo = Nodo(4)
    raiz1.izquierdo.derecho = Nodo(5)

    # Árbol no balanceado
    raiz2 = Nodo(1)
    raiz2.izquierdo = Nodo(2)
    raiz2.izquierdo.izquierdo = Nodo(3)
    raiz2.izquierdo.izquierdo.izquierdo = Nodo(4)

    print(f"Árbol 1 balanceado: {es_balanceado(raiz1)[0]}")
    print(f"Árbol 2 balanceado: {es_balanceado(raiz2)[0]}")

    assert es_balanceado(raiz1)[0] == True
    assert es_balanceado(raiz2)[0] == False
    print("\n✓ Todas las pruebas pasaron")
