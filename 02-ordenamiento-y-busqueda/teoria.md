# Teoría: Métodos de Ordenamiento y Búsqueda

---

## 1. Introducción

### 1.1 Definición del problema

**Ordenamiento:** Dada una secuencia de n elementos de un conjunto totalmente ordenado, producir una permutación de la secuencia tal que cada elemento sea menor o igual que su sucesor.

**Búsqueda:** Dada una secuencia y un valor objetivo, determinar si el objetivo existe en la secuencia y, en su caso, en qué posición.

### 1.2 Contexto histórico

| Año | Hito | Detalle |
|-----|------|---------|
| 1945 | Merge Sort | John von Neumann describe el algoritmo en un memorando durante el proyecto Manhattan |
| 1946 | Búsqueda binaria | John Mauchly la describe en una conferencia; primer uso en computación |
| 1956 | Bubble Sort | Edward Harry Friend la publica como algoritmo de enseñanza |
| 1960 | Quick Sort | Tony Hoare la inventa en la Universidad de Moscú mientras traducía del ruso |
| 1962 | Quick Sort publicado | Se publica formalmente en *Computer Journal* |
| 1964 | Heap Sort | J. W. J. Williams publica el algoritmo; luego refinado por Floyd |
| 1970s | Límite inferior | Se demuestra que todo ordenamiento por comparación requiere Ω(n log n) comparaciones |
| 1990s | Algoritmos híbridos | TimSort (Python), Introsort (C++), Dual-Pivot Quicksort (Java) |
| Hoy | Estado del arte | std::sort (Introsort), TimSort, PDQSort; ordenamientos lineales (Counting, Radix) |

### 1.3 Notación asintótica

| Notación | Significado |
|----------|-------------|
| O(g(n)) | Cota superior: T(n) crece a lo sumo como g(n) |
| Ω(g(n)) | Cota inferior: T(n) crece al menos como g(n) |
| Θ(g(n)) | Cota ajustada: T(n) crece exactamente como g(n)) |
| o(g(n)) | Estrictamente menor |

### 1.4 Modelo de comparación

En el modelo de comparación, el algoritmo solo obtiene información del orden comparando pares de elementos. El resultado fundamental:

> **Teorema (cota inferior de ordenamiento):** Todo algoritmo de ordenamiento basado en comparaciones requiere Ω(n log n) comparaciones en el peor caso.

**Demostración (bosquejo):** Cualquier algoritmo de ordenamiento por comparaciones puede modelarse como un árbol de decisión binario. Con n elementos hay n! permutaciones posibles; el árbol debe tener al menos n! hojas. Un árbol binario de altura h tiene como máximo `2^h` hojas, así que `2^h ≥ n!`. Por la aproximación de Stirling, `log(n!) = Θ(n log n)`, luego `h = Ω(n log n)`.

Consecuencia: Merge Sort y Heap Sort son **óptimos** en el modelo de comparación. Quick Sort lo es en promedio. Ningún ordenamiento con comparaciones puede hacerlo asintóticamente mejor.

### 1.5 Propiedades deseables

| Propiedad | Significado | ¿Importa? |
|-----------|-------------|-----------|
| **Estabilidad** | Elementos iguales conservan su orden relativo | Sí al ordenar por múltiples claves |
| **In-place** | Usa memoria extra O(1) | Sí en sistemas embebidos |
| **Adaptativo** | Más rápido con datos parcialmente ordenados | Sí en datos casi ordenados |
| **Online** | Puede ordenar mientras recibe datos | Sí en streaming |
| **Paralelizable** | Se puede dividir en subproblemas | Sí en big data |

---

## 2. Ordenamientos de comparación

### 2.1 Burbuja (Bubble Sort)

**Principio:** Recorrer la lista repetidamente comparando elementos adyacentes; intercambiar si están en orden incorrecto. Optimización: si una pasada no hace intercambios, la lista está ordenada.

```python
def burbuja(arr):
    n = len(arr)
    for i in range(n):
        intercambio = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                intercambio = True
        if not intercambio:
            break
    return arr
```

**Análisis:**
- Mejor caso: O(n) — lista ya ordenada (una sola pasada).
- Promedio: O(n²).
- Peor caso: O(n²) — lista en orden inverso.
- Inversiones: realiza exactamente una operación de intercambio por cada inversión en la lista.

**Propiedades:** Estable, in-place, adaptativo.

**Uso real:** Docencia. Nunca en producción. Su valor es pedagógico: es el algoritmo más simple de analizar.

### 2.2 Selección (Selection Sort)

**Principio:** Encontrar el mínimo de la región no ordenada e intercambiarlo con el primer elemento no ordenado. Repetir.

