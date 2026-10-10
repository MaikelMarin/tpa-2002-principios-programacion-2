r"""
Ejercicio 10: Algoritmo de Dijkstra
Dificultad: Avanzado

CONOCIMIENTO PREVIO NECESARIO
    - BFS (ejercicio 3): Dijkstra es su generalización con pesos.
    - Cola de PRIORIDAD / heap (00-fundamentos §8.6): reemplaza la
      cola FIFO de BFS.
    - Grafos ponderados y lista de adyacencia (ejercicio 1).
    - Inducción: la corrección se demuestra por inducción (§5.1).

PROBLEMA
    Dado un grafo ponderado con pesos NO NEGATIVOS y un origen s,
    hallar la distancia mínima de s a todos los demás vértices.

FONDO MATEMÁTICO
    La idea codiciosa: mantener un conjunto de vértices con distancia
    ya DEFINITIVA. En cada paso:
      1. Extraer del heap el vértice no procesado con menor distancia
         tentativa.
      2. Fijar su distancia (ya es óptima).
      3. RELAJAR sus aristas: para cada vecino v, si
         dist[u] + peso(u,v) < dist[v], actualizar dist[v].

    El heap reemplaza a la cola FIFO de BFS. En BFS, el siguiente
    vértice a procesar es el que llegó primero. En Dijkstra, es el de
    MENOR DISTANCIA, que puede haber sido descubierto después pero
    estar más cerca.

INVARIANTE (la clave de la corrección)
    Al extraer un vértice u del heap, dist[u] es la distancia mínima
    real desde el origen. Es decir: ya es DEFINITIVA.

    DEMOSTRACIÓN:
    * Caso base: el origen se inserta con distancia 0. Óbvio.
    * Hipótesis: todos los extraídos antes que u tienen distancia
      correcta.
    * Paso: supongamos que existiera un camino MÁS CORTO a u, que
      pasara por algún w aún no extraído. Ese camino usa una arista
      (x, u) con x ya extraído. Pero cuando x se extrajo, se relajó
      (x, u), así que dist[u] ≤ dist[x] + peso(x,u), que es la
      longitud del camino por x. Contradicción. Luego dist[u] es
      óptima. ∎

    IMPORTANTE: esta demostración depende de que los pesos sean no
    negativos. Con un peso negativo, el camino "más corto" por w
    podría mejorarse DESPUÉS de haber extraído u, invalidando la
    conclusión. Por eso Dijkstra falla con pesos negativos.

ESTRATEGIA

```python
import heapq

def dijkstra(grafo, origen):
    dist = {v: float('inf') for v in grafo.vertices}
    dist[origen] = 0
    cola = [(0, origen)]                    # (distancia, vertice)

    while cola:
        d, u = heapq.heappop(cola)
        if d > dist[u]:
            continue                        # entrada obsoleta
        for v, peso in grafo.vecinos(u):
            if d + peso < dist[v]:          # relajar
                dist[v] = d + peso
                heapq.heappush(cola, (dist[v], v))
    return dist
```

    El chequeo `if d > dist[u]: continue` descarta entradas obsoletas:
    un vértice puede estar varias veces en el heap con distintas
    distancias, y solo la menor importa. Sin ese filtro se procesaría
    el mismo vértice múltiples veces.

TRAZA paso a paso
    Grafo: 0→1(4), 0→2(1), 2→1(2), 1→3(5), 2→3(1)

    Inicio: dist = {0:0, 1:∞, 2:∞, 3:∞}, cola = [(0,0)]

    Paso 1: pop (0,0). d=0 = dist[0], procesar.
        vecino 1: 0+4=4 < ∞ → dist[1]=4, push (4,1)
        vecino 2: 0+1=1 < ∞ → dist[2]=1, push (1,2)
        dist = {0:0, 1:4, 2:1, 3:∞}

    Paso 2: pop (1,2). d=1 = dist[2], procesar.
        vecino 0: no está en la lista de 2 (o ya es óptimo)
        vecino 1: 1+2=3 < 4 → dist[1]=3, push (3,1)
        vecino 3: 1+1=2 < ∞ → dist[3]=2, push (2,3)
        dist = {0:0, 1:3, 2:1, 3:2}

    Paso 3: pop (2,3). d=2 = dist[3], procesar.
        3 no tiene vecinos sin procesar relevantes.

    Paso 4: pop (3,1). d=3 = dist[1], procesar.
        vecino 3: 3+5=8, no mejora 2.

    Paso 5: pop (4,1). d=4 > dist[1]=3 → OBSOLETO, continuar.

    Resultado: dist = {0:0, 1:3, 2:1, 3:2}

    Note que el camino a 1 es 0→2→1 (peso 3), NO 0→1 directo (peso 4).
    Dijkstra encontró el camino indirecto más barato. Es exactamente
    lo que BFS no puede hacer: BFS habría dicho que 1 está a distancia
    1 (una arista), ignorando los pesos.

COMPLEJIDAD
    Con heap binario: O((V + E) log V).
    Con lista simple (buscar el mínimo recorriendo): O(V²).
    Con heap de Fibonacci: O(E + V log V) — óptimo teórico.

    Para grafos densos (E ≈ V²), O(V²) con lista simple puede ser
    competitivo porque evita el factor log.

CUÁNDO FALLA: PESOS NEGATIVOS
    Si una arista tiene peso negativo, el invariante se rompe: un
    camino podría mejorar DESPUÉS de haber fijado un vértice.

    Alternativa: BELLMAN-FORD. O(V·E). Más lento, pero:
      - Admite pesos negativos.
      - Detecta ciclos de peso negativo (que harían la distancia −∞).

    Regla: si hay pesos negativos, Dijkstra NO sirve. Sin excepción.

APLICACIONES REALES
    - Protocolos de enrutamiento (OSPF en redes IP).
    - GPS y planificación de rutas.
    - Redes de telecomunicaciones.
    - Motores de recomendación (camino más corto en grafo de Items).

RELACIÓN CON OTROS TEMAS
    - Kruskal y Prim (ejercicios 15, 16) resuelven un problema
      distinto: conectar TODOS los vértices con mínimo coste, no
      llegar desde un origen.
    - BFS es el caso particular de Dijkstra con todos los pesos = 1.
"""


