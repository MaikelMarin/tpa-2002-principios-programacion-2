r"""
Ejercicio 15: Algoritmo de Kruskal (MST)
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - Union-Find con compresión de caminos (abajo).
    - Ordenamiento (tema 02): Kruskal se apoya en ordenar aristas.
    - Propiedad de corte del MST (teoria.md §5.2).
    - Grafos ponderados (ejercicio 1).

PROBLEMA
    Dado un grafo conexo ponderado, hallar el subconjunto de aristas
    de peso total MÍNIMO que conecta todos los vértices sin formar
    ciclos: el Árbol de Expansión Mínima (MST).

FONDO MATEMÁTICO
    Un MST de un grafo con n vértices tiene exactamente n−1 aristas.
    La estrategia codiciosa de Kruskal:

        Ordenar las aristas por peso ascendente. Añadir cada arista si
        NO forma un ciclo con las ya seleccionadas.

    ¿Por qué funciona? Por la PROPIEDAD DE CORTE:
        En todo corte del grafo, la arista de peso mínimo que lo cruce
        pertenece a algún MST.

    Como las aristas se procesan en orden ascendente y cada una se
    acepta solo si une dos componentes distintas (cruza un corte real),
    cada arista aceptada satisface la propiedad y pertenece a un MST.

LA ESTRUCTURA CLAVE: UNION-FIND
    Para detectar ciclos eficientemente se usa Union-Find
    (conjuntos disjuntos):

        encontrar(x): ¿a qué componente pertenece x?
        union(x, y): une dos componentes. Devuelve False si ya estaban
                     en la misma (lo que indicaría un ciclo).

    Dos optimizaciones lo hacen casi O(1) amortizado:
      1. Compresión de caminos: al buscar, se apunta todo el camino
         directamente a la raíz.
      2. Unión por rango/altura: se cuelga el árbol más chico del más
         grande.

    Con ambas, el coste por operación es O(α(n)), donde α es la
    inversa de la función de Ackermann. Para cualquier n práctico,
    α(n) ≤ 5. Es decir: EFECTIVAMENTE CONSTANTE.

TRAZA de union-find
    Componentes: {0}, {1}, {2}, {3}

    union(0, 1) → ¿misma raíz? No → unir. Componentes: {0,1}, {2}, {3}
    union(1, 2) → encontrar(1) va a la raíz del {0,1}; encontrar(2)={2}
                  → distintas → unir. Componentes: {0,1,2}, {3}
    union(0, 2) → encontrar(0)=encontrar(2) → MISMA → devuelve False
                  (añadir esta arista formaría un ciclo)

IMPLEMENTACIÓN

```python
class UnionFind:
    def __init__(self, n):
        self.padre = list(range(n))
        self.rango = [0] * n

    def encontrar(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.encontrar(self.padre[x])   # compresión
        return self.padre[x]

    def union(self, x, y):
        rx, ry = self.encontrar(x), self.encontrar(y)
        if rx == ry:
            return False                    # mismo componente
        if self.rango[rx] < self.rango[ry]:
            self.padre[rx] = ry             # cuelga el chico del grande
        elif self.rango[rx] > self.rango[ry]:
            self.padre[ry] = rx
        else:
            self.padre[ry] = rx
            self.rango[rx] += 1
        return True

def kruskal(n, aristas):
    aristas.sort(key=lambda a: a[2])         # O(E log E)
    uf = UnionFind(n)
    mst = []
    for u, v, peso in aristas:
        if uf.union(u, v):                   # une componentes distintas
            mst.append((u, v, peso))
    return mst
```

COMPLEJIDAD
    Tiempo: O(E log E). Dominado por el ordenamiento. Las operaciones
    de Union-Find son O(α(n)) amortizado, despreciables.
    Espacio: O(V) para la estructura.

    Como E ≤ V², O(E log E) = O(E log V) también.

DEMOSTRACIÓN DE CORRECCIÓN
    Por la propiedad de corte (teorema §5.2). Cada arista aceptada
    cruza un corte entre dos componentes distintas, y es la de menor
    peso que lo hace (porque se procesan en orden ascendente y las
    anteriores que cruzaban ese corte ya fueron rechazadas o formaban
    ciclos). Luego cada arista aceptada pertenece a un MST. El
    resultado tiene n−1 aristas y es acíclico, luego es un MST. ∎

COMPARACIÓN CON PRIM
    Criterio        Kruskal                    Prim
    Enfoque         Sobre aristas              Sobre vértices
    Estructura      Union-Find                 Cola de prioridad
    Mejor para      Grafos dispersos           Grafos densos
    Complejidad     O(E log E)                 O(E log V) con heap
    Simple de       Sí                         Algo más compleja
    implementar

CASOS LÍMITE
    - Grafo no conexo: kruskal devuelve un BOSQUE de expansión
      mínima, no un árbol único. Hay que verificar la conectividad
      por separado.
    - Aristas con el mismo peso: el orden entre ellas es arbitrario;
      el MST sigue siendo válido pero puede no ser único.
    - Grafo de un solo vértice: MST vacío.
"""


