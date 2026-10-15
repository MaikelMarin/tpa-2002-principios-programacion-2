r"""
Ejercicio 16: Laberinto (backtracking sobre cuadrcula)
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Backtracking y la plantilla HACER/EXPLORAR/DESHACER (seccin 4.2).
    - Matrices / listas de listas (00-fundamentos 8.2).
    - DFS sobre grafos (tema 04): un laberinto ES un grafo.

PROBLEMA
    Encontrar un camino desde la entrada hasta la salida de un
    laberinto representado como cuadrcula.

        0 = camino libre      1 = pared
        S = entrada           E = salida

FONDO MATEMTICO
    Un laberinto es un GRAFO: cada celda libre es un vrtice, y dos
    celdas son adyacentes si comparten un lado (arriba, abajo,
    izquierda, derecha). No se permite movimiento diagonal.

    Eso significa que resolver un laberinto es aplicar DFS (tema 04).
    La diferencia con el DFSAllo es que aqu NO queremos solo llegar:
    queremos el CAMINO, y para eso hace falta backtracking puro.

    EL ESTADO del backtracking son dos cosas:
      1. La posicin actual (fila, col).
      2. El conjunto de celdas ya visitadas.

    La segunda es necesaria para no entrar en ciclo infinito: sin
    marcar visitadas, el camino podra ir y volver entre dos celdas
    para siempre.

    BUG CLSICO EVITADO AQUI: el orden de las comprobaciones.
    Si se verifica "es la salida?" ANTES de "es una pared?", un
    laberinto cuya celda de salida sea pared devuelve un camino
    "vlido" que termina dentro de una pared. Las podas deben ir
    PRIMERO y el caso de xito DESPUS.

ESTRATEGIA

```python
def resolver(laberinto, fila, col, visitadas, camino):
    if (fila, col) == (salida_f, salida_c):
        return True                                # solucin completa
    if fuera_de_rango(fila, col): return False     # poda: limites
    if laberinto[fila][col] == 1: return False     # poda: pared
    if (fila, col) in visitadas: return False      # poda: ya visitada

    visitadas.add((fila, col))                     # HACER
    camino.append((fila, col))

    for df, dc in [(-1,0), (1,0), (0,-1), (0,1)]:  # 4 direcciones
        if resolver(laberinto, fila+df, col+dc, visitadas, camino):
            return True                            # encontrado: no deshacer

    camino.pop()                                   # DESHACER (callejn)
    return False
```

    Note la asimetra con las N reinas:
      - Si una rama lleva a la solucin, se retorna INMEDIATAMENTE y NO
        se deshace el camino.
      - Si una rama es un callejn sin salida, se DESHACE y se prueba
        otra direccin.

    Ese "deshacer solo en el fracaso" es la esencia del backtracking.

TRAZA sobre la cuadrcula 3x3
    0 0 1
    1 0 1
    1 0 0        (entrada en 0,0, salida en 2,2)

    resolver(0,0): libre, no visitada. Marcar. Camino=[(0,0)]
      direccin arriba   -> fuera de rango, podado
      direccin abajo    -> (1,0) es pared (1), podado
      direccin izq      -> fuera de rango, podado
      direccin der      -> (0,1) libre -> resolver(0,1)
        marcar. Camino=[(0,0),(0,1)]
          arriba  -> fuera de rango
          abajo   -> (1,1) libre -> resolver(1,1)
            marcar. Camino=[(0,0),(0,1),(1,1)]
              arriba -> (0,1) ya visitada, podado
              abajo  -> (2,1) libre -> resolver(2,1)
                marcar. Camino=[(0,0),(0,1),(1,1),(2,1)]
                  arriba -> (1,1) ya visitada
                  abajo  -> fuera de rango
                  izq    -> (2,0) es pared
                  der    -> (2,2) = SALIDA. return True
                return True (sin deshacer)
              return True
          ...

    Camino final: (0,0) -> (0,1) -> (1,1) -> (2,1) -> (2,2)

DEMOSTRACIN DE CORRECCIN
    Por induccin sobre la longitud del camino.

    - Si la celda actual es la salida, se devuelve el camino, que es
      vlido por construccin (cada paso aadi una celda adyacente
      libre).
    - Si no, se exploran las 4 direcciones. Cada llamada recursiva
      parte de una celda adyacente vlida, as que cualquier solucin
      encontrada es un camino real.
    - El conjunto `visitadas` garantiza que ninguna celda se repita,
      luego el camino es SIMPLE (sin ciclos) y de longitud finita.

    Si el laberinto no tiene salida, todas las ramas se podan y se
    devuelve False. 

COMPLEJIDAD
    Tiempo: O(4^(n*m)) en el peor caso terico (4 direcciones por
    celda). En la prctica, con `visitadas`, cada celda se procesa
    como mucho una vez por camino, y el nmero de caminos explorados
    es polinomial en laberintos normales.

    Ms precisamente: O(C * n * m) donde C es el nmero de caminos
    simples que se exploran antes de encontrar la solucin.

    Espacio: O(n * m) para `visitadas` y la pila de recursin.

    Compare con BFS (tema 04): BFS encuentra el camino MS CORTO y
    garantiza O(V+E). El backtracking encuentra UN camino, sin
    garantizar que sea el ms corto.

    REGLA: si solo importa la longitud mnima, use BFS. Si importa
    explorar todas las rutas posibles o hay restricciones complejas,
    use backtracking.

APLICACIONES
    Videojuegos: pathfinding con restricciones.
    Robots: navegacin con obstculos.
  - Puzzles: caballero, puentes, sokoban.

RELACIN CON OTROS TEMAS
    - El laberinto ES un grafo (tema 04): las celdas son vrtices y
      los movimientos son aristas. El DFS del ejercicio 5 resuelve lo
      mismo pero sin devolver el camino.
    - El coloreo de grafos (ejercicio 18) aplica la misma plantilla
      sobre grafos explcitos.
"""


