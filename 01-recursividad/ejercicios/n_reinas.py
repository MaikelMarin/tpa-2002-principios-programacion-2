"""
Ejercicio 8: N reinas (Backtracking)
Dificultad: Avanzado

Problema: Colocar N reinas en un tablero N×N de manera que ninguna
se ataque entre sí.

Historia:
- 1848: Max Bezzel plantea el problema original (8 reinas)
- 1850: Franz Nauck encuentra la primera solución
- 1970s: Se convierte en problema canónico de backtracking

Restricciones:
- No pueden compartir fila
- No pueden compartir columna
- No pueden compartir diagonal
"""

def es_seguro(tablero, fila, col, n):
    """Verifica si es seguro colocar una reina en (fila, col)."""
    # Verificar columna
    for i in range(fila):
        if tablero[i][col] == 1:
            return False
    # Verificar diagonal superior izquierda
    for i, j in zip(range(fila, -1, -1), range(col, -1, -1)):
        if tablero[i][j] == 1:
            return False
    # Verificar diagonal superior derecha
    for i, j in zip(range(fila, -1, -1), range(col, n)):
        if tablero[i][j] == 1:
            return False
    return True


def resolver_n_reinas(tablero, col, n, soluciones=None):
    """Resuelve el problema de las N reinas usando backtracking."""
    if soluciones is None:
        soluciones = []
    if col >= n:
        # Solución encontrada: copiar el tablero
        solucion = [fila[:] for fila in tablero]
        soluciones.append(solucion)
        return True
    for fila in range(n):
        if es_seguro(tablero, fila, col, n):
            tablero[fila][col] = 1  # Colocar reina
            resolver_n_reinas(tablero, col + 1, n, soluciones)
            tablero[fila][col] = 0  # Backtrack: quitar reina
    return len(soluciones) > 0


def n_reinas(n, mostrar=True):
    """Encuentra todas las soluciones para el problema de N reinas."""
    tablero = [[0] * n for _ in range(n)]
    soluciones = []
    resolver_n_reinas(tablero, 0, n, soluciones)
    if mostrar:
        print(f"N={n}: {len(soluciones)} soluciones encontradas")
        for idx, solucion in enumerate(soluciones[:3]):  # Mostrar primeras 3
            print(f"\nSolución {idx + 1}:")
            for fila in solucion:
                print(" ".join("Q" if c == 1 else "." for c in fila))
    return soluciones


if __name__ == "__main__":
    import time

    for n in [4, 5, 6, 8]:
        inicio = time.time()
        soluciones = n_reinas(n, mostrar=(n <= 6))
        tiempo = time.time() - inicio
        print(f"  Tiempo: {tiempo:.4f}s\n")

    # Verificar cantidades conocidas
    assert len(n_reinas(4, mostrar=False)) == 2
    assert len(n_reinas(5, mostrar=False)) == 10
    assert len(n_reinas(6, mostrar=False)) == 4
    assert len(n_reinas(8, mostrar=False)) == 92
    print("✓ Todas las pruebas pasaron")
