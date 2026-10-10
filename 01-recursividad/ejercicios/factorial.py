"""
Ejercicio 1: Factorial recursivo
Dificultad: Básico

Definición matemática:
    n! = n × (n-1) × (n-2) × ... × 1
    0! = 1

Recurrencia:
    factorial(n) = n × factorial(n-1)
    factorial(0) = 1
"""

def factorial(n):
    """Calcula el factorial de n de forma recursiva."""
    if n < 0:
        raise ValueError("El factorial no está definido para números negativos")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


def factorial_iterativo(n):
    """Versión iterativa para comparación."""
    if n < 0:
        raise ValueError("El factorial no está definido para números negativos")
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


if __name__ == "__main__":
    for i in range(11):
        print(f"{i}! = {factorial(i)}")

    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(10) == 3628800
    assert factorial(5) == factorial_iterativo(5)
    print("\n✓ Todas las pruebas pasaron")
