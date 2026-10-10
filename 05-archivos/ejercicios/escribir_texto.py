r"""
Ejercicio 2: Escribir archivo de texto
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Modo "w" y "a" (teoria.md §3.1).
    - La diferencia CRÍTICA entre truncar y añadir.
    - Gestor de contexto `with` (00-fundamentos §10.5).

PROBLEMA
    Escribir contenido en un archivo de texto.

FONDO MATEMÁTICO
    La diferencia entre "w" y "a" es la más importante del tema:

        "w" (write)  → TRUNCA: borra todo y empieza de cero.
        "a" (append) → AÑADE: conserva lo que había.

    Confundirlos es una fuente clásica de pérdida de datos: abrir con
    "w" un archivo importante lo destruye instantáneamente.

    Regla mental: "w" = crear o reemplazar. "a" = sumar.

ESTRATEGIA

```python
# Reemplazar (o crear)
with open("salida.txt", "w", encoding="utf-8") as f:
    f.write("Contenido nuevo\n")

# Añadir al final
with open("salida.txt", "a", encoding="utf-8") as f:
    f.write("Contenido añadido\n")
```

    Detalles:
      1. `encoding="utf-8"` explícito: el mismo problema del ejercicio 1.
      2. `f.write` NO añade "\n" automáticamente. Hay que incluirlo.
      3. `writelines` acepta una lista de líneas (más eficiente que
         muchas llamadas a write por separado).

TRAZA de ejecución con "w"
    Archivo previo: "VIEJO\nVIEJO\n"

    open("f.txt", "w")
      → el sistema TRUNCA el archivo a 0 bytes
      → "VIEJO" se ha perdido

    f.write("NUEVO\n")
      → escribe 6 bytes

    Resultado: "NUEVO\n"

    Contraste con "a":
    open("f.txt", "a")
      → el puntero va al final, el contenido se conserva
    f.write("EXTRA\n")
      → añade al final

    Resultado: "NUEVO\nEXTRA\n"

COMPLEJIDAD
    write: O(1) amortizado. La escritura va a un búfer (típicamente
    8 KB) que se vacía en bloque al disco. Escribir muchas cosas
    pequeñas seguidas es eficiente.

    writelines con una lista: más eficiente que N llamadas a write,
    porque reduce el overhead de la API.

ERRORES COMUNES
    1. Usar "w" cuando se quería "a" → pérdida de datos.
    2. Olvidar el "\n" → todas las líneas pegadas.
    3. Sin encoding → falla en otro sistema operativo.
    4. Escribir en un archivo abierto en modo lectura → io.UnsupportedOperation.

APLICACIONES
    - Generar reportes y archivos de salida.
    - Guardar configuración.
    - Serializar datos.

RELACIÓN CON OTROS TEMAS
    - El modo append ("a") es la base de los sistemas de logs
      (tema 04, ejercicio 12).
    - El buffering es lo que se optimiza en el tema 06.
"""


def escribir_archivo(ruta, contenido):
    """Escribe (o reemplaza) el contenido de un archivo."""
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)


def anadir_archivo(ruta, contenido):
    """Añade al final sin borrar lo existente."""
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(contenido)


def escribir_lineas(ruta, lineas):
    """Escribe una lista de líneas de forma eficiente."""
    with open(ruta, "w", encoding="utf-8") as f:
        f.writelines(lineas)


if __name__ == "__main__":
    import os

    # Crear archivo
    escribir_archivo("test.txt", "Hola, mundo!\n")
    assert os.path.exists("test.txt")

    # Sobrescribir: "w" destruye el anterior
    escribir_archivo("test.txt", "Sobrescrito!\n")
    with open("test.txt", "r", encoding="utf-8") as f:
        assert f.read() == "Sobrescrito!\n"
    print("Modo 'w': el contenido anterior se perdió (truncado)")

    # Añadir: "a" conserva
    anadir_archivo("test.txt", "Segunda línea\n")
    with open("test.txt", "r", encoding="utf-8") as f:
        contenido = f.read()
    assert contenido == "Sobrescrito!\nSegunda línea\n"
    print(f"Modo 'a': {contenido!r}")

    # Demostración de que "w" destruye y "a" no
    escribir_archivo("importante.txt", "DATOS IMPORTANTES\n")
    anadir_archivo("importante.txt", "MÁS DATOS\n")
    assert "DATOS IMPORTANTES" in open("importante.txt").read()

    escribir_archivo("importante.txt", "nuevo")        # ¡destruye!
    with open("importante.txt") as f:
        assert f.read() == "nuevo", "'w' borró todo"
    print("Confirmado: 'w' sobre un archivo existente lo destruye")

    # Un archivo inexistente se CREA en ambos modos
    os.remove("importante.txt")
    anadir_archivo("nuevo.txt", "creado con 'a'\n")
    assert os.path.exists("nuevo.txt")
    print("'a' también crea el archivo si no existe")

    # writelines: eficiente para muchas líneas
    lineas = [f"Línea {i}\n" for i in range(1000)]
    escribir_lineas("muchas.txt", lineas)
    with open("muchas.txt", "r", encoding="utf-8") as f:
        n = sum(1 for _ in f)
    assert n == 1000
    print(f"\nwritelines con 1000 líneas: {n} líneas escritas")

    # El "\n" NO se añade automáticamente
    escribir_archivo("sin_salto.txt", "A")
    anadir_archivo("sin_salto.txt", "B")
    with open("sin_salto.txt") as f:
        assert f.read() == "AB", "sin \\n las escrituras se pegan"
    print("Sin \\n: 'A' + 'B' = 'AB' (se pegan)")

    # Con "\n" quedan separadas
    escribir_archivo("con_salto.txt", "A\n")
    anadir_archivo("con_salto.txt", "B\n")
    with open("con_salto.txt") as f:
        assert f.read() == "A\nB\n"
    print("Con \\n: 'A\\n' + 'B\\n' = 'A\\nB\\n'")

    # Escribir en modo lectura falla
    import io
    with open("test.txt", "r", encoding="utf-8") as f:
        try:
            f.write("x")
            raise AssertionError("debía lanzar error")
        except io.UnsupportedOperation:
            print("Escribir en modo lectura: io.UnsupportedOperation")

    # Encoding explícito: necesario para no ASCII
    escribir_archivo("unicode.txt", "El niño comió café\n")
    with open("unicode.txt", "r", encoding="utf-8") as f:
        assert f.read() == "El niño comió café\n"
    print("\nUnicode (ñ, acentos): escrito y leído correctamente")

    # Comparación de rendimiento: write vs writelines
    import time

    inicio = time.time()
    with open("lento.txt", "w", encoding="utf-8") as f:
        for i in range(50000):
            f.write(f"Línea {i}\n")
    t_write = time.time() - inicio

    inicio = time.time()
    escribir_lineas("rapido.txt", [f"Línea {i}\n" for i in range(50000)])
    t_writelines = time.time() - inicio

    print(f"\n50,000 líneas:")
    print(f"  write() uno a uno:  {t_write*1000:.0f} ms")
    print(f"  writelines() lista: {t_writelines*1000:.0f} ms")

    for a in ["test.txt", "importante.txt", "nuevo.txt", "muchas.txt",
              "sin_salto.txt", "con_salto.txt", "unicode.txt",
              "lento.txt", "rapido.txt"]:
        if os.path.exists(a):
            os.remove(a)

    print("\n✓ Todas las pruebas pasaron")
