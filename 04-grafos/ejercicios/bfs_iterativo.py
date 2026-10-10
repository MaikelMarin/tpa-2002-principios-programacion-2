r"""
Ejercicio 3: BFS iterativo (Breadth-First Search)
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Cola (00-fundamentos §8.5): la estructura que hace funcionar BFS.
    - Lista de adyacencia (ejercicio 1): la representación que consume.
    - Invariantes de bucle (§6.4): la corrección se apoya en uno.

PROBLEMA
    Recorrer un grafo por niveles, desde un vértice origen.

FONDO MATEMÁTICO
    BFS visita los vértices en orden NO DECRECIENTE de distancia al
    origen. Esa propiedad es la que lo hace el algoritmo correcto
    para el camino más corto en grafos no ponderados.

    La razón es la cola (FIFO): si se descubren los vértices a
    distancia d+1 al procesar los de distancia d, y la cola los
    atiende en orden de llegada, entonces ningún vértice a distancia
    d+2 puede visitarse antes de que se terminen los de d+1.

ESTRATEGIA

```python
def bfs(grafo, inicio):
    visitados = {inicio}          # ← marcar al ENCOLAR, no al desencolar
    cola = deque([inicio])
    while cola:
        v = cola.popleft()
        visitar(v)
        for vecino, _ in grafo.vecinos(v):
            if vecino not in visitados:
                visitados.add(vecino)     # ← aquí también
                cola.append(vecino)
```

    DETALLE CRÍTICO: marcar al ENCOLAR, no al desencolar.
    Si se marca al desencolar, el mismo vértice puede entrar varias
    veces a la cola (descubierto por distintos caminos), lo que
    duplica trabajo y puede inflar la cola a O(E) en vez de O(V).

TRAZA sobre el grafo:
        0 ─ 1
        │ ╲ │
        2 ─ 3

    cola = [0], visitados = {0}

    pop 0 → visitar 0. Vecinos: 1, 2.
       1 no visitado → visitados={0,1}, cola=[1]
       2 no visitado → visitados={0,1,2}, cola=[1,2]
    pop 1 → visitar 1. Vecinos: 0, 2, 3.
       0 ya visitado. 2 ya visitado.
       3 no visitado → visitados={0,1,2,3}, cola=[2,3]
    pop 2 → visitar 2. Vecinos: 0, 1, 3. Todos visitados.
    pop 3 → visitar 3. Vecinos: 1. Ya visitado.

    Orden de visita: 0, 1, 2, 3
    Distancias: 0→0, 1→1, 2→1, 3→2

    Verificación: el orden es no decreciente en distancia. ✓

DEMOSTRACIÓN DE CORRECCIÓN
    Invariante: en cada momento, la cola contiene exactamente los
    vértices descubiertos y aún no visitados, en orden no decreciente
    de distancia.

    - Inicialización: solo el origen (distancia 0).
    - Conservación: al visitar v (distancia d), sus vecinos no
      visitados tienen distancia d+1 y se añaden al final, detrás de
      los de distancia d que aún estaban. El invariante se preserva.
    - Terminación: la cola se vacía; todos los vértices alcanzables
      se visitaron exactamente una vez. ∎

COMPLEJIDAD
    Tiempo: O(V + E). Cada vértice se encola/desencola una vez; cada
    arista se examina una vez desde cada extremo (2E en no dirigido,
    pero E en dirigido).
    Espacio: O(V) para la cola y el conjunto de visitados.

APLICACIONES
    - Camino más corto en grafos no ponderados (guardando predecesores).
    - Grados de separación en redes sociales.
    - Componentes conexos.
    - Verificar si un grafo es bipartito (coloreando por BFS).
    - Web crawling nivel por nivel.

RELACIÓN CON OTROS TEMAS
    - El recorrido por niveles de un ÁRBOL (ejercicio 2 del tema 03)
      es BFS con una diferencia: en un árbol no hace falta el conjunto
      de visitados, porque no hay ciclos que puedan causar revisitas.
    - Dijkstra (ejercicio 10) es una generalización de BFS con pesos:
      en vez de una cola FIFO, usa una cola de prioridad.
"""


class Grafo:
    """Grafo no dirigido con lista de adyacencia."""

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


