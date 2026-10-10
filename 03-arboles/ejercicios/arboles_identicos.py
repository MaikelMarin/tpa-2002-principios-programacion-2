r"""
Ejercicio 11: Árboles idénticos
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Recursión sobre árboles.
    - Inducción estructural sobre pares de árboles.
    - Diferencia entre "idénticos" y "simétricos".

PROBLEMA (dos variantes)
    1. ¿Son dos árboles idénticos? Misma estructura Y mismos valores.
    2. ¿Es un árbol simétrico (espejo de sí mismo)?

ESTRATEGIA PARA "IDÉNTICOS"
    Comparar recursivamente:
        si ambos son None      → idénticos (caso base)
        si uno es None         → distintos
        si los valores difieren → distintos
        si no                  → idénticos si y solo si
                                  izq(a)≡izq(b) Y der(a)≡der(b)

    Caso base: dos árboles vacíos son idénticos. Un árbol vacío y uno
    con un nodo no lo son.

TRAZA de son_identicos(A, B) con:
    A:  1        B:  1
       / \          / \
      2   3        2   3

    ambos no None, valores 1 == 1 → recursar
      son_identicos(A.izq=2, B.izq=2): 2==2, ambos hojas → True
      son_identicos(A.der=3, B.der=3): 3==3 → True
    → True

    Contraste con A: 1/2,3  vs  C: 1/3,2:
      son_identicos(A.izq=2, C.izq=3): 2 != 3 → False

DEMOSTRACIÓN
    Inducción estructural sobre el par (a, b).
    Caso base: ambos None → True (correcto, definición).
    Caso uno vacío: False (correcto).
    Paso: si a.valor == b.valor, los árboles son idénticos si y solo
    si sus subárboles izquierdos lo son Y sus subárboles derechos lo
    son. Es exactamente la definición de identidad de árboles. ∎

COMPLEJIDAD
    Tiempo: O(min(n_a, n_b)). En cuanto difiere una rama, se corta.
    Espacio: O(min(h_a, h_b)) de pila.

    No es O(n) siempre: si los primeros nodos difieren, se corta en
    O(1). Decir O(n) sería correcto como cota pero impreciso.

ESTRATEGIA PARA "SIMÉTRICO"
    Un árbol es simétrico si su subárbol izquierdo es el espejo del
    derecho. Se resuelve con una función que compara dos árboles
    "en espejo":

        espejo(a, b):
            si ambos None → True
            si uno None → False
            si a.valor != b.valor → False
            return espejo(a.izq, b.der) and espejo(a.der, b.izq)

    Observe el CRUCE: el izquierdo de uno se compara con el DERECHO
    del otro. Ese cruce es toda la diferencia con "idénticos".

TRAZA de es_simetrico sobre:
            1
           / \
          2   2
         /     \
        3       3

    es_simetrico(1): llama espejo(2, 2)
      valores iguales
      espejo(3, None) → uno es None → False

    Correcto: NO es simétrico, porque el 3 está a la izquierda en un
    lado y a la derecha en el otro.

    Árbol simétrico correcto:
            1
           / \
          2   2
         / \ / \
        3  4 4  3

RELACIÓN CON OTROS TEMAS
    La misma idea de "comparar dos estructuras recursivamente" se usa
      para verificar que dos grafos son isomorfos (tema 04).
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def son_identicos(a, b):
    """¿Son dos árboles idénticos en estructura y valores?"""
    if a is None and b is None:
        return True                     # caso base: ambos vacíos
    if a is None or b is None:
        return False                    # uno vacío, el otro no
    if a.valor != b.valor:
        return False
    return (son_identicos(a.izquierdo, b.izquierdo) and
            son_identicos(a.derecho, b.derecho))


def es_simetrico(nodo):
    """¿El árbol es espejo de sí mismo?"""
    def espejo(a, b):
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
        if a.valor != b.valor:
            return False
        # El cruce izq↔der es lo que define el espejo
        return espejo(a.izquierdo, b.derecho) and espejo(a.derecho, b.izquierdo)

    return espejo(nodo, nodo)


if __name__ == "__main__":
    # Árboles idénticos
    a1 = Nodo(1); a1.izquierdo = Nodo(2); a1.derecho = Nodo(3)
    a1.izquierdo.izquierdo = Nodo(4)

    a2 = Nodo(1); a2.izquierdo = Nodo(2); a2.derecho = Nodo(3)
    a2.izquierdo.izquierdo = Nodo(4)

    print(f"a1 y a2 idénticos: {son_identicos(a1, a2)}")
    assert son_identicos(a1, a2) is True

    # Mismos valores, distinta estructura
    a3 = Nodo(1); a3.izquierdo = Nodo(2); a3.derecho = Nodo(3)
    a3.izquierdo.derecho = Nodo(4)          # el 4 cambió de lado
    print(f"a1 y a3 idénticos: {son_identicos(a1, a3)}")
    assert son_identicos(a1, a3) is False

    # Distintos valores
    a4 = Nodo(1); a4.izquierdo = Nodo(9); a4.derecho = Nodo(3)
    assert son_identicos(a1, a4) is False

    # Casos base
    assert son_identicos(None, None) is True
    assert son_identicos(None, a1) is False
    assert son_identicos(a1, None) is False
    assert son_identicos(Nodo(5), Nodo(5)) is True
    assert son_identicos(Nodo(5), Nodo(6)) is False

    # Un solo nodo vs un nodo con hijos
    hoja = Nodo(1)
    con_hijos = Nodo(1); con_hijos.izquierdo = Nodo(2)
    assert son_identicos(hoja, con_hijos) is False

    # --- Simetría ---
    # No simétrico (el 3 a la izquierda en un lado, a la derecha en otro)
    no_sim = Nodo(1)
    no_sim.izquierdo = Nodo(2); no_sim.derecho = Nodo(2)
    no_sim.izquierdo.izquierdo = Nodo(3)
    no_sim.derecho.derecho = Nodo(3)
    no_sim.izquierdo.derecho = Nodo(4)      # falta el espejo del 4
    assert es_simetrico(no_sim) is False

    # Simétrico
    sim = Nodo(1)
    sim.izquierdo = Nodo(2); sim.derecho = Nodo(2)
    sim.izquierdo.izquierdo = Nodo(3); sim.izquierdo.derecho = Nodo(4)
    sim.derecho.izquierdo = Nodo(4); sim.derecho.derecho = Nodo(3)
    print(f"Árbol simétrico: {es_simetrico(sim)}")
    assert es_simetrico(sim) is True

    # Casos base de simetría
    assert es_simetrico(None) is True
    assert es_simetrico(Nodo(1)) is True
    desbalanceado = Nodo(1); desbalanceado.izquierdo = Nodo(2)
    assert es_simetrico(desbalanceado) is False

    # Un árbol que solo tiene hijo izquierdo NO es simétrico
    # (es la trampa clásica: parece "balanceado" pero no es espejo)
    asimetrico = Nodo(1); asimetrico.izquierdo = Nodo(2)
    assert es_simetrico(asimetrico) is False
    assert asimetrico.izquierdo.derecho is None, "asimetrico no tiene espejo"

    # Pero un árbol vacío por un lado y con nodo por el otro tampoco
    vacio_vs_nodo = Nodo(1)
    vacio_vs_nodo.derecho = Nodo(2)
    assert es_simetrico(vacio_vs_nodo) is False

    # Simétrico perfecto de 3 niveles
    perfecto_sim = Nodo(1)
    perfecto_sim.izquierdo = Nodo(2); perfecto_sim.derecho = Nodo(2)
    perfecto_sim.izquierdo.izquierdo = Nodo(3); perfecto_sim.izquierdo.derecho = Nodo(4)
    perfecto_sim.derecho.izquierdo = Nodo(4); perfecto_sim.derecho.derecho = Nodo(3)
    assert es_simetrico(perfecto_sim) is True

    # Verificación cruzada con son_identicos: un árbol simétrico debe
    # ser idéntico a su espejo
    def espejar(n):
        if n is None:
            return None
        nuevo = Nodo(n.valor)
        nuevo.izquierdo = espejar(n.derecho)
        nuevo.derecho = espejar(n.izquierdo)
        return nuevo

    assert son_identicos(perfecto_sim, espejar(perfecto_sim)) is True
    assert son_identicos(a1, espejar(a1)) is False

    print("\n✓ Todas las pruebas pasaron")
