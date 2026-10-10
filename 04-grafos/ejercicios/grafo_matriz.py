"""
Ejercicio 2: Grafo con matriz de adyacencia
Dificultad: Básico

Implementación de un grafo usando matriz de adyacencia.
"""


class GrafoMatriz:
    def __init__(self, n, dirigido=False):
        self.n = n
        self.dirigido = dirigido
        self.matriz = [[0] * n for _ in range(n)]

    def agregar_arista(self, u, v, peso=1):
        self.matriz[u][v] = peso
        if not self.dirigido:
            self.matriz[v][u] = peso

    def eliminar_arista(self, u, v):
        self.matriz[u][v] = 0
        if not self.dirigido:
            self.matriz[v][u] = 0

    def hay_arista(self, u, v):
        return self.matriz[u][v] != 0

    def vecinos(self, v):
        return [i for i in range(self.n) if self.matriz[v][i] != 0]

    def __repr__(self):
        return f"GrafoMatriz({self.matriz})"


if __name__ == "__main__":
    g = GrafoMatriz(4)
    g.agregar_arista(0, 1)
    g.agregar_arista(0, 2)
    g.agregar_arista(1, 2)
    g.agregar_arista(1, 3)

    print(f"Grafo: {g}")
    print(f"Vecinos de 1: {g.vecinos(1)}")

    assert g.hay_arista(0, 1) == True
    assert g.hay_arista(0, 3) == False
    assert g.vecinos(1) == [0, 2, 3]
    print("\n✓ Todas las pruebas pasaron")
