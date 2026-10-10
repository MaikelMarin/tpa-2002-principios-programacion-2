"""
Ejercicio 9: CSV a lista de diccionarios
Dificultad: Básico

Lee un archivo CSV y convierte cada fila en un diccionario.
"""


import csv


def csv_a_diccionarios(archivo_csv):
    """Lee un CSV y retorna una lista de diccionarios."""
    with open(archivo_csv, "r", newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        return list(lector)


def diccionarios_a_csv(diccionarios, archivo_csv):
    """Escribe una lista de diccionarios a un CSV."""
    if not diccionarios:
        return
    campos = diccionarios[0].keys()
    with open(archivo_csv, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(diccionarios)


if __name__ == "__main__":
    import os

    # Crear CSV de prueba
    datos = [
        {"nombre": "Ana", "edad": 25, "ciudad": "San José"},
        {"nombre": "Luis", "edad": 30, "ciudad": "Heredia"},
        {"nombre": "Carlos", "edad": 35, "ciudad": "Alajuela"}
    ]

    diccionarios_a_csv(datos, "test.csv")
    resultado = csv_a_diccionarios("test.csv")

    print("CSV leído como diccionarios:")
    for fila in resultado:
        print(f"  {fila}")

    assert len(resultado) == 3
    assert resultado[0]["nombre"] == "Ana"
    os.remove("test.csv")
    print("\n✓ Todas las pruebas pasaron")
