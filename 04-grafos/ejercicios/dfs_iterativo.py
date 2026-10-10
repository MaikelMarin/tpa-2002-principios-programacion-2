"""
Ejercicio 4: DFS iterativo (Depth-First Search)
Dificultad: Básico

Explorar tan lejos como sea posible a lo largo de cada rama antes de
retroceder. Usa una pila (LIFO).

Complejidad: O(V + E)
"""


def dfs_iterativo(grafo, inicio):
    """Recorrido DFS iterativo usando una pila."""
    visitados = set()
    pila = [inicio]
    resultado = []
    while pila:
        vertice = pila.pop()
        if vertice not in visitados:
            visitados.add(vertice)
            resultado.append(vertice)
            for vecino, _ in reversed(grafo.vecinos(vertice)):
                if vecino not in visitados:
                    pila.append(vecino)
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
    resultado = dfs_iterativo(g, 0)
    print(f"DFS desde 0: {resultado}")
    assert resultado == [0, 1, 3, 4, 2]
    print("\n✓ Todas las pruebas pasaron")
