r"""
Ejercicio 19: K-ésimo elemento menor
Dificultad: Avanzado

CONOCIMIENTO PREVIO NECESARIO
    - Recorrido inorden (devuelve los valores ORDENADOS de un BST).
    - Iterador de BST (ejercicio 15).
    - Logaritmos: la diferencia entre O(h) y O(n).

PROBLEMA
    Encontrar el k-ésimo elemento más pequeño de un BST.

FONDO MATEMÁTICO
    PROPIEDAD CLAVE: el recorrido inorden de un BST produce los
    valores en orden ascendente (teorema §4.1). Por tanto, el k-ésimo
    más pequeño es simplemente el k-ésimo elemento del inorden.

    De ahí salen dos enfoques muy distintos:

    1. INORDEN COMPLETO: generar todo el recorrido y tomar el
       elemento k. Fácil, pero O(n) tiempo y O(n) espacio.

    2. CON SUBÁRBOLES TAMAÑO: si cada nodo guarda el tamaño de su
       subárbol, se puede DESCENDER directamente como en una búsqueda
       binaria, descartando subárboles enteros. O(h) tiempo, O(1)
       espacio.

    El segundo enfoque es el interesante: en vez de generar n
    elementos, solo baja por la altura del árbol.

ESTRATEGIA DEL ENFOQUE EFICIENTE
    Cada nodo conoce `tamano_izq` = número de nodos en su subárbol
    izquierdo. Entonces:

        si k == tamano_izq + 1:  el nodo actual ES el k-ésimo
        si k <= tamano_izq:      está en el subárbol izquierdo
        si k >  tamano_izq + 1:  está en el derecho, y ahora
                                  buscamos el (k - tamano_izq - 1)-ésimo

    El −1 cuenta el nodo actual, que queda "consumido" al bajar a la
    derecha.

TRAZA de k_esimo(raiz, 3) sobre:
            5            tamano_izq(5) = 3 (nodos 1, 3, 4)
           / \
          3   8          tamano_izq(3) = 1 (nodo 1)
         / \   \
        1   4   9

    k = 3.
    Nodo 5: tamano_izq = 3. ¿3 == 3+1=4? No. ¿3 <= 3? Sí → bajar izq, k sigue 3.
    Nodo 3: tamano_izq = 1. ¿3 == 1+1=2? No. ¿3 > 2? Sí → bajar der,
            k = 3 − 1 − 1 = 1.
    Nodo 4: es hoja, tamano_izq = 0. ¿1 == 0+1=1? ¡SÍ! → devolver 4.

    Verificación: inorden = [1, 3, 4, 5, 8, 9]. El 3.º es 4. ✓

    Solo 3 comparaciones, no 5 nodos recorridos.

DEMOSTRACIÓN DE CORRECCIÓN
    Invariante: al entrar en un nodo con parámetro k, el k-ésimo menor
    elemento de SU subárbol es la respuesta buscada.

    - Si k == tamano_izq + 1: hay exactamente k−1 elementos menores
      que el nodo actual (los de su subárbol izquierdo), luego el
      nodo actual es el k-ésimo. Correcto.
    - Si k <= tamano_izq: el elemento está entre los tamano_izq
      menores, todos en el subárbol izquierdo. Bajar preserva el
      invariante con el mismo k.
    - Si k > tamano_izq + 1: hay tamano_izq + 1 elementos menores o
      iguales (el izquierdo más el nodo), así que buscamos el
      (k − tamano_izq − 1)-ésimo del subárbol derecho. El invariante
      se preserva con el nuevo k. ∎

COMPLEJIDAD
    Con tamaños almacenados: O(h) tiempo, O(1) espacio iterativo.
        - Balanceado: O(log n)
        - Degenerado: O(n)
    Sin tamaños (inorden completo): O(n) tiempo, O(h) espacio con
    el iterador, o O(n) si se materializa la lista.

COMPARACIÓN
    Enfoque                  Tiempo      Espacio
    Inorden + índice k       O(n)        O(h) con iterador
    Con tamaños de subárbol  O(h)        O(1)

    El precio del segundo: cada inserción y eliminación debe
    mantener actualizados los tamaños. Es el mismo trade-off que
    aceptan los árboles de orden estadístico (order-statistic trees).

RELACIÓN CON OTROS TEMAS
    - Los order-statistic trees son una extensión de los Rojo-Negro
      que permite seleccionar el k-ésimo en O(log n) garantizado.
    - En bases de datos, `SELECT ... ORDER BY ... LIMIT 1 OFFSET k`
      sobre un índice B-tree se resuelve con esta técnica.
"""


class Nodo:
    """Nodo que almacena el tamaño de su subárbol izquierdo."""

    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.tamano_izq = 0

    def __repr__(self):
        return f"Nodo({self.valor})"


