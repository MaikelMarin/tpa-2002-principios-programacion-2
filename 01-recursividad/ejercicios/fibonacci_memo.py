"""
Ejercicio 7: Fibonacci con memoización
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Tabla hash (00-fundamentos §8.6): el caché es un diccionario
      con acceso O(1) promedio.
    - Subproblemas superpuestos: el concepto que hace necesaria la
      memoización.

PROBLEMA
    El mismo Fibonacci, pero sin recalcular lo ya calculado.

FONDO MATEMÁTICO
    La recursión ingenua repite trabajo: fib(3) se calcula 2 veces,
    fib(2) 3 veces, y así. La memoización guarda cada resultado la
    primera vez que se obtiene y lo reutiliza después.

    Es la idea central de la PROGRAMACIÓN DINÁMICA:
        1. El problema tiene subestructura óptima.
        2. Los subproblemas se superan (se repiten).
    Basta con esas dos condiciones para que la memoización funcione.

ESTRATEGIA
    1. Mantener un diccionario `memo` de valor ya calculado.
    2. Antes de recursar, consultar si el valor está en memo.
    3. Si está, devolverlo inmediatamente (O(1)).
    4. Si no, calcularlo, guardarlo, y devolverlo.

    Cada valor de 0 a n se calcula exactamente UNA vez. El árbol de
    recursión se convierte en una cadena lineal.

IMPLEMENTACIÓN

```python
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:                      # ← ya calculado
        return memo[n]
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]
```

Nota: se usa `memo=None` como valor por defecto y se crea el
diccionario dentro, en vez de `memo={}` en la firma. Es un detalle
importante de Python: los argumentos por defecto se evalúan UNA sola
vez al definir la función, así que un `memo={}` sería COMPARTIDO entre
todas las llamadas y acumularía resultados de ejecuciones anteriores.

TRAZA DE fib_memo(5)
    Llamada        Acción                          memo después
    fib_memo(5)    no está → recurre               {}
    fib_memo(4)    no está → recurre               {}
    fib_memo(3)    no está → recurre               {}
    fib_memo(2)    calcula 1, guarda               {2:1}
    fib_memo(1)    caso base                       {2:1}
    fib_memo(3)    1+1=2, guarda                   {2:1,3:2}
    fib_memo(2)    ¡ESTÁ EN MEMO! retorna 1        {2:1,3:2}
    fib_memo(4)    2+1=3, guarda                   {2:1,3:2,4:3}
    fib_memo(3)    ¡ESTÁ EN MEMO! retorna 2        {2:1,3:2,4:3}
    fib_memo(5)    3+2=5, guarda                   {2:1,...,5:5}

    Observe que fib(2) y fib(3) se consultan dos veces pero se
    CALCULAN una sola vez. Es exactamente la diferencia.

DEMOSTRACIÓN DE CORRECCIÓN
    Idéntica a la de la versión ingenua: por inducción sobre n. La
    memoización no cambia qué se devuelve, solo cuándo: si memo[n]
    existe, es porque se guardó el resultado correcto de una llamada
    anterior. ∎

COMPLEJIDAD
    Tiempo: O(n). Cada uno de los n valores se calcula una vez, y
    cada cálculo hace trabajo O(1) (dos consultas al diccionario).
    Espacio: O(n) por el diccionario + O(n) por la pila de recursión.

COMPARACIÓN DE VERSIONES
    Versión              Tiempo      Espacio    Recursión
    Ingenua              Θ(φ^n)      Θ(n)       Sí
    Memoización (esta)   Θ(n)        Θ(n)       Sí
    Bottom-up (siguiente) Θ(n)       Θ(1)       No

    Memoizar fib(40) pasa de ~35 segundos a microsegundos.
"""


def fibonacci_memo(n, memo=None):
    """Fibonacci con memoización (top-down): O(n) tiempo, O(n) espacio.

    El parámetro memo se crea dentro (no como argumento por defecto
    mutable) para que cada llamada externa parta de un caché limpio.
    """
    if memo is None:
        memo = {}

    if n < 0:
        raise ValueError("n debe ser no negativo")

    if n <= 1:                     # casos base
        return n

    if n in memo:                  # ← ya calculado antes
        return memo[n]

    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def fibonacci_bottom_up(n):
    """Fibonacci iterativo con dos variables: O(n) tiempo, O(1) espacio.

    Se incluye para mostrar que la memoización no es la única forma
    de eliminar el recálculo.
    """
    if n < 0:
        raise ValueError("n debe ser no negativo")
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b            # solo dos valores vivos
    return b


if __name__ == "__main__":
    import time

    # La versión memoizada resuelve al instante lo que a la ingenua
    # le tomaría minutos.
    for n in [10, 30, 50, 90]:
        inicio = time.time()
        resultado = fibonacci_memo(n)
        tiempo = time.time() - inicio
        print(f"  F({n:2d}) = {resultado:>25,}  ({tiempo*1000:.3f} ms)")

    # Valores conocidos, incluido uno grande
    assert fibonacci_memo(0) == 0
    assert fibonacci_memo(1) == 1
    assert fibonacci_memo(10) == 55
    assert fibonacci_memo(50) == 12586269025
    assert fibonacci_memo(90) == 2880067194370816120

    # Coincide con la versión bottom-up
    for n in [0, 1, 5, 25, 100]:
        assert fibonacci_memo(n) == fibonacci_bottom_up(n), f"discrepancia en n={n}"

    # El caché no se filtra entre llamadas externas
    assert fibonacci_memo(10) == 55          # segunda llamada externa
    assert fibonacci_memo(12) == 144

    try:
        fibonacci_memo(-1)
        raise AssertionError("debía lanzar ValueError")
    except ValueError:
        pass

    print("\n✓ Todas las pruebas pasaron")
