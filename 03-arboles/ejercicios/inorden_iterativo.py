r"""
Ejercicio 10: Inorden iterativo (con pila)
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Recorrido inorden recursivo (ejercicio recorridos.py).
    - Pila (00-fundamentos §8.4): aquí se usa una explícita.
    - Límite de recursión de Python (§10.2): la razón de esta versión.

PROBLEMA
    Recorrer un BST en inorden SIN recursión, usando una pila.

¿POR QUÉ EXISTE ESTA VERSIÓN?
    La recursión consume un marco de pila por nivel de profundidad.
    Python limita la profundidad a ~1000 por defecto.

    Un BST degenerado de 5,000 nodos tiene profundidad 5,000: la
    versión recursiva lanza RecursionError. La iterativa, no.

    Además, la iterativa permite PAUSAR y reanudar el recorrido (es
    la base del iterador del ejercicio 15), lo que con recursión pura
    no es posible.

ESTRATEGIA: SIMULAR LA PILA DE LLAMADAS
    En la recursión, el inorden hace tres cosas en orden:
        1. Bajar por la izquierda.
        2. Visitar el nodo.
        3. Ir a la derecha.

    Con una pila explícita, el patrón es:

        actual = raiz
        mientras haya trabajo:
            mientras actual no sea None:
                apilar actual          ← equivale a la llamada recursiva
                actual = actual.izquierdo
            actual = desapilar
            visitar(actual)            ← la "visita"
            actual = actual.derecho    ← ir a la rama derecha

    El bucle interno apila TODA la rama izquierda antes de visitar.
    Es exactamente lo que hace la recursión, solo que con una pila que
    controlamos nosotros.

TRAZA sobre:
        2
       / \
      1   3

    actual = 2
    Bucle externo, iteración 1:
      Bucle interno: apilar 2, actual = 1
                     apilar 1, actual = None → salir
      desapilar → actual = 1
      visitar 1
      actual = 1.derecho = None
    Bucle externo, iteración 2:
      Bucle interno: actual es None, no apila nada
      desapilar → actual = 2
      visitar 2
      actual = 2.derecho = 3
    Bucle externo, iteración 3:
      Bucle interno: apilar 3, actual = None → salir
      desapilar → actual = 3
      visitar 3
      actual = 3.derecho = None
    Pila vacía y actual es None → terminar

    Resultado: 1, 2, 3 (¡ordenado!)

DEMOSTRACIÓN DE CORRECCIÓN
    El invariante: en cada momento, la pila contiene exactamente los
    nodos cuyas ramas izquierdas ya se visitaron pero que aún no se
    han visitado ellos mismos, en orden de profundidad decreciente.

    - La visita ocurre siempre nada más desapilar, que es cuando ya se
      procesó toda la rama izquierda de ese nodo.
    - Al desapilar n, se visita n y luego se procesa su subárbol
      derecho, que contiene solo valores mayores que n.
    Luego la secuencia de visitas es creciente, que es la definición
    de inorden. ∎

COMPLEJIDAD
    Tiempo: Θ(n). Cada nodo se apila y desapila exactamente una vez.
    Espacio: O(h). La pila nunca tiene más de h+1 elementos
             (la rama izquierda más larga).

    Este O(h) es espacio de HEAP, no de pila de recursión: no hay
    límite de Python que lo restrinja.

RELACIÓN CON OTROS TEMAS
    - El mismo patrón "pila explícita que simula la recursión" se usa
      en el DFS iterativo de grafos (tema 04).
    - El iterador del ejercicio 15 usa esta función con un `yield`.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def inorden_iterativo(raiz):
    """Inorden iterativo con pila explícita: O(n) tiempo, O(h) espacio."""
    pila = []
    actual = raiz
    resultado = []

    while actual or pila:
        # Bajar por la izquierda apilando todo el camino
        while actual:
            pila.append(actual)
            actual = actual.izquierdo

        # Visitar el nodo más a la izquierda pendiente
        actual = pila.pop()
        resultado.append(actual.valor)

        # Pasar a la rama derecha
        actual = actual.derecho

    return resultado


def inorden_recursivo(nodo):
    """Versión recursiva, para verificar que ambas coinciden."""
    if nodo is None:
        return []
    return inorden_recursivo(nodo.izquierdo) + [nodo.valor] + inorden_recursivo(nodo.derecho)


if __name__ == "__main__":
    raiz = Nodo(1)
    raiz.izquierdo = Nodo(2)
    raiz.derecho = Nodo(3)
    raiz.izquierdo.izquierdo = Nodo(4)
    raiz.izquierdo.derecho = Nodo(5)
    raiz.derecho.derecho = Nodo(6)

    print(f"Inorden iterativo:  {inorden_iterativo(raiz)}")
    print(f"Inorden recursivo:  {inorden_recursivo(raiz)}")

    assert inorden_iterativo(raiz) == [4, 2, 5, 1, 3, 6]
    assert inorden_iterativo(raiz) == inorden_recursivo(raiz)

    # Casos base
    assert inorden_iterativo(None) == []
    solo = Nodo(7)
    assert inorden_iterativo(solo) == [7]

    # Correctitud sobre muchos árboles aleatorios
    import random
    random.seed(31)
    for _ in range(300):
        n = random.randint(0, 40)
        valores = random.sample(range(-100, 101), n)
        if valores:
            raiz_a = Nodo(valores[0])
            for v in valores[1:]:
                actual = raiz_a
                while True:
                    if v < actual.valor:
                        if actual.izquierdo is None:
                            actual.izquierdo = Nodo(v); break
                        actual = actual.izquierdo
                    else:
                        if actual.derecho is None:
                            actual.derecho = Nodo(v); break
                        actual = actual.derecho
        else:
            raiz_a = None
        assert inorden_iterativo(raiz_a) == sorted(valores)

    # LA RAZÓN DE SER: profundidad > límite de recursión de Python
    profundo = Nodo(0)
    actual = profundo
    for v in range(1, 3000):              # 3,000 niveles
        actual.derecho = Nodo(v)
        actual = actual.derecho

    print(f"\nÁrbol degenerado de 3,000 nodos:")
    print(f"  Inorden iterativo: {len(inorden_iterativo(profundo))} nodos ✓")

    # La versión recursiva FALLA con esta profundidad
    import sys
    try:
        inorden_recursivo(profundo)
        print("  Inorden recursivo: funcionó (límite alto en este sistema)")
    except RecursionError:
        print(f"  Inorden recursivo: RecursionError (límite Python = {sys.getrecursionlimit()})")

    # La iterativa entrega ordenado incluso aquí
    assert inorden_iterativo(profundo) == list(range(3000))

    # La pila nunca supera h+1 elementos
    def pila_maxima(raiz):
        pila = []
        actual = raiz
        max_pila = 0
        while actual or pila:
            while actual:
                pila.append(actual)
                actual = actual.izquierdo
            max_pila = max(max_pila, len(pila))
            actual = pila.pop()
            actual = actual.derecho
        return max_pila

    bal = Nodo(4)
    bal.izquierdo = Nodo(2); bal.derecho = Nodo(6)
    bal.izquierdo.izquierdo = Nodo(1); bal.izquierdo.derecho = Nodo(3)
    bal.derecho.izquierdo = Nodo(5); bal.derecho.derecho = Nodo(7)
    print(f"  Pila máxima en árbol de altura 2: {pila_maxima(bal)} (= h+1)")
    assert pila_maxima(bal) == 3

    print("\n✓ Todas las pruebas pasaron")
