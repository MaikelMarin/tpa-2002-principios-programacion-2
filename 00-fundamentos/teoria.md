# Teoría: Fundamentos

Andamiaje matemático y computacional necesario para comprender los seis temas del proyecto. Este documento es el cimiento: todo lo demás se apoya en él.

## Cómo usar este documento

No está pensado para leerse de corrido. Cada tema del proyecto indica en su sección **Prerequisitos** qué apartados de este documento necesita. Cuando un ejercicio asuma conocimiento previo, dirá exactamente cuál.

| Tema del proyecto | Apartados que necesita de aquí |
|-------------------|-------------------------------|
| 01 Recursividad | 3 (Inducción), 4 (Logaritmos), 5 (Sumatorias), 7 (Análisis), 8 (Recurrencias), 10 (Memoria) |
| 02 Ordenamiento y búsqueda | 2 (Notación asintótica), 4 (Logaritmos), 5 (Sumatorias), 7 (Análisis), 8 (Recurrencias) |
| 03 Árboles | 3 (Inducción estructural), 4 (Logaritmos), 8 (Recurrencias), 10 (Memoria), 11 (Python) |
| 04 Grafos | 2 (Notación), 3 (Inducción), 8 (Recurrencias), 9 (Estructuras), 10 (Memoria) |
| 05 Archivos | 9 (Estructuras), 10 (Memoria), 11 (Python) |
| 06 Grandes datos | 4 (Logaritmos), 5 (Sumatorias), 8 (Recurrencias), 10 (Memoria), 11 (Python) |

---

## 1. Mapa conceptual

```
                        FUNDAMENTOS
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   MATEMÁTICOS          COMPUTACIONALES      HERRAMIENTAS
        │                    │                    │
   ┌────┴────┐          ┌────┴────┐          ┌────┴────┐
   │         │          │         │          │         │
Notación  Inducción  Análisis  Recurrencias  Python  Estructuras
asintótica  matemática  algoritmos  (Teorema   esencial  básicas
   │         │          │         Maestro)    │         │
   │         │          │          │          │         │
 Conjuntos  Sumatorias  Memoria   Logaritmos  Clases   Arreglos
 de funciones  y series  stack/heap  y    y refs   Listas
   │         │          │         exponentes    │     Pilas/Colas
   │         │          │          │          │         │
   └─────────┴──────────┴──────────┴──────────┴─────────┘
                             │
                    Soporta los 6 temas
```

---

## 2. Notación asintótica

### 2.1 Por qué existe

Cuando comparamos dos algoritmos, contar operaciones exactas es inútil: depende del lenguaje, del compilador, de la máquina. Necesitamos una forma de hablar del **crecimiento** ignorando constantes.

La notación asintótica responde: *cuando n crece, ¿cómo crece el coste?*

### 2.2 Definiciones formales

**O grande (cota superior):**

`f(n) = O(g(n))` si existen constantes `c > 0` y `n₀ ≥ 0` tales que para todo `n ≥ n₀`:

```
0 ≤ f(n) ≤ c · g(n)
```

Lectura: "f crece a lo sumo como g, salvo constante".

**Omega (cota inferior):**

`f(n) = Ω(g(n))` si existen constantes `c > 0` y `n₀ ≥ 0` tales que para todo `n ≥ n₀`:

```
0 ≤ c · g(n) ≤ f(n)
```

Lectura: "f crece al menos como g".

**Theta (cota ajustada):**

`f(n) = Θ(g(n))` si y solo si `f(n) = O(g(n))` **y** `f(n) = Ω(g(n))`.

Lectura: "f crece exactamente como g, salvo constante".

**o pequeña (estrictamente menor):**

`f(n) = o(g(n))` si para toda constante `c > 0` existe `n₀` tal que para todo `n ≥ n₀`: `0 ≤ f(n) < c · g(n)`.

Diferencia clave con O: en `o`, la desigualdad es estricta para **toda** c, no solo para alguna. Ejemplo: `n = o(n²)` es verdadero; `2n² = o(n²)` es falso.

**omega pequeña (estrictamente mayor):**

`f(n) = ω(g(n))` si `g(n) = o(f(n))`. Análogo al anterior.

### 2.3 La cuantificación es lo importante

El error más común es tratar `O(g(n))` como "el tiempo exacto". No lo es.

`f(n) = O(g(n))` **no** significa:
- que f tarde exactamente g(n),
- que f nunca supere g(n) (solo a partir de n₀, y salvo la constante c),
- que el algoritmo sea ineficiente o eficiente en términos absolutos.

Significa únicamente: *a partir de cierto tamaño, f está acotada por una constante multiplicativa de g*.

### 2.4 Derivación paso a paso

**Ejemplo: demostrar que `3n² + 5n + 7 = O(n²)`**

Hay que encontrar `c` y `n₀` tales que `3n² + 5n + 7 ≤ c·n²` para todo `n ≥ n₀`.

Para `n ≥ 1`: `5n ≤ 5n²` y `7 ≤ 7n²`.Entonces:

```
3n² + 5n + 7 ≤ 3n² + 5n² + 7n² = 15n²
```

Así que con `c = 15` y `n₀ = 1` la desigualdad se cumple. Luego `3n² + 5n + 7 = O(n²)`.

**Ejemplo: demostrar que `n²/2 - 3n = Ω(n²)` es falso**

Para `n = 2`: `4/2 - 6 = -4`, negativo. Una cota inferior exige no negatividad desde n₀, pero  el término dominante `n²/2` gana eventualmente: para `n ≥ 7`, `n²/2 - 3n = n(n/2 - 3) ≥ n(0.5) > 0`. Y `n²/2 - 3n ≥ (1/4)n²` cuando `n²/4 ≥ 3n`, es decir `n ≥ 12`. Con `c = 1/4`, `n₀ = 12`, se cumple. Luego **sí** es `Ω(n²)`.

Moralejas: los términos de menor orden y las constantes **desaparecen**; el signo importa solo para valores pequeños de n.

### 2.5 Propiedades útiles

