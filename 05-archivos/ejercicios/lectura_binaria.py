"""
Ejercicio 6: Lectura binaria
Dificultad: Intermedio

Lee datos en formato binario con diferentes tipos de datos.
"""


import struct


def leer_entero(ruta, posicion=0):
    """Lee un entero de 4 bytes desde una posición específica."""
    with open(ruta, "rb") as f:
        f.seek(posicion)
        return struct.unpack("<i", f.read(4))[0]


def leer_flotante(ruta, posicion=0):
    """Lee un flotante de 4 bytes desde una posición específica."""
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

    assert entero == 12345
    assert abs(flotante - 2.718) < 0.001
    os.remove("test.bin")
    print("\n✓ Todas las pruebas pasaron")
