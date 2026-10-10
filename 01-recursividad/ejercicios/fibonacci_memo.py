"""
Ejercicio 7: Fibonacci con memoización
Dificultad: Intermedio

La memoización es una técnica de programación dinámica que almacena
resultados previamente calculados para evitar recalcularlos.

Complejidad: O(n) tiempo, O(n) espacio
"""

def fibonacci_memo(n, memo=None):
    """Calcula Fibonacci con memoización (top-down)."""
    if memo is None:
        memo = {}
    if n < 0:
        raise ValueError("n debe ser no negativo")
    if n in memo:
        return memo[n]
    if n <= 0:
        return 0
    if n == 1:
        return 1
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def fibonacci_bottom_up(n):
    """Versión bottom-up (iterativa) — O(n) tiempo, O(1) espacio."""
    if n < 0:
        raise ValueError("n debe ser no negativo")
    if n <= 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


if __name__ == "__main__":
    import time

    # Comparación de rendimiento
    n = 35

    inicio = time.time()
    resultado_ingenuo = fibonacci_ingenuo(n) if 'fibonacci_ingenuo' in dir() else None
    # No ejecutamos el ingenuo para n=35 porque es muy lento

    inicio = time.time()
    resultado_memo = fibonacci_memo(n)
    tiempo_memo = time.time() - inicio

    inicio = time.time()
    resultado_bottom = fibonacci_bottom_up(n)
    tiempo_bottom = time.time() - inicio

    print(f"F({n}) con memoización = {resultado_memo} ({tiempo_memo:.6f}s)")
    print(f"F({n}) bottom-up = {resultado_bottom} ({tiempo_bottom:.6f}s)")

    # Pruebas con n grande
    print(f"\nF(100) = {fibonacci_memo(100)}")
    print(f"F(100) bottom-up = {fibonacci_bottom_up(100)}")

    assert fibonacci_memo(0) == 0
    assert fibonacci_memo(1) == 1
    assert fibonacci_memo(10) == 55
    assert fibonacci_memo(50) == 12586269025
    assert fibonacci_bottom_up(100) == fibonacci_memo(100)
    print("\n✓ Todas las pruebas pasaron")
