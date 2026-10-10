"""
Ejercicio 12: Problema de la mochila (Knapsack) con Backtracking
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - Backtracking con dos opciones por elemento (sección 4.5 del
      teoria.md).
    - Subproblemas superpuestos: el concepto que justifica la
      programación dinámica como mejora.
    - Python esencial: listas y estados mutables compartidos.

PROBLEMA
    Dados n objetos, cada uno con peso w_i y valor v_i, y una mochila
    de capacidad máxima W, seleccionar el subconjunto de objetos que
    MAXIMICE el valor total sin exceder la capacidad.

        pesos    = [2, 3, 4, 5, 9]
        valores  = [3, 4, 5, 8, 10]
        W        = 10
        óptimo   = valor 20, objetos {1, 2, 3} (pesos 3+4+5=12?) ...

    Cada objeto se toma o no se toma: NO se puede tomar una fracción.
    Es la variante 0/1 (la fraccionaria se resuelve con greedy).

FONDO MATEMÁTICO
    Es un problema de optimización combinatoria, NP-difícil en general.
    No se conoce algoritmo polinomial exacto para el caso general.

    Tiene las dos propiedades que habilitan la programación dinámica:
      1. Subestructura óptima: la mejor solución con los primeros i
         objetos y capacidad c se construye a partir de la mejor
         solución con los primeros i-1 objetos.
      2. Subproblemas superpuestos: el par (i, capacidad restante)
         se alcanza por muchos caminos distintos del árbol de decisión.

    La segunda propiedad es exactamente la que hace explotar al
    backtracking, igual que en Fibonacci.

ESTRATEGIA (backtracking)
    Árbol de decisión binario: en el nivel i decidimos el destino del
    objeto i. Dos ramas por objeto:
      - Rama A: NO tomar el objeto i.
      - Rama B: tomarlo, si cabe (peso_actual + w_i <= W).

    Al llegar a i == n, se comparó con el mejor valor encontrado.

    Estado del backtracking:
      - indice: qué objeto se está decidiendo
      - peso_actual y valor_actual: estado acumulado
      - seleccion: qué objetos se tomaron (para reconstruir la solución)

PODA APLICADA
    La rama B solo se explora si el objeto cabe. Es una poda básica.

    Poda más fuerte (no implementada aquí): si valor_actual + la suma
    de TODOS los valores restantes no supera al mejor encontrado,
    cortar la rama. Con esa poda el backtracking se acerca mucho antes
    a la solución óptima.

TRAZA del árbol de decisión (4 objetos simplificados)
    nivel 0: ¿tomar obj 0?
      ├── NO → nivel 1
      │    ├── NO → nivel 2 ...
      │    └── SÍ → nivel 2 ...
      └── SÍ (si cabe) → nivel 1
           ├── NO → nivel 2 ...
           └── SÍ → nivel 2 ...

    Con n objetos hay 2^n hojas. Cada hoja es un subconjunto posible.

DEMOSTRACIÓN DE CORRECCIÓN
    El algoritmo explora las 2^n combinaciones posibles (la poda solo
    descarta las que violan la capacidad, que no son soluciones
    válidas). Entre todas las válidas, guardar la de mayor valor da
    por definición el óptimo. ∎

COMPLEJIDAD
    Tiempo: O(2^n) sin poda. Cada uno de los 2^n subconjuntos se
    evalúa en O(1) amortizado (se acumula peso y valor al bajar).
    Espacio: O(n) de pila + O(n) por la selección.

    Con programación dinámica: O(n × W) tiempo y espacio. Mucho mejor
    cuando W no es enorme: para n=100, W=1000 serían 10^6 operaciones
    frente a 2^100.

COMPARACIÓN DE ENFOQUES
    Enfoque              Tiempo       Cuándo usarlo
    Backtracking         O(2^n)       n pequeño, o restricciones
                                     complejas donde la DP no aplica
    Programación dinámica O(n × W)    Cuando W es moderado. Es la
                                     solución estándar del problema.
    Greedy (fraccionario) O(n log n)  SOLO si se permiten fracciones.
                                     En la variante 0/1 da resultados
                                     subóptimos.

RELACIÓN CON FIBONACCI
    Es exactamente la misma lección: el problema no es la recursión,
    es RECALCULAR. El par (indice, capacidad restante) se repite en
    muchas ramas del árbol. Memoizar ese par convierte O(2^n) en
    O(n × W). Es la programación dinámica aplicada a estado de dos
    dimensiones.

APLICACIONES REALES
    - Selección de proyectos con presupuesto limitado.
    - Carga de contenedores o camiones.
    - Asignación de ancho de banda o memoria.
    - Corte de material minimizando desperdicio.
"""


