r"""
Ejercicio 11: Grafo bipartito
Dificultad: Avanzado

CONOCIMIENTO PREVIO NECESARIO
    - BFS (ejercicio 3): el algoritmo que resuelve esto.
    - Coloreo de grafos.
    - La equivalencia: bipartito ⟺ no tiene ciclos de longitud impar.

PROBLEMA
    Determinar si los vértices de un grafo se pueden dividir en dos
    grupos de modo que toda arista conecte vértices de grupos
    distintos.

    Es decir: ¿se puede colorear el grafo con 2 colores sin que dos
    vértices adyacentes compartan color?

FONDO MATEMÁTICO
    TEOREMA: un grafo es bipartito si y solo si no contiene ciclos de
    longitud impar.

    Intuición: al recorrer un ciclo, los vértices deben alternar de
    color. Si el ciclo tiene longitud par, al cerrar los colores
    coinciden. Si es impar, el último vértice tendría el mismo color
    que el primero, que es su vecino: contradicción.

    El algoritmo: colorear por BFS asignando colores alternos. Si
    alguna arista conecta dos vértices del mismo color, no es
    bipartito.

ESTRATEGIA
    1. Asignar color 0 al origen, meterlo en la cola.
    2. Al procesar un vértice, cada vecino no coloreado recibe el
       color opuesto.
    3. Si un vecino YA está coloreado y tiene el MISMO color, hay un
       ciclo impar → no es bipartito.
    4. Repetir desde cada vértice no coloreado (grafo puede ser
       inconexo).

TRAZA sobre el cuadrado: 0 ─ 1 ─ 2 ─ 3 ─ 0
    color = {0: 0}, cola = [0]

    pop 0 (color 0). Vecinos 1 y 3, sin colorear.
        color[1] = 1, color[3] = 1
    pop 1 (color 1). Vecinos 0 (color 0, distinto: OK), 2.
        color[2] = 0
    pop 3 (color 1). Vecinos 0 (color 0: OK), 2 (color 0: OK).
    pop 2 (color 0). Vecinos 1 (color 1: OK), 3 (color 1: OK).

    Resultado: colores {0:0, 1:1, 2:0, 3:1}. Bipartito ✓
    Grupos: {0, 2} y {1, 3}.

    Contraste con el triángulo: 0 ─ 1 ─ 2 ─ 0
    pop 0 (0). Vecinos 1, 2 → color 1.
    pop 1 (1). Vecino 0 (0: OK), vecino 2 → color[2]=1.
    pop 2 (color 1). Vecino 0 (color 0: OK).
        Pero también vecino 1: color[1] = 1 = MISMO color → NO bipartito.

    El triángulo es un ciclo de longitud 3 (impar). Correcto.

DEMOSTRACIÓN DE CORRECCIÓN
    * Si el algoritmo dice bipartito: los colores asignados verifican
      que toda arista conecta colores distintos (se comprobó cada
      arista). Luego los dos conjuntos de color forman una bipartición.
    * Si no es bipartito: existe un ciclo de longitud impar (teorema).
      Sea v el primer vértice del ciclo que se repite. Los vértices
      entre las dos apariciones de v forman un ciclo cerrado, y BFS
      asignó colores alternos a lo largo de él, así que los dos
      extremos de la arista que lo cierra tienen el mismo color. Se
      detecta. ∎

COMPLEJIDAD
    Tiempo: O(V + E). Es BFS con trabajo O(1) extra por arista.
    Espacio: O(V) para los colores y la cola.

CASOS LÍMITE
    - Grafo vacío: bipartito (trivialmente, dos conjuntos vacíos).
    - Un solo vértice: bipartito.
    - Un árbol: SIEMPRE bipartito (no tiene ciclos).
    - Grafo inconexo: hay que repetir desde cada componente.

APLICACIONES
    - Asignación de tareas a dos máquinas.
    - Emparejamiento máximo (mercado de empleo, asignación estudiantes-cursos).
    - Detección de ciclos impares como prueba de corrección en grafos.

RELACIÓN CON OTROS TEMAS
    - La demostración del teorema usa inducción sobre la longitud del
      ciclo (tema 00, §3).
    - Es la versión con 2 colores del problema general de coloreo de
      grafos, que es NP-completo para 3 o más colores.
"""


from collections import deque


class Grafo:
    """Grafo no dirigido con lista de adyacencia."""

    def __init__(self):
        self.adyacencia = {}

    def agregar_arista(self, u, v):
        self.adyacencia.setdefault(u, [])
        self.adyacencia.setdefault(v, [])
        self.adyacencia[u].append((v, 1))
        self.adyacencia[v].append((u, 1))

    def vecinos(self, v):
        return self.adyacencia.get(v, [])

    @property
    def vertices(self):
        return list(self.adyacencia.keys())


