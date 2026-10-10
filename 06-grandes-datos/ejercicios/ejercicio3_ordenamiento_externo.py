r"""
Ejercicio 3: Ordenamiento externo (External Sort)
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - Merge Sort (tema 02, ejercicio 5): la base del algoritmo.
    - Streaming (teoria.md 2): la fase de mezcla lee secuencialmente.
    - Heap (00-fundamentos 8.6): la mezcla de k vas.
    - Archivos de texto (tema 05).

PROBLEMA
    Ordenar un archivo con nmeros que NO cabe en memoria.

FONDO MATEMTICO
    La estrategia tiene dos fases (teoria.md 3.2):

    FASE 1 — Dividir y ordenar (runs):
      1. Leer bloques de tamao M (lo que cabe en RAM).
      2. Ordenar cada bloque EN MEMORIA (Quick Sort es ideal).
      3. Escribir cada bloque ordenado a un archivo temporal.

    FASE 2 — Mezclar (merge k-vas):
      1. Abrir todos los temporales.
      2. Mantener un heap con el primer elemento de cada archivo.
      3. Extraer el mnimo, escribirlo a la salida, y cargar el
         siguiente elemento de ESE archivo.

    POR QU FUNCIONA: la fase 2 lee cada archivo SECUENCIALMENTE. No
    hay accesos aleatorios: ni un solo seek dentro de los datos. Eso
    es lo que lo hace viable en disco.

ANLISIS DE COSTE
    Fase 1: N ledos + N escritos.
    Fase 2: N ledos + N escritos.
    Total: ~4N operaciones de E/S SECUENCIALES.

    Compare con Merge Sort de 2 vas sobre disco: log(N/M) pasadas,
    cada una con 2N lecturas/escrituras. Con k-vas equilibrado se
    minimiza el nmero de pasadas.

POR QU UN HEAP Y NO UNA LISTA
    En cada paso hay que encontrar el MNIMO entre k elementos (uno
    por archivo). Con lista sera O(k) por paso -> O(N*k) total.
    Con heap es O(log k) por paso -> O(N log k) total.

TRAZA de la fase 2 con 2 archivos
    A = [1, 4, 7]     B = [2, 5, 8]

    heap inicial: [(1, A), (2, B)]
    pop 1, escribir 1, cargar 4 de A -> heap [(2,B), (4,A)]
    pop 2, escribir 2, cargar 5 de B -> heap [(4,A), (5,B)]
    pop 4, escribir 4, cargar 7 de A -> heap [(5,B), (7,A)]
    pop 5, escribir 5, B agotado    -> heap [(7,A)]
    pop 7, escribir 7, A agotado    -> heap []
    fin

    Salida: 1, 2, 4, 5, 7, 8 (ordenada)

DEMOSTRACIN DE CORRECCIN
    Invariante: el heap contiene siempre el menor elemento NO ESCRITO
    de cada archivo, y todos los archivos estn ordenados.

    - Al extraer el mnimo del heap, es el mnimo de todos los
      pendientes (porque cada archivo aporta su mnimo pendiente y el
      heap los compara).
    - Escribirlo y cargar el siguiente de ese archivo preserva el
      invariante.
    Luego la salida se genera en orden ascendente. Caso base: heap
    vaco = no quedan elementos. 

COMPLEJIDAD
    Tiempo: O(N log(N/M)) con k-vas, donde k = N/M es el nmero de
    bloques.
    Espacio: O(M) para el bloque en memoria + O(k) para el heap.

    El trade-off fundamental: si M es ms grande, menos archivos
    temporales (k pequeo, heap ms chico, menos pasadas). Pero M est
    limitado por la RAM disponible.

PARALELIZACIN
    La fase 1 es trivialmente paralela: cada bloque se ordena en un
    proceso/ncleo independiente. Es lo que hace la versin con
    multiprocessing (solucin 3).

APLICACIONES
    - Bases de datos ordenando tablas que exceden la memoria.
    - Procesamiento de logs masivos.
    - Compiladores ordenando smbolos.

RELACIN CON OTROS TEMAS
    - El concepto de "run" es el mismo que usa TimSort para detectar
      secuencias ya ordenadas (tema 02).
"""


import heapq
import tempfile
import os


def ordenamiento_externo(entrada, salida, bloque=10000):
    """Ordena un archivo de nmeros por external sort. O(N log(N/M)).

    `bloque` es cuntos nmeros caben en memoria a la vez.
    """
    # ---------- FASE 1: dividir, ordenar, escribir temporales ----------
    temporales = []
    with open(entrada, "r", encoding="utf-8") as f:
        while True:
            # Leer un bloque
            datos = []
            for _ in range(bloque):
                linea = f.readline()
                if not linea:
                    break
                datos.append(int(linea))

            if not datos:
                break

            # Ordenar EN MEMORIA (rpidosec: todo est en RAM)
            datos.sort()

            # Escribir a un temporal
            temp = tempfile.NamedTemporaryFile(
                mode="w+", delete=False, encoding="utf-8")
            temp.writelines(f"{d}\n" for d in datos)
            temp.close()
            temporales.append(temp.name)

    print(f"Fase 1 completa: {len(temporales)} archivos temporales")

    # ---------- FASE 2: mezclar k-vas con heap ----------
    archivos = [open(t, "r", encoding="utf-8") for t in temporales]
    heap = []

    with open(salida, "w", encoding="utf-8") as out:
        # Sembrar el heap con el primer elemento de cada archivo
        for i, a in enumerate(archivos):
            linea = a.readline()
            if linea:
                heapq.heappush(heap, (int(linea), i))

        # Extraer siempre el mnimo
        while heap:
            valor, i = heapq.heappop(heap)
            out.write(f"{valor}\n")

            # Cargar el siguiente del MISMO archivo
            linea = archivos[i].readline()
            if linea:
                heapq.heappush(heap, (int(linea), i))

    print(f"Fase 2 completa: escritos en {salida}")

    # ---------- Limpieza ----------
    for a in archivos:
        a.close()
    for t in temporales:
        os.unlink(t)


if __name__ == "__main__":
    import random

    random.seed(3000)
    n = 100000
    with open("desordenados.txt", "w", encoding="utf-8") as f:
        for _ in range(n):
            f.write(f"{random.randint(1, 1000000)}\n")

    print(f"Archivo de entrada: {n:,} nmeros")
    ordenamiento_externo("desordenados.txt", "ordenados.txt", bloque=10000)

    # Verificar que est ordenado y que no se perdi ningn nmero
    with open("ordenados.txt", encoding="utf-8") as f:
        numeros = [int(l) for l in f]

    assert len(numeros) == n, f"se perdieron nmeros: {len(numeros)} != {n}"
    assert numeros == sorted(numeros), "no est ordenado"
    print(f"\nVerificado: {len(numeros):,} nmeros ordenados correctamente")

    # Verificar que es una permutacin del original (mismos elementos)
    with open("desordenados.txt", encoding="utf-8") as f:
        originales = [int(l) for l in f]
    assert sorted(originales) == numeros
    print("Es una permutacin fiel del original")

    os.remove("desordenados.txt")
    os.remove("ordenados.txt")
    print("\n Todas las pruebas pasaron")
