r"""
Ejercicio 18: Coloreo de grafos
Dificultad: Avanzado

CONOCIMIENTO PREVIO NECESARIO
    - Backtracking y la plantilla HACER/EXPLORAR/DESHACER (sección 4.2).
    - Grafos y lista de adyacencia (tema 04, ejercicio 1).
    - Grafos bipartitos y coloreo BFS (tema 04, ejercicio 11).

PROBLEMA
    Asignar colores a los vrtices de un grafo de modo que dos
    vrtices adyacentes NUNCA compartan color, usando como maximo m
    colores.

FONDO MATEMTICO
    EL PROBLEMA DEL NUMERO CROMATICO: cul es el mínimo nmero de
    colores necesarios para colorear un grafo?

    Es uno de los problemas NP-completos clsicos. No se conoce
    algoritmo polinomial que lo resuelva Exactamente para grafos
    arbitrarios.

    Hechos relacionados:
      - Todo rbol es 2-coloreable (bipartito).
      - Un grafo bipartito es exactamente 2-coloreable.
      - Un ciclo par es 2-coloreable; un ciclo impar necesita 3.
      - El nmero cromtico de un grafo completo de n vrtices es n.

    Backtracking resuelve el problema de DECISIN ("se puede con m
    colores?") explorando asignaciones. Con poda fuerte es viable
    para grafos pequeos.

    CONTRASTE CON EL GRAFO BIPARTITO (tema 04):
        El test de bipartito usa BFS y colorea por niveles: O(V+E).
        Pero solo funciona para 2 colores. Con 3 o ms, no hay un
        atajo as, y hace falta backtracking.

    Esa es la razn por la que "es bipartito?" es fcil y "es
    3-coloreable?" es NP-completo.

ESTRATEGIA

```python
def colorear(grafo, m):
    colores = {}                                   # vertice -> color

    def backtrack(vertice):
        if vertice == todos_los_vertices():
            return True                            # todos coloreados

        for color in range(1, m + 1):
            if es_seguro(vertice, color):           # PODA
                colores[vertice] = color            # HACER
                if backtrack(siguiente(vertice)):   # EXPLORAR
                    return True
                del colores[vertice]                # DESHACER

        return False                              # ningn color sirve

    backtrack(primer_vertice())
    return colores
```

    La poda `es_seguro` comprueba que ningn vecino YA coloreado tenga
    ese color. Es ms dbil que la del Sudoku (solo mira vecinos
    directos), pero igualmente efectiva.

TRAZA sobre un tringulo A-B-C, m=3
    backtrack(A):.color 1 seguro (sin vecinos coloreados) -> A=1
      backtrack(B):
        color 1: vecino A tiene 1 -> PODADO
        color 2: seguro -> B=2
          backtrack(C):
            color 1: vecino A tiene 1 -> PODADO
            color 2: vecino B tiene 2 -> PODADO
            color 3: seguro -> C=3
              backtrack(fin): todos coloreados -> TRUE
    Resultado: {A:1, B:2, C:3}

    Con m=2 el mismo tringulo:
    backtrack(A): A=1
      backtrack(B):
        color 1: podado (A lo tiene)
        color 2: B=2
          backtrack(C):
            color 1: podado (A)
            color 2: podado (B)
            ninguno sirve -> return False
        B=2 no funciona -> deshacer
      ningn color para B -> return False
    Ningn color para A -> return False
    Resultado: no se puede (correcto: ciclo impar necesita 3)

    Es exactamente el teorema de ciclos impares del tema 04, ahora
    demostrado por backtracking en vez de por BFS.

DEMOSTRACIN DE CORRECCIN
    Por induccin sobre el nmero de vrtices.

    - Caso base: todos los vrtices coloreados. Cada asignacin respet
      la poda (ningn vecino comparta color), luego es un coloreo
      válido.
    - Paso: para el vrtice actual, se prueban los m colores. Los
      inseguros se descartan correctamente (habra conflicto). Los
      seguros se exploran recursivamente.

    Si existe un coloreo con m colores, el backtracking lo encuentra
    (en el peor caso explora todas las asignaciones parciales que
    pasan la poda). Si no existe, todas las ramas fallan. 

COMPLEJIDAD
    Tiempo: O(m^V) en el peor caso (m opciones por vrtice, V vrtices).
    Con poda, mucho menos en la práctica.

    Espacio: O(V) de pista + O(V) para el mapa de colores.

    Para V=20, m=3: 3^20 = 3.500 millones de combinaciones. Con poda
    fuerte, en la práctica se resuelve rapIdsimo.

APLICACIONES
    - Asignacin de frecuencias en redes de radio.
    - Planificacin de exmenes (sin conflictos de horario).
    - Asignacin de registros en compiladores.
    - Resolucin de Sudoku (ejercicio 17): es un coloreo con 9 colores
      y restricciones ms complejas.

RELACIN CON OTROS TEMAS
    - Es la generalizacin del test de bipartito (tema 04, ejercicio 11),
      que solo cubre m=2.
    - El Sudoku (ejercicio 17) es el mismo patrn con ms restricciones.
"""