def bfs(grafo, inicio):
    """BFS iterativo. O(V + E) tiempo, O(V) espacio.

    Devuelve la lista de vértices en orden de visita.
    """
    from collections import deque

    visitados = {inicio}
    cola = deque([inicio])
    resultado = []

    while cola:
        vertice = cola.popleft()
        resultado.append(vertice)
        for vecino, _ in grafo.vecinos(vertice):
            if vecino not in visitados:
                visitados.add(vecino)          # marcar al ENCOLAR
                cola.append(vecino)

    return resultado


def distancias_bfs(grafo, inicio):
    """Calcula la distancia mínima a cada vértice (sin pesos).

    BFS garantiza distancias correctas porque visita en orden de
    distancia creciente.
    """
    from collections import deque

    dist = {inicio: 0}
    cola = deque([inicio])

    while cola:
        vertice = cola.popleft()
        for vecino, _ in grafo.vecinos(vertice):
            if vecino not in dist:
                dist[vecino] = dist[vertice] + 1
                cola.append(vecino)

    return dist


if __name__ == "__main__":
    # Grafo de prueba:
    #   0 ─ 1
    #   │ ╲ │
    #   2 ─ 3
    grafo = Grafo()
    for u, v in [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)]:
        grafo.agregar_arista(u, v)

    resultado = bfs(grafo, 0)
    print(f"BFS desde 0: {resultado}")
    assert resultado[0] == 0, "empieza por el origen"

    # Todos los vértices alcanzables se visitan una sola vez
    assert sorted(resultado) == [0, 1, 2, 3]
    assert len(resultado) == len(set(resultado)), "sin repetidos"

    # Distancias correctas
    dist = distancias_bfs(grafo, 0)
    print(f"Distancias: {dist}")
    assert dist[0] == 0
    assert dist[1] == 1
    assert dist[2] == 1
    assert dist[3] == 1, "0-3 está conectado directamente"

    # En una cadena, las distancias son las posiciones
    cadena = Grafo()
    for u, v in [(1, 2), (2, 3), (3, 4)]:
        cadena.agregar_arista(u, v)
    d_cadena = distancias_bfs(cadena, 1)
    print(f"\nCadena 1-2-3-4, distancias desde 1: {d_cadena}")
    assert d_cadena == {1: 0, 2: 1, 3: 2, 4: 3}

    # Camino más corto: BFS da el mínimo número de aristas
    estrella = Grafo()
    estrella.agregar_arista(0, 1)
    estrella.agregar_arista(0, 2)
    estrella.agregar_arista(0, 3)
    d_estr = distancias_bfs(estrella, 0)
    assert all(d == 1 for k, d in d_estr.items() if k != 0)

    # Componente conexa: solo se alcanzan los conectados
    dos_componentes = Grafo()
    dos_componentes.agregar_arista(0, 1)
    dos_componentes.agregar_arista(2, 3)          # componente separada
    r = bfs(dos_componentes, 0)
    print(f"\nGrafo con dos componentes, BFS desde 0: {r}")
    assert sorted(r) == [0, 1], "no se alcanza la otra componente"
    assert 2 not in r and 3 not in r

    # Grafo vacío y caso base
    vacio = Grafo()
    assert bfs(vacio, 0) == [0], "el origen siempre se visita"
    assert distancias_bfs(vacio, 0) == {0: 0}

    # Un solo vértice aislado
    aislado = Grafo()
    aislado.adyacencia = {5: []}
    assert bfs(aislado, 5) == [5]

    # Verificación: BFS desde cualquier vértice visita todos los
    # vértices de su componente conexa
    import random
    random.seed(111)
    for _ in range(200):
        g = Grafo()
        n = random.randint(1, 12)
        for _ in range(random.randint(0, n * 2)):
            if n > 1:
                g.agregar_arista(random.randrange(n), random.randrange(n))
        origen = random.randrange(n)
        vistos = set(bfs(g, origen))
        # Todos los vértices de la componente deben aparecer
        assert origen in vistos
        # Cada arista debe tener ambos extremos visitados
        for u in vistos:
            for vecino, _ in g.vecinos(u):
                assert vecino in vistos, "BFS debe alcanzar a todo vecino"

    print("\n✓ Todas las pruebas pasaron")
