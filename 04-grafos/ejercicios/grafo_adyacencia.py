r"""
Ejercicio 1: Grafo con lista de adyacencia
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Tabla hash (00-fundamentos §8.6): la lista de adyacencia es un
      diccionario de listas.
    - Grafo dirigido vs no dirigido (teoria.md §1.1): la diferencia
      cambia cómo se registran las aristas.

PROBLEMA
    Implementar un grafo con lista de adyacencia, con operaciones
    para añadir/eliminar vértices y aristas, y consultar vecinos.

FONDO MATEMÁTICO
    La lista de adyacencia almacena, para cada vértice, la lista de
    sus vecinos. Es la representación estándar porque su espacio es
    O(V + E), proporcional al tamaño REAL del grafo, no a V².

    Para un grafo NO DIRIGIDO, cada arista (u, v) aparece DOS veces:
    en la lista de u y en la de v. Eso es exactamente el Teorema del
    Saludo de Manos: Σ grado(v) = 2|E|.

ESTRATEGIA

```python
class Grafo:
    def __init__(self, dirigido=False):
        self.dirigido = dirigido
        self.adyacencia = {}          # vertice -> lista de (vecino, peso)

    def agregar_arista(self, u, v, peso=1):
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        self.adyacencia[u].append((v, peso))
        if not self.dirigido:
            self.adyacencia[v].append((u, peso))   # ← la clave
```

    El `if not self.dirigido` es lo que distingue ambos tipos. Sin él,
    un grafo no dirigido se volvería dirigo silenciosamente.

TRAZA de construcción
    agregar_arista(0, 1):
        adyacencia = {0: [], 1: []}
        adyacencia[0] = [(1, 1)]
        no dirigido → adyacencia[1] = [(0, 1)]

    agregar_arista(0, 2):
        adyacencia[0] = [(1,1), (2,1)]
        adyacencia[2] = [(0,1)]

    agregar_arista(1, 2):
        adyacencia[1] = [(0,1), (2,1)]
        adyacencia[2] = [(0,1), (1,1)]

    Resultado:
        0: [(1,1), (2,1)]
        1: [(0,1), (2,1)]
        2: [(0,1), (1,1)]

    Verificación: Σ grados = 2+2+2 = 6 = 2·3 aristas. ✓

COMPLEJIDAD DE CADA OPERACIÓN
    Operación                    Complejidad
    agregar_vertice              O(1)
    agregar_arista               O(1)
    eliminar_arista              O(grado)   [hay que filtrar la lista]
    eliminar_vertice             O(V + E)   [hay que limpiar todas las listas]
    vecinos(v)                   O(1)       [devolver la lista]
    ¿existe arista (u,v)?        O(grado(u))

    Note que eliminar_vertice es caro: hay que recorrer TODAS las
    listas quitando referencias al vértice eliminado. En un grafo
    grande eso es O(V + E).

COMPARACIÓN CON LA MATRIZ
    Operación           Lista          Matriz
    Espacio             O(V+E)         O(V²)
    ¿Existe arista?     O(grado)       O(1)     ← gana la matriz
    Vecinos             O(grado)       O(V)     ← gana la lista
    Añadir vértice      O(1)           O(V²)

    La matriz solo gana en la consulta puntual de existencia. Para
    todo lo demás (recorridos, que es el 90% del trabajo con grafos),
    la lista gana.

DETALLE: ¿POR QUÉ GUARDAR (vecino, peso) Y NO SOLO vecino?
    Porque así la misma estructura sirve para grafos ponderados y no
    ponderados. En los no ponderados el peso es siempre 1 y se ignora.
    Es una generalización gratuita: no cuesta nada y evita tener dos
    clases distintas.

RELACIÓN CON OTROS TEMAS
    - BFS y DFS (ejercicios 3-5) consumen esta estructura.
    - Dijkstra, Kruskal y Prim la usan con pesos reales.
"""


