r"""
Ejercicio 18: Árbol de expresiones
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - Árboles binarios y sus recorridos (ejercicio recorridos.py).
    - Notación postfija (RPN).
    - Recursión sobre árboles.

PROBLEMA
    Representar una expresión aritmética como árbol y evaluarla.

FONDO MATEMÁTICO
    Un árbol de expresiones es un árbol binario donde:
      - Las HOJAS son operandos (números).
      - Los nodos INTERNOS son operadores (+, −, ×, ÷).

    La estructura del árbol codifica la PRECEDENCIA, así que no hacen
    falta paréntesis:

        (3 + 5) × 2

                ×
               / \
              +   2
             / \
            3   5

    Y los recorridos dan las tres notaciones clásicas:
      - Preorden:  × + 3 5 2     (notación prefija / polaca)
      - Inorden:   3 + 5 × 2     (notación infija, necesita paréntesis)
      - Postorden: 3 5 + 2 ×     (notación postfija / polaca inversa)

ESTRATEGIA DE EVALUACIÓN (postorden recursivo)
    La evaluación es un postorden natural:

        1. Evaluar el subárbol izquierdo.
        2. Evaluar el subárbol derecho.
        3. Aplicar el operador del nodo actual a ambos resultados.

    ¿Por qué postorden? Porque para aplicar un operador hay que tener
    listos sus dos operandos, y esos están en los subárboles. Es un
    caso de "resolver las dependencias antes".

    Implementación:

```python
def evaluar(nodo):
    if isinstance(nodo.valor, (int, float)):
        return nodo.valor                 # hoja = operando
    izq = evaluar(nodo.izquierdo)         # resolver operandos
    der = evaluar(nodo.derecho)
    if nodo.valor == '+': return izq + der
    if nodo.valor == '-': return izq - der
    if nodo.valor == '*': return izq * der
    if nodo.valor == '/':
        if der == 0: raise ZeroDivisionError("división por cero")
        return izq / der
```

TRAZA de evaluar sobre el árbol de arriba:
    evaluar(×)
      evaluar(+)                     ← subárbol izquierdo
        evaluar(3) = 3               ← hoja
        evaluar(5) = 5               ← hoja
        return 3 + 5 = 8
      evaluar(2) = 2                 ← hoja
      return 8 × 2 = 16

    Resultado: 16

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción estructural.
    Caso base: nodo hoja. Se devuelve su valor, que es el valor de la
    expresión que representa (un solo operando). Correcto.
    Hipótesis: evaluar() es correcto para los subárboles de un nodo.
    Paso: para un nodo operador, la expresión que representa es
    (expr_izq) op (expr_der). Por hipótesis, evaluar devuelve el valor
    de cada lado, y aplicar el operador da el valor de la expresión
    completa. Correcto. ∎

COMPLEJIDAD
    Tiempo: Θ(n). Cada nodo se visita una vez y el trabajo por nodo
    es O(1) (una operación aritmética).
    Espacio: O(h) de pila; O(n) si se cuenta el árbol.

    Es óptimo: hay que mirar cada nodo al menos una vez.

CASOS LÍMITE
    - División por cero: debe lanzar excepción, no devolver inf.
    - Un solo número (árbol de un nodo): devuelve ese número.
    - Operador desconocido: la implementación debería lanzar error en
      vez de retornar 0 silenciosamente (0 sería un valor plausible
      y el error pasaría desapercibido).
    - Árbol vacío (None): devolver 0 o lanzar; hay que documentarlo.

RELACIÓN CON OTROS TEMAS
    - Los COMPILADORES construyen un árbol de sintaxis abstracta (AST)
      así, y lo evalúan o lo traducen a código máquina.
    - La evaluación postfija con una pila (sin árbol) es equivalente:
      es lo que hacen las calculadoras HP.
    - El parsing de expresiones usa recursión descendente (tema 01).
"""


class Nodo:
    """Nodo de árbol de expresiones: operando (hoja) u operador."""

    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def evaluar(nodo):
    """Evalúa el árbol de expresiones. O(n) tiempo, O(h) espacio."""
    if nodo is None:
        return 0

    # Caso base: hoja con un operando
    if isinstance(nodo.valor, (int, float)):
        return nodo.valor

    # Resolver los operandos primero (postorden)
    izq = evaluar(nodo.izquierdo)
    der = evaluar(nodo.derecho)

    if nodo.valor == '+':
        return izq + der
    if nodo.valor == '-':
        return izq - der
    if nodo.valor == '*':
        return izq * der
    if nodo.valor == '/':
        if der == 0:
            raise ZeroDivisionError("División por cero en el árbol de expresiones")
        return izq / der

    raise ValueError(f"Operador desconocido: {nodo.valor!r}")


def postfija(nodo):
    """Recorrido postfijo: la expresión en notación polaca inversa."""
    if nodo:
        postfija(nodo.izquierdo)
        postfija(nodo.derecho)
        print(nodo.valor, end=" ")
        # Nota: esta versión imprime; para obtener una lista, ver abajo


def postfija_lista(nodo):
    """Postfijo que devuelve una lista en vez de imprimir."""
    if nodo is None:
        return []
    return postfija_lista(nodo.izquierdo) + postfija_lista(nodo.derecho) + [nodo.valor]


