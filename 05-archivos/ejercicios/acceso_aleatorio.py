r"""
Ejercicio 8: Acceso aleatorio
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Modo "r+b" (lectura y escritura binaria).
    - El concepto de puntero de posición en un archivo.
    - Tamaños fijos de tipos (ejercicio 5).

PROBLEMA
    Modificar una región específica de un archivo sin reescribirlo
    completo.

FONDO MATEMÁTICO
    Un archivo es una secuencia de bytes indexada desde 0. El sistema
    operativo mantiene un PUNTERO de posición que indica dónde se va a
    leer o escribir a continuación.

    `seek(posición)` mueve ese puntero. Tras seek, una lectura o
    escritura opera desde esa posición.

    LOS TRES ORÍGENES (whence):
        0 = inicio del archivo   → f.seek(1024)
        1 = posición actual      → f.seek(10, 1)   (avanzar 10)
        2 = final del archivo    → f.seek(-4, 2)   (4 antes del final)

FÓRMULA DE OFFSET PARA REGISTROS FIJOS
    Si cada registro mide T bytes, el registro k está en:

        posición = k × T

    Acceder a cualquier registro es O(1): un seek y una lectura. Es
    la base de las bases de datos más simples.

ESTRATEGIA

```python
# Escribir en una posición sin tocar el resto
def escribir_en_posicion(ruta, posicion, datos):
    with open(ruta, "r+b") as f:        # r+b: lee y escribe sin truncar
        f.seek(posicion)
        f.write(datos)
```

    El modo "r+b" es importante: abre para lectura Y escritura SIN
    borrar el contenido. Con "wb" se destruiría el archivo entero.

TRAZA sobre "ABCDEFGHIJ" (10 bytes)
    Escribir "XY" en la posición 5:

    Estado inicial:  A B C D E F G H I J
    Posición:        0 1 2 3 4 5 6 7 8 9

    f.seek(5)      → el puntero va a la posición 5 (la F)
    f.write("XY")  → escribe X en 5, Y en 6

    Estado final:    A B C D E X Y H I J

    Note: se sobrescribieron F y G, NO F y H. Escribir 2 bytes desde la
    posición 5 consume las posiciones 5 y 6.

    Resultado: "ABCDEXYHIJ"

DEMOSTRACIÓN DE CORRECCIÓN
    seek(pos) coloca el puntero en pos. write(datos) escribe len(datos)
    bytes empezando en pos, sobrescribiendo lo que hubiera. Los bytes
    fuera del rango [pos, pos+len) no se tocan. Es la semántica
    declarada del sistema de archivos POSIX. ∎

COMPLEJIDAD
    seek: O(1) — solo mueve un puntero.
    read/write: O(k) donde k es la cantidad pedida.

    El acceso aleatorio NO cuesta más que el secuencial para el
    sistema de archivos, aunque el disco físico sí busque la pista
    (por eso el tema 06 prefiere el acceso secuencial).

CASOS LÍMITE
    - Escribir más allá del final: el archivo se extiende, y el hueco
      se rellena con bytes nulos (archivo disperso).
    - Leer más allá del final: devuelve menos bytes de los pedidos,
      o cadena vacía.
    - Posición negativa con whence=0: depende del sistema.

APLICACIONES
    - Bases de datos de registros fijos.
    - Índices sobre archivos ordenados.
    - Parchear binarios.
    - Logs rotativos: leer desde un offset conocido.

RELACIÓN CON OTROS TEMAS
    - El tema 06 muestra que para archivos enormes, el acceso
      ALEATORIO es mucho más lento que el secuencial en disco: cada
      seek puede forzar una búsqueda mecánica.
"""


def leer_en_posicion(ruta, posicion, tamano):
    """Lee `tamano` bytes desde `posicion`. O(k)."""
    with open(ruta, "rb") as f:
        f.seek(posicion)
        return f.read(tamano)


def escribir_en_posicion(ruta, posicion, datos):
    """Escribe `datos` en `posicion` sin tocar el resto."""
    # "r+b" lee y escribe SIN truncar el archivo
    with open(ruta, "r+b") as f:
        f.seek(posicion)
        f.write(datos)


