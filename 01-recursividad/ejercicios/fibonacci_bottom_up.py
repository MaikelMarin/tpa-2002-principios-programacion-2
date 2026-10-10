"""
Ejercicio 13: Fibonacci bottom-up
Dificultad: Intermedio

Versión iterativa de programación dinámica (bottom-up).
Complejidad: O(n) tiempo, O(1) espacio.
"""

def fibonacci_bottom_up(n):
    """Calcula Fibonacci de forma iterativa con espacio constante."""
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


def fibonacci_tabla(n):
    """Versión con tabla completa (para ver todos los valores)."""
    if n < 0:
        raise ValueError("n debe ser no negativo")
    if n <= 0:
        return [0]
    tabla = [0] * (n + 1)
    tabla[1] = 1
    for i in range(2, n + 1):
        tabla[i] = tabla[i - 1] + tabla[i - 2]
    return tabla


if __name__ == "__main__":
    n = 20
    print(f"Fibonacci bottom-up F({n}) = {fibonacci_bottom_up(n)}")
    print(f"Tabla completa: {fibonacci_tabla(n)}")

    assert fibonacci_bottom_up(0) == 0
    assert fibonacci_bottom_up(1) == 1
    assert fibonacci_bottom_up(10) == 55
    assert fibonacci_bottom_up(50) == 12586269025
    assert fibonacci_bottom_up(100) == 354224848179261915075
    print("\n✓ Todas las pruebas pasaron")
