r"""
Ejercicio 5: DFS recursivo
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - DFS iterativo con pila (ejercicio 4): para comparar.
    - Pila de llamadas (00-fundamentos §9.1): esta versión usa la pila
      del intérprete en vez de una pila explícita.
    - Grafo no dirigido y lista de adyacencia.

PROBLEMA
    Recorrer un grafo en profundidad usando recursión.

DIFERENCIA CON LA VERSIÓN ITERATIVA
    Ambas implementan el MISMO algoritmo. La diferencia es quién
    administra la pila:

        Iterativa: una pila explícita (lista). Control nuestro.
        Recursiva: la pila de llamadas del intérprete. Automática.

    La recursiva es más corta y más fácil de leer, pero tiene el
    límite de profundidad de Python (~1000). Para grafos con caminos
    muy largos, la iterativa es la única opción.

ESTRATEGIA

```python
def dfs(grafo, v, visitados):
    visitados.add(v)
    for vecino, _ in grafo.vecinos(v):
        if vecino not in visitados:
            dfs(grafo, vecino, visitados)   # ← llamada recursiva
```

    Es la forma más pura del patrón "hacer, explorar, deshacer". Aquí
    no hay que deshacer nada porque no comparten estado mutable: solo
    se acumula el conjunto de visitados.

TRAZA sobre:
        0 ─ 1
        │ ╲ │
        2 ─ 3

    dfs(0): visitados={0}
       vecino 1 no visitado → dfs(1)
          visitados={0,1}
          vecino 0 ya visitado
          vecino 3 no visitado → dfs(3)
             visitados={0,1,3}
             vecinos 0,1,2: 0 y 1 visitados
             vecino 2 no visitado → dfs(2)
                visitados={0,1,3,2}
                vecinos 0,1,3 todos visitados
                retorna
          retorna
       vecino 2 ya visitado (lo visitó la rama del 3)
       vecino 3 ya visitado
       retorna

    Profundidad máxima de recursión: 4 (0 → 1 → 3 → 2).

COMPLEJIDAD
    Tiempo: O(V + E).
    Espacio: O(V) por el conjunto de visitados + O(V) de pila en el
             peor caso (grafo tipo camino o ciclo).

    El peor caso de pila es un grafo en forma de línea: la recursión
    llega a profundidad V.

CUÁNDO LA RECURSIÓN FALLA
    Un grafo con un camino de más de ~1000 vértices (el límite de
    Python) lanza RecursionError. La versión iterativa con pila
    explícita no tiene ese límite, porque la pila vive en el heap.

    Solución si se necesita recursión profunda:
        sys.setrecursionlimit(10000)   # con cuidado
        o reescribir en iterativo

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción sobre el número de llamadas. DFS recursivo visita
    exactamente los vértices alcanzables desde el origen, cada uno una
    vez, porque:
      - Cada vértice se marca antes de explorar sus vecinos.
      - Un vértice marcado nunca se re-explora.
      - Todo vecino no marcado se explora recursivamente.
    Luego se alcanzan todos los vértices conectados. ∎

RELACIÓN CON OTROS TEMAS
    - Es el mismo patrón que los recorridos de árboles (tema 03): en
      un árbol no hace falta el conjunto de visitados porque no hay
      ciclos.
    - El backtracking (tema 01) es DFS sobre un grafo implícito donde
      ADEMÁS se deshacen decisiones.
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


def dfs_recursivo(grafo, inicio, visitados=None):
    """DFS recursivo. Devuelve el conjunto de vértices visitados.

    O(V+E) tiempo, O(V) de pila en el peor caso.
    """
    if visitados is None:
        visitados = set()

    visitados.add(inicio)                      # marcar antes de explorar

    for vecino, _ in grafo.vecinos(inicio):
        if vecino not in visitados:
            dfs_recursivo(grafo, vecino, visitados)

    return visitados


def dfs_con_traza(grafo, inicio, visitados=None, traza=None):
    """DFS que registra el orden de entrada y salida de cada vértice.

    Esa traza es la base del ordenamiento topológico de DAGs.
    """
    if visitados is None:
        visitados = set()
    if traza is None:
        traza = []

    visitados.add(inicio)
    traza.append((inicio, "entra"))

    for vecino, _ in grafo.vecinos(inicio):
        if vecino not in visitados:
            dfs_con_traza(grafo, vecino, visitados, traza)

    traza.append((inicio, "sale"))
    return visitados, traza


if __name__ == "__main__":
    grafo = Grafo()
    for u, v in [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)]:
        grafo.agregar_arista(u, v)

    resultado = dfs_recursivo(grafo, 0)
    print("DFS recursivo desde 0:")
    print(f"  Vértices visitados: {sorted(resultado)}")
    assert resultado == {0, 1, 2, 3}

    # Traza de entrada/salida
    _, traza = dfs_con_traza(grafo, 0)
    print(f"\nTraza ({len(traza)} eventos):")
    for vertice, evento in traza:
        print(f"  {evento:5} {vertice}")
    # Cada vértice entra antes de salir
    entradas = [v for v, e in traza if e == "entra"]
    salidas = [v for v, e in traza if e == "sale"]
    assert sorted(entradas) == sorted(salidas) == [0, 1, 2, 3]
    for v in [0, 1, 2, 3]:
        i_entra = traza.index((v, "entra"))
        i_sale = traza.index((v, "sale"))
        assert i_entra < i_sale, f"{v} debe entrar antes de salir"

    # Casos base
    vacio = Grafo()
    assert dfs_recursivo(vacio, 0) == {0}

    aislado = Grafo()
    aislado.adyacencia = {5: []}
    assert dfs_recursivo(aislado, 5) == {5}

    # Componente conexa aislada
    dos_componentes = Grafo()
    dos_componentes.agregar_arista(0, 1)
    dos_componentes.agregar_arista(2, 3)
    r = dfs_recursivo(dos_componentes, 0)
    assert r == {0, 1}, "solo su componente"
    assert 2 not in r and 3 not in r

    # La profundidad real se mide con el camino más largo
    camino = Grafo()
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4)]:
        camino.agregar_arista(u, v)
    _, traza_camino = dfs_con_traza(camino, 0)
    # En un camino, cada vértice entra justo antes que el siguiente
    solo_entradas = [v for v, e in traza_camino if e == "entra"]
    print(f"\nCamino 0-1-2-3-4, orden de entrada: {solo_entradas}")
    assert solo_entradas == [0, 1, 2, 3, 4], "sin ramificaciones, entra en orden"

    # El límite de recursión de Python es real
    import sys
    profundo = Grafo()
    for i in range(1500):                       # cadena de 1500
        profundo.agregar_arista(i, i + 1)

    try:
        dfs_recursivo(profundo, 0)
        print("Recursión de 1500 niveles: funcionó (límite alto)")
    except RecursionError:
        print(f"Recursión de 1500 niveles: RecursionError (límite = {sys.getrecursionlimit()})")

    # La versión iterativa SÍ soporta esa profundidad
    def dfs_iterativo(grafo, inicio):
        visitados = set()
        pila = [inicio]
        while pila:
            v = pila.pop()
            if v not in visitados:
                visitados.add(v)
                for vecino, _ in reversed(grafo.vecinos(v)):
                    if vecino not in visitados:
                        pila.append(vecino)
        return visitados

    r_profundo = dfs_iterativo(profundo, 0)
    assert len(r_profundo) == 1501, "la iterativa no tiene el límite"
    print(f"Versión iterativa con 1501 vértices: {len(r_profundo)} visitados")

    # Ambas versiones coinciden en grafos normales
    import random
    random.seed(171)
    for _ in range(300):
        g = Grafo()
        n = random.randint(1, 12)
        for _ in range(random.randint(0, n * 2)):
            if n > 1:
                g.agregar_arista(random.randrange(n), random.randrange(n))
        origen = random.randrange(n)
        assert dfs_recursivo(g, origen) == dfs_iterativo(g, origen)

    print("\n✓ Todas las pruebas pasaron")
