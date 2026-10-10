"""
Ejercicio 3: Fibonacci recursivo
Dificultad: Básico

Definición:
    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2)  para n > 1

Complejidad: O(2^n) — exponencial (ineficiente para n grande)
"""

def fibonacci(n):
    """Calcula el n-ésimo número de Fibonacci de forma recursiva ingenua."""
    if n < 0:
        raise ValueError("n debe ser no negativo")
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == "__main__":
    print("Serie de Fibonacci (primeros 15 términos):")
    for i in range(15):
        print(f"F({i}) = {fibonacci(i)}")

    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(10) == 55
    assert fibonacci(15) == 610
    print("\n✓ Todas las pruebas pasaron")