class Grafo:
    """Grafo no dirigido con lista de adyacencia."""

    def __init__(self):
        self.adyacencia = {}

    def agregar_vertice(self, v):
        if v not in self.adyacencia:
            self.adyacencia[v] = []

    def agregar_arista(self, u, v):
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        self.adyacencia[u].append(v)
        self.adyacencia[v].append(u)

    def vecinos(self, v):
        return self.adyacencia.get(v, [])

    @property
    def vertices(self):
        return list(self.adyacencia.keys())


def es_seguro(grafo, vertice, color, colores):
    """Poda: algn vecino ya coloreado tiene ese color?"""
    for vecino in grafo.vecinos(vertice):
        if colores.get(vecino) == color:
            return False                          # conflicto
    return True


def colorear_grafo(grafo, m):
    """Colorea el grafo con como maximo m colores.

    Devuelve el mapa {vertice: color} o None si no es posible.
    """
    vertices = grafo.vertices
    colores = {}
    intentos = [0]

    def backtrack(indice):
        if indice == len(vertices):
            return True                           # todos coloreados

        vertice = vertices[indice]

        for color in range(1, m + 1):
            intentos[0] += 1
            if es_seguro(grafo, vertice, color, colores):
                colores[vertice] = color           # HACER
                if backtrack(indice + 1):          # EXPLORAR
                    return True
                del colores[vertice]               # DESHACER

        return False                              # ningn color sirve

    if backtrack(0):
        return colores, intentos[0]
    return None, intentos[0]


def numero_cromatico_minimo(grafo, max_colores=None):
    """Encuentra el mínimo nmero de colores probando m = 1, 2, 3, ...

    Casos especiales:
      - Grafo vaco (sin vrtices): 0 colores.
      - Con al menos un vrtice: como mínimo 1 color.
    """
    vertices = grafo.vertices
    if not vertices:
        return 0, {}                             # grafo vacio

    n = len(vertices)
    if max_colores is None:
        max_colores = n

    for m in range(1, max_colores + 1):
        resultado, _ = colorear_grafo(grafo, m)
        if resultado is not None:
            return m, resultado
    return None, None


