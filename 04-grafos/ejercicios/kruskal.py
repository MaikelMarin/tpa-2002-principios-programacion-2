"""
Ejercicio 15: Algoritmo de Kruskal (MST)
Dificultad: Experto

Encuentra el Árbol de Expansión Mínima (MST) de un grafo ponderado.

Historia: Joseph Kruskal lo publicó en 1956.

Complejidad: O(E log E)
"""


class UnionFind:
    def __init__(self, n):
        self.padre = list(range(n))
        self.rango = [0] * n

    def encontrar(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.encontrar(self.padre[x])
        return self.padre[x]

    def union(self, x, y):
        raiz_x = self.encontrar(x)
        raiz_y = self.encontrar(y)
        if raiz_x == raiz_y:
            return False
        if self.rango[raiz_x] < self.rango[raiz_y]:
            self.padre[raiz_x] = raiz_y
        elif self.rango[raiz_x] > self.rango[raiz_y]:
            self.padre[raiz_y] = raiz_x
        else:
            self.padre[raiz_y] = raiz_x
            self.rango[raiz_x] += 1
        return True


def kruskal(num_vertices, aristas):
    """Encuentra el MST usando el algoritmo de Kruskal."""
    aristas_ordenadas = sorted(aristas, key=lambda x: x[2])
    uf = UnionFind(num_vertices)
    mst = []
    for u, v, peso in aristas_ordenadas:
        if uf.union(u, v):
            mst.append((u, v, peso))
            if len(mst) == num_vertices - 1:
                break
    return mst


if __name__ == "__main__":
    aristas = [
        (0, 1, 4), (0, 2, 1), (1, 2, 2),
        (1, 3, 5), (2, 3, 1), (2, 4, 3),
        (3, 4, 2)
    ]

    mst = kruskal(5, aristas)
    print("Árbol de Expansión Mínima (Kruskal):")
    total = 0
    for u, v, peso in mst:
        print(f"  {u} — {v}: {peso}")
        total += peso
    print(f"Peso total: {total}")

    assert total == 7
    assert len(mst) == 4
    print("\n✓ Todas las pruebas pasaron")
