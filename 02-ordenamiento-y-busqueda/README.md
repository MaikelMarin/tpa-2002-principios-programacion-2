# 02 — Ordenamiento y Búsqueda

## Mapa conceptual

```
              ORDENAMIENTO Y BÚSQUEDA
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   CUADRÁTICOS   DIVIDE Y VENCERÁS   LINEALES
   O(n²)         O(n log n)          O(n+k)
        │              │              │
   ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
   │         │    │         │    │         │
Burbuja  Selección Quick   Merge  Counting  Radix
   │         │    │         │      (enteros
Inserción        Híbrido  Enlazado  acotados)
                 │
            ┌────┴────┐
            │         │
        In-place   Funcional
        (Lomuto)   (3 vías)

              BÚSQUEDA
        ┌───────┴───────┐
        │               │
     Lineal         Binaria
     O(n)           O(log n)
     (desordenado) ─── arista ───→ Lista rotada
```

## Temas a tocar

| # | Tema | Qué se cubre |
|---|------|--------------|
| 1 | Introducción | Definiciones, historia, modelo de comparación, **demostración de la cota Ω(n log n)** |
| 2 | Propiedades | Estabilidad, in-place, adaptatividad, online — con ejemplos |
| 3 | Cuadráticos | Burbuja, Selección, Inserción con análisis exacto de comparaciones |
| 4 | Eficientes | Quick Sort (funcional e in-place), Merge Sort, Heap Sort |
| 5 | Híbridos | Quick + Inserción: por qué todas las bibliotecas estándar lo usan |
| 6 | Lineales | Counting, Radix, Bucket: romper la barrera explotando estructura |
| 7 | Búsqueda | Lineal, binaria (con invariante), coste de ordenar antes de buscar |

## Contenido categorizado

| Categoría | Descripción | Ejercicios |
|-----------|-------------|------------|
| **Ordenamiento básico** | Los tres O(n²): cuándo cada uno tiene sentido pese a su complejidad | 1, 2, 3 |
| **Divide y vencerás** | Partir el problema; la recursividad del tema 01 aplicada a ordenar | 4, 5, 8 |
| **Estructuras de datos** | Merge Sort sobre lista enlazada: dónde NO sirve Quick Sort | 9 |
| **Hibridación** | Combinar algoritmos por tamaño de partición | 11 |
| **Búsqueda** | Lineal vs binaria; la precondición que rompe todo | 6, 7 |
| **Búsqueda avanzada** | Listas rotadas: adaptar el invariante | 10 |

## Lista de ejercicios y ubicación de soluciones

| # | Ejercicio | Dificultad | Solución |
|---|-----------|------------|----------|
| 1 | Bubble Sort | Básico | [`ejercicios/burbuja.py`](ejercicios/burbuja.py) |
| 2 | Selection Sort | Básico | [`ejercicios/seleccion.py`](ejercicios/seleccion.py) |
| 3 | Insertion Sort | Básico | [`ejercicios/insercion.py`](ejercicios/insercion.py) |
| 4 | Quick Sort | Intermedio | [`ejercicios/quick_sort.py`](ejercicios/quick_sort.py) |
| 5 | Merge Sort | Intermedio | [`ejercicios/merge_sort.py`](ejercicios/merge_sort.py) |
| 6 | Búsqueda lineal | Básico | [`ejercicios/busqueda_lineal.py`](ejercicios/busqueda_lineal.py) |
| 7 | Búsqueda binaria | Intermedio | [`ejercicios/busqueda_binaria.py`](ejercicios/busqueda_binaria.py) |
| 8 | Quick Sort in-place | Avanzado | [`ejercicios/quick_sort_inplace.py`](ejercicios/quick_sort_inplace.py) |
| 9 | Merge Sort en lista enlazada | Experto | [`ejercicios/merge_sort_lista_enlazada.py`](ejercicios/merge_sort_lista_enlazada.py) |
| 10 | Búsqueda en lista rotada | Experto | [`ejercicios/binaria_rotada.py`](ejercicios/binaria_rotada.py) |
| 11 | Ordenamiento híbrido | Experto | [`ejercicios/ordenamiento_hibrido.py`](ejercicios/ordenamiento_hibrido.py) |

Cada archivo incluye teoría extendida, invariante del algoritmo, traza paso a paso, demostración de corrección, análisis de complejidad, verificación experimental y casos límite.

## Ruta de aprendizaje recomendada

1. **Ejercicios 1, 2, 3** — los tres cuadráticos. Compare sus casos: Burbuja e Inserción son `O(n)` en el mejor caso, Selección no.
2. **Ejercicio 6** — búsqueda lineal: la línea de base.
3. **Ejercicio 7** — búsqueda binaria: entienda el invariante antes de seguir.
4. **Ejercicio 5** — Merge Sort: el primer `n log n`, con su invariante de mezcla.
5. **Ejercicio 4** — Quick Sort funcional: compare la claridad con el coste.
6. **Ejercicio 8** — Quick Sort in-place: la versión real, con partición de Lomuto.
7. **Ejercicio 11** — híbrido: por qué las bibliotecas estándar no usan Quick Sort puro.
8. **Ejercicio 9** — Merge Sort sobre lista enlazada: dónde Quick Sort no puede llegar.
9. **Ejercicio 10** — lista rotada: cierre, modificando el invariante.

## Prerrequisitos

De `00-fundamentos`: notación asintótica (§2), logaritmos (§4), sumatorias (§5), invariantes de bucle (§6), recurrencias (§7), arreglos (§8), caché (§9).

## Teoría

Ver [`teoria.md`](teoria.md) — incluye la demostración completa de la cota inferior Ω(n log n) por árbol de decisión y el análisis exacto de comparaciones de cada algoritmo.