if __name__ == "__main__":
    # --- Tricolo: ciclo par -> 2 colores ---
    cuadrado = Grafo()
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        cuadrado.agregar_arista(u, v)

    colores, intentos = colorear_grafo(cuadrado, 2)
    print(f"Cuadrado (ciclo par) con 2 colores: {colores}")
    assert colores is not None, "un ciclo par es 2-coloreable"

    # Verificar que es un coloreo válido
    for u in cuadrado.vertices:
        for v in cuadrado.vecinos(u):
            assert colores[u] != colores[v], f"{u} y {v} comparten color"
    assert set(colores.values()) <= {1, 2}
    print("  Coloreo valido verificado")

    # --- Tricolo: ciclo impar -> 3 colores, no 2 ---
    triangulo = Grafo()
    for u, v in [(0, 1), (1, 2), (2, 0)]:
        triangulo.agregar_arista(u, v)

    con2, _ = colorear_grafo(triangulo, 2)
    assert con2 is None, "un ciclo impar NO es 2-coloreable"
    print("\nTriangulo con 2 colores: imposible")

    con3, _ = colorear_grafo(triangulo, 3)
    assert con3 is not None, "con 3 colores s es posible"
    print(f"Triangulo con 3 colores: {con3}")
    for u in triangulo.vertices:
        for v in triangulo.vecinos(u):
            assert con3[u] != con3[v]

    # --- Numero cromatico ---
    m_cuadrado, _ = numero_cromatico_minimo(cuadrado)
    m_triangulo, _ = numero_cromatico_minimo(triangulo)
    print(f"\nNumeros cromaticos: cuadrado={m_cuadrado}, tringulo={m_triangulo}")
    assert m_cuadrado == 2
    assert m_triangulo == 3

    # --- Grafo completo de n vrtices: número cromatico = n ---
    for n in [3, 4, 5]:
        completo = Grafo()
        for u in range(n):
            for v in range(u + 1, n):
                completo.agregar_arista(u, v)
        m, _ = numero_cromatico_minimo(completo)
        assert m == n, f"K{n} deberia necesitar {n} colores, necesita {m}"
        print(f"Grafo completo K{n}: numero cromatico {m}")

    # --- rbol: siempre 2 colores ---
    arbol = Grafo()
    for u, v in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]:
        arbol.agregar_arista(u, v)
    m_arbol, _ = numero_cromatico_minimo(arbol)
    assert m_arbol == 2, "todo rbol es bipartito"
    print(f"Arbol: numero cromatico {m_arbol}")

    # --- Casos base ---
    vacio = Grafo()
    assert numero_cromatico_minimo(vacio) == (0, {}) or numero_cromatico_minimo(vacio)[0] == 0
    print("Grafo vacio: 0 colores")

    aislado = Grafo()
    aislado.agregar_vertice("solo")
    m_aislado, col_aislado = numero_cromatico_minimo(aislado)
    assert m_aislado == 1
    assert col_aislado == {"solo": 1}
    print("Un vertice aislado: 1 color")

    una_arista = Grafo()
    una_arista.agregar_arista("A", "B")
    m_arista, _ = numero_cromatico_minimo(una_arista)
    assert m_arista == 2
    print("Una arista: 2 colores")

    # --- Verificacion exhaustiva aleatoria ---
    import random
    random.seed(181)
    verificados = 0
    for _ in range(200):
        n = random.randint(1, 8)
        g = Grafo()
        for i in range(n):
            g.agregar_vertice(i)
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < 0.4:
                    g.agregar_arista(u, v)

        m, colores = numero_cromatico_minimo(g)
        assert colores is not None

        # El coloreo devuelto debe ser valido
        for u in g.vertices:
            for v in g.vecinos(u):
                assert colores[u] != colores[v], \
                    f"coloreo invalido en el grafo {g.adyacencia}"

        # Y debe usar exactamente m colores (no mas)
        assert len(set(colores.values())) == m, \
            f"uso {len(set(colores.values()))} colores, no {m}"

        # Y m-1 colores NO deben bastar (propiedad de minimidad)
        if m > 1:
            con_menos, _ = colorear_grafo(g, m - 1)
            assert con_menos is None, \
                f"con {m-1} colores s se pudo: m no era minimo"
        verificados += 1

    print(f"\nVerificados {verificados} grafos aleatorios")
    print("  (coloreo valido + usa exactamente m colores + m-1 no bastaba)")

    # --- Efecto de la poda: medir intentos ---
    mediano = Grafo()
    n = 15
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < 0.25:
                mediano.agregar_arista(u, v)

    _, intentos_con_poda = colorear_grafo(mediano, 3)
    print(f"\nEfecto de la poda (grafo de 15 vertices, 3 colores):")
    print(f"  Intentos con poda:    {intentos_con_poda:,}")
    print(f"  Sin poda serian:      {3**15:,} (3^15)")
    assert intentos_con_poda < 3 ** 15

    print("\n Todas las pruebas pasaron")
