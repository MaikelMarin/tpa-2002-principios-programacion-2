# Teoría: Estructuras de Datos Tipo Red (Grafos)

## Prerequisitos

| Apartado de `00-fundamentos` | Por qué se necesita aquí |
|-------------------------------|--------------------------|
| **2. Notación asintótica** | Todo el análisis de recorridos y algoritmos usa O, Θ |
| **3. Inducción matemática** | La corrección de Dijkstra y de la poda del MST se demuestran por inducción |
| **6. Invariantes de bucle** | BFS, DFS y Dijkstra tienen invariantes que garantizan su corrección |
| **7. Recurrencias** | Merge Sort no aplica aquí, pero el análisis por niveles sí |
| **8. Estructuras** | **Tabla hash** (lista de adyacencia), **cola** (BFS), **pila** (DFS), **heap** (Dijkstra) |
| **9. Modelo de memoria** | Por qué la lista de adyacencia gana a la matriz en grafos dispersos |
| **10. Python** | Diccionarios, `deque`, `heapq`, estructuras anidadas |

---

## 1. Conceptos fundamentales

### 1.1 Definición formal

Un **grafo** `G = (V, E)` consta de:
- **V:** conjunto finito no vacío de **vértices** (nodos).
- **E:** conjunto de **aristas**, pares de vértices.

Una arista `(u, v)` conecta los vértices `u` y `v`. Si el par es **ordenado**, el grafo es **dirigido** (dígrafo): la arista va de `u` hacia `v`. Si no, es **no dirigido**.

### 1.2 Contexto histórico

| Año | Hito | Detalle |
|-----|------|---------|
| 1736 | **Nace la teoría de grafos** | Leonhard Euler resuelve el problema de los puentes de Königsberg: ¿se puede cruzar la ciudad pasando una sola vez por cada uno de sus siete puentes? |
| 1852 | Problema de los 4 colores | Francis Guthrie pregunta si todo mapa se puede colorear con 4 colores |
| 1878 | Grafos en química | Arthur Cayley los aplica al conteo de isómeros |
| 1920s | Grafos en ingeniería | Modelado de circuitos eléctricos |
| 1950s | Adopción en computación | Grafos para redes y algoritmos |
| 1956 | MST (Kruskal) | Joseph Kruskal publica su algoritmo |
| 1930/1957 | MST (Prim) | Vojtěch Jarník (1930); Robert Prim lo redescubre (1957) |
| 1959 | **Dijkstra** | Edsger Dijkstra publica su algoritmo; le vale el Turing Award en 1972 |
| 1970s | Algoritmos clásicos | DFS, BFS y ordenamiento topológico se formalizan |
| Hoy | Aplicaciones masivas | Google Maps, redes sociales, motores de recomendación, logística |

El problema de Königsberg es el origen de todo: Euler demostró que era **imposible** modelando la ciudad como un grafo y observando que los cuatro nodos tenían grado impar.

### 1.3 Terminología esencial

| Término | Definición |
|---------|------------|
| **Vértice / Nodo** | Unidad fundamental |
| **Arista / Arco** | Conexión entre dos vértices |
| **Grado** | Número de aristas incidentes a un vértice |
| **Grado de entrada / salida** | En dígrafos: aristas que entran / salen |
| **Camino** | Secuencia de vértices conectados por aristas |
| **Ciclo** | Camino que empieza y termina en el mismo vértice |
| **Camino simple** | Camino sin vértices repetidos |
| **Conexo** | Existe camino entre cualquier par de vértices |
| **Fuertemente conexo** | En dígrafos: camino en ambas direcciones |
| **Componente conexo** | Subgrafo conexo maximal |
| **Grafo completo** | Todo par de vértices conectado (`n(n−1)/2` aristas) |
| **Bipartito** | Vértices en dos conjuntos; aristas solo entre conjuntos |
| **Acíclico (DAG)** | Sin ciclos |

**Teorema (saludo de manos).** En cualquier grafo, la suma de los grados de todos los vértices es igual al doble del número de aristas:

```
Σ grado(v) = 2|E|
```

Consecuencia: **el número de vértices de grado impar siempre es par**. Es el resultado que usó Euler para resolver Königsberg.

---

## 2. Tipos de grafos y aplicaciones

| Tipo | Descripción | Aplicación |
|------|-------------|------------|
| No dirigido | Aristas bidireccionales | Amistades, redes de carreteras |
| Dirigido (dígrafo) | Aristas con dirección | Seguidores, dependencias |
| Ponderado | Cada arista tiene un peso | Distancias, costos, ancho de banda |
| No ponderado | Todas las aristas equivalentes | Conectividad básica |
| Bipartito | Dos conjuntos independientes | Asignación estudiantes-cursos |
| Acíclico (DAG) | Sin ciclos | Dependencias de compilación |
| Árbol | Conexo y acíclico con `n−1` aristas | Estructura jerárquica |
| Completo | Todos los vértices conectados | Redes de comunicación |

