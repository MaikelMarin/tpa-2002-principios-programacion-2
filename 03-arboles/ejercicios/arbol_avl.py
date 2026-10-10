"""
Ejercicio 16: Árbol AVL
Dificultad: Experto

Un árbol AVL es un BST balanceado donde la diferencia de altura entre
subárboles es como máximo 1. Usa rotaciones para mantener el balance.

Historia: Adelson-Velsky y Landi lo inventaron en 1962.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 1


class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        # Inserción BST normal
        if nodo is None:
            return Nodo(valor)
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar(nodo.derecho, valor)
        else:
            return nodo
        # Actualizar altura
        nodo.altura = 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))
        # Obtener factor de balance
        balance = self._balance(nodo)
        # Rotaciones
        # Caso LL
        if balance > 1 and valor < nodo.izquierdo.valor:
            return self._rotacion_derecha(nodo)
        # Caso RR
        if balance < -1 and valor > nodo.derecho.valor:
            return self._rotacion_izquierda(nodo)
        # Caso LR
        if balance > 1 and valor > nodo.izquierdo.valor:
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            return self._rotacion_derecha(nodo)
        # Caso RL
        if balance < -1 and valor < nodo.derecho.valor:
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            return self._rotacion_izquierda(nodo)
        return nodo

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _balance(self, nodo):
        if not nodo:
            return 0
        return self._altura(nodo.izquierdo) - self._altura(nodo.derecho)

    def _rotacion_derecha(self, y):
        x = y.izquierdo
        t2 = x.derecho
        x.derecho = y
        y.izquierdo = t2
        y.altura = 1 + max(self._altura(y.izquierdo), self._altura(y.derecho))
        x.altura = 1 + max(self._altura(x.izquierdo), self._altura(x.derecho))
        return x

    def _rotacion_izquierda(self, x):
        y = x.derecho
        t2 = y.izquierdo
        y.izquierdo = x
        x.derecho = t2
        x.altura = 1 + max(self._altura(x.izquierdo), self._altura(x.derecho))
        y.altura = 1 + max(self._altura(y.izquierdo), self._altura(y.derecho))
        return y


def inorden(nodo):
    if nodo:
        inorden(nodo.izquierdo)
        print(nodo.valor, end=" ")
        inorden(nodo.derecho)


if __name__ == "__main__":
    avl = ArbolAVL()
    for val in [10, 20, 30, 40, 50, 25]:
        avl.insertar(val)

    print("Árbol AVL (inorden):")
    inorden(avl.raiz)
    print()
    print(f"Altura del árbol: {avl.raiz.altura}")
    assert avl.raiz.valor == 20
    print("\n✓ Todas las pruebas pasaron")
