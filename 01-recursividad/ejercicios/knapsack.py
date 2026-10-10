"""
Ejercicio 12: Problema de la mochila (Knapsack) con Backtracking
Dificultad: Experto

Definición: Dado un conjunto de objetos con peso y valor, y una mochila
con capacidad máxima, seleccionar objetos que maximicen el valor total
sin exceder la capacidad.

Complejidad: O(2^n) — exponencial
"""

def knapsack_backtracking(pesos, valores, capacidad):
    """Resuelve el problema de la mochila usando backtracking."""
    n = len(pesos)
    mejor_valor = [0]
    mejor_seleccion = [[]]

    def backtrack(indice, peso_actual, valor_actual, seleccion):
        if indice == n:
            if valor_actual > mejor_valor[0]:
                mejor_valor[0] = valor_actual
                mejor_seleccion[0] = seleccion[:]
            return
        # No incluir el objeto actual
        backtrack(indice + 1, peso_actual, valor_actual, seleccion)
        # Incluir el objeto actual (si cabe)
        if peso_actual + pesos[indice] <= capacidad:
            seleccion.append(indice)
            backtrack(indice + 1, peso_actual + pesos[indice], valores[indice] + valor_actual, seleccion)
            seleccion.pop()

    backtrack(0, 0, 0, [])
    return mejor_valor[0], mejor_seleccion[0]


def knapsack_fuerza_bruta(pesos, valores, capacidad):
    """Versión de fuerza bruta para verificación."""
    from itertools import combinations
    n = len(pesos)
    mejor_valor = 0
    mejor_seleccion = []
    for r in range(n + 1):
        for combo in combinations(range(n), r):
            peso_total = sum(pesos[i] for i in combo)
            valor_total = sum(valores[i] for i in combo)
            if peso_total <= capacidad and valor_total > mejor_valor:
                mejor_valor = valor_total
                mejor_seleccion = list(combo)
    return mejor_valor, mejor_seleccion


if __name__ == "__main__":
    # Problema: capacidad 10, 5 objetos
    pesos = [2, 3, 4, 5, 9]
    valores = [3, 4, 5, 8, 10]
    capacidad = 10

    valor, seleccion = knapsack_backtracking(pesos, valores, capacidad)
    print(f"Capacidad: {capacidad}")
    print(f"Objetos (peso, valor): {list(zip(pesos, valores))}")
    print(f"\nMejor selección: {seleccion}")
    print(f"Valor total: {valor}")
    print(f"Peso total: {sum(pesos[i] for i in seleccion)}")

    # Verificar con fuerza bruta
    valor_fb, seleccion_fb = knapsack_fuerza_bruta(pesos, valores, capacidad)
    assert valor == valor_fb
    print(f"\nVerificación fuerza bruta: valor = {valor_fb}")
    print("\n✓ Todas las pruebas pasaron")
