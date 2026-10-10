# Teoría: Fundamentos de Recursividad

---

## 1. Introducción a la recursividad

### 1.1 Definición formal

Una función **recursiva** es una función que se llama a sí misma durante su ejecución. Formalmente, una función f es recursiva si en su cuerpo aparece una llamada a f.

La recursividad se basa en dos principios matemáticos fundamentales:

1. **División del problema:** Un problema grande se descompone en uno o más subproblemas del mismo tipo, pero de menor tamaño.
2. **Caso base:** Existe al menos un caso que puede resolverse directamente, sin recursión.

Sin caso base, la recursión sería infinita. Sin reducción del problema, la recursión nunca llegaría al caso base.

### 1.2 Contexto matemático

La recursividad tiene raíces en las matemáticas:

- **Inducción matemática:** Es el argumento gemelo de la recursión. La inducción demuestra que una propiedad P(n) es cierta para todo n probando P(0) y que P(k) implica P(k+1). La recursión *construye* lo que la inducción *demuestra*.
- **Relaciones de recurrencia:** Ecuaciones como `T(n) = 2T(n/2) + n` describen el costo de algoritmos recursivos. Se resuelven con el Teorema Maestro, el método de sustracción o el árbol de recursión.
- **Funciones μ-recursivas (años 30):** Gödel, Kleene y Church formalizaron qué funciones son computables. La recursividad es uno de los modelos equivalentes de computabilidad, junto con la Máquina de Turing y el cálculo λ.

### 1.3 Evolución histórica detallada

| Año | Hito | Detalle |
|-----|------|---------|
| 1845 | Condición de recursividad matemática | Gotthold Eisenstein establece condiciones para definir secuencias por recurrencia |
| 1889 | Definición por recursión de funciones | Giuseppe Peano axiomatiza los naturales y define formalmente la recursión primitiva |
| 1931 | Teoremas de incompletitud | Gödel usa la autorreferencia, cercana a la recursividad, para demostrar sus teoremas |
| 1936 | Computabilidad | Alan Turing publica su máquina; Alonzo Church el cálculo λ; ambos demuestran que los problemas recursivamente enumerables son indecidibles |
| 1936 | Máquina de Turing universal | Demuestra que una máquina puede simular otra: base de la computación moderna |
| 1958 | Lenguaje LISP | John McCarthy crea el primer lenguaje con recursión como mecanismo principal de control |
| 1960 | ALGOL 60 | Primer lenguaje con especificación formal (BNF) que incluye recursión |
| 1960 | Programación estructurada | Hoare, Dijkstra y Wirth promueven la recursión sobre `GOTO` |
| 1970 | Autómatas y compiladores | La recursión descendente se convierte en técnica estándar de parsing |
| 1990s | Programación dinámica | Se formaliza la memoización (top-down) y el bottom-up |
| Hoy | Todo el ecosistema | Parsers, compiladores, bases de datos (índices B-tree), IA (divide y vencerás) |

### 1.4 Componentes de una función recursiva

Una función recursiva correcta tiene siempre estas partes:

1. **Caso base:** La condición que detiene la recursión. Debe ser alcanzable.
2. **Reducción:** Cada llamada recursiva opera sobre datos estrictamente menores o un problema estrictamente más pequeño.
3. **Llamada recursiva:** La función se invoca a sí misma.

Ejemplo completo:

```python
def factorial(n):
    # Caso base
    if n <= 1:
        return 1
    # Paso recursivo: n * factorial(n-1)
    return n * factorial(n - 1)
```

### 1.5 La pila de llamadas (Call Stack)

La pila de llamadas es una región de memoria que almacena el estado de cada función activa. Cada llamada recursiva apila un marco (frame) que contiene:

- Los parámetros recibidos
- Las variables locales
- La dirección de retorno
- El valor de retorno parcial

Visualización paso a paso de `factorial(4)`:

```
┌──────────────────────────────────────┐
│ factorial(4) → 4 * factorial(3)     │   Apilado 1
│                                      │
│  factorial(3) → 3 * factorial(2)    │   Apilado 2
│                                      │
│   factorial(2) → 2 * factorial(1)   │   Apilado 3
│                                      │
│    factorial(1) → 1  ← CASO BASE    │   Apilado 4 (fondo)
│                                      │
│   Desapilado: factorial(1) = 1      │   Retorna 1
│  Desapilado: factorial(2) = 2×1 = 2 │   Retorna 2
│ Desapilado: factorial(3) = 3×2 = 6  │   Retorna 6
│ Desapilado: factorial(4) = 4×6 = 24 │   Retorna 24
└──────────────────────────────────────┘
```

