"""
Ejercicio 7: Acceso secuencial
Dificultad: Básico

Lee o escribe datos en orden, desde el principio hasta el final.
"""


def acceso_secuencial_lectura(ruta):
    """Lee un archivo secuencialmente."""
    with open(ruta, "r") as f:
        for linea in f:
            yield linea.strip()


def acceso_secuencial_escritura(ruta, datos):
    """Escribe datos secuencialmente."""
    with open(ruta, "w") as f:
        for dato in datos:
            f.write(f"{dato}\n")


if __name__ == "__main__":
    import os

    # Escritura secuencial
    datos = ["Línea 1", "Línea 2", "Línea 3"]
    acceso_secuencial_escritura("test.txt", datos)

    # Lectura secuencial
    lineas = list(acceso_secuencial_lectura("test.txt"))
    print(f"Líneas: {lineas}")

    assert lineas == datos
    os.remove("test.txt")
    print("\n✓ Todas las pruebas pasaron")
