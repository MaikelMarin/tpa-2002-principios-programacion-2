r"""
Ejercicio 3 (solución): Ordenamiento externo paralelo
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - Ejercicio 3 (enunciado): el algoritmo secuencial.
    - Multiprocessing en Python.
    - Anlisis del speedup máximo (Ley de Amdahl).

PROBLEMA
    Acelerar la fase 1 del ordenamiento externo paralelizando la
    creacin de los runs.

FONDO MATEMTICO
    RECORDAR LA ESTRUCTURA DEL ALGORITMO:
      Fase 1 (ordenar bloques): PARALELA. Cada bloque es independiente.
      Fase 2 (mezclar): SECUENCIAL. Hay un nico flujo de salida.

    Por eso el speedup máximo est limitado. Si la fase 1 cuesta una
    fraccin f del tiempo total, la fase 2 cuesta (1-f) y NO se puede
    acelerar. Con p procesos:

        Speedup maximo = 1 / ((1-f) + f/p)     [Ley de Amdahl]

    Ejemplo: si f = 0.5 (la fase 1 es la mitad del tiempo) y p = 4:
        Speedup = 1 / (0.5 + 0.125) = 1.6x
    NO 4x. La fase secuencial domina.

    Esto es importante: paralelizar tiene rendimientos decrecientes,
    y hay que medir dnde est realmente el cuello de botella.

ESTRATEGIA

```python
from multiprocessing import Pool

def ordenar_bloque(datos):
    datos.sort()               # cada bloque se ordena en su proceso
    return datos

with Pool() as pool:
    bloques = leer_todos_los_bloques()
    bloques_ordenados = pool.map(ordenar_bloque, bloques)   # paralelo
```

    `pool.map` distribuye los bloques entre los ncleos disponibles y
    recoge los resultados en orden. Es la forma ms simple de
    paralelizar en Python.

    LIMITACIN DE MEMORIA: `pool.map` recoge TODOS los resultados. Si
    hay millones de bloques, todos quedan en RAM. Para eso existe
    `imap` (resultados perezosos).

    OVERHEAD DE SERIALIZACIN: cada bloque se enva al proceso hijo
    (pickle) y se devuelve ordenado. Ese coste puede anular la
    ganancia si los bloques son pequeos.

TRAZA con 4 bloques y 4 ncleos
    Bloques: [B0, B1, B2, B3]

    pool.map:
      ncleo 1 <- B0
      ncleo 2 <- B1
      ncleo 3 <- B2
      ncleo 4 <- B3
      (todos en paralelo)
    Resultados: [B0', B1', B2', B3']  en el orden original

    Fase 2: mezclar los 4 en un nico archivo ordenado.

COMPLEJIDAD
    Fase 1: O(N/p) tiempo con p ncleos (ideal).
    Fase 2: O(N log k) tiempo, secuencial.
    Total:  O(N/p + N log k)

    En la práctica, el overhead de serializacin y la contencin por
    E/S reducen la ganancia. Medir es obligatorio.

CUANDO PARALELIZAR NO SIRVE
    1. Bloques pequeos: el overhead de pickle domina.
    2. Disco saturado: la fase 2 no se acelera y el disco es el lmite.
    3. Un solo ncleo: no hay paralelismo posible.

APLICACIONES
    - Ordenamiento de datos a escala en clsters.
    - Procesamiento por lotes (batch).

RELACIN CON OTROS TEMAS
    - El patrn "dividir, procesar en paralelo, combinar" es el de
      MapReduce (teoria.md 5).
"""


import heapq
import tempfile
import os
import random
import time
from multiprocessing import Pool


def ordenar_bloque(datos):
    """Ordena un bloque en memoria. Se ejecuta en un proceso aparte."""
    datos.sort()
    return datos


def leer_bloques(entrada, tamano):
    """Lee el archivo en bloques de `tamano` nmeros."""
    bloques = []
    with open(entrada, encoding="utf-8") as f:
        while True:
            bloque = []
            for _ in range(tamano):
                linea = f.readline()
                if not linea:
                    break
                bloque.append(int(linea))
            if not bloque:
                break
            bloques.append(bloque)
    return bloques


