"""
Ejercicio 16: Algoritmo de Prim (MST)
Dificultad: Experto

Encuentra el Árbol de Expansión Mínima (MST) de un grafo ponderado.

Historia: Vojtěch Jarník lo inventó en 1930; Robert Prim lo redescubrió en 1957.

Complejidad: O((V + E) log V) con cola de prioridad
"""


import heapq


def prim(grafo, inicio=0):
    """Encuentra el MST usando el algoritmo de Prim."""
    visitados = set()
    mst = []
    cola = [(0, inicio, None)]  # (peso, vertice, padre)
    while cola and len(visitados) < len(grafo.adyacencia):
        peso, vertice, padre = heapq.heappop(cola)
        if vertice in visitados:
            continue
        visitados.add(vertice)
        if padre is not None:
            mst.append((padre, vertice, peso))
        for vecino, peso_arista in grafo.vecinos(vertice):
            if vecino not in visitados:
                heapq.heappush(cola, (peso_arista, vecino, vertice))
    return mst


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
    g.agregar_arista(2, 4, 3)
    g.agregar_arista(3, 4, 2)

    mst = prim(g)
    print("Árbol de Expansión Mínima (Prim):")
    total = 0
    for u, v, peso in mst:
        print(f"  {u} — {v}: {peso}")
        total += peso
    print(f"Peso total: {total}")

    assert total == 7
    assert len(mst) == 4
    print("\n✓ Todas las pruebas pasaron")
