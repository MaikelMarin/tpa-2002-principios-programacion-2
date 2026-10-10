"""
Ejercicio 10: Algoritmo de Dijkstra
Dificultad: Avanzado

Encuentra el camino más corto desde un origen a todos los demás vértices
en un grafo ponderado con pesos no negativos.

Historia: Edsger Dijkstra lo inventó en 1959.

Complejidad: O((V + E) log V) con cola de prioridad
"""


import heapq


def dijkstra(grafo, inicio):
    """Calcula las distancias más cortas desde inicio a todos los vértices."""
    distancias = {v: float('inf') for v in grafo.adyacencia}
    distancias[inicio] = 0
    cola = [(0, inicio)]
    while cola:
        dist_actual, vertice = heapq.heappop(cola)
        if dist_actual > distancias[vertice]:
            continue
        for vecino, peso in grafo.vecinos(vertice):
            nueva_dist = dist_actual + peso
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                heapq.heappush(cola, (nueva_dist, vecino))
    return distancias


if __name__ == "__main__":
    class Grafo:
        def __init__(self):
            self.adyacencia = {}
        def agregar_arista(self, u, v, peso):
            if u not in self.adyacencia:
                self.adyacencia[u] = []
            if v not in self.adyacencia:
                self.adyacencia[v] = []
            self.adyacencia[u].append((v, peso))
            self.adyacencia[v].append((u, peso))
        def vecinos(self, v):
            return self.adyacencia.get(v, [])

    g = Grafo()
    g.agregar_arista(0, 1, 4)
    g.agregar_arista(0, 2, 1)
    g.agregar_arista(1, 2, 2)
    g.agregar_arista(1, 3, 5)
    g.agregar_arista(2, 3, 1)

    distancias = dijkstra(g, 0)
    print("Distancias desde 0:")
    for v, d in sorted(distancias.items()):
        print(f"  0 → {v}: {d}")

    assert distancias[0] == 0
    assert distancias[1] == 3
    assert distancias[2] == 1
    assert distancias[3] == 2
    print("\n✓ Todas las pruebas pasaron")
