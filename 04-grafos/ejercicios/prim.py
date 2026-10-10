r"""
Ejercicio 16: Algoritmo de Prim (MST)
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - Kruskal (ejercicio 15): el otro algoritmo de MST, para comparar.
    - Cola de prioridad / heap (igual que Dijkstra, ejercicio 10).
    - Grafos ponderados.
    - Propiedad de corte (teoria.md §5.2).

PROBLEMA
    El mismo que Kruskal: hallar el Árbol de Expansión Mínima.

FONDO MATEMÁTICO
    La estrategia de Prim es la OPUESTA a Kruskal:

        Kruskal: recorre las ARISTAS en orden de peso y decide si
                 aceptarlas. Es "global".

        Prim: parte de UN VÉRTICE y hace crecer el árbol añadiendo
              siempre la arista más barata que lo conecte con un
              vértice exterior. Es "local".

    Ambos son codiciosos y ambos se apoyan en la propiedad de corte:
    la arista más barata que cruza el corte (árbol actual, resto del
    grafo) pertenece a un MST.

ESTRATEGIA

```python
def prim(grafo, inicio=0):
    visitados = set()
    mst = []
    cola = [(0, inicio, None)]           # (peso, vertice, padre)

    while cola and len(visitados) < len(grafo.vertices):
        peso, vertice, padre = heapq.heappop(cola)
        if vertice in visitados:
            continue
        visitados.add(vertice)
        if padre is not None:
            mst.append((padre, vertice, peso))
        for vecino, w in grafo.vecinos(vertice):
            if vecino not in visitados:
                heapq.heappush(cola, (w, vecino, vertice))
    return mst
```

    El heap contiene CANDIDATAS: aristas que conectan el árbol con el
    exterior. Siempre se extrae la más barata. Eso es exactamente la
    propiedad de corte aplicada iterativamente.

TRAZA paso a paso
    Grafo: 0─1(4), 0─2(1), 1─2(2), 1─3(5), 2─3(1), 2─4(3), 3─4(2)

    Inicio: visitados={}, cola=[(0,0,None)]

    pop (0,0,None) → visitar 0. mst=[] (no tiene padre)
        vecinos: 1(4), 2(1) → push (4,1,0), (1,2,0)
        cola = [(1,2,0), (4,1,0)]
        visitados = {0}

    pop (1,2,0) → visitar 2. mst = [(0,2,1)]
        vecinos: 0(1) ya, 1(2) push (2,1,2), 3(1) push (1,3,2), 4(3) push (3,4,2)
        cola = [(1,3,2), (2,1,2), (3,4,2), (4,1,0)]

    pop (1,3,2) → visitar 3. mst = [(0,2,1), (2,3,1)]
        vecinos: 1(5) push (5,1,3), 2(1) ya, 4(2) push (2,4,3)
        cola = [(2,1,2), (2,4,3), (3,4,2), (4,1,0), (5,1,3)]

    pop (2,1,2) → visitar 1. mst = [(0,2,1), (2,3,1), (2,1,2)]
        vecinos: todos visitados o ya en cola
        cola = [(2,4,3), (3,4,2), (4,1,0), (5,1,3)]

    pop (2,4,3) → visitar 4. mst += [(3,4,2)]
        Todos visitados.

    MST: (0,2,1), (2,3,1), (2,1,2), (3,4,2) → total 6

    Note que las aristas aceptadas son las mismas que en Kruskal
    (aunque en distinto orden): ambos encuentran el mismo MST.

COMPLEJIDAD
    Con heap binario: O((V + E) log V).
    Con lista simple (buscar el mínimo recorriendo): O(V²).
    Con heap de Fibonacci: O(E + V log V).

    Para grafos DENSOS, O(V²) con lista simple es competitivo porque
    el factor log se evita. Es justamente el caso donde Prim gana a
    Kruskal.

DEMOSTRACIÓN DE CORRECCIÓN
    Invariante: al inicio de cada iteración, el conjunto de aristas
    en `mst` es un subárbol que forma parte de algún MST.

    - Inicialización: vacío, trivial.
    - Conservación: se extrae la arista de menor peso que cruza el
      corte (árbol actual / resto). Por la propiedad de corte, esa
      arista pertenece a algún MST. Añadirla preserva que el
      resultado forme parte de un MST.
    - Al terminar se tienen n−1 aristas acíclicas que conectan todo:
      es un MST. ∎

CASOS LÍMITE
    - Grafo no conexo: Prim NO lo detecta. Devuelve solo el árbol del
      componente del vértice inicial. Hay que verificar conectividad.
    - Aristas con el mismo peso: el MST puede no ser único.
    - Un solo vértice: MST vacío, la arista de la semilla no se añade
      (padre es None).

COMPARACIÓN DIRECTA CON KRUSKAL
    Criterio           Prim                        Kruskal
    Complejidad        O(E log V)                  O(E log E)
    Mejor escenario    Grafos DENSOS               Grafos DISPERSOS
    Estructura         Heap + conjunto visitados    Union-Find
    Detecta no         No (devuelve parcial)        Sí (bosque visible)
    conexo
    Por dónde empieza  Un vértice dado              La arista más barata

    REGLA PRÁCTICA: si E >> V (denso), Prim. Si E ≈ V (disperso),
    Kruskal. En la práctica ambos sirven para la mayoría de los casos.
"""


