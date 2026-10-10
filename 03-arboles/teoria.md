# Teoría: Estructuras de Datos Jerárquicas (Árboles)

## Prerequisitos

| Apartado de `00-fundamentos` | Por qué se necesita aquí |
|-------------------------------|--------------------------|
| **3. Inducción matemática** | La corrección de las operaciones sobre árboles se demuestra por **inducción estructural** (§3.6), no sobre enteros |
| **4. Logaritmos** | La altura de un árbol balanceado es `log n`; eso es lo que hace eficiente al BST |
| **7. Recurrencias** | Los recorridos y operaciones se analizan con recurrencias |
| **8. Estructuras (lista enlazada)** | Un árbol es una lista enlazada con dos referencias por nodo en vez de una |
| **9. Modelo de memoria** | Los nodos viven en el heap; entender referencias es imprescindible para no corromper el árbol |
| **10. Python (clases)** | Toda la implementación se apoya en clases con atributos que apuntan a otros nodos |

---

## 1. Conceptos fundamentales

### 1.1 Definición formal

Un **árbol** es un grafo conexo y acíclico. Equivalentemente, una estructura T definida por:

1. Un nodo distinguido llamado **raíz**.
2. Subárboles disjuntos, cada uno de los cuales es a su vez un árbol.

Un **árbol binario** es un árbol donde cada nodo tiene como máximo dos hijos, llamados **hijo izquierdo** e **hijo derecho**, y donde se distingue el orden entre ellos.

Observe que la definición es **recursiva**: un árbol contiene árboles. Por eso los algoritmos sobre árboles son recursivos por naturaleza (tema 01).

### 1.2 Contexto histórico

| Año | Hito | Detalle |
|-----|------|---------|
| 1847 | Árboles en matemáticas | Gustav Kirchhoff usa árboles para analizar circuitos eléctricos |
| 1857 | Teoría de grafos | Arthur Cayley aplica árboles a isómeros químicos |
| 1893 | Árboles binarios | Édouard Lucas formaliza la noción |
| 1950s | Adopción en computación | Estructura estándar para representar jerarquías |
| 1960 | BST | P. F. Windley describe el árbol binario de búsqueda |
| 1962 | Árbol AVL | **Adelson-Velsky y Landi** inventan el primer árbol de búsqueda **balanceado** |
| 1970 | Árbol B | Bayer y McCreight lo diseñan pensando en bases de datos |
| 1972 | Árbol Rojo-Negro | Rudolf Bayer lo inventa; derivado del B-tree |
| 1984 | Rojo-Negro en C++ | Se vuelve la base de `std::map` |
| Hoy | Ubicuidad | Índices de bases de datos (B-tree), DOM de navegadores, sistemas de archivos, compiladores, IA |

### 1.3 Terminología

```
                    A ← raíz
                   / \
                  B   C ← hermanos
                 /   / \
                D   E   F ← hojas
```

| Término | Definición |
|---------|------------|
| **Nodo** | Elemento con un valor y referencias a hijos |
| **Raíz** | Nodo único sin padre |
| **Hoja** | Nodo sin hijos |
| **Nodo interno** | Nodo con al menos un hijo |
| **Padre / Hijo** | Relación directa vertical |
| **Hermanos** | Nodos con el mismo padre |
| **Ancestro / Descendiente** | Relación transitiva vertical |
| **Subárbol** | Árbol formado por un nodo y todos sus descendientes |
| **Altura** | Número de aristas de la raíz a la hoja más lejana |
| **Profundidad** | Número de aristas de la raíz al nodo |
| **Nivel** | Profundidad + 1 |
| **Grado** | Número de hijos de un nodo |
| **Camino** | Secuencia de nodos conectados por aristas |

### 1.4 Relaciones métricas fundamentales

Para un árbol con **n** nodos y altura **h**:

| Propiedad | Valor |
|-----------|-------|
| Número de aristas | `n − 1` |
| Nodos en el nivel k | Como máximo `2^k` |
| Nodos totales | Como máximo `2^(h+1) − 1` |
| Altura mínima posible | `⌊log₂ n⌋` |
| Hojas en un árbol lleno | `(n + 1) / 2` |

**Estas fórmulas explican la importancia del balanceo.** Compare:

| n | Altura si degenerado | Altura si balanceado |
|---|---------------------|---------------------|
| 1,000 | 999 | 9 |
| 1,000,000 | 999,999 | 19 |

Buscar en el degenerado es O(n) — igual que una lista enlazada, pero con más overhead. Buscar en el balanceado es O(log n). Es la diferencia que justifica la existencia de AVL y Rojo-Negro.

---

## 2. Tipos de árboles binarios

| Tipo | Definición | Propiedad |
|------|------------|-----------|
| **Lleno (Full)** | Cada nodo tiene 0 o 2 hijos | Ningún nodo con un solo hijo |
| **Completo (Complete)** | Todos los niveles llenos; el último se llena de izquierda a derecha | Base del heap binario |
| **Perfecto** | Completo y todas las hojas al mismo nivel | Exactamente `2^(h+1) − 1` nodos |
| **Balanceado** | Para todo nodo, \|h(izq) − h(der)\| ≤ 1 | Altura O(log n) |
| **Degenerado** | Cada nodo interno tiene un solo hijo | Se comporta como lista enlazada |
| **BST** | izq < raíz < der para todo nodo | Búsqueda O(h) |

---

## 3. Recorridos

### 3.1 Los tres recorridos en profundidad (DFS)

Difieren solo en **cuándo** se visita la raíz:

| Recorrido | Orden | Uso |
|-----------|-------|-----|
| **Preorden** | Raíz → Izq → Der | Clonar un árbol, serializar, notación prefija |
| **Inorden** | Izq → Raíz → Der | Recorrer un BST en orden ascendente |
| **Postorden** | Izq → Der → Raíz | Liberar memoria, notación postfija |

```python
def preorden(nodo):
    if nodo:
        visitar(nodo)
        preorden(nodo.izquierdo)
        preorden(nodo.derecho)
```

**Análisis.** Los tres son `T(n) = 2T(n/2) + O(1)` → **Θ(n)** tiempo, y **Θ(h)** de pila (la profundidad máxima).

### 3.2 Recorrido en anchura (BFS)

Por niveles, usando una cola:

```python
from collections import deque

def por_niveles(raiz):
    if not raiz:
        return
    cola = deque([raiz])
    while cola:
        nodo = cola.popleft()
        visitar(nodo)
        if nodo.izquierdo:
            cola.append(nodo.izquierdo)
        if nodo.derecho:
            cola.append(nodo.derecho)
```

**Complejidad.** Θ(n) tiempo. Espacio **Θ(w)** donde w es el ancho máximo, que puede ser `⌈n/2⌉` — peor que el O(log n) de DFS en un árbol balanceado. Es un trade-off real, no un detalle.

### 3.3 Ejemplo de referencia

```
        1
       / \
      2   3
     / \   \
    4   5   6
```

| Recorrido | Resultado |
|-----------|-----------|
| Preorden | 1 2 4 5 3 6 |
| Inorden | 4 2 5 1 3 6 |
| Postorden | 4 5 2 6 3 1 |
| Por niveles | 1 2 3 4 5 6 |

### 3.4 Reconstrucción desde recorridos

**Teorema.** Un árbol binario queda determinado de forma única por su recorrido **preorden + inorden**, o por **postorden + inorden**.

**¿Por qué?** En el preorden, el primer elemento es la raíz. Ese elemento divide al inorden en subárbol izquierdo y derecho. Aplicando recursivamente se reconstruye todo.

**Importante:** preorden + postorden **NO** basta. No permiten distinguir si un nodo único es hijo izquierdo o derecho.

---

## 4. Árbol de búsqueda binaria (BST)

### 4.1 Definición e invariante

Un **BST** es un árbol binario donde para **todo** nodo N:
- Todos los valores del subárbol izquierdo de N son **menores** que el valor de N.
- Todos los valores del subárbol derecho de N son **mayores** que el valor de N.
- Ambos subárboles son a su vez BST.

Esta invariante es lo que permite **descartar la mitad del árbol en cada comparación**.

**Demostración: el inorden de un BST produce una secuencia ordenada.**

*Caso base:* árbol vacío; la secuencia vacía está trivialmente ordenada.

*Hipótesis:* para los subárboles I y D de la raíz r, sus inordenes producen secuencias ordenadas.