def calcular_tamano(nodo):
    """Rellena tamano_izq en cada nodo (postorden)."""
    if nodo is None:
        return 0
    izq = calcular_tamano(nodo.izquierdo)
    nodo.tamano_izq = izq
    der = calcular_tamano(nodo.derecho)
    return 1 + izq + der


def k_esimo_menor(raiz, k):
    """K-ésimo menor usando tamaños: O(h) tiempo, O(1) espacio."""
    actual = raiz
    while actual:
        t_izq = actual.tamano_izq

        if k == t_izq + 1:
            return actual.valor             # es este nodo
        elif k <= t_izq:
            actual = actual.izquierdo        # está a la izquierda
        else:
            k -= t_izq + 1                   # consumir izq + nodo actual
            actual = actual.derecho          # está a la derecha
    return None


def insertar(raiz, valor):
    """Inserta en el BST."""
    if raiz is None:
        return Nodo(valor)
    if valor < raiz.valor:
        raiz.izquierdo = insertar(raiz.izquierdo, valor)
    elif valor > raiz.valor:
        raiz.derecho = insertar(raiz.derecho, valor)
    return raiz


def inorden(nodo):
    if nodo is None:
        return []
    return inorden(nodo.izquierdo) + [nodo.valor] + inorden(nodo.derecho)


if __name__ == "__main__":
    # Construir el árbol del ejemplo
    raiz = None
    for val in [5, 3, 8, 1, 4, 9]:
        raiz = insertar(raiz, val)
    calcular_tamano(raiz)

    io = inorden(raiz)
    print(f"Inorden: {io}")
    print(f"\nK-ésimo menor:")
    for k in range(1, len(io) + 1):
        v = k_esimo_menor(raiz, k)
        print(f"  {k}º → {v}")
        assert v == io[k - 1], f"falló en k={k}"

    # Casos base
    assert k_esimo_menor(raiz, 1) == min(io), "el primero es el mínimo"
    assert k_esimo_menor(raiz, len(io)) == max(io), "el último es el máximo"

    # Fuera de rango
    assert k_esimo_menor(raiz, 0) is None
    assert k_esimo_menor(raiz, len(io) + 1) is None
    assert k_esimo_menor(None, 1) is None

    # Un solo nodo
    solo = insertar(None, 42)
    calcular_tamano(solo)
    assert k_esimo_menor(solo, 1) == 42

    # Verificación exhaustiva aleatoria
    import random
    random.seed(71)
    for _ in range(300):
        valores = random.sample(range(-500, 500), random.randint(1, 40))
        arbol = None
        for v in valores:
            arbol = insertar(arbol, v)
        calcular_tamano(arbol)
        ordenados = sorted(valores)
        for k in range(1, len(ordenados) + 1):
            assert k_esimo_menor(arbol, k) == ordenados[k - 1], f"k={k}"

    # El enfoque O(h) vs el O(n): contar nodos visitados
    def k_esimo_contando(raiz, k):
        pasos = 0
        actual = raiz
        while actual:
            pasos += 1
            t_izq = actual.tamano_izq
            if k == t_izq + 1:
                return actual.valor, pasos
            elif k <= t_izq:
                actual = actual.izquierdo
            else:
                k -= t_izq + 1
                actual = actual.derecho
        return None, pasos

    # Árbol balanceado de 1023 nodos (2^10 − 1)
    def construir_balanceado(vals):
        if not vals:
            return None
        m = len(vals) // 2
        n = Nodo(vals[m])
        n.izquierdo = construir_balanceado(vals[:m])
        n.derecho = construir_balanceado(vals[m + 1:])
        return n

    bal = construir_balanceado(list(range(1, 1024)))
    calcular_tamano(bal)
    io_bal = inorden(bal)

    print(f"\nBST balanceado de {len(io_bal)} nodos:")
    for k in [1, 500, 1023]:
        valor, pasos = k_esimo_contando(bal, k)
        print(f"  k={k}: valor={valor}, nodos visitados={pasos} (altura ≈ 10)")
        assert valor == io_bal[k - 1]
        assert pasos <= 11, "no debería visitar más que la altura"

    # Coste de mantener los tamaños: cada inserción los actualiza
    arbol = None
    for v in [5, 3, 8, 1, 4]:
        arbol = insertar(arbol, v)
    calcular_tamano(arbol)
    n1 = inorden(arbol)[1]
    print(f"\nCon tamaños: 2.º menor = {k_esimo_menor(arbol, 2)} (esperado {n1})")
    assert k_esimo_menor(arbol, 2) == n1

    print("\n✓ Todas las pruebas pasaron")
