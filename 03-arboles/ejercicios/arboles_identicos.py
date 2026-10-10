"""
Ejercicio 11: Árboles idénticos
Dificultad: Intermedio

Determina si dos árboles binarios son idénticos en estructura y valores.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


def son_identicos(a, b):
    """Verifica si dos árboles son idénticos."""
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return (a.valor == b.valor and
            son_identicos(a.izquierdo, b.izquierdo) and
            son_identicos(a.derecho, b.derecho))


def es_simetrico(nodo):
    """Verifica si un árbol es simétrico (espejo de sí mismo)."""
    def espejo(a, b):
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
        return (a.valor == b.valor and
                espejo(a.izquierdo, b.derecho) and
                espejo(a.derecho, b.izquierdo))
    return espejo(nodo, nodo)


if __name__ == "__main__":
    # Árboles idénticos
    a1 = Nodo(1)
    a1.izquierdo = Nodo(2)
    a1.derecho = Nodo(3)

    a2 = Nodo(1)
    a2.izquierdo = Nodo(2)
    a2.derecho = Nodo(3)

    # Árbol diferente
    a3 = Nodo(1)
    a3.izquierdo = Nodo(3)
    a3.derecho = Nodo(2)

    print(f"a1 y a2 idénticos: {son_identicos(a1, a2)}")
    print(f"a1 y a3 idénticos: {son_identicos(a1, a3)}")

    assert son_identicos(a1, a2) == True
    assert son_identicos(a1, a3) == False
    assert son_identicos(None, None) == True
    print("\n✓ Todas las pruebas pasaron")
