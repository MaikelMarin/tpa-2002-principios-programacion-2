# Teoría: Procesamiento de Archivos

## Prerequisitos

| Apartado de `00-fundamentos` | Por qué se necesita aquí |
|-------------------------------|--------------------------|
| **8. Estructuras (arreglo)** | Un archivo es una secuencia de bytes; leerlo es como recorrer un arreglo |
| **9. Modelo de memoria** | La diferencia entre RAM y disco explica toda la jerarquía de almacenamiento (§1.2) |
| **10. Python** | `with` (§10.5), excepciones (§10.6), `struct` (§10.7), `collections` (§10.8) |
| **5. Sumatorias** | Para calcular el tamaño de archivos y el coste de lectura |

---

## 1. Sistemas de archivos

### 1.1 Definición

Un **sistema de archivos** es el conjunto de estructuras de datos y algoritmos que un sistema operativo utiliza para organizar, almacenar, nombrar, recuperar y **proteger** la información en un dispositivo de almacenamiento.

Responde a preguntas fundamentales:
- ¿Dónde se guardan físicamente los bytes de un archivo?
- ¿Cómo se traduce un nombre como `documento.txt` a bloques de disco?
- ¿Cómo se evita que dos archivos se sobrescriban?
- ¿Qué pasa si el sistema se apaga a mitad de una escritura?

### 1.2 Evolución histórica

| Año | Hito | Detalle |
|-----|------|---------|
| 1956 | Primer disco duro | IBM RAMAC 350: 5 MB, 24 pulgadas de diámetro, 50 discos |
| 1961 | Primer sistema de archivos | CTSS (MIT): archivos como secuencias de bytes |
| 1965 | Sistema jerárquico | Multics: directorios que contienen subdirectorios |
| 1969 | UNIX | "Todo es un archivo": dispositivo unificado |
| 1972 | I-nodos | UNIX separa metadatos de datos |
| 1977 | FAT12 | Microsoft para MS-DOS |
| 1984 | HFS | Apple: sistema jerárquico para Macintosh |
| 1993 | NTFS | Microsoft: journaling, permisos ACL, archivos dispersos |
| 1993 | ext2 | Linux |
| 2001 | HFS+ | Apple: Unicode, journaling |
| 2006 | ZFS | Sun: checksums, pools de almacenamiento, copy-on-write |
| 2008 | ext4 | Linux: extents, journaling mejorado |
| 2017 | APFS | Apple: optimizado para SSD, snapshots, clones |

### 1.3 Anatomía de un archivo

Un archivo tiene dos partes conceptuales:

**Metadatos** (típicamente en el i-nodo):
- Nombre (vive en el directorio, no en el i-nodo)
- Tamaño en bytes
- Fechas: creación, modificación, acceso
- Permisos de lectura/escritura/ejecución
- Propietario y grupo
- Tipo de archivo
- **Punteros a los bloques de datos**

**Datos:** el contenido real, almacenado en bloques (típicamente de 4 KB).

### 1.4 Estrategias de asignación de bloques

| Método | Descripción | Ventaja | Desventaja |
|--------|-------------|---------|------------|
| **Contigua** | Bloques consecutivos en disco | Acceso secuencial rapidísimo | Fragmentación externa |
| **Enlazada** | Cada bloque apunta al siguiente | Sin fragmentación | Acceso aleatorio lento |
| **Indexada (i-nodo)** | Tabla de punteros a bloques | Acceso aleatorio directo | Tamaño fijo de tabla |
| **Extents** | Rangos contiguos (inicio, longitud) | Eficiente en espacio | Fragmentación si crece disperso |

---

## 2. Archivos de texto vs binarios

### 2.1 Archivos de texto

Secuencia de caracteres codificados (ASCII, UTF-8, Latin-1…).

Propiedades:
- Legibles por humanos.
- Interpretan los saltos de línea (`\n` en Unix, `\r\n` en Windows).
- Independientes de la plataforma (salvo la codificación).

### 2.2 Archivos binarios

Secuencia cruda de bytes.

Propiedades:
- Almacenan datos con formato interno propio (imágenes, audio, ejecutables).
- Más compactos: un entero ocupa 4 bytes, no varios caracteres.
- Requieren conocer el formato para interpretarse.
- Pueden contener bytes nulos, imposibles en archivos de texto.

### 2.3 Codificaciones de caracteres

