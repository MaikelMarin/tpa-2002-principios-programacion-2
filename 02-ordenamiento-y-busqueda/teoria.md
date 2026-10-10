# Teoría: Métodos de Ordenamiento y Búsqueda

## Prerequisitos

| Apartado de `00-fundamentos` | Por qué se necesita aquí |
|-------------------------------|--------------------------|
| **2. Notación asintótica** | Todo el tema habla de O, Θ y Ω. Sin ella, las tablas de complejidad son decorativas |
| **4. Logaritmos** | La búsqueda binaria es `log n`; Quick Sort y Merge Sort son `n log n` |
| **5. Sumatorias** | Bubble, Selection e Insertion se analizan con `Σ i = n(n+1)/2` |
| **6. Análisis e invariantes** | Cada algoritmo de ordenamiento tiene un invariante que garantiza su corrección |
| **7. Recurrencias** | Merge Sort y Quick Sort se analizan resolviendo `T(n) = 2T(n/2) + f(n)` |
| **8. Estructuras (arreglo)** | Todos estos algoritmos operan sobre arreglos; el acceso O(1) por índice es su premisa |

---

## 1. Introducción

### 1.1 Definición de los problemas

**Ordenamiento.** Dada una secuencia de n elementos de un conjunto totalmente ordenado, producir una permutación tal que cada elemento sea menor o igual que su sucesor.

Entrada: `⟨a₁, a₂, ..., aₙ⟩`
Salida: `⟨a'₁, a'₂, ..., a'ₙ⟩` donde `a'₁ ≤ a'₂ ≤ ... ≤ a'ₙ`

**Búsqueda.** Dada una secuencia y un valor objetivo, determinar si existe y en qué posición.

**¿Por qué importan?** Ordenar es el paso previo de muchísimas operaciones: la búsqueda binaria requiere orden; el merge de dos listas requiere orden; agrupar y reportar requiere orden. Se estima que una fracción significativa de todo el cómputo mundial es ordenamiento.

### 1.2 Contexto histórico

| Año | Hito | Detalle |
|-----|------|---------|
| 1945 | Merge Sort | Von Neumann lo describe en un memorando durante el Proyecto Manhattan |
| 1946 | Búsqueda binaria | John Mauchly la presenta en una conferencia |
| 1956 | Bubble Sort | Edward Harry Friend la publica como algoritmo de enseñanza |
| 1959 | Shell Sort | Donald Shell publica su mejora de Insertion Sort |
| 1960 | Quick Sort | Tony Hoare la inventa en la Universidad de Moscú mientras trabajaba en traducción automática |
| 1962 | Quick Sort publicado | Se publica formalmente en *The Computer Journal* |
| 1964 | Heap Sort | J. W. J. Williams publica el algoritmo; Floyd lo refina |
| 1970s | Cota inferior | Se demuestra que todo ordenamiento por comparaciones requiere Ω(n log n) |
| 1990s | TimSort | Tim Peters lo diseña para Python; hoy es estándar en Python y Java (objetos) |
| 1996 | Introsort | David Musser lo diseña para C++ STL; hoy es `std::sort` |
| 2009 | PDQSort | Orson Peters lo publica; usado en Rust y versiones recientes de C++ |

### 1.3 El modelo de comparación

En el **modelo de comparación**, el algoritmo solo obtiene información del orden comparando pares de elementos. No puede inspectar bits ni asumir estructura de los datos.

**Teorema (cota inferior del ordenamiento).** Todo algoritmo de ordenamiento basado en comparaciones requiere **Ω(n log n)** comparaciones en el peor caso.

**Demostración por árbol de decisión.**

Cualquier algoritmo de ordenamiento por comparaciones puede modelarse como un árbol de decisión binario:
- Cada nodo interno es una comparación `aᵢ ≤ aⱼ` con dos salidas (sí / no).
- Cada hoja es una permutación, es decir, un orden de salida posible.
- El camino raíz → hoja describe las comparaciones hechas para una entrada concreta.

