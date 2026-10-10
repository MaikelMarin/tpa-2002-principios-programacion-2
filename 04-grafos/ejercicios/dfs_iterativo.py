r"""
Ejercicio 4: DFS iterativo (Depth-First Search)
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Pila (00-fundamentos §8.4): la estructura que hace funcionar DFS.
    - BFS (ejercicio 3): para comparar ambas estrategias.
    - Lista de adyacencia (ejercicio 1).

PROBLEMA
    Recorrer un grafo en profundidad, desde un vértice origen.

FONDO MATEMÁTICO
    DFS explora tan leajo como puede por cada rama antes de
    retroceder. Es el análogo de recorrer un laberinto tocando siempre
    la misma pared.

    La diferencia con BFS no es solo el orden de visita: BFS explora
    por NIVELES (anchura), DFS por RAMAS (profundidad). Eso las hace
    útiles para cosas distintas.

ESTRATEGIA (pila explícita)

```python
def dfs(grafo, inicio):
    visitados = set()
    pila = [inicio]
    while pila:
        v = pila.pop()
        if v not in visitados:        # ← marcar al DESAPILAR
            visitados.add(v)
            for vecino, _ in reversed(grafo.vecinos(v)):
                if vecino not in visitados:
                    pila.append(vecino)
    return visitados
```

    DETALLE: `reversed()` en los vecinos.
    Como la pila es LIFO, si se añaden los vecinos en orden [A, B, C],
    se sacan C, B, A. Para que se exploren en el orden original, hay
    que insertarlos al revés. Sin el reversed, el recorrido es válido
    pero visita en orden distinto al DFS recursivo.

    DETALLE: marcar al DESAPILAR (a diferencia de BFS).
    En DFS la misma marca al desapilar funciona bien porque cada
    vértice se apila pocas veces. Pero insertar el chequeo al apilar
    también es válido. Ambas son correctas; la diferencia está en
    cuántas veces entra cada vértice a la pila.

TRAZA sobre:
        0 ─ 1
        │ ╲ │
        2 ─ 3

    pila = [0]
    pop 0 → visitar 0. Vecinos (al revés): [2, 1, 0]... 
            en realidad vecinos(0) = [1, 2, 3] → reversed = [3, 2, 1]
            apilar 3, 2, 1 → pila = [3, 2, 1]
    pop 1 → visitar 1. Vecinos de 1 = [0, 3] → reversed = [3, 0]
            0 visitado, apilar 3 → pila = [3, 2, 3]
    pop 3 → visitar 3. Vecinos de 3 = [0, 1, 2] → todos visitados o en pila
            pila = [3, 2]
    pop 2 → visitar 2. pila = [3]
    pop 3 → ya visitado. pila = []

    Orden de visita: 0, 1, 3, 2

    Compare con BFS desde 0: 0, 1, 2, 3. Distinto orden, mismos vértices.

COMPLEJIDAD
    Tiempo: O(V + E). Cada vértice se visita una vez; cada arista se
    examina una vez desde cada extremo (en no dirigido).
    Espacio: O(V) para la pila y los visitados.

    Nota: en la versión de "marcar al desapilar" sin filtro al
    insertar, un vértice puede apilarse varias veces, pero el número
    total de apilamientos sigue siendo O(E).

CUÁNDO USAR DFS Y CUÁNDO BFS
    Tarea                                  Algoritmo
    Camino más corto sin pesos             BFS
    Detectar ciclos                        DFS
    Ordenamiento topológico                DFS
    Componentes fuertemente conexos        DFS
    Encontrar cualquier camino             DFS
    Recorrer por niveles                   BFS
    Comprobar conectividad                 Cualquiera

RELACIÓN CON OTROS TEMAS
    - El recorrido preorden de un árbol (tema 03) es DFS sobre una
      estructura sin ciclos.
    - El backtracking (tema 01) es una variante de DFS que además
      puede deshacer decisiones.
    - La pila de llamadas del sistema es exactamente una pila de DFS.
"""


class Grafo:
    """Grafo no dirigido con lista de adyacencia."""

    def __init__(self):
        self.adyacencia = {}

    def agregar_arista(self, u, v):
        if u not in self.adyacencia:
            self.adyacencia[u] = []
        if v not in self.adyacencia:
            self.adyacencia[v] = []
        self.adyacencia[u].append((v, 1))
        self.adyacencia[v].append((u, 1))

    def vecinos(self, v):
        return self.adyacencia.get(v, [])