En Python:

```python
import sys

def factorial(n, profundidad=0):
    sangria = "  " * profundidad
    print(f"{sangria}→ factorial({n})")
    if n <= 1:
        print(f"{sangria}← retorna 1")
        return 1
    resultado = n * factorial(n - 1, profundidad + 1)
    print(f"{sangria}← retorna {resultado}")
    return resultado

factorial(4)
```

Salida:

```
→ factorial(4)
  → factorial(3)
    → factorial(2)
      → factorial(1)
      ← retorna 1
    ← retorna 2
  ← retorna 6
← retorna 24
```

**Límite de recursión en Python:**

```python
import sys
print(sys.getrecursionlimit())   # 1000 por defecto
sys.setrecursionlimit(5000)      # Se puede aumentar con cuidado
```

Superar el límite produce `RecursionError`. En Java es `StackOverflowError`; en C++, fallo de segmento.

### 1.6 Recursividad vs Iteración

| Criterio | Recursividad | Iteración |
|----------|-------------|-----------|
| Legibilidad | Elegante para problemas recursivos (árboles, backtracking) | Simple para bucles |
| Memoria | O(n) por la pila | O(1) |
| Velocidad | Overhead de llamadas | Más rápida |
| Riesgo | Stack overflow | Bucle infinito |
| Uso ideal | Backtracking, árboles, divide y vencerás | Bucles simples |

---

## 2. Funciones recursivas clásicas

### 2.1 Factorial

Definición matemática: `n! = n × (n-1) × … × 1`, con `0! = 1`.

Recurrencia: `factorial(n) = n × factorial(n-1)`, `factorial(0) = 1`.

Python:
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

Java:
```java
public static int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

C++:
```cpp
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

**Cuidado:** El factorial crece extremadamente rápido. `20! ≈ 2.4×10^18` ya desborda un `int`. En Python los enteros son de precisión arbitraria; en Java usar `long` o `BigInteger`; en C++ `long long`.

### 2.2 Potencia

Recurrencia: `potencia(b, e) = b × potencia(b, e-1)`, `potencia(b, 0) = 1`.

Versión ineficiente: O(e).

Versión con divide y vencerás: O(log e).

```python
def potencia_eficiente(base, exponente):
    if exponente == 0:
        return 1
    mitad = potencia_eficiente(base, exponente // 2)
    if exponente % 2 == 0:
        return mitad * mitad
    return base * mitad * mitad
```

¿Por qué funciona? Porque `b^e = (b^(e/2))²` si e es par, y `b^e = b × (b^((e-1)/2))²` si e es impar. Cada llamada reduce el exponente a la mitad.

### 2.3 Serie de Fibonacci

Definición:
```
F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2)   para n ≥ 2
```

Historia: Leonardo de Pisa (Fibonacci) publicó esta secuencia en *Liber Abaci* (1202) para modelar el crecimiento de conejos. Aparece en la naturaleza: filotaxis, disposición de semillas, conchas del nautilus.

**Versión ingenua:** O(2^n). Es el ejemplo clásico de lo que NO se debe hacer: recalcula los mismos valores exponencialmente veces.

**Memoización (top-down):** O(n) tiempo, O(n) espacio.

```python
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

**Bottom-up (iterativo):** O(n) tiempo, O(1) espacio.

```python
def fib_bottom_up(n):
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

### 2.4 Otras funciones recursivas notables

- **Máximo común divisor (Euclides):** `mcd(a, b) = mcd(b, a mod b)`, `mcd(a, 0) = a`. O(log min(a,b)).
- **Suma de dígitos:** `suma(n) = n % 10 + suma(n // 10)`, base `n == 0`.
- **Número de particiones:** Funciones recursivas de partición en teoría de números.
- **Coeficientes binomiales:** `C(n,k) = C(n-1,k-1) + C(n-1,k)`.

---

## 3. Recursión con estructuras de datos