Con n elementos hay `n!` permutaciones posibles, así que el árbol necesita **al menos n! hojas**.

Un árbol binario de altura h tiene como máximo `2^h` hojas. Entonces:

```
2^h ≥ n!
h ≥ log(n!)
```

Por la aproximación de Stirling, `log(n!) = Θ(n log n)`. Luego:

```
h = Ω(n log n)
```

La altura del árbol es el peor caso del algoritmo. ∎

**Consecuencias directas:**
1. Merge Sort y Heap Sort son **óptimos**: alcanzan la cota.
2. Quick Sort es óptimo **en promedio**.
3. Ningún algoritmo por comparaciones puede ser asintóticamente mejor.
4. Para romper la barrera hay que salir del modelo: Counting Sort, Radix Sort y Bucket Sort explotan estructura de los datos y llegan a O(n).

---

## 2. Propiedades de los algoritmos de ordenamiento

| Propiedad | Significado | ¿Cuándo importa? |
|-----------|-------------|------------------|
| **Estabilidad** | Elementos iguales conservan su orden relativo de entrada | Al ordenar por múltiples claves en pasadas separadas |
| **In-place** | Usa memoria auxiliar O(1) | Sistemas embebidos, datos muy grandes |
| **Adaptativo** | Más rápido con datos parcialmente ordenados | Datos casi ordenados (logs, correcciones) |
| **Online** | Puede ordenar mientras recibe datos | Streaming |
| **Paralelizable** | Se divide en subproblemas independientes | Big data (tema 06) |

**Estabilidad con ejemplo.** Ordene por (apellido) una lista ya ordenada por (nombre):

```
Entrada (ordenada por nombre):      Salida deseada (estable):
  Ana Torres                         Ana Torres
  Luis Torres                        Luis Torres
  Ana Rojas                          Ana Rojas
  Luis Rojas                         Luis Rojas
```

Un algoritmo **estable** conserva que Ana Torres sigue antes que Luis Torres. Uno **inestable** los podría invertir. Si luego quiere ordenar por ambos criterios, la estabilidad es obligatoria.

---

## 3. Ordenamientos cuadráticos

### 3.1 Burbuja (Bubble Sort)

**Invariante.** Tras la pasada i, los i últimos elementos están en su posición final y son los i mayores.

**Estrategia.** Recorrer la lista comparando pares adyacentes; intercambiar si están en orden inverso. Tras una pasada completa, el mayor quedó al final.

```python
def burbuja(arr):
    n = len(arr)
    for i in range(n):
        intercambio = False
        for j in range(n - i - 1):        # los i últimos ya están fijos
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                intercambio = True
        if not intercambio:                # optimización
            break
    return arr
```

**Análisis exacto de comparaciones.**

| Pasada i | Comparaciones |
|----------|---------------|
| 0 | n − 1 |
| 1 | n − 2 |
| ... | ... |
| n − 1 | 0 |

Total: `(n−1) + (n−2) + ... + 0 = (n−1)n/2 = Θ(n²)`

**Casos:**
- Mejor (ya ordenado): `O(n)` — una pasada sin intercambios, gracias a la optimización.
- Promedio: `Θ(n²)`.
- Peor (orden inverso): `Θ(n²)`.

**Intercambios.** Exactamente uno por cada **inversión** del arreglo. En el peor caso hay `n(n−1)/2` inversiones.

**Propiedades:** Estable, in-place, adaptativo.

**Veredicto.** Solo docente. Nunca en producción. Su valor es que es el algoritmo más fácil de analizar correctamente, y por eso abre el tema.

### 3.2 Selección (Selection Sort)

**Invariante.** Tras la pasada i, los primeros i elementos son los i menores, en orden.

**Estrategia.** Buscar el mínimo de la región no ordenada e intercambiarlo con el primer elemento de esa región.

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

**Análisis.** Comparaciones: **siempre** `n(n−1)/2 = Θ(n²)`, sin importar el orden de entrada. Intercambios: exactamente `n − 1`.

