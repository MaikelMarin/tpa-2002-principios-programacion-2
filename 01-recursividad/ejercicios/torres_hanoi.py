"""
Ejercicio 9: Torres de Hanói
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Divide y vencerás con reducción n-1 (no n/2).
    - Resolución de recurrencias por sustitución (00-fundamentos §7.3).

PROBLEMA
    Mover una torre de n discos de la aguja origen a la aguja destino,
    usando una aguja auxiliar, cumpliendo tres reglas.

REGLAS
    1. Solo se mueve un disco a la vez.
    2. Un disco grande nunca puede colocarse sobre uno más pequeño.
    3. Solo se puede mover el disco superior de una torre.

HISTORIA
    Inventado por Édouard Lucas en 1883. La leyenda dice que un
    monasterio mueve 64 discos de oro entre tres agujas de diamante;
    cuando terminen, se acaba el mundo.

    Con la solución óptima se necesitan 2^64 - 1 ≈ 1.84 × 10^19
    movimientos. A un segundo por movimiento: unos 585,000 millones
    de años. La leyenda es una forma pintoresca de decir que O(2^n)
    es inviable.

FONDO MATEMÁTICO
    La observación que hace funcionar la recursión:

        Para mover n discos de A a C, PRIMERO hay que liberar el disco
        más grande (el n), que está en el fondo. Para eso hay que
        mover los n-1 discos de arriba a la aguja auxiliar B.

    Es decir: el problema de tamaño n se resuelve con:
        1. Resolver el problema de tamaño n-1 (A → B).
        2. Mover el disco grande (A → C).
        3. Resolver el problema de tamaño n-1 otra vez (B → C).

    Los pasos 1 y 3 son EL MISMO problema con un disco menos. Esa es
    la recursión.

ESTRATEGIA (código)

```python
def torres_hanoi(n, origen, destino, auxiliar):
    if n == 1:                      # caso base: un disco
        mover(1, origen, destino)
        return 1
    movimientos = 0
    movimientos += torres_hanoi(n-1, origen, auxiliar, destino)  # 1
    mover(n, origen, destino)                                    # 2
    movimientos += 1
    movimientos += torres_hanoi(n-1, auxiliar, destino, origen)  # 3
    return movimientos
```

TRAZA DE torres_hanoi(3)  (A=origen, B=auxiliar, C=destino)
    Llamada              n   Acción
    h(3,A→C)             3   → h(2,A→B)
    ↳ h(2,A→B)           2   → h(1,A→C)
    ↳↳ h(1,A→C)          1   MUEVE disco 1: A→C
    ↳ h(2,A→B)           2   MUEVE disco 2: A→B
    ↳ h(2,A→B)           2   → h(1,C→B)
    ↳↳ h(1,C→B)          1   MUEVE disco 1: C→B
    h(3,A→C)             3   MUEVE disco 3: A→C
    h(3,A→C)             3   → h(2,B→C)
    ↳ h(2,B→C)           2   → h(1,B→A)
    ↳↳ h(1,B→A)          1   MUEVE disco 1: B→A
    ↳ h(2,B→C)           2   MUEVE disco 2: B→C
    ↳ h(2,B→C)           2   → h(1,A→C)
    ↳↳ h(1,A→C)          1   MUEVE disco 1: A→C

    Total: 7 movimientos.

ANÁLISIS
    Recurrencia: T(n) = 2·T(n-1) + 1, con T(1) = 1.

    Resolución por sustitución:
        T(n) = 2T(n-1) + 1
             = 2[2T(n-2) + 1] + 1 = 4T(n-2) + 2 + 1
             = 4[2T(n-3) + 1] + 3 = 8T(n-3) + 4 + 2 + 1
             = ...
             = 2^(n-1)·T(1) + (2^(n-2) + ... + 2 + 1)
             = 2^(n-1) + (2^(n-1) - 1)
             = 2^n - 1

    Resultado: T(n) = 2^n - 1.

    OPTIMALIDAD: está demostrado que 2^n - 1 es el número MÍNIMO de
    movimientos. No existe algoritmo que lo haga mejor. La razón:
    para mover el disco n (el grande) hace falta tener los otros n-1
    en la aguja auxiliar, y esa configuración requiere al menos
    T(n-1) movimientos; luego hay que mover el disco n y repetir.

DEMOSTRACIÓN DE CORRECCIÓN (inducción sobre n)
    Caso base: n = 1. Se mueve el disco directamente. Válido.

    Hipótesis: torres_hanoi(k) mueve k discos correctamente.

    Paso: para n discos, el paso 1 mueve los n-1 de arriba al auxiliar
    (válido por hipótesis, y el disco grande queda libre). El paso 2
    mueve el disco grande a su destino (válido: el destino está vacío
    o tiene discos más grandes). El paso 3 mueve los n-1 encima del
    grande (válido por hipótesis, y ninguno es mayor que el grande).
    Al final los n discos están en el destino, en orden. ∎

COMPLEJIDAD
    Tiempo: Θ(2^n) — imparable para n ≥ 30.
    Espacio: Θ(n) de pila (la profundidad es n, no 2^n).

COMPARACIÓN RECURSIÓN vs ITERACIÓN
    La solución recursiva son ~10 líneas y es evidente. La iterativa
    existe y es O(1) de espacio, pero es considerablemente más larga
    y difícil de entender, y no por eso más rápida.

    Regla: cuando la recursión es clara y la profundidad es pequeña
    (n discos → profundidad n), la recursión gana por legibilidad.

GENERALIZACIÓN ABIERTA
    Con 3 torres, 2^n - 1 es óptimo y demostrado. Con 4 torres, el
    algoritmo de Frame-Stewart (1941) es más eficiente, pero NO se ha
    demostrado que sea óptimo para todo n. Es uno de los problemas
    abiertos más conocidos de la matemática recreativa.
"""


