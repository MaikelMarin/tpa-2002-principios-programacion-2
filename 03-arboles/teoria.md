# Teoría: Estructuras de Datos Jerárquicas (Árboles)

---

## 1. Conceptos fundamentales

### 1.1 Definición formal

Un **árbol** es un grafo conexo y acíclico. Equivalentemente, es una estructura T con:
- Un nodo distinguido llamado **raíz**.
- Subárboles disjuntos, cada uno de los cuales es a su vez un árbol.

Un **árbol binario** es un árbol donde cada nodo tiene como máximo dos hijos, llamados hijo izquierdo e hijo derecho, y donde se distingue el orden entre ellos.

### 1.2 Contexto histórico

| Año | Hito | Detalle |
|-----|------|---------|
| 1847 | Árboles en grafos | Gustav Kirchhoff usa árboles para analizar circuitos eléctricos |
| 1857 | Teoría de grafos | Arthur Cayley aplica árboles a la química (isómeros) |
| 1893 | Árboles binarios | Édouard Lucas formaliza la noción |
| 1950s | Adopción en computación | Estructura estándar para jerarquías |
| 1960 | BST | P. F. Windley describe el árbol binario de búsqueda |
| 1962 | Árbol AVL | Adelson-Velsky y Landi inventan el primer árbol balanceado |
| 1970 | Árbol B | Bayer y McCreight lo diseñan para bases de datos |
| 1972 | Árbol Rojo-Negro | Rudolf Bayer lo inventa; derivado del B-tree |
| 1984 | Árbol Rojo-Negro en C++ | Se convierte en base de `std::map` |
| Hoy | Ubicuidad | Índices de bases de datos, DOM, sistemas de archivos, IA |

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
| **Nodo** | Elemento del árbol con un valor y referencias a hijos |
| **Raíz** | Nodo único sin padre |
| **Hoja** | Nodo sin hijos |
| **Nodo interno** | Nodo con al menos un hijo |
| **Padre / Hijo** | Relación directa de arriba hacia abajo |
| **Hermanos** | Nodos que comparten padre |
| **Ancestro / Descendiente** | Relación transitiva de arriba/abajo |
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
| Número de aristas | n − 1 |
| Nodos en el nivel k | Como máximo 2^k |
| Nodos totales | Como máximo 2^(h+1) − 1 |
| Altura mínima | ⌊log₂(n)⌋ |
| Nodos hoja en árbol lleno | (n + 1) / 2 |

Estas propiedades explican por qué el balance importa: un árbol con n = 1,000,000 de nodos tiene altura 19 si es compacto, pero 1,000,000 si es degenerado. Esa diferencia es la que separa O(log n) de O(n).

---

## 2. Tipos de árboles binarios

| Tipo | Definición | Propiedad |
|------|------------|-----------|
| **Lleno (Full)** | Cada nodo tiene 0 o 2 hijos | Ningún nodo con un solo hijo |
| **Completo (Complete)** | Todos los niveles llenos; el último se llena de izquierda a derecha | Base del heap binario |
| **Perfecto** | Completo y todas las hojas al mismo nivel | Exactamente `2^(h+1) − 1` nodos |
| **Balanceado** | Para todo nodo: |h(izq) − h(der)| ≤ 1 | Altura O(log n) |
| **Degenerado** | Cada nodo interno tiene un solo hijo | Se comporta como lista enlazada |
| **BST** | Izq < raíz < der para todo nodo | Búsqueda O(h) |
| **Heap** | Padre ≥ hijos (máximo) o ≤ hijos (mínimo) | Estructura de cola de prioridad |

---

## 3. Recorridos

### 3.1 Recorridos en profundidad (DFS)

Los tres órdenes clásicos difieren solo en **cuándo** se visita la raíz:

**Preorden (Raíz → Izq → Der):**
```python
def preorden(nodo):
    if nodo:
        visitar(nodo)
        preorden(nodo.izquierdo)
        preorden(nodo.derecho)
```
Uso: clonar un árbol, serializar, generar expresiones en notación prefija.

**Inorden (Izq → Raíz → Der):**
```python
def inorden(nodo):
    if nodo:
        inorden(nodo.izquierdo)
        visitar(nodo)
        inorden(nodo.derecho)
```
Uso: recorrer un BST en orden ascendente. **Propiedad clave:** el inorden de un BST produce la secuencia ordenada.

**Postorden (Izq → Der → Raíz):**
```python
def postorden(nodo):
    if nodo:
        postorden(nodo.izquierdo)
        postorden(nodo.derecho)
        visitar(nodo)
```
Uso: liberar memoria (borrar hijos antes que el padre), expresiones postfijas, cálculos de tamaño de subárbol.

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

Complejidad: O(n). Espacio: O(w) donde w es el ancho máximo del árbol (hasta ⌈n/2⌉).

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