---

## 3. Representación

### 3.1 Matriz de adyacencia

Matriz `V × V` donde `M[i][j]` indica si existe arista de `i` a `j` (1, o el peso).

```
Grafo:       Matriz:
  0 ─ 1     [0 1 1 0]
  │ ╲ │      [1 0 1 1]
  2 ─ 3      [1 1 0 0]
             [0 1 0 0]
```

**Características:**
- Espacio: **O(V²)** siempre, incluso si hay pocas aristas.
- Verificar si `(u, v)` existe: **O(1)**.
- Iterar vecinos de un vértice: **O(V)** (hay que recorrer la fila).
- Añadir vértice: requiere redimensionar la matriz.

### 3.2 Lista de adyacencia

Diccionario/array de listas: `adyacencia[u]` contiene los vecinos de `u`.

```
Grafo:      Lista:
  0 ─ 1     0: [1, 2]
  │ ╲ │     1: [0, 2, 3]
  2 ─ 3     2: [0, 1]
            3: [1]
```

**Características:**
- Espacio: **O(V + E)**.
- Verificar si `(u, v)` existe: **O(grado(u))**.
- Iterar vecinos de un vértice: **O(grado(u))**.
- Añadir arista: **O(1)**.

### 3.3 Comparativa y cuándo usar cada una

| Criterio | Matriz | Lista |
|----------|--------|-------|
| Espacio | O(V²) | O(V + E) |
| ¿Existe arista? | O(1) | O(grado) |
| Iterar vecinos | O(V) | O(grado) |
| Añadir arista | O(1) | O(1) |
| Añadir vértice | O(V²) | O(1) |
| Óptima para | Grafos **densos** | Grafos **dispersos** |

**El cálculo que decide.** Un grafo con 10,000 vértices y 20,000 aristas:
- Matriz: 100,000,000 entradas reservadas, de las cuales ~20,000 son útiles (0.02%).
- Lista: ~30,000 entradas.

**Regla práctica:** la mayoría de los grafos reales (redes sociales, carreteras, web) son **dispersos**, así que la lista de adyacencia es la representación estándar. La matriz solo gana cuando el grafo es denso o cuando se consulta muchísimo "¿existe esta arista?".

---

## 4. Recorridos

### 4.1 BFS (Breadth-First Search) — En anchura

**Principio.** Explorar todos los vértices a distancia `k` antes de pasar a distancia `k+1`. Usa una **cola** (FIFO).

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

**Complejidad.** O(V + E). Cada vértice se encola y desencola una vez; cada arista se examina una vez por extremo.

**Propiedad clave: camino más corto en grafos no ponderados.**

BFS visita los vértices en orden **no decreciente de distancia al origen**. Esto es exactamente lo que lo hace el algoritmo correcto para calcular distancias mínimas cuando todas las aristas pesan lo mismo.

**Demostración (bosquejo).** Por inducción sobre la distancia. Los vértices a distancia 0 (el origen) se visitan primero. Al procesar un vértice a distancia `d`, se descubren todos sus vecinos no visitados, que están a distancia `d+1` como máximo. Como la cola es FIFO, ningún vértice a distancia `d+2` se visita antes de que se hayan visitado todos los de `d+1`. Luego la secuencia de visitas está ordenada por distancia. ∎

**Aplicaciones:** camino más corto sin pesos, grados de separación, redes sociales, web crawling nivel por nivel, componentes conexos, grafos bipartitos (coloreo por BFS).

### 4.2 DFS (Depth-First Search) — En profundidad

**Principio.** Explorar tan lejos como sea posible por cada rama antes de retroceder. Usa una **pila** (LIFO) o recursión.

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

**Complejidad.** O(V + E), igual que BFS.

**Aplicaciones:**
- **Detección de ciclos.** En no dirigido: si se alcanza un vértice visitado que no es el padre inmediato, hay ciclo. En dígrafo: tres estados (BLANCO/GRIS/NEGRO); alcanzar un vértice GRIS implica ciclo (arista de retroceso).
- **Ordenamiento topológico** en DAG: el orden inverso de finalización de DFS.
- **Componentes fuertemente conexos** (Kosaraju).
- **Backtracking** (laberintos, coloreo).

### 4.3 BFS vs DFS