import heapq


class Grafo:
    """Grafo dirigido ponderado con lista de adyacencia."""

    def __init__(self):
        self.adyacencia = {}

    def agregar_arista(self, u, v, peso):
        if u not in self.adyacencia:
            self.adyacencia[u] = []
        if v not in self.adyacencia:
            self.adyacencia[v] = []
        self.adyacencia[u].append((v, peso))

    def vecinos(self, v):
        return self.adyacencia.get(v, [])

    @property
    def vertices(self):
        return list(self.adyacencia.keys())


def dijkstra(grafo, origen):
    """Distancias mínimas desde origen. O((V+E) log V) con heap.

    REQUISITO: todos los pesos deben ser no negativos.
    """
    dist = {v: float('inf') for v in grafo.vertices}
    dist[origen] = 0
    cola = [(0, origen)]

    while cola:
        d, u = heapq.heappop(cola)

        if d > dist[u]:
            continue                          # entrada obsoleta

        for v, peso in grafo.vecinos(u):
            if d + peso < dist[v]:            # relajar
                dist[v] = d + peso
                heapq.heappush(cola, (dist[v], v))

    return dist


def dijkstra_con_camino(grafo, origen):
    """Dijkstra que también reconstruye los caminos.

    Guarda el predecesor de cada vértice para poder reconstruir la
    ruta completa.
    """
    dist = {v: float('inf') for v in grafo.vertices}
    previo = {v: None for v in grafo.vertices}
    dist[origen] = 0
    cola = [(0, origen)]

    while cola:
        d, u = heapq.heappop(cola)
        if d > dist[u]:
            continue
        for v, peso in grafo.vecinos(u):
            if d + peso < dist[v]:
                dist[v] = d + peso
                previo[v] = u
                heapq.heappush(cola, (dist[v], v))

    return dist, previo


def reconstruir_camino(previo, origen, destino):
    """Reconstruye el camino desde origen hasta destino."""
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = previo[actual]
    camino.reverse()
    return camino if camino[0] == origen else []