LABERINTO_EJEMPLO = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
]

MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # arriba, abajo, izq, der


def resolver_laberinto(laberinto, entrada=(0, 0), salida=None):
    """Encuentra UN camino con backtracking. Devuelve la lista o None."""
    if salida is None:
        salida = (len(laberinto) - 1, len(laberinto[0]) - 1)

    filas, cols = len(laberinto), len(laberinto[0])
    visitadas = set()
    camino = []

    def backtrack(fila, col):
        # --- Podas PRIMERO, xito despus ---
        # El orden importa: si la celda de SALIDA es una pared, no debe
        # aceptarse como llegada. Verificar el xito antes que la pared
        # hara que el algoritmo "llegue" a una pared.
        if not (0 <= fila < filas and 0 <= col < cols):
            return False                          # fuera del tablero
        if laberinto[fila][col] == 1:
            return False                          # pared (incluida la salida)
        if (fila, col) in visitadas:
            return False                          # ya visitada

        # --- Caso base: llegamos a una celda libre ---
        if (fila, col) == salida:
            camino.append((fila, col))
            return True

        # --- HACER ---
        visitadas.add((fila, col))
        camino.append((fila, col))

        # --- EXPLORAR las 4 direcciones ---
        for df, dc in MOVIMIENTOS:
            if backtrack(fila + df, col + dc):
                return True                       # encontrado: NO deshacer

        # --- DESHACER (callejn sin salida) ---
        camino.pop()
        return False

    if backtrack(*entrada):
        return camino
    return None


def todos_los_caminos(laberinto, entrada=(0, 0), salida=None):
    """Encuentra TODOS los caminos simples (sin poda de optimalidad)."""
    if salida is None:
        salida = (len(laberinto) - 1, len(laberinto[0]) - 1)

    filas, cols = len(laberinto), len(laberinto[0])
    caminos = []
    visitadas = set()
    camino_actual = []

    def backtrack(fila, col):
        # Mismo orden que resolver_laberinto: podas antes del xito
        if not (0 <= fila < filas and 0 <= col < cols):
            return
        if laberinto[fila][col] == 1:
            return
        if (fila, col) in visitadas:
            return

        if (fila, col) == salida:
            caminos.append(camino_actual[:] + [(fila, col)])
            return                                 # NO retornar True

        visitadas.add((fila, col))
        camino_actual.append((fila, col))

        for df, dc in MOVIMIENTOS:
            backtrack(fila + df, col + dc)

        # Aqu S siempre se deshace: queremos todas las rutas
        camino_actual.pop()
        visitadas.discard((fila, col))

    backtrack(*entrada)
    return caminos


