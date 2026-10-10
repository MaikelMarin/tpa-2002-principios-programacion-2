r"""
Ejercicio 16: Árbol AVL
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - BST y el problema del desbalance (teoria.md §4.3).
    - Rotaciones y factor de balance (teoria.md §5).
    - Recursión y devolución de nodos (ejercicio insertar_bst.py).

PROBLEMA
   Implementar un BST que se mantiene balanceado tras cada operación,
   de modo que la altura sea siempre O(log n).

FONDO MATEMÁTICO
    El invariante del AVL: para todo nodo,
        BF(nodo) = altura(izq) − altura(der) ∈ {−1, 0, +1}

    Si una inserción rompe el invariante, se aplican ROTACIONES para
    restaurarlo. Hay cuatro casos, según dónde se produjo el
    desequilibrio:

        LL  (izquierda-izquierda)  → rotación derecha simple
        RR  (derecha-derecha)      → rotación izquierda simple
        LR  (izquierda-derecha)    → izquierda en el hijo, luego derecha
        RL  (derecha-izquierda)    → derecha en el hijo, luego izquierda

    Los casos simples LL y RR se resuelven con UNA rotación. Los casos
    dobles LR y RL necesitan DOS, porque el desequilibrio está en
    zigzag: primero se convierte el caso doble en simple, y luego se
    aplica la rotación simple.

¿POR QUÉ LAS ROTACIONES PRESERVAN EL BST?
    Una rotación derecha sobre y (con hijo izquierdo x):
        y                    x
       / \        →         / \
      x   T3               T1  y
     / \                      / \
    T1  T2                   T2  T3

    El inorden antes:  T1, x, T2, y, T3
    El inorden después: T1, x, T2, y, T3   ← ¡idéntico!

    Como el recorrido inorden no cambia, el conjunto de valores sigue
    en el mismo orden relativo, y la propiedad BST se conserva. Esto es
    lo que hace legítima cualquier rotación: reordena la ESTRUCTURA
    sin tocar el orden de los DATOS.

ESTRATEGIA DE IMPLEMENTACIÓN
    1. Insertar como en un BST normal (recursivo, bajando comparando).
    2. Al VOLVER de la recursión, actualizar la altura del nodo actual.
    3. Calcular el factor de balance.
    4. Si |BF| > 1, identificar el caso y rotar.

    El orden importa: hay que actualizar la altura ANTES de calcular
    el balance, porque el balance usa las alturas de los hijos.

    Identificación del caso (tras el desbalance en el nodo `n`):
        BF(n) > 1 y valor < n.izq.valor  →  LL  → rotar derecha
        BF(n) < -1 y valor > n.der.valor →  RR  → rotar izquierda
        BF(n) > 1 y valor > n.izq.valor  →  LR  → rotar izq en hijo, der en n
        BF(n) < -1 y valor < n.der.valor →  RL  → rotar der en hijo, izq en n

TRAZA DE UNA ROTACIÓN DERECHA (caso LL)
    Insertar 1, 2, 3 en orden. Sin balanceo:

        1              2              3
         \              \              \
          2       →      3      →       2
           \                                \
            3                                1
        alt=2          alt=2            alt=1 (rotado)

    Tras insertar 3, el BF de la raíz 1 es -2 → caso RR.
    Rotación izquierda sobre 1: el 2 sube, y queda balanceado.
    Inorden antes y después: [1, 2, 3]. Igual.

    Resultado final:
          2
         / \
        1   3      altura 1, BF(2)=0

COMPLEJIDAD
    Inserción: O(log n). Bajar cuesta O(log n) porque el árbol está
    balanceado; las rotaciones en el camino de vuelta cuestan O(1)
    (como máximo una doble o dos simples).

    Espacio: O(log n) de pila de recursión.

    Búsqueda: O(log n) GARANTIZADO, no solo en promedio. Esta es la
    diferencia clave con un BST sin balancear.

DEMOSTRACIÓN DE CORRECCIÓN DEL BALANCEO
    Cota de altura: sea N(h) el mínimo número de nodos en un AVL de
    altura h. Se cumple:
        N(0)=1, N(1)=2, N(h) = N(h-1) + N(h-2) + 1
    que es la recurrencia de Fibonacci. Luego N(h) crece al menos
    como φ^h, y por tanto h = O(log n). Más precisamente
    h ≤ 1.44 · log₂(n+1).

    Esto es lo que garantiza las O(log n) de TODAS las operaciones. ∎
"""