if __name__ == "__main__":
    # Grafo del ejemplo:
    #   0 →1(4), 0→2(1), 2→1(2), 1→3(5), 2→3(1)
    g = Grafo()
    g.agregar_arista(0, 1, 4)
    g.agregar_arista(0, 2, 1)
    g.agregar_arista(2, 1, 2)
    g.agregar_arista(1, 3, 5)
    g.agregar_arista(2, 3, 1)

    dist = dijkstra(g, 0)
    print("Distancias desde 0:")
    for v, d in sorted(dist.items()):
        print(f"  0 → {v}: {d}")

    assert dist[0] == 0
    assert dist[1] == 3, "el camino 0→2→1 (3) es más barato que 0→1 (4)"
    assert dist[2] == 1
    assert dist[3] == 2, "el camino 0→2→3 (2) es más barato que 0→1→3 (9)"

    # Reconstrucción de caminos
    dist2, previo = dijkstra_con_camino(g, 0)
    assert dist2 == dist, "ambas versiones deben coincidir"

    camino_1 = reconstruir_camino(previo, 0, 1)
    print(f"\nCamino óptimo a 1: {camino_1}")
    assert camino_1 == [0, 2, 1], "debe tomar el atajo por 2"

    camino_3 = reconstruir_camino(previo, 0, 3)
    print(f"Camino óptimo a 3: {camino_3}")
    assert camino_3 == [0, 2, 3]

    # Verificar que el peso del camino reconstruido coincide con dist
    def peso_camino(grafo, camino):
        total = 0
        for a, b in zip(camino, camino[1:]):
            for v, p in grafo.vecinos(a):
                if v == b:
                    total += p
                    break
        return total

    assert peso_camino(g, camino_1) == dist[1]
    assert peso_camino(g, camino_3) == dist[3]

    # Caso base: origen a sí mismo
    assert dijkstra(g, 0)[0] == 0
    camino_origen = reconstruir_camino(previo, 0, 0)
    assert camino_origen == [0]

    # Vértice inalcanzable
    g.adyacencia[99] = []                     # vértice aislado
    dist3 = dijkstra(g, 0)
    assert dist3[99] == float('inf'), "inalcanzable = infinito"
    print(f"\nVértice 99 (aislado): distancia = {dist3[99]}")

    # Comparación con BFS: con pesos unitarios, deben coincidir
    unitario = Grafo()
    for u, v in [(0, 1), (0, 2), (1, 3), (2, 3)]:
        unitario.agregar_arista(u, v, 1)
    d_unit = dijkstra(unitario, 0)
    assert d_unit[3] == 2, "con pesos 1, coincide con BFS"

    # Verificación contra fuerza bruta (Bellman-Ford)
    def bellman_ford(grafo, origen):
        dist = {v: float('inf') for v in grafo.vertices}
        dist[origen] = 0
        for _ in range(len(grafo.vertices) - 1):
            for u in grafo.vertices:
                if dist[u] == float('inf'):
                    continue
                for v, peso in grafo.vecinos(u):
                    if dist[u] + peso < dist[v]:
                        dist[v] = dist[u] + peso
        return dist

    import random
    random.seed(131)
    for _ in range(200):
        g2 = Grafo()
        n = random.randint(2, 8)
        for _ in range(random.randint(1, n * 2)):
            g2.agregar_arista(random.randrange(n), random.randrange(n),
                              random.randint(1, 20))
        d_dij = dijkstra(g2, 0)
        d_bf = bellman_ford(g2, 0)
        assert d_dij == d_bf, "Dijkstra y Bellman-Ford deben coincidir"

    # La razón del heap: sin él, sería O(V²)
    import time
    grande = Grafo()
    n = 2000
    for i in range(n):
        if i + 1 < n:
            grande.agregar_arista(i, i + 1, random.randint(1, 5))
        if i + 10 < n:
            grande.agregar_arista(i, i + 10, random.randint(1, 50))

    inicio = time.time()
    d_grande = dijkstra(grande, 0)
    t = time.time() - inicio
    print(f"\nGrafo de {n} vértices: {t*1000:.1f} ms")
    assert all(v < float('inf') for v in d_grande.values()), "todos alcanzables"

    print("\n✓ Todas las pruebas pasaron")