def knapsack_backtracking(pesos, valores, capacidad):
    """Knapsack 0/1 por backtracking: O(2^n).

    Devuelve (mejor_valor, lista_de_índices_seleccionados).
    """
    n = len(pesos)
    mejor_valor = [0]
    mejor_seleccion = [[]]

    def backtrack(indice, peso_actual, valor_actual, seleccion):
        # Caso base: se decidió por todos los objetos
        if indice == n:
            if valor_actual > mejor_valor[0]:
                mejor_valor[0] = valor_actual
                mejor_seleccion[0] = seleccion[:]      # ← copia
            return

        # Rama A: NO tomar el objeto `indice`
        backtrack(indice + 1, peso_actual, valor_actual, seleccion)

        # Rama B: tomarlo, solo si cabe (poda por capacidad)
        if peso_actual + pesos[indice] <= capacidad:
            seleccion.append(indice)                   # HACER
            backtrack(indice + 1,
                      peso_actual + pesos[indice],
                      valor_actual + valores[indice],
                      seleccion)
            seleccion.pop()                            # DESHACER

    backtrack(0, 0, 0, [])
    return mejor_valor[0], mejor_seleccion[0]


def knapsack_fuerza_bruta(pesos, valores, capacidad):
    """Verificación por fuerza bruta: enumerar todos los subconjuntos.

    Más lenta, pero independiente del algoritmo anterior. Sirve para
    confirmar que el backtracking da el óptimo.
    """
    from itertools import combinations

    n = len(pesos)
    mejor_valor = 0
    mejor_seleccion = []

    for r in range(n + 1):
        for combo in combinations(range(n), r):
            peso = sum(pesos[i] for i in combo)
            valor = sum(valores[i] for i in combo)
            if peso <= capacidad and valor > mejor_valor:
                mejor_valor = valor
                mejor_seleccion = list(combo)

    return mejor_valor, mejor_seleccion


def knapsack_dp(pesos, valores, capacidad):
    """Knapsack 0/1 por programación dinámica: O(n × W).

    Se incluye para mostrar el salto de O(2^n) a polinomial mediante
    memoización de (objetos considerados, capacidad restante).
    """
    n = len(pesos)
    # dp[c] = mejor valor usando capacidad c
    dp = [0] * (capacidad + 1)

    for i in range(n):
        # Recorrer hacia atrás para no reutilizar el mismo objeto
        for c in range(capacidad, pesos[i] - 1, -1):
            dp[c] = max(dp[c], dp[c - pesos[i]] + valores[i])

    return dp[capacidad]


if __name__ == "__main__":
    import time

    # Instancia del problema
    pesos    = [2, 3, 4, 5, 9]
    valores  = [3, 4, 5, 8, 10]
    capacidad = 10

    print(f"Capacidad de la mochila: {capacidad}")
    print(f"Objetos (peso, valor):")
    for i, (p, v) in enumerate(zip(pesos, valores)):
        print(f"  obj {i}: peso={p}, valor={v}")

    # Resolver por backtracking
    valor, seleccion = knapsack_backtracking(pesos, valores, capacidad)

    print(f"\n--- Resultado por backtracking ---")
    print(f"Valor total: {valor}")
    print(f"Objetos seleccionados: {seleccion}")
    print(f"Peso total: {sum(pesos[i] for i in seleccion)}")
    assert sum(pesos[i] for i in seleccion) <= capacidad, "excede la capacidad"

    # Verificar contra fuerza bruta
    valor_fb, seleccion_fb = knapsack_fuerza_bruta(pesos, valores, capacidad)
    print(f"\n--- Verificación por fuerza bruta ---")
    print(f"Valor: {valor_fb}, objetos: {seleccion_fb}")
    assert valor == valor_fb, "el backtracking no encontró el óptimo"

    # Verificar contra programación dinámica
    valor_dp = knapsack_dp(pesos, valores, capacidad)
    print(f"--- Verificación por programación dinámica ---")
    print(f"Valor: {valor_dp}")
    assert valor == valor_dp, "discrepancia con la DP"

    # Comparación de tiempos con una instancia más grande
    print("\n--- Comparación de rendimiento (n=20) ---")
    import random
    random.seed(42)
    n = 20
    pesos_g   = [random.randint(1, 20) for _ in range(n)]
    valores_g = [random.randint(1, 50) for _ in range(n)]
    W = 60

    inicio = time.time()
    v_bt, _ = knapsack_backtracking(pesos_g, valores_g, W)
    t_bt = time.time() - inicio

    inicio = time.time()
    v_dp = knapsack_dp(pesos_g, valores_g, W)
    t_dp = time.time() - inicio

    print(f"  Backtracking: valor={v_bt}, tiempo={t_bt:.4f}s")
    print(f"  DP:           valor={v_dp}, tiempo={t_dp:.6f}s")
    print(f"  Aceleración:  {t_bt / t_dp:,.0f}x")
    assert v_bt == v_dp

    print("\n✓ Todas las pruebas pasaron")
