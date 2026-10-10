"""
Ejercicio 13: Fibonacci bottom-up
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Programación dinámica: tabulación (bottom-up) vs memoización
      (top-down).
    - Análisis de espacio: por qué O(1) es posible aquí.

PROBLEMA
    Calcular Fibonacci sin recursión y sin tabla auxiliar.

FONDO MATEMÁTICO
    La definición recursiva mira hacia atrás dos pasos. Eso significa
    que para calcular F(n) solo hacen falta los dos valores anteriores:
    no hay que conservar la serie completa.

    F(n) = F(n-1) + F(n-2)

    Si guardamos solo (F(n-1), F(n-2)), podemos avanzar:

        (0, 1) → (1, 1) → (1, 2) → (2, 3) → (3, 5) → ...

ESTRATEGIA
    1. Casos base: si n ≤ 1, devolver n.
    2. Inicializar dos variables: a = F(0) = 0, b = F(1) = 1.
    3. Iterar desde 2 hasta n, actualizando:
           a, b = b, a + b
       (asignación simultánea: se evalúan los dos lados antes de
       asignar, así que no se pierde el valor viejo de a).
    4. Devolver b.

TRAZA DE fibonacci_bottom_up(6)
    Iteración   a    b    nuevo b (= a+b)
    inicio      0    1    —
    k=2         1    1    (0+1)
    k=3         1    2    (1+1)
    k=4         2    3    (1+2)
    k=5         3    5    (2+3)
    k=6         5    8    (3+5)
    Resultado: b = 8

COMPLEJIDAD
    Tiempo: O(n) — n-1 iteraciones, cada una O(1).
    Espacio: O(1) — solo dos variables, sin importar n.

    Compare con la memoización: mismo tiempo, pero O(n) de espacio
    por el diccionario y O(n) de pila por la recursión.

POR QUÉ LA ASIGNACIÓN SIMULTÁNEA
    En Python, `a, b = b, a + b` evalúa primero el lado derecho
    completo con los valores antiguos, y después asigna. Es equivalente
    a:
        temporal = a + b
        a = b
        b = temporal
    Escribirlo como dos líneas separadas (`a = b` y luego `b = a + b`)
    daría un resultado incorrecto, porque `a` ya cambió.

COMPARACIÓN FINAL DE LAS TRES VERSIONES
    Versión          Tiempo    Espacio   Notas
    Ingenua          Θ(φ^n)    Θ(n)      Didáctica, inviable
    Memoización      Θ(n)      Θ(n)      Generaliza a problemas complejos
    Bottom-up        Θ(n)      Θ(1)      Mejor cuando solo hace falta un valor

    Regla práctica: si solo se necesita un valor final y la recurrencia
    tiene estado pequeño, bottom-up gana. Si hay que reportar muchos
    subresultados o la estructura es irregular, memoización.
"""


def fibonacci_bottom_up(n):
    """Fibonacci iterativo con espacio constante: O(n) tiempo, O(1) espacio."""
    if n < 0:
        raise ValueError("n debe ser no negativo")
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b        # asignación simultánea
    return b


def fibonacci_tabla(n):
    """Versión con tabla completa: O(n) tiempo, O(n) espacio.

    Se incluye para mostrar el coste de memoria cuando se conservan
    todos los subresultados en vez de solo los dos últimos.
    """
    if n < 0:
        raise ValueError("n debe ser no negativo")
    if n <= 1:
        return [0] if n == 0 else [0, 1][:n + 1]

    tabla = [0] * (n + 1)
    tabla[1] = 1
    for i in range(2, n + 1):
        tabla[i] = tabla[i - 1] + tabla[i - 2]
    return tabla


if __name__ == "__main__":
    print("Comparación de espacio:")

    n = 20
    print(f"  F({n}) con 2 variables  = {fibonacci_bottom_up(n)}")
    print(f"  F({n}) con tabla completa = {fibonacci_tabla(n)[-1]}")
    assert fibonacci_bottom_up(n) == fibonacci_tabla(n)[-1]

    print(f"\n  Tabla completa de F(0) a F({n}):")
    print(f"  {fibonacci_tabla(n)}")

    # Valores conocidos, incluido uno que desborda 64 bits
    assert fibonacci_bottom_up(0) == 0
    assert fibonacci_bottom_up(1) == 1
    assert fibonacci_bottom_up(2) == 1
    assert fibonacci_bottom_up(10) == 55
    assert fibonacci_bottom_up(50) == 12586269025

    # 21! desborda int64; F(92) es el último que cabe en uint64
    assert fibonacci_bottom_up(90) == 2880067194370816120
    assert fibonacci_bottom_up(93) == 12200160415121876738

    # Coincide con la versión memoizada
    def fib_ref(k):
        if k <= 1:
            return k
        return fib_ref(k - 1) + fib_ref(k - 2)

    for n in [0, 1, 5, 15]:
        assert fibonacci_bottom_up(n) == fib_ref(n)

    try:
        fibonacci_bottom_up(-1)
        raise AssertionError("debía lanzar ValueError")
    except ValueError:
        pass

    print("\n✓ Todas las pruebas pasaron")
