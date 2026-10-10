# 04 — Grafos

## Mapa conceptual

```
                        GRAFOS
                          │
        ┌─────────────────┼──────────────────┐
        │                 │                  │
   REPRESENTACIÓN     RECORRIDOS        ALGORITMOS
        │                 │                  │
   ┌────┴────┐       ┌────┴────┐       ┌─────┴──────┐
   │         │       │         │       │            │
Matriz    Lista     BFS      DFS    Caminos      MST
(V²)     (V+E)     cola     pila   mínimos     mínimos
                           3 estados            │
                              │              ┌──┴──┐
                              │           Kruskal Prim
                           ciclos         Union-Find Heap
```

## Temas a tocar

| # | Tema | Qué se cubre |
|---|------|--------------|
| 1 | Conceptos | Definición formal, historia (Euler/Königsberg 1736), terminología, **Teorema del Saludo de Manos** |
| 2 | Tipos | Dirigidos, ponderados, bipartitos, acíclicos, árboles |
| 3 | Representación | Matriz vs lista de adyacencia, con el cálculo de espacio que decide |
| 4 | Recorridos | BFS (camino más corto sin pesos), DFS (ciclos, topológico) |
| 5 | Algoritmos | Dijkstra (con demostración de corrección), Kruskal, Prim, ordenamiento topológico |
| 6 | Propiedades | Bipartito, componentes conexos, puentes |

## Contenido categorizado

| Categoría | Descripción | Ejercicios |
|-----------|-------------|------------|
| **Representación** | Lista de adyacencia y matriz, cuándo usar cada una | 1, 2 |
| **Recorridos** | BFS y DFS, iterativos y recursivos | 3, 4, 5 |
| **Estructura** | Ciclos en no dirigidos y en dígrafos (reglas distintas) | 6, 13 |
| **Caminos** | Camino más corto sin pesos; Dijkstra con pesos | 7, 10 |
| **MST** | Conectar todo con mínimo coste: Kruskal y Prim | 15, 16 |
| **Propiedades** | Grafos bipartitos por coloreo BFS | 11 |
| **Procesamiento** | Logs, JSON a grafo, sistema de archivos como árbol | 12, 18, 17 |
| **Compresión** | Run-Length Encoding | 14 |

## Lista de ejercicios y ubicación de soluciones

| # | Ejercicio | Dificultad | Solución |
|---|-----------|------------|----------|
| 1 | Grafo con lista de adyacencia | Básico | [`ejercicios/grafo_adyacencia.py`](ejercicios/grafo_adyacencia.py) |
| 2 | Grafo con matriz de adyacencia | Básico | [`ejercicios/grafo_matriz.py`](ejercicios/grafo_matriz.py) |
| 3 | BFS iterativo | Básico | [`ejercicios/bfs_iterativo.py`](ejercicios/bfs_iterativo.py) |
| 4 | DFS iterativo | Básico | [`ejercicios/dfs_iterativo.py`](ejercicios/dfs_iterativo.py) |
| 5 | DFS recursivo | Intermedio | [`ejercicios/dfs_recursivo.py`](ejercicios/dfs_recursivo.py) |
| 6 | Ciclos en no dirigido | Intermedio | [`ejercicios/detectar_ciclos.py`](ejercicios/detectar_ciclos.py) |
| 7 | Camino más corto BFS | Intermedio | [`ejercicios/camino_minimo_bfs.py`](ejercicios/camino_minimo_bfs.py) |
| 8 | Copiar archivo binario | Básico | [`ejercicios/copiar_binario.py`](ejercicios/copiar_binario.py) |
| 9 | CSV a diccionarios | Básico | [`ejercicios/csv_a_diccionario.py`](ejercicios/csv_a_diccionario.py) |
| 10 | Dijkstra | Avanzado | [`ejercicios/dijkstra.py`](ejercicios/dijkstra.py) |
| 11 | Grafo bipartito | Avanzado | [`ejercicios/es_bipartito.py`](ejercicios/es_bipartito.py) |
| 12 | Sistema de logs | Intermedio | [`ejercicios/sistema_logs.py`](ejercicios/sistema_logs.py) |
| 13 | Ciclos en dirigido | Avanzado | [`ejercicios/grafo_dirigido_ciclos.py`](ejercicios/grafo_dirigido_ciclos.py) |
| 14 | Run-Length Encoding | Intermedio | [`ejercicios/run_length_encoding.py`](ejercicios/run_length_encoding.py) |
| 15 | Kruskal (MST) | Experto | [`ejercicios/kruskal.py`](ejercicios/kruskal.py) |
| 16 | Prim (MST) | Experto | [`ejercicios/prim.py`](ejercicios/prim.py) |
| 17 | Sistema de archivos simple | Experto | [`ejercicios/sistema_archivos_simple.py`](ejercicios/sistema_archivos_simple.py) |
| 18 | JSON a grafo | Intermedio | [`ejercicios/json_a_grafo.py`](ejercicios/json_a_grafo.py) |

Cada archivo incluye conocimiento previo, estrategia, invariante, traza paso a paso, demostración de corrección, análisis de complejidad y verificación experimental.

## Ruta de aprendizaje recomendada

1. **Ejercicios 1, 2** — las dos representaciones. Entienda el cálculo de espacio que decide cuál usar.
2. **Ejercicio 3** — BFS: el invariante que garantiza el camino más corto sin pesos.
3. **Ejercicio 4** — DFS con pila explícita; compare el orden de visita con BFS.
4. **Ejercicio 5** — DFS recursivo: la misma pila, pero la del intérprete.
5. **Ejercicio 6** — ciclos. La regla "vecino visitado que no es el padre".
6. **Ejercicio 13** — ciclos en dirigidos. **Por qué la regla anterior falla**: el caso A→B, C→B.
7. **Ejercicio 7** — camino más corto, reconstruyendo con predecesores.
8. **Ejercicio 10** — Dijkstra. El ejercicio más importante del tema.
9. **Ejercicio 11** — bipartito: el teorema de ciclos impares.
10. **Ejercicios 15, 16** — MST: dos enfoques codiciosos para el mismo problema.
11. **Ejercicios 8, 9, 12, 17, 18, 14** — aplicaciones prácticas.

## Prerrequisitos

De `00-fundamentos`: notación asintótica (§2), inducción (§3), invariantes (§6), tabla hash (§8.6), cola (§8.5), pila (§8.4), heap (§8.6), memoria (§9), Python (§10).

## Teoría

Ver [`teoria.md`](teoria.md) — incluye el Teorema del Saludo de Manos, la demostración de que BFS visita en orden de distancia, la demostración de corrección de Dijkstra, la propiedad de corte del MST y la cota de Union-Find.
