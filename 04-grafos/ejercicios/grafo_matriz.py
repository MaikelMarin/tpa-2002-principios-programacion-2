r"""
Ejercicio 2: Grafo con matriz de adyacencia
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Arreglos bidimensionales (00-fundamentos §8.2).
    - Comparación con lista de adyacencia (ejercicio 1).

PROBLEMA
    Representar un grafo con una MATRIZ de adyacencia, donde
    M[i][j] indica si existe arista de i a j (o su peso).

FONDO MATEMÁTICO
    La matriz es una tabla de V×V. Para un grafo no dirigido, la
    matriz es SIMÉTRICA: M[i][j] == M[j][i] siempre. Esa simetría es
    una propiedad observable que puede servir como verificación.

    El espacio es O(V²) SIN IMPORTAR cuántas aristas haya. Ese es el
    precio, y la razón por la que la lista de adyacencia suele ganar.

CUÁNDO SÍ CONVIENE LA MATRIZ
    1. El grafo es DENSO: E se acerca a V². Entonces toda la matriz
       tiene datos útiles y no se desperdicia.
    2. Se consulta MUY a menudo "¿existe la arista (u, v)?": O(1)
       frente a O(grado) de la lista.
    3. Los algoritmos necesitan acceso aleatorio rápido a cualquier
       par (Floyd-Warshall, análisis de alcanzabilidad).
    4. El grafo es pequeño y la simplicidad importa más que la memoria.

TRAZA de construcción
    Grafo: 0─1, 0─2, 1─2, 1─3

    Matriz 4x4, inicializada en 0:
       0 1 2 3
    0 [0 0 0 0]
    1 [0 0 0 0]
    2 [0 0 0 0]
    3 [0 0 0 0]

    agregar_arista(0, 1): M[0][1] = 1, M[1][0] = 1 (no dirigido)
    agregar_arista(0, 2): M[0][2] = 1, M[2][0] = 1
    agregar_arista(1, 2): M[1][2] = 1, M[2][1] = 1
    agregar_arista(1, 3): M[1][3] = 1, M[3][1] = 1

    Resultado:
       0 1 2 3
    0 [0 1 1 0]
    1 [1 0 1 1]
    2 [1 1 0 0]
    3 [0 1 0 0]

    Ver simetría: M[0][1]=M[1][0]=1, M[0][3]=M[3][0]=0. ✓

COMPLEJIDAD DE OPERACIONES
    Operación                    Matriz      Lista
    Espacio                      O(V²)       O(V+E)
    ¿Existe arista (u,v)?        O(1)        O(grado)
    Vecinos de u                 O(V)        O(grado)
    Añadir arista                O(1)        O(1)
    Añadir vértice               O(V²)       O(1)      ← gana la lista
    Eliminar vértice             O(V²)       O(V+E)

    Note la asimetría: la matriz gana en consulta puntual pero pierde
    en operaciones estructurales.

EL CÁLCULO QUE DECIDE
    V = 10,000, E = 20,000 (disperso):
       Matriz: 100,000,000 entradas
       Lista:  ~30,000 entradas
       → La matriz desperdicia 99.97% del espacio.

    V = 1,000, E = 400,000 (denso):
       Matriz: 1,000,000 entradas (todas útiles)
       Lista:  ~800,000 entradas
       → Ambas son razonables; la matriz gana por la consulta O(1).

DETALLE: GRAFOS PONDERADOS
    En vez de 1, se guarda el peso. El 0 significa "no hay arista",
    lo que impide tener aristas de peso 0. Solución: usar None o
    infinito como "no hay arista", o un valor centinela.

RELACIÓN CON OTROS TEMAS
    - El tema 06 (grandes datos) muestra que para grafos enormes ni
      siquiera la lista de adyacencia cabe, y hay que usar
      representaciones externas.
"""


class GrafoMatriz:
    """Grafo con matriz de adyacencia. Espacio O(V²)."""

    def __init__(self, n, dirigido=False):
        self.n = n
        self.dirigido = dirigido
        # Matriz n×n inicializada en 0 (sin aristas)
        self.matriz = [[0] * n for _ in range(n)]

    def agregar_arista(self, u, v, peso=1):
        """Añade una arista. En no dirigido, escribe en ambos lados."""
        self.matriz[u][v] = peso
        if not self.dirigido:
            self.matriz[v][u] = peso          # simetría

    def eliminar_arista(self, u, v):
        self.matriz[u][v] = 0
        if not self.dirigido:
            self.matriz[v][u] = 0

    def hay_arista(self, u, v):
        """¿Existe la arista? O(1). Es la fortaleza de la matriz."""
        return self.matriz[u][v] != 0

    def vecinos(self, v):
        """Devuelve los vecinos. O(V): recorre toda la fila."""
        return [i for i in range(self.n) if self.matriz[v][i] != 0]

    def grado(self, v):
        """Grado del vértice: contar entradas no nulas. O(V)."""
        return sum(1 for i in range(self.n) if self.matriz[v][i] != 0)

    def es_simetrica(self):
        """Verifica que la matriz sea simétrica (no dirigido)."""
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.matriz[i][j] != self.matriz[j][i]:
                    return False
        return True

    def num_aristas(self):
        total = sum(sum(1 for x in fila if x != 0) for fila in self.matriz)
        return total if self.dirigido else total // 2

    def __repr__(self):
        return f"GrafoMatriz({self.n}x{self.n})"


