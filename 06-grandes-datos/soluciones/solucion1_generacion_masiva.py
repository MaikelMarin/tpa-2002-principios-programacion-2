r"""
Ejercicio 1 (solución): Generacin masiva optimizada con bufer
Dificultad: Bsico

CONOCIMIENTO PREVIO NECESARIO
    - Ejercicio 1 (enunciado): la versión base.
    - Escritura con bufer y su efecto medible.

PROBLEMA
    Optimizar la generacin masiva escribiendo por bloques, y medir
    el efecto real del bufer.

FONDO MATEMTICO
    El coste de escribir N lneas se descompone en dos partes:

        Coste total = (llamadas de escritura) x (coste por llamada)
                    = (N / B) x C      donde B es el tamao del bufer

    Si B = 1 (escribir lnea a lnea): N llamadas.
    Si B = 1000: N/1000 llamadas.

    El coste por llamada tiene dos componentes:
      1. Overhead fijo de Python/API (independiente de B).
      2. Trabajo real proporcional a los bytes (no cambia).

    Con B grande, el overhead fijo se amortiza. El trabajo real no se
    reduce, as que hay un lmite: pasado cierto bufer, no se gana ms.

ESTRATEGIA
    Adems de `buffering=8192` (bufer del sistema operativo), acumular
    un bufer MANUAL en Python:

```python
with open(ruta, "w", buffering=8192) as f:
    buffer = []
    for i in range(num_registros):
        buffer.append(linea)
        if len(buffer) >= 1000:
            f.writelines(buffer)      # UNA llamda por 1000 lneas
            buffer = []
    if buffer:
        f.writelines(buffer)          # no olvidar el resto
```

    Son DOS niveles de bufer:
      1. `buffering=8192`: bufer del SISTEMA OPERATIVO.
      2. La lista `buffer`: bufer de PYTHON, que reduce llamadas.

    El punto 2 es fcil de olvidar, y es el que ms efecto tiene en
    Python porque elimina overhead del intrprete.

EL ERROR CLSICO: OLVIDAR EL LTIMO BLOQUE
    Si el nmero de lneas no es mltiplo del bufer, el ltimo bloque
    parcial se queda en la lista sin escribirse. Hay que vaciarlo
    tras el bucle:

        if buffer:
            f.writelines(buffer)

    Sin esas dos lneas, se pierden datos silenciosamente.

TRAZA con 2500 registros y bufer de 1000
    i=0..999    acumular -> buffer tiene 1000 -> escribir, vaciar
    i=1000..1999 acumular -> buffer tiene 1000 -> escribir, vaciar
    i=2000..2499 acumular -> buffer tiene 500
    Fin del bucle -> if buffer: escribir los 500 restantes

    3 llamadas a writelines, no 2500 a write.

COMPLEJIDAD
    Tiempo: O(n), con constante menor gracias a menos llamadas.
    Espacio: O(B) para el bufer, NO O(n).

DEMOSTRACIN DE CORRECCIN
    Cada lnea se aade al bufer exactamente una vez. El bufer se vaca
    cuando llega a B elementos o al final del bucle. Luego cada lnea
    se escribe exactamente una vez y en orden. 

APLICACIONES
    - Exportacin de datos masivos.
    - Generacin de archivos de log.
    - Cualquier escritura de muchos registros pequeos.

RELACIN CON OTROS TEMAS
    - El ejercicio 2 consume el archivo generado con streaming.
"""


import random


def generar_archivo_optimizado(ruta, num_registros, tamano_buffer=1000):
    """Genera CSV con bufer manual. O(n) tiempo, O(tamano_buffer) memoria."""
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("id,nombre,edad,saldo\n")

        buffer = []
        for i in range(num_registros):
            buffer.append(
                f"{i},Cliente_{i},{random.randint(18, 80)},"
                f"{round(random.uniform(-1000, 100000), 2)}\n"
            )

            # Vaciar al alcanzar el tamao de bufer
            if len(buffer) >= tamano_buffer:
                f.writelines(buffer)
                buffer = []

        # NO OLVIDAR el ltimo bloque parcial
        if buffer:
            f.writelines(buffer)


def generar_sin_buffer(ruta, num_registros):
    """Versin ingenua: una llamada a write por lnea. Para comparar."""
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("id,nombre,edad,saldo\n")
        for i in range(num_registros):
            f.write(
                f"{i},Cliente_{i},{random.randint(18, 80)},"
                f"{round(random.uniform(-1000, 100000), 2)}\n"
            )


if __name__ == "__main__":
    import os
    import time

    n = 1000000

    # --- Versin optimizada ---
    random.seed(1)
    inicio = time.time()
    generar_archivo_optimizado("datos_masivos.csv", n)
    t_opt = time.time() - inicio
    tam_opt = os.path.getsize("datos_masivos.csv")

    print(f"con bufer manual:")
    print(f"  Registros: {n:,}")
    print(f"  Tamao:     {tam_opt / (1024*1024):.2f} MB")
    print(f"  Tiempo:    {t_opt:.2f}s")

    # Verificar que est completo (no se perdi el ltimo bloque)
    lineas = sum(1 for _ in open("datos_masivos.csv", encoding="utf-8"))
    assert lineas == n + 1, f"se perdan datos: {lineas} != {n+1}"
    print(f"  Lneas:    {lineas:,} (completo, sin datos perdidos)")
    os.remove("datos_masivos.csv")

    # --- Comparacin con la versión sin bufer ---
    random.seed(1)
    inicio = time.time()
    generar_sin_buffer("datos_ingenuos.csv", n)
    t_sin = time.time() - inicio
    os.remove("datos_ingenuos.csv")

    print(f"\nsin bufer manual:")
    print(f"  Tiempo: {t_sin:.2f}s")
    if t_opt > 0:
        print(f"  Mejora:  {t_sin / t_opt:.2f}x mas rapido con bufer")

    # --- El último bloque parcial se escribe ---
    for n_prueba, buffer_esp in [(2500, 1000), (999, 1000), (1, 1000), (1000, 1000)]:
        generar_archivo_optimizado("parcial.csv", n_prueba, tamano_buffer=buffer_esp)
        lineas = sum(1 for _ in open("parcial.csv", encoding="utf-8"))
        assert lineas == n_prueba + 1, \
            f"fallo con n={n_prueba}: {lineas} != {n_prueba + 1}"
        print(f"  n={n_prueba}, bufer={buffer_esp}: {lineas - 1} registros OK")
    os.remove("parcial.csv")

    print("\n Todas las pruebas pasaron")