class Grafo:
    """Grafo con lista de adyacencia.

    Cada vértice mapea a una lista de tuplas (vecino, peso).
    Soporta grafos dirigidos y no dirigidos, con y sin pesos.
    """

    def __init__(self, dirigido=False):
        self.dirigido = dirigido
        self.adyacencia = {}

    def agregar_vertice(self, v):
        """Añade un vértice si no existe. O(1)."""
        if v not in self.adyacencia:
            self.adyacencia[v] = []

    def agregar_arista(self, u, v, peso=1):
        """Añade una arista. En no dirigido, la añade en ambos sentidos."""
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        self.adyacencia[u].append((v, peso))
        if not self.dirigido:
            self.adyacencia[v].append((u, peso))

    def eliminar_arista(self, u, v):
        """Elimina una arista. O(grado)."""
        self.adyacencia[u] = [(nodo, p) for nodo, p in self.adyacencia[u] if nodo != v]
        if not self.dirigido:
            self.adyacencia[v] = [(nodo, p) for nodo, p in self.adyacencia[v] if nodo != u]

    def eliminar_vertice(self, v):
        """Elimina un vértice y todas sus aristas. O(V + E)."""
        if v in self.adyacencia:
            del self.adyacencia[v]
            for u in self.adyacencia:
                self.adyacencia[u] = [(nodo, p) for nodo, p in self.adyacencia[u] if nodo != v]

    def vecinos(self, v):
        """Devuelve la lista de (vecino, peso). O(1)."""
        return self.adyacencia.get(v, [])

    def existe_arista(self, u, v):
        """¿Existe la arista (u, v)? O(grado(u))."""
        return any(nodo == v for nodo, _ in self.adyacencia.get(u, []))

    @property
    def vertices(self):
        return list(self.adyacencia.keys())

    def num_aristas(self):
        """Cuenta aristas. En no dirigido, suma grados y divide por 2."""
        total = sum(len(v) for v in self.adyacencia.values())
        return total if self.dirigido else total // 2

    def __repr__(self):
        return f"Grafo({self.adyacencia})"


if __name__ == "__main__":
    g = Grafo()                                    # no dirigido
    g.agregar_arista(0, 1)
    g.agregar_arista(0, 2)
    g.agregar_arista(1, 2)
    g.agregar_arista(1, 3)

    print(f"Grafo: {g}")
    print(f"Vértices: {g.vertices}")
    print(f"Aristas: {g.num_aristas()}")

    # El grafo es NO dirigido: la arista 0-1 aparece en AMBOS lados
    assert g.vecinos(1) == [(0, 1), (2, 1), (3, 1)]
    assert g.vecinos(0) == [(1, 1), (2, 1)]
    assert len(g.vecinos(1)) == 3, "el 1 tiene 3 vecinos: 0, 2 y 3"

    # Conteo de aristas correcto (no dirigido: suma de grados / 2)
    assert g.num_aristas() == 4

    # Teorema del Saludo de Manos: Σ grados = 2|E|
    suma_grados = sum(len(v) for v in g.adyacencia.values())
    print(f"\nSaludo de manos: Σ grados = {suma_grados} = 2·{g.num_aristas()}")
    assert suma_grados == 2 * g.num_aristas()

    # Existencia de aristas
    assert g.existe_arista(0, 1) is True
    assert g.existe_arista(0, 3) is False
    assert g.existe_arista(1, 0) is True, "no dirigido: también al revés"

    # Eliminar arista
    g.eliminar_arista(1, 2)
    assert g.existe_arista(1, 2) is False
    assert g.existe_arista(2, 1) is False, "se eliminó en ambos lados"
    assert g.num_aristas() == 3

    # Eliminar vértice
    g.eliminar_vertice(1)
    assert 1 not in g.adyacencia
    assert g.existe_arista(0, 1) is False, "las aristas al 1 desaparecieron"
    assert g.existe_arista(3, 1) is False
    assert g.num_aristas() == 1, "solo queda 0-2"

    # Grafo DIRIGIDO: la arista se registra en un solo sentido
    d = Grafo(dirigido=True)
    d.agregar_arista("A", "B")
    d.agregar_arista("B", "C")
    assert d.vecinos("A") == [("B", 1)]
    assert d.vecinos("B") == [("C", 1)], "en dirigido, B no apunta a A"
    assert d.vecinos("C") == []
    assert d.num_aristas() == 2, "en dirigido no se divide por 2"

    # Grafo PONDERADO
    p = Grafo(dirigido=True)
    p.agregar_arista("SJ", "Heredia", 12)
    p.agregar_arista("Heredia", "Alajuela", 15)
    assert p.vecinos("SJ") == [("Heredia", 12)], "el peso se conserva"

    # Vértice inexistente
    assert g.vecinos(999) == []
    assert g.existe_arista(999, 0) is False

    print("\n✓ Todas las pruebas pasaron")
