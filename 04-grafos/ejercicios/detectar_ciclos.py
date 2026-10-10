"""
Ejercicio 6: Detectar ciclos en grafo no dirigido
Dificultad: Intermedio

Usa DFS para detectar ciclos. Si se encuentra un vecino ya visitado
que no es el padre, hay ciclo.
"""


def tiene_ciclo(grafo):
    """Detecta si un grafo no dirigido tiene ciclos."""
    visitados = set()

    def dfs(v, padre):
        visitados.add(v)
        for vecino, _ in grafo.vecinos(v):
            if vecino not in visitados:
                if dfs(vecino, v):
                    return True
            elif vecino != padre:
                return True
        return False

    for vertice in grafo.adyacencia:
        if vertice not in visitados:
            if dfs(vertice, None):
                return True
    return False


if __name__ == "__main__":
    # Grafo con ciclo
    grafo1 = {
        0: [1, 2],
        1: [0, 2],
        2: [0, 1]
    }

    # Grafo sin ciclo (árbol)
    grafo2 = {
        0: [1, 2],
        1: [0],
        2: [0]
    }

    class GrafoDict:
        def __init__(self, adyacencia):
            self.adyacencia = adyacencia
        def vecinos(self, v):
            return [(n, 1) for n in self.adyacencia.get(v, [])]

    g1 = GrafoDict(grafo1)
    g2 = GrafoDict(grafo2)

    print(f"Grafo 1 tiene ciclo: {tiene_ciclo(g1)}")
    print(f"Grafo 2 tiene ciclo: {tiene_ciclo(g2)}")

    assert tiene_ciclo(g1) == True
    assert tiene_ciclo(g2) == False
    print("\n✓ Todas las pruebas pasaron")
