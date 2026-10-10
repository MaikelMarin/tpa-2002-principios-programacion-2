r"""
Ejercicio 9: CSV a lista de diccionarios
Dificultad: Bsico

CONOCIMIENTO PREVIO NECESARIO
    - Mdulo csv de Python (teoria.md 6.1).
    - Diccionarios (00-fundamentos 8.6).
    - Lectura lnea por lnea (ejercicio 3).

PROBLEMA
    Leer un archivo CSV y convertir cada fila en un diccionario.

FONDO MATEMTICO
    CSV (Comma-Separated Values) es un formato tabular en texto plano.
    La primera lnea suele ser la CABECERA: los nombres de las columnas.

        nombre,edad,ciudad
        Ana,25,San Jose
        Luis,30,Heredia

    Convertir a diccionarios asocia cada columna con su valor:

        {"nombre": "Ana", "edad": "25", "ciudad": "San Jose"}

    Note que TODOS los valores quedan como strings: "25", no 25.
    Hay que convertir manualmente si se quiere operar con ellos.

POR QU NO USAR split(",")
    La tentacin es partir cada lnea por comas. FALLA en casos reales:

        "Garca, Juan",30,Madrid

    Aqu la primera comas est DENTRO de un campo entrecomillado. Con
    split(",") se partira en el lugar equivocado.

    El mdulo csv maneja: comillas, comas internas, saltos de lnea
    dentro de campos, y comillas escapadas.

ESTRATEGIA

```python
import csv

with open("datos.csv", newline="", encoding="utf-8") as f:
    for fila in csv.DictReader(f):
        print(fila["nombre"])       # acceso por nombre de columna
```

    Paramentros importantes:
      - newline="": evita que csv interprete mal los saltos en algunos
        sistemas. Es la forma recomendada por la documentacin.
      - encoding="utf-8": el problema de siempre.
      - DictReader: devuelve diccionarios usando la cabecera.

TRAZA
    Archivo: "nombre,edad\nAna,25\nLuis,30\n"

    DictReader lee la primera lnea -> claves: ["nombre", "edad"]
    Lnea 2 -> {"nombre": "Ana", "edad": "25"}
    Lnea 3 -> {"nombre": "Luis", "edad": "30"}

COMPLEJIDAD
    Tiempo: O(n) donde n es el tamao del archivo.
    Espacio: O(filas) si se acumula todo; O(1) si se procesa una a una.

CASOS LMITE
    - Archivo sin cabecera: DictReader usara la primera fila como
      cabecera y la PERDER como dato.
    - Filas con distinto nmeros de columnas: las faltantes quedan
      como None, las sobrantes se agrupan bajo la clave None.
    - Campos vacos: cadena vaca "".
    - Comillas dobles dentro de campos: csv las desescapa.

APLICACIONES
    - Importar datos de hojas de clculo.
    - Intercambio de datos entre sistemas.
    - Migracin de datos.

RELACIN CON OTROS TEMAS
    - El tema 06 muestra cmo procesar CSVs que no caben en memoria.
"""


import csv