| Propiedad | Expresión |
|-----------|-----------|
| Transitividad | Si `f = O(g)` y `g = O(h)`, entonces `f = O(h)` |
| Suma | `f + g = O(max(f, g))` |
| Producto | Si `f = O(f')` y `g = O(g')`, entonces `f·g = O(f'·g')` |
| Polinomios | `aₖnᵏ + ... + a₀ = Θ(nᵏ)` si `aₖ > 0` |
| Logaritmos | `log_a(n) = Θ(log_b(n))` para cualesquiera bases `a, b > 1` |

La propiedad de logaritmos explica por qué en notación asintótica se escribe `log n` sin base: todas las bases son equivalentes salvo constante.

### 2.6 Jerarquía de crecimiento

De menor a mayor:

```
O(1) < O(log log n) < O(log n) < O(√n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)
```

Dónde cae cada familia de algoritmos del proyecto:

| Clase | Algoritmo |
|-------|-----------|
| `O(1)` | Acceso a arreglo por índice; verificar arista en matriz de adyacencia |
| `O(log n)` | Búsqueda binaria; altura de árbol balanceado |
| `O(n)` | Búsqueda lineal; recorrido de árbol o grafo (BFS/DFS) |
| `O(n log n)` | Merge Sort, Quick Sort (promedio), Heap Sort, Dijkstra con heap |
| `O(n²)` | Bubble, Selection, Insertion (peor caso); Dijkstra con lista |
| `O(2ⁿ)` | Fibonacci ingenuo; backtracking: Knapsack, subconjuntos, Sudoku, coloreo de grafos |
| `O(n!)` | Fuerza bruta de las N reinas; permutaciones |

### 2.7 Trampas frecuentes

1. **Confundir peor caso con caso promedio.** `T(n) = O(n²)` para Quick Sort describe el peor caso; su promedio es `O(n log n)`.
2. **Olvidar que la constante importa a escala pequeña.** En `n = 10`, un `O(n²)` con constante 1 vence a un `O(n log n)` con constante 1000. La asintótica solo manda cuando n es grande.
3. **Sumar logaritmos incorrectamente.** `log n + log n = 2 log n = Θ(log n)`, no `O(log² n)`.
4. **Tratar `O(n) = O(2n)`.** Son la misma clase: la constante no cuenta.

---

## 3. Inducción matemática

### 3.1 Por qué es la herramienta central

Cada vez que se afirma "este algoritmo es correcto para todo n" o "esta función recursiva devuelve el valor correcto", la justificación es una inducción. La inducción es el método para demostrar propiedades sobre los naturales, y por extensión sobre cualquier estructura definida recursivamente (listas, árboles, grafos).

Su relación con la recursión es exacta: **la recursión construye lo que la inducción demuestra**. Si un algoritmo es recursivo, su corrección se prueba por inducción sobre el tamaño de la entrada.

### 3.2 Inducción simple

**Principio.** Sea P una propiedad sobre los naturales. Si:

1. **Caso base:** P(0) es verdadero (o P(n₀) para algún n₀ inicial).
2. **Paso inductivo:** Para todo k ≥ 0, si P(k) es verdadero entonces P(k+1) es verdadero.

Entonces P(n) es verdadero para todo n ≥ 0.

**La hipótesis inductiva** es el "si P(k)" del paso 2. El error más común al escribir una inducción es **no usarla**: si el paso inductivo no invoca P(k), no es una inducción.

### 3.3 Demostración trabajada: suma de los primeros n naturales

**Teorema.** Para todo n ≥ 0: `1 + 2 + ... + n = n(n+1)/2`.

**Demostración por inducción sobre n.**

*Caso base (n = 0):* La suma vacía es 0, y `0·1/2 = 0`. P(0) se cumple.

*Hipótesis inductiva:* Supongamos que para algún k ≥ 0, `1 + 2 + ... + k = k(k+1)/2`.

*Paso inductivo:* Queremos probar P(k+1), es decir `1 + ... + k + (k+1) = (k+1)(k+2)/2`. Partimos de la izquierda:

```
1 + 2 + ... + k + (k+1)
  = [1 + 2 + ... + k] + (k+1)      (asociatividad)
  = k(k+1)/2 + (k+1)                (hipótesis inductiva)
  = (k+1)(k/2 + 1)                  (factor común k+1)
  = (k+1)(k+2)/2                    (simplificar)
```

Que es exactamente el lado derecho. Luego P(k+1) se cumple, y por inducción P(n) para todo n ≥ 0. ∎

### 3.4 Inducción fuerte

**Principio.** Si P(0) es verdadero, y para todo k ≥ 0 se cumple que *si P(i) es verdadero para todo i ≤ k* entonces P(k+1) es verdadero, entonces P(n) para todo n.

La diferencia: la hipótesis inductiva asume **todos** los casos anteriores, no solo k. Es la variante natural para algoritmos divide y vencerás, donde el subproblema no es exactamente "uno menos" sino "la mitad".

### 3.5 Demostración trabajada: correctitud de la búsqueda binaria

**Teorema.** Si `arr` está ordenado ascendentemente y el valor `x` está en `arr`, la búsqueda binaria devuelve un índice i con `arr[i] = x`.

**Invariante del bucle.** Al inicio de cada iteración con rango `[izq, der]`:
- Si `x` está en el arreglo, entonces `x` está en `arr[izq..der]`.

**Inicialización.** En la primera iteración el rango es todo el arreglo, y por hipótesis `x` está en él. El invariante se cumple.

*Nota:* usamos inducción fuerte porque el rango no se reduce en uno, sino a la mitad.

**Conservación.** Si `arr[medio] == x`, el algoritmo devuelve y termina correcto. Si `arr[medio] < x`, entonces `x` solo puede estar a la derecha (el arreglo está ordenado), y el nuevo rango `[medio+1, der]` lo conserva. Si `arr[medio] > x`, análogo con `[izq, medio-1]`. El invariante se preserva.

