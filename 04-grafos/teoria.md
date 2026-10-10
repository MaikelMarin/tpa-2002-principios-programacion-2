# Teoría: Estructuras de Datos Tipo Red (Grafos)

---

## 1. Conceptos fundamentales

### 1.1 Definición formal

Un **grafo** G = (V, E) consta de:
- **V:** conjunto finito no vacío de vértices (nodos).
- **E:** conjunto de aristas, pares de vértices.

Una **arista** (u, v) conecta los vértices u y v. Si el par es ordenado, el grafo es **dirigido** (dígrafo); si no, es **no dirigido**.

### 1.2 Contexto histórico

| Año | Hito | Detalle |
|-----|------|---------|
| 1736 | Nacimiento de la teoría de grafos | Leonhard Euler resuelve el problema de los puentes de Königsberg: ¿se puede cruzar la ciudad pasando una sola vez por cada puente? |
| 1852 | Problema de los 4 colores | Francis Guthrie pregunta si todo mapa se puede colorear con 4 colores; se demuestra en 1976 con ayuda de computadora |
| 1878 | "Silicate Societies" | Arthur Cayley aplica grafos a la química |
| 1891 | Teoría de grafos formal | Primer tratado sistemático |
| 1920s | Grafos en ingeniería | Modelado de circuitos eléctricos |
| 1950s | Adopción en computación | Grafos para redes y algoritmos |
| 1956 | MST (Kruskal) | Joseph Kruskal publica su algoritmo |
| 1959 | Dijkstra | Edsger Dijkstra publica el algoritmo de camino más corto; obra que le vale el Turing Award en 1972 |
| 1930/1957 | MST (Prim) | Vojtěch Jarník lo propone en 1930; Robert Prim lo redescubre en 1957 |
| 1970s | Algoritmos clásicos | DFS, BFS y ordenamiento topológico se formalizan |
| Hoy | Aplicaciones masivas | Google Maps, redes sociales, motores de recomendación, logística |

### 1.3 Terminología esencial

| Término | Definición |
|---------|------------|
| **Vértice / Nodo** | Unidad fundamental del grafo |
| **Arista / Arco** | Conexión entre dos vértices |
| **Grado** | Número de aristas incidentes a un vértice |
| **Grado de entrada / salida** | En dígrafos: aristas que entran / salen |
| **Camino** | Secuencia de vértices conectados por aristas |
| **Ciclo** | Camino que empieza y termina en el mismo vértice |
| **Camino simple** | Camino sin vértices repetidos |
| **Conexo** | Existe camino entre cualquier par de vértices |
| **Fuertemente conexo** | En dígrafos: camino en ambas direcciones entre cualquier par |
| **Componente conexo** | Subgrafo conexo maximal |
| **Grafo completo** | Todo par de vértices está conectado (n(n−1)/2 aristas) |
| **Grafo bipartito** | Los vértices se dividen en dos conjuntos; toda arista conecta conjuntos distintos |

**Teorema (saludo de manos):** En cualquier grafo, la suma de los grados de todos los vértices es igual al doble del número de aristas: `Σ grado(v) = 2|E|`. Consecuencia: el número de vértices de grado impar es siempre par.

---

## 2. Tipos de grafos y aplicaciones

| Tipo | Descripción | Aplicación |
|------|-------------|------------|
| No dirigido | Aristas bidireccionales | Amistades, redes de carreteras |
| Dirigido (dígrafo) | Aristas con dirección | Seguidores, dependencias |
| Ponderado | Cada arista tiene un peso | Distancias, costos, ancho de banda |
| No ponderado | Todas las aristas equivalentes | Conectividad básica |
| Bipartito | Dos conjuntos independientes | Asignación estudiantes-cursos, mercado de empleo |
| Acíclico (DAG) | Sin ciclos | Dependencias de compilación, tareas |
| Árbol | Conexo y acíclico con n−1 aristas | Estructura jerárquica |
| Completo | Todos los vértices conectados | Redes de comunicación |

---

## 3. Representación

### 3.1 Matriz de adyacencia

Matriz `V × V` donde `M[i][j]` indica si existe arista de i a j (1, o el peso).

```
Grafo:       Matriz:
  0 ─ 1     [0 1 1 0]
  │ ╲ │      [1 0 1 1]
  2 ─ 3      [1 1 0 0]
             [0 1 0 0]
```

**Características:**
- Espacio: O(V²) siempre, incluso si hay pocas aristas.
- Verificar si (u, v) existe: O(1).
- Iterar vecinos de un vértice: O(V) (hay que recorrer toda la fila).
- Añadir vértice: requiere redimensionar la matriz.

**Cuándo usarla:** Grafos densos, donde |E| se acerca a |V|²; cuando se consulta mucho "¿existe esta arista?".