class Nodo:
    """Nodo de árbol AVL: almacena también su altura."""

    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 1              # la hoja tiene altura 1


class ArbolAVL:
    """Árbol binario de búsqueda auto-balanceado (AVL)."""

    def __init__(self):
        self.raiz = None

    # ---------- API pública ----------

    def insertar(self, valor):
        """Inserta un valor y rebalancea si es necesario."""
        self.raiz = self._insertar(self.raiz, valor)

    def buscar(self, valor):
        """Búsqueda normal de BST: O(log n) garantizado."""
        return self._buscar(self.raiz, valor)

    # ---------- Internos ----------

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _balance(self, nodo):
        """Factor de balance: altura(izq) − altura(der)."""
        if not nodo:
            return 0
        return self._altura(nodo.izquierdo) - self._altura(nodo.derecho)

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._altura(nodo.izquierdo),
                              self._altura(nodo.derecho))

    def _buscar(self, nodo, valor):
        if nodo is None or nodo.valor == valor:
            return nodo
        if valor < nodo.valor:
            return self._buscar(nodo.izquierdo, valor)
        return self._buscar(nodo.derecho, valor)

    # ---------- Rotaciones ----------

    def _rotacion_derecha(self, y):
        """Caso LL: y está desbalanceado a la izquierda.

            y              x
           / \            / \
          x   T3   →    T1  y
         / \               / \
        T1  T2            T2  T3
        """
        x = y.izquierdo
        t2 = x.derecho

        # Rotar
        x.derecho = y
        y.izquierdo = t2

        # Actualizar alturas: primero y (ahora es hijo), luego x
        self._actualizar_altura(y)
        self._actualizar_altura(x)

        return x                       # nueva raíz del subárbol

    def _rotacion_izquierda(self, x):
        """Caso RR: x está desbalanceado a la derecha.

          x                 y
         / \               / \
        T1  y     →       x   T3
           / \           / \
          T2 T3         T1 T2
        """
        y = x.derecho
        t2 = y.izquierdo

        # Rotar
        y.izquierdo = x
        x.derecho = t2

        # Actualizar alturas: primero x (ahora es hijo), luego y
        self._actualizar_altura(x)
        self._actualizar_altura(y)

        return y                       # nueva raíz del subárbol

    # ---------- Inserción con rebalanceo ----------

    def _insertar(self, nodo, valor):
        # 1. Inserción BST normal
        if nodo is None:
            return Nodo(valor)
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar(nodo.derecho, valor)
        else:
            return nodo                 # duplicado: no se inserta

        # 2. Actualizar la altura de este nodo (AHORA, al volver)
        self._actualizar_altura(nodo)

        # 3. Calcular el factor de balance
        balance = self._balance(nodo)

        # 4. Si está desbalanceado, hay 4 casos

        # Caso LL: una rotación derecha basta
        if balance > 1 and valor < nodo.izquierdo.valor:
            return self._rotacion_derecha(nodo)

        # Caso RR: una rotación izquierda basta
        if balance < -1 and valor > nodo.derecho.valor:
            return self._rotacion_izquierda(nodo)

        # Caso LR: rotar el hijo a la izquierda, luego el nodo a la derecha
        if balance > 1 and valor > nodo.izquierdo.valor:
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            return self._rotacion_derecha(nodo)

        # Caso RL: rotar el hijo a la derecha, luego el nodo a la izquierda
        if balance < -1 and valor < nodo.derecho.valor:
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            return self._rotacion_izquierda(nodo)

        return nodo                     # ya estaba balanceado


def inorden(nodo):
    """Recorrido inorden: devuelve los valores ordenados si es BST."""
    if nodo is None:
        return []
    return inorden(nodo.izquierdo) + [nodo.valor] + inorden(nodo.derecho)


