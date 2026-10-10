"""
Ejercicio 8: N reinas (Backtracking)
Dificultad: Avanzado

PROBLEMA
    Colocar N reinas en un tablero de N×N de manera que ninguna
    ataque a otra. Dos reinas se atacan si comparten fila, columna
    o diagonal.

HISTORIA
    1848: Max Bezzel plantea el problema original (8 reinas).
    1850: Franz Nauck publica la primera solución.
    1970s: Se convierte en el problema canónico de backtracking.

ESTRATEGIA
    Colocar las reinas columna por columna. Como cada reina va en una
    columna distinta, las columnas NUNCA colisionan: solo hay que
    verificar filas y diagonales. Esto reduce el espacio de búsqueda
    de N^N (probar cada casilla) a N! (una posición por columna).

    ¿Por qué columna por columna y no casilla por casilla? Porque
    reduce el factor de ramificación: en la columna k solo quedan
    N-k filas libres como máximo.

    El algoritmo es backtracking puro:
        1. HACER: colocar una reina en una fila segura.
        2. EXPLORAR: pasar a la siguiente columna.
        3. DESHACER: si no funcionó, quitar la reina y probar otra fila.

INVARIANTE
    Al entrar en la columna `col`, las reinas de las columnas
    0 .. col-1 están colocadas y no se atacan entre sí.

CORRECCIÓN
    - Inicialización: en col=0 no hay reinas previas; el invariante se cumple.
    - Conservación: solo se coloca una reina si es_segura() confirma que
      no ataca a ninguna de las ya colocadas, así que el invariante se
      preserva al avanzar.
    - Terminación: si col llega a N, todas las reinas están colocadas y,
      por el invariante, no se atacan. Es una solución válida.

COMPLEJIDAD
    - Tiempo: O(N!) en el peor caso. Con la poda de es_segura, el número
      real de nodos explorados es mucho menor.
    - Espacio: O(N) de pila de recursión + O(N^2) por el tablero.

NÚMERO DE SOLUCIONES (para verificar)
    N=1 → 1    N=5 → 10   N=8  → 92
    N=4 → 2    N=6 → 4    N=10 → 724
"""


def es_segura(tablero, fila, col, n):
    """¿Es seguro colocar una reina en (fila, col)?

    Verifica las tres formas de ataque posibles dado que las reinas
    se colocan columna por columna:
      1. Misma fila (en columnas anteriores).
      2. Diagonal arriba-izquierda.
      3. Diagonal abajo-izquierda.
    """
    # 1. Misma fila: revisar las columnas ya ocupadas (0 .. col-1)
    for j in range(col):
        if tablero[fila][j] == 1:
            return False

    # 2. Diagonal arriba-izquierda: (fila-1, col-1), (fila-2, col-2)...
    for i, j in zip(range(fila, -1, -1), range(col, -1, -1)):
        if tablero[i][j] == 1:
            return False

    # 3. Diagonal abajo-izquierda: (fila+1, col-1), (fila+2, col-2)...
    for i, j in zip(range(fila, n, 1), range(col, -1, -1)):
        if tablero[i][j] == 1:
            return False

    return True


def resolver_n_reinas(tablero, col, n, soluciones=None):
    """Resuelve el problema de las N reinas por backtracking.

    Devuelve True si encontró al menos una solución, y acumula todas
    las encontradas en la lista `soluciones`.
    """
    if soluciones is None:
        soluciones = []

    # Caso base: se cubrieron todas las columnas
    if col >= n:
        soluciones.append([fila[:] for fila in tablero])  # copia
        return True

    for fila in range(n):
        if es_segura(tablero, fila, col, n):   # PODA
            tablero[fila][col] = 1             # HACER
            resolver_n_reinas(tablero, col + 1, n, soluciones)  # EXPLORAR
            tablero[fila][col] = 0             # DESHACER

    return len(soluciones) > 0


def n_reinas(n, mostrar=True):
    """Encuentra todas las soluciones para el problema de N reinas."""
    tablero = [[0] * n for _ in range(n)]
    soluciones = []
    resolver_n_reinas(tablero, 0, n, soluciones)

    if mostrar:
        print(f"N={n}: {len(soluciones)} soluciones encontradas")
        for idx, solucion in enumerate(soluciones[:3]):  # solo las 3 primeras
            print(f"\nSolución {idx + 1}:")
            for fila in solucion:
                print(" ".join("Q" if c == 1 else "." for c in fila))
    return soluciones


if __name__ == "__main__":
    import time

    # Verificación contra los valores conocidos
    for n in [1, 4, 5, 6, 8]:
        inicio = time.time()
        soluciones = n_reinas(n, mostrar=(n <= 6))
        tiempo = time.time() - inicio
        print(f"  Tiempo: {tiempo:.4f}s\n")

    # Los conteos oficiales (OEIS A000170)
    assert len(n_reinas(1, mostrar=False)) == 1
    assert len(n_reinas(4, mostrar=False)) == 2
    assert len(n_reinas(5, mostrar=False)) == 10
    assert len(n_reinas(6, mostrar=False)) == 4
    assert len(n_reinas(8, mostrar=False)) == 92
    print("✓ Todas las pruebas pasaron")