*Paso:* el inorden de T es `inorden(I) ⊕ r ⊕ inorden(D)`. Por la propiedad BST, todo valor en I es menor que r, y todo valor en D es mayor. Por hipótesis, ambas secuencias están ordenadas. Como todos los de la primera son menores que r y todos los de la segunda mayores, la concatenación completa está ordenada. ∎

**Consecuencia práctica:** para obtener los elementos ordenados de un BST basta con un recorrido inorden. No hace falta ordenar nada.

### 4.2 Operaciones fundamentales

**Búsqueda.**

```python
def buscar(nodo, valor):
    if nodo is None or nodo.valor == valor:
        return nodo
    if valor < nodo.valor:
        return buscar(nodo.izquierdo, valor)
    return buscar(nodo.derecho, valor)
```

Complejidad: **O(h)**. Si h = O(log n) → O(log n); si h = O(n) → O(n).

**Inserción.** Siempre ocurre en una hoja, así que no requiere reestructuración:

```python
def insertar(nodo, valor):
    if nodo is None:
        return Nodo(valor)
    if valor < nodo.valor:
        nodo.izquierdo = insertar(nodo.izquierdo, valor)
    elif valor > nodo.valor:
        nodo.derecho = insertar(nodo.derecho, valor)
    return nodo
```

**Eliminación — tres casos.**

| Caso | Situación | Solución |
|------|-----------|----------|
| 1 | Nodo hoja | Eliminar directamente |
| 2 | Nodo con un hijo | Reemplazar por ese hijo |
| 3 | Nodo con dos hijos | Copiar el valor del **sucesor inorden** (mínimo del subárbol derecho) al nodo, y eliminar ese sucesor |

```python
def eliminar(nodo, valor):
    if nodo is None:
        return None
    if valor < nodo.valor:
        nodo.izquierdo = eliminar(nodo.izquierdo, valor)
    elif valor > nodo.valor:
        nodo.derecho = eliminar(nodo.derecho, valor)
    else:
        if nodo.izquierdo is None:
            return nodo.derecho          # caso 1 o 2
        if nodo.derecho is None:
            return nodo.izquierdo        # caso 2
        sucesor = minimo(nodo.derecho)   # caso 3
        nodo.valor = sucesor.valor
        nodo.derecho = eliminar(nodo.derecho, sucesor.valor)
    return nodo
```

**¿Por qué el sucesor inorden y no el predecesor?** Ambos funcionan. El sucesor (mínimo del subárbol derecho) es el valor más cercano mayor al eliminado. Sustituirlo preserva la invariante porque: es mayor que todo el subárbol izquierdo (por definición del BST) y menor que todo el resto del subárbol derecho (por ser el mínimo de ese subárbol).

**Error común al demostrar el caso 3.** No basta con que el reemplazo sea "un valor cercano": hay que argumentar que sigue siendo mayor que todo el izquierdo y menor que todo el derecho. Con el sucesor inorden ese argumento es inmediato.

### 4.3 El problema del desbalance

Insertar datos ya ordenados produce un árbol degenerado:

```
Inserción 1,2,3,4,5:      Inserción equilibrada:
        1                       3
         \                     / \
          2                   1   4
           \                   \   \
            3                  2   5
             \
              4
               \
                5
    Altura: 4 (n-1)          Altura: 2 (log n)
```

Con altura n, todas las operaciones pasan a O(n): el BST degenera a una lista enlazada con peor constante.

### 4.4 Validación de BST

Un árbol es BST válido si y solo si su recorrido inorden produce una secuencia estrictamente creciente.

**El error clásico.** Verificar solo que el hijo izquierdo sea menor que el padre. No basta:

```
        5
       / \
      1   6
         / \
        3   7
```

Aquí `3 < 6` (parece OK) pero `3 < 5`, violando la invariante global. La verificación correcta propaga **límites**:

```python
def es_bst_valido(nodo, minimo=float('-inf'), maximo=float('inf')):
    if nodo is None:
        return True
    if not (minimo < nodo.valor < maximo):
        return False
    return (es_bst_valido(nodo.izquierdo, minimo, nodo.valor) and
            es_bst_valido(nodo.derecho, nodo.valor, maximo))
```

Cada nodo debe estar dentro del rango `(mínimo, máximo)` que hereda de sus ancestros, no solo respecto a su padre inmediato.

