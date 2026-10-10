r"""
Ejercicio 13: Postorden iterativo
Dificultad: Avanzado

CONOCIMIENTO PREVIO NECESARIO
    - Inorden iterativo con pila (ejercicio inorden_iterativo.py).
    - Postorden recursivo (ejercicio recorridos.py).
    - Por qué existe la versión iterativa (§10.2 de fundamentos).

PROBLEMA
    Recorrer un árbol en postorden SIN recursión, usando pilas.

¿POR QUÉ ES MÁS DIFÍCIL QUE EL INORDEN?
    En el inorden, al desapilar un nodo ya se visitó toda su rama
    izquierda, y la derecha aún no: el flujo es simple.

    En el postorden, hay que visitar AMBOS hijos antes del padre.
    Con una sola pila eso requiere registrar por dónde se viene
    (¿vengo del hijo izquierdo o del derecho?). Con dos pilas se
    evita ese registro.

ESTRATEGIA CON DOS PILAS
    La idea: invertir el resultado.

        1. Apilar la raíz en pila1.
        2. Mientras pila1 no esté vacía:
             nodo = pila1.pop()
             pila2.push(nodo)          ← se guarda INVERTIDO
             si nodo.izq: pila1.push(nodo.izq)
             si nodo.der: pila1.push(nodo.der)
        3. El postorden es pila2 invertida.

    ¿Por qué funciona? Al apilar los hijos en pila1 y luego sacarlos,
    se procesan en orden inverso. Es el mismo truco que usar una pila
    para invertir una secuencia.

TRAZA sobre:
        1
       / \
      2   3

    pila1 = [1], pila2 = []

    Iteración 1: pop 1 → push en pila2
                 pila2 = [1]
                 hijos de 1: push 2, push 3 en pila1
                 pila1 = [2, 3]

    Iteración 2: pop 3 → push en pila2
                 pila2 = [1, 3]
                 3 no tiene hijos

    Iteración 3: pop 2 → push en pila2
                 pila2 = [1, 3, 2]
                 2 no tiene hijos

    pila2 invertida = [2, 3, 1]  ← ¡postorden correcto!

DEMOSTRACIÓN DE CORRECCIÓN
    Invariante: al finalizar, pila2 contiene los nodos en orden
    inverso al postorden.

    - Observación clave: un nodo se apila en pila2 ANTES de que se
      apilen sus hijos (porque al sacarlo de pila1, se apilan sus
      hijos para procesarlos después). Por tanto, en pila2 el padre
      queda DEBAJO de sus hijos.
    - Al invertir pila2, los hijos quedan antes que el padre, y el
      orden entre hermanos es izquierdo antes que derecho porque se
      apiló primero el izquierdo y la pila lo saca último.
    Luego el resultado es exactamente el postorden. ∎

COMPLEJIDAD
    Tiempo: Θ(n). Cada nodo se apila y desapila un número constante
    de veces (2 en total).
    Espacio: O(n) para las dos pilas en el peor caso. O(h) en la
    recursión, pero aquí usamos O(n) de heap, que no tiene el límite
    de Python.

VERSIÓN CON UNA SOLA PILA
    Existe, pero requiere registrar el estado (qué hijo se visitó).
    Es más eficiente en memoria (O(h)) pero más difícil de entender.
    Para este curso se usa la versión de dos pilas por claridad.

RELACIÓN CON OTROS TEMAS
    - El patrón "pila que simula la recursión" es el mismo del DFS
      iterativo en grafos (tema 04).
    - El postorden se usa para liberar memoria de un árbol: borrar
      los hijos antes que el padre.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def postorden_iterativo(raiz):
    """Postorden iterativo con dos pilas: Θ(n) tiempo, O(n) espacio."""
    if not raiz:
        return []

    pila1, pila2 = [raiz], []

    while pila1:
        nodo = pila1.pop()
        pila2.append(nodo)

        # Apilar hijos: el izquierdo primero para que salga último
        if nodo.izquierdo:
            pila1.append(nodo.izquierdo)
        if nodo.derecho:
            pila1.append(nodo.derecho)

    # pila2 invertida da el postorden
    return [n.valor for n in reversed(pila2)]


def postorden_recursivo(nodo):
    """Versión recursiva, para verificar que coinciden."""
    if nodo is None:
        return []
    return postorden_recursivo(nodo.izquierdo) + \
           postorden_recursivo(nodo.derecho) + [nodo.valor]


if __name__ == "__main__":
    raiz = Nodo(1)
    raiz.izquierdo = Nodo(2)
    raiz.derecho = Nodo(3)
    raiz.izquierdo.izquierdo = Nodo(4)
    raiz.izquierdo.derecho = Nodo(5)
    raiz.derecho.derecho = Nodo(6)

    it = postorden_iterativo(raiz)
    rec = postorden_recursivo(raiz)
    print(f"Postorden iterativo: {it}")
    print(f"Postorden recursivo: {rec}")

    assert it == [4, 5, 2, 6, 3, 1]
    assert it == rec

    # Casos base
    assert postorden_iterativo(None) == []
    solo = Nodo(7)
    assert postorden_iterativo(solo) == [7]

    # Correctitud sobre muchos árboles aleatorios
    import random
    random.seed(41)
    for _ in range(300):
        n = random.randint(0, 40)
        if n == 0:
            arbol = None
        else:
            valores = random.sample(range(-100, 101), n)
            arbol = Nodo(valores[0])
            for v in valores[1:]:
                actual = arbol
                while True:
                    if v < actual.valor:
                        if actual.izquierdo is None:
                            actual.izquierdo = Nodo(v); break
                        actual = actual.izquierdo
                    else:
                        if actual.derecho is None:
                            actual.derecho = Nodo(v); break
                        actual = actual.derecho
        assert postorden_iterativo(arbol) == postorden_recursivo(arbol)

    # La razón de ser: profundidad > límite de Python
    profundo = Nodo(0)
    actual = profundo
    for v in range(1, 3000):
        actual.derecho = Nodo(v)
        actual = actual.derecho

    res = postorden_iterativo(profundo)
    print(f"\nÁrbol degenerado de 3,000 nodos: {len(res)} nodos recorridos")
    assert res == list(range(2999, -1, -1))

    try:
        postorden_recursivo(profundo)
        print("Recursivo: funcionó (límite alto)")
    except RecursionError:
        print("Recursivo: RecursionError (límite de Python)")

    # Propiedad del postorden: el padre siempre va después de sus hijos
    def verificar_postorden(raiz, secuencia):
        pos = {v: i for i, v in enumerate(secuencia)}
        def check(n):
            if n is None:
                return True
            if n.izquierdo and pos[n.izquierdo.valor] > pos[n.valor]:
                return False
            if n.derecho and pos[n.derecho.valor] > pos[n.valor]:
                return False
            return check(n.izquierdo) and check(n.derecho)
        return check(raiz)

    assert verificar_postorden(raiz, it), "algún padre apareció antes que su hijo"

    print("\n✓ Todas las pruebas pasaron")