**Reconstrucción:** Con preorden + inorden se reconstruye el árbol de forma única. Lo mismo con postorden + inorden. Solo preorden + postorden no es suficiente.

---

## 4. Árbol de búsqueda binaria (BST)

### 4.1 Definición y propiedad invariante

Un BST es un árbol binario donde para **todo** nodo N:
- Todos los valores en el subárbol izquierdo de N son **menores** que el valor de N.
- Todos los valores en el subárbol derecho de N son **mayores** que el valor de N.
- Ambos subárboles son a su vez BST.

Esta invariante es lo que permite descartar la mitad del árbol en cada comparación.

### 4.2 Operaciones fundamentales

**Búsqueda:**
```python
def buscar(nodo, valor):
    if nodo is None or nodo.valor == valor:
        return nodo
    if valor < nodo.valor:
        return buscar(nodo.izquierdo, valor)
    return buscar(nodo.derecho, valor)
```
Complejidad: O(h). Si h = O(log n) → O(log n); si h = O(n) → O(n).

**Inserción:**
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
La inserción siempre ocurre en una hoja, así que no requiere reestructuración.

**Eliminación — tres casos:**

| Caso | Situación | Solución |
|------|-----------|----------|
| 1 | Nodo hoja | Eliminar directamente |
| 2 | Nodo con un hijo | Reemplazar por ese hijo |
| 3 | Nodo con dos hijos | Copiar el valor del sucesor inorden (mínimo del subárbol derecho) al nodo, y eliminar el sucesor |

Caso 3 en código:
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
            return nodo.derecho
        if nodo.derecho is None:
            return nodo.izquierdo
        sucesor = minimo(nodo.derecho)
        nodo.valor = sucesor.valor
        nodo.derecho = eliminar(nodo.derecho, sucesor.valor)
    return nodo
```

**¿Por qué el sucesor inorden?** Porque es el valor más cercano mayor al eliminado, el único que preserva la invariante BST al sustituirlo.

### 4.3 El problema del desbalance

Insertar datos ordenados (1, 2, 3, 4, 5…) produce un árbol degenerado: altura n, no log n. Todas las operaciones pasan a O(n), igual que una lista enlazada, pero con más overhead.

```
Inserción ordenada:        Inserción balanceada:
        1                       3
         \                     / \
          2                   1   4
           \                   \   \
            3                  2   5
             \
              4
               \
                5
```

### 4.4 Validación de BST

Un árbol es BST válido si el recorrido inorden produce una secuencia estrictamente creciente. Verificación eficiente con límites durante el recorrido:

```python
def es_bst_valido(nodo, minimo=float('-inf'), maximo=float('inf')):
    if nodo is None:
        return True
    if not (minimo < nodo.valor < maximo):
        return False
    return (es_bst_valido(nodo.izquierdo, minimo, nodo.valor) and
            es_bst_valido(nodo.derecho, nodo.valor, maximo))
```

Error común: verificar solo que el hijo izquierdo sea menor que el padre. Eso no basta: `[5, 1, 6, None, None, 3, 8]` tiene 3 < 6 pero 3 < 5, violando la invariante global.

---

## 5. Árboles balanceados

### 5.1 Árbol AVL

Inventado en 1962 por **Adelson-Velsky y Landi**. Es el árbol de búsqueda balanceado más antiguo.

**Invariante:** Para todo nodo, el factor de balance `BF = altura(izq) − altura(der)` está en {−1, 0, +1}.

Si una inserción o eliminación viola la invariante, se aplican **rotaciones** para restaurarla. Hay cuatro casos:

| Caso | Desbalance | Rotación |
|------|-----------|----------|
| LL | Izquierda-Izquierda | Rotación derecha simple |
| RR | Derecha-Derecha | Rotación izquierda simple |
| LR | Izquierda-Derecha | Rotación izquierda en hijo, luego derecha |
| RL | Derecha-Izquierda | Rotación derecha en hijo, luego izquierda |

```python
class ArbolAVL:
    def insertar(self, raiz, valor):
        if raiz is None:
            return Nodo(valor)
        if valor < raiz.valor:
            raiz.izquierdo = self.insertar(raiz.izquierdo, valor)
        elif valor > raiz.valor:
            raiz.derecho = self.insertar(raiz.derecho, valor)
        else:
            return raiz

        raiz.altura = 1 + max(altura(raiz.izquierdo), altura(raiz.derecho))
        balance = altura(raiz.izquierdo) - altura(raiz.derecho)

        # Caso LL
        if balance > 1 and valor < raiz.izquierdo.valor:
            return rotar_derecha(raiz)
        # Caso RR
        if balance < -1 and valor > raiz.derecho.valor:
            return rotar_izquierda(raiz)
        # Caso LR
        if balance > 1 and valor > raiz.izquierdo.valor:
            raiz.izquierdo = rotar_izquierda(raiz.izquierdo)
            return rotar_derecha(raiz)
        # Caso RL
        if balance < -1 and valor < raiz.derecho.valor:
            raiz.derecho = rotar_derecha(raiz.derecho)
            return rotar_izquierda(raiz)
        return raiz