### 3.2 Lista de adyacencia

Diccionario/array de listas: `adyacencia[u]` contiene los vecinos de u.

```
Grafo:      Lista:
  0 ─ 1     0: [1, 2]
  │ ╲ │     1: [0, 2, 3]
  2 ─ 3     2: [0, 1]
            3: [1]
```

**Características:**
- Espacio: O(V + E).
- Verificar si (u, v) existe: O(grado(u)).
- Iterar vecinos de un vértice: O(grado(u)).
- Añadir arista: O(1).

**Cuándo usarla:** Grafos dispersos (la mayoría de los grafos reales). Es la representación estándar en la práctica.

### 3.3 Comparativa

| Criterio | Matriz | Lista |
|----------|--------|-------|
| Espacio | O(V²) | O(V + E) |
| ¿Existe arista (u,v)? | O(1) | O(grado) |
| Vecinos de u | O(V) | O(grado) |
| Añadir arista | O(1) | O(1) |
| Añadir vértice | O(V²) | O(1) |
| Óptima para | Grafos densos | Grafos dispersos |

---

## 4. Recorridos

### 4.1 BFS (Breadth-First Search) — En anchura

**Principio:** Explorar todos los vértices a distancia k antes de pasar a distancia k+1. Usa una **cola** (FIFO).

```python
from collections import deque

def bfs(grafo, inicio):
    visitados = {inicio}
    cola = deque([inicio])
    resultado = []
    while cola:
        v = cola.popleft()
        resultado.append(v)
        for vecino, _ in grafo.vecinos(v):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)
    return resultado
```

**Propiedades clave:**
- Complejidad: O(V + E).
- **Camino más corto en grafos no ponderados:** BFS visita los vértices en orden no decreciente de distancia desde el origen. Es la única forma eficiente de calcular distancias mínimas sin pesos.
- Capas: la distancia se puede rastrear almacenando, junto a cada vértice, la distancia o el predecesor.

**Aplicaciones:** Camino más corto sin pesos, grados de separación, red de amistades, web crawling nivel por nivel, detección de componentes conexos, grafos bipartitos (coloreo con BFS).

### 4.2 DFS (Depth-First Search) — En profundidad

**Principio:** Explorar tan lejos como sea posible por cada rama antes de retroceder. Usa una pila (LIFO) o recursión.

```python
def dfs(grafo, v, visitados=None):
    if visitados is None:
        visitados = set()
    visitados.add(v)
    for vecino, _ in grafo.vecinos(v):
        if vecino not in visitados:
            dfs(grafo, vecino, visitados)
    return visitados
```

**Propiedades clave:**
- Complejidad: O(V + E).
- Descubre la estructura del grafo profundamente; ideal para detectar estructuras jerárquicas.

**Aplicaciones:**
- **Detección de ciclos:** En un grafo no dirigido, si se alcanza un vértice visitado que no es el padre inmediato, hay ciclo. En un dígrafo, se usan tres estados (BLANCO/GRIS/NEGRO): alcanzar un vértice GRIS implica ciclo (arista de retroceso).
- **Ordenamiento topológico:** En un DAG, el orden inverso de finalización de DFS da un orden topológico válido.
- **Componentes fuertemente conexos:** El algoritmo de Kosaraju usa dos pasadas de DFS.
- **Backtracking en grafos:** Laberintos, Sudoku, coloreo.

### 4.3 BFS vs DFS

| Criterio | BFS | DFS |
|----------|-----|-----|
| Estructura | Cola (FIFO) | Pila (LIFO) / recursión |
| Camino más corto (sin pesos) | Sí | No |
| Detección de ciclos | No directamente | Sí |
| Ordenamiento topológico | No | Sí |
| Memoria | O(V) (cola) | O(V) (pila) |
| Exploración | Por niveles | Por ramas |
| Uso típico | Distancias, redes | Estructura, ciclos, dirigidos |

---

## 5. Algoritmos clásicos

### 5.1 Dijkstra — Camino más corto con pesos no negativos

**Problema:** Dado un grafo ponderado con pesos no negativos y un origen s, hallar la distancia mínima de s a todos los demás vértices.

**Historia:** Edsger Dijkstra lo diseñó en 1956 y lo publicó en 1959, sin usar lápiz ni papel (según su propia entrevista), en 20 minutos. Recibió el Turing Award en 1972.

**Idea:** Mantener un conjunto de vértices con distancia conocida mínima. En cada paso, seleccionar el vértice no procesado con menor distancia tentativa, fijarlo, y relajar sus aristas.