**Terminación.** El rango se reduce estrictamente en cada iteración (`der - izq` disminuye), y el bucle termina cuando `izq > der`, devolviendo -1. Pero si `x` estaba, el invariante garantiza que se encuentra antes de que el rango se vacíe. ∎

Este patrón —*invariante + inicialización + conservación + terminación*— es la plantilla para demostrar correctitud de **cualquier** bucle, y se usará repetidamente en los temas 02 y 04.

### 3.6 Inducción estructural

**Principio.** Para demostrar que una propiedad P vale para todos los elementos de una estructura definida recursivamente, basta probar:
1. P vale para los casos base de la definición.
2. Si P vale para las subestructuras inmediatas, entonces vale para la estructura construida sobre ellas.

**Aplicación a árboles.** Un árbol se define como: o bien es vacío, o bien es un nodo con dos subárboles. Para probar una propiedad sobre todos los árboles, se prueba para el árbol vacío y se prueba que si vale para los subárboles izquierdo y derecho, vale para el árbol completo.

**Demostración trabajada: el recorrido inorden de un BST produce una secuencia ordenada.**

**Teorema.** Sea T un BST. El recorrido inorden (izquierdo, raíz, derecho) visita los valores en orden estrictamente creciente.

**Demostración por inducción estructural sobre T.**

*Caso base:* T vacío. El recorrido no visita nada; la secuencia vacía está trivialmente ordenada.

*Hipótesis inductiva:* Supongamos que para los subárboles I (izquierdo) y D (derecho) de la raíz r, sus recorridos inorden producen secuencias ordenadas.

*Paso:* El recorrido inorden de T es `inorden(I)` seguido de `r` seguido de `inorden(D)`. Por la propiedad BST, todo valor en I es menor que r, y todo valor en D es mayor que r. Por hipótesis inductiva `inorden(I)` está ordenado y `inorden(D)` está ordenado. Como todos los elementos de la primera lista son menores que r, y todos los de la segunda son mayores, la concatenación completa está ordenada. ∎

### 3.7 Cuándo usar cada variante

| Situación | Variante |
|-----------|----------|
| Propiedad sobre enteros, paso de 1 en 1 | Simple |
| Algoritmo divide y vencerás (reduce a la mitad) | Fuerte |
| Estructuras recursivas: árboles, listas, expresiones | Estructural |
| Correctitud de un bucle | Simple (con invariante) |
| Acotación de una recurrencia | Fuerte |

---

## 4. Logaritmos y exponenciales

### 4.1 Por qué aparecen en todos los algoritmos

`log n` aparece cada vez que un algoritmo **reduce el problema a la mitad** en cada paso. Si de n elementos pasamos a n/2, luego a n/4, y queremos saber cuántos pasos hay hasta llegar a 1:

```
n → n/2 → n/4 → ... → 1
```

Después de k pasos quedan `n/2ᵏ` elementos. Paramos cuando `n/2ᵏ ≤ 1`, es decir `2ᵏ ≥ n`, es decir `k ≥ log₂ n`.

**Conclusión:** dividir a la mitad repetidamente da exactamente `log₂ n` pasos. Es la razón por la que la búsqueda binaria, la altura de un árbol balanceado y Merge Sort tienen un logaritmo.

### 4.2 Definición e identidades

`log_b(n)` es el exponente al que hay que elevar b para obtener n: `b^(log_b n) = n`.

| Identidad | Expresión |
|-----------|-----------|
| Producto | `log_b(xy) = log_b(x) + log_b(y)` |
| Cociente | `log_b(x/y) = log_b(x) - log_b(y)` |
| Potencia | `log_b(xᵏ) = k·log_b(x)` |
| Cambio de base | `log_b(n) = log_c(n) / log_c(b)` |
| Relación con potencias | `b^(log_b n) = n` y `log_b(bᵏ) = k` |

**Consecuencia del cambio de base:** todas las bases difieren solo en una constante multiplicativa (`1/log_c(b)`). Por eso en notación asintótica se escribe `log n` sin especificar base.

### 4.3 Logaritmos en distintas bases

Como `log₂ n = log₁₀ n / log₁₀ 2 ≈ 3.32 · log₁₀ n`, la base solo cambia el factor constante:

| Base | Notación | Uso típico |
|------|----------|------------|
| 2 | `log₂ n` | Algoritmos que dividen a la mitad |
| e | `ln n` | Análisis matemático, continuo |
| 10 | `log₁₀ n` | Escalas, órdenes de magnitud |

### 4.4 Crecimiento comparado

Para `n = 1,000,000`:

| Función | Valor | Interpretación |
|---------|-------|----------------|
| `log₂ n` | ~20 | Veinte pasos de división a la mitad |
| `√n` | 1,000 | |
| `n` | 1,000,000 | |
| `n log₂ n` | ~20,000,000 | |
| `n²` | 10¹² | |

La diferencia entre `n` y `n log n` para un millón de elementos es un factor de 20. La diferencia entre `n log n` y `n²` es un factor de 50,000. Por eso Merge Sort (`n log n`) puede ordenar un millón de elementos en segundos, mientras que Bubble Sort (`n²`) necesitaría horas.

### 4.5 Exponenciales y por qué son el enemigo

`2ⁿ` crece tan rápido que problemas de esa complejidad son inviables salvo para n diminuto:

| n | 2ⁿ |
|---|-----|
| 10 | 1,024 |
| 20 | ~1 millón |
| 30 | ~1,000 millones |
| 40 | ~1 billón |
| 60 | ~10¹⁸ (más que la edad del universo en nanosegundos) |

De aquí la regla práctica del proyecto: si un algoritmo es `O(2ⁿ)`, solo es usable para n ≤ ~25. Fibonacci ingenuo cae aqui, y su version con memorizacion baja a polinomial.

El **backtracking** (tema 01, §4) tambien vive en `O(2ⁿ)` en el peor caso: Knapsack, subconjuntos, Sudoku y coloreo de grafos. Para esos, la **poda** no cambia la complejidad asintotica pero si la viabilidad real: el Sudoku pasa de inviable a milisegundos. Cuando ademas hay *subproblemas superpuestos* (Knapsack, subconjuntos), la memorizacion baja el costo a polinomial.

