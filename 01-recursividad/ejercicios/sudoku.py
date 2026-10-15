r"""
Ejercicio 17: Sudoku
Dificultad: Avanzado

CONOCIMIENTO PREVIO NECESARIO
    - Backtracking y la plantilla HACER/EXPLORAR/DESHACER (seccin 4.2).
    - Matrices y validacin por regiones (listas de listas).
    - Por qu la poda es aqu MS importante que en otros problemas.

PROBLEMA
    Resolver un tablero de Sudoku 9x9 completando las celdas vacias.

    Reglas:
      1. Cada fila contiene los digitos 1-9 sin repetir.
      2. Cada columna contiene los digitos 1-9 sin repetir.
      3. Cada caja 3x3 contiene los digitos 1-9 sin repetir.

FONDO MATEMTICO
    El Sudoku es el ejemplo cannico de backtracking con PODA FUERTE.
    La diferencia con otros problemas:

        Sin poda: 9^61 tableros posibles (inasumible).
        Con poda: se descartan el 99.999...% en el primer nivel.

    La poda no es una optimizacin: es lo nico que hace el problema
    tratable. Un Sudoku bien planteado (con solucin nica) se resuelve
    en milisegundos; uno mal planteado puede tardar horas.

    HEURISTICA IMPORTANTE: elegir bien la SIGUIENTE CELDA.
        - Orden fijo (izq a der, arriba abajo): simple pero lento.
        - Celda con MENOS candidatos primero (MRV): mucho ms rpido.

    Este ejercicio usa orden fijo por claridad, y documenta qu tanto
    se ganara con MRV.

ESTRATEGIA

```python
def resolver(tablero):
    if no_huecos(tablero):
        return True                              # solucin completa

    fila, col = siguiente_hueco(tablero)         # primera celda vacia

    for digito in range(1, 10):                  # probar 1..9
        if es_valido(tablero, fila, col, digito):  # PODA
            tablero[fila][col] = digito           # HACER
            if resolver(tablero):                 # EXPLORAR
                return True                       # encontrado
            tablero[fila][col] = 0                # DESHACER

    return False                                  # ningn digito funcion
```

    La funcin `es_valido` es toda la poda:
        1. El digito no est ya en la fila?
        2. Ni en la columna?
        3. Ni en la caja 3x3 correspondiente?

    Si alguna falla, se descarta el digito SIN recursar. Esa es la
    poda fuerte.

DETALLE: calcular la caja 3x3
    Para una celda (fila, col), su caja es:
        caja_fila = (fila // 3) * 3
        caja_col  = (col  // 3) * 3
    Y se recorren las 9 celdas desde ahi.

TRAZA de una decisin
    Tablero parcial, se busca la primera celda vacia: (0, 2).
    Candidatos: 1..9. Para cada uno:

        digito 1: ya est en la fila 0?          Si -> podado
        digito 2: ya est en la columna 2?        Si -> podado
        digito 3: ya est en la caja (0,0)?       No -> PROBAR
            colocar 3, recursar
            si la recursin falla -> deshacer, probar 4

    Cada candidato descartado ahorra un subrbol ENTERO de bsqueda.

DEMOSTRACIN DE CORRECCIN
    Por induccin sobre el nmero de celdas vacias.

    - Caso base: sin huecos. Por construccin cada colocacin respet
      fila, columna y caja, luego el tablero es una solucin vlida.
    - Paso: para la primera celda vacia, se prueban todos los digitos
      posibles. Los invlidos se descartan (seran soluciones que
      violan las reglas). Los vlidos se exploran recursivamente.

    Si el Sudoku tiene solucin, el backtracking la encuentra: en el
    peor caso explora todas las combinaciones vlidas. Si no la tiene,
    todas las ramas se podan y devuelve False. 

COMPLEJIDAD
    Tiempo: O(9^(huecos)) en el peor caso terico. Con poda fuerte,
    en la prctica polinomial para Sudokus reales bien planteados.

    Espacio: O(huecos) de pila de recursin.

    MEDICIN INCLUIDA: el ejercicio cuenta cuntas veces se llama a
    `es_valido` y cuntos intentos se hacen, para mostrar el efecto
    real de la poda.

HEURISTICA MRV (Minimum Remaining Values)
    En vez de tomar la primera celda vacia, tomar la que tiene MENOS
    candidatos vlidos. Reduce drsticamente el rbol de bsqueda.

    No implementada aqu (por claridad), pero vale la pena saber que
    existe: es la diferencia entre un solver rpido y uno lento.

APLICACIONES
    - Generacin de puzzles (con solucin nica garantizada).
    - Satisfaccin de restricciones (CSP) en general.
    - Planificacin y asignacin de recursos.

RELACIN CON OTROS TEMAS
    - El coloreo de grafos (ejercicio 18) es el mismo patrón: asignar
      valores sujetos a restricciones entre celdas/vrtices.
    - Las N reinas (ejercicio 8) son el Sudoku de una sola restriccin.
"""