def evaluar_postfija(tokens):
    """Evalúa una expresión postfija con una pila: sin árbol.

    Es lo que hacen las calculadoras HP. Sirve para verificar que el
    árbol y la pila dan el mismo resultado.
    """
    pila = []
    for t in tokens:
        if isinstance(t, (int, float)):
            pila.append(t)
        else:
            if len(pila) < 2:
                raise ValueError("Expresión postfija mal formada")
            b = pila.pop()
            a = pila.pop()
            if t == '+':
                pila.append(a + b)
            elif t == '-':
                pila.append(a - b)
            elif t == '*':
                pila.append(a * b)
            elif t == '/':
                if b == 0:
                    raise ZeroDivisionError("División por cero")
                pila.append(a / b)
            else:
                raise ValueError(f"Operador desconocido: {t!r}")
    if len(pila) != 1:
        raise ValueError("Expresión postfija mal formada")
    return pila[0]


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

    resultado = evaluar(raiz)
    print(f"Resultado: {resultado}")
    assert resultado == 16

    # Verificación cruzada con la pila
    pf = postfija_lista(raiz)
    print(f"Postfija como lista: {pf}")
    assert evaluar_postfija(pf) == 16, "el árbol y la pila deben coincidir"

    # Otra expresión: 4 * (2 + 6) - 1
    raiz2 = Nodo('-')
    raiz2.izquierdo = Nodo('*')
    raiz2.derecho = Nodo(1)
    raiz2.izquierdo.izquierdo = Nodo(4)
    raiz2.izquierdo.derecho = Nodo('+')
    raiz2.izquierdo.derecho.izquierdo = Nodo(2)
    raiz2.izquierdo.derecho.derecho = Nodo(6)
    assert evaluar(raiz2) == 4 * (2 + 6) - 1 == 31
    assert evaluar_postfija(postfija_lista(raiz2)) == 31

    # Caso base: un solo número
    solo = Nodo(7)
    assert evaluar(solo) == 7
    assert evaluar_postfija([7]) == 7

    # División por cero: debe lanzar, no devolver inf
    div0 = Nodo('/')
    div0.izquierdo = Nodo(5)
    div0.derecho = Nodo(0)
    try:
        evaluar(div0)
        raise AssertionError("debía lanzar ZeroDivisionError")
    except ZeroDivisionError:
        print("División por cero detectada ✓")

    # La pila también detecta la división por cero
    try:
        evaluar_postfija([5, 0, '/'])
        raise AssertionError("debía lanzar ZeroDivisionError")
    except ZeroDivisionError:
        pass

    # Cuadrado: 5 * 5
    cuadrado = Nodo('*')
    cuadrado.izquierdo = Nodo(5); cuadrado.derecho = Nodo(5)
    assert evaluar(cuadrado) == 25

    # Resta NO conmutativa: importa el orden de los hijos
    resta = Nodo('-')
    resta.izquierdo = Nodo(10); resta.derecho = Nodo(3)
    assert evaluar(resta) == 7, "el orden de los hijos importa en la resta"
    resta_inv = Nodo('-')
    resta_inv.izquierdo = Nodo(3); resta_inv.derecho = Nodo(10)
    assert evaluar(resta_inv) == -7, "y también en la división y la resta"

    # División no conmutativa
    div = Nodo('/')
    div.izquierdo = Nodo(20); div.derecho = Nodo(4)
    assert evaluar(div) == 5.0

    # Verificación aleatoria contra eval() de Python
    import random

    def construir_aleatorio(profundidad, rng):
        if profundidad == 0 or rng.random() < 0.3:
            return Nodo(rng.randint(1, 20))
        nodo = Nodo(rng.choice(['+', '-', '*']))
        nodo.izquierdo = construir_aleatorio(profundidad - 1, rng)
        nodo.derecho = construir_aleatorio(profundidad - 1, rng)
        return nodo

    def a_infijo(n):
        if isinstance(n.valor, (int, float)):
            return str(n.valor)
        return f"({a_infijo(n.izquierdo)} {n.valor} {a_infijo(n.derecho)})"

    rng = random.Random(101)
    for _ in range(500):
        arbol = construir_aleatorio(3, rng)
        infijo = a_infijo(arbol)
        assert evaluar(arbol) == eval(infijo), f"discrepancia en {infijo}"
        assert evaluar_postfija(postfija_lista(arbol)) == eval(infijo)

    # Eficiencia: O(n) — cada nodo se visita una vez.
    # NOTA: la profundidad se limita a 900 porque la evaluación es
    # recursiva y Python pone el límite en 1000. Con árboles más
    # profundos har falta una versión iterativa o subir el límite.
    import sys

    profundo = Nodo('+')
    actual = profundo
    for i in range(900):
        actual.izquierdo = Nodo(1)          # hoja izquierda
        actual.derecho = Nodo('+')          # sigue bajando
        actual = actual.derecho
    # El último nivel: dos hojas
    actual.izquierdo = Nodo(1)
    actual.derecho = Nodo(1)

    # Conteo real de hojas: cada iteración añade 1 hoja izquierda
    # (900), más las 2 hojas del último nivel = 902.
    # Los 900 nodos '+' son operadores, no hojas.
    esperado = 900 + 2
    sys.setrecursionlimit(10000)
    try:
        valor = evaluar(profundo)
        print(f"\nSuma de {esperado} hojas distribuidas en 900 niveles: {valor}")
        assert valor == esperado
    finally:
        sys.setrecursionlimit(1000)

    print("\n✓ Todas las pruebas pasaron")
