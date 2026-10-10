r"""
Ejercicio 9: Contar lneas, palabras y caracteres
Dificultad: Bsico

CONOCIMIENTO PREVIO NECESARIO
    - Lectura de archivo completo (ejercicio 1).
    - str.split() y str.splitlines() (00-fundamentos 10.3).
    - La diferencia entre split("\\n") y splitlines().

PROBLEMA
    Calcular estadsticas bsicas de un archivo de texto: cuntas
    lneas, cuntas palabras y cuntos caracteres tiene.

FONDO MATEMTICO
    Hay una trampa sutil al contar lneas.

    Un archivo "A\\nB\\nC\\n" tiene TRES lneas de contenido, pero:

        contenido.split("\\n")      -> ["A", "B", "C", ""]
                                     4 elementos (el ltimo vacio)

        contenido.splitlines()      -> ["A", "B", "C"]
                                     3 elementos (correcto)

    El "\\n" final aade un elemento vacio con split. En cambio,
    splitlines() interpreta correctamente los finales de lnea y no
    genera ese elemento extra.

    Adems, splitlines() reconoce "\\r\\n" (Windows), "\\n" (Unix) y
    "\\r" (Mac clsico). split("\\n") no.

    Otro detalle: un archivo SIN salto final ("A\\nB\\nC") tambin
    tiene 3 lneas, y splitlines() lo cuenta bien.

ESTRATEGIA

```python
def contar_estadisticas(ruta):
    with open(ruta, encoding="utf-8") as f:
        contenido = f.read()

    return {
        "lineas":    len(contenido.splitlines()),
        "palabras":  len(contenido.split()),
        "caracteres": len(contenido)
    }
```

    Nota sobre palabras: contenido.split() SIN argumentos divide por
    cualquier espacio en blanco (espacios, tabs, saltos) y descarta
    los vacios. Es exactamente lo que se quiere para contar palabras.

TRAZA sobre "Hola mundo\\nSegunda lnea\\n"
    splitlines() -> ["Hola mundo", "Segunda lnea"]  -> 2 lneas
    split()      -> ["Hola", "mundo", "Segunda", "lnea"]  -> 4 palabras
    len()        -> 26 caracteres

COMPLEJIDAD
    Tiempo: O(n) — recorre todo el texto tres veces.
    Espacio: O(n) para el contenido + O(palabras) para las listas.

CASOS LMITE
    - Archivo vacio: 0 lneas, 0 palabras, 0 caracteres.
    - Solo espacios: 0 palabras (split descarta vacios), pero s
      caracteres.
    - Sin salto final: splitlines() cuenta las lneas reales.
    - Lneas vacas: se cuentan (a diferencia de las palabras).

APLICACIONES
    - Estadsticas de cdigo fuente (wc en Unix hace esto).
    - Anlisis de documentos.
    - Validacin de entradas de usuario.

RELACIN CON OTROS TEMAS
    - El comando `wc` de Unix hace exactamente esto.
    - Para archivos grandes, contar por streaming (sin cargar todo)
      es la tcnica del tema 06.
"""


def contar_estadisticas(ruta):
    """Cuenta lneas, palabras y caracteres. O(n) tiempo y espacio."""
    with open(ruta, encoding="utf-8") as f:
        contenido = f.read()

    return {
        "lineas": len(contenido.splitlines()),
        "palabras": len(contenido.split()),
        "caracteres": len(contenido)
    }


def contar_lineas_streaming(ruta):
    """Cuenta lneas sin cargar el archivo. O(1) memoria."""
    with open(ruta, encoding="utf-8") as f:
        return sum(1 for _ in f)