def es_bipartito(grafo):
    """Verifica si el grafo es bipartito por coloreo BFS. O(V+E)."""
    color = {}

    for inicio in grafo.vertices:
        if inicio in color:
            continue                          # componente ya procesada

        color[inicio] = 0
        cola = deque([inicio])

        while cola:
            vertice = cola.popleft()

            for vecino, _ in grafo.vecinos(vertice):
                if vecino not in color:
                    color[vecino] = 1 - color[vertice]   # color opuesto
                    cola.append(vecino)
                elif color[vecino] == color[vertice]:
                    return False               # mismo color → ciclo impar

    return True


def biparticion(grafo):
    """Devuelve los dos grupos si es bipartito, o None."""
    color = {}

    for inicio in grafo.vertices:
        if inicio in color:
            continue
        color[inicio] = 0
        cola = deque([inicio])
        while cola:
            vertice = cola.popleft()
            for vecino, _ in grafo.vecinos(vertice):
                if vecino not in color:
                    color[vecino] = 1 - color[vertice]
                    cola.append(vecino)
                elif color[vecino] == color[vertice]:
                    return None

    grupo_a = {v for v, c in color.items() if c == 0}
    grupo_b = {v for v, c in color.items() if c == 1}
    return grupo_a, grupo_b


if __name__ == "__main__":
    # Cuadrado (ciclo par): bipartito
    g1 = Grafo()
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        g1.agregar_arista(u, v)
    print(f"Cuadrado bipartito: {es_bipartito(g1)}")
    assert es_bipartito(g1) is True

    grupos = biparticion(g1)
    print(f"  Grupos: {grupos[0]} y {grupos[1]}")
    assert grupos == ({0, 2}, {1, 3}), "colores alternos"

    # Triángulo (ciclo impar): NO bipartito
    g2 = Grafo()
    for u, v in [(0, 1), (1, 2), (2, 0)]:
        g2.agregar_arista(u, v)
    print(f"Triángulo bipartito: {es_bipartito(g2)}")
    assert es_bipartito(g2) is False
    assert biparticion(g2) is None

    # Casos base
    vacio = Grafo()
    assert es_bipartito(vacio) is True, "vacío es bipartito"

    aislado = Grafo()
    aislado.adyacencia = {5: []}
    assert es_bipartito(aislado) is True
    assert biparticion(aislado) == ({5}, set())

    # Un árbol: SIEMPRE bipartito
    arbol = Grafo()
    for u, v in [(0, 1), (0, 2), (1, 3), (1, 4)]:
        arbol.agregar_arista(u, v)
    assert es_bipartito(arbol) is True, "los árboles no tienen ciclos"

    # Ciclos pares vs impares
    for k in [4, 6, 8]:
        ciclo_par = Grafo()
        for i in range(k):
            ciclo_par.agregar_arista(i, (i + 1) % k)
        assert es_bipartito(ciclo_par) is True, f"ciclo de {k} (par)"

    for k in [3, 5, 7]:
        ciclo_impar = Grafo()
        for i in range(k):
            ciclo_impar.agregar_arista(i, (i + 1) % k)
        assert es_bipartito(ciclo_impar) is False, f"ciclo de {k} (impar)"

    # Grafo inconexo: una componente bipartita y otra no
    mixto = Grafo()
    for u, v in [(0, 1), (1, 2), (2, 0)]:          # triángulo
        mixto.agregar_arista(u, v)
    for u, v in [(3, 4)]:                           # arista suelta
        mixto.agregar_arista(u, v)
    assert es_bipartito(mixto) is False, "una sola mala componente basta"

    # Estrella: bipartito (centro vs hojas)
    estrella = Grafo()
    for h in range(1, 8):
        estrella.agregar_arista(0, h)
    assert es_bipartito(estrella) is True
    grupos_e = biparticion(estrella)
    assert grupos_e == ({0}, {1, 2, 3, 4, 5, 6, 7})

    # Verificación: la bipartición es válida (ninguna arista dentro de un grupo)
    for grafo in [g1, arbol, estrella]:
        part = biparticion(grafo)
        if part is None:
            continue
        a, b = part
        for u in grafo.vertices:
            for vecino, _ in grafo.vecinos(u):
                assert (u in a) != (vecino in a) or (u in a) != (vecino in b), \
                    "una arista conecta vértices del mismo grupo"

    print("\n✓ Todas las pruebas pasaron")
