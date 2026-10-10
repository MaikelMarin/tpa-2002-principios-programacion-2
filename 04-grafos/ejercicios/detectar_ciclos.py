r"""
Ejercicio 6: Detectar ciclos en grafo no dirigido
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - DFS (ejercicios 4 y 5): la detección se basa en él.
    - El concepto de "padre" en un recorrido de árbol.
    - Grafos no dirigidos.

PROBLEMA
    Determinar si un grafo no dirigido contiene un ciclo.

FONDO MATEMÁTICO
    Un grafo CONEXO es un árbol si y solo si tiene exactamente n−1
    aristas. De ahí una primera forma de detectar ciclos:

        Si conexo y |E| == |V| − 1  → sin ciclos (es un árbol)
        Si |E| > |V| − 1            → hay ciclos (o es inconexo)

    Pero eso solo da una respuesta parcial para grafos inconexos. La
    forma general es buscar durante el DFS.

LA REGLA DE DETECCIÓN
    Durante el DFS, si encontramos un vecino YA VISITADO que NO es
    nuestro padre inmediato, entonces hay un ciclo.

    ¿Por qué funciona? Si el vecino visitado no es el padre, el único
    modo de haberlo visitado antes es que exista OTRO CAMINO desde
    nosotros hasta él. Ese otro camino, más la arista actual, forma
    un ciclo.

    El chequeo de "que no sea el padre" es EsSENCIAL: sin él, todo
    grafo parecería tener ciclo, porque cada nodo ve a su padre como
    vecino visitado.

TRAZA sobre el triángulo: A ─ B, B ─ C, A ─ C

    dfs(A, padre=None): visitados={A}
       vecino B no visitado → dfs(B, padre=A)
          visitados={A,B}
          vecino A: ¿visitado? Sí. ¿Es el padre? Sí (padre=A) → ignorar
          vecino C no visitado → dfs(C, padre=B)
             visitados={A,B,C}
             vecino A: ¿visitado? Sí. ¿Es el padre? NO (padre=B)
                       → ¡CICLO DETECTADO!

    El ciclo es A─B─C─A, cerrado por la arista C-A.

    Contraste con un árbol (mismos vértices, sin la arista A-C):
    dfs(A): vecino B → dfs(B): vecino A es padre (ok), vecino C → dfs(C):
             vecino B es padre (ok). Ningún otro vecino visitado.
             → sin ciclo. Correcto.

IMPLEMENTACIÓN

```python
def tiene_ciclo(grafo):
    visitados = set()

    def dfs(v, padre):
        visitados.add(v)
        for vecino, _ in grafo.vecinos(v):
            if vecino not in visitados:
                if dfs(vecino, v):         # ← pasa el padre
                    return True
            elif vecino != padre:          # ← la regla clave
                return True
        return False

    for vertice in grafo.vertices:          # por si hay varias componentes
        if vertice not in visitados:
            if dfs(vertice, None):
                return True
    return False
```

    Note que hay que recorrer TODOS los vértices como posibles
    orígenes, no solo uno: el grafo puede ser inconexo.

DEMOSTRACIÓN DE CORRECCIÓN
    * Si el algoritmo reporta ciclo: encontró un vecino visitado w que
      no es el padre de v. Como w fue visitado antes y no es el padre
      de v, existe un camino de w a v en el bosque DFS que no usa la
      arista (v, w). Esa arista más ese camino forman un ciclo. Existe.
    * Si existe un ciclo C: sea (u, w) la arista de C que se explora
      última. Cuando se explora, u y w ya están visitados (el ciclo
      los conecta). Como (u, w) es la última arista del ciclo
      explorada, cuando se procesa uno de sus extremos el otro ya fue
      visitado por otro camino, así que no es el padre. Se detecta. ∎

COMPLEJIDAD
    Tiempo: O(V + E). Es un DFS con trabajo O(1) extra por arista.
    Espacio: O(V) de pila de recursión.

    MUCHO más eficiente que la fórmula |E| vs |V|−1 cuando hay que
    reportar el ciclo, y funciona en grafos inconexos.

COMPARACIÓN CON GRAFOS DIRIGIDOS
    En un grafo DIRIGIDO esta regla NO funciona directamente. Allí hay
    que usar tres estados (BLANCO/GRIS/NEGRO) y detectar una ARISTA
    DE RETROCESO (llegar a un vértice GRIS, es decir, en la pila
    actual de recursión). Ver el ejercicio grafo_dirigido_ciclos.py.

APLICACIONES
    - Detectar deadlocks (grafos de espera).
    - Verificar que un grafo es un árbol (para algoritmos que lo
      requieren).
    - Validar dependencias (un ciclo = dependencia circular).
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

    @property
    def vertices(self):
        return list(self.adyacencia.keys())


def tiene_ciclo(grafo):
    """Detecta ciclos en grafo NO dirigido. O(V+E).

    La regla: un vecino ya visitado que no es el padre inmediato
    implica un ciclo.
    """
    visitados = set()

    def dfs(v, padre):
        visitados.add(v)

        for vecino, _ in grafo.vecinos(v):
            if vecino not in visitados:
                if dfs(vecino, v):
                    return True
            elif vecino != padre:
                return True                 # ciclo encontrado

        return False

    for vertice in grafo.vertices:           # puede ser inconexo
        if vertice not in visitados:
            if dfs(vertice, None):
                return True

    return False


if __name__ == "__main__":
    # Triángulo: tiene ciclo
    g1 = Grafo()
    for u, v in [(0, 1), (1, 2), (0, 2)]:
        g1.agregar_arista(u, v)
    print(f"Triángulo tiene ciclo: {tiene_ciclo(g1)}")
    assert tiene_ciclo(g1) is True

    # Árbol: sin ciclo
    g2 = Grafo()
    for u, v in [(0, 1), (0, 2)]:
        g2.agregar_arista(u, v)
    print(f"Árbol (0-1, 0-2) tiene ciclo: {tiene_ciclo(g2)}")
    assert tiene_ciclo(g2) is False

    # Cuadrado: tiene ciclo
    g3 = Grafo()
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        g3.agregar_arista(u, v)
    assert tiene_ciclo(g3) is True, "el cuadrado cierra"

    # Cadena (árbol): sin ciclo
    g4 = Grafo()
    for u, v in [(1, 2), (2, 3), (3, 4)]:
        g4.agregar_arista(u, v)
    assert tiene_ciclo(g4) is False, "una cadena no cierra"

    # Casos base
    vacio = Grafo()
    assert tiene_ciclo(vacio) is False

    aislado = Grafo()
    aislado.adyacencia = {5: []}
    assert tiene_ciclo(aislado) is False, "un vértice solo no forma ciclo"

    dos = Grafo()
    dos.agregar_arista(0, 1)
    assert tiene_ciclo(dos) is False, "dos vértices y una arista"

    # CICLO DE DOS VÉRTICES: la trampa de las aristas paralelas
    # Un grafo no dirigido NO debería tener dos aristas entre el mismo
    # par, pero si la implementación lo permite, SÍ es un ciclo.
    multi = Grafo()
    multi.agregar_arista(0, 1)
    multi.agregar_arista(0, 1)               # arista duplicada
    print(f"Aristas paralelas (0-1 dos veces): ciclo = {tiene_ciclo(multi)}")
    assert tiene_ciclo(multi) is True, "dos aristas entre el mismo par = ciclo"

    # Verificación con la fórmula |E| vs |V|−1 en grafos CONEXOS
    def es_conexo(grafo):
        if not grafo.vertices:
            return True
        visitados = set()
        pila = [grafo.vertices[0]]
        while pila:
            v = pila.pop()
            if v in visitados:
                continue
            visitados.add(v)
            for vecino, _ in grafo.vecinos(v):
                if vecino not in visitados:
                    pila.append(vecino)
        return len(visitados) == len(grafo.vertices)

    # Ciclo de 4 vs árbol de 4: mismo V, distinto E
    assert tiene_ciclo(g3) == (len(g3.vertices) - 1 < 4), "4 aristas, 4 vértices"

    # Grafo inconexo con ciclo en una sola componente
    mixto = Grafo()
    mixto.agregar_arista(0, 1)               # componente sin ciclo
    mixto.agregar_arista(2, 3)               # componente CON ciclo
    mixto.agregar_arista(3, 2)               # (arista paralela: ciclo)
    print(f"\nInconexo con ciclo en una parte: {tiene_ciclo(mixto)}")
    assert tiene_ciclo(mixto) is True, "debe revisar todas las componentes"

    # Verificación aleatoria contra la fórmula |E| vs |V|−1.
    #
    # NOTA METODOLÓGICA: para que la fórmula sea válida hay que generar
    # grafos SIN aristas paralelas (dos aristas entre el mismo par sí
    # forman un ciclo de longitud 2, y una fórmula basada en pares
    # únicos no lo reflejaría). Por eso se usa un conjunto de aristas.
    def es_conexo(g):
        if not g.vertices:
            return True
        vis = set()
        pila = [g.vertices[0]]
        while pila:
            v = pila.pop()
            if v in vis:
                continue
            vis.add(v)
            for vec, _ in g.vecinos(v):
                if vec not in vis:
                    pila.append(vec)
        return len(vis) == len(g.vertices)

    import random
    random.seed(181)
    verificados = 0

    for _ in range(400):
        n = random.randint(2, 10)
        # Generar aristas SIN duplicados: pares no ordenados únicos
        posibles = [(u, v) for u in range(n) for v in range(u + 1, n)]
        random.shuffle(posibles)
        elegidas = posibles[:random.randint(0, len(posibles))]

        g = Grafo()
        for i in range(n):
            g.adyacencia[i] = []              # todos los vértices existen
        for u, v in elegidas:
            g.agregar_arista(u, v)

        if not es_conexo(g):
            continue                          # la fórmula no aplica

        # Conexo: sin ciclos ⟺ |E| == |V| − 1
        esperado = len(elegidas) > len(g.vertices) - 1
        assert tiene_ciclo(g) == esperado, \
            f"discrepancia: V={len(g.vertices)}, E={len(elegidas)}"
        verificados += 1

    print(f"Verificados {verificados} grafos conexos contra la formula |E| vs |V|-1")

    print("\n✓ Todas las pruebas pasaron")
