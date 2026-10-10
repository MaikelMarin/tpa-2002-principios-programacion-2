r"""
Ejercicio 20: Serializar y deserializar BST
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - Recorrido preorden (teoria.md §3.1).
    - Reconstrucción de árboles desde recorridos (§3.4).
    - BST y su invariante (teoria.md §4.1).

PROBLEMA
    Convertir un BST a una cadena de texto y reconstruirlo desde ella.

¿PARA QUÉ SIRVE?
    - Enviar un árbol por red o guardarlo en disco.
    - Cachear estructuras entre sesiones.
    - Depurar: ver la estructura completa en un formato compacto.

FONDO MATEMÁTICO: ¿QUÉ RECORRIDO BASTA?
    De la sección 3.4: para reconstruir un árbol binario arbitrario
    hacen falta DOS recorridos, salvo que se marquen los nulos.

    Pero un BST tiene MÁS información: su invariante. Por eso el
    PREORDEN BASTO, sin marcar nulos:

        preorden = [8, 3, 1, 6, 4, 7, 10, 14, 13]

    ¿Por qué funciona? En el preorden, el primer elemento es la raíz.
    Los siguientes elementos menores que la raíz forman el subárbol
    IZQUIERDO, y los mayores el DERECHO — y esa división es única
    porque el BST está ordenado.

    Sin la invariante BST, [8, 3, 1, 6, ...] no permitiría saber si
    el 3 es hijo izquierdo o derecho del 8. Con la invariante, sí.

ESTRATEGIA DE SERIALIZACIÓN
    Recorrido preorden, guardando los valores separados por comas:

```python
def serializar(raiz):
    valores = []
    def preorden(n):
        if not n:
            return
        valores.append(str(n.valor))
        preorden(n.izquierdo)
        preorden(n.derecho)
    preorden(raiz)
    return ",".join(valores)
```

ESTRATEGIA DE DESERIALIZACIÓN
    1. Convertir la cadena a una lista de enteros.
    2. El primer elemento es la raíz.
    3. Encontrar el índice donde los valores dejan de ser menores que
       la raíz: ahí empieza el subárbol derecho.
    4. Recursar sobre cada mitad.

    La búsqueda del punto de corte se hace en O(n) recorriendo la
    lista, así que la reconstrucción completa es O(n²) en el peor
    caso (árbol degenerado). Con una cola y límites se logra O(n),
    pero la versión simple es más fácil de entender.

TRAZA COMPLETA
    Árbol:
            8
           / \
          3   10
         / \    \
        1   6    14
           /
          4

    Preorden: 8, 3, 1, 6, 4, 10, 14
    Serializado: "8,3,1,6,4,10,14"

    Deserializar "8,3,1,6,4,10,14":
      raíz = 8
      buscar el primer valor > 8 → el 10 (índice 5)
      izquierda  = [3, 1, 6, 4]   (todos < 8)
      derecha    = [10, 14]       (todos > 8)

      Reconstruir izquierda [3,1,6,4]:
        raíz = 3
        primer > 3 → el 6 (índice 2)
        izquierda = [1]    → hoja 1
        derecha   = [6, 4] → raíz 6, izquierda [4] → hoja 4

      Reconstruir derecha [10,14]:
        raíz = 10, sin menores, derecha [14] → hoja 14

    Resultado: el árbol original.

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción sobre el número de valores.

    Caso base: lista vacía → árbol vacío.

    Hipótesis: construir reconstruye correctamente listas de tamaño < n.

    Paso: para una lista de n valores, el primero es la raíz r. Los
    valores se dividen en menores (que van a la izquierda, porque el
    BST así lo exige) y mayores. Ambas partes tienen tamaño < n, y por
    hipótesis se reconstruyen correctamente. Como todo valor izquierdo
    < r < todo valor derecho, el resultado es un BST con la misma
    raíz y los mismos subárboles que el original. ∎

COMPLEJIDAD
    Serializar: O(n) tiempo, O(n) espacio.
    Deserializar: O(n²) peor caso (lista degenerada, la búsqueda del
    corte recorre casi todo cada vez). O(n) espacio.

    MEJORA: usando una cola y pasando límites (min, max) en vez de
    rebanar la lista, se baja a O(n). Es la versión que se usaría en
    producción.

CASOS LÍMITE
    - Cadena vacía → árbol vacío (None).
    - Un solo valor → árbol de un nodo.
    - Árbol degenerado (lista ordenada) → funciona, la recursión
      llega a profundidad n.
    - Valores negativos → el separador "," no causa problemas,
      pero sí hay que usar int() al parsear.
"""


