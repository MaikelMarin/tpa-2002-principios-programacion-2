r"""
Ejercicio 5: Escritura binaria
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Modo binario "wb" (teoria.md §3.1).
    - El módulo `struct` (00-fundamentos §10.7).
    - Diferencia entre texto y binario (teoria.md §2).

PROBLEMA
    Escribir datos en formato binario, empaquetando números en su
    representación nativa en bytes.

FONDO MATEMÁTICO
    Un entero como 42 se puede almacenar de dos formas:

        Texto:    "42"     → 2 bytes (0x34, 0x32)
        Binario:  42       → 4 bytes (0x2A, 0x00, 0x00, 0x00)

    El binario es más rápido de leer y escribir (no hay que parsear
    texto) pero depende del estándar de representación (endianness,
    tamaño de tipos). Por eso los archivos binarios necesitan un
    FORMATO documentado.

    Endianness:
        Little-endian (<): el byte menos significativo primero.
        Big-endian (>):    el byte más significativo primero.
    x86 y ARM usan little-endian. Los formatos de red usan big-endian.

ESTRATEGIA

```python
import struct

# Empaquetar: "i" = int 4 bytes, "f" = float 4 bytes
datos = struct.pack("<if", 42, 3.14)
with open("datos.bin", "wb") as f:
    f.write(datos)

# Desempaquetar
with open("datos.bin", "rb") as f:
    entero, flotante = struct.unpack("<if", f.read(8))
```

    Códigos de formato:
        i  → int (4 bytes)
        f  → float (4 bytes)
        d  → double (8 bytes)
        q  → long long (8 bytes)
        ?  → bool (1 byte)
        s  → string de longitud fija

    El prefijo "<" o ">" es OBLIGATORIO para ser portátil: si se omite,
    struct usa el orden nativo de la máquina y el archivo no será
    legible en una arquitectura distinta.

TRAZA de struct.pack("<if", 42, 3.14)
    "<"  → little-endian
    "i"  → empaquetar 42 como 4 bytes: 2A 00 00 00
    "f"  → empaquetar 3.14 como 4 bytes (IEEE 754)

    Resultado: b'\x2a\x00\x00\x00\xc3\xf5H@'  (8 bytes)

    Verificación al leer:
        struct.unpack("<if", b'\x2a\x00\x00\x00\xc3\xf5H@')  → (42, 3.14)

COMPLEJIDAD
    Tiempo: O(n) donde n es el número de bytes escritos/leídos.
    Espacio: O(n) para el buffer.

    El empaquetado es O(1) por campo: struct conoce el tamaño de cada
    tipo y escribe directamente.

PRECISIÓN DE PUNTO FLOTANTE
    3.14 no se puede representar exactamente en binario (IEEE 754).
    Al leer se obtiene 3.140000104904175, no 3.14 exacto.

    Consecuencia práctica: para dineros NUNCA uses float. Usa enteros
    en centavos, o decimal.Decimal.

APLICACIONES
    - Formatos de imagen (BMP, PNG tienen cabeceras binarias).
    - Protocolos de red.
    - Bases de datos y archivos de registro.
    - Intercambio entre programas en distinto lenguaje.

RELACIÓN CON OTROS TEMAS
    - El acceso aleatorio (ejercicio 8) se apoya en tamaños fijos:
      si cada registro mide 8 bytes, el registro k está en 8k.
"""


import struct


def escribir_binario(ruta, datos):
    """Escribe un diccionario con entero, flotante y bytes."""
    with open(ruta, "wb") as f:
        # Empaquetar: int (4) + float (4) + bytes crudos
        f.write(struct.pack("<i", datos["entero"]))
        f.write(struct.pack("<f", datos["flotante"]))
        f.write(datos["bytes"])


def leer_binario(ruta):
    """Lee el archivo binario y lo interpreta con el mismo formato."""
    with open(ruta, "rb") as f:
        entero = struct.unpack("<i", f.read(4))[0]
        flotante = struct.unpack("<f", f.read(4))[0]
        bytes_data = f.read()
    return {"entero": entero, "flotante": flotante, "bytes": bytes_data}


