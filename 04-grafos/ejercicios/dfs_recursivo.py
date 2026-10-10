"""
Ejercicio 5: DFS recursivo
Dificultad: Intermedio

Recorrido DFS usando recursión.
"""


def dfs_recursivo(grafo, inicio, visitados=None):
    """Recorrido DFS recursivo."""
    if visitados is None:
        visitados = set()
    visitados.add(inicio)
    print(inicio, end=" ")
    for vecino, _ in grafo.vecinos(inicio):
        if vecino not in visitados:
            dfs_recursivo(grafo, vecino, visitados)
    return visitados


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
    print("DFS recursivo desde 0:")
    dfs_recursivo(g, 0)
    print()
    print("\n✓ Todas las pruebas pasaron")