---

## 5. Árboles balanceados: AVL

Inventado en 1962 por **Adelson-Velsky y Landi**. Es el árbol de búsqueda balanceado más antiguo.

### 5.1 Invariante

Para todo nodo, el **factor de balance** debe estar en {−1, 0, +1}:

```
BF(nodo) = altura(subárbol izquierdo) − altura(subárbol derecho)
```

Si una inserción o eliminación viola la invariante, se aplican **rotaciones** para restaurarla.

### 5.2 Los cuatro casos de rotación

| Caso | Desbalance | Rotación necesaria |
|------|-----------|-------------------|
| **LL** | Izquierda-Izquierda | Rotación derecha simple |
| **RR** | Derecha-Derecha | Rotación izquierda simple |
| **LR** | Izquierda-Derecha | Izquierda en el hijo, luego derecha |
| **RL** | Derecha-Izquierda | Derecha en el hijo, luego izquierda |

**Rotación derecha simple (caso LL).** Sea y el nodo desbalanceado y x su hijo izquierdo:

```
    y                    x
   / \                  / \
  x   T3     →         T1  y
 / \      (rotar)         / \
T1  T2                   T2  T3
```

Tras la rotación, x sube a la posición de y. Los subárboles T1, T2 y T3 mantienen sus posiciones relativas. **La rotación preserva el orden del inorden**, que es la propiedad que garantiza que sigue siendo BST.

**Rotación doble LR.** El desbalance está "en zigzag": el hijo izquierdo tiene su propio hijo derecho como causante. Se aplica primero una rotación izquierda sobre el hijo, que convierte el caso LR en LL, y luego la rotación derecha.

### 5.3 Garantía del AVL

Con el invariante, la altura cumple `h ≤ 1.44 · log₂(n)`. Luego búsqueda, inserción y eliminación son **siempre O(log n)**.

**Coste de mantenimiento.** Cada inserción puede requerir hasta O(log n) rotaciones en el camino de vuelta, pero el coste amortizado por operación es O(1) rotaciones (como máximo se necesita una doble o dos simples por inserción).

### 5.4 Otras estructuras balanceadas (referencia)

| Estructura | Invariante | Ventaja |
|------------|-----------|---------|
| **Rojo-Negro** | Reglas de color + altura negra uniforme | Menos rotaciones que AVL al insertar |
| **B-tree** | Múltiples hijos por nodo | Minimiza accesos a disco; base de los índices de BD |
| **Splay tree** | El último accedido sube a la raíz | O(log n) amortizado; bueno con localidad de referencia |

El Rojo-Negro es la base de `std::map` (C++), `TreeMap` (Java) y el scheduler del kernel de Linux. Es ligeramente menos balanceado que AVL (altura ≤ 2·log₂n) pero requiere menos rotaciones, lo que lo hace más rápido en escritura.

---

## 6. Recorridos iterativos

La recursión consume pila. Para árboles muy altos, la versión iterativa con pila explícita es necesaria (tema 01, §1.5).

**Inorden iterativo.**

```python
def inorden_iterativo(raiz):
    pila, resultado = [], []
    actual = raiz
    while actual or pila:
        while actual:              # bajar por la izquierda apilando
            pila.append(actual)
            actual = actual.izquierdo
        actual = pila.pop()        # visitar
        resultado.append(actual.valor)
        actual = actual.derecho    # ir a la derecha
    return resultado
```

**Postorden iterativo** con dos pilas:

```python
def postorden_iterativo(raiz):
    if not raiz:
        return []
    pila1, pila2 = [raiz], []
    while pila1:
        nodo = pila1.pop()
        pila2.append(nodo)
        if nodo.izquierdo:
            pila1.append(nodo.izquierdo)
        if nodo.derecho:
            pila1.append(nodo.derecho)
    return [n.valor for n in reversed(pila2)]
```

Complejidad de ambos: Θ(n) tiempo, O(h) espacio.

---

## 7. Operaciones avanzadas

**Ancestro común más bajo (LCA).** En un BST, el LCA de dos valores p y q es el primer nodo cuyo valor queda entre ambos:

