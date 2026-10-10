"""
Ejercicio 1: Grafo con lista de adyacencia
Dificultad: Básico

Implementación de un grafo usando lista de adyacencia.
"""


class Grafo:
    def __init__(self, dirigido=False):
        self.dirigido = dirigido
        self.adyacencia = {}

    def agregar_vertice(self, v):
        if v not in self.adyacencia:
            self.adyacencia[v] = []

    def agregar_arista(self, u, v, peso=1):
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        self.adyacencia[u].append((v, peso))
        if not self.dirigido:
            self.adyacencia[v].append((u, peso))

    def eliminar_arista(self, u, v):
        self.adyacencia[u] = [(nodo, p) for nodo, p in self.adyacencia[u] if nodo != v]
        if not self.dirigido:
            self.adyacencia[v] = [(nodo, p) for nodo, p in self.adyacencia[v] if nodo != u]

    def eliminar_vertice(self, v):
        if v in self.adyacencia:
            del self.adyacencia[v]
            for u in self.adyacencia:
                self.adyacencia[u] = [(nodo, p) for nodo, p in self.adyacencia[u] if nodo != v]

    def vecinos(self, v):
        return self.adyacencia.get(v, [])

    def __repr__(self):
        return f"Grafo({self.adyacencia})"


if __name__ == "__main__":
    g = Grafo()
    g.agregar_arista(0, 1)
    g.agregar_arista(0, 2)
    g.agregar_arista(1, 2)
    g.agregar_arista(1, 3)

    print(f"Grafo: {g}")
    print(f"Vecinos de 1: {g.vecinos(1)}")

    assert g.vecinos(1) == [(2, 1), (3, 1)]
    assert g.vecinos(0) == [(1, 1), (2, 1)]
    print("\n✓ Todas las pruebas pasaron")
