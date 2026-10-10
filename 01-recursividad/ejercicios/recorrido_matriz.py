"""
Ejercicio 6: Recorrido recursivo de matriz
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Inducción doble (o inducción sobre pares ordenados).
    - Lista de listas: una matriz es una lista cuyos elementos son
      a su vez listas (las filas).

PROBLEMA
    Recorrer todos los elementos de una matriz (lista de listas) de
    forma recursiva, visitándolos en orden fila por fila.

FONDO MATEMÁTICO
    Una matriz de m×n se puede ver de dos formas, y ambas dan una
    recursión válida:

    Vista 1 — un solo índice lineal sobre m·n posiciones:
        pos = fila * n + col
        Avanzar en col hasta n, luego saltar a la siguiente fila.

    Vista 2 — recursión sobre filas, y dentro de cada fila recursión
        sobre columnas (recursión mutua):
            recorrer_filas(matriz)  llama a  recorrer_columnas(fila)
            recorrer_columnas(fila) llama a  recorrer_columnas(fila)

    La vista 1 es más simple de implementar con dos parámetros.

ESTRATEGIA
    Usar dos parámetros (fila, col) y dos reglas de avance:
      1. Si col llegó al final de la fila, pasar a (fila+1, 0).
      2. En otro caso, procesar el elemento actual y avanzar a (fila, col+1).
    El caso base es fila >= número de filas.

    Es exactamente un contador en base n, recorrido de forma recursiva.

TRAZA DE recorrer([[1,2],[3,4]], 0, 0)
    Llamada            (f,c)   Acción
    recorrer(M,0,0)    (0,0)   imprime 1 → recorrer(M,0,1)
    recorrer(M,0,1)    (0,1)   imprime 2 → recorrer(M,0,2)
    recorrer(M,0,2)    (0,2)   col=2=n → recorrer(M,1,0)
    recorrer(M,1,0)    (1,0)   imprime 3 → recorrer(M,1,1)
    recorrer(M,1,1)    (1,1)   imprime 4 → recorrer(M,1,2)
    recorrer(M,1,2)    (1,2)   col=n → recorrer(M,2,0)
    recorrer(M,2,0)    (2,0)   fila=2=m → CASO BASE, retorna

    Salida: 1 2 3 4

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción sobre fila*n + col (la posición lineal).

    Caso base: fila = m. No quedan elementos; se retorna. Correcto.

    Hipótesis: desde toda posición (f, c) con f*n + c < m*n, la función
    visita todos los elementos desde esa posición hasta el final.

    Paso: desde (f, c) con c < n, imprime el elemento actual y llama
    a (f, c+1), que por hipótesis visita el resto. Si c = n, llama a
    (f+1, 0), que por hipótesis visita el resto de la matriz. ∎

COMPLEJIDAD
    Sea N = m·n el número total de elementos.
    Tiempo: O(N) — cada elemento se visita una vez.
    Espacio: O(N) de pila — ¡un marco por elemento!

    Este último punto es importante: la profundidad de recursión es N,
    no log(N) ni m. Para una matriz de 100×100 serían 10,000 marcos,
    muy por encima del límite de ~1000 de Python.

    CONCLUSIÓN PRÁCTICA: para recorridos simples de matrices, la
    iteración doble es preferible. La recursión sobre matrices se
    reserva para algoritmos que se benefician de dividir, como la
    multiplicación de Strassen (divide y vencerás, O(n^2.81)).

DÓNDE SÍ CONVIENE LA RECURSIÓN SOBRE MATRICES
    - Multiplicación de matrices (Strassen): partir en 4 submatrices.
    - Rotación por capas.
    - Búsqueda en matriz ordenada (dividir en cuadrantes).
    - Detección de una submatriz dentro de otra.

CASOS LÍMITE
    - Matriz vacía (m = 0): retorna inmediatamente.
    - Matriz con filas vacías: si n = 0, col >= 0 siempre, así que
      avanza de fila sin imprimir nada.
    - Matriz no rectangular: el código usa matriz[0] como referencia
      de ancho; si las filas tienen distinto largo, falla. Es una
      precondición que debe documentarse.
"""


def recorrer_matriz(matriz, fila=0, col=0):
    """Recorre una matriz recursivamente en orden fila por fila.

    Precondición: todas las filas tienen la misma longitud.
    """
    if not matriz:                      # matriz vacía
        return
    if fila >= len(matriz):             # caso base: se acabaron las filas
        return
    if col >= len(matriz[0]):           # fin de la fila → siguiente fila
        recorrer_matriz(matriz, fila + 1, 0)
        return

    print(matriz[fila][col], end=" ")
    recorrer_matriz(matriz, fila, col + 1)


def suma_matriz(matriz, fila=0, col=0):
    """Suma todos los elementos de una matriz recursivamente."""
    if not matriz:
        return 0
    if fila >= len(matriz):
        return 0
    if col >= len(matriz[0]):
        return suma_matriz(matriz, fila + 1, 0)

    return matriz[fila][col] + suma_matriz(matriz, fila, col + 1)


def buscar_matriz(matriz, objetivo, fila=0, col=0):
    """Busca un elemento en una matriz. Devuelve (fila, col) o None."""
    if not matriz:
        return None
    if fila >= len(matriz):
        return None
    if col >= len(matriz[0]):
        return buscar_matriz(matriz, objetivo, fila + 1, 0)

    if matriz[fila][col] == objetivo:
        return (fila, col)
    return buscar_matriz(matriz, objetivo, fila, col + 1)


if __name__ == "__main__":
    matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    print("Recorrido: ", end="")
    recorrer_matriz(matriz)
    print()

    print(f"\nSuma total:  {suma_matriz(matriz)}")
    print(f"Buscar 5:    {buscar_matriz(matriz, 5)}")
    print(f"Buscar 1:    {buscar_matriz(matriz, 1)}")
    print(f"Buscar 9:    {buscar_matriz(matriz, 9)}")
    print(f"Buscar 100:  {buscar_matriz(matriz, 100)}")

    # Matriz 3x3 con 1..9
    assert suma_matriz(matriz) == 45
    assert buscar_matriz(matriz, 5) == (1, 1)
    assert buscar_matriz(matriz, 1) == (0, 0), "primera posición"
    assert buscar_matriz(matriz, 9) == (2, 2), "última posición"
    assert buscar_matriz(matriz, 100) is None, "no encontrado"

    # Casos límite
    assert suma_matriz([]) == 0
    assert buscar_matriz([], 5) is None
    assert suma_matriz([[]]) == 0, "fila vacía"

    # Matriz de un elemento
    assert suma_matriz([[42]]) == 42
    assert buscar_matriz([[42]], 42) == (0, 0)

    # La suma coincide con la iterativa (doble verificación)
    suma_iterativa = sum(sum(fila) for fila in matriz)
    assert suma_matriz(matriz) == suma_iterativa

    print("\n✓ Todas las pruebas pasaron")