```python
def lca_bst(raiz, p, q):
    while raiz:
        if p < raiz.valor and q < raiz.valor:
            raiz = raiz.izquierdo
        elif p > raiz.valor and q > raiz.valor:
            raiz = raiz.derecho
        else:
            return raiz.valor       # aquí se separan los caminos
    return None
```

**K-ésimo elemento menor.** Si cada nodo almacena el tamaño de su subárbol, se responde en O(h) descendiendo como en una búsqueda binaria: si `tamaño_izq + 1 == k`, es el actual; si `tamaño_izq >= k`, bajar a la izquierda; si no, bajar a la derecha con `k − tamaño_izq − 1`.

**Serialización.** Convertir el árbol a texto (p. ej. preorden con marcadores de nulo) y reconstruirlo. Necesario para transmitir o persistir árboles. Con preorden + marcadores de nulo, la reconstrucción es única.

**BST a lista enlazada.** Recorrido inorden reconectando punteros: produce una lista ordenada in-place, sin asignar nodos nuevos.

---

## 8. Comparación con otras estructuras

| Estructura | Búsqueda | Inserción | Eliminación | Orden |
|------------|----------|-----------|-------------|-------|
| Arreglo desordenado | O(n) | O(1) | O(n) | No |
| Arreglo ordenado | O(log n) | O(n) | O(n) | Sí |
| Lista enlazada | O(n) | O(1) | O(1) | No |
| Tabla hash | O(1) prom. | O(1) prom. | O(1) prom. | **No** |
| BST balanceado | O(log n) | O(log n) | O(log n) | **Sí** |

**La conclusión clave.** Los árboles existen para llenar el hueco que el hash no cubre: operaciones logarítmicas **con los datos ordenados**. Si necesita recorrer en orden, buscar el mínimo/máximo, o hacer consultas por rango, un hash no sirve y un BST sí.

---

## 9. Resumen

| Concepto | Idea central |
|----------|--------------|
| Definición recursiva | La estructura es recursiva, luego el algoritmo también |
| Altura | La métrica que gobierna todo; `log n` si balanceado, `n` si degenerado |
| Invariante BST | izq < raíz < der; habilita descartar mitad |
| Eliminación caso 3 | Sucesor inorden preserva la invariante |
| Validación | Hay que propagar límites, no comparar solo con el padre |
| Balanceo | Rotaciones que preservan el inorden |

**Los tres errores más frecuentes:**

1. **Validar un BST comparando solo con el padre inmediato.** Falla con casos como el de la §4.4.
2. **Elegir mal el reemplazo al eliminar un nodo con dos hijos.** Debe ser el sucesor o predecesor inorden, no "cualquier valor cercano".
3. **Olvidar actualizar la altura tras una rotación AVL.** El árbol queda inconsistente y el balance se calcula mal en operaciones futuras.

---

## Bibliografía anotada

1. **Cormen, T. H., Leiserson, C. E., Rivest, R. L. & Stein, C.** *Introduction to Algorithms*, III ed. MIT Press, 2009. — Capítulos 12 (BST) y 13 (Rojo-Negro).
2. **Goodrich, M. T., Tamassia, R. & Goldwasser, M. H.** *Data Structures & Algorithms in Python*. Wiley, 2013. — Capítulo 8, el más cercano al nivel del curso.
3. **Weiss, M. A.** *Data Structures & Algorithm Analysis in C++*, III ed. Addison Wesley, 2006. — Capítulo 4, con el AVL más detallado.
4. **Knuth, D. E.** *The Art of Computer Programming*, Vol. 3. Addison-Wesley, 1998. — Sección 6.2.2, el origen del análisis de BST.
5. **Adelson-Velsky, G. & Landis, E.** "An algorithm for the organization of information", *Doklady Akademii Nauk SSSR*, 146:263-266, 1962. — Artículo original del AVL.
6. **Bayer, R. & McCreight, E.** "Organization and maintenance of large ordered indices", *Acta Informatica*, 1:173-189, 1972. — Artículo original del B-tree.

## Recursos utilizados

- MIT OpenCourseWare — 6.006: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/
- VisuAlgo — Árbol binario de búsqueda: https://visualgo.net/en/bst
- GeeksforGeeks — Binary Search Tree: https://www.geeksforgeeks.org/binary-search-tree-data-structure/
- CMU 15-121 (Introduction to Data Structures) — Trees: https://www.cs.cmu.edu/~112/
