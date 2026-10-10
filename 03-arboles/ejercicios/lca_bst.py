r"""
Ejercicio 14: Ancestro común más bajo (LCA) en BST
Dificultad: Avanzado

CONOCIMIENTO PREVIO NECESARIO
    - Invariante BST (teoria.md §4.1).
    - Búsqueda descendente (ejercicio buscar_bst.py).
    - Logaritmos: por qué es O(h) y no O(n).

PROBLEMA
    Dados dos valores p y q en un BST, encontrar su ancestro común
    más bajo (Lowest Common Ancestor): el nodo más profundo que es
    ancestro de ambos.

    "Ancestro" incluye al propio nodo: el LCA de 2 y 4 en el árbol
    de abajo es 2, no 6.

FONDO MATEMÁTICO
    En un BST, el LCA se identifica por el PUNTO DE SEPARACIÓN de los
    caminos. Bajando desde la raíz:
      - Si p y q son AMBOS menores que el nodo actual → el LCA está
        en el subárbol izquierdo, seguir bajando.
      - Si p y q son AMBOS mayores → el LCA está en el subárbol
        derecho, seguir bajando.
      - EN OTRO CASO (uno menor y otro mayor, o uno igual) → los
        caminos se separan AQUÍ. Este nodo es el LCA.

    La intuición: mientras los dos valores vayan "hacia el mismo
    lado", compartirán más ancestros. En el momento en que uno se va
    a la izquierda y otro a la derecha, el nodo actual es el último
    ancestro compartido.

ESTRATEGIA (una sola pasada, sin recursión)
```python
def lca(raiz, p, q):
    while raiz:
        if p < raiz.valor and q < raiz.valor:
            raiz = raiz.izquierdo        # ambos a la izquierda
        elif p > raiz.valor and q > raiz.valor:
            raiz = raiz.derecho          # ambos a la derecha
        else:
            return raiz.valor            # ¡se separan aquí!
    return None
```

    No hace falta buscar p y q por separado. Basta con bajar una vez
    observando hacia dónde apuntan los dos valores.

TRAZA de lca(raiz, 2, 8) sobre:
            6
           / \
          2   8
         / \   \
        0   4   9

    raiz = 6: ¿2 < 6 y 8 < 6? No. ¿2 > 6 y 8 > 6? No.
              → se separan aquí → LCA = 6

    Correcto: 2 está en la izquierda del 6 y 8 en la derecha.

    lca(raiz, 2, 4):
    raiz = 6: ambos < 6 → bajar a la izquierda
    raiz = 2: ¿2 < 2? No. ¿2 > 2? No (son iguales)
              → se separan aquí → LCA = 2

    Correcto: 2 es ancestro de sí mismo y de 4.

    lca(raiz, 0, 4):
    raiz = 6: ambos < 6 → bajar a 2
    raiz = 2: 0 < 2 y 4 > 2 → se separan → LCA = 2

    Correcto.

DEMOSTRACIÓN DE CORRECCIÓN
    Invariante: al iniciar cada iteración, si el LCA existe, es el
    nodo actual o está en su subárbol.

    - Si p y q son ambos menores que el actual, entonces el LCA no
      puede ser el actual (ambos están estrictamente a su izquierda,
      así que hay ancestros más bajos que los contienen). El LCA está
      en el subárbol izquierdo. Al bajar, el invariante se preserva.
    - Caso simétrico para la derecha.
    - Si no se cumple ninguno de los dos casos, entonces uno de los
      valores es ≤ actual y el otro ≥ actual. Como el árbol es un
      BST, p y q están en subárboles distintos (o uno es el actual).
      En cualquiera de los dos casos, el nodo actual es ancestro de
      ambos y ningún descendiente suyo puede serlo. Es el LCA. ∎

COMPLEJIDAD
    Tiempo: O(h). Una sola pasada descendente.
        - Balanceado: O(log n)
        - Degenerado: O(n)
    Espacio: O(1) en la versión iterativa.

    Compare con la versión recursiva: O(h) de pila. Y con la versión
    "buscar caminos y comparar": O(n) y más complicada.

COMPARACIÓN CON ÁRBOL NO ORDENADO
    En un árbol binario cualquiera (sin la invariante BST) NO existe
    este atajo: hay que buscar los caminos desde la raíz hasta p y
    hasta q, y encontrar el último nodo común. Eso es O(n).

    La invariante BST es lo que convierte un O(n) en O(h).

RELACIÓN CON OTROS TEMAS
    - El mismo principio "aprovechar el orden para descartar" aparece
      en la búsqueda binaria sobre arreglos (tema 02) y en la
      búsqueda en lista rotada.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def lca_bst(raiz, p, q):
    """Ancestro común más bajo en un BST. O(h), O(1) de espacio."""
    while raiz:
        if p < raiz.valor and q < raiz.valor:
            raiz = raiz.izquierdo          # ambos por la izquierda
        elif p > raiz.valor and q > raiz.valor:
            raiz = raiz.derecho            # ambos por la derecha
        else:
            return raiz.valor              # punto de separación
    return None


def lca_bst_recursivo(raiz, p, q):
    """Versión recursiva: O(h) de pila."""
    if raiz is None:
        return None
    if p < raiz.valor and q < raiz.valor:
        return lca_bst_recursivo(raiz.izquierdo, p, q)
    if p > raiz.valor and q > raiz.valor:
        return lca_bst_recursivo(raiz.derecho, p, q)
    return raiz.valor


def camino_a(raiz, valor):
    """Camino desde la raíz hasta el valor (para verificar)."""
    camino = []
    actual = raiz
    while actual:
        camino.append(actual.valor)
        if actual.valor == valor:
            return camino
        actual = actual.izquierdo if valor < actual.valor else actual.derecho
    return None


if __name__ == "__main__":
    raiz = Nodo(6)
    raiz.izquierdo = Nodo(2)
    raiz.derecho = Nodo(8)
    raiz.izquierdo.izquierdo = Nodo(0)
    raiz.izquierdo.derecho = Nodo(4)
    raiz.derecho.izquierdo = Nodo(7)
    raiz.derecho.derecho = Nodo(9)

    print("LCA(2, 8) =", lca_bst(raiz, 2, 8))
    print("LCA(2, 4) =", lca_bst(raiz, 2, 4))
    print("LCA(0, 4) =", lca_bst(raiz, 0, 4))
    print("LCA(7, 9) =", lca_bst(raiz, 7, 9))

    assert lca_bst(raiz, 2, 8) == 6, "se separan en la raíz"
    assert lca_bst(raiz, 2, 4) == 2, "2 es ancestro de 4"
    assert lca_bst(raiz, 0, 4) == 2, "comparten el 2"
    assert lca_bst(raiz, 7, 9) == 8, "se separan en el 8"
    assert lca_bst(raiz, 6, 2) == 6, "la raíz es LCA de ella misma y un descendiente"
    assert lca_bst(raiz, 6, 6) == 6
    assert lca_bst(raiz, 0, 9) == 6, "extremos opuestos"

    # Ambas versiones coinciden
    for p in [0, 2, 4, 6, 7, 8, 9]:
        for q in [0, 2, 4, 6, 7, 8, 9]:
            assert lca_bst(raiz, p, q) == lca_bst_recursivo(raiz, p, q)

    # Verificación contra una implementación de referencia
    def lca_referencia(raiz, p, q):
        cp = camino_a(raiz, p)
        cq = camino_a(raiz, q)
        if cp is None or cq is None:
            return None
        comun = None
        for a, b in zip(cp, cq):
            if a == b:
                comun = a
            else:
                break
        return comun

    import random
    random.seed(53)
    for _ in range(200):
        # Construir BST aleatorio
        valores = random.sample(range(100), random.randint(1, 20))
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
        p, q = random.choice(valores), random.choice(valores)
        assert lca_bst(arbol, p, q) == lca_referencia(arbol, p, q), \
            f" discrepa con p={p}, q={q}"

    # Casos base
    assert lca_bst(None, 1, 2) is None
    solo = Nodo(5)
    assert lca_bst(solo, 5, 5) == 5
    assert lca_bst(solo, 1, 9) == 5

    # El LCA es realmente ancestro de ambos
    l = lca_bst(raiz, 0, 9)
    assert l in camino_a(raiz, 0) and l in camino_a(raiz, 9)

    # Eficiencia: O(h), no O(n)
    import time
    bal = Nodo(500)
    def construir_balanceado(vals):
        if not vals:
            return None
        m = len(vals) // 2
        n = Nodo(vals[m])
        n.izquierdo = construir_balanceado(vals[:m])
        n.derecho = construir_balanceado(vals[m+1:])
        return n
    bal = construir_balanceado(list(range(1, 1025)))    # 1024 nodos
    print(f"\nBST balanceado de 1024 nodos, raíz = {bal.valor}:")
    print(f"  LCA(1, 1024) = {lca_bst(bal, 1, 1024)} (la raíz)")
    assert lca_bst(bal, 1, 1024) == bal.valor, "el LCA de los extremos es la raíz"
    assert lca_bst(bal, 1, 2) == 2, "1 es descendiente de 2"

    # El peor caso es log2(1024) = 10 comparaciones
    pasos = [0]

    def lca_contando(raiz, p, q):
        c = 0
        while raiz:
            c += 1
            if p < raiz.valor and q < raiz.valor:
                raiz = raiz.izquierdo
            elif p > raiz.valor and q > raiz.valor:
                raiz = raiz.derecho
            else:
                pasos[0] = c
                return raiz.valor
        return None

    lca_contando(bal, 1, 1024)
    print(f"  Comparaciones: {pasos[0]} (log₂1024 = 10)")
    assert pasos[0] <= 11

    print("\n✓ Todas las pruebas pasaron")
