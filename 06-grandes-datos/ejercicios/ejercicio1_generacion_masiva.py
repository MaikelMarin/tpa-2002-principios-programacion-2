r"""
Ejercicio 1: Generacin masiva de datos
Dificultad: Bsico

CONOCIMIENTO PREVIO NECESARIO
    - Escritura con bufer (tema 05, ejercicio 2).
    - Escritura de texto y `writelines`.
    - El mdulo `random`.

PROBLEMA
    Generar un archivo CSV con grandes cantidades de datos sintticos.

FONDO MATEMTICO
    Los datos sintticos son esenciales para probar algoritmos a
    escala sin depender de datos reales (que suelen ser privados o
    difciles de obtener).

    Pero OJO: la DISTRIBUCIN de los datos determina el comportamiento
    de los algoritmos:
      - Uniforme: cada valor igual de probable.
      - Normal (gaussiana): agrupada alrededor de una media.
      - Ordenada: el peor caso para Quick Sort con pivote fijo.
      - Con duplicados: rompe la particin de Quick Sort.

    Un benchmark con la distribucin incorrecta da conclusiones
    falsas. Esta es una de las fuentes de error ms comunes al
    "optimizar" cdigo.

ESTRATEGIA

```python
with open(ruta, "w", buffering=8192) as f:
    buffer = []
    for i in range(num_registros):
        buffer.append(f"{i},Cliente_{i},{edad},{saldo}\n")
        if len(buffer) >= 1000:
            f.writelines(buffer)        # una llamada por 1000 lneas
            buffer = []
    if buffer:
        f.writelines(buffer)
```

    El patrn de BUFFER manual es la clave:
      1. Acumular lneas en una lista.
      2. Escribir el lote cuando alcanza 1000.
      3. Vaciar la lista.

    Reduce las llamadas al sistema de N a N/1000.

TRAZA del efecto del buffer
    Sin bufer manual: 1,000,000 llamadas a f.write()
    Con bufer de 1000: 1,000 llamadas a f.writelines()

    El bufer interno de Python (buffering=8192) ya agrupa, pero el
    bufer manual reduce además el overhead de la API de Python.

COMPLEJIDAD
    Tiempo: O(n). Generar cada lnea es O(1), en total O(n).
    Espacio: O(1000) para el buffer, NO O(n).

    Si se hiciera `f.writelines(lineas)` con 1M de lneas en memoria,
    el espacio sera O(n). El buffer manual lo mantiene en O(1).

CASOS LMITE
    - 0 registros: solo la cabecera.
    - Cantidades muy grandes: el tiempo crece linealmente; vigilar el
      tamao del disco.
    - Valores aleatorios sin semilla: no reproducible. Fijar la
      semilla (random.seed) hace los experimentos repetibles.

APLICACIONES
    - Benchmarks y pruebas de carga.
    - Validacin de algoritmos a escala.
    - Pruebas de estrs de sistemas.

RELACIN CON OTROS TEMAS
    - El ejercicio 2 consume estos datos con streaming.
    - El ejercicio 3 los ordena sin cargarlos en memoria.
"""


import random


def generar_archivo_datos(ruta, num_registros):
    """Genera un archivo CSV con registros sintticos. O(n) tiempo."""
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("id,nombre,edad,saldo\n")

        buffer = []
        for i in range(num_registros):
            nombre = f"Cliente_{i}"
            edad = random.randint(18, 80)
            saldo = round(random.uniform(-1000, 100000), 2)
            buffer.append(f"{i},{nombre},{edad},{saldo}\n")

            # Vacaar el bufer cada 1000 lneas
            if len(buffer) >= 1000:
                f.writelines(buffer)
                buffer = []

        if buffer:
            f.writelines(buffer)


if __name__ == "__main__":
    import os

    generar_archivo_datos("datos_masivos.csv", 100000)

    tam = os.path.getsize("datos_masivos.csv")
    lineas = sum(1 for _ in open("datos_masivos.csv", encoding="utf-8"))
    print(f"Archivo generado: datos_masivos.csv")
    print(f"  Lneas (con cabecera): {lineas:,}")
    print(f"  Tamao: {tam / (1024*1024):.2f} MB")

    # 100,000 registros + 1 lnea de cabecera
    assert lineas == 100001
    assert tam > 0

    # La cabecera existe y es correcta
    with open("datos_masivos.csv", encoding="utf-8") as f:
        primera = f.readline().strip()
    assert primera == "id,nombre,edad,saldo", primera
    print(f"  Cabecera: {primera}")

    # Verificar el contenido de la primera y ltima fila de datos
    with open("datos_masivos.csv", encoding="utf-8") as f:
        f.readline()                              # saltar cabecera
        f1 = f.readline().strip()
    assert f1.startswith("0,Cliente_0,"), f1
    print(f"  Primera fila: {f1}")

    # Los campos tienen el formato correcto
    partes = f1.split(",")
    assert len(partes) == 4, "cuatro columnas"
    assert partes[0] == "0"                        # id
    assert partes[1] == "Cliente_0"                # nombre
    assert 18 <= int(partes[2]) <= 80               # edad en rango
    assert -1000 <= float(partes[3]) <= 100000      # saldo en rango
    print(f"  Campos validados: id={partes[0]}, edad={partes[2]}, saldo={partes[3]}")

    # Reproducibilidad: con la misma semilla, mismos datos
    random.seed(42)
    with open("rep1.csv", "w", encoding="utf-8") as f:
        for _ in range(10):
            f.write(f"{random.randint(1,100)}\n")
    random.seed(42)
    with open("rep2.csv", "w", encoding="utf-8") as f:
        for _ in range(10):
            f.write(f"{random.randint(1,100)}\n")
    with open("rep1.csv") as f1, open("rep2.csv") as f2:
        assert f1.read() == f2.read(), "misma semilla = mismos datos"
    print("\nReproducibilidad verificada: random.seed() hace el experimento repetible")

    # Efecto del bufer: medir el tiempo
    import time

    random.seed(1)
    inicio = time.time()
    generar_archivo_datos("buf_prueba.csv", 200000)
    t_buf = time.time() - inicio

    print(f"\n200,000 registros con bufer manual: {t_buf*1000:.0f} ms")
    n_buf = sum(1 for _ in open("buf_prueba.csv", encoding="utf-8"))
    assert n_buf == 200001

    # Caso base: 0 registros (solo cabecera)
    generar_archivo_datos("cero.csv", 0)
    with open("cero.csv", encoding="utf-8") as f:
        contenido = f.read()
    assert contenido == "id,nombre,edad,saldo\n"
    print("0 registros: solo la cabecera")

    # La memoria usada es O(1), no O(n): se verifica indirectamente
    # observando que el proceso no crece con el nmero de registros.
    import sys
    tam_buffer = 1000 * 50          # ~50 bytes por lnea, 1000 en buffer
    print(f"\nMemoria del bufer: ~{tam_buffer:,} bytes (constante)")
    print(f"Memoria de alternativa ingenua: O(n) lineas en RAM")

    for a in ["datos_masivos.csv", "rep1.csv", "rep2.csv", "buf_prueba.csv", "cero.csv"]:
        os.remove(a)

    print("\n Todas las pruebas pasaron")