### 3.1 Listas

El patrón **cabeza + cola** es la base de la recursión sobre listas:

```python
def suma(lista):
    if not lista:          # Lista vacía = caso base
        return 0
    return lista[0] + suma(lista[1:])
```

Nota: `lista[1:]` crea una copia (O(n)). La versión con índice es más eficiente:

```python
def suma_indice(lista, i=0):
    if i >= len(lista):
        return 0
    return lista[i] + suma_indice(lista, i + 1)
```

En LISP (familia Scheme/Haskell), este patrón es primitivo: `car` (cabeza) y `cdr` (cola). Toda la programación funcional se construye sobre esto.

### 3.2 Listas anidadas

```python
def suma_anidada(lista):
    total = 0
    for elemento in lista:
        if isinstance(elemento, list):
            total += suma_anidada(elemento)
        else:
            total += elemento
    return total
```

Este patrón se usa en parsing de JSON/XML, donde la profundidad de anidación es arbitraria.

### 3.3 Matrices

Recorrido recursivo de una matriz:

```python
def recorrer(matriz, fila=0, col=0):
    if fila >= len(matriz):
        return
    if col >= len(matriz[0]):
        recorrer(matriz, fila + 1, 0)
        return
    print(matriz[fila][col], end=" ")
    recorrer(matriz, fila, col + 1)
```

Aplicaciones: recorrido en espiral, multiplicación de matrices (Strassen, divide y vencerás), rotación de matrices, detección de patrones.

### 3.4 Recursión mutua

Dos o más funciones se llaman entre sí:

```python
def es_par(n):
    if n == 0:
        return True
    return es_impar(n - 1)

def es_impar(n):
    if n == 0:
        return False
    return es_par(n - 1)
```

Se usa en compiladores (análisis sintáctico) y en máquinas de estado.

---

## 4. Vuelta atrás recursiva (Backtracking)

### 4.1 Concepto

El **backtracking** construye soluciones incrementalmente y retrocede cuando determina que una solución parcial no puede completarse. Es una búsqueda en profundidad sobre el espacio de soluciones.

Distinguir de la recursión simple:
- **Recursión pura:** Divide el problema y resuelve subproblemas independientes.
- **Backtracking:** Explora opciones secuencialmente, con la capacidad de deshacer.

### 4.2 Plantilla general

```python
def backtrack(estado):
    if es_completo(estado):
        registrar_solucion(estado)
        return
    for opcion in opciones_validas(estado):
        aplicar(opcion, estado)          # Hacer
        backtrack(estado)                # Explorar
        deshacer(opcion, estado)         # Deshacer (backtrack)
```

La llamada `deshacer` es lo que distingue al backtracking de la recursión pura.

### 4.3 Problema de las N reinas

Historia:
- **1848:** Max Bezzel, matemático alemán, plantea el problema de las 8 reinas.
- **1850:** Franz Nauck encuentra la primera solución.
- **1969:** Se convierte en problema estándar de backtracking en la literatura académica.

Definición: Colocar N reinas en un tablero N×N sin que ninguna ataque a otra. Dos reinas se atacan si comparten fila, columna o diagonal.

Enfoque: Colocar reina por columna. Para cada columna, probar cada fila. Si es segura, colocar y pasar a la siguiente columna. Si ninguna fila funciona, retroceder.

```python
def es_segura(tablero, fila, col, n):
    for i in range(fila):
        if tablero[i][col] == 1:
            return False
    for i, j in zip(range(fila, -1, -1), range(col, -1, -1)):
        if tablero[i][j] == 1:
            return False
    for i, j in zip(range(fila, -1, -1), range(col, n)):
        if tablero[i][j] == 1:
            return False
    return True

def resolver(tablero, col, n):
    if col >= n:
        return True
    for fila in range(n):
        if es_segura(tablero, fila, col, n):
            tablero[fila][col] = 1
            if resolver(tablero, col + 1, n):
                return True
            tablero[fila][col] = 0
    return False
```

Complejidad: O(N!) en el peor caso; con poda prácticamente es mucho menor. Para N=8 hay 92 soluciones; para N=10 hay 724.

### 4.4 Problema de la mochila (Knapsack)

