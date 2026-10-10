"""
Ejercicio 3: Ordenamiento externo (External Sort)
Dificultad: Experto

Ordena un archivo de texto con números que no cabe en memoria.
"""

import tempfile
import heapq
import os


def ordenamiento_externo(archivo_entrada, archivo_salida, tamano_bloque=10000):
    """Ordena un archivo grande usando ordenamiento externo."""
    # Fase 1: Dividir, ordenar y guardar bloques
    archivos_temporales = []
    with open(archivo_entrada, "r") as f:
        bloque = []
        for linea in f:
            bloque.append(int(linea.strip()))
            if len(bloque) >= tamano_bloque:
                bloque.sort()
                temp = tempfile.NamedTemporaryFile(mode="w+", delete=False)
                for num in bloque:
                    temp.write(f"{num}\n")
                temp.close()
                archivos_temporales.append(temp.name)
                bloque = []
        if bloque:
            bloque.sort()
            temp = tempfile.NamedTemporaryFile(mode="w+", delete=False)
            for num in bloque:
                temp.write(f"{num}\n")
            temp.close()
            archivos_temporales.append(temp.name)

    # Fase 2: Mezclar usando heap
    archivos_abiertos = [open(f, "r") for f in archivos_temporales]
    with open(archivo_salida, "w") as salida:
        heap = []
        for i, f in enumerate(archivos_abiertos):
            linea = f.readline()
            if linea:
                heapq.heappush(heap, (int(linea.strip()), i))
        while heap:
            valor, idx = heapq.heappop(heap)
            salida.write(f"{valor}\n")
            linea = archivos_abiertos[idx].readline()
            if linea:
                heapq.heappush(heap, (int(linea.strip()), idx))

    # Limpiar
    for f in archivos_abiertos:
        f.close()
    for temp in archivos_temporales:
        os.unlink(temp)

    print(f"Ordenamiento externo completado: {archivo_entrada} → {archivo_salida}")


if __name__ == "__main__":
    import random
    # Generar archivo con 100000 números
    with open("numeros_desordenados.txt", "w") as f:
        for _ in range(100000):
            f.write(f"{random.randint(1, 1000000)}\n")

    ordenamiento_externo("numeros_desordenados.txt", "numeros_ordenados.txt")
