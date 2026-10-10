# Teoría: Procesamiento de Grandes Cantidades de Datos

---

## 1. El problema

### 1.1 Definición

El procesamiento de grandes volúmenes de datos (*big data*) aborda situaciones donde el conjunto de datos:
- Es demasiado grande para caber en la memoria RAM del proceso.
- O es demasiado grande para procesarse eficientemente con algoritmos ingenuos.

No se trata solo de tamaño: 10 GB de datos con un algoritmo O(n²) es peor que 100 GB con uno O(n).

### 1.2 La jerarquía de memoria

| Nivel | Latencia típica | Capacidad típica | Acceso |
|-------|-----------------|------------------|--------|
| Registros de CPU | ~0.3 ns | Bytes | Directo |
| Caché L1 | ~1 ns | 32-64 KB | Directo |
| Caché L2 | ~4 ns | 256 KB - 1 MB | Directo |
| Caché L3 | ~20 ns | 8-32 MB | Directo |
| Memoria RAM | ~100 ns | 8-64 GB | Aleatorio |
| SSD NVMe | ~100 µs | 256 GB - 2 TB | Por bloques |
| Disco HDD | ~10 ms | 1-20 TB | Por bloques, busca |
| Red (misma región) | ~500 µs | Ilimitado | Protocolo |

**Dato clave:** la diferencia entre RAM y disco es de aproximadamente **100,000×** en latencia. Un algoritmo que minimiza accesos a disco puede superar por órdenes de magnitud a uno con "mejor" complejidad en RAM.

### 1.3 Las dimensiones del problema (las "V" del big data)

- **Volumen:** terabytes o petabytes.
- **Velocidad:** datos que llegan en streaming continuo.
- **Variedad:** texto, binario, estructurado, no estructurado.
- **Veracidad:** ruido, inconsistencias, valores faltantes.
- **Valor:** el objetivo final es extraer información útil.

---

## 2. Técnica fundamental: procesamiento por streaming

### 2.1 Concepto

En vez de cargar todo el conjunto de datos en memoria, se procesa un elemento (o un bloque) a la vez, manteniendo solo un estado agregado.

### 2.2 Antipatrón vs patrón correcto

```python
# MAL: carga todo el archivo en memoria
with open("ventas.csv") as f:
    lineas = f.readlines()          # ¡200 millones de strings en RAM!
total = sum(float(l.split(",")[2]) for l in lineas[1:])

# BIEN: procesa línea por línea
total = 0.0
with open("ventas.csv") as f:
    next(f)                          # saltar encabezado
    for linea in f:                 # una línea en memoria a la vez
        total += float(linea.split(",")[2])
```

La diferencia no es de complejidad asintótica: ambas son O(n) en tiempo. La diferencia es O(n) versus O(1) en memoria.

### 2.3 Generadores en Python

```python
def leer_registros(ruta):
    with open(ruta) as f:
        for linea in f:
            yield procesar(linea)    # produce un registro a la vez

# Consumo perezoso: nunca todos los datos en memoria
total = sum(r["monto"] for r in leer_registros("ventas.csv"))
```

Los generadores permiten encadenar transformaciones sin materializar resultados intermedios.

---

## 3. Ordenamiento externo (External Sort)

### 3.1 El problema

Ordenar N elementos cuando N no cabe en memoria de tamaño M.

Con Quick Sort o Merge Sort en memoria: imposible o inviable. Con acceso aleatorio a disco: cada acceso cuesta ~10 ms; O(N log N) accesos aleatorios serían catastróficos.

### 3.2 El algoritmo

**Fase 1 — Dividir y ordenar (runs):**
1. Leer bloques de M elementos.
2. Ordenar cada bloque en memoria (Quick Sort es ideal aquí: acceso aleatorio rápido, todo en RAM).
3. Escribir cada bloque ordenado a un archivo temporal en disco.

Resultado: `⌈N/M⌉` archivos temporales, cada uno ordenado internamente.

**Fase 2 — Mezclar (merge):**
1. Mezclar los archivos temporales con una **mezcla de k vías** usando un heap.
2. El heap contiene un elemento de cada archivo; se extrae el mínimo y se reemplaza por el siguiente elemento de ese archivo.
3. El resultado se escribe secuencialmente al archivo final.

**¿Por qué funciona?** La mezcla lee cada archivo **secuencialmente**, que es el modo de acceso más rápido en disco. No hay accesos aleatorios.

### 3.3 Análisis de costo

- **Fase 1:** Se leen y escriben N elementos una vez cada uno: 2N operaciones de E/S.
- **Fase 2:** Se leen N elementos y se escriben N: otras 2N operaciones.
- **Total:** aproximadamente 4N operaciones de E/S secuenciales.

Comparación con Merge Sort de 2 vías sobre disco: `log(N/M)` pasadas × 2N lecturas/escrituras. Con k-vías balanceado se minimiza el número de pasadas.

**Paralelización:** la Fase 1 es trivialmente paralela — cada bloque se ordena en un proceso/núcleo independiente. La Fase 2 puede paralelizarse particionando el rango de claves (cada trabajador toma un rango).