if __name__ == "__main__":
    import os

    # Crear archivo con datos conocidos
    with open("test.bin", "wb") as f:
        f.write(b"ABCDEFGHIJ")

    # Leer desde una posición
    datos = leer_en_posicion("test.bin", 3, 4)
    print(f"Posición 3, 4 bytes: {datos}")
    assert datos == b"DEFG"

    # Leer desde el inicio
    assert leer_en_posicion("test.bin", 0, 5) == b"ABCDE"

    # Escribir en una posición
    escribir_en_posicion("test.bin", 5, b"XY")

    with open("test.bin", "rb") as f:
        contenido = f.read()
    print(f"Contenido modificado: {contenido}")

    # Escribir 2 bytes en la posición 5 reemplaza F y G (pos 5 y 6)
    assert contenido == b"ABCDEXYHIJ", "escribir 2 bytes en pos 5 reemplaza F y G"

    # El resto del archivo quedó intacto
    assert contenido[:5] == b"ABCDE", "el principio no cambió"
    assert contenido[7:] == b"HIJ", "el final no cambió"

    # Los tres orígenes de seek
    assert leer_en_posicion("test.bin", 0, 3) == b"ABC"        # whence=0

    # whence=2: desde el final (leer los últimos 3 bytes)
    with open("test.bin", "rb") as f:
        f.seek(-3, 2)
        assert f.read() == b"HIJ"
    print("Seek desde el final (whence=2): HIJ")

    # whence=1: avanzar desde la posición actual
    with open("test.bin", "rb") as f:
        f.seek(2, 0)                  # posición 2
        f.seek(1, 1)                  # avanzar 1 → posición 3
        assert f.read(2) == b"DE"
    print("Seek relativo (whence=1): verificado")

    # Actualizar varias regiones
    escribir_en_posicion("test.bin", 0, b"XX")
    escribir_en_posicion("test.bin", 9, b"ZZ")
    with open("test.bin", "rb") as f:
        c = f.read()
    # Posiciones 0-1 = XX, 5-6 = XY, 9 = Z (la Z extra extiende el archivo)
    assert c == b"XXCDEXYHIZZ", "cada escritura pisa solo su rango"
    assert len(c) == 11, "escribir en la posición 9 extiende 1 byte"
    print(f"Dos regiones modificadas: {c}")

    # Escribir más allá del FINAL: el archivo se extiende
    # con bytes nulos en el hueco (archivo disperso)
    # En este punto el archivo mide 11 bytes, así que el hueco es
    # el rango [11, 20) y el total queda en 23 bytes.
    escribir_en_posicion("test.bin", 20, b"FIN")
    with open("test.bin", "rb") as f:
        c_ext = f.read()
    print(f"\nEscritura más allá del final: tamaño {len(c_ext)}")
    assert len(c_ext) == 23, "el archivo se extendió hasta 23 bytes"
    assert c_ext[20:23] == b"FIN", "los datos quedan en la posición pedida"
    # El hueco entre el final previo (11) y la posición 20 son nulos
    assert c_ext[11:20] == b"\x00" * 9, "el hueco son bytes nulos"
    print(f"Hueco [11:20] rellenado con {len(c_ext[11:20])} bytes nulos")

    # Leer más allá del final: devuelve menos de lo pedido
    resultado = leer_en_posicion("test.bin", 20, 100)
    assert resultado == b"FIN", "solo hay 3 bytes disponibles"
    print(f"Lectura de 100 desde pos 20: {resultado} (solo 3 disponibles)")

    # FÓRMULA DE OFFSET: registros de tamaño fijo
    TAM = 4
    with open("registros.bin", "wb") as f:
        for i in range(10):
            f.write((i * 100).to_bytes(TAM, "little"))

    # El registro k está en la posición k × TAM
    for k in [0, 3, 7, 9]:
        pos = k * TAM
        valor = int.from_bytes(leer_en_posicion("registros.bin", pos, TAM), "little")
        assert valor == k * 100, f"registro {k} debería valer {k*100}"
        print(f"  Registro {k} (posición {pos}): {valor}")
    print("Fórmula posición = índice × tamaño verificada")

    os.remove("test.bin")
    os.remove("registros.bin")
    print("\n✓ Todas las pruebas pasaron")
