r"""
Ejercicio 7: Eliminación en BST
Dificultad: Avanzado

CONOCIMIENTO PREVIO NECESARIO
    - Inserción en BST (ejercicio insertar_bst.py).
    - Invariante BST y el concepto de sucesor inorden (teoria.md §4.2).
    - Referencias a objetos (00-fundamentos §9.2): devolver nodos es
      la forma de modificar el árbol del llamador.

PROBLEMA
    Eliminar un valor de un BST manteniendo la invariante
    izquierdo < raíz < derecho.

ESTRATEGIA: LOS TRES CASOS
    Localizar el nodo bajando por comparaciones (como en búsqueda).
    Una vez encontrado, hay tres situaciones distintas:

    CASO 1 — El nodo es una HOJA (sin hijos):
        Simplemente eliminarlo. El padre apunta a None.

    CASO 2 — El nodo tiene UN solo hijo:
        Reemplazarlo por ese hijo. El hijo "hereda" la posición:
        todo el subárbol del hijo es mayor que todo el subárbol
        izquierdo del padre y menor que todo el derecho, así que la
        invariante se preserva.

    CASO 3 — El nodo tiene DOS hijos:
        No se puede promover a ninguno de los dos directamente.
        La solución: copiar el valor del SUCESOR INORDEN (el mínimo
        del subárbol derecho) en el nodo actual, y luego eliminar ese
        sucesor del subárbol derecho.

¿POR QUÉ EL SUCESOR INORDEN Y NO OTRO VALOR?
    El sucesor inorden S es el valor más pequeño del subárbol derecho.
    Tres hechos lo hacen el reemplazo correcto:
      1. S > todo el subárbol izquierdo del nodo eliminado
         (porque S está en el derecho, y el derecho es mayor).
      2. S < todo el resto del subárbol derecho
         (porque S es el MÍNIMO de ese subárbol).
      3. Eliminar a S del subárbol derecho es fácil: S no tiene hijo
         izquierdo (es el mínimo), así que es caso 1 o caso 2.

    Juntos, 1 y 2 garantizan que al copiar el valor de S en la raíz,
    la invariante BST se mantiene. Y 3 garantiza que la eliminación
    recursiva termina rápido.

    El PREDECESOR inorden (máximo del subárbol izquierdo) funciona
    igual por simetría.

TRAZA DEL CASO 3
    Eliminar 8 de:
                8
               / \
              3   10
                 /  \
                9    14

    Paso 1: localizar 8. Tiene dos hijos.
    Paso 2: sucesor inorden = mínimo del subárbol derecho (10)
            = 9 (bajando siempre por la izquierda desde 10).
    Paso 3: copiar el VALOR: la raíz ahora vale 9.
    Paso 4: eliminar el 9 del subárbol derecho.

    Resultado:
                9
               / \
              3   10
                    \
                    14

    Verificación: inorden = [3, 9, 10, 14] — ordenado. Invariante OK.

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción sobre la altura.

    Caso base: eliminar en un árbol vacío devuelve None. Correcto.

    Hipótesis: eliminar preserva la propiedad BST en subárboles de
    altura < h.

    Paso: para el nodo n con valor a eliminar,
      - Si n no tiene el valor buscado, se recurre sobre uno de sus
        subárboles (menor altura) y por hipótesis queda BST; la raíz
        no cambia, así que la invariante global se preserva.
      - Caso 1 (hoja): eliminar no afecta al resto.
      - Caso 2 (un hijo): el hijo ocupa la posición; por el argumento
        de herencia de rango, la invariante se preserva.
      - Caso 3: el sucesor S satisface las tres propiedades de arriba.
        Copiar su valor y eliminarlo (caso 1 o 2 en el subárbol
        derecho, recursión sobre algo más pequeño) mantiene todo. ∎

COMPLEJIDAD
    Tiempo: O(h). Bajar hasta el nodo (O(h)) y, en el caso 3, bajar
    hasta el sucesor (O(h)).
    Espacio: O(h) de pila. La versión iterativa usa O(1).

    En BST balanceado: O(log n). En degenerado: O(n).

CASOS LÍMITE
    - Eliminar la raíz cuando es el único nodo → árbol vacío.
    - Eliminar la raíz con dos hijos (el caso 3 más visible).
    - Eliminar un valor inexistente → el árbol no cambia.
    - Eliminar del árbol vacío → devuelve None.
"""


class Nodo:
    """Nodo de un árbol binario."""

    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def minimo(nodo):
    """Devuelve el nodo con el valor mínimo del subárbol.

    Es el sucesor inorden: el más a la izquierda posible.
    """
    while nodo.izquierdo:
        nodo = nodo.izquierdo
    return nodo


def maximo(nodo):
    """Devuelve el nodo con el valor máximo (predecesor inorden)."""
    while nodo.derecho:
        nodo = nodo.derecho
    return nodo


