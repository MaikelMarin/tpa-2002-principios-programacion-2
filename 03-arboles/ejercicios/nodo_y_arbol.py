r"""
Ejercicio 1: Nodo y Árbol Binario
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Clases y referencias (00-fundamentos §9.2, §10.1).
    - Listas enlazadas (§8.3): un árbol es una lista enlazada con dos
      referencias por nodo en vez de una.

PROBLEMA
    Implementar la estructura básica: un nodo con valor y dos hijos,
    y un árbol que permite insertar y buscar.

ESTRATEGIA
    La estructura mínima de un árbol binario:

```python
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None      # referencia, no objeto
        self.derecho = None
```

    Puntos que causan errores si no se tienen claros:
      - `self.izquierdo = None` crea una REFERENCIA nula. El nodo hijo
        solo existe cuando se asigna `Nodo(...)`. No se crea solo.
      - Dos variables pueden apuntar al MISMO nodo. Modificar una
        modifica el árbol completo (§9.2).
      - `__repr__` es lo que se muestra al imprimir; definirlo ahorra
        depurar a ciegas.

    El árbol envuelve la raíz:

```python
class ArbolBinario:
    def __init__(self, raiz=None):
        self.raiz = raiz
```

TRAZA DE CONSTRUCCIÓN
    arbol = ArbolBinario()          raiz = None
    arbol.insertar(5)               raiz = Nodo(5)
    arbol.insertar(3)               3 < 5 → raiz.izquierdo = Nodo(3)
    arbol.insertar(8)               8 > 5 → raiz.derecho = Nodo(8)

    Estructura resultante:
            5
           / \
          3   8

    Observe que insertar sobre un árbol vacío CAMBIA la raíz. Por eso
    `insertar` no puede ser un método que solo modifique nodos: tiene
    que poder reemplazar `self.raiz`.

DEMOSTRACIÓN DE CORRECCIÓN (de la búsqueda)
    La búsqueda baja comparando. Si el árbol es un BST (invariante),
    cada comparación descarta la mitad, así que encuentra el valor o
    llega a None.

    Nota: esta implementación NO aplica la invariante BST al insertar,
    solo coloca a la izquierda si es menor. En la práctica se usa el
    ejercicio insertar_bst.py.

COMPLEJIDAD
    Inserción: O(h). Búsqueda: O(h).
    Espacio: O(1) por operación (sin contar la recursión).

RELACIÓN CON OTROS TEMAS
    - Grafos (tema 04): un árbol es un grafo acíclico y conexo. La
      lista de adyacencia puede representar un árbol.
    - Archivos (tema 05): la serialización de árboles (ejercicio 20)
      usa exactamente esta estructura.
"""


class Nodo:
    """Nodo de árbol binario: valor + dos referencias a hijos."""

    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


class ArbolBinario:
    """Árbol binario con inserción y búsqueda simples."""

    def __init__(self, raiz=None):
        self.raiz = raiz

    def insertar(self, valor):
        """Inserta un valor. Si el árbol está vacío, crea la raíz."""
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        # Convención: menores a la izquierda, mayores o iguales a la derecha
        if valor < nodo.valor:
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.izquierdo, valor)
        else:
            if nodo.derecho is None:
                nodo.derecho = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.derecho, valor)

    def buscar(self, valor):
        """Busca un valor. Devuelve True si está."""
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return False
        if nodo.valor == valor:
            return True
        if valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierdo, valor)
        return self._buscar_recursivo(nodo.derecho, valor)

    def __repr__(self):
        return f"ArbolBinario(raiz={self.raiz})"


def inorden(nodo):
    """Recorrido inorden. Útil para inspeccionar el árbol."""
    if nodo is None:
        return []
    return inorden(nodo.izquierdo) + [nodo.valor] + inorden(nodo.derecho)


def altura(nodo):
    """Altura en aristas."""
    if nodo is None:
        return -1
    return 1 + max(altura(nodo.izquierdo), altura(nodo.derecho))


if __name__ == "__main__":
    arbol = ArbolBinario()

    # Árbol vacío
    assert arbol.raiz is None
    assert arbol.buscar(5) is False

    # Construcción
    for val in [5, 3, 7, 1, 4, 6, 8]:
        arbol.insertar(val)

    print(f"Inorden: {inorden(arbol.raiz)}")
    print(f"Altura:  {altura(arbol.raiz)}")

    # La raíz se creó correctamente
    assert arbol.raiz is not None
    assert arbol.raiz.valor == 5

    # Búsqueda
    assert arbol.buscar(5) is True, "la raíz debe encontrarse"
    assert arbol.buscar(1) is True
    assert arbol.buscar(8) is True
    assert arbol.buscar(10) is False, "no fue insertado"

    # Estructura correcta
    assert arbol.raiz.izquierdo.valor == 3
    assert arbol.raiz.derecho.valor == 7
    assert arbol.raiz.izquierdo.izquierdo.valor == 1
    assert arbol.raiz.derecho.derecho.valor == 8

    # Las hojas no tienen hijos
    assert arbol.raiz.izquierdo.izquierdo.izquierdo is None
    assert arbol.raiz.izquierdo.izquierdo.derecho is None

    # Inorden ordenado: es un BST válido
    assert inorden(arbol.raiz) == sorted(inorden(arbol.raiz))

    # Insertar duplicado (va a la derecha por la convención)
    arbol.insertar(4)
    assert arbol.raiz.izquierdo.derecho.valor == 4
    assert arbol.raiz.izquierdo.derecho.derecho is not None, "el duplicado fue a la derecha"

    # El duplicado añade un nivel: la altura pasa de 2 a 3
    assert altura(arbol.raiz) == 3, "el duplicado insertado a la derecha profundiza el árbol"

    # Inorden sigue ordenado (con el duplicado)
    assert inorden(arbol.raiz) == sorted(inorden(arbol.raiz))

    print("✓ Todas las pruebas pasaron")