| Codificación | Bits por carácter | Alcance |
|--------------|-------------------|---------|
| **ASCII** | 7 bits | 128 caracteres (inglés) |
| **Latin-1 (ISO-8859-1)** | 8 bits | 256 (europeo occidental, incluye ñ) |
| **Windows-1252** | 8 bits | Variante de Latin-1 de Microsoft |
| **UTF-8** | 1-4 bytes | Todos los Unicode |
| **UTF-16** | 2 o 4 bytes | Todos los Unicode |
| **UTF-32** | 4 bytes | Todos los Unicode, longitud fija |

**Regla práctica:** especificar siempre `encoding="utf-8"` al abrir archivos de texto en Python. El valor por defecto depende del sistema operativo (locale), lo que produce errores difíciles de depurar.

---

## 3. Lectura y escritura en Python

### 3.1 Modos de apertura

| Modo | Significado |
|------|-------------|
| `'r'` | Lectura. Falla si el archivo no existe |
| `'w'` | Escritura. Sobrescribe o crea |
| `'a'` | Añadir al final. Crea si no existe |
| `'x'` | Creación exclusiva. Falla si ya existe |
| `'r+'` | Lectura y escritura sin truncar |
| `'w+'` | Lectura y escritura truncando |
| `'a+'` | Lectura y añadir |
| Sufijo `b` | Modo binario (bytes en vez de texto) |

### 3.2 El gestor de contexto

```python
with open("archivo.txt", "r", encoding="utf-8") as f:
    datos = f.read()
# f se cierra aquí automáticamente, incluso si hay excepción
```

`with` equivale a `try/finally` con cierre garantizado. Es la forma idiomática en Python 3. **Siempre** se usa así: dejar archivos abiertos agota los descriptores del sistema operativo (típicamente 1024 por proceso en Linux).

### 3.3 Estrategias de lectura

```python
# Leer todo de una vez (cuidado con archivos grandes)
contenido = f.read()

# Leer línea por línea (eficiente en memoria)
for linea in f:
    procesar(linea)

# Leer todo en una lista de líneas
lineas = f.readlines()

# Leer una cantidad fija de bytes
bloque = f.read(4096)
```

**Regla de rendimiento:** para archivos grandes, iterar línea por línea es la forma eficiente, porque el sistema operativo gestiona el búfer y solo una línea reside en memoria a la vez.

### 3.4 Escritura eficiente

Python usa un búfer de escritura. Para máximo rendimiento, agrupar las escrituras:

```python
with open("salida.txt", "w", buffering=8192) as f:
    lineas = [f"linea {i}\n" for i in range(100000)]
    f.writelines(lineas)   # una sola llamada en vez de 100,000
```

### 3.5 Comparación entre lenguajes

**Java (try-with-resources):**

```java
try (BufferedReader br = new BufferedReader(new FileReader("archivo.txt"))) {
    String linea;
    while ((linea = br.readLine()) != null) {
        System.out.println(linea);
    }
}
```

**C++ (RAII):**

```cpp
#include <fstream>
std::ifstream entrada("archivo.txt");
std::string linea;
while (std::getline(entrada, linea)) {
    std::cout << linea << std::endl;
}
```

Los tres lenguajes resuelven el mismo problema (garantizar el cierre) con mecanismos distintos: `with` en Python, `try-with-resources` en Java, RAII en C++.

---

## 4. Archivos binarios

### 4.1 Concepto

Un archivo binario almacena datos en su representación nativa en memoria. Un entero `42` ocupa 4 bytes (`0x2A 0x00 0x00 0x00`), no los caracteres `'4'` y `'2'`.

### 4.2 Empaquetado de datos en Python

```python
import struct

# Empaquetar: entero (4 bytes) + flotante (4 bytes)
datos = struct.pack("<if", 42, 3.14)

# Desempaquetar
entero, flotante = struct.unpack("<if", datos)
```

Códigos de formato: `i` (int), `f` (float), `d` (double), `s` (string), `?` (bool), `q` (long long).

**Endianness:** el prefijo `<` indica little-endian; `>`, big-endian. **El orden de bytes importa** al intercambiar archivos entre máquinas con arquitecturas distintas.

### 4.3 En C++

```cpp
#include <fstream>
// Escritura binaria
std::ofstream archivo("datos.bin", std::ios::binary);
int número = 42;
archivo.write(reinterpret_cast<char*>(&número), sizeof(número));

// Lectura binaria
std::ifstream archivo("datos.bin", std::ios::binary);
int leido;
archivo.read(reinterpret_cast<char*>(&leido), sizeof(leido));
```

`reinterpret_cast<char*>` es necesario porque `write`/`read` operan sobre bytes, no sobre tipos.

---

## 5. Acceso secuencial y aleatorio

### 5.1 Acceso secuencial

Leer o escribir en orden, desde el principio. Es el modo natural de archivos de texto, registros de log y streams.