| Criterio | BFS | DFS |
|----------|-----|-----|
| Estructura | Cola (FIFO) | Pila (LIFO) / recursión |
| Camino más corto sin pesos | **Sí** | No |
| Detección de ciclos | No directamente | **Sí** |
| Ordenamiento topológico | No | **Sí** |
| Memoria | O(V) | O(V) (peor caso) |
| Exploración | Por niveles | Por ramas |
| Uso típico | Distancias, redes | Estructura, ciclos, dirigidos |

---

## 5. Algoritmos clásicos

### 5.1 Dijkstra — Camino más corto con pesos no negativos

**Problema.** Dado un grafo ponderado con pesos no negativos y un origen `s`, hallar la distancia mínima de `s` a todos los demás vértices.

**Historia.** Dijkstra lo diseñó en 1956 y lo publicó en 1959. Según su propia entrevista, lo diseñó sin lápiz ni papel, en unos 20 minutos, mientras su prometida hacía unas compras.

**Idea (codiciosa).** Mantener un conjunto de vértices con distancia conocida y definitiva. En cada paso, seleccionar el vértice **no procesado** con menor distancia tentativa, **fijarlo**, y **relajar** sus aristas.

```python
import heapq

def dijkstra(grafo, origen):
    dist = {v: float('inf') for v in grafo.vertices}
    dist[origen] = 0
    cola = [(0, origen)]

    while cola:
        d, u = heapq.heappop(cola)
        if d > dist[u]:
            continue                      # entrada obsoleta
        for v, peso in grafo.vecinos(u):
            if d + peso < dist[v]:        # relajar la arista
                dist[v] = d + peso
                heapq.heappush(cola, (dist[v], v))
    return dist
```

**Invariante.** Al extraer un vértice `u` del heap, `dist[u]` es la distancia mínima real desde el origen. Es decir: **ya es definitiva**.

**Demostración de corrección.**

*Caso base:* el origen se inserta con distancia 0, que es obviamente la mínima.

*Hipótesis:* supongamos que todos los vértices extraídos antes que `u` tienen su distancia definitiva correcta.

*Paso:* `u` se extrae con la menor distancia tentativa del heap. Supongamos que existiera un camino más corto a `u`, que pasara por algún vértice `w` aún no extraído. Ese camino usaría una arista `(x, u)` donde `x` ya fue extraído (o es `u` mismo). Pero cuando `x` se extrajo, se relajaron todas sus aristas, incluyendo `(x, u)`, así que `dist[u] ≤ dist[x] + peso(x,u)`, que es la longitud del camino por `x`. Contradicción con que existe uno más corto. Luego `dist[u]` es óptima. ∎

**Complejidad.**
- Con lista simple: **O(V²)**.
- Con heap binario: **O((V + E) log V)**.
- Con heap de Fibonacci: **O(E + V log V)** (óptimo teórico).

**Limitación fundamental.** Falla con pesos negativos, porque asume que al extraer un vértice su distancia ya es definitiva. Un peso negativo descubierto después invalidaría esa suposición. Para pesos negativos existe **Bellman-Ford**: O(V·E), que sí los admite y además detecta ciclos negativos.

**Aplicaciones reales.** Protocolos de enrutamiento (OSPF), GPS, planificación de rutas, redes de telecomunicaciones.

### 5.2 Kruskal — Árbol de expansión mínima (MST)

**Problema.** Dado un grafo conexo ponderado, hallar el subconjunto de aristas de peso total **mínimo** que conecta todos los vértices sin formar ciclos.

**Idea (codiciosa).** Ordenar las aristas por peso ascendente. Añadir cada arista si **no forma un ciclo** con las ya seleccionadas.

**Detectar ciclos:** estructura **Union-Find** (conjuntos disjuntos) con unión por rango y compresión de caminos. Su coste por operación es `O(α(n))`, donde α es la inversa de la función de Ackermann — crece tan lentamente que para cualquier `n` práctico `α(n) ≤ 5`. Es decir, efectivamente **O(1) amortizado**.

```python
def kruskal(vertices, aristas):
    aristas.sort(key=lambda a: a[2])          # O(E log E)
    uf = UnionFind(vertices)
    mst = []
    for u, v, peso in aristas:
        if uf.union(u, v):                   # ¿conectan componentes distintas?
            mst.append((u, v, peso))
    return mst
```

**Complejidad.** O(E log E), dominada por el ordenamiento.

**Demostración de corrección (propiedad de corte).** En todo corte del grafo, la arista de peso mínimo que lo cruce pertenece a algún MST. Como las aristas se procesan en orden ascendente y cada una se acepta solo si cruza un corte real (une dos componentes distintas), cada arista aceptada satisface la propiedad de corte y por tanto pertenece a un MST. El resultado tiene `V−1` aristas y es acíclico, luego es un MST. ∎