### 4.6 Teorema Maestro (vista rápida)

Para recurrencias de divide y vencerás `T(n) = a·T(n/b) + f(n)`, con `a ≥ 1`, `b > 1`:

Sea `c = log_b(a)` (el exponente crítico).

| Caso | Condición sobre f(n) | Solución |
|------|----------------------|----------|
| 1 | `f(n) = O(n^(c-ε))` para algún ε > 0 | `T(n) = Θ(n^c)` |
| 2 | `f(n) = Θ(n^c)` | `T(n) = Θ(n^c · log n)` |
| 3 | `f(n) = Ω(n^(c+ε))` y condición de regularidad | `T(n) = Θ(f(n))` |

El desarrollo completo, con ejemplos resueltos, está en la sección 8 de este documento.

---

## 5. Sumatorias y series

### 5.1 Por qué importan

Los bucles se analizan contando cuántas veces se ejecuta cada operación, y eso se expresa como una suma. Las tres series que aparecen una y otra vez en el proyecto son la aritmética, la geométrica y la armónica.

### 5.2 Serie aritmética

**Fórmula:** `1 + 2 + 3 + ... + n = n(n+1)/2`

**Demostración (atribuida a Gauss):** Escribe la serie dos veces, una ascendente y otra descendente, y suma columna a columna:

```
  S = 1   + 2      + 3      + ... + (n-1) + n
  S = n   + (n-1)  + (n-2)  + ... + 2     + 1
  ─────────────────────────────────────────────
 2S = (n+1) + (n+1) + (n+1) + ... + (n+1) + (n+1)   [n términos]
```

Luego `2S = n(n+1)`, y `S = n(n+1)/2`. ∎

**Uso:** contar comparaciones de Bubble Sort, Selection Sort e Insertion Sort, todas con `Σ de i=1 a n-1 de i = (n-1)n/2 ≈ n²/2`.

### 5.3 Serie geométrica

**Fórmula (razón r ≠ 1):** `1 + r + r² + ... + rⁿ = (r^(n+1) - 1)/(r - 1)`

Si `0 < r < 1`, la serie infinita converge: `Σ(k=0 a ∞) rᵏ = 1/(1-r)`.

**Uso:** analizar estructuras que se duplican por nivel (árboles), el análisis del heap, y el costo de la reducción a la mitad (`1 + 1/2 + 1/4 + ... = 2`).

### 5.4 Serie armónica

**Definición:** `H(n) = 1 + 1/2 + 1/3 + ... + 1/n`

**Comportamiento asintótico:** `H(n) = Θ(log n)`. Crece muy lentamente: para n = 1,000,000, H(n) ≈ 14.4.

**Uso:** el análisis esperado de Quick Sort cuando el pivote es aleatorio (sección 8.5 del tema 02), y el análisis amortizado de algunas estructuras.

### 5.5 Sumatorias con logaritmos

`Σ(k=1 a n) log k = log(n!) = Θ(n log n)` por la aproximación de Stirling. Es la fórmula que explica de inmediato por qué todo algoritmo que hace `log k` de trabajo para cada uno de n elementos termina en `n log n`.

### 5.6 Tabla de referencia rápida

| Suma | Resultado |
|------|-----------|
| `Σ(i=1 a n) 1` | `n` |
| `Σ(i=1 a n) i` | `n(n+1)/2 = Θ(n²)` |
| `Σ(i=1 a n) i²` | `n(n+1)(2n+1)/6 = Θ(n³)` |
| `Σ(i=1 a n) 1/i` | `H(n) = Θ(log n)` |
| `Σ(i=1 a n) log i` | `log(n!) = Θ(n log n)` |
| `Σ(i=0 a n) 2ⁱ` | `2^(n+1) - 1 = Θ(2ⁿ)` |

---

## 6. Análisis de algoritmos

### 6.1 Qué se mide

El coste de un algoritmo se mide en **operaciones fundamentales**: comparaciones, asignaciones, accesos a memoria. No en segundos: el tiempo real depende de la máquina, el lenguaje y el compilador.

**Operación fundamental** = la operación que domina el costo. En ordenamiento suele ser la comparación; en búsqueda, la comparación; en grafos, el acceso a un vértice o arista.

### 6.2 Contar operaciones: ejemplo trabajado

**Algoritmo:** Bubble Sort, versión básica.

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):              # (1)
        for j in range(n - i - 1):  # (2)
            if arr[j] > arr[j + 1]: # (3)
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

Conteo de comparaciones (línea 3):

| Valor de i | Iteraciones de j | Comparaciones |
|------------|------------------|---------------|
| 0 | n - 1 | n - 1 |
| 1 | n - 2 | n - 2 |
| ... | ... | ... |
| n - 1 | 0 | 0 |
| **Total** | | `(n-1) + (n-2) + ... + 0 = (n-1)n/2` |

Por la fórmula aritmética: `Θ(n²)` comparaciones. Los intercambios, en el peor caso (arreglo invertido), son también `Θ(n²)`.

### 6.3 Mejor caso, peor caso y caso promedio

| Concepto | Definición | Ejemplo: Quick Sort |
|----------|------------|---------------------|
| **Mejor caso** | Entrada más favorable | Pivote siempre divide equilibradamente: `Θ(n log n)` |
| **Peor caso** | Entrada más desfavorable | Pivote siempre el mínimo o máximo: `Θ(n²)` |
| **Caso promedio** | Esperado sobre entradas aleatorias | `Θ(n log n)` |

**Por qué importan los tres.** Un algoritmo puede tener el mismo peor caso que otro pero mejor promedio (Quick Sort vs Merge Sort). O el mismo promedio pero mejor mejor caso (Insertion Sort vs Quick Sort para datos casi ordenados). Publicar solo un número es engañoso: el proyecto siempre reporta los tres.

### 6.4 Invariantes de bucle

