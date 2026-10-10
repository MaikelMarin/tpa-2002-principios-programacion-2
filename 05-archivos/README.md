# 05 — Archivos

## Mapa conceptual

```
                 ARCHIVOS
                    │
        ┌───────────┼───────────┐
        │           │           │
   SISTEMAS     MODOS      ACCESO
        │           │           │
   ┌────┴────┐  ┌───┴───┐   ┌───┴───┐
   │         │  │       │   │       │
I-nodos  Asignacin r/w/a  rb/wb  Secuencial  Aleatorio
         bloques          (binario) (streaming)  (seek)
            │                              │
            └──────────┬───────────────────┘
                       │
              FORMATOS
        ┌──────────────┼──────────────┐
        │              │              │
      Texto         Binario       Estructurado
     (UTF-8)     (struct,endian)   (CSV, JSON)
```

## Temas a tocar

| # | Tema | Qué se cubre |
|---|------|--------------|
| 1 | Sistemas de archivos | Definin, historia (RAMAC 1956 → APFS 2017), anatoma del i-nodo, estrategias de asignacin de bloques |
| 2 | Texto vs binario | Cundo usar cada modo, codificaciones (ASCII, Latin-1, UTF-8, UTF-16, UTF-32) |
| 3 | Modos de apertura | r, w, a, x, r+, w+, a+ y sus variantes binarias |
| 4 | Binario | `struct`, endianness, tamaos de tipos, precisin IEEE 754 |
| 5 | Acceso | Secuencial (streaming) vs aleatorio (seek); frmula de offset |
| 6 | Formatos | CSV (con sus trampas), JSON |
| 7 | Errores | FileNotFoundError, PermissionError, IsADirectoryError, UnicodeDecodeError |

## Contenido categorizado

| Categora | Descripcin | Ejercicios |
|----------|-------------|------------|
| **Texto bsico** | Leer completo, escribir, aadir, leer por lneas | 1, 2, 4, 3 |
| **Binario** | Empaquetar con `struct`, endianness, tamaos de tipos | 5, 6 |
| **Acceso** | Secuencial (memoria O(1)) y aleatorio (offset por registro) | 7, 8 |
| **Anlisis** | Contar lneas/palabras/caracteres con la trampa de `split` | 9 |
| **Formatos** | CSV con comas internas, JSON a grafo | 9, 18 |
| **Persistencia** | Sistema de archivos virtual como rbol | 17 |
| **Compresin** | RLE sobre archivos reales | 14 |
| **Logs** | Append con timestamp y niveles | 12 |
| **Copia** | Copiar binario por bloques | 8 |

## Lista de ejercicios y ubicacin de soluciones

| # | Ejercicio | Dificultad | Solucin |
|---|-----------|------------|----------|
| 1 | Leer archivo de texto | Bsico | [`ejercicios/leer_texto.py`](ejercicios/leer_texto.py) |
| 2 | Escribir archivo de texto | Bsico | [`ejercicios/escribir_texto.py`](ejercicios/escribir_texto.py) |
| 3 | Leer lnea por lnea | Bsico | [`ejercicios/leer_linea_por_linea.py`](ejercicios/leer_linea_por_linea.py) |
| 4 | Aadir al final | Bsico | [`ejercicios/anadir_texto.py`](ejercicios/anadir_texto.py) |
| 5 | Escritura binaria | Intermedio | [`ejercicios/escritura_binaria.py`](ejercicios/escritura_binaria.py) |
| 6 | Lectura binaria | Intermedio | [`ejercicios/lectura_binaria.py`](ejercicios/lectura_binaria.py) |
| 7 | Acceso secuencial | Bsico | [`ejercicios/acceso_secuencial.py`](ejercicios/acceso_secuencial.py) |
| 8 | Acceso aleatorio | Intermedio | [`ejercicios/acceso_aleatorio.py`](ejercicios/acceso_aleatorio.py) |
| 9 | Contar lneas y palabras | Bsico | [`ejercicios/contar_lineas_palabras.py`](ejercicios/contar_lineas_palabras.py) |
| 10 | CSV a diccionarios | Bsico | [`ejercicios/csv_a_diccionario.py`](ejercicios/csv_a_diccionario.py) |
| 11 | Run-Length Encoding | Intermedio | [`ejercicios/run_length_encoding.py`](ejercicios/run_length_encoding.py) |
| 12 | Sistema de logs | Intermedio | [`ejercicios/sistema_logs.py`](ejercicios/sistema_logs.py) |
| 13 | Acceso aleatorio en C++ | Avanzado | [`ejercicios/acceso_aleatorio_cpp.cpp`](ejercicios/acceso_aleatorio_cpp.cpp) |
| 14 | Sistema de archivos simple | Experto | [`ejercicios/sistema_archivos_simple.py`](ejercicios/sistema_archivos_simple.py) |
| — | Copiar archivo binario | Bsico | [`ejercicios/copiar_binario.py`](ejercicios/copiar_binario.py) |

Cada archivo incluye conocimiento previo, fondo, estrategia, traza, demostracin, complejidad razonada y verificacin experimental.

## Ruta de aprendizaje recomendada

1. **Ejercicios 1, 2** — la pareja bsica: leer y escribir. Note que `encoding` no es opcional.
2. **Ejercicio 3** — leer por lneas: el salto de O(n) a O(1) en memoria. Mida la diferencia.
3. **Ejercicio 4** — append: por qu los logs usan "a" y nunca "w".
4. **Ejercicios 5, 6** — binario con `struct`. Entienda endianness antes de continuar.
5. **Ejercicio 7** — acceso secuencial y generadores. La base del tema 06.
6. **Ejercicio 8** — acceso aleatorio. La frmula posicin = ndice × tamao.
7. **Ejercicio 9** — la trampa de `split("\n")` vs `splitlines()`.
8. **Ejercicio 10** — CSV: por qu `split(",")` falla con comas internas.
9. **Ejercicio 14** — el sistema de archivos como rbol: cierre del tema.

## Prerrequisitos

De `00-fundamentos`: arreglos (§8.2), memoria RAM vs disco (§9), `with` (§10.5), excepciones (§10.6), `struct` (§10.7), diccionarios (§8.6).

## Teora

Ver [`teoria.md`](teoria.md) — incluye la anatoma del i-nodo, las cuatro estrategias de asignacin de bloques, la tabla de codificaciones y la frmula de offset para registros fijos.