if __name__ == "__main__":
    # El laberinto del ejemplo
    lab = LABERINTO_EJEMPLO
    print("Laberinto:")
    for fila in lab:
        print("  " + " ".join(str(x) for x in fila))

    camino = resolver_laberinto(lab)
    print(f"\nCamino encontrado: {camino}")
    assert camino is not None, "debera haber salida"
    assert camino[0] == (0, 0), "empieza en la entrada"
    assert camino[-1] == (4, 4), "termina en la salida"

    # El camino es vlido: pasos adyacentes, celdas libres, sin repetir
    for (f1, c1), (f2, c2) in zip(camino, camino[1:]):
        assert abs(f1 - f2) + abs(c1 - c2) == 1, "paso no adyacente"
        assert lab[f2][c2] == 0, "pasa por una pared"
    assert len(camino) == len(set(camino)), "el camino repite celdas"
    print(f"  Longitud: {len(camino) - 1} pasos (vlido, sin ciclos)")

    # Laberinto SIN salida
    sin_salida = [
        [0, 1],
        [1, 0],
    ]
    assert resolver_laberinto(sin_salida) is None
    print("\nLaberinto sin salida: devuelve None")

    # Casos base
    uno = [[0]]
    assert resolver_laberinto(uno) == [(0, 0)], "entrada = salida"
    print("Laberinto 1x1: la entrada es la salida")

    # Todo abierto: cualquier camino sirve
    abierto = [[0, 0], [0, 0]]
    c = resolver_laberinto(abierto)
    assert c == [(0, 0), (0, 1), (1, 1)] or len(c) >= 3
    print(f"Todo abierto: {c}")

    # Todos los caminos
    caminos = todos_los_caminos(abierto)
    print(f"\nCaminos simples en 2x2 abierto: {len(caminos)}")
    for p in caminos:
        print(f"  {p}")
    # En un 2x2 abierto hay exactamente 2 caminos simples
    assert len(caminos) == 2, f"esperaba 2, hay {len(caminos)}"

    # Todos los caminos son vlidos y distintos
    for p in caminos:
        assert p[0] == (0, 0) and p[-1] == (1, 1)
        assert len(p) == len(set(p))
        for (f1, c1), (f2, c2) in zip(p, p[1:]):
            assert abs(f1 - f2) + abs(c1 - c2) == 1

    # Verificacin exhaustiva: el camino encontrado es siempre vlido
    import random
    random.seed(161)
    verificados = 0
    for _ in range(300):
        filas = random.randint(1, 6)
        cols = random.randint(1, 6)
        lab_r = [[0 if random.random() < 0.7 else 1 for _ in range(cols)]
                 for _ in range(filas)]
        c = resolver_laberinto(lab_r)
        if c is None:
            # Verificar que realmente no hay salida
            assert todos_los_caminos(lab_r) == [] or not any(
                p[-1] == (filas - 1, cols - 1) for p in todos_los_caminos(lab_r)), \
                "se dijo que no habia salida pero si la hay"
        else:
            assert c[0] == (0, 0) and c[-1] == (filas - 1, cols - 1)
            assert len(c) == len(set(c))
            for (f1, c1), (f2, c2) in zip(c, c[1:]):
                assert abs(f1 - f2) + abs(c1 - c2) == 1
                assert lab_r[f2][c2] == 0
            verificados += 1
    print(f"\nVerificados {verificados} laberintos aleatorios con salida")

    # Rendimiento: laberinto grande
    import time
    n = 30
    grande = [[0] * n for _ in range(n)]
    # Aadir algunas paredes
    for i in range(n):
        grande[i][n // 2] = 1
    grande[n // 2][n // 2] = 0                    # un hueco
    grande[0][n // 2] = 0                         # otro hueco

    inicio = time.time()
    c_g = resolver_laberinto(grande)
    t = time.time() - inicio
    print(f"\nLaberinto {n}x{n} con paredes: {t*1000:.0f} ms, "
          f"camino de {len(c_g) if c_g else 0} pasos")

    print("\n Todas las pruebas pasaron")