### 5.3 Prim — Árbol de expansión mínima

**Idea (codiciosa).** Partir de un vértice cualquiera. Mantener un árbol en crecimiento. En cada paso, añadir la arista de **menor peso** que conecte el árbol con un vértice fuera de él.

**Complejidad.**
- Con matriz de adyacencia: **O(V²)**.
- Con heap binario: **O((V + E) log V)**.

**Kruskal vs Prim:**

| Criterio | Kruskal | Prim |
|----------|---------|------|
| Enfoque | Sobre aristas | Sobre vértices |
| Estructura | Union-Find | Cola de prioridad |
| Mejor para | Grafos **dispersos** | Grafos **densos** |
| Complejidad | O(E log E) | O(E log V) |

### 5.4 Ordenamiento topológico

En un DAG, un orden topológico es una ordenación lineal de los vértices tal que para toda arista `(u, v)`, `u` aparece **antes** que `v`.

**Algoritmo:** ejecutar DFS y devolver los vértices en orden **inverso** de finalización.

**Aplicaciones:** orden de compilación, resolución de dependencias, scheduling de tareas.

---

## 6. Propiedades y algoritmos adicionales

**Grafo bipartito.** Un grafo es bipartito si y solo si se puede colorear con dos colores de forma que ninguna arista conecte vértices del mismo color. Equivalente a: **no contiene ciclos de longitud impar**. Se verifica con BFS coloreando niveles alternos.

**Componentes conexos.** Con BFS o DFS desde cada vértice no visitado; cada recorrido delimita una componente. O(V + E).

**Puentes y puntos de articulación.** Aristas/vértices cuya eliminación aumenta el número de componentes. Se detectan con DFS registrando tiempos de descubrimiento y valores `low`.

---

## 7. Resumen

| Si necesita... | Use... | Complejidad |
|----------------|--------|-------------|
| Recorrer todo el grafo | BFS o DFS | O(V + E) |
| Camino más corto sin pesos | BFS | O(V + E) |
| Camino más corto con pesos | Dijkstra | O((V+E) log V) |
| Pesos negativos | Bellman-Ford | O(V·E) |
| Conectar todo con mínimo coste | Kruskal o Prim | O(E log E) |
| Detectar ciclos | DFS | O(V + E) |
| Ordenar dependencias | Ordenamiento topológico | O(V + E) |
| Ver si es bipartito | BFS coloreado | O(V + E) |

**Los tres errores más frecuentes:**

1. **Usar Dijkstra con pesos negativos.** Devuelve resultados incorrectos en silencio, no un error.
2. **Elegir matriz de adyacencia para un grafo disperso.** Desperdicia O(V²) de memoria.
3. **Olvidar marcar los vértices como visitados al encolarlos** (y no al desencolarlos) en BFS: el mismo vértice puede entrar varias veces a la cola.

---

## Bibliografía anotada

1. **Cormen, T. H., Leiserson, C. E., Rivest, R. L. & Stein, C.** *Introduction to Algorithms*, III ed. MIT Press, 2009. — Capítulos 22 (elementos de grafos), 23 (MST), 24 (caminos más cortos).
2. **Sedgewick, R. & Wayne, K.** *Algorithms*, IV ed. Addison-Wesley, 2011. — Capítulo 4: Graphs. El tratamiento más visual.
3. **Goodrich, M. T., Tamassia, R. & Goldwasser, M. H.** *Data Structures & Algorithms in Python*. Wiley, 2013. — Capítulo 14.
4. **Weiss, M. A.** *Data Structures & Algorithm Analysis in C++*, III ed. Addison Wesley, 2006. — Capítulo 13.
5. **Dijkstra, E. W.** "A note on two problems in connexion with graphs", *Numerische Mathematik*, 1:269-271, 1959. — Artículo original.
6. **Euler, L.** "Solutio problematis ad geometriam situs pertinentis", *Comentarii academiae scientiarum Petropolitanae*, 8:128-140, 1736. — El artículo que origina toda la teoría de grafos.
7. **Tarjan, R. E.** "Efficiency of a good but not linear set union algorithm", *Journal of the ACM*, 22(2):215-225, 1975. — Análisis de Union-Find.

## Recursos utilizados

- MIT OpenCourseWare — 6.006: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/
- VisuAlgo — Grafos: https://visualgo.net/en/graphds
- GeeksforGeeks — Graph Algorithms: https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/
- Brilliant.org — Graph Theory: https://brilliant.org/wiki/graph-theory/
