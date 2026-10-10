"""
Ejercicio 10: Permutaciones recursivas
Dificultad: Avanzado

CONOCIMIENTO PREVIO NECESARIO
    - Backtracking (sección 4 del teoria.md): esta es la versión más
      simple, porque NO hay poda.
    - Factorial: el número de permutaciones de n elementos es n!.

PROBLEMA
    Generar todas las permutaciones de una lista de elementos.

    permutaciones([1, 2, 3]) tiene 3! = 6 resultados.

FONDO MATEMÁTICO
    Una permutación es una reordenación de todos los elementos. El
    número de permutaciones de n elementos distintos es n!, porque
    hay n opciones para la primera posición, n-1 para la segunda, etc.

    Definición recursiva:
        permutaciones([])      = [[]]        (la permutación vacía)
        permutaciones(x :: L)  = para cada permutación P de permutaciones(L),
                                insertar x en todas las posiciones de P

    Hay otra formulación equivalente, más usada en código:
        elegir cada elemento como primero, y permutar el resto.

ESTRATEGIA (backtracking sin poda)
    Mantener:
      - `actual`: la permutación en construcción.
      - `usados`: qué elementos ya se incluyeron (evita repetir).

    En cada paso:
      1. Si `actual` tiene n elementos, es una permutación completa
         → guardar una COPIA (no la referencia, que se va a mutar).
      2. En otro caso, probar cada elemento no usado:
           - marcarlo como usado (HACER)
           - añadirlo a `actual`
           - recursar (EXPLORAR)
           - quitarlo de `actual` y liberarlo (DESHACER)

    No hay poda: se quieren TODAS las soluciones. Por eso el costo es
    exactamente n! y no hay forma de mejorarlo.

TRAZA DE permutaciones_backtrack([1, 2])
    Paso   actual   usados     Acción
    1      []       [F,F]      probar x=1
    2      [1]      [T,F]      probar x=2
    3      [1,2]    [T,T]      ¡completa! guardar [1,2]
    4      [1]      [T,F]      DESHACER x=2
    5      []       [F,F]      DESHACER x=1
    6      []       [F,F]      probar x=2
    7      [2]      [F,T]      probar x=1
    8      [2,1]    [T,T]      ¡completa! guardar [2,1]
    9      [2]      [F,T]      DESHACER x=1
    10     []       [F,F]      DESHACER x=2

    Resultado: [[1,2], [2,1]]

ERROR CLÁSICO: GUARDAR LA REFERENCIA
    Si se hiciera `resultado.append(actual)` en vez de
    `resultado.append(actual[:])`, todas las entradas apuntarían a la
    MISMA lista, que al final queda vacía. El resultado serían n!
    copias de []. Este error aparece en todo backtracking.

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción sobre n. Para n = 1, se genera [[x]], correcto.
    Para n > 1, cada elemento se elige exactamente una vez como
    primero (bucle sobre no usados), y para cada elección se generan
    por hipótesis todas las permutaciones del resto. Luego se generan
    todas las permutaciones sin repetición. ∎

COMPLEJIDAD
    Número de soluciones: n!
    Tiempo: O(n × n!) — cada permutación cuesta O(n) construirla.
    Espacio: O(n × n!) para guardar todos los resultados
             + O(n) de pila de recursión.

    Tabla de crecimiento:
        n = 5   →      120 permutaciones
        n = 10  →  3,628,800
        n = 15  →  1.3 billones

    De ahí la regla: si el algoritmo es O(n!), solo sirve para n ≤ 10.

RELACIÓN CON OTROS TEMAS
    - N reinas (ejercicio 8): mismo patrón + poda de seguridad.
    - Knapsack (ejercicio 12): mismo patrama + poda de capacidad.
    - Ordenamiento por fuerza bruta: se podría "ordenar" generando
      todas las permutaciones y quedándose con la ordenada. Sería
      O(n! × n), absurdo frente a O(n log n). Sirve para ver por qué
      existen los algoritmos de ordenamiento (tema 02).
"""


def permutaciones(lista):
    """Genera todas las permutaciones por recursión pura.

    Formulación: elegir cada elemento como primero y permutar el resto.
    """
    if len(lista) <= 1:
        return [lista]

    resultado = []
    for i, elemento in enumerate(lista):
        resto = lista[:i] + lista[i + 1:]
        for perm in permutaciones(resto):
            resultado.append([elemento] + perm)
    return resultado


def permutaciones_backtrack(lista):
    """Genera todas las permutaciones por backtracking (sin poda).

    Es la versión que generaliza a problemas con restricciones.
    """
    resultado = []
    n = len(lista)

    def backtrack(actual, usados):
        if len(actual) == n:
            resultado.append(actual[:])   # ← COPIA, no la referencia
            return

        for i in range(n):
            if not usados[i]:
                usados[i] = True                  # HACER
                actual.append(lista[i])
                backtrack(actual, usados)         # EXPLORAR
                actual.pop()                      # DESHACER
                usados[i] = False

    backtrack([], [False] * n)
    return resultado


if __name__ == "__main__":
    lista = [1, 2, 3]

    print(f"Permutaciones de {lista}:")
    for perm in permutaciones(lista):
        print(f"  {perm}")

    print(f"\nTotal: {len(permutaciones(lista))} permutaciones")
    print(f"Esperado: 3! = 6")

    # Ambas versiones dan el mismo conjunto
    assert sorted(map(tuple, permutaciones(lista))) == \
           sorted(map(tuple, permutaciones_backtrack(lista)))

    # Conteo exacto para varios n
    for n in [1, 2, 3, 4, 5]:
        import math
        lista_n = list(range(n))
        assert len(permutaciones(lista_n)) == math.factorial(n), f"n={n}"

    # Casos base
    assert permutaciones([]) == [[]]
    assert permutaciones([7]) == [[7]]

    # Caso del enunciado
    perms = permutaciones([1, 2, 3])
    assert [1, 2, 3] in perms
    assert [3, 2, 1] in perms
    assert [2, 1, 3] in perms

    # Sin duplicados
    unicas = {tuple(p) for p in perms}
    assert len(unicas) == len(perms), "no debe haber permutaciones repetidas"

    print("\n✓ Todas las pruebas pasaron")
