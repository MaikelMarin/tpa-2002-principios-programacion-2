"""
Ejercicio 1: Factorial recursivo
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Inducción matemática (00-fundamentos §3): la corrección se
      demuestra por inducción sobre n.
    - Pila de llamadas (00-fundamentos §9.1): cada llamada recursiva
      consume un marco; de ahí el espacio O(n).

PROBLEMA
    Calcular el factorial de n: el producto de todos los enteros
    desde 1 hasta n. Por convención, 0! = 1.

FONDO MATEMÁTICO
    El factorial es el número de formas de ordenar n elementos
    distintos (permutaciones). Crece más rápido que cualquier
    exponencial de base fija: 20! ya tiene 19 dígitos.

    Definición recursiva:
        0! = 1
        n! = n · (n-1)!   para n ≥ 1

    La definición matemática YA es recursiva. La traducción a código
    es casi literal: la segunda línea es el caso recursivo y la
    convención 0! = 1 es el caso base.

ESTRATEGIA
    No hay que inventar nada: la recurrencia se mapea directo al
    código. La única decisión es dónde poner el caso base.

    Se usa n <= 1 (y no n == 0) porque:
      1. 1! = 1 también, así que es matemáticamente correcto.
      2. Ahorra una llamada (no se invoca factorial(0)).
      3. Protege contra negativos, que caerían en recursión infinita.

TRAZA DE factorial(4)
    Llamada   n   ¿Base?   Cálculo        Retorna
    f(4)      4   No       4 × f(3)       espera
    f(3)      3   No       3 × f(2)       espera
    f(2)      2   No       2 × f(1)       espera
    f(1)      1   Sí       —              1
    f(2)      —    —       2 × 1          2
    f(3)      —    —       3 × 2          6
    f(4)      —    —       4 × 6          24

    Los "retorna" aparecen en orden INVERSO a las llamadas: la pila
    se desapila en LIFO y el valor se acumula al volver.

DEMOSTRACIÓN DE CORRECCIÓN (inducción sobre n)
    Caso base: n = 0. La función retorna 1, y 0! = 1. Correcto.

    Hipótesis inductiva: factorial(k) retorna k! para todo k < n.

    Paso: para n ≥ 1, la función retorna n · factorial(n-1). Por
    hipótesis, factorial(n-1) = (n-1)!. Luego retorna n·(n-1)! = n!.
    Correcto. ∎

COMPLEJIDAD
    Recurrencia: L(n) = L(n-1) + 1, con L(1) = 1  →  L(n) = n.
    Tiempo: O(n)   (una multiplicación por llamada)
    Espacio: O(n)  (un marco de pila por llamada)

CASOS LÍMITE
    - n negativo: se lanza ValueError. Sin esa guarda, la recursión
      nunca alcanzaría el caso base.
    - Desbordamiento: 21! excede el rango de un entero de 64 bits.
      Python tiene enteros de precisión arbitraria, así que no hay
      problema; en Java haría falta BigInteger.

VARIANTES
    - Iterativa: O(1) de espacio (incluida abajo para comparar).
    - De cola: no ahorra memoria en Python (no hay optimización de
      llamada de cola), pero es la forma idiomática en Scheme/Haskell.
"""


def factorial(n):
    """Calcula el factorial de n de forma recursiva.

    Recurrencia: factorial(n) = n · factorial(n-1)
    Caso base:   factorial(0) = factorial(1) = 1
    """
    if n < 0:
        raise ValueError("El factorial no está definido para números negativos")

    if n <= 1:                  # CASO BASE
        return 1

    return n * factorial(n - 1)  # CASO RECURSIVO


def factorial_iterativo(n):
    """Versión iterativa: O(1) de espacio en vez de O(n).

    Se incluye para comparar el coste de memoria de ambas versiones.
    """
    if n < 0:
        raise ValueError("El factorial no está definido para números negativos")

    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


if __name__ == "__main__":
    print("Factoriales del 0 al 10:")
    for i in range(11):
        print(f"  {i:2d}! = {factorial(i)}")

    # Caso base
    assert factorial(0) == 1, "0! debe ser 1 por convención"
    assert factorial(1) == 1, "1! debe ser 1"

    # Valores conocidos
    assert factorial(5) == 120
    assert factorial(10) == 3628800

    # Coincide con la versión iterativa
    for n in range(15):
        assert factorial(n) == factorial_iterativo(n), f"discrepancia en n={n}"

    # Entrada inválida
    try:
        factorial(-1)
        raise AssertionError("debía lanzar ValueError")
    except ValueError:
        pass

    print("\n✓ Todas las pruebas pasaron")
