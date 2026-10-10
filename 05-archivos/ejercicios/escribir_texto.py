"""
Ejercicio 2: Escribir archivo de texto
Dificultad: Básico

Escribe contenido en un archivo de texto (sobrescribe si existe).
"""


def escribir_archivo(ruta, contenido):
    """Escribe contenido en un archivo de texto."""
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)


if __name__ == "__main__":
    import os

    escribir_archivo("test.txt", "Hola, mundo!\n")
    escribir_archivo("test.txt", "Sobrescrito!\n")  # Sobrescribe

    with open("test.txt", "r") as f:
        contenido = f.read()

    print(f"Contenido: {contenido}")
    assert contenido == "Sobrescrito!\n"
    os.remove("test.txt")
    print("\n✓ Todas las pruebas pasaron")
