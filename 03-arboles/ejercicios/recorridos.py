r"""
Ejercicio 2: Recorridos de árbol binario
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Recursión sobre estructuras recursivas (tema 01, §3.5).
    - Cola (00-fundamentos §8.5): el recorrido por niveles usa una.

PROBLEMA
    Implementar los cuatro recorridos: preorden, inorden, postorden
    y por niveles.

FONDO MATEMÁTICO
    Los tres primeros difieren SOLO en cuándo se visita la raíz:

        preorden:   raíz → izquierdo → derecho
        inorden:    izquierdo → raíz → derecho
        postorden:  izquierdo → derecho → raíz

    Todos son O(n) tiempo. La diferencia está en el USO:
      - Preorden: clonar, serializar, notación prefija.
      - Inorden: obtener valores ordenados de un BST.
      - Postorden: liberar memoria, notación postfija.
    El cuarto (BFS) recorre por niveles y usa una cola.

ESTRATEGIA
    Recursión directa. El caso base es el subárbol nulo:

```python
def preorden(nodo):
    if nodo:                      # None es falsy: caso base implícito
        visitar(nodo)             # ← aquí va la "visita"
        preorden(nodo.izquierdo)
        preorden(nodo.derecho)
```

    Mover la línea `visitar(nodo)` entre las tres posiciones da los
    tres recorridos. Es la misma función con una línea en otro sitio.

    Para el recorrido por niveles se usa una cola (FIFO): se encolan
    los hijos al visitar, y se procesa en orden de descubrimiento.

TRAZA sobre el árbol:
            1
           / \
          2   3
         / \   \
        4   5   6

    Preorden:  visitar 1 → ir a izq (2) → visitar 2 → ir a izq (4)
                → visitar 4 (hoja) → volver, ir a der (5) → visitar 5
                → volver a 1, ir a der (3) → visitar 3 → der (6) → visitar 6
                Resultado: 1 2 4 5 3 6

    Inorden:   subárbol izq de 1: [4, 2, 5]; luego 1; luego [3, 6]
                Resultado: 4 2 5 1 3 6

    Postorden: [4, 5, 2], [6, 3], luego 1
                Resultado: 4 5 2 6 3 1

    Por niveles (BFS):
                cola=[1] → visitar 1, encolar 2,3 → cola=[2,3]
                visitar 2, encolar 4,5 → cola=[3,4,5]
                visitar 3, encolar 6 → cola=[4,5,6]
                visitar 4,5,6 (hojas, no encolan nada)
                Resultado: 1 2 3 4 5 6

COMPLEJIDAD
    Tiempo: Θ(n). Cada nodo se visita exactamente una vez.
    Espacio (DFS): Θ(h) de pila de recursión.
    Espacio (BFS): Θ(w) donde w es el ancho máximo del árbol, que
                   puede ser ⌈n/2⌉ en el peor caso (último nivel).
                   ¡Puede ser MUCHO más que el O(log n) del DFS!

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción estructural (00-fundamentos §3.6).
    Caso base: nodo None → no se visita nada; correcto.
    Paso: si los recorridos de los subárboles son correctos,
    concatenarlos con la visita de la raíz en la posición que define
    cada recorrido da la secuencia correcta. ∎

RELACIÓN CON OTROS TEMAS
    - El BFS sobre árboles es el mismo algoritmo que el BFS sobre
      grafos (tema 04). La única diferencia es que aquí los hijos
      están en atributos fijos, y allí hay que pedir los vecinos.
    - La serialización de BST (ejercicio 20) usa el preorden.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


def preorden(nodo):
    """Raíz → Izquierdo → Derecho."""
    if nodo:
        print(nodo.valor, end=" ")
        preorden(nodo.izquierdo)
        preorden(nodo.derecho)


def inorden(nodo):
    """Izquierdo → Raíz → Derecho."""
    if nodo:
        inorden(nodo.izquierdo)
        print(nodo.valor, end=" ")
        inorden(nodo.derecho)


def postorden(nodo):
    """Izquierdo → Derecho → Raíz."""
    if nodo:
        postorden(nodo.izquierdo)
        postorden(nodo.derecho)
        print(nodo.valor, end=" ")


def por_niveles(raiz):
    """BFS: nivel por nivel, usando una cola."""
    from collections import deque

    if not raiz:
        return

    cola = deque([raiz])
    while cola:
        nodo = cola.popleft()
        print(nodo.valor, end=" ")
        if nodo.izquierdo:
            cola.append(nodo.izquierdo)
        if nodo.derecho:
            cola.append(nodo.derecho)


if __name__ == "__main__":
    # Árbol de referencia
    #        1
    #       / \
    #      2   3
    #     / \   \
    #    4   5   6
    raiz = Nodo(1)
    raiz.izquierdo = Nodo(2)
    raiz.derecho = Nodo(3)
    raiz.izquierdo.izquierdo = Nodo(4)
    raiz.izquierdo.derecho = Nodo(5)
    raiz.derecho.derecho = Nodo(6)

    print("Preorden:  ", end=""); preorden(raiz); print()
    print("Inorden:   ", end=""); inorden(raiz); print()
    print("Postorden: ", end=""); postorden(raiz); print()
    print("Por nivel: ", end=""); por_niveles(raiz); print()

    # Verificación con valores capturados
    def a_lista(func, r):
        salida = []
        def capturar(n):
            if n:
                salida.append(n.valor)
                capturar(n.izquierdo)
                capturar(n.derecho)
        # Reimplementar para capturar sin imprimir
        if func == "pre":
            def rec(n):
                if n:
                    salida.append(n.valor); rec(n.izquierdo); rec(n.derecho)
        elif func == "in":
            def rec(n):
                if n:
                    rec(n.izquierdo); salida.append(n.valor); rec(n.derecho)
        else:
            def rec(n):
                if n:
                    rec(n.izquierdo); rec(n.derecho); salida.append(n.valor)
        rec(r)
        return salida

    assert a_lista("pre", raiz) == [1, 2, 4, 5, 3, 6]
    assert a_lista("in", raiz) == [4, 2, 5, 1, 3, 6]
    assert a_lista("post", raiz) == [4, 5, 2, 6, 3, 1]

    # BFS capturado
    from collections import deque

    def bfs_lista(r):
        out, cola = [], deque([r] if r is not None else [])
        while cola:
            n = cola.popleft()
            out.append(n.valor)
            if n.izquierdo:
                cola.append(n.izquierdo)
            if n.derecho:
                cola.append(n.derecho)
        return out

    assert bfs_lista(raiz) == [1, 2, 3, 4, 5, 6]

    # Casos base
    assert a_lista("pre", None) == []
    solo = Nodo(7)
    assert a_lista("pre", solo) == [7]
    assert bfs_lista(None) == []
    assert bfs_lista(solo) == [7]

    # Reconstrucción: preorden + inorden determinan el árbol
    def reconstruir(pre, ino):
        if not pre:
            return None
        raiz_v = pre[0]
        idx = ino.index(raiz_v)
        n = Nodo(raiz_v)
        n.izquierdo = reconstruir(pre[1:1+idx], ino[:idx])
        n.derecho = reconstruir(pre[1+idx:], ino[idx+1:])
        return n

    pre = a_lista("pre", raiz)
    ino = a_lista("in", raiz)
    rec = reconstruir(pre, ino)
    assert a_lista("pre", rec) == pre, "reconstrucción fallida"

    print("\n✓ Todas las pruebas pasaron")
