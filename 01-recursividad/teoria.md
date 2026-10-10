# Teoría: Fundamentos de Recursividad

## Prerequisitos

Antes de leer este documento se necesitan estos apartados de `00-fundamentos`:

| Apartado | Por qué se necesita aquí |
|----------|--------------------------|
| **3. Inducción matemática** | La corrección de toda función recursiva se demuestra por inducción. Es el gemelo de la recursión: si no se domina, este tema se vuelve memorístico |
| **4. Logaritmos y exponenciales** | Para entender por qué la búsqueda binaria es `log n` y Fibonacci ingenuo es `2ⁿ` |
| **5. Sumatorias** | Para analizar Torres de Hanói (`2ⁿ - 1`) y el costo por nivel |
| **7. Recurrencias** | Todo análisis de recursividad se expresa como `T(n) = aT(n/b) + f(n)` |
| **9. Modelo de memoria (stack)** | Cada llamada recursiva apila un marco. Sin entender el stack, el límite de recursión parece arbitrario |
| **10. Python esencial** | Clases para nodos, comprensiones para particiones, generadores, límite de recursión |

Si alguno de estos puntos no está claro, conviene leerlo primero. El documento asume que se conocen.

---

## 1. Introducción a la recursividad

### 1.1 Definición formal

Una función **recursiva** es una función que se invoca a sí misma durante su ejecución.

Más precisamente, una definición recursiva sobre un dominio D consta de:

1. **Cláusulas base:** los valores de la función para ciertos argumentos se definen directamente, sin apelar a la función misma.
2. **Cláusulas recursivas:** los valores restantes se definen en términos de la función aplicada a argumentos **menores** en un orden bien fundado.

La condición de "argumentos menores" es la que garantiza la terminación: hay una medida (típicamente el tamaño de la entrada) que decrece en cada llamada y está acotada inferiormente.

**Analogía.** Las muñecas matryoshka: cada muñeca contiene una más pequeña, hasta llegar a la que es maciza y no se abre. La muñeca maciza es el caso base; el proceso de abrir es la reducción; encontrar la muñeca dentro es la llamada recursiva.

**Segunda analogía, más técnica.** Un índice de un libro técnico: para entender "recursividad", el índice dice "véase recursividad". Eso sería una definición inútil (circular). Una definición recursiva útil sería: "recursividad: véase recursión, que a su vez se define en la página X". La clave es que la cadena de referencias **termina** en algo concreto.

### 1.2 Contexto matemático: la inducción es el gemelo

La recursión y la inducción matemática son el mismo fenómeno visto desde dos ángulos:

| Inducción (demuestra) | Recursión (construye) |
|-----------------------|----------------------|
| Prueba P(0) | Caso base |
| Prueba que P(k) implica P(k+1) | Llamada recursiva sobre problema menor |
| Conclusión: P(n) para todo n | El algoritmo cubre todo tamaño de entrada |

Si una función es recursiva, su corrección se demuestra por inducción sobre el tamaño de la entrada. Este documento muestra esa demostración explícita para factorial, potencia, búsqueda binaria y Hanoi.

### 1.3 Evolución histórica detallada

| Año | Hito | Detalle |
|-----|------|---------|
| 1845 | Condición de recursividad | Eisenstein establece condiciones matemáticas para definir secuencias por recurrencia |
| 1889 | Axiomas de Peano | Peano axiomatiza los naturales y define formalmente la recursión primitiva |
| 1931 | Incompletitud | Gödel usa la autorreferencia (concepto cercano) para sus teoremas |
| 1936 | Computabilidad | Turing (máquina), Church (cálculo λ) y Kleene (funciones recursivas) formalizan qué es computable; los tres modelos resultan equivalentes |
| 1958 | LISP | McCarthy crea el lenguaje donde la recursión es el mecanismo de control principal |
| 1960 | ALGOL 60 | Primer lenguaje con especificación formal que incluye recursión |
| 1960s | Estructurada | Dijkstra y Hoare promueven recursión sobre `GOTO`; nace la corrección formal |
| 1970 | Parsing | La recursión descendente se vuelve técnica estándar de compiladores |
| 1970s | Divide y vencerás | Merge Sort y Quick Sort popularizan la recursión "útil" |
| 1990s | Programación dinámica | Se formaliza memoización (top-down) y tabulación (bottom-up) |
| Hoy | Ubicuidad | Parsers, compiladores, índices B-tree, IA (divide y vencerás), backtracking |

**Dato relevante:** la tesis de Church-Turing establece que toda función computable es recursiva. En ese sentido, la recursión no es una técnica entre otras: es la forma misma de la computación.

### 1.4 Anatomía de una función recursiva

Toda función recursiva correcta tiene exactamente estas tres piezas:

```python
def funcion(n):
    # 1. CASO BASE: resuelve sin recursión
    if n <= 1:
        return 1

    # 2. REDUCCIÓN: n es estrictamente menor que el original
    # 3. LLAMADA: se invoca a sí misma
    return n * funcion(n - 1)
```

**Reglas de oro:**

1. **Debe existir al menos un caso base.** Sin él, la recursión es infinita y agota el stack.
2. **Cada llamada debe reducir el problema.** Si el argumento no decrece, jamás se alcanza el caso base.
3. **La reducción debe ser finita.** No basta con decrecer: debe decrecer hacia un valor donde el caso base aplique. Decrementar en 0.5 desde 10 nunca llega a 0.

**Error frecuente:** caso base inalcanzable. `def f(n): return 1 if n == 0 else f(n - 2)` con `n` impar nunca llega a 0: cae en -1, -3, -5... y desborda.

### 1.5 La pila de llamadas, marco por marco

La pila de llamadas es una región de memoria donde cada función activa tiene un **marco** (frame) con:

- Los parámetros recibidos
- Las variables locales
- La dirección de retorno (dónde continuar al terminar)
- El valor de retorno parcial

Traza completa de `factorial(3)` mostrando el contenido de cada marco:

| Paso | Acción | Pila (de arriba abajo) |
|------|--------|------------------------|
| 1 | Llamar `factorial(3)` | `[f(3): n=3]` |
| 2 | `f(3)` llama a `f(2)` | `[f(3): n=3]`, `[f(2): n=2]` |
| 3 | `f(2)` llama a `f(1)` | `[f(3)]`, `[f(2)]`, `[f(1): n=1]` |
| 4 | `f(1)` es caso base, retorna 1 | `[f(3)]`, `[f(2)]` ← retorna 1 |
| 5 | `f(2)` calcula `2×1`, retorna 2 | `[f(3)]` ← retorna 2 |
| 6 | `f(3)` calcula `3×2`, retorna 6 | vacía ← retorna 6 |

Visualización en Python:

```python
def factorial_traza(n, profundidad=0):
    sangria = "    " * profundidad
    print(f"{sangria}→ factorial({n})  [profundidad {profundidad}]")
    if n <= 1:
        print(f"{sangria}← caso base: retorna 1")
        return 1
    resultado = n * factorial_traza(n - 1, profundidad + 1)
    print(f"{sangria}← retorna {resultado}")
    return resultado

factorial_traza(3)
```

Salida:

```
→ factorial(3)  [profundidad 0]
    → factorial(2)  [profundidad 1]
        → factorial(1)  [profundidad 2]
        ← caso base: retorna 1
    ← retorna 2
← retorna 6
```

**Lectura clave:** observe que los `← retorna` aparecen en orden inverso a los `→`. La pila se desapila en orden LIFO. Por eso el valor se "acumula" al volver: cada nivel multiplica su `n` por lo que recibió.

**Límite de recursión:**

```python
import sys
sys.getrecursionlimit()       # 1000 por defecto en CPython
sys.setrecursionlimit(10000)  # subirlo es posible pero peligroso
```

Superar el límite lanza `RecursionError`. Subirlo mucho puede agotar el stack real del sistema operativo y cerrar el proceso. Para recursión profunda (> ~10,000 niveles) hay que reescribir en iterativo: esa es la razón de que los recorridos iterativos del tema 03 no sean opcionales.

### 1.6 Recursión de cola (tail recursion)

Una llamada es **de cola** cuando la llamada recursiva es la última operación: no hay nada pendiente por hacer con su resultado.

```python
# NO es de cola: hay que multiplicar después
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)      # ← multiplicación pendiente

# SÍ es de cola: la llamada es lo último
def factorial_cola(n, acumulador=1):
    if n <= 1:
        return acumulador
    return factorial_cola(n - 1, acumulador * n)   # ← nada pendiente
```

**Importancia:** en lenguajes con optimización de llamada de cola (Scheme, Haskell, Erlang, y C++ con compiladores optimizados), la versión de cola usa espacio **O(1)** en vez de O(n), porque el marco se reutiliza en vez de apilarse.

**Python y Java no hacen esta optimización.** En Python, ambas versiones usan O(n) de pila. La versión de cola sigue siendo útil por claridad, pero no ahorra memoria.

### 1.7 Recursividad vs iteración

| Criterio | Recursividad | Iteración |
|----------|-------------|-----------|
| Legibilidad | Elegante cuando el problema es recursivo por naturaleza (árboles, backtracking) | Simple para recorridos lineales |
| Memoria | O(profundidad) de pila | O(1) típicamente |
| Velocidad | Overhead de llamadas a función | Más rápida |
| Riesgo | `RecursionError` / stack overflow | Bucle infinito si la condición falla |
| Depuración | Traza clara por la pila | Más plana |

**Regla de decisión práctica:**

- El problema se descompone en subproblemas del mismo tipo → **recursión** (Merge Sort, árboles, backtracking)
- Es un recorrido lineal con estado simple → **iteración**
- La profundidad puede ser enorme → **iteración** obligada
- Hay que exprimir rendimiento → **iteración**

### 1.8 Coste: cómo se mide una función recursiva

Para una función recursiva se miden dos cosas:

1. **Número de llamadas** (o tamaño del árbol de recursión) → determina el tiempo.
2. **Profundidad máxima** → determina el espacio de pila.

Ejemplo con Fibonacci ingenuo: el árbol de llamadas para `fib(5)` tiene 15 nodos (número de llamadas), pero profundidad máxima 5. El tiempo es proporcional al número de nodos (`Θ(2ⁿ)`); el espacio, a la profundidad (`Θ(n)`). **Estas dos cantidades pueden diferir enormemente**, y confundirlas es un error común.

---

## 2. Funciones recursivas clásicas

Estas cinco funciones son el alfabeto de la recursión. Cada una se presenta con su estrategia, su traza, su demostración de corrección y su análisis de coste.

### 2.1 Factorial

**Definición matemática.** Para n ≥ 0: `n! = n × (n-1) × ... × 1`, con la convención `0! = 1`.

**Recurrencia.** `factorial(n) = n × factorial(n-1)`, con `factorial(0) = 1`.

**Estrategia.** La definición matemática ya es recursiva: el factorial de n se expresa usando el factorial de n-1. La traducción a código es casi literal. No hay que inventar nada: la recurrencia se mapea directo al caso recursivo y el hecho de que `0! = 1` es el caso base.

**Implementación.**

```python
def factorial(n):
    """n! definido recursivamente."""
    if n < 0:
        raise ValueError("El factorial no está definido para negativos")
    if n <= 1:                 # caso base
        return 1
    return n * factorial(n - 1)  # caso recursivo
```

**Por qué el caso base es `n <= 1` y no `n == 0`.** Ambas son correctas matemáticamente, porque `1! = 1` también. Usar `n <= 1` ahorra una llamada (no se invoca `factorial(0)`), y evita el problema de que un `n` negativo pase de largo. Es la forma idiomática.

**Traza de `factorial(4)`:**

| Llamada | n | ¿Caso base? | Cálculo | Retorna |
|---------|---|-------------|---------|---------|
| `f(4)` | 4 | No | `4 × f(3)` | espera |
| `f(3)` | 3 | No | `3 × f(2)` | espera |
| `f(2)` | 2 | No | `2 × f(1)` | espera |
| `f(1)` | 1 | **Sí** | — | 1 |
| `f(2)` | — | — | `2 × 1` | 2 |
| `f(3)` | — | — | `3 × 2` | 6 |
| `f(4)` | — | — | `4 × 6` | 24 |