```

**Garantía:** Con el AVL, la altura es siempre `h ≤ 1.44 log₂(n)`, luego búsqueda, inserción y eliminación son **siempre O(log n)**.

### 5.2 Árbol Rojo-Negro (referencia)

Invariantes:
1. Todo nodo es rojo o negro.
2. La raíz es negra.
3. Toda hoja nula (NIL) es negra.
4. Un nodo rojo no puede tener hijos rojos.
5. Todo camino de un nodo a sus hojas descendientes tiene el mismo número de nodos negros.

Garantía: `h ≤ 2 log₂(n+1)`, luego O(log n) en operaciones. Ventaja sobre AVL: menos rotaciones en inserción/eliminación (más rápido en escritura), a cambio de árboles ligeramente más altos. Es la base de `std::map` (C++), `TreeMap` (Java) y el scheduler del kernel de Linux.

### 5.3 Árbol B (referencia)

Generalización a m hijos por nodo (no solo 2). Diseñado para sistemas donde leer un bloque grande de disco es casi tan costoso como leer un byte: minimiza accesos a disco. Es la base de los índices en bases de datos relacionales, NTFS, HFS+, ext4.

---

## 6. Recorridos iterativos

La recursión consume pila. La versión iterativa usa una pila explícita:

**Inorden iterativo:**
```python
def inorden_iterativo(raiz):
    pila, resultado = [], []
    actual = raiz
    while actual or pila:
        while actual:
            pila.append(actual)
            actual = actual.izquierdo
        actual = pila.pop()
        resultado.append(actual.valor)
        actual = actual.derecho
    return resultado
```

**Postorden iterativo (con dos pilas):**
```python
def postorden_iterativo(raiz):
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

---

## 7. Operaciones avanzadas

**Ancestro común más bajo (LCA):** En un BST, el LCA de dos valores p y q es el primer nodo cuyo valor queda entre ambos:

```python
def lca_bst(raiz, p, q):
    while raiz:
        if p < raiz.valor and q < raiz.valor:
            raiz = raiz.izquierdo
        elif p > raiz.valor and q > raiz.valor:
            raiz = raiz.derecho
        else:
            return raiz.valor
```

**K-ésimo menor:** Con subárboles que almacenan su tamaño, se responde en O(h) descendiendo como en búsqueda binaria.

**Serialización:** Convertir un árbol a texto (p. ej. preorden con marcadores de nulo) y reconstruirlo. Útil para transmitir o persistir estructuras.

**BST a lista enlazada:** Recorrido inorden reconectando punteros; produce una lista ordenada in-place.

---

## 8. Aplicaciones

| Aplicación | Estructura |
|------------|-----------|
| Índices de bases de datos | Árbol B / B+ |
| Sistemas de archivos | Árboles de directorios |
| Compiladores | Árbol de sintaxis abstracta (AST) |
| Navegadores | Árbol DOM |
| Compresión | Árbol de Huffman |
| Expresiones | Árbol de expresiones |
| Búsqueda de texto | Trie / árbol de sufijos |
| IA | Árboles de decisión, minimax |

---

## Bibliografía

1. **Cormen, T. H., Leiserson, C. E., Rivest, R. L. & Stein, C.** *Introduction to Algorithms*, III ed. MIT Press, 2009. — Capítulos 12 (BST), 13 (Rojo-Negro), 18 (Árboles B).
2. **Goodrich, M. T., Tamassia, R. & Goldwasser, M. H.** *Data Structures & Algorithms in Python*. Wiley, 2013. — Capítulo 8: Trees.
3. **Weiss, M. A.** *Data Structures & Algorithm Analysis in C++*, III ed. Addison Wesley, 2006. — Capítulo 4.
4. **Knuth, D. E.** *The Art of Computer Programming*, Vol. 3: Sorting and Searching, II ed. Addison-Wesley, 1998. — Sección 6.2.2.
5. **Adelson-Velsky, G. & Landis, E.** "An algorithm for the organization of information", *Doklady Akademii Nauk SSSR*, 146:263-266, 1962. — Artículo original del AVL.

## Recursos utilizados

- MIT OpenCourseWare — 6.006: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/
- VisuAlgo — Árbol binario de búsqueda: https://visualgo.net/en/bst
- GeeksforGeeks — Binary Search Tree: https://www.geeksforgeeks.org/binary-search-tree-data-structure/
