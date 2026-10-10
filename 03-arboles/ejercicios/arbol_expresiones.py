"""
Ejercicio 18: Árbol de expresiones
Dificultad: Experto

Implementa un árbol de expresiones aritméticas y evalúalo.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


def evaluar(nodo):
    """Evalúa un árbol de expresiones aritméticas."""
    if nodo is None:
        return 0
    # Si es un nodo hoja (operando)
    if isinstance(nodo.valor, (int, float)):
        return nodo.valor
    # Si es un operador
    izquierda = evaluar(nodo.izquierdo)
    derecha = evaluar(nodo.derecho)
    if nodo.valor == '+':
        return izquierda + derecha
    elif nodo.valor == '-':
        return izquierda - derecha
    elif nodo.valor == '*':
        return izquierda * derecha
    elif nodo.valor == '/':
        return izquierda / derecha
    return 0


def postfija(nodo):
    """Recorrido postfija del árbol de expresiones."""
    if nodo:
        postfija(nodo.izquierdo)
        postfija(nodo.derecho)
        print(nodo.valor, end=" ")


if __name__ == "__main__":
    # Expresión: (3 + 5) * 2
    raiz = Nodo('*')
    raiz.izquierdo = Nodo('+')
    raiz.derecho = Nodo(2)
    raiz.izquierdo.izquierdo = Nodo(3)
    raiz.izquierdo.derecho = Nodo(5)

    print("Expresión postfija:")
    postfija(raiz)
    print()
    print(f"Resultado: {evaluar(raiz)}")
    assert evaluar(raiz) == 16
    print("\n✓ Todas las pruebas pasaron")