def torres_hanoi(n, origen="A", destino="C", auxiliar="B"):
    """Resuelve las Torres de Hanói. Devuelve el número de movimientos.

    Imprime cada movimiento. Con n discos realiza exactamente 2^n - 1.
    """
    if n == 1:                          # caso base
        print(f"Mover disco 1 de {origen} a {destino}")
        return 1

    movimientos = 0

    # Paso 1: mover los n-1 de arriba al auxiliar (libera el grande)
    movimientos += torres_hanoi(n - 1, origen, auxiliar, destino)

    # Paso 2: mover el disco grande a su destino
    print(f"Mover disco {n} de {origen} a {destino}")
    movimientos += 1

    # Paso 3: mover los n-1 del auxiliar al destino, encima del grande
    movimientos += torres_hanoi(n - 1, auxiliar, destino, origen)

    return movimientos


def torres_hanoi_visual(n):
    """Versión con estado visible, para entender qué ocurre en cada paso."""
    torres = {
        "A": list(range(n, 0, -1)),     # el disco grande (n) abajo
        "B": [],
        "C": []
    }

    def mostrar():
        for nombre in ["A", "B", "C"]:
            print(f"  {nombre}: {torres[nombre]}")
        print()

    def mover(n, origen, destino, auxiliar):
        if n == 1:
            disco = torres[origen].pop()
            torres[destino].append(disco)
            print(f"Mover disco {disco} de {origen} a {destino}")
            mostrar()
            return 1

        mov = mover(n - 1, origen, auxiliar, destino)

        disco = torres[origen].pop()
        torres[destino].append(disco)
        print(f"Mover disco {disco} de {origen} a {destino}")
        mostrar()
        mov += 1

        mov += mover(n - 1, auxiliar, destino, origen)
        return mov

    print(f"Estado inicial ({n} discos):")
    mostrar()
    return mover(n, "A", "C", "B")


if __name__ == "__main__":
    print("=== Torres de Hanói con 3 discos ===\n")
    movimientos = torres_hanoi(3)
    print(f"\nTotal de movimientos: {movimientos}")
    print(f"Mínimo teórico (2^3 - 1): {2**3 - 1}")
    assert movimientos == 7

    # Verificar la fórmula 2^n - 1 para varios n
    print("\nVerificación de la fórmula 2^n - 1:")
    for n in range(1, 8):
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):   # silenciar salida
            m = torres_hanoi(n)
        assert m == 2**n - 1, f"n={n}: {m} != {2**n - 1}"
        print(f"  n={n}: {m:>3d} movimientos  (= 2^{n} - 1)")

    # Versión visual
    print("\n=== Versión visual (3 discos) ===\n")
    movimientos_visual = torres_hanoi_visual(3)
    assert movimientos_visual == 7

    print("\n✓ Todas las pruebas pasaron")