Un **invariante** es una propiedad que se cumple antes y después de cada iteración. Es la herramienta para demostrar correctitud de bucles (sección 3.5).

Inariantes clave del proyecto:

| Algoritmo | Invariante |
|-----------|------------|
| Búsqueda binaria | Si x está en arr, está en `arr[izq..der]` |
| Bubble Sort | Tras la pasada i, los i últimos elementos están en su posición final |
| Insertion Sort | Tras la iteración i, `arr[0..i]` está ordenado |
| Merge (mezcla) | `resultado` contiene los menores elementos ya ordenados de ambas mitades |
| Dijkstra | Al extraer un vértice del heap, su distancia es definitiva |
| BFS | Los vértices se visitan en orden no decreciente de distancia al origen |

### 6.5 Análisis amortizado

**Idea:** una operación puede ser cara ocasionalmente, pero si se reparte su costo entre muchas operaciones baratas, el costo *promedio por operación* es bajo.

**El ejemplo canónico: Union-Find con compresión de caminos.**

Cada operación `find` puede recorrer un camino largo. Pero cada vez que lo hace, **acorta** ese camino para todas las futuras llamadas. Si se hacen m operaciones sobre n elementos, el costo total es `O(m · α(n))`, donde α es la inversa de la función de Ackermann, que crece tan lentamente que para cualquier n práctico α(n) ≤ 5.

Moraleja: el análisis amortizado explica por qué Union-Find, visto desde una sola operación, parece `O(n)`, pero usado en Kruskal sobre m operaciones es efectivamente `O(1)` por operación. Es el resultado que hace eficiente el MST.

### 6.6 Modelos de coste

| Modelo | Descripción | Uso |
|--------|-------------|-----|
| **Uniforme** | Cada operación cuesta 1 | Análisis estándar del proyecto |
| **Logarítmico** | Cada operación sobre k bits cuesta `O(log k)` | Análisis de algoritmos numéricos |
| **Comparación** | Solo comparaciones cuentan | Ordenamiento; da la cota Ω(n log n) |

El modelo de comparación es el que produce el teorema de la sección 7.4 del tema 02.

---

## 7. Recurrencias

### 7.1 Qué es una recurrencia

Una **recurrencia** expresa el costo de un problema en términos del costo de subproblemas menores:

```
T(n) = a · T(n/b) + f(n)
```

Se lee: "resolver un problema de tamaño n cuesta a llamadas recursivas sobre problemas de tamaño n/b, más f(n) de trabajo adicional".

Resolver la recurrencia = encontrar su forma cerrada (sin T del lado derecho).

### 7.2 Las tres recurrencias del proyecto

| Recurrencia | Algoritmo | Solución |
|-------------|-----------|----------|
| `T(n) = 2T(n/2) + O(n)` | Merge Sort | `Θ(n log n)` |
| `T(n) = T(n/2) + O(1)` | Búsqueda binaria | `Θ(log n)` |
| `T(n) = 2T(n/2) + O(1)` | Recorrido de árbol | `Θ(n)` |
| `T(n) = T(n-1) + O(n)` | Quick Sort peor caso | `Θ(n²)` |

### 7.3 Método 1: sustitución

Adivinar la solución y verificarla por inducción.

**Ejemplo:** `T(n) = 2T(n/2) + n`, con `T(1) = 1`.

Conjetura: `T(n) = n log n + n`. Verifiquemos por inducción sobre n (suponiendo n potencia de 2):

```
T(n) = 2T(n/2) + n
     = 2[(n/2) log(n/2) + n/2] + n      (hipótesis inductiva)
     = n log(n/2) + n + n
     = n(log n - log 2) + 2n
     = n log n - n + 2n
     = n log n + n                        ✓
```

La conjetura es correcta. ∎

**Limitación:** hay que adivinar la solución primero. Funciona bien cuando la forma es obvia.

### 7.4 Método 2: árbol de recursión

Dibujar el árbol de llamadas y sumar el costo por nivel.

Para `T(n) = 2T(n/2) + n`:

```
Nivel 0:  n              → costo n
Nivel 1:  n/2 + n/2      → costo n
Nivel 2:  n/4 × 4        → costo n
...
Nivel k:  n/2ᵏ nodos     → costo n cada uno
Niveles totales: log₂ n
```

Costo total = `n × log₂ n = Θ(n log n)`.

**Ventaja:** intuitivo y visual. **Limitación:** requiere que el costo por nivel sea regular.

### 7.5 Método 3: Teorema Maestro

Para `T(n) = a·T(n/b) + f(n)` con `a ≥ 1`, `b > 1`, sea `c = log_b(a)`:

| Caso | Condición | Solución |
|------|-----------|----------|
| 1 | `f(n) = O(n^(c-ε))`, algún ε > 0 | `T(n) = Θ(n^c)` |
| 2 | `f(n) = Θ(n^c)` | `T(n) = Θ(n^c · log n)` |
| 3 | `f(n) = Ω(n^(c+ε))` y `a·f(n/b) ≤ k·f(n)` con k < 1 | `T(n) = Θ(f(n))` |

**Interpretación de c:** `n^c` es "el costo de las hojas del árbol" (las llamadas base). Los tres casos comparan el costo de combinar (`f(n)`) contra el costo de las hojas.

**Ejemplos resueltos:**

*`T(n) = 2T(n/2) + n`:* `a = 2`, `b = 2`, `c = log₂ 2 = 1`. Como `f(n) = n = Θ(n¹)`, es **caso 2**: `T(n) = Θ(n log n)`. ✓

*`T(n) = 2T(n/2) + 1`:* `a = 2`, `b = 2`, `c = 1`. `f(n) = 1 = O(n^(1-ε))` con ε = 1. Es **caso 1**: `T(n) = Θ(n^1) = Θ(n)`. ✓

*`T(n) = 8T(n/2) + n²`:* `a = 8`, `b = 2`, `c = log₂ 8 = 3`. `f(n) = n² = O(n^(3-ε))` con ε = 1. Es **caso 1**: `T(n) = Θ(n³)`. ✓