def eliminar(raiz, valor):
    """Elimina un valor del BST. Devuelve la raíz resultante.

    Maneja los tres casos: hoja, un hijo, dos hijos.
    """
    if raiz is None:
        return None                              # caso base

    # Bajar buscando el nodo
    if valor < raiz.valor:
        raiz.izquierdo = eliminar(raiz.izquierdo, valor)
    elif valor > raiz.valor:
        raiz.derecho = eliminar(raiz.derecho, valor)
    else:
        # --- Nodo encontrado ---

        # Caso 1 y 2: sin hijo izquierdo, o sin ninguno
        if raiz.izquierdo is None:
            return raiz.derecho

        # Caso 2: sin hijo derecho
        if raiz.derecho is None:
            return raiz.izquierdo

        # Caso 3: dos hijos → usar el sucesor inorden
        sucesor = minimo(raiz.derecho)
        raiz.valor = sucesor.valor               # copiar el valor
        raiz.derecho = eliminar(raiz.derecho, sucesor.valor)  # borrar el sucesor

    return raiz


def insertar(raiz, valor):
    """Inserta un valor en el BST (necesario para construir los tests)."""
    if raiz is None:
        return Nodo(valor)
    if valor < raiz.valor:
        raiz.izquierdo = insertar(raiz.izquierdo, valor)
    elif valor > raiz.valor:
        raiz.derecho = insertar(raiz.derecho, valor)
    return raiz


def buscar(nodo, valor):
    """Busca un valor. Devuelve True si está."""
    if nodo is None:
        return False
    if nodo.valor == valor:
        return True
    if valor < nodo.valor:
        return buscar(nodo.izquierdo, valor)
    return buscar(nodo.derecho, valor)


def inorden(nodo):
    """Recorrido inorden. En un BST devuelve los valores ordenados."""
    if nodo is None:
        return []
    return inorden(nodo.izquierdo) + [nodo.valor] + inorden(nodo.derecho)


def altura(nodo):
    """Altura del árbol en aristas."""
    if nodo is None:
        return -1
    return 1 + max(altura(nodo.izquierdo), altura(nodo.derecho))


def es_bst_valido(nodo, minimo_v=float('-inf'), maximo_v=float('inf')):
    """Verifica la invariante BST propagando límites."""
    if nodo is None:
        return True
    if not (minimo_v < nodo.valor < maximo_v):
        return False
    return (es_bst_valido(nodo.izquierdo, minimo_v, nodo.valor) and
            es_bst_valido(nodo.derecho, nodo.valor, maximo_v))


if __name__ == "__main__":
    # Construir el árbol de prueba
    raiz = None
    for val in [8, 3, 10, 1, 6, 14]:
        raiz = insertar(raiz, val)

    # --- CASO 1: eliminar una hoja (el 1) ---
    raiz = eliminar(raiz, 1)
    assert buscar(raiz, 1) is False
    assert buscar(raiz, 3) is True, "el padre debe quedar intacto"
    assert es_bst_valido(raiz), "invariante rota tras caso 1"

    # --- CASO 2: eliminar nodo con un solo hijo (el 14) ---
    raiz = insertar(raiz, 13)                # 14 gana hijo izquierdo
    raiz = eliminar(raiz, 14)                # tenía un hijo
    assert buscar(raiz, 14) is False
    assert buscar(raiz, 13) is True, "el hijo debe ocupar la posición"
    assert es_bst_valido(raiz), "invariante rota tras caso 2"

    # --- CASO 3: eliminar nodo con dos hijos (el 10) ---
    raiz = eliminar(raiz, 10)
    assert buscar(raiz, 10) is False
    assert buscar(raiz, 13) is True
    assert buscar(raiz, 6) is True, "el resto del árbol debe quedar intacto"
    assert inorden(raiz) == sorted(inorden(raiz)), "inorden desordenado"
    assert es_bst_valido(raiz), "invariante rota tras caso 3"

    # --- Eliminar la RAÍZ con dos hijos ---
    raiz = eliminar(raiz, 8)
    assert buscar(raiz, 8) is False
    assert es_bst_valido(raiz)
    assert inorden(raiz) == sorted(inorden(raiz))

    # La nueva raíz debe ser el sucesor inorden del 8, que era el 13
    assert raiz.valor == 13, f"raíz debería ser 13, es {raiz.valor}"

    # --- Casos límite ---
    # Eliminar valor inexistente: el árbol no cambia
    antes = inorden(raiz)
    raiz = eliminar(raiz, 999)
    assert inorden(raiz) == antes, "eliminar inexistente no debe cambiar nada"

    # Eliminar del árbol vacío
    assert eliminar(None, 5) is None

    # Eliminar hasta dejar el árbol vacío
    while raiz is not None:
        raiz = eliminar(raiz, raiz.valor)
    assert raiz is None, "el árbol debería quedar vacío"

    # Eliminar la raíz de un árbol de un solo nodo
    unico = insertar(None, 42)
    unico = eliminar(unico, 42)
    assert unico is None

    print("✓ Todas las pruebas pasaron")
