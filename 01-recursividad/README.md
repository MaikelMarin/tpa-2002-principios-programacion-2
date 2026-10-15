# 01 — Recursividad

## Mapa conceptual

```
                    RECURSIVIDAD
                          │
        ┌─────────────────┼──────────────────┐
        │                 │                  │
   FUNDAMENTOS       FUNCIONES           ESTRUCTURAS
        │            RECURSIVAS          AVANZADAS
        │                 │                  │
   ┌────┴────┐       ┌────┴────┐        ┌────┴────┐
   │         │       │         │        │         │
Caso    Pila de   Clásicas  Análisis   Backtracking  Listas
base   llamadas   (fact,    de        (hacer/       y
       (marco)   fib,pot) recurrencias deshacer)    matrices
                                          │
                                     ┌─────┴─────┐
                                     │           │
                                  N reinas    Knapsack
                                  (poda)     (DP después)
```

## Temas a tocar

| # | Tema | Qué se cubre |
|---|------|--------------|
| 1 | Introducción | Definición formal, inducción como gemelo, historia, pila de llamadas, recursión de cola, coste |
| 2 | Funciones clásicas | Factorial, potencia (2 versiones), Fibonacci (3 versiones), Euclides, suma de dígitos, Ackermann |
| 3 | Estructuras de datos | Listas (cabeza+cola), listas anidadas, matrices, recursión mutua |
| 4 | Backtracking | Plantilla, poda, N reinas, Knapsack, permutaciones |
| 5 | Torres de Hanói | Solución, recurrencia, optimalidad |
| 6 | Análisis de recursiones | Las recurrencias del tema y sus soluciones |
| 7 | Programación dinámica | Memoización vs tabulación |

## Contenido categorizado

| Categoría | Descripción | Ejercicios |
|-----------|-------------|------------|
| **Fundamentos** | Caso base, reducción, pila de llamadas. Todo lo demás depende de esto | 1, 2, 3, 14 |
| **Recursión sobre listas** | Patrón cabeza + cola, con y sin copias | 4, 5, 6 |
| **Divide y vencerás** | Partir el problema a la mitad en vez de reducirlo en uno | 2 (potencia eficiente), 11 |
| **Backtracking** | Hacer / explorar / deshacer. Siete problemas: permutaciones, N reinas, Knapsack, subconjuntos, laberinto, Sudoku, coloreo | 8, 10, 12, 15, 16, 17, 18 |
| **Problemas clásicos** | Torres de Hanói, N reinas, Knapsack | 9, 8, 12 |
| **Programación dinámica** | Memoización y tabulación como evolución de la recursión | 7, 13, 12 |

## Lista de ejercicios y ubicación de soluciones

| # | Ejercicio | Dificultad | Solución |
|---|-----------|------------|----------|
| 1 | Factorial recursivo | Básico | [`ejercicios/factorial.py`](ejercicios/factorial.py) |
| 2 | Potencia (ingenua y eficiente) | Básico | [`ejercicios/potencia.py`](ejercicios/potencia.py) |
| 3 | Fibonacci recursivo | Básico | [`ejercicios/fibonacci.py`](ejercicios/fibonacci.py) |
| 4 | Suma recursiva de lista | Básico | [`ejercicios/suma_lista.py`](ejercicios/suma_lista.py) |
| 5 | Lista anidada recursiva | Intermedio | [`ejercicios/lista_anidada.py`](ejercicios/lista_anidada.py) |
| 6 | Recorrido recursivo de matriz | Intermedio | [`ejercicios/recorrido_matriz.py`](ejercicios/recorrido_matriz.py) |
| 7 | Fibonacci con memoización | Intermedio | [`ejercicios/fibonacci_memo.py`](ejercicios/fibonacci_memo.py) |
| 8 | N reinas (backtracking) | Avanzado | [`ejercicios/n_reinas.py`](ejercicios/n_reinas.py) |
| 9 | Torres de Hanói | Intermedio | [`ejercicios/torres_hanoi.py`](ejercicios/torres_hanoi.py) |
| 10 | Permutaciones recursivas | Avanzado | [`ejercicios/permutaciones.py`](ejercicios/permutaciones.py) |
| 11 | Búsqueda binaria recursiva | Intermedio | [`ejercicios/busqueda_binaria.py`](ejercicios/busqueda_binaria.py) |
| 12 | Mochila (knapsack) | Experto | [`ejercicios/knapsack.py`](ejercicios/knapsack.py) |
| 13 | Fibonacci bottom-up | Intermedio | [`ejercicios/fibonacci_bottom_up.py`](ejercicios/fibonacci_bottom_up.py) |
| 14 | Palíndromo recursivo | Básico | [`ejercicios/palindromo.py`](ejercicios/palindromo.py) |
| 15 | Subconjuntos que sumen k | Intermedio | [`ejercicios/subconjuntos_suman_k.py`](ejercicios/subconjuntos_suman_k.py) |
| 16 | Laberinto | Intermedio | [`ejercicios/laberinto.py`](ejercicios/laberinto.py) |
| 17 | Sudoku | Avanzado | [`ejercicios/sudoku.py`](ejercicios/sudoku.py) |
| 18 | Coloreo de grafos | Avanzado | [`ejercicios/coloreo_grafos.py`](ejercicios/coloreo_grafos.py) |

Cada archivo incluye teoría extendida, traza de ejecución, demostración de corrección, análisis de complejidad, casos límite y pruebas automáticas.

## Ruta de aprendizaje recomendada

1. **Ejercicios 1, 4, 14** — entender el caso base y el patrón cabeza + cola.
2. **Ejercicio 2** — ver cómo la reducción a la mitad cambia O(n) en O(log n).
3. **Ejercicio 3** — ver una recursión "correcta" pero inviable.
4. **Ejercicio 7 y 13** — las dos soluciones al problema anterior.
5. **Ejercicio 9** — el ejemplo canónico de divide y vencerás.
6. **Ejercicio 10** — backtracking sin poda (se quieren todas las soluciones).
7. **Ejercicio 8** — backtracking con poda: el primer problema donde podar es obligatorio.
8. **Ejercicio 15** — subconjuntos: la poda **condicional** (solo válida con positivos).
9. **Ejercicio 16** — laberinto: backtracking sobre una cuadrícula, no sobre un árbol.
10. **Ejercicio 17** — Sudoku: poda **fuerte**, donde sin ella el problema es inviable.
11. **Ejercicio 18** — coloreo de grafos: la generalización que conecta con el tema 04.
12. **Ejercicio 12** — Knapsack: cierra el tema, une backtracking con programación dinámica.

## Prerrequisitos

De `00-fundamentos`: inducción (§3), logaritmos (§4), sumatorias (§5), recurrencias (§7), memoria/stack (§9), Python (§10).

## Teoría

Ver [`teoria.md`](teoria.md) — 1,075 líneas con demostraciones completas y análisis de cada algoritmo.
