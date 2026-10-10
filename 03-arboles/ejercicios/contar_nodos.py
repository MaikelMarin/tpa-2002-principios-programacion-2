r"""
Ejercicio 3: Contar nodos recursivamente
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Recursión sobre árboles (ejercicio recorridos.py).
    - Inducción estructural (§3.6 de fundamentos).
    - Diferencia entre "número de llamadas" y "profundidad".

PROBLEMA
    Contar el número total de nodos de un árbol binario, y también
    cuántos son hojas.

ESTRATEGIA
    Patrón "combinar resultados de los subárboles", la forma canónica
    de recursión sobre árboles:

        nodos(nodo) = 1 + nodos(nodo.izquierdo) + nodos(nodo.derecho)

    El 1 cuenta el nodo actual; las dos llamadas cuentan los subárboles.
    Caso base: nodo None contribuye 0.

    Para contar HOJAS, el patrón cambia ligeramente: un nodo es hoja
    si AMBOS hijos son None.

        hojas(nodo) = 1                      si izq y der son None
                    = hojas(izq) + hojas(der) en otro caso

TRAZA de nodos() sobre:
            1
           / \
          2   3

    nodos(1) = 1 + nodos(2) + nodos(3)
             = 1 + (1 + nodos(None) + nodos(None))
                 + (1 + nodos(None) + nodos(None))
             = 1 + (1 + 0 + 0) + (1 + 0 + 0)
             = 3

    Observe que se hacen 7 llamadas para 3 nodos: una por cada nodo
    real más una por cada referencia nula. Eso es normal y no cambia
    la complejidad (sigue siendo Θ(n) porque las referencias nulas
    son exactamente n+1 en un árbol binario).

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción estructural.
    Caso base: nodos(None) = 0. Correcto.
    Hipótesis: nodos() es correcto para subárboles de altura < h.
    Paso: nodos(n) = 1 + nodos(izq) + nodos(der). Por hipótesis, las
    dos llamadas devuelven los tamaños correctos. Sumar 1 (el nodo
    actual) da el total. ∎

COMPLEJIDAD
    Tiempo: Θ(n). Se visita cada nodo exactamente una vez, más las
    n+1 referencias nulas (coste constante adicional).
    Espacio: Θ(h) de pila. En árbol degenerado, Θ(n).

ERROR CLÁSICO: CONFUNDIR CONTAR NODOS CON LA ALTURA
    Contar nodos devuelve n (el total). La altura devuelve el camino
    más largo (log n o n). Son métricas distintas:
      - Para calcular la ALTURA se toma el MÁXIMO de los subárboles.
      - Para contar NODOS se SUMAN los subárboles.
    Confundir max con suma es el error más común en este ejercicio.

RELACIÓN CON OTROS TEMAS
    - El mismo patrón "1 + recursión + recursión" aparece al calcular
      el tamaño de subárboles en un AVL (necesario para el balanceo).
    - En grafos (tema 04), contar componentes conexos usa la misma
      idea de explotar alcanzabilidad.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def contar_nodos(nodo):
    """Cuenta el total de nodos del árbol.

    nodos(n) = 1 + nodos(izq) + nodos(der)
    """
    if nodo is None:
        return 0
    return 1 + contar_nodos(nodo.izquierdo) + contar_nodos(nodo.derecho)


def contar_hojas(nodo):
    """Cuenta los nodos hoja (sin hijos)."""
    if nodo is None:
        return 0
    if nodo.izquierdo is None and nodo.derecho is None:
        return 1
    return contar_hojas(nodo.izquierdo) + contar_hojas(nodo.derecho)


def contar_internos(nodo):
    """Cuenta los nodos con al menos un hijo."""
    if nodo is None:
        return 0
    if nodo.izquierdo is None and nodo.derecho is None:
        return 0
    return 1 + contar_internos(nodo.izquierdo) + contar_internos(nodo.derecho)


if __name__ == "__main__":
    # Árbol de referencia
    #        1
    #       / \
    #      2   3
    #     / \   \
    #    4   5   6
    raiz = Nodo(1)
    raiz.izquierdo = Nodo(2)
    raiz.derecho = Nodo(3)
    raiz.izquierdo.izquierdo = Nodo(4)
    raiz.izquierdo.derecho = Nodo(5)
    raiz.derecho.derecho = Nodo(6)

    print(f"Total de nodos:   {contar_nodos(raiz)}")
    print(f"Total de hojas:   {contar_hojas(raiz)}")
    print(f"Nodos internos:   {contar_internos(raiz)}")

    assert contar_nodos(raiz) == 6
    assert contar_hojas(raiz) == 3, "las hojas son 4, 5 y 6"

    # Casos base
    assert contar_nodos(None) == 0, "árbol vacío"
    assert contar_hojas(None) == 0
    assert contar_internos(None) == 0

    # Un solo nodo: es hoja y no es interno
    solo = Nodo(42)
    assert contar_nodos(solo) == 1
    assert contar_hojas(solo) == 1
    assert contar_internos(solo) == 0

    # Invariante: nodos = hojas + internos
    def verificar(n):
        if n is None:
            return True
        assert contar_nodos(n) == contar_hojas(n) + contar_internos(n)
        return verificar(n.izquierdo) and verificar(n.derecho)
    assert verificar(raiz)

    # Árbol degenerado (lista): 1 hoja, n-1 internos
    deg = Nodo(1)
    actual = deg
    for v in [2, 3, 4, 5]:
        actual.derecho = Nodo(v)
        actual = actual.derecho
    assert contar_nodos(deg) == 5
    assert contar_hojas(deg) == 1, "degenerado: solo la última es hoja"
    assert contar_internos(deg) == 4

    # Árbol lleno perfecto de 7 nodos: 4 hojas, 3 internos
    pleno = Nodo(1)
    pleno.izquierdo = Nodo(2)
    pleno.derecho = Nodo(3)
    pleno.izquierdo.izquierdo = Nodo(4)
    pleno.izquierdo.derecho = Nodo(5)
    pleno.derecho.izquierdo = Nodo(6)
    pleno.derecho.derecho = Nodo(7)
    assert contar_nodos(pleno) == 7
    assert contar_hojas(pleno) == 4
    assert contar_internos(pleno) == 3

    # Verificación: número de llamadas = 2n + 1
    llamadas = [0]
    def nodos_contando(n):
        llamadas[0] += 1
        if n is None:
            return 0
        return 1 + nodos_contando(n.izquierdo) + nodos_contando(n.derecho)
    nodos_contando(raiz)
    print(f"\nLlamadas realizadas: {llamadas[0]} (= 2·6+1)")
    assert llamadas[0] == 2 * 6 + 1

    print("\n✓ Todas las pruebas pasaron")