def csv_a_diccionarios(archivo_csv):
    """Lee un CSV y devuelve una lista de diccionarios.

    Usa la primera lnea como cabecera.
    """
    with open(archivo_csv, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def diccionarios_a_csv(diccionarios, archivo_csv):
    """Escribe una lista de diccionarios a un CSV."""
    if not diccionarios:
        return

    campos = list(diccionarios[0].keys())
    with open(archivo_csv, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(diccionarios)


if __name__ == "__main__":
    import os

    # Datos de prueba
    datos = [
        {"nombre": "Ana", "edad": 25, "ciudad": "San Jose"},
        {"nombre": "Luis", "edad": 30, "ciudad": "Heredia"},
        {"nombre": "Carlos", "edad": 35, "ciudad": "Alajuela"},
    ]

    diccionarios_a_csv(datos, "test.csv")
    assert os.path.exists("test.csv")

    with open("test.csv", encoding="utf-8") as f:
        contenido = f.read()
    print(f"CSV escrito:\n{contenido}")

    # La cabecera se escribi primero
    assert contenido.startswith("nombre,edad,ciudad")
    assert "Ana" in contenido

    # Leer de vuelta
    resultado = csv_a_diccionarios("test.csv")
    print("Leido como diccionarios:")
    for fila in resultado:
        print(f"  {fila}")

    assert len(resultado) == 3
    assert resultado[0]["nombre"] == "Ana"
    assert resultado[1]["ciudad"] == "Heredia"
    assert resultado[2]["ciudad"] == "Alajuela"

    # OJO: los valores son STRINGS, no enteros
    assert resultado[0]["edad"] == "25", "csv devuelve texto"
    assert isinstance(resultado[0]["edad"], str)
    # Para operar hay que convertir
    assert int(resultado[0]["edad"]) == 25
    print(f"\nConvertido: edad de Ana = {int(resultado[0]['edad'])}")

    # Round-trip: escribir y leer da los mismos datos (como strings)
    for original, leido in zip(datos, resultado):
        for clave in original:
            assert str(original[clave]) == leido[clave], \
                f"discrepancia en {clave}"
    print("Round-trip verificado")

    # Caso base: CSV vacio (solo cabecera)
    diccionarios_a_csv([{"a": 1}], "solo_cabecera.csv")
    with open("solo_cabecera.csv", "w", encoding="utf-8") as f:
        f.write("a,b\n")
    assert csv_a_diccionarios("solo_cabecera.csv") == []
    print("CSV sin datos: lista vacia")

    # Lista vacia: no se escribe nada
    diccionarios_a_csv([], "vacio.csv")
    assert not os.path.exists("vacio.csv") or os.path.getsize("vacio.csv") == 0
    print("Lista vacia: no se escribe archivo")

    # Campos con comas: csv requiere entrecomillado
    with open("comas.csv", "w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(["nombre", "profesion"])
        escritor.writerow(["Juan Garcia", "Ingeniero, desarrollador"])

    r_comas = csv_a_diccionarios("comas.csv")
    assert r_comas[0]["nombre"] == "Juan Garcia"
    assert r_comas[0]["profesion"] == "Ingeniero, desarrollador", \
        "la coma interna se preservo"
    print(f"\nComa interna preservada: {r_comas[0]['profesion']!r}")

    # Demostrar que split("," SI falla aqui
    with open("comas.csv", encoding="utf-8") as f:
        lineas = f.read().splitlines()
    partes = lineas[1].split(",")
    print(f"  split(',') da: {partes} <- INCORRECTO, parte el campo")
    assert len(partes) != 2, "split no maneja las comas internas"

    # Campos vacios
    with open("vacios.csv", "w", encoding="utf-8") as f:
        f.write("a,b,c\n1,,3\n,,\n")
    r_vacios = csv_a_diccionarios("vacios.csv")
    assert r_vacios[0]["b"] == "", "campo vacio = cadena vacia"
    assert r_vacios[1]["a"] == ""
    print("Campos vacios manejados como cadenas vacias")

    # CSV grande
    muchos = [{"id": i, "valor": i * 2, "activo": "si" if i % 2 else "no"}
              for i in range(10000)]
    diccionarios_a_csv(muchos, "muchos.csv")
    r_muchos = csv_a_diccionarios("muchos.csv")
    assert len(r_muchos) == 10000
    assert r_muchos[9999]["valor"] == str(9999 * 2)
    print(f"\nCSV de 10,000 filas escrito y leido")

    # Nota: "vacio.csv" no se crea con una lista vacia, por eso se
    # comprueba su existencia antes de borrarlo.
    for a in ["test.csv", "solo_cabecera.csv", "comas.csv",
              "vacios.csv", "muchos.csv"]:
        os.remove(a)
    if os.path.exists("vacio.csv"):
        os.remove("vacio.csv")

    print("\n Todas las pruebas pasaron")
