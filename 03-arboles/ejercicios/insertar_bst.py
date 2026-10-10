r"""
Ejercicio 6: Inserción en BST
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - BST y su invariante (teoria.md §4.1).
    - Recursión sobre árboles (tema 01): el caso base es el subárbol nulo.
    - Referencias a objetos (00-fundamentos §9.2): reasignar `raiz`
      modifica el árbol del llamador.

PROBLEMA
    Insertar un valor en un BST manteniendo la invariante
    izquierdo < raíz < derecho.

ESTRATEGIA
    La inserción siempre ocurre en una HOJA. Bajar comparando:

      1. Si el subárbol está vacío (nodo is None), aquí va el nuevo
         nodo: devolver Nodo(valor).
      2. Si valor < nodo.valor, insertar en el subárbol izquierdo.
      3. Si valor > nodo.valor, insertar en el subárbol derecho.
      4. Si valor == nodo.valor, no hacer nada (no se permiten
         duplicados en esta implementación).

    Observe que la función DEVUELVE el nodo. Esto es clave: cuando se
    llega a una posición vacía, el nuevo nodo se devuelve y el padre
    lo asigna a su hijo izquierdo o derecho. Por eso la firma es
    `insertar(raiz, valor) -> raiz` y no una modificación in-place.

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción sobre la altura del subárbol.

    Caso base: nodo es None. Se devuelve un nodo hoja con el valor;
    un árbol de un nodo es trivialmente BST.

    Hipótesis: insertar en cualquier subárbol de altura < h preserva
    la propiedad BST.

    Paso: sea T de altura h con raíz r.
      - Si valor < r: por hipótesis, insertar(T.izq) da un BST. Como
        valor < r, poner ese BST a la izquierda mantiene la invariante.
      - Si valor > r: análogo por la derecha.
      - Si valor == r: no se modifica; la invariante ya se cumplía.

    En todos los casos el resultado es un BST. ∎

COMPLEJIDAD
    Tiempo: O(h). En BST balanceado O(log n); en degenerado O(n).
    Espacio: O(h) de pila de recursión.

    La versión iterativa usa O(1) de espacio:

```python
def insertar_iterativo(raiz, valor):
    nuevo = Nodo(valor)
    if raiz is None:
        return nuevo
    actual = raiz
    while True:
        if valor < actual.valor:
            if actual.izquierdo is None:
                actual.izquierdo = nuevo
                break
            actual = actual.izquierdo
        elif valor > actual.valor:
            if actual.derecho is None:
                actual.derecho = nuevo
                break
            actual = actual.derecho
        else:
            break                  # duplicado: no se inserta
    return raiz
```

TRAZA de insertar(raiz=8, valor=3) sobre el árbol:
            8                →  3 < 8, bajar a la izquierda
           / \                     |
          3   10                  3 < 8 repetido
         / \   \              →  no hacer nada
        1   6   14

    insertar(raiz=8, valor=12):
            8                →  12 > 8, bajar a la derecha
           / \                     |
          3   10                  12 > 10, bajar a la derecha
         / \   \                       |
        1   6   14                    14.derecho es None → insertar aquí
                 \
                 12

POLÍTICA ANTE DUPLICADOS
    Esta implementación los RECHAZA. Las alternativas son:
      - Permitirlos siempre a la derecha (o siempre a la izquierda):
        el BST sigue siendo válido, pero las operaciones se
        desbalancean si todos los duplicados van al mismo lado.
      - Llevar un contador en el nodo: más compacto, pero complica
        la eliminación.
    Rechazar es lo más simple y suficiente para este curso.

RELACIÓN CON OTROS TEMAS
    La misma estructura "bajar comparando" aparece en la búsqueda
    binaria sobre arreglos (tema 02). La diferencia: aquí no hay
    índices, hay punteros, y no se puede acceder al "medio" en O(1),
    por eso el árbol es la alternativa cuando se necesitan
    inserciones frecuentes.
"""


