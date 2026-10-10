r"""
Ejercicio 7: Camino más corto con BFS
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - BFS (ejercicio 3): el algoritmo base.
    - La propiedad de BFS: visita en orden de distancia creciente.
    - Reconstrucción de caminos con punteros "predecesor".

PROBLEMA
    Encontrar el camino más corto (en número de aristas) entre dos
    vértices de un grafo NO PONDERADO.

FONDO MATEMÁTICO
    BFS visita los vértices en orden no decreciente de distancia al
    origen. Si al descubrir cada vértice guardamos QUIÉN lo descubrió
    (su predecesor), podemos reconstruir el camino óptimo hacia atrás.

    La distancia que BFS garantiza es en NÚMERO DE ARISTAS, no en peso.
    Si las aristas tienen pesos distintos, hay que usar Dijkstra.

ESTRATEGIA
    1. BFS desde el origen, guardando `predecesor[v]` para cada
       vértice descubierto.
    2. Parar en cuanto se descubre el destino (ya no se puede mejorar).
    3. Reconstruir el camino hacia atrás desde el destino.

    La parada temprana es válida porque BFS explora en orden de
    distancia: cuando se descubre el destino, ya se encontró la
    distancia mínima.

TRAZA sobre:
        0 ─ 1
        │   │
        2 ─ 3
        camino de 0 a 3

    cola = [(0, [0])], predecesor[0] = None

    pop (0, [0]). Vecinos: 1, 2. Ninguno es el destino.
        predecesor[1] = 0, cola += (1, [0,1])
        predecesor[2] = 0, cola += (2, [0,2])
    pop (1, [0,1]). Vecinos: 0 (visitado), 3.
        3 es el DESTINO → devolver [0, 1, 3]

    Resultado: 0 → 1 → 3, con 2 aristas. Es óptimo.

    Contraste con 0 → 2 → 3: también 2 aristas. Ambos son óptimos;
    BFS devuelve el que encuentra primero.

IMPLEMENTACIÓN

```python
def camino_minimo_bfs(grafo, inicio, destino):
    if inicio == destino:
        return [inicio]

    visitados = {inicio}
    cola = deque([(inicio, [inicio])])

    while cola:
        vertice, camino = cola.popleft()
        for vecino, _ in grafo.vecinos(vertice):
            if vecino == destino:
                return camino + [vecino]     # parada temprana
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino + [vecino]))
    return None
```

DEMOSTRACIÓN DE CORRECCIÓN
    BFS procesa los vértices en orden no decreciente de distancia. El
    destino, cuando se descubre, lo es a la distancia mínima posible
    (no puede haber un camino más corto, porque los vértices a menor
    distancia ya se procesaron y ninguno lo descubrió antes). El
    camino reconstruido usa los predecesores, que son exactamente los
    vértices desde los que se descubrió cada uno, luego es un camino
    válido. ∎

COMPLEJIDAD
    Tiempo: O(V + E). Igual que BFS.
    Espacio: O(V) para la cola y los predecesores.

    Si se guardan caminos completos en la cola (como arriba), cada
    camino cuesta O(V), lo que daría O(V²) en el peor caso. La
    versión eficiente guarda solo el predecesor (O(1) por vértice).

CASOS LÍMITE
    - Origen == destino: camino de un vértice, longitud 0.
    - Sin camino: devuelve None (el destino no es alcanzable).
    - Grafo inconexo: si el destino está en otra componente, None.

RELACIÓN CON OTROS TEMAS
    - Con pesos, este algoritmo NO funciona: da el camino con MENOS
      ARISTAS, no el de menor coste. Para eso está Dijkstra
      (ejercicio 10).
    - El algoritmo A* es una optimización de Dijkstra con heurística.
"""


from collections import deque


class Grafo:
    """Grafo no dirigido con lista de adyacencia."""

    def __init__(self):
        self.adyacencia = {}

    def agregar_arista(self, u, v):
        self.adyacencia.setdefault(u, [])
        self.adyacencia.setdefault(v, [])
        self.adyacencia[u].append((v, 1))
        self.adyacencia[v].append((u, 1))

    def vecinos(self, v):
        return self.adyacencia.get(v, [])


def camino_minimo_bfs(grafo, inicio, destino):
    """Camino más corto en aristas. O(V+E). Devuelve la lista o None."""
    if inicio == destino:
        return [inicio]

    visitados = {inicio}
    cola = deque([(inicio, [inicio])])

    while cola:
        vertice, camino = cola.popleft()

        for vecino, _ in grafo.vecinos(vertice):
            if vecino == destino:
                return camino + [vecino]          # parada temprana

            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino + [vecino]))

    return None