**Propiedades:** No estable, in-place, **no adaptativo**.

**Cuándo tiene sentido.** Cuando escribir es mucho más caro que leer: memorias flash, EEPROM, registros en disco. Es el algoritmo con el **mínimo número de escrituras** posible (`n−1` intercambios), y en esos soportes eso importa más que el número de comparaciones.

### 3.3 Inserción (Insertion Sort)

**Invariante.** Tras la iteración i, el subarreglo `arr[0..i]` está ordenado.

**Estrategia.** Como ordenar cartas en la mano: tomar el siguiente elemento, desplazar los mayores hacia la derecha, e insertarlo en su posición.

```python
def insercion(arr):
    for i in range(1, len(arr)):
        clave = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > clave:
            arr[j + 1] = arr[j]        # desplazar
            j -= 1
        arr[j + 1] = clave             # insertar
    return arr
```

**Análisis.**
- Mejor (ordenado): `O(n)` — una comparación por elemento.
- Promedio: `Θ(n²/4)` — la mitad del peor caso.
- Peor (inverso): `Θ(n²/2)`.

**Propiedades:** Estable, in-place, adaptativo, **online**.

**Por qué es el más importante de los tres.** Es el mejor algoritmo para arreglos pequeños (n ≲ 20). Por eso TimSort e Introsort cambian a Insertion Sort cuando las particiones bajan de un umbral. También es el más rápido cuando los datos están *casi* ordenados.

**Análisis por inversiones.** El costo de Insertion Sort es proporcional al número de inversiones del arreglo. Si hay k inversiones, hace `O(n + k)` trabajo. Eso explica su adaptatividad: datos casi ordenados tienen pocas inversiones.

---

## 4. Ordenamientos eficientes

### 4.1 Quick Sort

**Invariante de la partición.** Tras particionar alrededor del pivote p: todo elemento a la izquierda es ≤ p, todo elemento a la derecha es ≥ p, y p está en su posición final.

