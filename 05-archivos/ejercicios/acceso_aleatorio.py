"""
Ejercicio 8: Acceso aleatorio
Dificultad: Intermedio

Manipula el puntero de lectura/escritura para acceder directamente.
"""


def leer_en_posicion(ruta, posicion, tamano):
    """Lee un número específico de bytes desde una posición."""
    with open(ruta, "rb") as f:
        f.seek(posicion)
        return f.read(tamano)


def escribir_en_posicion(ruta, posicion, datos):
    """Escribe datos en una posición específica."""
    with open(ruta, "r+b") as f:
        f.seek(posicion)
        f.write(datos)


if __name__ == "__main__":
    import os

    # Crear archivo con datos conocidos
    with open("test.bin", "wb") as f:
        f.write(b"ABCDEFGHIJ")

    # Leer desde posición 3
    datos = leer_en_posicion("test.bin", 3, 4)
    print(f"Datos en posición 3: {datos}")

    # Escribir en posición 5
    escribir_en_posicion("test.bin", 5, b"XY")

    with open("test.bin", "rb") as f:
        contenido = f.read()
    print(f"Contenido modificado: {contenido}")

    assert datos == b"DEFG"
    assert contenido == b"ABCDEFXYIJ"
    os.remove("test.bin")
    print("\n✓ Todas las pruebas pasaron")