Ventaja: simple, óptimo en búfer. Desventaja: para alcanzar el byte N hay que leer los N−1 anteriores.

### 5.2 Acceso aleatorio

Manipular la posición del puntero con `seek` para leer o escribir en cualquier offset directamente.

```python
with open("datos.bin", "r+b") as f:
    f.seek(1024)          # byte 1024 desde el inicio
    f.seek(-4, 2)         # 4 bytes antes del final (whence=2)
    f.seek(10, 1)         # 10 bytes adelante desde la posición (whence=1)
    bloque = f.read(16)
```

Orígenes (`whence`): 0 = inicio, 1 = posición actual, 2 = final.

### 5.3 Fórmula de offset para registros de tamaño fijo

```
posición = índice_del_registro × tamaño_del_registro
```

Acceder al registro k es **O(1)** con un solo `seek`. Es la base de las bases de datos simples y los índices.

### 5.4 Casos de uso del acceso aleatorio

| Caso | Técnica |
|------|---------|
| **Base de datos** | Registros de tamaño fijo indexados por posición |
| **Índices** | Búsqueda binaria sobre archivo ordenado en disco |
| **Logs rotativos** | Leer desde un offset conocido |
| **Parches** | Modificar una región sin reescribir el archivo |
| **Key-value stores** | Bitcask y similares |

### 5.5 Archivos mapeados en memoria

Técnica avanzada (`mmap`): mapear el archivo al espacio de direcciones del proceso. El acceso se hace con punteros normales y el sistema operativo carga las páginas bajo demanda. Combina la comodidad del acceso aleatorio con la eficiencia de la memoria virtual.

---

## 6. Formatos estructurados

### 6.1 CSV (Comma-Separated Values)

Formato tabular en texto plano. Estándar de intercambio de datos.

```python
import csv
with open("datos.csv", newline="", encoding="utf-8") as f:
    for fila in csv.DictReader(f):
        print(fila["columna"])
```

**Cuidados:** entrecomillado de campos con comas, saltos de línea dentro de campos, y codificación. Siempre usar el módulo `csv`, nunca partir la línea con `split(",")`.

### 6.2 JSON

Formato de intercambio basado en la sintaxis de objetos de JavaScript. Soporta objetos, arreglos, cadenas, números, booleanos y nulos.

### 6.3 Compresión

Run-Length Encoding (RLE): reemplaza secuencias repetidas por un contador. Algoritmos reales: gzip (DEFLATE), bzip2 (Burrows-Wheeler), zstd.

---

## 7. Manejo de errores

```python
try:
    with open("inexistente.txt") as f:
        contenido = f.read()
except FileNotFoundError:
    print("El archivo no existe")
except PermissionError:
    print("Sin permisos de lectura")
except IsADirectoryError:
    print("Es un directorio, no un archivo")
except UnicodeDecodeError:
    print("Problema de codificación")
```

Las excepciones específicas son: `FileNotFoundError`, `PermissionError`, `IsADirectoryError`, `NotADirectoryError`, `UnicodeDecodeError`, `OSError` (disco lleno, demasiados archivos abiertos).

**Regla:** capturar la excepción **específica**, no `except Exception` a secas, que oculta errores reales de programación.

---

## Bibliografía anotada

1. **Silberschatz, A., Galvin, P. B. & Gagne, G.** *Operating System Concepts*, X ed. Wiley, 2018. — Capítulos 10-13: la referencia sobre sistemas de archivos.
2. **Tanenbaum, A. S. & Bos, H.** *Modern Operating Systems*, IV ed. Pearson, 2014. — Capítulo 4: File Systems.
3. **Lutz, M.** *Learning Python*, V ed. O'Reilly, 2013. — Capítulo 9: Files and I/O.
4. **Stroustrup, B.** *The C++ Programming Language*, IV ed. Addison-Wesley, 2013. — Capítulo 37: Stream I/O.
5. **Loomis, M. E. S.** *Data Management and File Structures*, II ed. Prentice-Hall, 1991. — Organización de archivos y acceso secuencial/aleatorio.

## Recursos utilizados

- Python Documentation — Reading and Writing Files: https://docs.python.org/3/tutorial/inputoutput.html
- Python Documentation — csv module: https://docs.python.org/3/library/csv.html
- Python Documentation — struct module: https://docs.python.org/3/library/struct.html
- GeeksforGeeks — File Handling in Python: https://www.geeksforgeeks.org/file-handling-python/
- Microsoft Docs — File System Basics: https://docs.microsoft.com/en-us/windows/win32/fileio/file-systems