def dfs_iterativo(grafo, inicio):
    """DFS iterativo con pila. O(V + E) tiempo, O(V) espacio."""
    visitados = set()
    pila = [inicio]
    resultado = []

    while pila:
        vertice = pila.pop()
        if vertice not in visitados:
            visitados.add(vertice)
            resultado.append(vertice)
            # reversed para explorar en el orden original de inserción
            for vecino, _ in reversed(grafo.vecinos(vertice)):
                if vecino not in visitados:
                    pila.append(vecino)

    return resultado


def dfs_recursivo(grafo, inicio, visitados=None):
    """DFS recursivo, para verificar que ambas coinciden."""
    if visitados is None:
        visitados = set()
    visitados.add(inicio)
    for vecino, _ in grafo.vecinos(inicio):
        if vecino not in visitados:
            dfs_recursivo(grafo, vecino, visitados)
    return visitados


if __name__ == "__main__":
    # Grafo de prueba:
    #   0 ─ 1
    #   │ ╲ │
    #   2 ─ 3
    grafo = Grafo()
    for u, v in [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)]:
        grafo.agregar_arista(u, v)

    resultado = dfs_iterativo(grafo, 0)
    print(f"DFS desde 0: {resultado}")

    # Todos los vértices alcanzables, sin repetidos
    assert sorted(resultado) == [0, 1, 2, 3]
    assert len(resultado) == len(set(resultado))

    # Empieza por el origen
    assert resultado[0] == 0

    # La versión recursiva visita los mismos vértices
    rec = dfs_recursivo(grafo, 0)
    assert set(resultado) == rec, "iterativa y recursiva deben coincidir"
    print(f"DFS recursivo visita: {sorted(rec)}")

    # Casos base
    vacio = Grafo()
    assert dfs_iterativo(vacio, 0) == [0]

    aislado = Grafo()
    aislado.adyacencia = {5: []}
    assert dfs_iterativo(aislado, 5) == [5]

    # DFS explora una rama completa antes de cambiar
    # En una cadena 0-1-2-3, DFS visita 0,1,2,3 (una sola rama)
    cadena = Grafo()
    for u, v in [(0, 1), (1, 2), (2, 3)]:
        cadena.agregar_arista(u, v)
    assert dfs_iterativo(cadena, 0) == [0, 1, 2, 3]

    # Contraste con BFS en un árbol de dos niveles
    arbol = Grafo()
    arbol.agregar_arista(0, 1)
    arbol.agregar_arista(0, 2)
    arbol.agregar_arista(1, 3)
    arbol.agregar_arista(1, 4)
    # DFS va profundo: 0, 1, 3, 4, 2 (o similar)
    dfs_arbol = dfs_iterativo(arbol, 0)
    print(f"\nÁrbol, DFS: {dfs_arbol}")
    assert dfs_arbol[0] == 0
    # El 1 (hijo) viene antes que el 2 (otro hijo): DFS baja primero
    assert dfs_arbol.index(1) < dfs_arbol.index(2)

    # Verificación aleatoria contra la versión recursiva
    import random
    random.seed(121)
    for _ in range(300):
        g = Grafo()
        n = random.randint(1, 12)
        for _ in range(random.randint(0, n * 2)):
            if n > 1:
                g.agregar_arista(random.randrange(n), random.randrange(n))
        origen = random.randrange(n)
        assert set(dfs_iterativo(g, origen)) == dfs_recursivo(g, origen)

    # DFS no garantiza distancia mínima (a diferencia de BFS)
    diamante = Grafo()
    for u, v in [(0, 1), (0, 2), (1, 3), (2, 3)]:
        diamante.agregar_arista(u, v)
    # Si DFS va 0→1→3 primero, cuando llegue a 3 por el otro lado ya
    # estará visitado: no puede recalcular distancias.
    orden = dfs_iterativo(diamante, 0)
    print(f"\nDiamante, DFS: {orden}")
    assert orden.index(3) < orden.index(2) or orden.index(3) < orden.index(1), \
        "DFS llega a 3 por el primer camino que encuentra"

    print("\n✓ Todas las pruebas pasaron")