*`T(n) = T(n/2) + 1`:* `a = 1`, `b = 2`, `c = log₂ 1 = 0`. `f(n) = 1 = Θ(n⁰)`. Es **caso 2**: `T(n) = Θ(n⁰ log n) = Θ(log n)`. ✓

### 7.6 Cuando el Teorema Maestro no aplica

No aplica si:
- `a` no es constante (p. ej. `T(n) = 2n·T(n/2)`)
- `f(n)` no encaja en ningún caso (p. ej. `T(n) = 2T(n/2) + n log n`)
- Los subproblemas no tienen el mismo tamaño

Para esos casos se usa sustitución o el método del árbol.

---

## 8. Estructuras de datos fundamentales

### 8.1 Por qué empiezan aquí y no en árboles

Los seis temas del proyecto construyen sobre estas cinco estructuras. Si no se dominan sus costes, no se puede evaluar si un BST o un grafo es mejor opción. Son la línea de base contra la que se compara todo lo demás.

### 8.2 Arreglo (array)

Secuencia de elementos del mismo tipo almacenados en posiciones contiguas de memoria.

```python
arr = [10, 20, 30, 40, 50]
arr[2]        # acceso directo: 30
len(arr)      # tamaño: 5
```

| Operación | Coste | Por qué |
|-----------|-------|---------|
| Acceso por índice | `O(1)` | Dirección = base + índice × tamaño |
| Búsqueda | `O(n)` | Hay que revisar uno a uno |
| Inserción al final | `O(1)` amortizado | Duplicar capacidad cuando se llena |
| Inserción/eliminación en medio | `O(n)` | Hay que desplazar elementos |
| Eliminar último | `O(1)` | |

**Propiedad clave:** el acceso por índice es `O(1)` porque la memoria es contigua: la dirección del elemento i se calcula aritméticamente, sin recorrer nada. Esta propiedad es la que explotan la búsqueda binaria y la matriz de adyacencia.

**En Python:** la `list` es un arreglo dinámico. Acceder por índice es `O(1)`. **Pero** `arr.insert(0, x)` y `arr.pop(0)` son `O(n)` porque desplazan todo; para eso está `collections.deque`.

### 8.3 Lista enlazada (linked list)

Secuencia de nodos, cada uno con un valor y una referencia al siguiente.

```python
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None
```

| Operación | Coste | Por qué |
|-----------|-------|---------|
| Acceso por índice | `O(n)` | Hay que recorrer desde la cabeza |
| Búsqueda | `O(n)` | Ídem |
| Inserción/eliminación al inicio | `O(1)` | Solo cambiar la referencia de la cabeza |
| Inserción/eliminación con referencia al nodo previo | `O(1)` | Reapuntar |
| Búsqueda del nodo previo | `O(n)` | |

**Diferencia fundamental con el arreglo:** sacrifica el acceso aleatorio (que era la fortaleza del arreglo) a cambio de inserción/eliminación baratas sin desplazar datos.

**Comparación directa:**

| Criterio | Arreglo | Lista enlazada |
|----------|---------|----------------|
| Acceso `arr[i]` | `O(1)` | `O(n)` |
| Insertar al inicio | `O(n)` | `O(1)` |
| Insertar al final | `O(1)` amortizado | `O(n)` (o `O(1)` con puntero a la cola) |
| Memoria | Compacta, un bloque | Dispersa, un objeto por nodo + referencia |
| Localidad de caché | Excelente | Mala |

**Dónde aparece en el proyecto:** el tema 03 (BST a lista enlazada) y el tema 02 (Merge Sort sobre lista enlazada, donde la ausencia de acceso aleatorio no molesta porque Merge Sort solo necesita dividir y mezclar secuencialmente).

### 8.4 Pila (stack)

Estructura LIFO: último en entrar, primero en salir.

```python
from collections import deque
pila = deque()
pila.append(1)    # push
pila.pop()        # pop
pila[-1]          # ver el tope sin quitar
```

| Operación | Coste |
|-----------|-------|
| push | `O(1)` |
| pop | `O(1)` |
| ver tope | `O(1)` |
| buscar | `O(n)` |

**Quién la usa en el proyecto:**
- La **pila de llamadas** del intérprete (sección 10.1) — cada llamada recursiva apila un marco.
- El **DFS iterativo** (tema 04) — los vértices por visitar viven en una pila.
- Los **recorridos iterativos de árboles** (tema 03) — el inorden y postorden sin recursión.

En Python, `list.append` y `list.pop` ya son `O(1)`, así que una lista sirve como pila; `deque` es preferible si también se opera por el frente.

### 8.5 Cola (queue)

Estructura FIFO: primero en entrar, primero en salir.

```python
from collections import deque
cola = deque([1, 2, 3])
cola.append(4)       # encolar
cola.popleft()       # desencolar
```

| Operación | Coste |
|-----------|-------|
| encolar | `O(1)` |
| desencolar | `O(1)` |
| ver frente | `O(1)` |

**Error común:** usar `list.pop(0)` como cola. Eso es `O(n)` porque desplaza todos los elementos. La forma correcta es `collections.deque`, que es `O(1)` por ambos extremos.

**Quién la usa en el proyecto:** el **BFS** (tema 04), donde los vértices se procesan exactamente en el orden en que se descubrieron. Esa propiedad FIFO es la que garantiza que BFS encuentre el camino más corto en grafos no ponderados.

### 8.6 Tabla hash (hash table / diccionario)

Estructura que asocia claves a valores usando una función hash.

```python
d = {}
d["clave"] = "valor"     # insertar/actualizar: O(1) promedio
d["clave"]                # consultar: O(1) promedio
"clave" in d             # pertenencia: O(1) promedio
```

| Operación | Promedio | Peor caso |
|-----------|----------|-----------|
| Insertar | `O(1)` | `O(n)` |
| Consultar | `O(1)` | `O(n)` |
| Eliminar | `O(1)` | `O(n)` |
| Pertenencia | `O(1)` | `O(n)` |