import heapq


class Grafo:
    """Grafo no dirigido ponderado con lista de adyacencia."""

    def __init__(self):
        self.adyacencia = {}

    def agregar_arista(self, u, v, peso=1):
        if u not in self.adyacencia:
            self.adyacencia[u] = []
        if v not in self.adyacencia:
            self.adyacencia[v] = []
        self.adyacencia[u].append((v, peso))
        self.adyacencia[v].append((u, peso))

    def vecinos(self, v):
        return self.adyacencia.get(v, [])

    @property
    def vertices(self):
        return list(self.adyacencia.keys())


def prim(grafo, inicio=0):
    """MST por Prim. O((V+E) log V) con heap.

    Devuelve la lista de aristas (padre, vertice, peso) del MST.
    """
    visitados = set()
    mst = []
    cola = [(0, inicio, None)]             # (peso, vertice, padre)

    while cola and len(visitados) < len(grafo.vertices):
        peso, vertice, padre = heapq.heappop(cola)

        if vertice in visitados:
            continue

        visitados.add(vertice)
        if padre is not None:
            mst.append((padre, vertice, peso))

        # Añadir candidatas: aristas al exterior
        for vecino, w in grafo.vecinos(vertice):
            if vecino not in visitados:
                heapq.heappush(cola, (w, vecino, vertice))

    return mst


