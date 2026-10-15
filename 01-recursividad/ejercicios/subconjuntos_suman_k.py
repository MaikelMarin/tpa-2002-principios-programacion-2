r"""
Ejercicio 15: Subconjuntos que sumen k
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Backtracking y la plantilla HACER/EXPLORAR/DESHACER (sección 4.2
      del teoria.md).
    - Permutaciones por backtracking (ejercicio 10): este es el mismo
      patrón con PODA.
    - Listas y estado mut compartido (00-fundamentos 9.2).

PROBLEMA
    Dada una lista de nmeros y un objetivo k, encontrar TODOS los
    subconjuntos cuyos elementos sumen exactamente k.

        numeros = [3, 34, 4, 12, 5, 2],  k = 9
        soluciones: [4, 5] y [3, 4, 2]

FONDO MATEMTICO
    El espacio de bsqueda es el conjunto de partes: 2^n subconjuntos.
    Cada elemento tiene exactamente dos opciones:

        INCLUIRLO    suma += numero, se aade a la seleccin
        NO INCLUIRLO la suma no cambia

    Eso da un rbol binario de 2^n hojas. La pregunta interesante es:
    cmo evitar recorrerlo entero?

    LA PODA (y por qu funciona aqu):
        Si suma_parcial + numero_actual > k, NO incluirlo.

    Pero ATENCIN: esa poda solo es vlida si todos los nmeros son
    POSITIVOS. Con negativos, aadir un elemento podra reducir la suma
    y volver a acercarse al objetivo, as que podar sera incorrecto.

    Es una restriccin que hay que documentar, no asumir.

ESTRATEGIA
    Backtracking con dos ramas por elemento:

```python
def backtrack(indice, suma, seleccion):
    if suma == k:
        registrar(seleccion)
        # NO retornar: puede haber otro elemento que sume 0
    if indice == n:
        return
    if suma + numeros[indice] <= k:      # PODA (solo con positivos)
        seleccion.append(indice)          # HACER
        backtrack(indice + 1, suma + numeros[indice], seleccion)
        seleccion.pop()                   # DESHACER
    backtrack(indice + 1, suma, seleccion)  # rama "no incluirlo"
```

    DETALLE SUTIL: al encontrar una solucin NO se retorna. Hay que
    seguir explorando por dos motivos:
      1. Puede existir otra solucin con el mismo prefijo.
      2. Si hay un 0 en la lista, incluirlo o no da dos soluciones
         distintas con la misma suma.

    Ese "no retornar" es la diferencia con problemas como las N
    reinan, donde una solucin completa s termina la rama.

TRAZA con numeros = [2, 3, 4], k = 5
    backtrack(0, 0, [])
      rama incluir 2: seleccion=[0], suma=2
        backtrack(1, 2, [0])
          rama incluir 3: suma=5 -> SOLUCION [2, 3] (no retorna)
            backtrack(2, 5, [0,1])   -> 5+4>5, podado; rama no incluir
          rama no incluir 3: backtrack(1, 2, [0]) con suma 2
            rama incluir 4: suma=6 > 5 -> PODADO
            rama no incluir 4: backtrack(3, 2, [0]) -> indice fin
      rama no incluir 2: suma=0
        backtrack(1, 0, [])
          rama incluir 3: suma=3
            rama incluir 4: suma=7 > 5 -> PODADO
          rama no incluir 3: suma=0
            rama incluir 4: suma=4 != 5, backtrack(3,...) fin
            rama no incluir 4: suma=0

    Solucin encontrada: [2, 3] (ndices 0 y 1).

    Note cunto se pod: de 8 subconjuntos posibles solo se exploraron
    unos pocos caminos.

DEMOSTRACIN DE CORRECCIN
    Por induccin sobre el nmero de elementos procesados.
    Caso base: indice == n. Ya no hay decisiones que tomar; si la
    suma es k, la seleccin actual es una solucin vlida.
    Paso: para el elemento en `indice`, se exploran las dos nicas
    opciones posibles (incluirlo o no). Si incluirlo supera k, se poda
    esa rama, lo cual es correcto SOLO si los nmeros son positivos
    (entonces cualquier suma futura con este elemento ya sera > k).

    Luego el algoritmo enumera exactamente los subconjuntos que suman
    k, sin repetir ni omitir ninguno. 

COMPLEJIDAD
    Tiempo: O(2^n) en el peor caso. Con poda, mucho menos en la
    prctica (depende de cunto se poda).
    Espacio: O(n) de pila + O(n) por la seleccin parcial.

    CON PROGRAMACIN DINMICA baja a O(n*k): el par (indice, suma
    restante) se repite en muchas ramas, igual que en Fibonacci y en
    el Knapsack (ejercicio 12). Es exactamente la misma leccin.

LA RESTRICCIN DE POSITIVOS
    Con nmeros negativos la poda es INVLIDA. Ejemplo:
        numeros = [5, -3, 7], k = 9
        suma 5, incluir -3 -> suma 2, incluir 7 -> 9. SOLUCION.

    Con la poda ingenua, al llegar a suma 5 + (-3) = 2 no se poda nada
    (2 <= 9), as que funcionara aqu. Pero considere:
        numeros = [10, -8, 7], k = 9
        10 + (-8) = 2, +7 = 9. Si la poda fuera "suma > k, cortar",
        al tener 10 > 9 se podara y se perdera la solucin.

    Por eso la poda correcta es: podar solo si suma + elemento > k
    **y** todos los elementos restantes son positivos.

APLICACIONES
    - Seleccin de proyectos con presupuesto (variante del Knapsack).
    - Encontrar combinaciones de monedas que sumen un monto.
    - Particin de conjuntos.

RELACIN CON OTROS TEMAS
    - Es el paso intermedio entre las permutaciones (ejercicio 10, sin
      poda) y el Knapsack (ejercicio 12, con poda + DP).
    - El coloreo de grafos (ejercicio 18) usa la misma plantilla.
"""