**Demostración de corrección (inducción sobre n).**

*Caso base:* `n = 0`. La función retorna 1, y `0! = 1` por definición. Correcto.

*Hipótesis inductiva:* supongamos que `factorial(k)` retorna `k!` para todo `k < n`.

*Paso:* para `n ≥ 1`, la función retorna `n × factorial(n-1)`. Por hipótesis inductiva, `factorial(n-1) = (n-1)!`. Luego retorna `n × (n-1)! = n!`. Correcto. ∎

**Análisis de coste.**

- Recurrencia de llamadas: `L(n) = L(n-1) + 1` con `L(1) = 1` → `L(n) = n`.
- Tiempo: **O(n)**, una multiplicación por llamada.
- Espacio: **O(n)** de pila, una marco por llamada (no optimización de cola en Python).

**Límite numérico.** `21! ≈ 5.1 × 10¹⁹` ya excede el rango de un entero de 64 bits (`~9.2 × 10¹⁸`). En Python los enteros son de precisión arbitraria así que no hay desborde; en Java haría falta `BigInteger` y en C++ `long long` o biblioteca de precisión arbitraria. Este es un detalle que se retoma en el tema 02.

**Variantes.**

```python
# Iterativa: O(1) de espacio
def factorial_iterativo(n):
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado

# De cola: equivalente en Python (sin optimización), útil en Scheme/Haskell
def factorial_cola(n, acumulador=1):
    if n <= 1:
        return acumulador
    return factorial_cola(n - 1, acumulador * n)

# Con la biblioteca estándar
import math
math.factorial(5)      # 120
math.prod(range(1, 6)) # 120
```

**Ejercicio relacionado:** `ejercicios/factorial.py`.

### 2.2 Potencia

**Definición.** `b^e` = b multiplicado por sí mismo e veces, con `b⁰ = 1`.

**Recurrencia ingenua.** `potencia(b, e) = b × potencia(b, e-1)`, con `potencia(b, 0) = 1`.

**Estrategia (versión ingenua).** Idéntica al factorial: la definición ya es recursiva. Coste O(e) con O(e) de pila.

**Estrategia (versión eficiente).** Observar que el exponente se puede **partir a la mitad**:

```
b^e = (b^(e/2))²          si e es par
b^e = b × (b^((e-1)/2))²  si e es impar
```

Esto es divide y vencerás puro: en vez de reducir el problema en 1, se reduce a la mitad.

**Implementación eficiente.**

```python
def potencia(b, e):
    if e == 0:
        return 1
    mitad = potencia(b, e // 2)
    if e % 2 == 0:
        return mitad * mitad
    return b * mitad * mitad
```

**Traza de `potencia(2, 10)`:**

| Llamada | (b, e) | Calcula | Sub-llamadas |
|---------|--------|---------|--------------|
| `p(2,10)` | par | `mitad²` | `p(2,5)` |
| `p(2,5)` | impar | `2 × mitad²` | `p(2,2)` |
| `p(2,2)` | par | `mitad²` | `p(2,1)` |
| `p(2,1)` | impar | `2 × mitad²` | `p(2,0)` |
| `p(2,0)` | base | 1 | — |

Son 5 llamadas para exponente 10, no 10. En general, `Θ(log e)` llamadas.

**Análisis de coste.**

- Recurrencia: `T(e) = T(e/2) + O(1)`. Por Teorema Maestro (caso 2, con `a=1`, `b=2`, `c=0`): **Θ(log e)**.
- Espacio: **Θ(log e)** de pila.

**Comparación:** para `e = 1,000,000`, la versión ingenua hace un millón de multiplicaciones; la eficiente, 20.

**Ejercicio relacionado:** `ejercicios/potencia.py`.

### 2.3 Serie de Fibonacci

**Definición.** `F(0) = 0`, `F(1) = 1`, `F(n) = F(n-1) + F(n-2)` para `n ≥ 2`.

**Contexto.** Leonardo de Pisa publicó la secuencia en *Liber Abaci* (1202) modelando cría de conejos. Aparece en filotaxis (disposición de hojas y semillas), en conchas del nautilus y en la razón áurea: `F(n+1)/F(n) → φ ≈ 1.618`.

**Versión ingenua.**

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

**Por qué es catastrófica.** El árbol de llamadas de `fib(5)`:

```
                    fib(5)
               /              \
          fib(4)                fib(3)
         /      \              /      \
     fib(3)    fib(2)       fib(2)    fib(1)
     /    \    /    \      /    \
 fib(2) fib(1) ...        fib(1) fib(0)
```

Note que `fib(3)` se calcula **dos veces**, `fib(2)` **tres veces**. El número de llamadas sigue `L(n) = L(n-1) + L(n-2) + 1`, que es `Θ(φⁿ) ≈ Θ(1.618ⁿ)`. Para `n = 40` son más de 100 millones de llamadas.

**Medición real.**

| n | Llamadas (aprox.) | Tiempo ingenuo |
|---|-------------------|----------------|
| 25 | ~242,785 | milisegundos |
| 30 | ~2.7 millones | ~0.3 s |
| 35 | ~29.8 millones | ~3 s |
| 40 | ~331 millones | ~35 s |

**Solución 1: memoización (top-down).**

