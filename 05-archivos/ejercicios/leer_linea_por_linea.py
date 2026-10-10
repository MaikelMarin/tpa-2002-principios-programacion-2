r"""
Ejercicio 3: Leer línea por línea
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Leer archivo completo (ejercicio 1): para comparar el coste.
    - Iteración sobre objetos archivo en Python.
    - Búferes del sistema operativo (teoria.md §3.3).

PROBLEMA
    Leer un archivo de texto procesando una línea a la vez.

FONDO MATEMÁTICO
    La diferencia con f.read() es de MEMORIA, no de tiempo:

        f.read()               → O(n) memoria (todo en RAM)
        iterar líneas          → O(línea más larga) memoria

    Un archivo de 4 GB podría leerse completo con `for linea in f`
    usando unos pocos KB de RAM. Con f.read() necesitaría 4 GB.

    ¿Cómo es posible? El búfer del sistema operativo lee bloques
    (típicamente 8 KB) según se necesitan, y Python mantiene solo la
    línea actual en memoria.

ESTRATEGIA

```python
with open(ruta, "r", encoding="utf-8") as f:
    for linea in f:
        procesar(linea)      # línea incluye el "\n" al final
```

    El objeto archivo es un ITERABLE: cada `next()` lee hasta el
    siguiente salto de línea. Es eficiente por diseño del lenguaje.

    Detalle: cada `linea` incluye el `\n` final, salvo la última si el
    archivo no termina en salto. Se suele quitar con .rstrip("\n")
    o .strip().

TRAZA de ejecución
    Archivo: "A\nB\nC\n"

    for linea in f:
      1. el búfer lee "A\nB\nC\n" (bloque pequeño)
      2. devuelve "A\n" → procesar("A\n")
      3. devuelve "B\n" → procesar("B\n")
      4. devuelve "C\n" → procesar("C\n")
      5. fin del archivo → el bucle termina

    4 iteraciones detectadas, 3 líneas procesadas.

COMPLEJIDAD
    Tiempo: O(n) — se leen todos los bytes.
    Espacio: O(m) donde m es la longitud de la línea más larga,
             NO O(n). Esa es toda la ventaja.

MANERAS DE LEER, COMPARADAS
    Método                  Memoria      Cuándo usarlo
    f.read()                O(n)         Archivos pequeños
    for linea in f          O(línea)     Archivos grandes, procesar
    f.readlines()           O(n)         Cuando se quiere una lista
    f.readline()            O(línea)     Control manual del flujo
    f.read(4096)            O(bloque)   Binario, bloques fijos

APLICACIONES
    - Procesar logs de servidor (gigabytes).
    - Leer CSVs grandes.
    - Filtrar líneas que cumplan una condición.

RELACIÓN CON OTROS TEMAS
    - El tema 06 (grandes datos) se apoya completamente en esta
      técnica: es la base del procesamiento por streaming.
"""


def leer_lineas(ruta):
    """Lee un archivo línea por línea. O(m) memoria, no O(n).

    Devuelve una lista con las líneas (sin el salto final).
    """
    lineas = []
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            lineas.append(linea.rstrip("\n"))
    return lineas


def procesar_lineas(ruta, funcion):
    """Aplica una función a cada línea sin acumular nada.

    Memoria O(1) sin importar el tamaño del archivo.
    """
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            funcion(linea.rstrip("\n"))


if __name__ == "__main__":
    import os

    with open("test.txt", "w", encoding="utf-8") as f:
        f.write("Línea 1\nLínea 2\nLínea 3\n")

    lineas = leer_lineas("test.txt")
    print(f"Líneas leídas: {lineas}")

    assert lineas == ["Línea 1", "Línea 2", "Línea 3"]
    assert len(lineas) == 3

    # Los saltos de línea se eliminaron
    assert "\n" not in lineas[0]
    assert not any("\n" in l for l in lineas)

    # Casos base
    with open("vacio.txt", "w", encoding="utf-8") as f:
        pass
    assert leer_lineas("vacio.txt") == []

    # Una sola línea, SIN salto final
    with open("sin_salto.txt", "w", encoding="utf-8") as f:
        f.write("única línea")
    assert leer_lineas("sin_salto.txt") == ["única línea"]
    print("Archivo sin salto final: funciona")

    # Líneas vacías se conservan (no se descartan)
    con_vacias = "A\n\nB\n\n\nC\n"
    with open("vacias.txt", "w", encoding="utf-8") as f:
        f.write(con_vacias)
    assert leer_lineas("vacias.txt") == ["A", "", "B", "", "", "C"]
    print(f"Líneas vacías conservadas: {leer_lineas('vacias.txt')}")

    # Procesar sin acumular: memoria constante
    contador = [0]
    procesar_lineas("test.txt", lambda l: contador.__setitem__(0, contador[0] + 1))
    assert contador[0] == 3
    print(f"Procesadas {contador[0]} líneas sin acumular")

    # Comparación de memoria con f.read()
    lineas_grandes = [f"Línea {i}\n" for i in range(100000)]
    with open("grande.txt", "w", encoding="utf-8") as f:
        f.writelines(lineas_grandes)

    import sys

    # f.read(): carga todo (O(n))
    with open("grande.txt", "r", encoding="utf-8") as f:
        contenido = f.read()
    mem_read = sys.getsizeof(contenido)

    # for linea in f: solo la línea actual (O(m))
    linea_mas_larga = 0
    with open("grande.txt", "r", encoding="utf-8") as f:
        for linea in f:
            linea_mas_larga = max(linea_mas_larga, sys.getsizeof(linea))

    print(f"\nArchivo de 100,000 líneas:")
    print(f"  f.read() en memoria:      {mem_read:,} bytes")
    print(f"  línea más larga:          {linea_mas_larga:,} bytes")
    print(f"  Ratio: {mem_read / linea_mas_larga:,.0f}x menos memoria")
    assert mem_read > linea_mas_larga * 100

    # Ambas formas leen el mismo contenido
    lineas_leidas = leer_lineas("grande.txt")
    assert lineas_leidas == contenido.splitlines()

    # Contar líneas equivale a len(splitlines)
    with open("grande.txt", "r", encoding="utf-8") as f:
        n = sum(1 for _ in f)
    assert n == 100000
    print(f"  Contadas {n:,} líneas con memoria O(1)")

    for a in ["test.txt", "vacio.txt", "sin_salto.txt", "vacias.txt", "grande.txt"]:
        os.remove(a)

    print("\n✓ Todas las pruebas pasaron")
