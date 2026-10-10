r"""
Ejercicio 8: Verificar si un árbol es BST válido
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Invariante BST (teoria.md §4.1).
    - El error clásico de validación (teoria.md §4.4).

PROBLEMA
    Determinar si un árbol binario cumple la propiedad BST.

EL ERROR CLÁSICO (y por qué este ejercicio existe)
    La verificación ingenua es: "el hijo izquierdo es menor que el
    padre y el derecho es mayor". ESO NO BASTA.

    Contraejemplo:
            5
           / \
          1   6
             / \
            3   7

    Veamos: 1 < 5 ✓, 6 > 5 ✓, 3 < 6 ✓, 7 > 6 ✓.
    ¡Todo parece correcto! Pero el 3 está en el subárbol DERECHO del 5
    y sin embargo 3 < 5. La invariante BST exige que TODOS los valores
    del subárbol derecho sean MAYORES que 5. El 3 la viola.

    La verificación ingenua falla porque solo compara cada nodo con su
    PADRE INMEDIATO, ignorando a los ancestros más lejanos.

LA SOLUCIÓN: PROPAGAR LÍMITES
    Cada nodo debe estar dentro del rango (mínimo, máximo) que hereda
    de sus ancestros, no solo respecto a su padre:

        es_bst_valido(nodo, minimo, maximo):
            si nodo is None:  return True
            si no (minimo < nodo.valor < maximo):  return False
            return (es_bst_valido(nodo.izquierdo, minimo, nodo.valor)
                and es_bst_valido(nodo.derecho, nodo.valor, maximo))

    Al bajar por la izquierda, el MÁXIMO se restringe al valor actual.
    Al bajar por la derecha, el MÍNIMO se restringe.

TRAZA con el contraejemplo
    es_bst_valido(5, −∞, +∞)
      5 en rango ✓
      → es_bst_valido(1, −∞, 5):      1 en rango ✓ → hoja, True
      → es_bst_valido(6, 5, +∞):      6 en rango ✓
          → es_bst_valido(3, 5, 6):    3 NO está en (5, 6) ← ¡FALLA!
          → es_bst_valido(7, 6, +∞):  7 en rango ✓
          retorna False

    Detectado correctamente.

LA SEGUNDA SOLUCIÓN: INORDEN ORDENADO
    Un árbol es BST si y solo si su recorrido inorden produce una
    secuencia estrictamente creciente (teorema §4.1).

        def es_bst_valido_inorden(raiz):
            valores = inorden(raiz)
            return all(valores[i] < valores[i+1] for i in range(len(valores)-1))

    Es más simple de escribir, pero usa O(n) de memoria extra para
    la lista. La versión de límites usa O(h).

    CUIDADO con el < vs <=: si el árbol permite duplicados, el
    inorden no es estrictamente creciente. Esta implementación
    rechaza duplicados.

DEMOSTRACIÓN DE CORRECCIÓN (versión de límites)
    Invariante: al llamar es_bst_valido(n, mn, mx), se garantiza que
    si el subárbol n es un BST válido Y mn < todo valor de n < mx,
    entonces toda la estructura es un BST válido.

    - Si n no está en (mn, mx), se retorna False: correcto, porque
      violaría la restricción heredada de un ancestro.
    - Si n está en rango, se propaga (mn, n) a la izquierda y (n, mx)
      a la derecha. Como todo valor izquierdo debe ser < n y todo
      derecho > n (invariante BST), los rangos son exactamente las
      restricciones necesarias y suficientes. ∎

COMPLEJIDAD
    Tiempo: O(n). Se visita cada nodo una vez.
    Espacio: O(h) de pila para la versión de límites;
             O(n) para la versión de inorden.

RELACIÓN CON OTROS TEMAS
    - El mismo patrón "propagar restricciones al recursar" aparece en
      elorden topológico (tema 04), donde se propaga el estado de
      visita de cada vértice.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def es_bst_valido(nodo, minimo=float('-inf'), maximo=float('inf')):
    """Verifica la propiedad BST propagando límites. O(h) de espacio."""
    if nodo is None:
        return True
    if not (minimo < nodo.valor < maximo):
        return False
    return (es_bst_valido(nodo.izquierdo, minimo, nodo.valor) and
            es_bst_valido(nodo.derecho, nodo.valor, maximo))


def es_bst_valido_inorden(nodo):
    """Alternativa: el inorden de un BST es estrictamente creciente.

    Más simple, pero O(n) de espacio por la lista.
    """
    valores = []

    def inorden(n):
        if n:
            inorden(n.izquierdo)
            valores.append(n.valor)
            inorden(n.derecho)

    inorden(nodo)
    return all(valores[i] < valores[i + 1] for i in range(len(valores) - 1))


if __name__ == "__main__":
    # BST válido
    raiz1 = Nodo(5)
    raiz1.izquierdo = Nodo(3)
    raiz1.derecho = Nodo(7)
    raiz1.izquierdo.izquierdo = Nodo(1)
    raiz1.izquierdo.derecho = Nodo(4)

    print(f"Árbol 1 es BST válido: {es_bst_valido(raiz1)}")
    assert es_bst_valido(raiz1) is True
    assert es_bst_valido_inorden(raiz1) is True

    # El contraejemplo clásico: pasa la verificación ingenua, falla aquí
    raiz2 = Nodo(5)
    raiz2.izquierdo = Nodo(1)
    raiz2.derecho = Nodo(6)
    raiz2.derecho.izquierdo = Nodo(3)      # 3 < 5 pero está a la derecha de 5
    raiz2.derecho.derecho = Nodo(7)

    print(f"Árbol 2 es BST válido: {es_bst_valido(raiz2)}")
    assert es_bst_valido(raiz2) is False, "el contraejemplo debe detectarse"
    assert es_bst_valido_inorden(raiz2) is False

    # La verificación ingenua NO detecta el problema
    def ingenua(n):
        if n is None:
            return True
        if n.izquierdo and not n.izquierdo.valor < n.valor:
            return False
        if n.derecho and not n.derecho.valor > n.valor:
            return False
        return ingenua(n.izquierdo) and ingenua(n.derecho)

    print(f"Verificación ingenua dice: {ingenua(raiz2)} (¡incorrecto!)")
    assert ingenua(raiz2) is True, "la ingenua se deja engañar"

    # Casos base
    assert es_bst_valido(None) is True, "árbol vacío es BST"
    solo = Nodo(1)
    assert es_bst_valido(solo) is True

    # Duplicados: no es BST estricto
    dup = Nodo(5)
    dup.izquierdo = Nodo(5)
    assert es_bst_valido(dup) is False, "duplicado rechazado"
    assert es_bst_valido_inorden(dup) is False

    # Más casos: violación a distintas profundidades
    profundo = Nodo(10)
    profundo.izquierdo = Nodo(5)
    profundo.derecho = Nodo(15)
    profundo.izquierdo.izquierdo = Nodo(2)
    profundo.izquierdo.derecho = Nodo(8)
    profundo.izquierdo.derecho.derecho = Nodo(9)
    profundo.izquierdo.derecho.derecho.derecho = Nodo(12)   # 12 > 10, en el izq de 10
    assert es_bst_valido(profundo) is False, "violación profunda detectada"

    # Árbol que solo falla por el límite derecho
    der = Nodo(10)
    der.izquierdo = Nodo(5)
    der.derecho = Nodo(15)
    der.derecho.izquierdo = Nodo(12)     # 12 < 15 pero > 10, en el izq de 15: OK
    assert es_bst_valido(der) is True

    der.derecho.izquierdo.izquierdo = Nodo(9)   # 9 < 10, viola el mínimo heredado
    assert es_bst_valido(der) is False

    print("\n✓ Todas las pruebas pasaron")