def altura(nodo):
    """Altura en aristas."""
    if nodo is None:
        return -1
    return 1 + max(altura(nodo.izquierdo), altura(nodo.derecho))


if __name__ == "__main__":
    import math

    avl = ArbolAVL()

    # Insertar datos que degenerarían un BST normal
    for val in [10, 20, 30, 40, 50, 25]:
        avl.insertar(val)

    el = inorden(avl.raiz)
    assert el == sorted(el), "el inorden debe quedar ordenado"

    # El árbol debe quedar balanceado pese a insertar casi en orden
    assert altura(avl.raiz) <= 2, f"altura {altura(avl.raiz)} es excesiva"

    # La raíz es la mediana aproximada, NO el primer valor insertado
    assert avl.raiz.valor == 30, f"raíz debería ser 30, es {avl.raiz.valor}"

    # Búsqueda funciona
    assert avl.buscar(25) is not None
    assert avl.buscar(99) is None

    # El invariante AVL se cumple en todos los nodos
    def verificar_avl(nodo):
        if nodo is None:
            return True
        bf = altura(nodo.izquierdo) - altura(nodo.derecho)
        if abs(bf) > 1:
            return False
        return verificar_avl(nodo.izquierdo) and verificar_avl(nodo.derecho)

    assert verificar_avl(avl.raiz), "algún nodo viola el invariante AVL"

    # CASO LL: insertar en orden descendente
    avl_ll = ArbolAVL()
    for v in [30, 20, 10]:
        avl_ll.insertar(v)
    assert abs(altura(avl_ll.raiz.izquierdo) - altura(avl_ll.raiz.derecho)) <= 1
    assert avl_ll.raiz.valor == 20, "tras LL la raíz debe subir"

    # CASO RR: insertar en orden ascendente
    avl_rr = ArbolAVL()
    for v in [10, 20, 30]:
        avl_rr.insertar(v)
    assert avl_rr.raiz.valor == 20, "tras RR la raíz debe subir"

    # CASO LR y RL: zigzag
    avl_lr = ArbolAVL()
    for v in [30, 10, 20]:
        avl_lr.insertar(v)
    assert avl_lr.raiz.valor == 20, "tras LR la raíz debe ser la mediana"

    avl_rl = ArbolAVL()
    for v in [10, 30, 20]:
        avl_rl.insertar(v)
    assert avl_rl.raiz.valor == 20, "tras RL la raíz debe ser la mediana"

    # VERIFICACIÓN DE LA COTA: altura <= 1.44·log2(n)
    avl_grande = ArbolAVL()
    import random
    random.seed(9)
    datos = list(range(500))
    random.shuffle(datos)
    for v in datos:
        avl_grande.insertar(v)

    h = altura(avl_grande.raiz)
    n = 500
    cota = 1.44 * math.log2(n + 1)
    print(f"n={n}, altura={h}, cota teórica={cota:.1f}")
    assert h <= cota, "se violó la cota de altura del AVL"
    assert verificar_avl(avl_grande.raiz)

    # El inorden de un árbol grande sigue ordenado
    el = inorden(avl_grande.raiz)
    assert el == sorted(el)

    # Comparación con BST degenerado
    class BSTSimple:
        def __init__(self):
            self.raiz = None
        def insertar(self, valor):
            self.raiz = self._ins(self.raiz, valor)
        def _ins(self, nodo, valor):
            if nodo is None:
                return Nodo(valor)
            if valor < nodo.valor:
                nodo.izquierdo = self._ins(nodo.izquierdo, valor)
            else:
                nodo.derecho = self._ins(nodo.derecho, valor)
            return nodo

    bst = BSTSimple()
    for v in range(200):
        bst.insertar(v)
    print(f"\nInserción ordenada de 200 elementos:")
    print(f"  BST normal:  altura {altura(bst.raiz)}")
    print(f"  AVL:         altura {altura(avl_grande.raiz)} (con 500 elementos)")
    assert altura(bst.raiz) == 199, "BST degenerado: altura n-1"

    print("\n✓ Todas las pruebas pasaron")