if __name__ == "__main__":
    import os

    datos = {"entero": 42, "flotante": 3.14, "bytes": b"\x00\x01\x02\x03"}
    escribir_binario("test.bin", datos)

    # Verificar el tamaño: 4 + 4 + 4 = 12 bytes
    assert os.path.getsize("test.bin") == 12
    print(f"Tamaño del archivo: {os.path.getsize('test.bin')} bytes")

    # Verificar el contenido byte a byte
    with open("test.bin", "rb") as f:
        crudo = f.read()
    print(f"Bytes: {crudo!r}")
    assert crudo[:4] == b"\x2a\x00\x00\x00", "42 en little-endian de 4 bytes"
    assert crudo[8:] == b"\x00\x01\x02\x03", "los bytes crudos al final"

    # Leer y verificar
    leidos = leer_binario("test.bin")
    print(f"Datos leídos: {leidos}")

    assert leidos["entero"] == 42, "el entero se conserva exacto"
    assert leidos["bytes"] == b"\x00\x01\x02\x03"
    # El float NO es exacto: 3.14 no es representable en IEEE 754
    assert abs(leidos["flotante"] - 3.14) < 0.001
    print(f"Float leído: {leidos['flotante']} (no exactamente 3.14)")

    # Endianness: el mismo dato en big-endian da bytes distintos
    be = struct.pack(">i", 42)
    le = struct.pack("<i", 42)
    print(f"\n42 little-endian: {le!r}")
    print(f"42 big-endian:    {be!r}")
    assert le == b"\x2a\x00\x00\x00"
    assert be == b"\x00\x00\x00\x2a"
    assert le != be, "el orden de bytes cambia la representación"

    # Ambos se desempaquetan correctamente con el formato correcto
    assert struct.unpack("<i", le)[0] == 42
    assert struct.unpack(">i", be)[0] == 42
    # Pero NO con el formato equivocado
    assert struct.unpack("<i", be)[0] != 42, "interpretar mal da basura"

    # Tamaños de los tipos
    tamanios = {
        "i (int)": len(struct.pack("<i", 0)),
        "q (long long)": len(struct.pack("<q", 0)),
        "f (float)": len(struct.pack("<f", 0)),
        "d (double)": len(struct.pack("<d", 0)),
        "? (bool)": len(struct.pack("<?", True)),
        "h (short)": len(struct.pack("<h", 0)),
    }
    print("\nTamaños de tipos:")
    for nombre, tam in tamanios.items():
        print(f"  {nombre}: {tam} bytes")

    # Valores extremos de cada tipo
    assert struct.unpack("<i", struct.pack("<i", 2147483647))[0] == 2147483647
    assert struct.unpack("<i", struct.pack("<i", -2147483648))[0] == -2147483648
    print("\nint32 cubre [-2147483648, 2147483647]")

    # Desbordamiento: struct lanza error
    try:
        struct.pack("<i", 2 ** 40)             # no cabe en 4 bytes
        raise AssertionError("debía lanzar error")
    except struct.error:
        print("Desbordamiento detectado correctamente")

    # Precisión de punto flotante
    exacto = struct.unpack("<d", struct.pack("<d", 0.1))[0]
    print(f"\n0.1 en double: {exacto!r}")
    assert exacto == 0.1, "0.1 se representa igual al leerlo"
    aproximado = struct.unpack("<f", struct.pack("<f", 0.1))[0]
    print(f"0.1 en float:  {aproximado!r}")
    assert aproximado != 0.1, "en float simple, 0.1 pierde precisión"

    # REGLA: para dinero, usar enteros
    precio_centavos = 3140
    assert precio_centavos / 100 == 31.40
    print("\nPara dinero: guardar centavos como entero (3140 = 31.40)")

    os.remove("test.bin")
    print("\n✓ Todas las pruebas pasaron")