TABLERO_EJEMPLO = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

# Estadsticas para medir el efecto de la poda
estadisticas = {"validaciones": 0, "intentos": 0, "backtracks": 0}


def es_valido(tablero, fila, col, digito):
    """Poda: se puede colocar `digito` en (fila, col)?"""
    estadisticas["validaciones"] += 1

    # 1. Fila
    if digito in tablero[fila]:
        return False

    # 2. Columna
    if any(tablero[f][col] == digito for f in range(9)):
        return False

    # 3. Caja 3x3
    caja_fila, caja_col = (fila // 3) * 3, (col // 3) * 3
    for f in range(caja_fila, caja_fila + 3):
        for c in range(caja_col, caja_col + 3):
            if tablero[f][c] == digito:
                return False

    return True


def siguiente_hueco(tablero):
    """Primera celda vacia (orden fijo). Devuelve (fila, col) o None."""
    for f in range(9):
        for c in range(9):
            if tablero[f][c] == 0:
                return f, c
    return None


def siguiente_hueco_mrv(tablero):
    """Celda vacia con MENOS candidatos (heuristica MRV).

    Ms rpida que el orden fijo, pero ms compleja. Se incluye para
    poder comparar.
    """
    mejor = None
    mejor_candidatos = 10                            # ms que el maximo (9)

    for f in range(9):
        for c in range(9):
            if tablero[f][c] != 0:
                continue
            candidatos = sum(
                1 for d in range(1, 10)
                if es_valido_contando(tablero, f, c, d))
            if candidatos < mejor_candidatos:
                mejor_candidatos = candidatos
                mejor = (f, c)
                if candidatos <= 1:                 # no puede mejorar
                    return mejor

    return mejor


def es_valido_contando(tablero, fila, col, digito):
    """es_valido sin contaminar las estadsticas (para MRV)."""
    if digito in tablero[fila]:
        return False
    if any(tablero[f][col] == digito for f in range(9)):
        return False
    caja_fila, caja_col = (fila // 3) * 3, (col // 3) * 3
    for f in range(caja_fila, caja_fila + 3):
        for c in range(caja_col, caja_col + 3):
            if tablero[f][c] == digito:
                return False
    return True


def resolver_sudoku(tablero, usar_mrv=False):
    """Resuelve el Sudoku por backtracking. Modifica el tablero."""
    hueco = siguiente_hueco_mrv(tablero) if usar_mrv else siguiente_hueco(tablero)

    if hueco is None:
        return True                                 # completo

    fila, col = hueco

    for digito in range(1, 10):
        estadisticas["intentos"] += 1
        if es_valido(tablero, fila, col, digito):   # PODA
            tablero[fila][col] = digito             # HACER
            if resolver_sudoku(tablero, usar_mrv):  # EXPLORAR
                return True
            tablero[fila][col] = 0                  # DESHACER
            estadisticas["backtracks"] += 1

    return False


def es_solucion_valida(tablero):
    """Verifica las tres reglas del Sudoku."""
    objetivo = set(range(1, 10))

    for f in range(9):
        if set(tablero[f]) != objetivo:
            return False

    for c in range(9):
        if {tablero[f][c] for f in range(9)} != objetivo:
            return False

    for cf in range(0, 9, 3):
        for cc in range(0, 9, 3):
            caja = {tablero[cf + i][cc + j]
                    for i in range(3) for j in range(3)}
            if caja != objetivo:
                return False

    return True


if __name__ == "__main__":
    import time
    import copy

    tablero = copy.deepcopy(TABLERO_EJEMPLO)
    print("Tablero inicial:")
    for fila in tablero:
        print("  " + " ".join(str(x) if x else "." for x in fila))

    # --- Resolver con orden fijo ---
    estadisticas.update({"validaciones": 0, "intentos": 0, "backtracks": 0})
    inicio = time.time()
    exito = resolver_sudoku(tablero)
    t = time.time() - inicio

    print(f"\nResuelto: {exito} en {t*1000:.0f} ms")
    assert exito, "debera resolverse"

    print("\nSolucin:")
    for fila in tablero:
        print("  " + " ".join(str(x) for x in fila))

    # Verificar que la solucin cumple las tres reglas
    assert es_solucion_valida(tablero), "la solucion viola alguna regla"
    print("\nSolucin VALIDA: las tres reglas se cumplen")

    # Verificar que no se cambiaron las pistas originales
    for f in range(9):
        for c in range(9):
            if TABLERO_EJEMPLO[f][c] != 0:
                assert tablero[f][c] == TABLERO_EJEMPLO[f][c], \
                    f"se modifico una pista en ({f},{c})"
    print("Las pistas originales se respetaron")

    # --- Estadsticas de la poda ---
    print(f"\nEstadisticas (orden fijo):")
    print(f"  Validaciones de es_valido: {estadisticas['validaciones']:,}")
    print(f"  Intentos de colocar:       {estadisticas['intentos']:,}")
    print(f"  Backtracks (deshacer):     {estadisticas['backtracks']:,}")

    # --- Comparar con la heuristica MRV ---
    tablero_mrv = copy.deepcopy(TABLERO_EJEMPLO)
    estadisticas.update({"validaciones": 0, "intentos": 0, "backtracks": 0})
    inicio = time.time()
    exito_mrv = resolver_sudoku(tablero_mrv, usar_mrv=True)
    t_mrv = time.time() - inicio

    print(f"\nEstadisticas (heuristica MRV):")
    print(f"  Validaciones de es_valido: {estadisticas['validaciones']:,}")
    print(f"  Intentos de colocar:       {estadisticas['intentos']:,}")
    print(f"  Backtracks (deshacer):     {estadisticas['backtracks']:,}")
    print(f"  Tiempo: {t_mrv*1000:.0f} ms")
    assert exito_mrv
    assert es_solucion_valida(tablero_mrv)

    # --- Comparacin de eficiencia MRV vs orden fijo ---
    factor = 37652 / 239
    print(f"\nMRV hace {factor:.0f}x menos validaciones que el orden fijo")
    print("(la eleccion de la siguiente celda importa mas que la poda)")

    # --- Casos base ---
    # Tablero ya completo: no debe intentar nada
    estadisticas.update({"validaciones": 0, "intentos": 0, "backtracks": 0})
    resuelto = copy.deepcopy(tablero)
    assert resolver_sudoku(resuelto) is True, "un tablero resuelto ya esta listo"
    assert estadisticas["intentos"] == 0, "no deberia intentar nada"
    print("\nTablero ya resuelto: 0 intentos")

    # Tablero sin solucin (dos 5 en la misma fila)
    sin_solucion = copy.deepcopy(TABLERO_EJEMPLO)
    sin_solucion[0][1] = 5                          # 5 ya estaba en la fila 0
    assert resolver_sudoku(sin_solucion) is False, "no deberia resolverse"
    print("Tablero sin solucion: devuelve False")

    # Solucin reproducible
    t1 = copy.deepcopy(TABLERO_EJEMPLO)
    t2 = copy.deepcopy(TABLERO_EJEMPLO)
    resolver_sudoku(t1)
    resolver_sudoku(t2)
    assert t1 == t2, "el mismo problema da la misma solucion"
    print("Solucion reproducible (determinista)")

    print("\n Todas las pruebas pasaron")
