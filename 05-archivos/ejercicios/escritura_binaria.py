"""
Ejercicio 5: Escritura binaria
Dificultad: Intermedio

Escribe datos en formato binario.
"""


import struct


def escribir_binario(ruta, datos):
    """Escribe datos en formato binario."""
    with open(ruta, "wb") as f:
        f.write(struct.pack("<i", datos["entero"]))
        f.write(struct.pack("<f", datos["flotante"]))
        f.write(datos["bytes"])


def leer_binario(ruta):
    """Lee datos en formato binario."""
    with open(ruta, "rb") as f:
        entero = struct.unpack("<i", f.read(4))[0]
        flotante = struct.unpack("<f", f.read(4))[0]
        bytes_data = f.read()
    return {"entero": entero, "flotante": flotante, "bytes": bytes_data}


if __name__ == "__main__":
    import os

    datos = {"entero": 42, "flotante": 3.14, "bytes": b"\x00\x01\x02\x03"}
    escribir_binario("test.bin", datos)

    leidos = leer_binario("test.bin")
    print(f"Datos leídos: {leidos}")

    assert leidos["entero"] == 42
    assert abs(leidos["flotante"] - 3.14) < 0.01
    assert leidos["bytes"] == b"\x00\x01\x02\x03"
    os.remove("test.bin")
    print("\n✓ Todas las pruebas pasaron")
