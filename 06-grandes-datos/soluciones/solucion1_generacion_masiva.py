"""
Solución 1: Generación masiva de datos optimizada
Dificultad: Básico

Versión optimizada que minimiza el uso de memoria.
"""

import random
import os
import time


def generar_archivo_optimizado(ruta, num_registros):
    """Genera archivo CSV usando buffer de escritura."""
    inicio = time.time()
    with open(ruta, "w", buffering=8192) as f:
        f.write("id,nombre,edad,saldo\n")
        buffer = []
        for i in range(num_registros):
            nombre = f"Cliente_{i}"
            edad = random.randint(18, 80)
            saldo = round(random.uniform(-1000, 100000), 2)
            buffer.append(f"{i},{nombre},{edad},{saldo}\n")
            if len(buffer) >= 10000:
                f.writelines(buffer)
                buffer = []
        if buffer:
            f.writelines(buffer)

    tiempo = time.time() - inicio
    tamano = os.path.getsize(ruta) / (1024*1024)
    print(f"Archivo generado: {ruta}")
    print(f"Registros: {num_registros:,}")
    print(f"Tamaño: {tamano:.2f} MB")
    print(f"Tiempo: {tiempo:.2f}s")


if __name__ == "__main__":
    generar_archivo_optimizado("datos_masivos.csv", 1000000)
