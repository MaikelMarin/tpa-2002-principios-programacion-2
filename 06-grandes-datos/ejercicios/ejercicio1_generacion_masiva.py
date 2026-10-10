"""
Ejercicio 1: Generación masiva de datos
Dificultad: Básico

Genera archivos de texto con grandes cantidades de datos sintéticos.
"""

import random
import os


def generar_archivo_datos(ruta, num_registros):
    """Genera un archivo CSV con registros sintéticos."""
    with open(ruta, "w") as f:
        f.write("id,nombre,edad,saldo\n")
        for i in range(num_registros):
            nombre = f"Cliente_{i}"
            edad = random.randint(18, 80)
            saldo = round(random.uniform(-1000, 100000), 2)
            f.write(f"{i},{nombre},{edad},{saldo}\n")
    print(f"Archivo generado: {ruta} con {num_registros} registros")
    print(f"Tamaño: {os.path.getsize(ruta) / (1024*1024):.2f} MB")


if __name__ == "__main__":
    generar_archivo_datos("datos_masivos.csv", 100000)
