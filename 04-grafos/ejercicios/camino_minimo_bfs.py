"""
Ejercicio 7: Camino más corto con BFS
Dificultad: Intermedio

Encuentra el camino más corto entre dos vértices en un grafo no ponderado.
"""


from collections import deque


def camino_minimo_bfs(grafo, inicio, destino):
    """Encuentra el camino más corto usando BFS."""
    if inicio == destino:
        return [inicio]
    visitados = {inicio}
    cola = deque([(inicio, [inicio])])
    while cola:
        vertice, camino = cola.popleft()
        for vecino, _ in grafo.vecinos(vertice):
            if vecino == destino:
                return camino + [vecino]
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino + [vecino]))
    return None


if __name__ == "__main__":
    grafo = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 4],
        3: [1, 5],
        4: [1, 2, 5],
        5: [3, 4]
    }

    class GrafoDict:
        def __init__(self, adyacencia):
            self.adyacencia = adyacencia
        def vecinos(self, v):
            return [(n, 1) for n in self.adyacencia.get(v, [])]

    g = GrafoDict(grafo)
    camino = camino_minimo_bfs(g, 0, 5)
    print(f"Camino más corto de 0 a 5: {camino}")
    assert camino == [0, 1, 3, 5] or camino == [0, 1, 4, 5] or camino == [0, 2, 4, 5]
    print("\n✓ Todas las pruebas pasaron")