**Estrategia (divide y vencerás).**
1. Elegir un pivote.
2. **Particionar** el arreglo alrededor del pivote.
3. Ordenar recursivamente cada partición.

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivote = arr[len(arr) // 2]
    izquierda  = [x for x in arr if x < pivote]
    medio      = [x for x in arr if x == pivote]
    derecha    = [x for x in arr if x > pivote]
    return quick_sort(izquierda) + medio + quick_sort(derecha)
```

Esta versión es clara pero **no es in-place** (crea listas nuevas) y no es estable.

**Versión in-place (partición de Lomuto).** Es la que se usa en la práctica:

```python
def quick_sort_inplace(arr, bajo=0, alto=None):
    if alto is None:
        alto = len(arr) - 1
    if bajo < alto:
        pi = particion(arr, bajo, alto)
        quick_sort_inplace(arr, bajo, pi - 1)
        quick_sort_inplace(arr, pi + 1, alto)
    return arr

def particion(arr, bajo, alto):
    pivote = arr[alto]              # pivote = último elemento
    i = bajo - 1                    # frontera de los menores
    for j in range(bajo, alto):
        if arr[j] <= pivote:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[alto] = arr[alto], arr[i + 1]
    return i + 1                    # posición final del pivote
```

**Análisis de complejidad.**

| Elección del pivote | Recurrencia | Solución |
|---------------------|-------------|----------|
| Siempre el del medio (equilibrado) | `T(n) = 2T(n/2) + O(n)` | `Θ(n log n)` |
| Siempre el mínimo o máximo | `T(n) = T(n-1) + O(n)` | `Θ(n²)` |
| Aleatorio (promedio) | Esperanza | `Θ(n log n)` |

Por Teorema Maestro, el caso equilibrado es `a=2, b=2, c=1`, `f(n)=n=Θ(n^c)` → caso 2 → `Θ(n log n)`.

**Por qué el peor caso es real.** Si el arreglo ya está ordenado y se toma el último elemento como pivote, cada partición separa un solo elemento: `T(n) = T(n-1) + O(n) = Θ(n²)`. Es un fallo documentado de implementaciones naif que provocó problemas de rendimiento en sistemas reales.

**Optimizaciones prácticas.**
- **Pivote aleatorio:** elimina el peor caso para entradas patológicas.
- **Mediana de tres:** probar el primero, el del medio y el último; usar la mediana.
- **Partición de tres vías:** agrupar los elementos iguales al pivote. Clave con muchos duplicados.
- **Umbral de inserción:** cambiar a Insertion Sort cuando la partición es pequeña (≲ 16).
- **IntroSort:** si la recursión se profundiza demasiado, cambiar a Heap Sort. Así se garantiza `O(n log n)` en el peor caso. Es `std::sort`.

**Propiedades:** No estable, in-place (en la versión de partición), no adaptativo.

**Por qué gana en la práctica pese a tener el mismo `n log n` que Merge Sort.** Localidad de caché (00-fundamentos §9.3): Quick Sort recorre el arreglo secuencialmente y aprovecha las líneas de caché; Merge Sort copia a memoria auxiliar. En datos reales Quick Sort suele ser 2-3× más rápido.

### 4.2 Merge Sort

**Invariante de la mezcla.** Al mezclar dos subarreglos ordenados, `resultado` contiene los menores elementos ya ordenados de ambos.

**Estrategia (divide y vencerás).**
1. Dividir el arreglo en dos mitades.
2. Ordenar recursivamente cada mitad.
3. **Mezclar** las dos mitades ordenadas en una sola.

```python
def merge(izq, der):
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:          # ≤ conserva la estabilidad
            resultado.append(izq[i]); i += 1
        else:
            resultado.append(der[j]); j += 1
    resultado.extend(izq[i:])          # resto de la izquierda
    resultado.extend(der[j:])          # resto de la derecha
    return resultado

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    m = len(arr) // 2
    return merge(merge_sort(arr[:m]), merge_sort(arr[m:]))
```

**Análisis.** `T(n) = 2T(n/2) + Θ(n)`. Teorema Maestro caso 2 → **`Θ(n log n)` siempre**, sin excepciones.

**Traza de la mezcla** para `izq=[2,5,8]`, `der=[1,3,9]`:

| Paso | i | j | Comparación | resultado |
|------|---|---|-------------|-----------|
| 1 | 0 | 0 | 2 vs 1 → toma der | [1] |
| 2 | 0 | 1 | 2 vs 3 → toma izq | [1,2] |
| 3 | 1 | 1 | 5 vs 3 → toma der | [1,2,3] |
| 4 | 1 | 2 | 5 vs 9 → toma izq | [1,2,3,5] |
| 5 | 2 | 2 | 8 vs 9 → toma izq | [1,2,3,5,8] |
| 6 | — | — | izq agotada | [1,2,3,5,8,9] |

**Por qué `≤` y no `<` en la comparación.** Cuando los elementos son iguales, tomar primero de la izquierda preserva el orden original. Con `<` se volvería inestable.

**Propiedades:** Estable, no in-place (O(n) auxiliar), no adaptativo pero **predecible**.

**Cuándo usar Merge Sort y no Quick Sort:**
1. **Ordenamiento externo** (datos que no caben en RAM, tema 06): Merge Sort lee y escribe secuencialmente, que es el modo más rápido en disco.
2. **Listas enlazadas:** no necesita acceso aleatorio, solo dividir y mezclar secuencialmente.
3. **Cuando se requiere estabilidad garantizada.**
4. **Cuando se necesita la garantía de `O(n log n)` en el peor caso** (sistemas con requisitos de tiempo real).

### 4.3 Heap Sort (referencia)

**Estrategia.** Construir un heap máximo con los elementos; extraer repetidamente el máximo y ponerlo al final.

**Propiedades:** No estable, in-place, **siempre** `Θ(n log n)`.

**Por qué no es el más usado pese a sus garantías.** Peor localidad de caché: saltar por el árbol genera más fallos de caché que recorrer un arreglo. En la práctica es más lento que Quick Sort, aunque su peor caso esté garantizado.

---

## 5. Ordenamientos lineales (sin comparación)

Si se conoce estructura de los datos, se puede saltar la barrera de `n log n`.

### 5.1 Counting Sort

**Idea.** Contar cuántas veces aparece cada valor, y usar esos conteos para colocar cada elemento directamente.

```python
def counting_sort(arr, k):
    """Ordena enteros en el rango [0, k]."""
    conteo = [0] * (k + 1)
    for x in arr:
        conteo[x] += 1
    resultado = []
    for valor in range(k + 1):
        resultado.extend([valor] * conteo[valor])
    return resultado
```

**Complejidad:** `Θ(n + k)`. **Estable** si se acumulan los conteos como posiciones finales.

**Limitación:** solo enteros en un rango acotado. Para k = 10⁹ y n = 100, reservar 10⁹ posiciones es absurdo.

### 5.2 Radix Sort

**Idea.** Ordenar por dígito, del menos significativo al más significativo. Cada pasada es un Counting Sort sobre un dígito.

```python
def radix_sort(arr):
    exp = 1
    maximo = max(arr)
    while maximo // exp > 0:
        counting_sort_por_digito(arr, exp)
        exp *= 10
    return arr
```

**Complejidad:** `Θ(d · (n + k))` donde d es el número de dígitos y k el rango de un dígito (10).

**Ventaja:** funciona con rangos enormes siempre que el número de dígitos sea moderado.

### 5.3 Bucket Sort

**Idea.** Distribuir los elementos en cubos según su rango, ordenar cada cubo (con Insertion, típicamente), y concatenar.

**Complejidad:** `Θ(n)` promedio con distribución uniforme; `Θ(n²)` peor caso si todo cae en un cubo.

---

## 6. Comparativa completa

| Algoritmo | Mejor | Promedio | Peor | Estable | In-place | Adaptativo |
|-----------|-------|----------|------|---------|----------|------------|
| Burbuja | `O(n)` | `Θ(n²)` | `Θ(n²)` | Sí | Sí | Sí |
| Selección | `Θ(n²)` | `Θ(n²)` | `Θ(n²)` | No | Sí | No |
| Inserción | `O(n)` | `Θ(n²)` | `Θ(n²)` | Sí | Sí | Sí |
| Shell | `O(n log n)` | ~`Θ(n^1.3)` | `Θ(n²)` | No | Sí | — |
| Quick Sort | `O(n log n)` | `Θ(n log n)` | `Θ(n²)` | No | Sí | No |
| Merge Sort | `Θ(n log n)` | `Θ(n log n)` | `Θ(n log n)` | Sí | No | No |
| Heap Sort | `Θ(n log n)` | `Θ(n log n)` | `Θ(n log n)` | No | Sí | No |
| Counting | `Θ(n+k)` | `Θ(n+k)` | `Θ(n+k)` | Sí | No | No |
| Radix | `Θ(d(n+k))` | `Θ(d(n+k))` | `Θ(d(n+k))` | Sí | No | No |

---

## 7. Búsqueda

### 7.1 Búsqueda lineal

Recorrer secuencialmente. `Θ(n)`. Funciona en listas desordenadas y es la única opción si no hay orden. No requiere precondiciones.

### 7.2 Búsqueda binaria

**Precondición obligatoria:** la lista debe estar ordenada.

**Invariante del bucle.** Si x está en el arreglo, entonces está en `arr[izq..der]`.

```python
def busqueda_binaria(arr, objetivo):
    izq, der = 0, len(arr) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if arr[medio] == objetivo:
            return medio
        elif arr[medio] < objetivo:
            izq = medio + 1          # descartar la mitad izquierda
        else:
            der = medio - 1          # descartar la mitad derecha
    return -1
```

**Complejidad.** `T(n) = T(n/2) + O(1)` → `Θ(log n)`.

**Impacto cuantificado:**

| Tamaño | Lineal | Binaria |
|--------|--------|---------|
| 10 | 10 | 3 |
| 1,000 | 1,000 | 10 |
| 1,000,000 | 1,000,000 | 20 |
| 1,000,000,000 | 10⁹ | 30 |

**Variantes.**
- **Lower bound:** primer elemento ≥ objetivo (o su posición de inserción).
- **Upper bound:** primer elemento > objetivo.
- **Búsqueda en lista rotada:** determinar qué mitad está ordenada.
- **Búsqueda exponencial:** para listas de tamaño desconocido o infinitas.

### 7.3 Coste de ordenar antes de buscar

Ordenar cuesta `O(n log n)`. Después, cada búsqueda cuesta `O(log n)`.

- k búsquedas sin ordenar: `k × O(n)`
- k búsquedas ordenando primero: `O(n log n) + k × O(log n)`

Ordenar conviene cuando `n log n + k log n < k·n`, es decir, aproximadamente cuando `k > log n`. Para n = 1,000,000 eso son apenas ~20 búsquedas. **Ordenar casi siempre conviene** si se va a buscar más de unas pocas decenas de veces.

---

## 8. Resumen

| Si necesita... | Use... |
|----------------|--------|
| Ordenar de propósito general | Quick Sort (o el `sorted()` del lenguaje) |
| Estabilidad garantizada | Merge Sort |
| Peor caso garantizado sin memoria extra | Heap Sort |
| Datos que no caben en RAM | Merge Sort (externo, tema 06) |
| Arreglos pequeños (< 20) | Insertion Sort |
| Datos casi ordenados | Insertion Sort o TimSort |
| Enteros en rango acotado | Counting Sort o Radix Sort |
| Mínimo número de escrituras | Selection Sort |
| Buscar una vez en lista desordenada | Búsqueda lineal |
| Buscar muchas veces | Ordenar + búsqueda binaria |

**Los tres errores más frecuentes:**

1. **Aplicar búsqueda binaria a una lista no ordenada.** Devuelve resultados incorrectos, no un error.
2. **Elegir el último elemento como pivote de Quick Sort sin aleatorizar.** Convierte el caso promedio en `O(n²)` para entradas ordenadas.
3. **Implementar una cola con `list.pop(0)`.** Es `O(n)`, no `O(1)`. Ver 00-fundamentos §8.5.

---

## Bibliografía anotada

1. **Cormen, T. H., Leiserson, C. E., Rivest, R. L. & Stein, C.** *Introduction to Algorithms*, III ed. MIT Press, 2009. — Capítulos 2 (cota inferior), 6 (Heapsort), 7 (Quicksort), 8 (ordenamiento lineal).
2. **Knuth, D. E.** *The Art of Computer Programming*, Vol. 3: Sorting and Searching, II ed. Addison-Wesley, 1998. — La referencia canónica, ~800 páginas sobre el tema.
3. **Sedgewick, R. & Wayne, K.** *Algorithms*, IV ed. Addison-Wesley, 2011. — El tratamiento más claro y visual.
4. **Weiss, M. A.** *Data Structures & Algorithm Analysis in C++*, III ed. Addison Wesley, 2006. — Capítulo 7.
5. **Hoare, C. A. R.** "Quicksort", *The Computer Journal*, 5(1):10-16, 1962. — Artículo original de Quick Sort.
6. **Musser, D. R.** "Introspective Sorting and Selection Algorithms", *Software: Practice and Experience*, 27(8):983-993, 1997. — Origen de `std::sort`.
7. **Peters, T.** "listobject.c timsort" y su descripción en https://github.com/python/cpython — Origen de TimSort.

## Recursos utilizados

- MIT OpenCourseWare — 6.006: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/
- VisuAlgo — Ordenamiento: https://visualgo.net/en/sorting
- Big-O Cheat Sheet: https://www.bigocheatsheet.com/
- Python Documentation — Sorting HOW TO: https://docs.python.org/3/howto/sorting.html
- cppreference — std::sort: https://en.cppreference.com/w/cpp/algorithm/sort