```python
def seleccion(arr):
    n = len(arr)
    for i in range(n):
        minimo = i
        for j in range(i + 1, n):
            if arr[j] < arr[minimo]:
                minimo = j
        arr[i], arr[minimo] = arr[minimo], arr[i]
    return arr
```

**Análisis:**
- Siempre O(n²): exactamente `n(n-1)/2` comparaciones, independientemente del orden.
- Intercambios: exactamente n-1 (el mínimo posible de intercambios).

**Propiedades:** No estable, in-place, **no adaptativo**.

**Uso real:** Cuando el costo de escritura/intercambio es muy superior al de lectura (memorias flash, EEPROM), porque realiza el mínimo número de escrituras posible.

### 2.3 Inserción (Insertion Sort)

**Principio:** Construir la lista ordenada de izquierda a derecha. Para cada nuevo elemento, desplazar los mayores hacia la derecha e insertarlo en su posición.

```python
def insercion(arr):
    for i in range(1, len(arr)):
        clave = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > clave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = clave
    return arr
```

**Análisis:**
- Mejor caso: O(n) — lista ordenada (solo n-1 comparaciones).
- Promedio: O(n²) — `n²/4` inversiones.
- Peor caso: O(n²) — orden inverso.

**Propiedades:** Estable, in-place, adaptativo, online.

**Uso real:** El mejor algoritmo para listas pequeñas (n < ~20). TimSort e Introsort cambian a Inserción cuando las particiones bajan de cierto umbral. También se usa en sistemas casi ordenados (p. ej. corrección de datos levemente desordenados).

### 2.4 Quick Sort