class UnionFind:
    """Conjuntos disjuntos con compresión de caminos y unión por rango."""

    def __init__(self, n):
        self.padre = list(range(n))
        self.rango = [0] * n

    def encontrar(self, x):
        # Compresión de caminos: apuntar todo a la raíz
        if self.padre[x] != x:
            self.padre[x] = self.encontrar(self.padre[x])
        return self.padre[x]

    def union(self, x, y):
        rx, ry = self.encontrar(x), self.encontrar(y)
        if rx == ry:
            return False                     # ya estaban juntos: ciclo
        # Unión por rango: cuelga el árbol más chico del más grande
        if self.rango[rx] < self.rango[ry]:
            self.padre[rx] = ry
        elif self.rango[rx] > self.rango[ry]:
            self.padre[ry] = rx
        else:
            self.padre[ry] = rx
            self.rango[rx] += 1
        return True


def kruskal(num_vertices, aristas):
    """MST por Kruskal. O(E log E).

    Devuelve la lista de aristas (u, v, peso) del MST.
    """
    aristas_ordenadas = sorted(aristas, key=lambda a: a[2])
    uf = UnionFind(num_vertices)
    mst = []

    for u, v, peso in aristas_ordenadas:
        if uf.union(u, v):                   # une componentes distintas
            mst.append((u, v, peso))
            if len(mst) == num_vertices - 1:
                break                        # ya está completo

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

    # El MST óptimo de este grafo pesa 6 (verificado por fuerza bruta)
    assert total == 6, "el MST optimo de este grafo pesa 6 (verificado por fuerza bruta)"
    assert len(mst) == 4, "un MST de 5 vértices tiene 4 aristas"

    # Verificación: el MST conecta todos los vértices y es acíclico
    def verificar_mst(n, mst):
        if len(mst) != n - 1:
            return False
        uf = UnionFind(n)
        for u, v, _ in mst:
            if not uf.union(u, v):
                return False                 # ciclo
        # Todos en una componente
        return len({uf.encontrar(i) for i in range(n)}) == 1

    assert verificar_mst(5, mst)

    # Verificación contra fuerza bruta: es realmente el MÍNIMO
    from itertools import combinations

    def mst_fuerza_bruta(n, aristas):
        mejor = None
        for r in range(n - 1, n):
            for sub in combinations(aristas, r):
                uf = UnionFind(n)
                ok = True
                for u, v, _ in sub:
                    if not uf.union(u, v):
                        ok = False
                        break
                if ok and len({uf.encontrar(i) for i in range(n)}) == 1:
                    t = sum(a[2] for a in sub)
                    if mejor is None or t < mejor:
                        mejor = t
        return mejor

    assert total == mst_fuerza_bruta(5, aristas), "no es el mínimo"

    # Casos base
    assert kruskal(1, []) == [], "un vértice: MST vacío"
    assert kruskal(2, [(0, 1, 7)]) == [(0, 1, 7)], "dos vértices"

    # Grafo no conexo: devuelve bosque, no árbol
    no_conexo = [(0, 1, 1), (2, 3, 1)]
    bosque = kruskal(4, no_conexo)
    print(f"\nGrafo no conexo: {len(bosque)} aristas (bosque, no árbol)")
    assert len(bosque) == 2, "no se puede conectar todo"
    assert verificar_mst(4, bosque) is False or len(bosque) < 3

    # Empates: el MST sigue siendo válido aunque no sea único
    empates = [(0, 1, 1), (1, 2, 1), (0, 2, 1)]
    mst_empates = kruskal(3, empates)
    assert len(mst_empates) == 2
    assert sum(a[2] for a in mst_empates) == 2

    # Verificación aleatoria contra fuerza bruta
    import random
    random.seed(151)
    for _ in range(100):
        n = random.randint(2, 6)
        aristas_r = []
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < 0.6:
                    aristas_r.append((u, v, random.randint(1, 30)))
        # Asegurar conectividad
        for i in range(n - 1):
            if not any((a == i and b == i + 1) or (a == i + 1 and b == i)
                       for a, b, _ in aristas_r):
                aristas_r.append((i, i + 1, random.randint(1, 30)))

        mst_r = kruskal(n, aristas_r)
        bruto = mst_fuerza_bruta(n, aristas_r)
        assert sum(a[2] for a in mst_r) == bruto, f"no es mínimo: {aristas_r}"

    # Eficiencia: Union-Find hace que el costo sea el del ordenamiento
    import time
    n = 3000
    grandes = [(random.randrange(n), random.randrange(n), random.randint(1, 1000))
               for _ in range(8000)]
    # Garantizar conectividad mínima
    for i in range(n - 1):
        grandes.append((i, i + 1, random.randint(1, 1000)))

    inicio = time.time()
    mst_g = kruskal(n, grandes)
    t = time.time() - inicio
    print(f"\nGrafo de {n} vértices y {len(grandes)} aristas: {t*1000:.0f} ms")
    print(f"  MST con {len(mst_g)} aristas, peso {sum(a[2] for a in mst_g)}")
    assert len(mst_g) == n - 1, "el MST debe tener n-1 aristas"

    print("\n✓ Todas las pruebas pasaron")