class Nodo:
    """Nodo de un árbol binario."""

    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def inorden(nodo):
    """Recorrido inorden. Devuelve una lista ordenada si es BST."""
    if nodo is None:
        return []
    return inorden(nodo.izquierdo) + [nodo.valor] + inorden(nodo.derecho)


def altura(nodo):
    """Altura del árbol (aristas). -1 si está vacío."""
    if nodo is None:
        return -1
    return 1 + max(altura(nodo.izquierdo), altura(nodo.derecho))


def insertar(raiz, valor):
    """Inserta un valor en el BST. Devuelve la raíz (posiblemente nueva).

    Recurrencia: T(h) = T(h-1) + O(1) → O(h).
    """
    if raiz is None:
        return Nodo(valor)                    # caso base: hoja nueva

    if valor < raiz.valor:
        raiz.izquierdo = insertar(raiz.izquierdo, valor)
    elif valor > raiz.valor:
        raiz.derecho = insertar(raiz.derecho, valor)
    # valor == raiz.valor: no se hace nada (sin duplicados)

    return raiz


def insertar_iterativo(raiz, valor):
    """Versión iterativa: O(1) de espacio en vez de O(h) de pila."""
    nuevo = Nodo(valor)
    if raiz is None:
        return nuevo

    actual = raiz
    while True:
        if valor < actual.valor:
            if actual.izquierdo is None:
                actual.izquierdo = nuevo
                break
            actual = actual.izquierdo
        elif valor > actual.valor:
            if actual.derecho is None:
                actual.derecho = nuevo
                break
            actual = actual.derecho
        else:
            break                            # duplicado
    return raiz


def buscar(nodo, valor):
    """Busca un valor en el BST. Devuelve el nodo o None."""
    if nodo is None or nodo.valor == valor:
        return nodo
    if valor < nodo.valor:
        return buscar(nodo.izquierdo, valor)
    return buscar(nodo.derecho, valor)


if __name__ == "__main__":
    # Construir el árbol de ejemplo: raíz 8
    raiz = None
    for val in [8, 3, 10, 1, 6, 14]:
        raiz = insertar(raiz, val)

    # Inserción simple
    raiz = insertar(raiz, 7)
    assert buscar(raiz, 7) is not None, "7 debería estar"
    assert buscar(raiz, 7).derecho is None, "7 es hoja"

    # Árbol completo correcto
    assert buscar(raiz, 8) is not None
    assert buscar(raiz, 3) is not None
    assert buscar(raiz, 14) is not None
    assert buscar(raiz, 99) is None, "99 no fue insertado"

    # La versión iterativa da el mismo resultado que la recursiva
    raiz_it = None
    for val in [8, 3, 10, 1, 6, 14, 7]:
        raiz_it = insertar_iterativo(raiz_it, val)
    assert inorden(raiz) == inorden(raiz_it), "ambas versiones deben coincidir"

    # Casos base
    r = insertar(None, 5)                  # árbol vacío
    assert r.valor == 5
    assert r.izquierdo is None and r.derecho is None

    r = insertar(r, 5)                     # duplicado: no cambia nada
    assert r.valor == 5 and r.izquierdo is None and r.derecho is None

    r = insertar(r, 3)                     # va a la izquierda
    assert r.izquierdo.valor == 3

    r = insertar(r, 7)                     # va a la derecha
    assert r.derecho.valor == 7

    # Insertar datos ordenados → árbol degenerado (altura n)
    degenerado = None
    for val in [1, 2, 3, 4, 5]:
        degenerado = insertar(degenerado, val)
    assert altura(degenerado) == 4, "degenerado: altura = n-1"

    # Insertar equilibrado → altura log n
    equilibrado = None
    for val in [4, 2, 6, 1, 3, 5, 7]:
        equilibrado = insertar(equilibrado, val)
    assert altura(equilibrado) == 2, "perfecto: altura 2"

    print("✓ Todas las pruebas pasaron")