**Principio (divide y vencerás):**
1. Elegir un pivote.
2. **Particionar:** reorganizar la lista de modo que los elementos menores que el pivote queden a la izquierda y los mayores a la derecha.
3. Ordenar recursivamente cada partición.

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivote = arr[len(arr) // 2]
    izquierda = [x for x in arr if x < pivote]
    medio = [x for x in arr if x == pivote]
    derecha = [x for x in arr if x > pivote]
    return quick_sort(izquierda) + medio + quick_sort(derecha)
```

**Análisis de complejidad:**
- Si el pivote divide equilibradamente: `T(n) = 2T(n/2) + O(n) = Θ(n log n)`.
- Si el pivote es siempre el mínimo o máximo: `T(n) = T(n-1) + O(n) = Θ(n²)`.
- Promedio sobre todas las permutaciones: Θ(n log n).

**Optimizaciones prácticas:**
- **Pivote aleatorio:** Evita el peor caso en datos patológicos.
- **Mediana de tres:** Probar el primero, el del medio y el último; usar la mediana como pivote.
- **Partición de tres vías (3-way):** Agrupar elementos iguales al pivote. Clave cuando hay muchos duplicados.
- **Umbral de inserción:** Cambiar a Insertion Sort cuando la partición es pequeña.

**Propiedades:** No estable, in-place (en su forma con partición de Hoare/Lomuto).

**Uso real:** El algoritmo de ordenamiento de propósito general más usado históricamente. Base de Introsort (C++ STL) y Dual-Pivot Quicksort (Java para primitivos).

### 2.5 Merge Sort

**Principio (divide y vencerás):**
1. Dividir la lista en dos mitades.
2. Ordenar recursivamente cada mitad.
3. Mezclar (merge) las dos mitades ordenadas en una sola.

```python
def merge(izq, der):
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            resultado.append(izq[i]); i += 1
        else:
            resultado.append(der[j]); j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    m = len(arr) // 2
    return merge(merge_sort(arr[:m]), merge_sort(arr[m:]))
```

**Análisis:**
- Recurrencia: `T(n) = 2T(n/2) + Θ(n)`.
- Por Teorema Maestro: `Θ(n log n)` **siempre**, sin excepciones. Predecible.
- Espacio: O(n) auxiliar para la mezcla.

**Propiedades:** Estable, no in-place, no adaptativo pero predecible.

**Uso real:**
- Ordenamiento externo (datos que no caben en memoria): Merge Sort es ideal porque procesa secuencialmente.
- Listas enlazadas: no requiere acceso aleatorio, solo división y mezcla.
- TimSort (Python): Merge Sort mejorado con detección de corridas ordenadas.
- Bases de datos: ordenamiento de tablas que exceden la memoria.

### 2.6 Heap Sort (referencia)

**Principio:** Construir un heap máximo con los elementos; extraer repetidamente el máximo.

**Propiedades:** No estable, in-place, siempre Θ(n log n). No adaptativo. Peor uso de caché que Quick Sort por accesos no locales.

---

## 3. Ordenamientos lineales (sin comparación)

Cuando se conocen restricciones sobre los datos (enteros en rango acotado, cadenas de longitud fija), se puede ordenar en O(n):

| Algoritmo | Idea | Complejidad | Requisito |
|-----------|------|-------------|-----------|
| Counting Sort | Contar ocurrencias de cada valor | O(n + k) | Enteros en rango k |
| Radix Sort | Ordenar por dígito, de menos a más significativo | O(d × (n + k)) | d dígitos, rango k |
| Bucket Sort | Distribuir en cubos por rango y ordenar cada cubo | O(n) promedio | Distribución uniforme |

**Conclusión clave:** Romper la barrera de Ω(n log n) requiere explotar información sobre la estructura de los datos, no solo compararlos.

---

## 4. Búsqueda

### 4.1 Búsqueda lineal

Revisar cada elemento secuencialmente. Complejidad: Θ(n). Funciona en listas desordenadas. No requiere precondiciones.

### 4.2 Búsqueda binaria

**Precondición:** La lista debe estar ordenada.

**Principio:** Comparar con el elemento central; descartar la mitad que no puede contener al objetivo; repetir.

```python
def busqueda_binaria(arr, objetivo):
    izq, der = 0, len(arr) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if arr[medio] == objetivo:
            return medio
        elif arr[medio] < objetivo:
            izq = medio + 1
        else:
            der = medio - 1
    return -1
```

**Análisis:** Recurrencia `T(n) = T(n/2) + O(1)`, luego `Θ(log n)`.

**Impacto práctico:**

| Tamaño | Lineal | Binaria |
|--------|--------|---------|
| 10 | 10 | 3 |
| 1,000 | 1,000 | 10 |
| 1,000,000 | 1,000,000 | 20 |
| 1,000,000,000 | 10⁹ | 30 |

**Variantes:**
- Búsqueda del primer/último elemento igual (lower bound / upper bound).
- Búsqueda en lista rotada.
- Búsqueda de un valor en una matriz 2D ordenada.
- Búsqueda exponencial (para listas infinitas o de tamaño desconocido).

### 4.3 Coste de ordenar antes de buscar

Ordenar cuesta O(n log n); luego cada búsqueda cuesta O(log n). Interesa ordenar si se harán al menos Ω(log n) búsquedas. Análisis: `n log n + k log n` versus `k × n`. Ordenar gana cuando `k > log n / (1 - log n/n)`, es decir, desde unas pocas búsquedas.

---

## 5. Comparativa completa

| Algoritmo | Mejor | Promedio | Peor | Estable | In-place | Adaptativo | Notas |
|-----------|-------|----------|------|---------|----------|------------|-------|
| Burbuja | O(n) | O(n²) | O(n²) | Sí | Sí | Sí | Solo docente |
| Selección | O(n²) | O(n²) | O(n²) | No | Sí | No | Mínimas escrituras |
| Inserción | O(n) | O(n²) | O(n²) | Sí | Sí | Sí | Ideal para n pequeño |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | No | Sí | No | El más rápido en la práctica |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | Sí | No | No | Ideal para externo |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | No | Sí | No | Garantía sin memoria extra |
| TimSort | O(n) | O(n log n) | O(n log n) | Sí | No | Sí | Python estándar |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | Sí | No | No | Enteros acotados |

---

## Bibliografía

1. **Cormen, T. H., Leiserson, C. E., Rivest, R. L. & Stein, C.** *Introduction to Algorithms*, III ed. MIT Press, 2009. — Capítulos 2, 6, 7, 8 (límite inferior, Quick Sort, ordenamiento lineal).
2. **Knuth, D. E.** *The Art of Computer Programming*, Vol. 3: Sorting and Searching, II ed. Addison-Wesley, 1998. — La referencia canónica.
3. **Sedgewick, R. & Wayne, K.** *Algorithms*, IV ed. Addison-Wesley, 2011. — Capítulo 2: Sorting.
4. **Weiss, M. A.** *Data Structures & Algorithm Analysis in C++*, III ed. Addison Wesley, 2006. — Capítulo 7.
5. **Hoare, C. A. R.** "Quicksort", *The Computer Journal*, 5(1):10-16, 1962. — Artículo original de Quick Sort.
6. **von Neumann, J.** "The Merge Sort", memorando interno, 1945. — Origen de Merge Sort.

## Recursos utilizados

- MIT OpenCourseWare — 6.006: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/
- VisuAlgo — Ordenamiento: https://visualgo.net/en/sorting
- Big-O Cheat Sheet: https://www.bigocheatsheet.com/
- Python Documentation — Sorting HOW TO: https://docs.python.org/3/howto/sorting.html
