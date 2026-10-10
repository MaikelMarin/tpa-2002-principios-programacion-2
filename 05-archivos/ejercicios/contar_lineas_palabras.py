"""
Ejercicio 9: Contar líneas, palabras y caracteres
Dificultad: Básico

Cuenta líneas, palabras y caracteres de un archivo de texto.
"""


def contar_estadisticas(ruta):
    """Cuenta líneas, palabras y caracteres de un archivo."""
    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read()
    lineas = contenido.split("\n")
    palabras = contenido.split()
    caracteres = len(contenido)
    return {
        "lineas": len(lineas),
        "palabras": len(palabras),
        "caracteres": caracteres
    }


if __name__ == "__main__":
    import os

    with open("test.txt", "w") as f:
        f.write("Hola mundo\nSegunda línea\nTercera línea\n")

    stats = contar_estadisticas("test.txt")
    print(f"Estadísticas: {stats}")

    assert stats["lineas"] == 3
    assert stats["palabras"] == 6
    os.remove("test.txt")
    print("\n✓ Todas las pruebas pasaron")
