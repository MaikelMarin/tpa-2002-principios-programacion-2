"""
Solución 3: Ordenamiento externo con multiprocessing
Dificultad: Experto

Versión paralela que usa múltiples procesos para la fase de ordenamiento.
"""

import tempfile
import heapq
import os
from multiprocessing import Pool
import random
import time


def ordenar_bloque(datos):
    """Ordena un bloque de datos (para multiprocessing)."""
    datos.sort()
    return datos


def ordenamiento_externo_paralelo(archivo_entrada, archivo_salida, tamano_bloque=10000):
    """Ordena un archivo grande usando ordenamiento externo paralelo."""
    inicio = time.time()

    # Fase 1: Dividir y ordenar bloques en paralelo
    bloques = []
    with open(archivo_entrada, "r") as f:
        bloque = []
        for linea in f:
            bloque.append(int(linea.strip()))
            if len(bloque) >= tamano_bloque:
                bloques.append(bloque)
                bloque = []
        if bloque:
            bloques.append(bloque)

    print(f"Ordenando {len(bloques)} bloques en paralelo...")
    with Pool() as pool:
        bloques_ordenados = pool.map(ordenar_bloque, bloques)

    # Fase 2: Mezclar usando heap
    print("Mezclando bloques...")
    iteradores = [iter(b) for b in bloques_ordenados]
    with open(archivo_salida, "w") as salida:
        heap = []
        for i, it in enumerate(iteradores):
            try:
                valor = next(it)
                heapq.heappush(heap, (valor, i))
            except StopIteration:
                pass
        while heap:
            valor, idx = heapq.heappop(heap)
            salida.write(f"{valor}\n")
            try:
                valor = next(iteradores[idx])
                heapq.heappush(heap, (valor, idx))
            except StopIteration:
                pass

    tiempo = time.time() - inicio
    print(f"Ordenamiento completado en {tiempo:.2f}s")


if __name__ == "__main__":
    # Generar datos
    print("Generando datos de prueba...")
    with open("numeros_desordenados.txt", "w") as f:
        for _ in range(500000):
            f.write(f"{random.randint(1, 10000000)}\n")

    ordenamiento_externo_paralelo("numeros_desordenados.txt", "numeros_ordenados.txt")
