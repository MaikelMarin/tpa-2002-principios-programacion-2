"""
Ejercicio 11: Grafo bipartito
Dificultad: Avanzado

Un grafo es bipartito si sus vértices se pueden dividir en dos conjuntos
disjuntos de manera que toda arista conecte vértices de conjuntos diferentes.

Se detecta intentando colorear el grafo con 2 colores.
"""


from collections import deque


def es_bipartito(grafo):
    """Verifica si un grafo es bipartito usando BFS con coloreo."""
    color = {}
    for inicio in grafo.adyacencia:
        if inicio in color:
            continue
        color[inicio] = 0
        cola = deque([inicio])
        while cola:
            vertice = cola.popleft()
            for vecino, _ in grafo.vecinos(vertice):
                if vecino not in color:
                    color[vecino] = 1 - color[vertice]
                    cola.append(vecino)
                elif color[vecino] == color[vertice]:
                    return False
    return True


if __name__ == "__main__":
    class Grafo:
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

    # Grafo bipartito (cuadrado)
    g1 = Grafo()
    g1.agregar_arista(0, 1)
    g1.agregar_arista(1, 2)
    g1.agregar_arista(2, 3)
    g1.agregar_arista(3, 0)

    # Grafo no bipartito (triángulo)
    g2 = Grafo()
    g2.agregar_arista(0, 1)
    g2.agregar_arista(1, 2)
    g2.agregar_arista(2, 0)

    print(f"Grafo 1 bipartito: {es_bipartito(g1)}")
    print(f"Grafo 2 bipartito: {es_bipartito(g2)}")

    assert es_bipartito(g1) == True
    assert es_bipartito(g2) == False
    print("\n✓ Todas las pruebas pasaron")