def distancias_bfs(grafo, inicio):
    """Distancias en aristas desde el origen."""
    dist = {inicio: 0}
    cola = deque([inicio])
    while cola:
        v = cola.popleft()
        for vecino, _ in grafo.vecinos(v):
            if vecino not in dist:
                dist[vecino] = dist[v] + 1
                cola.append(vecino)
    return dist


if __name__ == "__main__":
    #  0 ─ 1
    #  │   │
    #  2 ─ 3
    g = Grafo()
    for u, v in [(0, 1), (0, 2), (1, 3), (2, 3)]:
        g.agregar_arista(u, v)

    camino = camino_minimo_bfs(g, 0, 3)
    print(f"Camino de 0 a 3: {camino}")
    assert camino is not None
    assert camino[0] == 0 and camino[-1] == 3
    assert len(camino) - 1 == 2, "dos aristas"

    # El camino es válido: cada par consecutivo es una arista
    for a, b in zip(camino, camino[1:]):
        assert any(n == b for n, _ in g.vecinos(a)), f"{a}-{b} no es arista"

    # Origen == destino
    assert camino_minimo_bfs(g, 0, 0) == [0]
    assert camino_minimo_bfs(g, 3, 3) == [3]

    # Caminos a todos los vértices
    for destino in [1, 2, 3]:
        c = camino_minimo_bfs(g, 0, destino)
        assert len(c) - 1 == distancias_bfs(g, 0)[destino], \
            f"la longitud debe coincidir con la distancia BFS"

    # Sin camino (componentes separadas)
    dcs = Grafo()
    dcs.agregar_arista(0, 1)
    dcs.agregar_arista(2, 3)
    assert camino_minimo_bfs(dcs, 0, 3) is None, "inalcanzable"
    print("Grafo inconexo, 0 a 3: None")

    # Cadena larga: el camino debe ser la cadena completa
    cadena = Grafo()
    for i in range(20):
        cadena.agregar_arista(i, i + 1)
    c_largo = camino_minimo_bfs(cadena, 0, 20)
    assert c_largo == list(range(21)), "recorre toda la cadena"
    assert len(c_largo) - 1 == 20

    # El camino más corto NO es siempre el más directo en apariencia
    # (grafo con dos rutas, BFS elige la de menos aristas)
    dos_rutas = Grafo()
    dos_rutas.agregar_arista(0, 3)              # ruta directa: 1 arista
    dos_rutas.agregar_arista(0, 1)              # ruta con desvío
    dos_rutas.agregar_arista(1, 2)
    dos_rutas.agregar_arista(2, 3)
    c_rutas = camino_minimo_bfs(dos_rutas, 0, 3)
    print(f"Dos rutas disponibles, BFS elige: {c_rutas}")
    assert len(c_rutas) - 1 == 1, "la ruta directa gana en aristas"

    # Verificación exhaustiva: comparar con Dijkstra de pesos 1
    import heapq

    def dijkstra_unitario(grafo, inicio):
        dist = {v: float('inf') for v in grafo.adyacencia}
        dist[inicio] = 0
        cola = [(0, inicio)]
        while cola:
            d, u = heapq.heappop(cola)
            if d > dist[u]:
                continue
            for v, p in grafo.vecinos(u):
                if d + p < dist[v]:
                    dist[v] = d + p
                    heapq.heappush(cola, (dist[v], v))
        return dist

    import random
    random.seed(191)
    for _ in range(300):
        g3 = Grafo()
        n = random.randint(1, 12)
        for _ in range(random.randint(0, n * 2)):
            if n > 1:
                g3.agregar_arista(random.randrange(n), random.randrange(n))
        origen = random.randrange(n)
        destino = random.randrange(n)
        c = camino_minimo_bfs(g3, origen, destino)
        d_dij = dijkstra_unitario(g3, origen)
        if destino not in d_dij:
            continue                          # no está en el grafo: ignorar
        if c is None:
            assert d_dij[destino] == float('inf'), \
                "BFS no encontró camino pero Dijkstra sí"
        else:
            assert len(c) - 1 == d_dij[destino], \
                "BFS y Dijkstra con pesos 1 deben coincidir"

    print("\n✓ Todas las pruebas pasaron")