class Nodo:
    """Nodo de un árbol binario."""

    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def serializar(raiz):
    """Convierte un BST a cadena usando preorden.

    El preorden basta (sin marcar nulos) gracias a la invariante BST.
    """
    valores = []

    def preorden(nodo):
        if not nodo:
            return
        valores.append(str(nodo.valor))
        preorden(nodo.izquierdo)
        preorden(nodo.derecho)

    preorden(raiz)
    return ",".join(valores)


def deserializar(datos):
    """Reconstruye un BST desde su representación en preorden."""
    if not datos:
        return None

    valores = [int(x) for x in datos.split(",")]

    def construir(preorden):
        if not preorden:
            return None

        valor = preorden[0]
        nodo = Nodo(valor)

        # Encontrar dónde empiezan los mayores que la raíz
        i = 1
        while i < len(preorden) and preorden[i] < valor:
            i += 1

        nodo.izquierdo = construir(preorden[1:i])   # menores
        nodo.derecho = construir(preorden[i:])       # mayores
        return nodo

    return construir(valores)


def insertar(raiz, valor):
    """Inserta en el BST (para construir los árboles de prueba)."""
    if raiz is None:
        return Nodo(valor)
    if valor < raiz.valor:
        raiz.izquierdo = insertar(raiz.izquierdo, valor)
    elif valor > raiz.valor:
        raiz.derecho = insertar(raiz.derecho, valor)
    return raiz


def inorden(nodo):
    """Recorrido inorden: valores ordenados si es BST."""
    if nodo is None:
        return []
    return inorden(nodo.izquierdo) + [nodo.valor] + inorden(nodo.derecho)


def preorden(nodo):
    """Recorrido preorden."""
    if nodo is None:
        return []
    return [nodo.valor] + preorden(nodo.izquierdo) + preorden(nodo.derecho)


if __name__ == "__main__":
    # Árbol de prueba
    raiz = None
    for val in [8, 3, 10, 1, 6, 14, 4]:
        raiz = insertar(raiz, val)

    # Serializar
    s = serializar(raiz)
    print(f"Serializado: {s}")
    assert s == "8,3,1,6,4,10,14", f"preorden inesperado: {s}"

    # Deserializar
    restaurado = deserializar(s)
    print(f"Inorden del restaurado: {inorden(restaurado)}")
    assert inorden(restaurado) == inorden(raiz)
    assert preorden(restaurado) == preorden(raiz), "estructura distinta"

    # Idempotencia: serializar(deserializar(s)) == s
    assert serializar(restaurado) == s, "no es idempotente"

    # Casos límite
    assert deserializar("") is None, "cadena vacía → árbol vacío"

    uno = deserializar("42")
    assert uno is not None and uno.valor == 42
    assert uno.izquierdo is None and uno.derecho is None

    # Árbol degenerado (valores ascendentes)
    deg = deserializar("1,2,3,4,5")
    assert preorden(deg) == [1, 2, 3, 4, 5]

    # Round-trip con muchos árboles aleatorios
    import random
    random.seed(17)
    for _ in range(200):
        n = random.randint(0, 25)
        valores = random.sample(range(-50, 50), n)
        arbol = None
        for v in valores:
            arbol = insertar(arbol, v)
        s = serializar(arbol)
        reconstruido = deserializar(s)
        assert preorden(reconstruido) == preorden(arbol), \
            f"falló el round-trip con {valores}"

    # El árbol reconstruido es un BST válido
    def es_bst_valido(nodo, mn=float('-inf'), mx=float('inf')):
        if nodo is None:
            return True
        if not (mn < nodo.valor < mx):
            return False
        return (es_bst_valido(nodo.izquierdo, mn, nodo.valor) and
                es_bst_valido(nodo.derecho, nodo.valor, mx))

    assert es_bst_valido(restaurado), "el restaurado no es BST válido"

    # Con valores negativos el separador no causa problemas
    neg = None
    for v in [-5, -10, -3, 0, 5]:
        neg = insertar(neg, v)
    s_neg = serializar(neg)
    assert deserializar(s_neg) is not None
    assert preorden(deserializar(s_neg)) == preorden(neg)

    print("\n✓ Todas las pruebas pasaron")
