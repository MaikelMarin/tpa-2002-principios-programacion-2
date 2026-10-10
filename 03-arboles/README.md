# 03 — Árboles

## Mapa conceptual

```
                        ÁRBOLES
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   FUNDAMENTOS         RECORRIDOS        OPERACIONES
        │                  │                  │
   ┌────┴────┐        ┌────┴────┐        ┌────┴────┐
   │         │        │         │        │         │
Definición  Métricas  DFS (3)   BFS     BST      Balanceados
recursiva   altura    inorden  niveles  buscar/   AVL
            #nodos   pre/post         insertar/  (rotaciones)
                                     eliminar
```

## Temas a tocar

| # | Tema | Qué se cubre |
|---|------|--------------|
| 1 | Fundamentos | Definición formal, historia, terminología, relaciones métricas (`n ≤ 2^(h+1)−1`) |
| 2 | Tipos | Lleno, completo, perfecto, balanceado, degenerado, BST |
| 3 | Recorridos | Preorden, inorden, postorden, por niveles. Demostración de que el inorden de un BST es ascendente |
| 4 | BST | Invariante, búsqueda, inserción, eliminación en sus tres casos, el problema del desbalance, validación |
| 5 | Balanceo | AVL: invariante, cuatro casos de rotación, cota `h ≤ 1.44·log₂(n)` |
| 6 | Iterativos | Inorden y postorden sin recursión (evitan el límite de pila) |
| 7 | Avanzado | LCA, k-ésimo menor, serialización, BST a lista |

## Contenido categorizado

| Categoría | Descripción | Ejercicios |
|-----------|-------------|------------|
| **Estructura básica** | Nodos, referencias, construcción del árbol | 1 |
| **Recorridos** | Los cuatro órdenes y sus usos | 2, 10, 13 |
| **Métricas** | Contar nodos/hojas, altura y sus cotas | 3, 4 |
| **BST: operaciones** | Búsqueda, inserción, eliminación (3 casos) | 5, 6, 7 |
| **Validación** | Verificar la invariante propagando límites | 8 |
| **Consultas** | Mínimo/máximo, k-ésimo, LCA | 9, 14, 19 |
| **Recorridos iterativos** | Sin recursión: superan el límite de pila | 10, 13 |
| **Balanceo** | AVL con rotaciones y su cota teórica | 12, 16 |
| **Conversión** | BST a lista enlazada in-place | 17 |
| **Aplicaciones** | Árbol de expresiones, serialización | 18, 20 |

## Lista de ejercicios y ubicación de soluciones

| # | Ejercicio | Dificultad | Solución |
|---|-----------|------------|----------|
| 1 | Nodo y Árbol Binario | Básico | [`ejercicios/nodo_y_arbol.py`](ejercicios/nodo_y_arbol.py) |
| 2 | Recorridos de árbol | Básico | [`ejercicios/recorridos.py`](ejercicios/recorridos.py) |
| 3 | Contar nodos | Básico | [`ejercicios/contar_nodos.py`](ejercicios/contar_nodos.py) |
| 4 | Altura de un árbol | Básico | [`ejercicios/altura_arbol.py`](ejercicios/altura_arbol.py) |
| 5 | Búsqueda en BST | Intermedio | [`ejercicios/buscar_bst.py`](ejercicios/buscar_bst.py) |
| 6 | Inserción en BST | Intermedio | [`ejercicios/insertar_bst.py`](ejercicios/insertar_bst.py) |
| 7 | Eliminación en BST | Avanzado | [`ejercicios/eliminar_bst.py`](ejercicios/eliminar_bst.py) |
| 8 | Verificar BST válido | Intermedio | [`ejercicios/es_bst_valido.py`](ejercicios/es_bst_valido.py) |
| 9 | Mínimo y máximo | Básico | [`ejercicios/min_max_bst.py`](ejercicios/min_max_bst.py) |
| 10 | Inorden iterativo | Intermedio | [`ejercicios/inorden_iterativo.py`](ejercicios/inorden_iterativo.py) |
| 11 | Árboles idénticos | Intermedio | [`ejercicios/arboles_identicos.py`](ejercicios/arboles_identicos.py) |
| 12 | Árbol balanceado | Avanzado | [`ejercicios/es_balanceado.py`](ejercicios/es_balanceado.py) |
| 13 | Postorden iterativo | Avanzado | [`ejercicios/postorden_iterativo.py`](ejercicios/postorden_iterativo.py) |
| 14 | LCA en BST | Avanzado | [`ejercicios/lca_bst.py`](ejercicios/lca_bst.py) |
| 15 | Iterador para BST | Experto | [`ejercicios/iterador_bst.py`](ejercicios/iterador_bst.py) |
| 16 | Árbol AVL | Experto | [`ejercicios/arbol_avl.py`](ejercicios/arbol_avl.py) |
| 17 | BST a lista enlazada | Experto | [`ejercicios/bst_a_lista_enlazada.py`](ejercicios/bst_a_lista_enlazada.py) |
| 18 | Árbol de expresiones | Experto | [`ejercicios/arbol_expresiones.py`](ejercicios/arbol_expresiones.py) |
| 19 | K-ésimo elemento menor | Avanzado | [`ejercicios/k_esimo_menor.py`](ejercicios/k_esimo_menor.py) |
| 20 | Serializar y deserializar BST | Experto | [`ejercicios/serializar_bst.py`](ejercicios/serializar_bst.py) |

Cada archivo incluye conocimiento previo, estrategia, invariante, traza paso a paso, demostración de corrección, análisis de complejidad y verificación experimental.

## Ruta de aprendizaje recomendada

1. **Ejercicios 1, 2** — estructura y los cuatro recorridos. Son la base de todo.
2. **Ejercicios 3, 4** — métricas. Entienda que **contar** suma y **altura** toma el máximo: confundirlos es el error clásico.
3. **Ejercicio 5** — búsqueda en BST: el invariante que permite descartar la mitad.
4. **Ejercicio 8** — el contraejemplo que engaña a la verificación ingenua.
5. **Ejercicios 6, 7** — inserción y eliminación. El caso 3 (dos hijos) es el más difícil.
6. **Ejercicio 9** — por qué mínimo y máximo son O(h) y no O(n).
7. **Ejercicios 10, 13** — versiones iterativas: por qué existen (límite de recursión).
8. **Ejercicio 12** — la verificación eficiente en una sola pasada (11x medida).
9. **Ejercicio 14** — LCA: el punto de separación de caminos.
10. **Ejercicio 15** — el iterador y el O(1) amortizado.
11. **Ejercicios 16, 19** — AVL y k-ésimo: sacar provecho del balanceo.
12. **Ejercicios 17, 18, 20** — conversión, evaluación y serialización.

## Prerrequisitos

De `00-fundamentos`: inducción estructural (§3.6), logaritmos (§4), recurrencias (§7), lista enlazada (§8.3), pila (§8.4), referencias (§9.2), clases en Python (§10.1), límite de recursión (§10.2).

## Teoría

Ver [`teoria.md`](teoria.md) — 474 líneas con demostraciones de la propiedad inorden-ordenado, los tres casos de eliminación, las cuatro rotaciones AVL y la cota de altura.