if __name__ == "__main__":
    g = Grafo()
    for u, v, w in [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5),
                    (2, 3, 1), (2, 4, 3), (3, 4, 2)]:
        g.agregar_arista(u, v, w)

    mst = prim(g)
    print("Árbol de Expansión Mínima (Prim):")
    total = 0
    for u, v, peso in mst:
        print(f"  {u} — {v}: {peso}")
        total += peso
    print(f"Peso total: {total}")

    # El MST óptimo de este grafo pesa 6 (verificado por fuerza bruta)
    assert total == 6, "el MST optimo de este grafo pesa 6 (verificado por fuerza bruta)"
    assert len(mst) == 4, "5 vértices → 4 aristas"

    # Verificación: conecta todo, sin ciclos
    class UnionFind:
        def __init__(self, n):
            self.padre = list(range(n))
        def encontrar(self, x):
            while self.padre[x] != x:
                self.padre[x] = self.padre[self.padre[x]]; x = self.padre[x]
            return x
        def union(self, x, y):
            rx, ry = self.encontrar(x), self.encontrar(y)
            if rx == ry:
                return False
            self.padre[rx] = ry
            return True

    uf = UnionFind(5)
    for u, v, _ in mst:
        assert uf.union(u, v), "no debe haber ciclos"
    assert len({uf.encontrar(i) for i in range(5)}) == 1, "debe conectar todo"

    # PRIM Y KRUSKAL deben dar el MISMO peso total
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "kruskal", "04-grafos/ejercicios/kruskal.py")
    mod = importlib.util.module_from_spec(spec)
    import sys
    sys.modules["kruskal_04"] = mod
    # No ejecutamos el módulo (tiene su __main__); solo pedimos la función
    with open("04-grafos/ejercicios/kruskal.py", encoding="utf-8") as f:
        src_kruskal = f.read().split('if __name__')[0]
    ns = {}
    exec(src_kruskal, ns)

    aristas = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5),
               (2, 3, 1), (2, 4, 3), (3, 4, 2)]
    mst_k = ns["kruskal"](5, aristas)
    total_k = sum(a[2] for a in mst_k)
    print(f"\nKruskal da peso {total_k}, Prim da peso {total}")
    assert total == total_k, "ambnos algoritmos deben dar el mismo MST"

    # Casos base
    assert prim(Grafo()) == [], "grafo vacío"

    uno = Grafo()
    uno.adyacencia = {0: []}
    assert prim(uno, 0) == [], "un vértice: MST vacío (la semilla no se añade)"

    dos = Grafo()
    dos.agregar_arista(0, 1, 7)
    assert prim(dos, 0) == [(0, 1, 7)], "dos vértices, una arista"

    # Grafo no conexo: Prim NO lo detecta, devuelve parcial
    no_conexo = Grafo()
    no_conexo.agregar_arista(0, 1, 1)
    no_conexo.agregar_arista(2, 3, 1)
    mst_nc = prim(no_conexo, 0)
    print(f"\nGrafo no conexo: Prim devuelve {len(mst_nc)} aristas (parcial)")
    assert len(mst_nc) == 1, "solo cubre el componente del vértice inicial"
    assert 2 not in {u for u, _, _ in mst_nc} and 2 not in {v for _, v, _ in mst_nc}

    # Verificación aleatoria: Prim == Kruskal en peso total
    import random
    random.seed(161)
    coincidencias = 0
    for _ in range(100):
        n = random.randint(2, 7)
        g2 = Grafo()
        aristas2 = []
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < 0.6:
                    w = random.randint(1, 30)
                    g2.agregar_arista(u, v, w)
                    aristas2.append((u, v, w))
        for i in range(n - 1):
            if not any((a == i and b == i + 1) or (a == i + 1 and b == i)
                       for a, b, _ in aristas2):
                w = random.randint(1, 30)
                g2.agregar_arista(i, i + 1, w)
                aristas2.append((i, i + 1, w))

        mst_p = prim(g2, 0)
        mst_k2 = ns["kruskal"](n, aristas2)
        if sum(a[2] for a in mst_p) == sum(a[2] for a in mst_k2):
            coincidencias += 1
        else:
            raise AssertionError(f"discrepancia con n={n}, {aristas2}")
    print(f"Prim == Kruskal en {coincidencias}/100 grafos aleatorios")

    # Eficiencia en grafo grande
    import time
    n = 2000
    g3 = Grafo()
    for i in range(n):
        if i + 1 < n:
            g3.agregar_arista(i, i + 1, random.randint(1, 100))
        if i + 5 < n:
            g3.agregar_arista(i, i + 5, random.randint(1, 100))
    inicio = time.time()
    mst3 = prim(g3, 0)
    t = time.time() - inicio
    print(f"\nGrafo de {n} vértices: {t*1000:.0f} ms, MST con {len(mst3)} aristas")
    assert len(mst3) == n - 1

    print("\n✓ Todas las pruebas pasaron")