### 3.4 Implementación de referencia

```python
import heapq, tempfile, os

def ordenamiento_externo(entrada, salida, bloque=10000):
    temporales = []
    with open(entrada) as f:
        while True:
            datos = []
            for _ in range(bloque):
                linea = f.readline()
                if not linea:
                    break
                datos.append(int(linea))
            if not datos:
                break
            datos.sort()
            temp = tempfile.NamedTemporaryFile("w+", delete=False)
            temp.writelines(f"{d}\n" for d in datos)
            temp.close()
            temporales.append(temp.name)

    archivos = [open(t) for t in temporales]
    heap = []
    for i, a in enumerate(archivos):
        linea = a.readline()
        if linea:
            heapq.heappush(heap, (int(linea), i))

    with open(salida, "w") as out:
        while heap:
            valor, i = heapq.heappop(heap)
            out.write(f"{valor}\n")
            linea = archivos[i].readline()
            if linea:
                heapq.heappush(heap, (int(linea), i))

    for a in archivos:
        a.close()
    for t in temporales:
        os.unlink(t)
```

---

## 4. Técnicas complementarias

### 4.1 Escritura con búfer

Las llamadas al sistema operativo tienen costo fijo. Agrupar escrituras en búferes de 4-64 KB mejora dramáticamente el rendimiento.

```python
with open("salida.txt", "w", buffering=8192) as f:   # búfer de 8 KB
    buffer = []
    for i in range(1000000):
        buffer.append(f"linea {i}\n")
        if len(buffer) >= 1000:
            f.writelines(buffer)      # una llamada por 1000 líneas
            buffer.clear()
    if buffer:
        f.writelines(buffer)
```

### 4.2 Compresión

Comprimir datos antes de escribir reduce el volumen de E/S, que suele ser el cuello de botella. RLE, gzip, zstd. La compresión consume CPU, pero la CPU suele estar ociosa esperando al disco.

### 4.3 Muestreo y aproximación

Para estadísticas sobre conjuntos masivos, no siempre se necesita exactitud:
- **Media/varianza:** algoritmos de un solo paso (Welford) sin almacenar datos.
- **Percentiles:** esbozos probabilísticos (t-digest, GK) con error acotado.
- **Conteo de distintos:** HyperLogLog con ~1% de error usando pocos KB.

### 4.4 Proyección y poda

Procesar solo las columnas necesarias y filtrar temprano reduce el volumen de datos que fluye por el sistema.

---

## 5. De un núcleo a muchos: el siguiente nivel

Cuando una máquina no basta:

| Técnica | Idea |
|---------|------|
| **Multiprocessing** | Dividir el trabajo entre núcleos/máquinas; cada uno procesa una partición |
| **MapReduce** | `map` transforma en paralelo; `shuffle` agrupa por clave; `reduce` agrega. Popularizado por Google (2004) |
| **Procesamiento distribuido** | Hadoop, Spark: distribuyen datos y cómputo en un clúster |
| **Bases de datos analíticas** | Motores columnar (ClickHouse, BigQuery) optimizados para agregaciones masivas |

**Patrón clave en todos:** dividir los datos en particiones independientes, procesar en paralelo, y combinar resultados parciales.

---

## 6. Cuándo usar cada técnica

| Situación | Técnica recomendada |
|-----------|---------------------|
| Archivo que cabe en RAM | Procesamiento directo en memoria |
| Archivo mayor que RAM, operación de una pasada | Streaming / generadores |
| Archivo mayor que RAM, requiere ordenamiento | Ordenamiento externo |
| Escritura masiva de resultados | Búfer grande + writelines |
| Estadísticas sobre datos masivos | Algoritmos de una pasada |
| Agregaciones repetidas sobre los mismos datos | Índices o base de datos |
| Ninguna máquina basta | Procesamiento distribuido (MapReduce/Spark) |

---

## Bibliografía

1. **Cormen, T. H., Leiserson, C. E., Rivest, R. L. & Stein, C.** *Introduction to Algorithms*, III ed. MIT Press, 2009. — Capítulo 6: Heapsort (mezcla con heap).
2. **Knuth, D. E.** *The Art of Computer Programming*, Vol. 3: Sorting and Searching, II ed. Addison-Wesley, 1998. — Sección 5.4: External Sorting.
3. **Dean, J. & Ghemawat, S.** "MapReduce: Simplified Data Processing on Large Clusters", *OSDI*, 2004. — Paper fundacional de Google.
4. **Kleppmann, M.** *Designing Data-Intensive Applications*. O'Reilly, 2017. — Capítulos 10-11: procesamiento por lotes y streaming.
5. **Zhao, S.** *Big Data: Principles and Paradigms*. Morgan Kaufmann, 2018.

## Recursos utilizados

- MIT OpenCourseWare — 6.046J Design and Analysis of Algorithms: https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/
- GeeksforGeeks — External Sorting: https://www.geeksforgeeks.org/external-sorting/
- Python Documentation — Generators: https://docs.python.org/3/tutorial/classes.html#generators
- Google Research — MapReduce paper: https://research.google/pubs/pub62/
