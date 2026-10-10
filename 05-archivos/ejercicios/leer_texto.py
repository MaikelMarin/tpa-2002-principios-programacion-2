r"""
Ejercicio 1: Leer archivo de texto
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Gestor de contexto `with` (00-fundamentos §10.5).
    - Codificación de caracteres (teoria.md §2.3).
    - Excepciones (00-fundamentos §10.6).

PROBLEMA
    Leer el contenido completo de un archivo de texto.

FONDO MATEMÁTICO
    Un archivo de texto es una secuencia de bytes que se interpreta
    como caracteres según una CODIFICACIÓN. El mismo archivo leído con
    la codificación incorrecta produce texto corrupto o un error.

    Por eso `encoding="utf-8"` no es opcional: el valor por defecto de
    Python depende del sistema operativo (el locale), lo que hace que
    el mismo código falle en una máquina y funcione en otra.

ESTRATEGIA

```python
with open(ruta, "r", encoding="utf-8") as f:
    return f.read()
```

    Tres elementos, ninguno decorativo:
      1. `with` → cierra el archivo siempre, incluso si hay excepción.
      2. `encoding="utf-8"` → comportamiento idéntico en todo sistema.
      3. `f.read()` → lee TODO el archivo de una vez.

    El modo `"r"` es el de lectura. Si el archivo no existe, lanza
    FileNotFoundError.

TRAZA de ejecución
    open("test.txt", "r", encoding="utf-8")
      → el sistema operativo busca el archivo en disco
      → devuelve un descriptor de archivo
    f.read()
      → lee todos los bytes del archivo
      → los decodifica de UTF-8 a str
      → devuelve "Hola, mundo!\nSegunda línea\n"
    Salida del bloque with
      → f.close() automático

COMPLEJIDAD
    Tiempo: O(n) donde n es el tamaño del archivo en bytes.
    Espacio: O(n) porque f.read() carga todo en memoria.

    PARA ARCHIVOS GRANDES: f.read() es peligroso. Un archivo de 4 GB
    cargado en memoria puede agotar la RAM. La alternativa es leer
    línea por línea (ejercicio 3) o por bloques.

MANEJO DE ERRORES
    FileNotFoundError    el archivo no existe
    PermissionError      sin permisos de lectura
    IsADirectoryError    la ruta es un directorio
    UnicodeDecodeError   el archivo no es UTF-8 válido

RELACIÓN CON OTROS TEMAS
    - El tema 06 (grandes datos) muestra cómo leer archivos que NO
      caben en memoria.
    - El modo binario (ejercicios 5 y 6) lee bytes en vez de texto.
"""


def leer_archivo(ruta):
    """Lee y devuelve el contenido completo de un archivo de texto.

    O(n) tiempo y espacio, donde n es el tamaño del archivo.
    """
    # encoding="utf-8" es explícito a propósito: el valor por defecto
    # depende del locale del sistema operativo.
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def leer_archivo_seguro(ruta):
    """Versión que maneja los errores comunes sin propagarlos."""
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read(), None
    except FileNotFoundError:
        return None, "El archivo no existe"
    except PermissionError:
        return None, "Sin permisos de lectura"
    except IsADirectoryError:
        return None, "La ruta es un directorio, no un archivo"
    except UnicodeDecodeError:
        return None, "El archivo no es UTF-8 válido"


if __name__ == "__main__":
    import os

    # Crear archivo de prueba
    with open("test.txt", "w", encoding="utf-8") as f:
        f.write("Hola, mundo!\nSegunda línea\n")

    contenido = leer_archivo("test.txt")
    print(f"Contenido:\n{contenido}")

    # El contenido es exactamente lo escrito
    assert contenido == "Hola, mundo!\nSegunda línea\n"
    assert "Hola, mundo!" in contenido
    assert "Segunda línea" in contenido

    # El salto de línea se conserva
    assert contenido.count("\n") == 2

    # Archivo vacío: devuelve cadena vacía, no None
    with open("vacio.txt", "w", encoding="utf-8") as f:
        pass
    assert leer_archivo("vacio.txt") == ""
    print("Archivo vacío → cadena vacía")

    # Caracteres no ASCII: la ñ y las tildes funcionan con UTF-8
    with open("unicode.txt", "w", encoding="utf-8") as f:
        f.write("El niño comió mañana y café\n")
    c_uni = leer_archivo("unicode.txt")
    assert c_uni == "El niño comió mañana y café\n"
    print(f"Unicode: {c_uni.strip()}")

    # El MANEJO DE ERRORES funciona
    contenido, error = leer_archivo_seguro("no_existe.txt")
    assert contenido is None
    assert error == "El archivo no existe"
    print(f"Archivo inexistente → {error}")

    _, err_dir = leer_archivo_seguro(".")
    assert err_dir == "La ruta es un directorio, no un archivo"
    print(f"Directorio → {err_dir}")

    # Con ruta válida, el error es None
    contenido, error = leer_archivo_seguro("test.txt")
    assert error is None
    assert contenido is not None

    # Round-trip: escribir y leer da el mismo contenido
    original = "Línea 1\nLínea 2\nÚltima línea"
    with open("roundtrip.txt", "w", encoding="utf-8") as f:
        f.write(original)
    assert leer_archivo("roundtrip.txt") == original

    # Contenido grande: funciona, pero carga todo en memoria
    lineas = [f"Línea número {i}\n" for i in range(10000)]
    with open("grande.txt", "w", encoding="utf-8") as f:
        f.writelines(lineas)
    c_grande = leer_archivo("grande.txt")
    assert c_grande.count("\n") == 10000
    print(f"\nArchivo de 10,000 líneas leído: {len(c_grande):,} caracteres")
    print(f"  Tamaño en memoria: ~{len(c_grande):,} bytes")

    for archivo in ["test.txt", "vacio.txt", "unicode.txt", "roundtrip.txt", "grande.txt"]:
        os.remove(archivo)

    print("\n✓ Todas las pruebas pasaron")