if __name__ == "__main__":
    g = GrafoMatriz(4)
    for u, v in [(0, 1), (0, 2), (1, 2), (1, 3)]:
        g.agregar_arista(u, v)

    print("Matriz de adyacencia:")
    print("     " + " ".join(str(i) for i in range(4)))
    for i, fila in enumerate(g.matriz):
        print(f"  {i}  " + " ".join(str(x) for x in fila))

    # Verificación: la matriz es simétrica (no dirigido)
    assert g.es_simetrica(), "la matriz debe ser simétrica"

    # Consulta O(1)
    assert g.hay_arista(0, 1) is True
    assert g.hay_arista(0, 3) is False
    assert g.hay_arista(1, 0) is True, "simétrica: también al revés"

    # Vecinos: recorrido de fila
    assert g.vecinos(0) == [1, 2]
    assert g.vecinos(1) == [0, 2, 3]
    assert g.vecinos(3) == [1]

    # Grados
    print(f"\nGrados: {[g.grado(i) for i in range(4)]}")
    assert [g.grado(i) for i in range(4)] == [2, 3, 2, 1]

    # Saludo de manos: Σ grados = 2|E|
    suma = sum(g.grado(i) for i in range(4))
    print(f"Σ grados = {suma} = 2·{g.num_aristas()}")
    assert suma == 2 * g.num_aristas()
    assert g.num_aristas() == 4

    # Eliminar arista
    g.eliminar_arista(1, 2)
    assert g.hay_arista(1, 2) is False
    assert g.hay_arista(2, 1) is False, "se eliminó en ambos lados"
    assert g.num_aristas() == 3

    # Casos base
    vacio = GrafoMatriz(3)
    assert vacio.num_aristas() == 0
    assert vacio.vecinos(0) == []
    assert vacio.es_simetrica() is True, "matriz de ceros es simétrica"

    uno = GrafoMatriz(1)
    uno.agregar_arista(0, 0)                    # self-loop
    assert uno.hay_arista(0, 0) is True
    assert uno.grado(0) == 1

    # Grafo DIRIGIDO: la matriz NO es simétrica
    d = GrafoMatriz(3, dirigido=True)
    d.agregar_arista(0, 1)
    d.agregar_arista(1, 2)
    assert d.hay_arista(0, 1) is True
    assert d.hay_arista(1, 0) is False, "dirigido: solo un sentido"
    assert d.es_simetrica() is False
    assert d.num_aristas() == 2, "en dirigido no se divide por 2"
    assert d.vecinos(0) == [1]
    assert d.vecinos(1) == [2]
    assert d.vecinos(2) == []

    # Grafo PONDERADO
    p = GrafoMatriz(3, dirigido=True)
    p.agregar_arista(0, 1, 5)
    p.agregar_arista(0, 2, 3)
    assert p.matriz[0][1] == 5, "el peso se guarda en la celda"
    assert p.matriz[1][0] == 0, "no hay arista de vuelta"

    # El espacio es O(V²) sin importar las aristas
    n = 200
    grande = GrafoMatriz(n)
    grande.agregar_arista(0, 1)                 # UNA sola arista
    # La matriz completa sigue reservada
    total_celdas = n * n
    print(f"\nGrafo de {n} vértices y 1 arista:")
    print(f"  Celdas reservadas: {total_celdas:,} (espacio O(V²))")
    assert total_celdas == 40000

    # Comparación de coste de consulta vs lista
    # Matriz: O(1). Lista: O(grado).
    import time
    m_grande = GrafoMatriz(1000)
    for i in range(1000 - 1):
        m_grande.agregar_arista(i, i + 1)        # cadena
    inicio = time.time()
    for _ in range(100000):
        m_grande.hay_arista(500, 501)
    t_consulta = time.time() - inicio
    print(f"  100,000 consultas hay_arista: {t_consulta*1000:.1f} ms (O(1) cada una)")

    print("\n✓ Todas las pruebas pasaron")