```python
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:
        return memo[n]                 # ← ya calculado, no recalcular
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

Cada valor se calcula **una sola vez** y se guarda. Recurrencia: `T(n) = T(n-1) + O(1)` → **O(n)** tiempo, O(n) espacio.

**Solución 2: tabulación (bottom-up).**

```python
def fib_bottom_up(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b                 # solo dos variables
    return b
```

**O(n) tiempo, O(1) espacio.** No usa recursión ni memoria auxiliar.

**Comparación de las tres versiones:**

| Versión | Tiempo | Espacio | Recursión |
|---------|--------|---------|-----------|
| Ingenua | `Θ(φⁿ)` — inviable | `Θ(n)` | Sí |
| Memoización | `Θ(n)` | `Θ(n)` | Sí |
| Tabulación | `Θ(n)` | `Θ(1)` | No |

**Lección que trasciende a Fibonacci.** El problema no era la recursión: era **recalcular lo mismo**. La memoización arregla eso sin abandonar la recursión. Esa idea (guardar resultados de subproblemas) es la programación dinámica, y se usa en Knapsack (sección 4.5).

**Ejercicios relacionados:** `ejercicios/fibonacci.py`, `ejercicios/fibonacci_memo.py`, `ejercicios/fibonacci_bottom_up.py`.

### 2.4 Máximo común divisor (Euclides)

**Definición.** `mcd(a, b)` es el mayor entero que divide a ambos.

**Recurrencia (algoritmo de Euclides).** `mcd(a, b) = mcd(b, a mod b)`, con `mcd(a, 0) = a`.

**Estrategia.** La idea clave: cualquier divisor común de a y b también divide a `a mod b`, así que el problema se reduce al par `(b, a mod b)`, estrictamente menor.

```python
def mcd(a, b):
    if b == 0:
        return a
    return mcd(b, a % b)
```

**Traza de `mcd(48, 18)`:**

| Llamada | (a, b) | a mod b | Siguiente |
|---------|--------|---------|-----------|
| `mcd(48,18)` | (48,18) | 12 | `mcd(18,12)` |
| `mcd(18,12)` | (18,12) | 6 | `mcd(12,6)` |
| `mcd(12,6)` | (12,6) | 0 | `mcd(6,0)` |
| `mcd(6,0)` | (6,0) | — | retorna 6 |

**Análisis.** Cada dos pasos, el segundo argumento se reduce al menos a la mitad (Lema de Lamé). Luego **O(log min(a,b))** pasos. Para `a, b` de 64 bits, como máximo ~90 pasos.

**Demostración de corrección (bosquejo).** Si `d` divide a `a` y a `b`, entonces divide a `a - qb = a mod b`. Recíprocamente, si `d` divide a `b` y a `a mod b`, divide a `qb + (a mod b) = a`. Luego el conjunto de divisores comunes es idéntico en ambos pares, y el mayor también. ∎

### 2.5 Otras funciones recursivas notables

**Suma de dígitos.**

```python
def suma_digitos(n):
    if n < 10:
        return n
    return n % 10 + suma_digitos(n // 10)
```

Estrategia: separar el último dígito (`n % 10`) y recurrir sobre el resto (`n // 10`). O(log n) pasos, porque el número de dígitos es logarítmico.

**Coeficiente binomial (triángulo de Pascal).**

```python
def combinatorio(n, k):
    if k == 0 or k == n:
        return 1
    return combinatorio(n - 1, k - 1) + combinatorio(n - 1, k)
```

Corresponde a la identidad `C(n,k) = C(n-1,k-1) + C(n-1,k)`. La versión ingenua recalcula mucho (mismo problema que Fibonacci); con memoización baja a O(n·k). La fórmula cerrada `n! / (k!(n-k)!)` es O(1) si se precalculan factoriales.

**Función de Ackermann (advertencia).**

```python
def ackermann(m, n):
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))
```

Función recursiva total (siempre termina) pero **no primitiva recursiva**: crece más rápido que cualquier función primitiva recursiva. `ackermann(3, 4) = 125`, pero `ackermann(4, 2)` ya tiene 19,729 dígitos. Se menciona como muestra de que "recursivo" no implica "eficiente".

---

## 3. Recursión con estructuras de datos

### 3.1 Listas: el patrón cabeza + cola

**Estrategia.** Una lista no vacía se descompone en dos partes: la **cabeza** (primer elemento) y la **cola** (resto). Si el problema sobre la cola ya está resuelto, combinarlo con la cabeza da la solución completa.

```python
def suma(lista):
    if not lista:              # lista vacía = caso base
        return 0
    return lista[0] + suma(lista[1:])   # cabeza + solución de la cola
```

**Traza de `suma([1, 2, 3])`:**

| Llamada | lista | Cabeza | Cola | Cálculo |
|---------|-------|--------|------|---------|
| `s([1,2,3])` | [1,2,3] | 1 | [2,3] | `1 + s([2,3])` |
| `s([2,3])` | [2,3] | 2 | [3] | `2 + s([3])` |
| `s([3])` | [3] | 3 | [] | `3 + s([])` |
| `s([])` | [] | — | — | 0 (base) |

Al desapilar: `3+0=3`, `2+3=5`, `1+5=6`.

**Problema de rendimiento oculto.** `lista[1:]` crea una **copia nueva** de la cola: O(n) por llamada, O(n²) total. Para listas grandes eso es inaceptable.

**Solución: recursión con índice.**

```python
def suma_indice(lista, i=0):
    if i >= len(lista):
        return 0
    return lista[i] + suma_indice(lista, i + 1)
```

Aquí no se copia nada: O(n) total. La profundidad sigue siendo O(n).

**En la programación funcional.** En LISP (y por herencia en Scheme), este patrón es primitivo: `car` devuelve la cabeza y `cdr` la cola. Toda la recursión sobre listas se construye sobre esos dos operadores. Python no los tiene, pero `lista[0]` y `lista[1:]` los emulan (con el costo de copia mencionado).

**Demostración de corrección (inducción sobre la longitud).**

*Caso base:* lista vacía. La suma es 0, y la función retorna 0.

*Hipótesis:* `suma(cola)` retorna la suma de la cola.

*Paso:* `suma(lista) = lista[0] + suma(cola) = lista[0] + suma(cola)` por hipótesis, que es exactamente la suma de todos los elementos. ∎

**Ejercicio relacionado:** `ejercicios/suma_lista.py`.

### 3.2 Listas anidadas

**Problema.** Una lista puede contener otras listas, a profundidad arbitraria:

```python
[1, [2, 3], [4, [5, 6]]]
```

**Estrategia.** Recorrer cada elemento. Si es una lista, recurrir; si es un número, sumarlo. La estructura es recursiva, luego el algoritmo debe serlo.

```python
def suma_anidada(lista):
    total = 0
    for elemento in lista:
        if isinstance(elemento, list):
            total += suma_anidada(elemento)   # subproblema del mismo tipo
        else:
            total += elemento
    return total
```

**Traza de `suma_anidada([1, [2, 3]])`:**

| Llamada | Elemento | ¿Lista? | Acción |
|---------|----------|---------|--------|
| `sn([1,[2,3]])` | 1 | No | total = 1 |
| `sn([1,[2,3]])` | [2,3] | **Sí** | llama `sn([2,3])` |
| ↳ `sn([2,3])` | 2 | No | total = 2 |
| ↳ `sn([2,3])` | 3 | No | total = 5, retorna 5 |
| `sn([1,[2,3]])` | — | — | 1 + 5 = 6 |

**Dónde aparece en el mundo real.** Exactamente así funcionan los parsers de JSON y XML: la estructura es un valor, o una lista de valores, o un diccionario de valores. La recursión es la única forma natural de procesarla. También se usa en sistemas de archivos (un directorio contiene archivos y otros directorios).

**Ejercicio relacionado:** `ejercicios/lista_anidada.py`.

### 3.3 Matrices

**Problema.** Recorrer todos los elementos de una matriz (lista de listas).

**Estrategia.** Tratar la matriz como una lista de filas: recurrir sobre filas, y dentro de cada fila recorrer las columnas. Dos enfoques equivalentes:

```python
# Enfoque 1: dos parámetros (fila, columna)
def recorrer(matriz, fila=0, col=0):
    if fila >= len(matriz):
        return
    if col >= len(matriz[0]):
        recorrer(matriz, fila + 1, 0)     # siguiente fila
        return
    print(matriz[fila][col], end=" ")
    recorrer(matriz, fila, col + 1)       # siguiente columna

# Enfoque 2: aprovechar que la matriz es una lista de listas
def recorrer_filas(matriz, i=0):
    if i >= len(matriz):
        return
    imprimir_lista(matriz[i])             # recorrido lineal de la fila
    recorrer_filas(matriz, i + 1)
```

**Aplicaciones reales de recursión sobre matrices:**
- Multiplicación de matrices con el algoritmo de Strassen (divide y vencerás, O(n^2.81))
- Rotación de matrices por capas recursivas
- Detección de patrones (una matriz contiene a otra)
- Recorrido en espiral

**Nota sobre eficiencia.** Para recorridos simples, la iteración doble es preferible: menos overhead y mejor localidad de caché (sección 9 de fundamentos). La recursión sobre matrices se reserva para algoritmos que realmente se benefician de dividir (Strassen) o donde la claridad importa más que la velocidad.

**Ejercicio relacionado:** `ejercicios/recorrido_matriz.py`.

### 3.4 Recursión mutua

Dos o más funciones se llaman entre sí formando un ciclo.

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

**Estrategia.** Un problema par se reduce a un problema impar de tamaño menor, y viceversa. El caso base está en ambas funciones.

**Dónde aparece.** En compiladores: el parser de expresiones aritméticas usa recursión mutua (`expresión → término → factor → expresión`). También en máquinas de estado y en la validación de estructuras anidadas (JSON, HTML).

**Riesgo.** Es más fácil perder de vista el caso base y crear un ciclo infinito. Al escribir recursión mutua, hay que verificar que **alguna** de las funciones del ciclo tenga un caso base alcanzable.

### 3.5 Recursión en árboles y grafos (adelanto)

La recursión brilla cuando la estructura de datos es recursiva por definición. El caso base ya no es "lista vacía" sino "subárbol nulo" o "vértice sin vecinos". El tema 03 desarrolla esto a fondo; aquí basta la idea central:

```python
def recorrer(nodo):
    if nodo is None:          # caso base: subárbol vacío
        return
    recorrer(nodo.izquierdo)
    recorrer(nodo.derecho)
```

Observe que es exactamente el patrón cabeza+cola de la sección 3.1, con dos colas en vez de una. **La recursión sobre listas y la recursión sobre árboles son el mismo patrón.** Entender esto deja los temas 03 y 04 prácticamente resueltos de antemano.

---

## 4. Vuelta atrás recursiva (Backtracking)

### 4.1 Concepto y diferencia con la recursión pura

El **backtracking** (vuelta atrás) es una técnica de búsqueda que construye soluciones **incrementalmente** y abandona una solución parcial en cuanto determina que no puede completarse.

La diferencia con la recursión pura es sutil pero fundamental:

| Recursión pura | Backtracking |
|----------------|--------------|
| Divide el problema en subproblemas **independientes** | Explora opciones **secuencialmente** sobre un estado compartido |
| Cada subproblema se resuelve una vez | El mismo subproblema puede explorarse con distintos estados |
| No hay "deshacer" | **Deshacer** es la operación característica |
| Ejemplo: Merge Sort, Fibonacci | Ejemplo: N reinas, laberintos, Sudoku |

La clave: el backtracking **muta** un estado, explora, y luego **restaura** el estado. Por eso depende críticamente de que las variables sean referencias compartidas (sección 9.2 de fundamentos).

### 4.2 Plantilla general

```python
def backtrack(estado):
    # 1. ¿Solución completa?
    if es_completa(estado):
        registrar_solucion(estado)
        return

    # 2. Probar cada opción disponible
    for opcion in opciones_validas(estado):
        if es_segura(opcion, estado):       # poda
            aplicar(opcion, estado)         # HACER
            backtrack(estado)               # EXPLORAR
            deshacer(opcion, estado)        # DESHACER  ← el backtracking
```

Las tres operaciones HACER / EXPLORAR / DESHACER son la firma del algoritmo. La función `es_segura` implementa la **poda**: descarta ramas que no pueden llevar a solución.

**Analogía.** Buscar la salida de un laberinto tocando siempre la pared con la mano derecha. Avanzas (hacer), si encuentras un callejón sin salida vuelves a la última bifurcación (deshacer) y pruebas el otro camino. Nunca marcas el camino recorrido como permanente.

### 4.3 Por qué funciona la poda

La poda es lo que hace el backtracking viable. Sin ella, sería fuerza bruta: `O(n!)` o peor. Con ella, se descartan ramas completas del árbol de búsqueda.

**Cuantificación para las N reinas.** Sin poda habría que probar `nⁿ` colocaciones (n opciones por columna, n columnas). Con la poda de diagonales y filas, para n = 8 se exploran unos pocos miles de nodos en vez de 16 millones. La poda no cambia la complejidad asintótica del peor caso, pero cambia todo en la práctica.

### 4.4 Problema de las N reinas

**Historia.**
- **1848:** Max Bezzel, matemático alemán, plantea el problema de las 8 reinas.
- **1850:** Franz Nauck publica la primera solución.
- **1969-1970s:** Se convierte en el problema canónico para enseñar backtracking.

**Definición.** Colocar N reinas en un tablero de N×N sin que ninguna ataque a otra. Dos reinas se atacan si comparten **fila**, **columna** o **diagonal**.

**Estrategia.** Colocar las reinas **columna por columna**. En cada columna, probar cada fila. Como cada reina va en una columna distinta, las columnas nunca colisionan; solo hay que verificar filas y diagonales. Esto reduce el espacio de búsqueda de `nⁿ` a `n!`.

**¿Por qué columna por columna y no casilla por casilla?** Porque reduce el factor de ramificación. Con columnas, en la columna k hay como máximo n-k opciones reales (las anteriores ya están ocupadas). Es la diferencia entre explorar `nⁿ` y `n!` configuraciones.

**Verificación de seguridad.**

Como las reinas se colocan **columna por columna**, dos reinas nunca comparten columna. Las colisiones posibles son: misma **fila** (una reina ya colocada en esa fila, en una columna anterior) y las dos **diagonales** que bajan desde posición actual hacia columnas anteriores (arriba-izquierda y abajo-izquierda).

```python
def es_segura(tablero, fila, col, n):
    """¿Es seguro colocar una reina en (fila, col)?"""
    # 1. Misma fila: revisar las columnas ya ocupadas (0 .. col-1)
    for j in range(col):
        if tablero[fila][j] == 1:
            return False
    # 2. Diagonal arriba-izquierda
    for i, j in zip(range(fila, -1, -1), range(col, -1, -1)):
        if tablero[i][j] == 1:
            return False
    # 3. Diagonal abajo-izquierda
    for i, j in zip(range(fila, n, 1), range(col, -1, -1)):
        if tablero[i][j] == 1:
            return False
    return True
```

**Error clásico (y su porqué).** Verificar la columna con `for i in range(fila)` parece razonable, pero es inútil: como se coloca exactamente una reina por columna, la columna actual está vacía por construcción. Lo que hay que verificar es la **fila** (que se repite entre columnas). Y hay que recorrer **ambas** diagonales hacia la izquierda, no solo la que sube. Con solo una de las dos, se cuelan reinas que se atacan.

**Solución completa.**

```python
def resolver(tablero, col, n):
    if col >= n:                    # todas las columnas cubiertas
        return True
    for fila in range(n):
        if es_segura(tablero, fila, col, n):
            tablero[fila][col] = 1          # HACER
            if resolver(tablero, col + 1, n):
                return True                  # encontrada, no seguir
            tablero[fila][col] = 0          # DESHACER
    return False
```

**Traza parcial para n = 4** (columna 0, filas 0 y 1):

| Paso | Acción | Estado |
|------|--------|--------|
| 1 | Colocar reina en (0,0) | col 0: fila 0 |
| 2 | Intentar col 1: fila 0 → atacada | retroceder |
| 3 | Intentar col 1: fila 1 → segura | col 0: fila 0, col 1: fila 1 |
| 4 | Intentar col 2: todas atacadas | ambas reinas quedaron mal |
| 5 | **Backtracking:** quitar reina de col 1 | col 0: fila 0 |
| 6 | Intentar col 1: fila 2 → segura | col 0: fila 0, col 1: fila 2 |
| ... | continúa | |

**Número de soluciones:**

| N | Soluciones |
|---|------------|
| 1 | 1 |
| 4 | 2 |
| 5 | 10 |
| 6 | 4 |
| 7 | 40 |
| 8 | 92 |
| 10 | 724 |
| 12 | 14,200 |

**Análisis de coste.** Peor caso `O(N!)`, pero con la poda el número real de nodos explorados es mucho menor. No se conoce una fórmula cerrada; la sucesión está en el OEIS como A000170.

**Ejercicio relacionado:** `ejercicios/n_reinas.py`.

### 4.5 Problema de la mochila (Knapsack)

**Definición.** Dados n objetos, cada uno con peso `wᵢ` y valor `vᵢ`, y una mochila de capacidad W, seleccionar el subconjunto de objetos que **maximice el valor total** sin exceder W.

**Estrategia por backtracking.** Para cada objeto hay exactamente dos opciones: **incluirlo** o **no incluirlo**. Eso da un árbol binario de `2ⁿ` hojas.

```python
def knapsack(pesos, valores, capacidad):
    n = len(pesos)
    mejor = {"valor": 0, "seleccion": []}

    def backtrack(i, peso_actual, valor_actual, seleccion):
        if i == n:                              # se decidió por todos
            if valor_actual > mejor["valor"]:
                mejor["valor"] = valor_actual
                mejor["seleccion"] = seleccion[:]
            return
        # Opción A: NO incluir el objeto i
        backtrack(i + 1, peso_actual, valor_actual, seleccion)
        # Opción B: incluirlo, si cabe
        if peso_actual + pesos[i] <= capacidad:
            seleccion.append(i)                 # HACER
            backtrack(i + 1, peso_actual + pesos[i],
                      valor_actual + valores[i], seleccion)
            seleccion.pop()                     # DESHACER

    backtrack(0, 0, 0, [])
    return mejor["valor"], mejor["seleccion"]
```

**Poda aplicable.** Si incluso tomando **todos** los objetos restantes no se supera el mejor valor actual, se puede cortar la rama. Con esa poda el backtracking se acerca a la solución óptima mucho antes.

**Complejidad.** `O(2ⁿ)` sin poda, `O(n·W)` con programación dinámica. La versión con DP es la que se usa en la práctica; el backtracking se enseresa porque generaliza a problemas donde la DP no aplica (restricciones complejas).

**Relación con la programación dinámica.** Knapsack tiene **subproblemas superpuestos** (el mismo `(i, capacidad restante)` se alcanza por muchos caminos). Es exactamente el caso donde la memoización transforma un `O(2ⁿ)` en `O(n·W)`. Es la misma lección que Fibonacci, pero con estado de dos dimensiones.

**Ejercicio relacionado:** `ejercicios/knapsack.py`.

### 4.6 Otros problemas clásicos de backtracking

| Problema | Estado | Poda |
|----------|--------|------|
| **Generar permutaciones** | Lista usada + permutación parcial | Ninguna (se quieren todas) |
| **Subconjuntos que sumen k** | Suma parcial | Podar si la suma ya excede k |
| **Laberinto** | Posición + visitados | No revisitar celdas |
| **Sudoku** | Tablero parcial | Validar fila, columna y caja |
| **Coloreo de grafos** | Colores asignados | Dos adyacentes no comparten color |

El generador de permutaciones es el más instructivo porque es backtracking **sin poda**: se quieren todas las soluciones, no una. Es el patrón que aparece en `ejercicios/permutaciones.py`.

---

## 5. Torres de Hanói

### 5.1 Historia y reglas

Inventado por el matemático francés **Édouard Lucas** en 1883.

**Reglas:**
1. Solo se mueve un disco a la vez.
2. Un disco grande nunca puede colocarse sobre uno más pequeño.
3. Solo se puede mover el disco superior de una torre.

**La leyenda.** Un monasterio tiene tres agujas de diamante y 64 discos de oro. Los monjes los mueven según las reglas; cuando terminen, se acaba el mundo. Con la solución óptima se necesitan `2⁶⁴ - 1 ≈ 1.8 × 10¹⁹` movimientos. A un segundo por movimiento, unos **585,000 millones de años**.

### 5.2 Estrategia

La solución recursiva se basa en una observación: para mover n discos del origen al destino, hay que:

1. Liberar el disco más grande (el n), que está en el fondo. Para eso, mover los **n-1 discos de arriba** al auxiliar.
2. Mover el disco n directamente al destino.
3. Mover los n-1 discos del auxiliar al destino, encima del disco n.

Los pasos 1 y 3 son el **mismo problema con n-1 discos**. Esa es la recursión.

```python
def torres_hanoi(n, origen="A", destino="C", auxiliar="B"):
    if n == 1:
        print(f"Mover disco 1 de {origen} a {destino}")
        return 1
    movimientos = 0
    # Paso 1: liberar el disco grande
    movimientos += torres_hanoi(n - 1, origen, auxiliar, destino)
    # Paso 2: mover el disco grande
    print(f"Mover disco {n} de {origen} a {destino}")
    movimientos += 1
    # Paso 3: reubicar los n-1 sobre el grande
    movimientos += torres_hanoi(n - 1, auxiliar, destino, origen)
    return movimientos
```

### 5.3 Traza de `torres_hanoi(3)`

| Llamada | n | Acción |
|---------|---|--------|
| `h(3)` | 3 | → `h(2, A→B)` |
| ↳ `h(2,A→B)` | 2 | → `h(1, A→C)` |
| ↳↳ `h(1,A→C)` | 1 | **Mueve disco 1: A→C** |
| ↳ `h(2,A→B)` | 2 | **Mueve disco 2: A→B** |
| ↳ `h(2,A→B)` | 2 | → `h(1, C→B)` |
| ↳↳ `h(1,C→B)` | 1 | **Mueve disco 1: C→B** |
| `h(3)` | 3 | **Mueve disco 3: A→C** |
| `h(3)` | 3 | → `h(2, B→C)` |
| ↳ `h(2,B→C)` | 2 | → `h(1, B→A)` |
| ↳↳ `h(1,B→A)` | 1 | **Mueve disco 1: B→A** |
| ↳ `h(2,B→C)` | 2 | **Mueve disco 2: B→C** |
| ↳ `h(2,B→C)` | 2 | → `h(1, A→C)` |
| ↳↳ `h(1,A→C)` | 1 | **Mueve disco 1: A→C** |

Total: 7 movimientos.

### 5.4 Análisis

**Recurrencia.** `T(n) = 2·T(n-1) + 1`, con `T(1) = 1`.

Resolviendo por sustitución:

```
T(n)   = 2T(n-1) + 1
       = 2[2T(n-2) + 1] + 1 = 4T(n-2) + 2 + 1
       = 4[2T(n-3) + 1] + 2 + 1 = 8T(n-3) + 4 + 2 + 1
       = ...
       = 2^(n-1)·T(1) + (2^(n-1) - 1)
       = 2^(n-1) + 2^(n-1) - 1
       = 2^n - 1
```

**Resultado: `T(n) = 2ⁿ - 1`.** Está **demostrado** que es el número mínimo (no existe solución con menos movimientos): cualquier algoritmo necesita al menos eso.

**Coste:**
- Tiempo: `Θ(2ⁿ)` — imparable para n ≥ 30.
- Espacio: `Θ(n)` de pila (la profundidad es n).

### 5.5 Generalización: cuatro torres (Frame-Stewart)

Con 4 torres en vez de 3, se conoce un algoritmo (Frame-Stewart, 1941) que es más eficiente, pero **no se ha demostrado** que sea óptimo para todo n. Es uno de los problemas abiertos más famosos de la matemática recreativa. Buen recordatorio de que "recursivo" y "óptimo" son cuestiones separadas.

### 5.6 Por qué Hanói es el ejemplo perfecto de recursión

1. La solución recursiva es **corta** (10 líneas) y **evidente** una vez que se ve la idea.
2. La versión iterativa es posible pero considerablemente más larga y difícil de entender.
3. La recurrencia se resuelve limpiamente a forma cerrada.
4. Demuestra que `2ⁿ - 1` es óptimo, no solo una cota.

**Ejercicio relacionado:** `ejercicios/torres_hanoi.py`.

---

## 6. Análisis de recursiones: métodos aplicados

La sección 7 de `00-fundamentos` desarrolla los tres métodos con detalle general. Aquí se aplican a las recurrencias específicas de este tema.

### 6.1 Las recurrencias del tema

| Función | Recurrencia | Solución | Método |
|---------|-------------|----------|--------|
| Factorial | `T(n) = T(n-1) + O(1)` | `Θ(n)` | Directo |
| Potencia ingenua | `T(e) = T(e-1) + O(1)` | `Θ(e)` | Directo |
| Potencia eficiente | `T(e) = T(e/2) + O(1)` | `Θ(log e)` | Teorema Maestro |
| Fibonacci ingenuo | `T(n) = T(n-1) + T(n-2) + O(1)` | `Θ(φⁿ)` | Ecuación característica |
| Fibonacci memoizado | `T(n) = T(n-1) + O(1)` | `Θ(n)` | Directo |
| Torres de Hanói | `T(n) = 2T(n-1) + O(1)` | `Θ(2ⁿ)` | Sustitución |
| Búsqueda binaria | `T(n) = T(n/2) + O(1)` | `Θ(log n)` | Teorema Maestro |

### 6.2 Fibonacci: por qué `Θ(φⁿ)`

La recurrencia `T(n) = T(n-1) + T(n-2) + 1` es una ecuación en diferencias lineal. Su solución homogénea tiene la forma `T(n) = A·φⁿ + B·ψⁿ`, donde φ ≈ 1.618 (razón áurea) y ψ ≈ -0.618 son las raíces de `x² = x + 1`. Como `|ψ| < 1`, el término `B·ψⁿ` se desvanece y domina `A·φⁿ`. Luego **Θ(φⁿ)**.

**Nota irónica:** la recurrencia del costo de Fibonacci es la misma que la de Fibonacci mismo. No es coincidencia: el árbol de llamadas tiene forma de árbol de Fibonacci.

### 6.3 Cuándo la recursión es una mala idea

| Situación | Problema | Alternativa |
|-----------|----------|-------------|
| Profundidad > ~10,000 | `RecursionError` | Versión iterativa |
| Subproblemas superpuestos | Recalcular (Fibonacci, Knapsack) | Memoización |
| Recorrido lineal simple | Overhead innecesario | Bucle |
| Estado enorme por marco | Presión de memoria | Iteración con estado explícito |
| Rendimiento crítico | Llamadas a función | Iteración |

**Regla general:** la recursión es una herramienta de **claridad**, no de velocidad. Se usa cuando hace el código más evidente, y se abandona cuando el coste es inaceptable.

---

## 7. Programación dinámica: el siguiente nivel

La **programación dinámica** (DP) no es un tema separado: es recursión con memoria. Aplica cuando un problema tiene:

1. **Subestructura óptima:** la solución óptima se construye con soluciones óptimas de subproblemas.
2. **Subproblemas superpuestos:** los mismos subproblemas aparecen múltiples veces.

Las dos implementaciones:

| Enfoque | Cómo | Ventaja | Desventaja |
|---------|------|---------|------------|
| **Top-down (memoización)** | Recursión + caché | Solo calcula lo necesario; fácil de escribir | Overhead de recursión |
| **Bottom-up (tabulación)** | Iteración de lo pequeño a lo grande | Sin recursión; mejor localidad | Calcula todo, incluso lo no usado |

**Aplicación a Fibonacci** (sección 2.3) y **a Knapsack** (sección 4.5). El patrón es siempre el mismo:

```python
# 1. Identificar el estado: (i, capacidad_restante)
# 2. Definir la recurrencia entre estados
# 3. Elegir top-down (dict) o bottom-up (tabla)
# 4. Caso base y orden de llenado
```

Este patrón se retoma en el tema 06 (grandes datos), donde la memoria deja de ser gratis.

---

## 8. Resumen del tema

| Concepto | Idea central | Dónde se usa después |
|----------|--------------|----------------------|
| Caso base + reducción | Toda recursión necesita terminar | Todos los temas |
| Pila de llamadas | Cada llamada cuesta un marco | Límite de recursión, recorridos iterativos (03) |
| Patrón cabeza+cola | Listas y árboles se recorren igual | Árboles (03), grafos (04) |
| Divide y vencerás | Partir el problema a la mitad | Merge/Quick Sort (02), potencia, Hanoi |
| Hacer / Explorar / Deshacer | Backtracking | Grafos (04), laberintos |
| Memoización | No recalcular subproblemas | Knapsack, grandes datos (06) |

**Los tres errores más frecuentes al aprender recursividad:**

1. **Caso base inalcanzable.** La reducción no garantiza llegar a él. Síntoma: `RecursionError` inmediato.
2. **No usar la hipótesis inductiva al demostrar corrección.** La demostración se vuelve circular o vacía.
3. **Confundir número de llamadas con profundidad.** El tiempo depende de la primera; la memoria, de la segunda.

---

## Bibliografía anotada

1. **Cormen, T. H., Leiserson, C. E., Rivest, R. L. & Stein, C.** *Introduction to Algorithms*, III ed. MIT Press, 2009. — Capítulo 4 (Divide and Conquer) para el método de sustitución y el Teorema Maestro.
2. **Goodrich, M. T., Tamassia, R. & Goldwasser, M. H.** *Data Structures & Algorithms in Python*. Wiley, 2013. — Capítulo 4 (Recursion), el más cercano al nivel del curso.
3. **Weiss, M. A.** *Data Structures & Algorithm Analysis in C++*, III ed. Addison Wesley, 2006. — Capítulo 7, sección de recursión y análisis de recurrencias.
4. **Abelson, H. & Sussman, G. J.** *Structure and Interpretation of Computer Programs*, II ed. MIT Press, 1996. — Capítulo 1: el tratamiento más profundo de recursión vs iteración.
5. **Knuth, D. E.** *The Art of Computer Programming*, Vol. 1. Addison-Wesley, 1997. — Sección 1.2.1 sobre inducción matemática.
6. **Levitin, A.** *Introduction to the Design and Analysis of Algorithms*, III ed. Pearson, 2011. — Capítulo 8: el tratamiento más claro de backtracking.
7. **Horowitz, E. & Sahni, S.** *Fundamentals of Computer Algorithms*. Computer Science Press, 1978. — Capítulo 5: backtracking y poda.

## Recursos utilizados

- MIT OpenCourseWare — 6.006: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/
- MIT OpenCourseWare — 6.042J Mathematics for Computer Science (inducción): https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/
- Brilliant.org — Backtracking: https://brilliant.org/wiki/recursion-backtracking/
- OEIS A000170 (número de soluciones de las N reinas): https://oeis.org/A000170
- Python Documentation — `sys.setrecursionlimit`: https://docs.python.org/3/library/sys.html#sys.setrecursionlimit