if __name__ == "__main__":
    import os

    # Archivo de prueba
    with open("test.txt", "w", encoding="utf-8") as f:
        f.write("Hola mundo\nSegunda lnea\nTercera lnea\n")

    stats = contar_estadisticas("test.txt")
    print(f"Estadsticas: {stats}")

    assert stats["lineas"] == 3, "splitlines() cuenta 3, no 4"
    assert stats["palabras"] == 6
    assert stats["caracteres"] == len("Hola mundo\nSegunda lnea\nTercera lnea\n")

    # LA TRAMPA: split("\\n") dara 4
    with open("test.txt", encoding="utf-8") as f:
        contenido = f.read()
    print(f"\nsplitlines(): {len(contenido.splitlines())} lneas (correcto)")
    print(f"split('\\\\n'):    {len(contenido.split(chr(10)))} elementos (incorrecto)")
    assert len(contenido.splitlines()) == 3
    assert len(contenido.split("\n")) == 4, "split genera el elemento vacio"

    # Archivo sin salto final: tambin 3 lneas
    with open("sin_salto.txt", "w", encoding="utf-8") as f:
        f.write("Lnea 1\nLnea 2\nLnea 3")          # sin \\n al final
    s2 = contar_estadisticas("sin_salto.txt")
    print(f"\nSin salto final: {s2['lineas']} lneas")
    assert s2["lineas"] == 3

    # Archivo vacio
    with open("vacio.txt", "w", encoding="utf-8") as f:
        pass
    s3 = contar_estadisticas("vacio.txt")
    assert s3["lineas"] == 0
    assert s3["palabras"] == 0
    assert s3["caracteres"] == 0
    print(f"Archivo vacio: {s3}")

    # Solo espacios: 0 palabras pero s caracteres
    with open("espacios.txt", "w", encoding="utf-8") as f:
        f.write("   \n\t\n  ")
    s4 = contar_estadisticas("espacios.txt")
    assert s4["palabras"] == 0, "split() descarta los espacios"
    assert s4["lineas"] == 3
    assert s4["caracteres"] == 8
    print(f"\nSolo espacios: {s4}")
    print("  split() sin argumentos descarta los vacios")

    # Lneas vacas s se cuentan
    with open("vacias.txt", "w", encoding="utf-8") as f:
        f.write("A\n\nB\n\n\nC\n")
    s5 = contar_estadisticas("vacias.txt")
    assert s5["lineas"] == 6, "las lneas vacas cuentan"
    assert s5["palabras"] == 3, "pero no aportan palabras"
    print(f"\nLneas vacas conservadas: {s5}")

    # Salto de lnea Windows: splitlines() lo maneja.
    # NOTA: en modo TEXTO Python traduce \r\n a \n (traduccin
    # universal), as que el contenido ledo tiene 6 caracteres, no 9.
    with open("windows.txt", "w", newline="", encoding="utf-8") as f:
        f.write("A\r\nB\r\nC\r\n")
    s6 = contar_estadisticas("windows.txt")
    print(f"\nSaltos CRLF (Windows), modo texto: {s6}")
    assert s6["lineas"] == 3, "splitlines maneja CRLF"
    assert s6["caracteres"] == 6, "el \r\n se tradujo a \n"

    # En modo BINARIO los \r s aparecen
    with open("windows.txt", "rb") as f:
        bytes_reales = len(f.read())
    print(f"  En modo binario: {bytes_reales} bytes (los \r s cuentan)")
    assert bytes_reales == 9
    # Conteo por streaming: memoria O(1)
    lineas_grandes = [f"Lnea {i} con algunas palabras\n" for i in range(100000)]
    with open("grande.txt", "w", encoding="utf-8") as f:
        f.writelines(lineas_grandes)

    n_stream = contar_lineas_streaming("grande.txt")
    n_full = contar_estadisticas("grande.txt")["lineas"]
    print(f"\nArchivo de 100,000 lneas:")
    print(f"  Streaming (O(1) memoria):    {n_stream}")
    print(f"  Archivo completo (O(n)):     {n_full}")
    assert n_stream == n_full == 100000

    # splitlines() == conteo por streaming
    assert contar_lineas_streaming("grande.txt") == \
           contar_estadisticas("grande.txt")["lineas"]

    for a in ["test.txt", "sin_salto.txt", "vacio.txt", "espacios.txt",
              "vacias.txt", "windows.txt", "grande.txt"]:
        os.remove(a)

    print("\n Todas las pruebas pasaron")