def subconjuntos_que_suman(numeros, objetivo):
    """Encuentra todos los subconjuntos que suman `objetivo`.

    Requiere nmeros POSITIVOS (la poda lo asume).
    Devuelve una lista de subconjuntos (listas de valores).
    """
    n = len(numeros)
    soluciones = []

    def backtrack(indice, suma_actual, seleccion):
        if suma_actual == objetivo:
            soluciones.append(seleccion[:])    # copia
            # NO retornar: puede haber ms soluciones con este prefijo

        if indice == n:
            return

        # PODA: solo incluir si no supera el objetivo (vlido con positivos)
        if suma_actual + numeros[indice] <= objetivo:
            seleccion.append(numeros[indice])              # HACER
            backtrack(indice + 1, suma_actual + numeros[indice], seleccion)
            seleccion.pop()                                # DESHACER

        # Rama "no incluir este elemento" (siempre vlida)
        backtrack(indice + 1, suma_actual, seleccion)

    backtrack(0, 0, [])
    return soluciones


def subconjuntos_que_suman_general(numeros, objetivo):
    """Versin SIN poda: funciona con negativos. O(2^n) siempre."""
    n = len(numeros)
    soluciones = []

    def backtrack(indice, suma_actual, seleccion):
        if indice == n:
            if suma_actual == objetivo:
                soluciones.append(seleccion[:])
            return
        seleccion.append(numeros[indice])
        backtrack(indice + 1, suma_actual + numeros[indice], seleccion)
        seleccion.pop()
        backtrack(indice + 1, suma_actual, seleccion)

    backtrack(0, 0, [])
    return soluciones


if __name__ == "__main__":
    # Caso del enunciado
    numeros = [3, 34, 4, 12, 5, 2]
    objetivo = 9
    soluciones = subconjuntos_que_suman(numeros, objetivo)
    print(f"Numeros: {numeros}, objetivo: {objetivo}")
    print(f"Soluciones: {soluciones}")

    # Verificar cada solucin
    for sub in soluciones:
        assert sum(sub) == objetivo, f"{sub} no suma {objetivo}"
        # Son subconjuntos vlidos (elementos de la lista original)
        for elem in sub:
            assert elem in numeros
    # Las dos soluciones esperadas
    esperadas = {tuple(sorted(s)) for s in soluciones}
    assert (4, 5) in esperadas, "falta [4, 5]"
    assert (2, 3, 4) in esperadas or (3, 4, 2) in esperadas or (2, 4, 3) in esperadas, \
        "falta [3, 4, 2]"

    # Sin solucin posible
    assert subconjuntos_que_suman([1, 2, 3], 100) == []
    print("Objetivo inalcanzable: lista vacia")

    # Casos base
    assert subconjuntos_que_suman([], 0) == [[]], "el conjunto vacio suma 0"
    assert subconjuntos_que_suman([5], 5) == [[5]], "un elemento exacto"
    assert subconjuntos_que_suman([5], 3) == [], "un elemento, no alcanza"
    assert subconjuntos_que_suman([1, 1], 2) == [[1, 1]], "duplicados"

    # Verificacin exhaustiva contra fuerza bruta
    from itertools import combinations

    def fuerza_bruta(numeros, objetivo):
        resultado = []
        for r in range(len(numeros) + 1):
            for combo in combinations(numeros, r):
                if sum(combo) == objetivo:
                    resultado.append(list(combo))
        return resultado

    import random
    random.seed(151)
    verificados = 0
    for _ in range(500):
        n = random.randint(0, 12)
        numeros_r = [random.randint(1, 20) for _ in range(n)]   # positivos
        objetivo_r = random.randint(0, 40)
        bt = {tuple(sorted(s)) for s in subconjuntos_que_suman(numeros_r, objetivo_r)}
        fb = {tuple(sorted(s)) for s in fuerza_bruta(numeros_r, objetivo_r)}
        assert bt == fb, f"discrepancia: {numeros_r}, k={objetivo_r}"
        verificados += 1
    print(f"\nVerificados {verificados} casos contra fuerza bruta")

    # EFECTO DE LA PODA: medir caminos explorados
    def contar_llamadas(numeros, objetivo):
        contador = [0]
        n = len(numeros)

        def bt(indice, suma):
            contador[0] += 1
            if suma == objetivo:
                pass                              # no retorna
            if indice == n:
                return
            if suma + numeros[indice] <= objetivo:
                bt(indice + 1, suma + numeros[indice])
            bt(indice + 1, suma)

        bt(0, 0)
        return contador[0]

    numeros_poda = [random.randint(1, 30) for _ in range(20)]
    objetivo_poda = 25
    llamadas_poda = contar_llamadas(numeros_poda, objetivo_poda)
    print(f"\nEfecto de la poda (20 numeros, objetivo {objetivo_poda}):")
    print(f"  Caminos explorados con poda: {llamadas_poda:,}")
    print(f"  Sin poda serian:            {2**21 - 1:,}")
    print(f"  Reduccion: {(2**21 - 1) / llamadas_poda:,.0f}x menos caminos")
    assert llamadas_poda < 2 ** 21 - 1

    # La versin general (sin poda) da el mismo resultado con positivos
    assert {tuple(sorted(s)) for s in subconjuntos_que_suman_general(numeros, objetivo)} \
        == esperadas
    print("La version general coincide con la podada (con positivos)")

    print("\n Todas las pruebas pasaron")