**Por qué el peor caso es O(n):** si todas las claves colisionan al mismo índice, la tabla degrada a una lista. Con una buena función hash y redimensionado, la probabilidad es insignificante.

**Quién la usa en el proyecto:** lista de adyacencia (tema 04), conjuntos de visitados en BFS/DFS, memoización (tema 01), y el diccionario de frecuencias en conteo.

### 8.7 Tabla comparativa maestra

| Estructura | Acceso | Búsqueda | Inserción | Eliminación | Ordenada |
|------------|--------|----------|-----------|-------------|----------|
| Arreglo (desordenado) | `O(1)` | `O(n)` | `O(n)` / `O(1)` al final | `O(n)` | No |
| Arreglo (ordenado) | `O(1)` | `O(log n)` | `O(n)` | `O(n)` | Sí |
| Lista enlazada | `O(n)` | `O(n)` | `O(1)` | `O(1)`* | No |
| Pila | `O(n)` | `O(n)` | `O(1)` | `O(1)` | LIFO |
| Cola | `O(n)` | `O(n)` | `O(1)` | `O(1)` | FIFO |
| Tabla hash | — | `O(1)` | `O(1)` | `O(1)` | No |
| BST balanceado | — | `O(log n)` | `O(log n)` | `O(log n)` | Sí |

\* con referencia al nodo previo.

**Cómo leer esta tabla:** si necesitas acceso rápido por clave, hash. Si necesitas datos ordenados con inserción y borrado eficientes, BST balanceado. Si solo apilas o encolas, pila o cola. Los temas 03 y 04 existen precisamente para llenar la fila que el hash no cubre: datos **ordenados** con operaciones logarítmicas.

---

## 9. Modelo de memoria

### 9.1 Stack vs heap

Todo programa tiene dos regiones de memoria principales:

**Stack (pila):**
- Almacena marcos de llamadas: parámetros, variables locales, dirección de retorno.
- Crece y se encoge automáticamente con las llamadas a función.
- Muy rápida: asignar es solo mover un puntero.
- **Limitada:** típicamente 8 MB en Linux. Agotarla da `RecursionError` en Python, `StackOverflowError` en Java, fallo de segmento en C++.

**Heap:**
- Almacena objetos cuya vida supera a la función que los creó (en Python, todos los objetos).
- Crece y se encoge por el recolector de basura.
- Más lenta, pero prácticamente ilimitada (limitada por la RAM).

**Consecuencia directa:** cada llamada recursiva consume stack. Por eso la recursión tiene un límite (~1000 en Python) y por qué la versión iterativa de un algoritmo usa menos memoria que la recursiva para el mismo problema.

### 9.2 Referencias vs valores

**Python:** las variables son **referencias** a objetos. Asignar no copia:

```python
a = [1, 2, 3]
b = a          # b apunta al MISMO objeto
b.append(4)
print(a)       # [1, 2, 3, 4]  ← a también cambió
```

Para copiar de verdad:

```python
import copy
b = a[:]           # copia superficial
b = copy.deepcopy(a)  # copia profunda
```

**Por qué importa:** en los algoritmos del proyecto, pasar una lista a una función no la protege de modificaciones. El backtracking depende de esto: modifica el estado compartido y luego lo deshace. Y los errores más frecuentes en los ejercicios de árboles vienen de confundir "reasignar un nodo" con "modificar el nodo".

**C++ (contraste):** las variables son valores por defecto. Copiar un `std::vector` sí duplica los datos. Los punteros y las referencias existen para evitar esa copia. Esta diferencia es una de las razones por las que el proyecto compara Python con C++.

### 9.3 Localidad de caché

La CPU lee memoria en **líneas de caché** (típicamente 64 bytes), no byte a byte. Si los datos que usa un algoritmo están contiguos, una sola línea de caché sirve para varios accesos.

- **Arreglos:** contiguos, excelente localidad. Recorrerlos es rápido pese a ser `O(n)`.
- **Listas enlazadas:** dispersos en el heap, cada nodo puede estar en una línea de caché distinta. Recorrerlos es mucho más lento en la práctica de lo que sugiere el `O(n)`.

**Aplicación real en el proyecto:** Merge Sort y Quick Sort recorren arreglos de forma secuencial y aprovechan la caché. Heap Sort salta por el árbol de forma no secuencial y sufre más fallos de caché. Ambos son `Θ(n log n)`, pero Quick Sort es consistentemente más rápido en la práctica. La diferencia no está en la complejidad, está en la localidad.

### 9.4 Cuánta memoria usa cada estructura

Para n elementos (en Python, aproximado):

| Estructura | Memoria | Nota |
|------------|---------|------|
| Lista de n enteros | ~8n bytes (punteros) + objetos int | Los enteros pequeños están internados |
| `deque` | Similar, con overhead por bloque | |
| Lista enlazada de n nodos | ~56n bytes (objeto + 2 referencias) | Mucho más que un arreglo |
| Tabla hash con n entradas | ~3-4n entradas reservadas | Redimensiona al 2/3 de carga |
| Matriz n×n | ~8n² bytes (o n² objetos lista) | El motivo por el que se prefiere lista de adyacencia en grafos dispersos |

**Implicación para grafos:** una matriz de adyacencia para un grafo con 10,000 vértices y 20,000 aristas reserva 100 millones de entradas, de las cuales ~20,000 son útiles. La lista de adyacencia usa memoria proporcional a `V + E`. Por eso en grafos dispersos (el caso real) siempre se usa lista de adyacencia. Este cálculo está desarrollado en la sección 3 del tema 04.

---

## 10. Python esencial para el proyecto

No es un tutorial de Python: es exactamente lo que hay que saber para leer y escribir el código de los seis temas sin tropiezos.

### 10.1 Clases y referencias

La base de los árboles y grafos:

```python
class Nodo:
    def __init__(self, valor):
        self.valor = valor          # atributo de instancia
        self.izquierdo = None       # referencia, no un objeto
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"
```

