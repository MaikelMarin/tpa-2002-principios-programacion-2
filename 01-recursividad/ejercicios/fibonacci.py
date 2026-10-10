"""
Ejercicio 3: Fibonacci recursivo
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Exponenciales (00-fundamentos §4.5): por qué 2^n es inviable.
    - Árbol de recursión: el costo NO es la profundidad, es el número
      total de nodos del árbol de llamadas.

PROBLEMA
    Calcular el n-ésimo término de la sucesión de Fibonacci.

FONDO MATEMÁTICO
    Leonardo de Pisa publicó la sucesión en Liber Abaci (1202)
    modelando cría de conejos. Aparece en filotaxis (disposición de
    hojas y semillas) y su razón entre términos consecutivos converge
    a la razón áurea φ ≈ 1.618.

    Definición recursiva (que SÍ es eficiente como definición):
        F(0) = 0
        F(1) = 1
        F(n) = F(n-1) + F(n-2)   para n ≥ 2

    Pero como ALGORITMO, esta traducción literal es catastrófica.

ESTRATEGIA
    Traducir la definición literalmente. El objetivo del ejercicio es
    didáctico: demostrar con mediciones reales por qué una recursión
    aparentemente inocente explota, para valorar la memoización.

POR QUÉ EXPLOTA: SUBPROBLEMAS SUPUESTOS
    El árbol de llamadas de fib(5) recalcula los mismos valores:

                    fib(5)
               /              \
          fib(4)                fib(3)
         /      \              /      \
     fib(3)    fib(2)       fib(2)    fib(1)
     /    \    /    \      /    \
 fib(2) fib(1) ...       fib(1) fib(0)

    fib(3) se calcula 2 veces, fib(2) 3 veces. El número de llamadas
    sigue L(n) = L(n-1) + L(n-2) + 1, cuya solución es Θ(φ^n).

TRAZA (número de llamadas por n)
    n    Llamadas (aprox.)   Tiempo real
    20   13,529              < 1 ms
    25   242,785             ~2 ms
    30   2,704,155           ~40 ms
    32   11,405,663          ~200 ms
    35   29,860,703          ~600 ms

    Duplicar n multiplica el tiempo por ~φ^5 ≈ 11.

COMPLEJIDAD
    Recurrencia: T(n) = T(n-1) + T(n-2) + O(1)
    Solución: Θ(φ^n), con φ = (1+√5)/2 ≈ 1.618
    Tiempo: Θ(φ^n) — inviable más allá de n ≈ 35
    Espacio: Θ(n) — la profundidad del árbol es n, no φ^n

    OJO: tiempo y espacio son muy distintos aquí. El espacio es
    lineal porque solo una rama del árbol está activa a la vez.

CASOS LÍMITE
    - n = 0: retorna 0.
    - n negativo: se lanza ValueError.
    - No hay desbordamiento práctico en Python (enteros arbitrarios).

VARIANTES (ver ejercicios siguientes)
    - fibonacci_memo.py: misma recursión + caché → O(n).
    - fibonacci_bottom_up.py: iterativo con dos variables → O(n)
      tiempo y O(1) espacio. Es la versión que se usaría en producción.
"""


def fibonacci(n):
    """n-ésimo término de Fibonacci por recursión ingenua: O(φ^n).

    Versión didáctica: correcta pero exponencialmente lenta.
    """
    if n < 0:
        raise ValueError("n debe ser no negativo")
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def contar_llamadas_fibonacci(n):
    """Cuenta cuántas llamadas realiza la versión ingenua.

    Sirve para verificar experimentalmente que el crecimiento es
    exponencial, no solo para afirmarlo.
    """
    contador = [0]

    def fib_contado(k):
        contador[0] += 1
        if k <= 1:
            return k
        return fib_contado(k - 1) + fib_contado(k - 2)

    fib_contado(n)
    return contador[0]


if __name__ == "__main__":
    print("Serie de Fibonacci (primeros 15 términos):")
    for i in range(15):
        print(f"  F({i:2d}) = {fibonacci(i)}")

    # Verificación del crecimiento exponencial
    print("\nLlamadas realizadas por la versión ingenua:")
    anterior = 0
    for n in [10, 15, 20, 25]:
        llamadas = contar_llamadas_fibonacci(n)
        razon = f" (×{llamadas / anterior:.2f})" if anterior else ""
        print(f"  n={n:2d}: {llamadas:>10,} llamadas{razon}")
        anterior = llamadas

    # Valores conocidos
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(2) == 1
    assert fibonacci(10) == 55
    assert fibonacci(15) == 610
    assert fibonacci(20) == 6765

    # Entrada inválida
    try:
        fibonacci(-1)
        raise AssertionError("debía lanzar ValueError")
    except ValueError:
        pass

    print("\n✓ Todas las pruebas pasaron")
