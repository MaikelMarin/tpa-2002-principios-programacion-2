"""
Ejercicio 8: Copiar archivo binario
Dificultad: Básico

Copia un archivo binario de forma eficiente usando bloques.
"""


def copiar_binario(origen, destino, tamano_buffer=1024):
    """Copia un archivo binario usando un buffer."""
    with open(origen, "rb") as f_origen, open(destino, "wb") as f_destino:
        while True:
            bloque = f_origen.read(tamano_buffer)
            if not bloque:
                break
            f_destino.write(bloque)


if __name__ == "__main__":
    import os

    # Crear archivo de prueba
    with open("test_origen.bin", "wb") as f:
        f.write(b"\x00\x01\x02\x03" * 100)

    copiar_binario("test_origen.bin", "test_destino.bin")

    # Verificar
    with open("test_origen.bin", "rb") as f1, open("test_destino.bin", "rb") as f2:
        assert f1.read() == f2.read()

    os.remove("test_origen.bin")
    os.remove("test_destino.bin")
    print("✓ Todas las pruebas pasaron")