Puntos que causan errores:
- `self.izquierdo = None` crea una **referencia** nula; el objeto solo existe al asignar `Nodo(...)`.
- Dos variables pueden apuntar al mismo nodo. Modificar una modifica la otra (sección 9.2).
- `__repr__` es lo que se muestra al imprimir; definirla ahorra depurar a ciegas.

### 10.2 El límite de recursión

```python
import sys
sys.getrecursionlimit()      # 1000 por defecto
sys.setrecursionlimit(10000) # se puede subir, con cuidado
```

Subirlo demasiado provoca un cierre del proceso por agotar el stack real del sistema operativo. Para recursión profunda (más de ~10,000 niveles) hay que reescribir en iterativo. Este límite es el que hace que los recorridos iterativos del tema 03 no sean opcionales.

### 10.3 Comprensiones de lista

Forma compacta y eficiente de construir listas:

```python
# Equivalente a un bucle for con append
cuadrados = [x * x for x in range(10)]

# Con filtro
pares = [x for x in range(20) if x % 2 == 0]

# Con transformación condicional
signos = ["pos" if x > 0 else "neg o cero" for x in [-1, 0, 2]]
```

Se usan en Quick Sort para las particiones y en construcción de listas de vecinos.

### 10.4 Generadores

Producen valores **uno a la vez**, sin materializar la lista completa. Clave para el tema 06.

```python
def leer_lineas(ruta):
    with open(ruta) as f:
        for linea in f:          # el archivo se lee bajo demanda
            yield linea.strip()

# Consumo perezoso: nunca todas las líneas en memoria a la vez
total = sum(1 for _ in leer_lineas("grande.txt"))
```

**Diferencia crucial:**

```python
[f"linea {i}" for i in range(10**6)]        # construye 1M de strings en memoria
(f"linea {i}" for i in range(10**6))        # no construye nada todavía
```

Un generador con paréntesis en vez de corchetes no ocupa memoria hasta que se consume. Esta es la diferencia entre procesar 1 GB de datos y quedarse sin RAM.

### 10.5 `with` y gestión de recursos

```python
with open("archivo.txt", "r", encoding="utf-8") as f:
    datos = f.read()
# f se cierra aquí automáticamente, incluso si hay excepción
```

Equivale a `try/finally` con cierre garantizado. Siempre se usa así en el proyecto: dejar archivos abiertos agota los descriptores del sistema operativo.

### 10.6 Excepciones

```python
try:
    with open("inexistente.txt") as f:
        contenido = f.read()
except FileNotFoundError:
    print("El archivo no existe")
except PermissionError:
    print("Sin permisos")
except UnicodeDecodeError:
    print("Problema de codificación")
```

Las excepciones del proyecto son las del tema 05. Patrón: capturar la excepción **específica**, no `except Exception` a secas, que oculta errores reales de programación.

### 10.7 El módulo `struct` (archivos binarios)

```python
import struct

# Empaquetar: entero (4 bytes) + flotante (4 bytes)
datos = struct.pack("<if", 42, 3.14)

# Desempaquetar
entero, flotante = struct.unpack("<if", datos)
```

`<` = little-endian, `i` = int de 4 bytes, `f` = float de 4 bytes. El orden de bytes importa al intercambiar archivos entre máquinas; está desarrollado en la sección 4 del tema 05.

### 10.8 `collections` imprescindible

| Herramienta | Para qué | Coste |
|-------------|----------|-------|
| `deque` | Pila y cola con `O(1)` por ambos extremos | |
| `defaultdict` | Diccionario con valor por defecto | Igual que `dict` |
| `Counter` | Contar frecuencias | `O(n)` |
| `heapq` | Cola de prioridad (heap binario) | `push`/`pop` en `O(log n)` |

```python
from collections import deque, defaultdict

# Pila
pila = deque()
pila.append(1); pila.pop()

# Cola (NO usar list.pop(0), que es O(n))
cola = deque([1, 2])
cola.append(3); cola.popleft()

# Diccionario con valor por defecto
conteo = defaultdict(int)
conteo["clave"] += 1        # sin KeyError, inicia en 0
```

---

## Bibliografía

1. **Cormen, T. H., Leiserson, C. E., Rivest, R. L. & Stein, C.** *Introduction to Algorithms*, III ed. MIT Press, 2009. — Capítulo 3: Growth of Functions (notación asintótica), Capítulo 4: Divide and Conquer (recurrencias y Teorema Maestro).
2. **Knuth, D. E.** *The Art of Computer Programming*, Vol. 1: Fundamental Algorithms, III ed. Addison-Wesley, 1997. — Secciones 1.2.1-1.2.10: análisis matemático y notación.
3. **Sedgewick, R. & Wayne, K.** *Algorithms*, IV ed. Addison-Wesley, 2011. — Sección 1.4: Analysis of Algorithms.
4. **Goodrich, M. T., Tamassia, R. & Goldwasser, M. H.** *Data Structures & Algorithms in Python*. Wiley, 2013. — Capítulo 5: Stacks, Queues, and Deques.
5. **Weiss, M. A.** *Data Structures & Algorithm Analysis in C++*, III ed. Addison Wesley, 2006. — Capítulo 2: Algorithm Analysis.
6. **Black, P. E. (ed.)** *Dictionary of Algorithms and Data Structures*, NIST. — Definiciones formales de referencia.
7. **Hein, J. L.** *Discrete Structures, Logic, and Computability*, IV ed. Jones & Bartlett, 2010. — Inducción matemática y demostraciones.

## Recursos utilizados

- MIT OpenCourseWare — 6.006 Introduction to Algorithms: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/
- MIT OpenCourseWare — 6.042J Mathematics for Computer Science (inducción y demostraciones): https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/
- Khan Academy — Asymptotic notation: https://www.khanacademy.org/computing/computer-science/algorithms/asymptotic-notation
- Python Documentation — `collections`: https://docs.python.org/3/library/collections.html
- Python Documentation — Functional Programming (generadores y comprensiones): https://docs.python.org/3/howto/functional.html





