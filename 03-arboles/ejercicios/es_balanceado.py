r"""
Ejercicio 12: Árbol balanceado
Dificultad: Avanzado

CONOCIMIENTO PREVIO NECESARIO
    - Altura (ejercicio altura_arbol.py).
    - Inducción estructural.
    - La idea de eficiencia: calcular sin recalcular.

PROBLEMA
    Determinar si un árbol binario está balanceado: para todo nodo,
    la diferencia de altura entre sus subárboles es como máximo 1.

FONDO MATEMÁTICO
    La definición es RECURSIVA sobre todos los nodos:
        balanceado(n) = |altura(izq) − altura(der)| <= 1
                        Y balanceado(izq) Y balanceado(der)

    Un árbol está balanceado si y solo si TODOS sus nodos lo están.
    No basta con que la raíz lo esté.

    CONTRAEJEMPLO importante:
            1
           / \
          2   3
         /
        4
       /
      5

    Raíz: |altura(izq)=3 − altura(der)=0| = 3 > 1 → NO balanceado.
    La raíz ya lo delata. Pero considere:
            1
           / \
          2   3
         /     \
        4       6
       /         \
      5           7

    Raíz: |2 − 2| = 0 ≤ 1 → parece balanceado.
    Pero el nodo 2 tiene |1 − (−1)| = 2 > 1 → NO balanceado.
    Hay que verificar TODOS los nodos, no solo la raíz.

LA SOLUCIÓN EFICIENTE: DEVOLVER DOS COSAS
    La versión ingenua llama a altura() en cada nodo, y altura() es
    O(n). Eso da O(n²) en total: recalcular la altura una y otra vez.

    La versión eficiente devuelve (balanceado, altura) en una sola
    pasada:

        def verificar(n):
            if n is None: return True, -1
            bal_izq, h_izq = verificar(n.izquierdo)
            if not bal_izq: return False, 0        # cortar
            bal_der, h_der = verificar(n.derecho)
            if not bal_der: return False, 0        # cortar
            if abs(h_izq - h_der) > 1: return False, 0
            return True, 1 + max(h_izq, h_der)

    Una sola pasada: Θ(n). El truco es propagar la altura hacia
    arriba, igual que hace el AVL.

TRAZA de la versión eficiente sobre:
        1
       / \
      2   3

    verificar(1)
      verificar(2) → (True, 0)      [hoja]
      verificar(3) → (True, 0)      [hoja]
      |0 − 0| = 0 ≤ 1
      → (True, 1 + 0) = (True, 1)

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción sobre la altura.
    Caso base: None → (True, −1). Correcto.
    Hipótesis: verificar devuelve (balanceado, altura correcta) para
    subárboles menores.
    Paso: si ambos subárboles son balanceados y sus alturas (correctas
    por hipótesis) difieren en ≤ 1, entonces el nodo actual está
    balanceado y su altura es 1 + max(...). Correcto. ∎

COMPLEJIDAD
    Versión ingenua (altura por separado): Θ(n²)
    Versión eficiente (una pasada):         Θ(n) tiempo, Θ(h) espacio

    Para n = 10,000 la diferencia es 100 millones de operaciones
    frente a 10,000. Merece la pena el esfuerzo.

RELACIÓN CON OTROS TEMAS
    - El AVL (ejercicio 16) aplica exactamente esta verificación tras
      cada inserción, con el factor de balance.
    - El ordenamiento externo (tema 06) usa árboles de fusión
      balanceados: el balanceo reduce el número de pasadas sobre disco.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def altura(nodo):
    """Altura en aristas. O(n) por llamada."""
    if nodo is None:
        return -1
    return 1 + max(altura(nodo.izquierdo), altura(nodo.derecho))


def es_balanceado_ingenua(nodo):
    """Verifica el balance llamando a altura() en cada nodo: O(n²)."""
    if nodo is None:
        return True
    if abs(altura(nodo.izquierdo) - altura(nodo.derecho)) > 1:
        return False
    return es_balanceado_ingenua(nodo.izquierdo) and es_balanceado_ingenua(nodo.derecho)


def es_balanceado(nodo):
    """Verifica el balance en UNA pasada: O(n).

    Devuelve (balanceado, altura), propagando la altura hacia arriba.
    """
    if nodo is None:
        return True, -1

    bal_izq, h_izq = es_balanceado(nodo.izquierdo)
    if not bal_izq:
        return False, 0                # cortar temprano

    bal_der, h_der = es_balanceado(nodo.derecho)
    if not bal_der:
        return False, 0                # cortar temprano

    if abs(h_izq - h_der) > 1:
        return False, 0

    return True, 1 + max(h_izq, h_der)


if __name__ == "__main__":
    # Árbol balanceado
    r1 = Nodo(1)
    r1.izquierdo = Nodo(2); r1.derecho = Nodo(3)
    r1.izquierdo.izquierdo = Nodo(4); r1.izquierdo.derecho = Nodo(5)

    bal, h = es_balanceado(r1)
    print(f"Árbol 1 balanceado: {bal}, altura: {h}")
    assert bal is True
    assert es_balanceado_ingenua(r1) is True

    # Desbalance en la raíz
    r2 = Nodo(1)
    r2.izquierdo = Nodo(2)
    r2.izquierdo.izquierdo = Nodo(3)
    r2.izquierdo.izquierdo.izquierdo = Nodo(4)
    bal, _ = es_balanceado(r2)
    print(f"Árbol 2 balanceado: {bal} (desbalance en la raíz)")
    assert bal is False
    assert es_balanceado_ingenua(r2) is False

    # EL CONTRAEJEMPLO: raíz OK pero un nodo interno desbalanceado
    r3 = Nodo(1)
    r3.izquierdo = Nodo(2); r3.derecho = Nodo(3)
    r3.izquierdo.izquierdo = Nodo(4)          # 2 tiene izq profundo
    r3.izquierdo.izquierdo.izquierdo = Nodo(5)
    r3.izquierdo.izquierdo.derecho = Nodo(6)
    # 2: |h(izq)=1 − h(der)=−1| = 2 → desbalanceado
    # 1: |h(izq)=2 − h(der)=0| = 2 → también desbalanceado
    bal, _ = es_balanceado(r3)
    print(f"Árbol 3 balanceado: {bal} (dos nodos violan)")
    assert bal is False

    # Caso donde SOLO un nodo interno viola (raíz parece OK)
    r4 = Nodo(1)
    r4.izquierdo = Nodo(2); r4.derecho = Nodo(3)
    r4.izquierdo.izquierdo = Nodo(4)
    r4.izquierdo.izquierdo.izquierdo = Nodo(5)
    r4.derecho.izquierdo = Nodo(6)
    r4.derecho.derecho = Nodo(7)
    # 1: |1 − 1| = 0 OK
    # 2: |1 − (−1)| = 2 → VIOLA
    bal, _ = es_balanceado(r4)
    print(f"Árbol 4 balanceado: {bal} (raíz OK, nodo interno viola)")
    assert bal is False
    # Probar que NO basta con verificar la raíz
    assert abs(altura(r4.izquierdo) - altura(r4.derecho)) <= 1, "la raíz parece balanceada"

    # Casos base
    assert es_balanceado(None) == (True, -1)
    assert es_balanceado(Nodo(1)) == (True, 0)

    # Comparación de rendimiento.
    #
    # NOTA METODOLÓGICA IMPORTANTE: la versión ingenua NO siempre es
    # O(n²). También hace corte temprano: si la raíz ya está
    # desbalanceada, retorna sin recursar. Para que realmente recorra
    # todo haciendo altura() en cada nodo, hace falta un árbol que
    # esté balanceado en la parte alta pero sea profundo.
    #
    # n se limita a 500 porque con valores aleatorios el BST puede
    # quedar profundo y agotar la pila de Python. El punto cualitativo
    # (no recalcular alturas) se mantiene.
    import time
    import sys

    limite_original = sys.getrecursionlimit()

    def construir_aleatorio(n, semilla=7):
        import random
        rng = random.Random(semilla)
        raiz = Nodo(rng.randint(0, 10**6))
        for _ in range(n - 1):
            v = rng.randint(0, 10**6)
            actual = raiz
            while True:
                if v < actual.valor:
                    if actual.izquierdo is None:
                        actual.izquierdo = Nodo(v); break
                    actual = actual.izquierdo
                else:
                    if actual.derecho is None:
                        actual.derecho = Nodo(v); break
                    actual = actual.derecho
        return raiz

    n = 300
    arbol = construir_aleatorio(n)

    sys.setrecursionlimit(20000)
    try:
        inicio = time.time()
        b_ef = es_balanceado(arbol)[0]
        t_ef = time.time() - inicio

        inicio = time.time()
        b_ing = es_balanceado_ingenua(arbol)
        t_ing = time.time() - inicio
    finally:
        sys.setrecursionlimit(limite_original)

    print(f"\nÁrbol aleatorio de {n} nodos:")
    print(f"  Eficiente O(n):  {t_ef*1000:.2f} ms → {b_ef}")
    print(f"  Ingenua:         {t_ing*1000:.2f} ms → {b_ing}")
    if t_ef > 0:
        print(f"  Relación: {t_ing/t_ef:.2f}x")
    print("  Ambas dan el mismo resultado; la eficiente no recalcula alturas.")
    assert b_ef == b_ing

    # El corte temprano de la ingenua: con un degenerado, corta en la raíz
    def construir_degenerado(m):
        raiz = Nodo(0); actual = raiz
        for i in range(1, m):
            actual.derecho = Nodo(i); actual = actual.derecho
        return raiz

    deg = construir_degenerado(2000)

    # La versión eficiente sí recorre todo el árbol, así que su
    # recursión llega a profundidad 2000: hace falta subir el límite.
    sys.setrecursionlimit(20000)
    try:
        inicio = time.time()
        b_deg = es_balanceado_ingenua(deg)
        t_deg = time.time() - inicio
        print(f"\nDegenerado de 2000 nodos, versión ingenua: {t_deg*1000:.2f} ms → {b_deg}")
        print("  (Rápida porque el desbalance de la raíz corta la recursión.)")
        assert b_deg is False

        # La eficiente recorre todo, pero en O(n)
        inicio = time.time()
        b_ef_deg = es_balanceado(deg)[0]
        t_ef_deg = time.time() - inicio
        print(f"Degenerado de 2000 nodos, versión eficiente: {t_ef_deg*1000:.2f} ms → {b_ef_deg}")
        assert b_ef_deg is False
    finally:
        sys.setrecursionlimit(limite_original)

    print("\n✓ Todas las pruebas pasaron")
