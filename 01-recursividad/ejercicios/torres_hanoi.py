"""
Ejercicio 9: Torres de Hanói
Dificultad: Intermedio

Historia: Inventado por Édouard Lucas en 1883.

Reglas:
1. Solo se puede mover un disco a la vez
2. Un disco grande no puede estar encima de uno pequeño
3. Solo se puede mover el disco superior de cada torre

Solución recursiva:
    1. Mover n-1 discos de origen a auxiliar
    2. Mover el disco n de origen a destino
    3. Mover n-1 discos de auxiliar a destino

Número mínimo de movimientos: 2^n - 1
"""

def torres_hanoi(n, origen="A", destino="C", auxiliar="B"):
    """Resuelve las Torres de Hanói recursivamente."""
    if n == 1:
        print(f"Mover disco 1 de {origen} a {destino}")
        return 1
    movimientos = 0
    movimientos += torres_hanoi(n - 1, origen, auxiliar, destino)
    print(f"Mover disco {n} de {origen} a {destino}")
    movimientos += 1
    movimientos += torres_hanoi(n - 1, auxiliar, destino, origen)
    return movimientos


def torres_hanoi_visual(n):
    """Versión con representación visual del estado."""
    torres = {
        "A": list(range(n, 0, -1)),
        "B": [],
        "C": []
    }

    def mostrar():
        print(f"  A: {torres['A']}")
        print(f"  B: {torres['B']}")
        print(f"  C: {torres['C']}")
        print()

    def mover(n, origen, destino, auxiliar):
        if n == 1:
            disco = torres[origen].pop()
            torres[destino].append(disco)
            print(f"Mover disco {disco} de {origen} a {destino}")
            mostrar()
            return 1
        mov = 0
        mov += mover(n - 1, origen, auxiliar, destino)
        disco = torres[origen].pop()
        torres[destino].append(disco)
        print(f"Mover disco {disco} de {origen} a {destino}")
        mostrar()
        mov += 1
        mov += mover(n - 1, auxiliar, destino, origen)
        return mov

    print(f"Estado inicial (n={n}):")
    mostrar()
    return mover(n, "A", "C", "B")


if __name__ == "__main__":
    n = 3
    print(f"=== Torres de Hanói con {n} discos ===\n")
    movimientos = torres_hanoi(n)
    print(f"\nTotal de movimientos: {movimientos}")
    print(f"Mínimo teórico (2^{n} - 1): {2**n - 1}")
    assert movimientos == 2**n - 1

    print(f"\n=== Versión visual ===\n")
    movimientos_visual = torres_hanoi_visual(3)
    assert movimientos_visual == 7
    print("\n✓ Todas las pruebas pasaron")
