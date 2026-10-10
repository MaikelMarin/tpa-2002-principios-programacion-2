"""
Ejercicio 3: BFS iterativo (Breadth-First Search)
Dificultad: Básico

Explorar todos los vecinos de un vértice antes de pasar al siguiente nivel.
Usa una cola (FIFO).

Complejidad: O(V + E)
"""


from collections import deque


def bfs(grafo, inicio):
    """Recorrido BFS desde un vértice inicial."""
    visitados = set()
    cola = deque([inicio])
    visitados.add(inicio)
    resultado = []
    while cola:
        vertice = cola.popleft()
        resultado.append(vertice)
        for vecino, _ in grafo.vecinos(vertice):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)
    return resultado


if __name__ == "__main__":
    grafo = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 4],
        3: [1],
        4: [1, 2]
    }

    class GrafoDict:
        def __init__(self, adyacencia):
            self.adyacencia = adyacencia
        def vecinos(self, v):
            return [(n, 1) for n in self.adyacencia.get(v, [])]

    g = GrafoDict(grafo)
    resultado = bfs(g, 0)
    print(f"BFS desde 0: {resultado}")
    assert resultado == [0, 1, 2, 3, 4]
    print("\n✓ Todas las pruebas pasaron")
