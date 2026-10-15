r"""
Ejercicio 7: Acceso secuencial
Dificultad: Bsico

CONOCIMIENTO PREVIO NECESARIO
    - Leer lnea por lnea (ejercicio 3).
    - La diferencia entre acceso secuencial y aleatorio (teoria.md 5).
    - El concepto de buffer del sistema operativo.

PROBLEMA
    Procesar un archivo completo en orden, de principio a fin.

FONDO MATEMTICO
    El acceso secuencial recorre el archivo EN ORDEN. Es el modo ms
    rápido posible en disco, por una razn fsica:

    - Un disco duro mecnico (HDD) tiene un cabezal que se mueve
      fsicamente. Leer secuencialmente evita esos saltos (seeks).
    - Un SSD lee pginas, y el acceso secuencial aprovecha el
      read-ahead que hace el controlador.

    Resultado: el modo secuencial puede ser 10-100x ms rápido que el
    aleatorio sobre el mismo archivo, aunque ambos sean O(n) en
    complejidad.

ESTRATEGIA

```python
def acceso_secuencial_lectura(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:              # buffer gestionado por el SO
            yield linea.strip()

def acceso_secuencial_escritura(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        for dato in datos:
            f.write(f"{dato}\n")
```

    El generador (`yield`) es la forma idiomtica: procesa un elemento
    a la vez sin acumular nada en memoria.

TRAZA sobre un archivo de 3 lneas
    El SO lee un bloque (p. ej. 8 KB) que contiene las 3 lneas.
    El bucle devuelve una a una:
      iteracion 1: "Linea 1"
      iteracion 2: "Linea 2"
      iteracion 3: "Linea 3"
    Fin del archivo: el bucle termina.

    Note: las tres lneas caban en un solo bloque, as que solo hubo
    UNA lectura de disco. Eso es lo que hace eficiente al secuencial.

COMPLEJIDAD
    Tiempo: O(n) con constante PEQUEA (pocas lecturas de disco).
    Espacio: O(tamao del buffer + lnea ms larga).

    Compare con el acceso aleatorio, que hace O(n) saltos: cada uno
    puede costar milisegundos en HDD.

POR QU EL SECUENCIAL GANA EN LA PRCTICA
    Es la razn por la que:
      - Merge Sort se usa para ordenamiento externo (tema 06).
      - Los logs se escriben en append, nunca en medio.
      - Las bases de datos hacen "sequential scans" cuando estiman
        que van a leer una fraccin grande de la tabla.

CUANDO S NECESARIO EL ALEATORIO
    - Cuando se busca UNA aguja en un pajar (acceso por ndice).
    - Cuando se procesa una fraccin muy pequea del archivo.

APLICACIONES
    - Procesamiento de logs y CSVs grandes.
    - Ordenamiento externo.
    - Compresin y cifrado de archivos.

RELACIN CON OTROS TEMAS
    - El tema 06 (grandes datos) se apoya completamente en el acceso
      secuencial: es la nica forma viable de procesar archivos que
      no caben en memoria.
"""


def acceso_secuencial_lectura(ruta):
    """Lee un archivo secuencialmente, lnea por lnea. Generador."""
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            yield linea.rstrip("\n")


def acceso_secuencial_escritura(ruta, datos):
    """Escribe datos secuencialmente, uno por lnea."""
    with open(ruta, "w", encoding="utf-8") as f:
        for dato in datos:
            f.write(f"{dato}\n")


if __name__ == "__main__":
    import os

    # Escritura secuencial
    datos = ["Linea 1", "Linea 2", "Linea 3"]
    acceso_secuencial_escritura("test.txt", datos)

    assert os.path.exists("test.txt")
    with open("test.txt", encoding="utf-8") as f:
        contenido = f.read()
    assert contenido == "Linea 1\nLinea 2\nLinea 3\n"
    print(f"Escritura secuencial: {contenido!r}")

    # Lectura secuencial: devuelve lo mismo en el mismo orden
    resultado = list(acceso_secuencial_lectura("test.txt"))
    assert resultado == datos, "el orden se preserva"
    print(f"Lectura secuencial: {resultado}")

    # Round-trip
    assert list(acceso_secuencial_lectura("test.txt")) == datos

    # Casos base
    with open("vacio.txt", "w", encoding="utf-8") as f:
        pass
    assert list(acceso_secuencial_lectura("vacio.txt")) == []
    print("Archivo vacio: lista vacia")

    acceso_secuencial_escritura("uno.txt", ["único"])
    assert list(acceso_secuencial_lectura("uno.txt")) == ["único"]

    # El generador NO acumula: memoria constante
    import sys

    lineas_grandes = [f"Linea {i}" for i in range(200000)]
    acceso_secuencial_escritura("grande.txt", lineas_grandes)
    tam = os.path.getsize("grande.txt")
    print(f"\nArchivo de {tam:,} bytes ({len(lineas_grandes):,} lineas)")

    # Contar consumiendo el generador: memoria O(1)
    contador = 0
    for _ in acceso_secuencial_lectura("grande.txt"):
        contador += 1
    assert contador == 200000
    print(f"  Contadas {contador:,} lineas con memoria O(1)")

    # Consumo perezoso: parar a la mitad
    gen = acceso_secuencial_lectura("grande.txt")
    primeras = []
    for i, linea in enumerate(gen):
        if i >= 5:
            break
        primeras.append(linea)
    assert primeras == ["Linea 0", "Linea 1", "Linea 2", "Linea 3", "Linea 4"]
    print(f"  Consumo perezoso, primeras 5: {primeras}")

    # Filtrar sin cargar: buscar una lnea concreta
    objetivo = "Linea 199999"
    encontrada = None
    for linea in acceso_secuencial_lectura("grande.txt"):
        if linea == objetivo:
            encontrada = linea
            break
    assert encontrada == objetivo
    print(f"  Busqueda y parada temprana: {encontrada}")

    # Demostrar que el secuencial NO lee todo cuando se para antes
    # (el generador permite abandonar a mitad de camino)
    import time

    # Secuencial: recorrer 100,000 lineas
    inicio = time.time()
    n = 0
    for _ in acceso_secuencial_lectura("grande.txt"):
        n += 1
        if n >= 100000:
            break
    t_seq = time.time() - inicio
    print(f"\n  Recorridas 100,000 lineas: {t_seq*1000:.0f} ms")

    # Aleatorio: leer 100,000 veces desde posiciones dispersas
    with open("grande.txt", "rb") as f:
        tamano = os.path.getsize("grande.txt")
        inicio = time.time()
        import random
        random.seed(221)
        for _ in range(100000):
            pos = random.randrange(0, tamano - 10)
            f.seek(pos)
            f.read(10)
    t_ale = time.time() - inicio
    print(f"  100,000 lecturas aleatorias: {t_ale*1000:.0f} ms")
    print(f"  Diferencia: el acceso aleatorio cuesta mas por salto")

    for a in ["test.txt", "vacio.txt", "uno.txt", "grande.txt"]:
        os.remove(a)

    print("\n Todas las pruebas pasaron")
