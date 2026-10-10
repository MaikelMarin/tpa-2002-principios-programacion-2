r"""
Ejercicio 6: Lectura binaria
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Modo "rb" (teoria.md §3.1).
    - struct.unpack (ejercicio 5).
    - Difercias entre leer texto y leer bytes.

PROBLEMA
    Leer datos numéricos desde un archivo binario.

FONDO MATEMÁTICO
    Leer texto y leer binario difieren en la UNIDAD:

        Texto:   decodifica bytes a caracteres (str)
        Binario: devuelve bytes crudos (bytes)

    En modo texto, Python además interpreta los saltos de línea según
    el sistema operativo ("\r\n" → "\n" en Windows). En modo binario
    no hay NINGUNA interpretación: cada byte llega tal cual.

    Eso hace al modo binario la única opción para:
      - Imágenes, audio, video.
      - Ejecutables.
      - Cualquier formato con datos numéricos.

ESTRATEGIA

```python
import struct

with open("datos.bin", "rb") as f:
    entero = struct.unpack("<i", f.read(4))[0]     # 4 bytes
    flotante = struct.unpack("<f", f.read(4))[0]   # 4 bytes
```

    f.read(4) lee EXACTAMENTE 4 bytes. Si hay menos, devuelve lo que
    haya (y struct fallará si no puede llenar su formato).

    El orden de lectura importa: se lee en el mismo orden en que se
    escribió.

TRAZA sobre un archivo de 8 bytes: 2A 00 00 00 | C3 F5 48 40
    f.read(4)  → b'\x2a\x00\x00\x00'
    struct.unpack("<i", ...) → (42,)
      → entero = 42

    f.read(4)  → b'\xc3\xf5H@'
    struct.unpack("<f", ...) → (3.1400001,)
      → flotante = 3.1400001

COMPLEJIDAD
    Tiempo: O(n) donde n es el tamaño leído.
    Espacio: O(n) para el buffer.

DEMOSTRACIÓN DE CORRECCIÓN DEL ROUND-TRIP
    Si se escribe con struct.pack(fmt, valores) y se lee con
    struct.unpack(fmt, datos) usando el MISMO fmt y el MISMO orden,
    se recuperan los valores originales (salvo la precisión de punto
    flotante, que es inherente a IEEE 754, no al formato). ∎

CASOS LÍMITE
    - Archivo vacío: f.read(4) devuelve b"" y struct lanza error.
    - Archivo truncado: si sobran 2 bytes, unpack falla.
    - Archivo más grande: sobran bytes, se ignoran si no se leen.

APLICACIONES
    - Leer cabeceras de formatos (BMP, PNG, WAV).
    - Intercambio de datos entre programas.
    - Leer registros de bases de datos propias.

RELACIÓN CON OTROS TEMAS
    - El acceso aleatorio (ejercicio 8) combina la lectura binaria con
      seek para saltar a registros concretos.
"""


import struct


def leer_entero(ruta, posicion=0):
    """Lee un entero de 4 bytes desde una posición."""
    with open(ruta, "rb") as f:
        f.seek(posicion)
        return struct.unpack("<i", f.read(4))[0]


def leer_flotante(ruta, posicion=0):
    """Lee un flotante de 4 bytes desde una posición."""
    with open(ruta, "rb") as f:
        f.seek(posicion)
        return struct.unpack("<f", f.read(4))[0]


if __name__ == "__main__":
    import os

    # Crear archivo con datos conocidos
    with open("test.bin", "wb") as f:
        f.write(struct.pack("<i", 12345))
        f.write(struct.pack("<f", 2.718))

    entero = leer_entero("test.bin")
    flotante = leer_flotante("test.bin", 4)
    print(f"Entero: {entero}")
    print(f"Flotante: {flotante}")

    # Round-trip exacto
    assert entero == 12345
    assert abs(flotante - 2.718) < 0.001
    assert leer_entero("test.bin", 0) == 12345

    # Tamaño del archivo
    assert os.path.getsize("test.bin") == 8, "4 + 4 bytes"
    print(f"Tamaño: {os.path.getsize('test.bin')} bytes")

    # El orden de lectura importa: debe coincidir con el de escritura
    with open("test.bin", "rb") as f:
        e = struct.unpack("<i", f.read(4))[0]
        fl = struct.unpack("<f", f.read(4))[0]
    assert e == 12345 and abs(fl - 2.718) < 0.001

    # Archivo vacío: f.read devuelve b"" y struct falla
    with open("vacio.bin", "wb") as f:
        pass
    try:
        leer_entero("vacio.bin")
        raise AssertionError("debía lanzar error")
    except struct.error:
        print("Archivo vacío: struct.error detectado")

    # Archivo truncado: si hay menos bytes, falla
    with open("truncado.bin", "wb") as f:
        f.write(b"\x01\x02")                     # solo 2 de 4 bytes
    try:
        leer_entero("truncado.bin")
        raise AssertionError("debía lanzar error")
    except struct.error:
        print("Archivo truncado: struct.error detectado")

    # CASO LÍMITE: leer más allá del final devuelve menos bytes
    resultado = leer_entero_simple = None
    with open("test.bin", "rb") as f:
        f.seek(6)
        parcial = f.read(4)
    assert len(parcial) == 2, "solo quedan 2 bytes desde la posición 6"
    print(f"Lectura parcial desde pos 6: {parcial!r} (2 de 4 bytes)")

    # Leer TODOS los enteros de un archivo
    with open("lista.bin", "wb") as f:
        for i in range(10):
            f.write(struct.pack("<i", i * 10))

    enteros = []
    with open("lista.bin", "rb") as f:
        while True:
            datos = f.read(4)
            if not datos:
                break
            enteros.append(struct.unpack("<i", datos)[0])

    print(f"\nEnteros leídos: {enteros}")
    assert enteros == [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

    # Tamaño del archivo y número de registros
    import os as _os
    n_registros = _os.path.getsize("lista.bin") // 4
    assert n_registros == 10
    print(f"Archivo de {_os.path.getsize('lista.bin')} bytes = {n_registros} registros de 4")

    # No hay interpretación de saltos de línea en modo binario
    with open("saltos.bin", "wb") as f:
        f.write(b"linea1\r\nlinea2\r\n")
    with open("saltos.bin", "rb") as f:
        crudo = f.read()
    assert crudo == b"linea1\r\nlinea2\r\n", "los bytes llegan tal cual"
    print(f"\nModo binario conserva \\r\\n: {crudo!r}")

    # En modo texto, Windows/Unix los interpretan
    with open("saltos.bin", "r", encoding="utf-8") as f:
        texto = f.read()
    print(f"Modo texto: {texto!r}")

    for a in ["test.bin", "vacio.bin", "truncado.bin", "lista.bin", "saltos.bin"]:
        _os.remove(a)

    print("\n✓ Todas las pruebas pasaron")