def escribir_bloques(bloques):
    """Escribe cada bloque ordenado a un archivo temporal."""
    temporales = []
    for bloque in bloques:
        temp = tempfile.NamedTemporaryFile(
            mode="w+", delete=False, encoding="utf-8")
        temp.writelines(f"{d}\n" for d in bloque)
        temp.close()
        temporales.append(temp.name)
    return temporales


def mezclar(temporales, salida):
    """Mezcla k-vas con heap. Secuencial."""
    archivos = [open(t, encoding="utf-8") for t in temporales]
    heap = []

    with open(salida, "w", encoding="utf-8") as out:
        for i, a in enumerate(archivos):
            linea = a.readline()
            if linea:
                heapq.heappush(heap, (int(linea), i))

        while heap:
            valor, i = heapq.heappop(heap)
            out.write(f"{valor}\n")
            linea = archivos[i].readline()
            if linea:
                heapq.heappush(heap, (int(linea), i))

    for a in archivos:
        a.close()


def ordenamiento_externo_paralelo(entrada, salida, tamano_bloque=10000):
    """Fase 1 paralela, fase 2 secuencial."""
    print("Fase 1 (paralela): leyendo y ordenando bloques...")

    bloques = leer_bloques(entrada, tamano_bloque)

    # PARALELO: cada bloque se ordena en su propio proceso
    with Pool() as pool:
        ordenados = pool.map(ordenar_bloque, bloques)

    temporales = escribir_bloques(ordenados)
    print(f"  {len(temporales)} bloques ordenados")

    print("Fase 2 (secuencial): mezclando...")
    mezclar(temporales, salida)
    print("  Mezcla completa")

    for t in temporales:
        os.unlink(t)


if __name__ == "__main__":
    n = 500000

    print(f"Generando {n:,} nmeros aleatorios...")
    random.seed(42)
    with open("desordenados.txt", "w", encoding="utf-8") as f:
        buffer = []
        for _ in range(n):
            buffer.append(f"{random.randint(1, 10000000)}\n")
            if len(buffer) >= 1000:
                f.writelines(buffer)
                buffer = []
        if buffer:
            f.writelines(buffer)

    # --- Versin paralela ---
    inicio = time.time()
    ordenamiento_externo_paralelo("desordenados.txt", "ordenados.txt",
                                   tamano_bloque=10000)
    t_par = time.time() - inicio

    # Verificar correctitud
    with open("ordenados.txt", encoding="utf-8") as f:
        numeros = [int(l) for l in f]
    assert len(numeros) == n, f"se perdieron: {len(numeros)} != {n}"
    assert numeros == sorted(numeros), "no est ordenado"
    print(f"\nVerificado: {len(numeros):,} nmeros ordenados")

    # --- Versin secuencial (para comparar) ---
    inicio = time.time()
    print("\nVersin secuencial para comparar...")
    bloques = leer_bloques("desordenados.txt", 10000)
    for b in bloques:
        b.sort()
    temps = escribir_bloques(bloques)
    mezclar(temps, "ordenados_seq.txt")
    for t in temps:
        os.unlink(t)
    t_seq = time.time() - inicio

    with open("ordenados_seq.txt", encoding="utf-8") as f:
        numeros_seq = [int(l) for l in f]
    assert numeros_seq == numeros, "ambas versiones deben coincidir"

    print(f"\n--- Comparacin ---")
    print(f"  Secuencial: {t_seq:.2f}s")
    print(f"  Paralelo:   {t_par:.2f}s")
    if t_par > 0:
        print(f"  Speedup:    {t_seq / t_par:.2f}x")
    print(f"  Ncleos disponibles: {os.cpu_count()}")
    print("\n  Nota: el speedup est limitado por la Ley de Amdahl.")
    print("  La fase 2 (mezclar) es secuencial y no se acelera.")

    os.remove("desordenados.txt")
    os.remove("ordenados.txt")
    os.remove("ordenados_seq.txt")
    print("\n Todas las pruebas pasaron")