Definición: Dados objetos con peso y valor, y una mochila con capacidad máxima, maximizar el valor transportado sin exceder la capacidad.

Solución por backtracking: O(2^n). Solución por programación dinámica: O(n×W), donde W es la capacidad.

---

## 5. Torres de Hanói

Inventado por el matemático francés **Édouard Lucas** en 1883.

Reglas:
1. Solo se mueve un disco a la vez.
2. Un disco grande no puede colocarse sobre uno pequeño.
3. Solo se puede mover el disco superior de una torre.

Solución recursiva:

```python
def torres_hanoi(n, origen="A", destino="C", auxiliar="B"):
    if n == 1:
        print(f"Mover disco 1 de {origen} a {destino}")
        return 1
    movimientos = 0
    movimientos += torres_hanoi(n - 1, origen, auxiliar, destino)
    print(f"Mover disco {n} de {origen} a {destino}")
    movimientos += 1
    movimientos += torres_hanoi(n - 1, auxiliar, destino, origen)
    return movimientos
```

Recurrencia: `T(n) = 2T(n-1) + 1`, con `T(1) = 1`. Solución: `T(n) = 2^n - 1`.

Leyenda: Los monjes de un monasterio mueven 64 discos; al terminar, se acaba el mundo. A un disco por segundo, tomaría 585 mil millones de años.

---

## 6. Análisis de recursiones

### 6.1 Teorema Maestro

Para recurrencias de la forma `T(n) = aT(n/b) + f(n)`:

| Caso | Condición | Resultado |
|------|-----------|-----------|
| 1 | f(n) = O(n^(log_b(a) - ε)) | T(n) = Θ(n^log_b(a)) |
| 2 | f(n) = Θ(n^log_b(a)) | T(n) = Θ(n^log_b(a) × log n) |
| 3 | f(n) = Ω(n^(log_b(a) + ε)) | T(n) = Θ(f(n)) |

### 6.2 Ejemplos

| Recurrencia | Algoritmo | Solución |
|-------------|-----------|----------|
| T(n) = 2T(n/2) + O(n) | Merge Sort | Θ(n log n) |
| T(n) = T(n/2) + O(1) | Búsqueda binaria | Θ(log n) |
| T(n) = 2T(n/2) + O(1) | Recorrido de árbol | Θ(n) |
| T(n) = T(n-1) + O(n) | Quick Sort peor caso | Θ(n²) |

### 6.3 Profundidad de recursión

La profundidad máxima de recursión determina el uso de pila:

- Búsqueda binaria: O(log n) — muy segura.
- Merge Sort: O(log n) de profundidad, O(n) de espacio por los merges.
- Backtracking N reinas: O(N) de profundidad, pero explora O(N!) nodos.

---

## Bibliografía

1. **Cormen, T. H., Leiserson, C. E., Rivest, R. L. & Stein, C.** *Introduction to Algorithms*, III ed. MIT Press, 2009. — Capítulos 2, 4 (Teorema Maestro) y 35 (Programación dinámica).
2. **Goodrich, M. T., Tamassia, R. & Goldwasser, M. H.** *Data Structures & Algorithms in Python*. Wiley, 2013. — Capítulo 4: Recursion.
3. **Weiss, M. A.** *Data Structures & Algorithm Analysis in C++*, III ed. Addison Wesley, 2006. — Capítulo 3.
4. **Sedgewick, R. & Wayne, K.** *Algorithms*, IV ed. Addison-Wesley, 2011. — Sección 1.1: Basic Programming Models.
5. **Knuth, D. E.** *The Art of Computer Programming*, Vol. 1: Fundamental Algorithms, III ed. Addison-Wesley, 1997.
6. **Abelson, H. & Sussman, G. J.** *Structure and Interpretation of Computer Programs*, II ed. MIT Press, 1996. — Capítulo 1: Building Abstractions with Procedures.

## Recursos utilizados

- MIT OpenCourseWare — 6.006 Introduction to Algorithms (otoño 2011): https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/
- GeeksforGeeks — Recursion and Backtracking: https://www.geeksforgeeks.org/recursion/
- Brilliant.org — Backtracking: https://brilliant.org/wiki/recursion-backtracking/
- Python Documentation — sys.setrecursionlimit: https://docs.python.org/3/library/sys.html#sys.setrecursionlimit
