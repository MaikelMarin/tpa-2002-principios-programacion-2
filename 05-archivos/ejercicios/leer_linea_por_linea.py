"""
Ejercicio 3: Leer línea por línea
Dificultad: Básico

Lee un archivo de texto línea por línea de forma eficiente.
"""


def leer_lineas(ruta):
    """Lee un archivo línea por línea y retorna una lista."""
    lineas = []
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            lineas.append(linea.rstrip("\n"))
    return lineas


if __name__ == "__main__":
    import os

    with open("test.txt", "w") as f:
        f.write("Línea 1\nLínea 2\nLínea 3\n")

    lineas = leer_lineas("test.txt")
    print(f"Líneas: {lineas}")

    assert len(lineas) == 3
    assert lineas[0] == "Línea 1"
    os.remove("test.txt")
    print("\n✓ Todas las pruebas pasaron")