```python
import heapq

def dijkstra(grafo, origen):
    dist = {v: float('inf') for v in grafo.vertices}
    dist[origen] = 0
    cola = [(0, origen)]
    while cola:
        d, u = heapq.heappop(cola)
        if d > dist[u]:
            continue  # Entrada obsoleta
        for v, peso in grafo.vecinos(u):
            if d + peso < dist[v]:
                dist[v] = d + peso
                heapq.heappush(cola, (dist[v], v))
    return dist
```

**Complejidad:**
- Con lista simple: O(V²).
- Con cola de prioridad (heap binario): O((V + E) log V).
- Con heap de Fibonacci: O(E + V log V) (óptimo teórico).

**Limitación fundamental:** Falla con pesos negativos, porque asume que al fijar un vértice su distancia ya es definitiva. Con pesos negativos existe Bellman-Ford: O(V×E), que sí los admite.

**Uso real:** Protocolos de enrutamiento (OSPF), GPS, redes de telecomunicaciones, planificación de rutas.

### 5.2 Kruskal — Árbol de expansión mínima (MST)

**Problema:** Dado un grafo conexo ponderado, hallar el subconjunto de aristas de peso total mínimo que conecta todos los vértices sin ciclos.

**Idea (codiciosa):** Ordenar las aristas por peso ascendente. Añadir cada arista si no forma un ciclo con las ya seleccionadas.

**Detectar ciclos:** se usa la estructura **Union-Find** (conjuntos disjuntos) con unión por rango y compresión de caminos, que da complejidad casi O(1) amortizada por operación.

```python
def kruskal(vertices, aristas):
    aristas.sort(key=lambda a: a[2])
    uf = UnionFind(vertices)
    mst = []
    for u, v, peso in aristas:
        if uf.union(u, v):
            mst.append((u, v, peso))
    return mst
```

**Complejidad:** O(E log E), dominada por el ordenamiento.

**Historia:** Joseph Kruskal lo publicó en 1956; el nombre proviene de su trabajo sobre árboles de expansión.

### 5.3 Prim — Árbol de expansión mínima (MST)

**Idea (codiciosa):** Partir de un vértice cualquiera. Mantener un árbol en crecimiento. En cada paso, añadir la arista de menor peso que conecte el árbol con un vértice fuera de él.

**Complejidad:**
- Con matriz de adyacencia: O(V²).
- Con heap binario: O((V + E) log V).

**Kruskal vs Prim:**

| Criterio | Kruskal | Prim |
|----------|---------|------|
| Enfoque | Sobre aristas | Sobre vértices |
| Estructura | Union-Find | Cola de prioridad |
| Mejor para | Grafos dispersos | Grafos densos |
| Complejidad | O(E log E) | O(E log V) |

### 5.4 Ordenamiento topológico (referencia)

En un DAG, un orden topológico es una ordenación lineal de los vértices tal que para toda arista (u, v), u aparece antes que v. Aplicaciones: orden de compilación, resolución de dependencias, scheduling de tareas.

---

## 6. Propiedades y algoritmos adicionales

**Grafo bipartito:** Un grafo es bipartito si y solo si se puede colorear con dos colores de forma que ninguna arista conecte vértices del mismo color. Equivalente a: **no contiene ciclos de longitud impar**. Se verifica con BFS coloreando niveles alternos.

**Componentes conexos:** Con BFS o DFS desde cada vértice no visitado; cada recorrido delimita una componente. Complejidad O(V + E).

**Puentes y puntos de articulación:** Aristas/vértices cuya eliminación aumenta el número de componentes conexos. Se detectan con DFS registrando tiempos de descubrimiento y valores "low".

---

## Bibliografía

1. **Cormen, T. H., Leiserson, C. E., Rivest, R. L. & Stein, C.** *Introduction to Algorithms*, III ed. MIT Press, 2009. — Capítulos 22 (Elementos de grafos), 23 (MST), 24 (Caminos más cortos).
2. **Sedgewick, R. & Wayne, K.** *Algorithms*, IV ed. Addison-Wesley, 2011. — Capítulo 4: Graphs.
3. **Goodrich, M. T., Tamassia, R. & Goldwasser, M. H.** *Data Structures & Algorithms in Python*. Wiley, 2013. — Capítulo 14.
4. **Weiss, M. A.** *Data Structures & Algorithm Analysis in C++*, III ed. Addison Wesley, 2006. — Capítulo 13.
5. **Dijkstra, E. W.** "A note on two problems in connexion with graphs", *Numerische Mathematik*, 1:269-271, 1959. — Artículo original.
6. **Euler, L.** "Solutio problematis ad geometriam situs pertinentis", *Comentarii academiae scientiarum Petropolitanae*, 8:128-140, 1736. — Artículo que origina la teoría de grafos.

## Recursos utilizados

- MIT OpenCourseWare — 6.006: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/
- VisuAlgo — Grafos: https://visualgo.net/en/graphds
- GeeksforGeeks — Graph Algorithms: https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/
