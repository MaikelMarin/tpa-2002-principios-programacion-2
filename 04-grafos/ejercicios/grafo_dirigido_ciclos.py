"""
Ejercicio 13: Detectar ciclos en grafo dirigido
Dificultad: Avanzado

Usa DFS con estados (BLANCO, GRIS, NEGRO) para detectar ciclos.
"""


BLANCO = 0  # No visitado
GRIS = 1    # En proceso
NEGRO = 2   # Terminado


def tiene_ciclo_dirigido(grafo):
    """Detecta ciclos en un grafo dirigido usando DFS con estados."""
    estado = {v: BLANCO for v in grafo.adyacencia}

    def dfs(v):
        estado[v] = GRIS
        for vecino, _ in grafo.vecinos(v):
            if estado[vecino] == GRIS:
                return True
            if estado[vecino] == BLANCO:
                if dfs(vecino):
                    return True
        estado[v] = NEGRO
        return False

    for vertice in grafo.adyacencia:
        if estado[vertice] == BLANCO:
            if dfs(vertice):
                return True
    return False


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
        def vecinos(self, v):
            return self.adyacencia.get(v, [])

    # Grafo con ciclo
    g1 = Grafo()
    g1.agregar_arista(0, 1)
    g1.agregar_arista(1, 2)
    g1.agregar_arista(2, 0)

    # Grafo sin ciclo (DAG)
    g2 = Grafo()
    g2.agregar_arista(0, 1)
    g2.agregar_arista(0, 2)
    g2.agregar_arista(1, 3)
    g2.agregar_arista(2, 3)

    print(f"Grafo 1 tiene ciclo: {tiene_ciclo_dirigido(g1)}")
    print(f"Grafo 2 tiene ciclo: {tiene_ciclo_dirigido(g2)}")

    assert tiene_ciclo_dirigido(g1) == True
    assert tiene_ciclo_dirigido(g2) == False
    print("\n✓ Todas las pruebas pasaron")
