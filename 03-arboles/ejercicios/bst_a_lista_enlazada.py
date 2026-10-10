r"""
Ejercicio 17: BST a lista enlazada
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - Recorrido inorden (teoria.md §3.1).
    - Listas enlazadas (00-fundamentos §8.3).
    - Referencias a objetos (§9.2): por qué no se crean nodos nuevos.

PROBLEMA
    Convertir un BST en una lista enlazada ordenada, IN-PLACE:
    reutilizando los nodos del árbol, sin asignar memoria nueva.

FONDO MATEMÁTICO
    El inorden de un BST produce los valores en orden ascendente
    (§4.1). Si durante ese recorrido vamos reconectando los punteros,
    el resultado es una lista ordenada.

    Conversión de punteros:
        nodo.izquierdo  →  None      (ya no se usa como árbol)
        nodo.derecho    →  siguiente nodo del inorden

    El TRUCO para hacerlo in-place: mantener un puntero al ÚLTIMO
    nodo visitado (`anterior`). Al entrar en un nodo, se conecta
    `anterior.derecho = nodo_actual`.

TRAZA sobre:
        2
       / \
      1   3

    anterior = None, cabeza = None

    inorden(2):
      inorden(2.izq = 1):
        inorden(1.izq = None) → nada
        VISITAR 1:
          anterior es None → cabeza = 1
          anterior = 1
        inorden(1.der = None) → nada
      VISITAR 2:
        anterior(1).derecho = 2     ← reconexión
        anterior = 2
      inorden(2.der = 3):
        VISITAR 3:
          anterior(2).derecho = 3
          anterior = 3

    Resultado: cabeza = 1 → 1.derecho = 2 → 2.derecho = 3

    Verificación: 1 → 2 → 3, ordenado. Y no se creó ningún NodoLista:
    se reusaron los nodos del árbol.

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción estructural.
    Caso base: nodo None → no se modifica nada. Correcto.
    Hipótesis: la conversión de subárboles menores produce listas
    ordenadas y deja `anterior` apuntando al último nodo.
    Paso: el inorden visita izq, luego el nodo, luego der. Como el
    inorden de un BST es ascendente y cada visita enlaza el nodo al
    anterior, la secuencia resultante es ascendente y completa. ∎

COMPLEJIDAD
    Tiempo: Θ(n). Cada nodo se visita una vez.
    Espacio: O(h) de pila de recursión. ¡No se asigna memoria de
    datos! Los nodos del árbol se reciclan como nodos de lista.

    Compare con la versión que crea nodos nuevos: O(n) de memoria
    adicional.

CUÁNDO USAR ESTO
    - Para aplanar un índice en memoria de forma eficiente.
    - Cuando se necesita recorrer en orden repetidamente: la lista se
      recorre con O(1) de espacio, mientras que el árbol necesita O(h)
      por cada recorrido.
    - Como paso intermedio al fusionar dos BST.

ADVERTENCIA: la operación DESTRUYE el árbol
    Tras la conversión, la estructura original ya no es un árbol: los
    punteros se reapuntaron. Si se necesita conservar el árbol, hay
    que hacer una copia primero (que costaría O(n)).

RELACIÓN CON OTROS TEMAS
    - El mismo principio de "recorrer reconectando" se usa en el
      aplanamiento de estructuras (flatten) en programación funcional.
    - En bases de datos, fusionar dos índices B-tree produce una
      estructura plana ordenada similar.
"""


class Nodo:
    """Nodo que sirve tanto de árbol como de lista enlazada."""

    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None       # como árbol
        self.derecho = None         # como árbol Y como "siguiente"

    def __repr__(self):
        return f"Nodo({self.valor})"


def bst_a_lista_enlazada(raiz):
    """Convierte un BST en lista enlazada ordenada, in-place.

    Devuelve la cabeza de la lista. Reutiliza los nodos del árbol.
    """
    estado = {"cabeza": None, "anterior": None}

    def inorden(nodo):
        if not nodo:
            return

        inorden(nodo.izquierdo)

        # Reconectar: el nodo anterior apunta a este por la "derecha"
        if estado["anterior"]:
            estado["anterior"].derecho = nodo
        else:
            estado["cabeza"] = nodo          # el primero es la cabeza
        estado["anterior"] = nodo

        # El izquierdo ya no se usa como árbol
        nodo.izquierdo = None

        inorden(nodo.derecho)

    inorden(raiz)

    # El último nodo no debe apuntar a nada
    if estado["anterior"]:
        estado["anterior"].derecho = None

    return estado["cabeza"]


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
    """Recorrido inorden: valores ordenados del BST."""
    if nodo is None:
        return []
    return inorden(nodo.izquierdo) + [nodo.valor] + inorden(nodo.derecho)


if __name__ == "__main__":
    raiz = None
    for val in [4, 2, 5, 1, 3]:
        raiz = insertar(raiz, val)

    print(f"Inorden del árbol: {inorden(raiz)}")

    cabeza = bst_a_lista_enlazada(raiz)

    # Recorrer la lista resultante
    valores = []
    actual = cabeza
    while actual:
        valores.append(actual.valor)
        actual = actual.derecho

    print(f"Lista enlazada:     {valores}")
    assert valores == [1, 2, 3, 4, 5], "la lista debe estar ordenada"

    # La cabeza es el mínimo
    assert cabeza.valor == 1

    # El último nodo no apunta a nada
    actual = cabeza
    while actual.derecho:
        actual = actual.derecho
    assert actual.derecho is None, "el último nodo debe terminar en None"
    assert actual.valor == 5

    # Los punteros izquierdos quedaron limpios
    actual = cabeza
    while actual:
        assert actual.izquierdo is None, "no debe quedar puntero izquierdo"
        actual = actual.derecho

    # IN-PLACE: no se crearon nodos nuevos
    def contar_nodos(n):
        c = 0
        while n:
            c += 1
            n = n.derecho
        return c

    n_original = 5
    assert contar_nodos(cabeza) == n_original, "debe haber los mismos nodos"

    # Casos base
    assert bst_a_lista_enlazada(None) is None
    uno = insertar(None, 42)
    c = bst_a_lista_enlazada(uno)
    assert c.valor == 42 and c.derecho is None

    # Degenerado (lista ascendente insertada en orden)
    deg = None
    for v in [1, 2, 3, 4, 5, 6, 7]:
        deg = insertar(deg, v)
    c = bst_a_lista_enlazada(deg)
    vals = []
    while c:
        vals.append(c.valor); c = c.derecho
    assert vals == [1, 2, 3, 4, 5, 6, 7]

    # Verificación aleatoria exhaustiva
    import random
    random.seed(81)
    for _ in range(300):
        n = random.randint(0, 30)
        valores = random.sample(range(-200, 200), n)
        if valores:
            arbol = None
            for v in valores:
                arbol = insertar(arbol, v)
        else:
            arbol = None
        c = bst_a_lista_enlazada(arbol)
        res = []
        while c:
            res.append(c.valor); c = c.derecho
        assert res == sorted(valores), f"falló con {valores}"

    # Árbol grande: eficiencia
    grande = None
    import random as rnd
    rnd.seed(99)
    for v in rnd.sample(range(10000), 2000):
        grande = insertar(grande, v)
    c = bst_a_lista_enlazada(grande)
    cont = 0
    while c:
        cont += 1; c = c.derecho
    print(f"\nÁrbol de 2000 nodos convertido: {cont} nodos en la lista")
    assert cont == 2000

    print("\n✓ Todas las pruebas pasaron")
