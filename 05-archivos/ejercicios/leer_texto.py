"""
Ejercicio 1: Leer archivo de texto
Dificultad: Básico

Lee el contenido completo de un archivo de texto.
"""


def leer_archivo(ruta):
    """Lee y retorna el contenido completo de un archivo de texto."""
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    import os

    # Crear archivo de prueba
    with open("test.txt", "w") as f:
        f.write("Hola, mundo!\nSegunda línea\n")

    contenido = leer_archivo("test.txt")
    print(f"Contenido:\n{contenido}")

    assert "Hola, mundo!" in contenido
    assert "Segunda línea" in contenido
    os.remove("test.txt")
    print("\n✓ Todas las pruebas pasaron")
