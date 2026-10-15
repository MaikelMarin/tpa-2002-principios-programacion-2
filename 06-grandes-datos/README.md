# 06 — Procesamiento de Grandes Cantidades de Datos

## Mapa conceptual

```
                  GRANDES DATOS
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   EL PROBLEMA    TCNICAS       SIGUIENTE NIVEL
        │              │              │
   ┌────┴────┐    ┌─────┴──────┐   ┌───┴───┐
   │         │    │            │   │       │
Jerarqua  Streaming  Ordenamiento  Multiproc  MapReduce
memoria   (generad.)  externo      essing    (Google
   │                    │           │         2004)
RAM 100ns        Fase 1     Fase 2  Ley de    map/shuffle/
disco 100000x    paralela   k-vas   Amdahl    reduce
                  heap
```

## Temas a tocar

| # | Tema | Qué se cubre |
|---|------|--------------|
| 1 | El problema | Jerarqua de memoria cuantificada (RAM 100 ns vs disco 10 ms = 100,000×), las dimensiones del problema |
| 2 | Streaming | Procesar un elemento a la vez; O(1) memoria frente a O(n) |
| 3 | Ordenamiento externo | Fase 1 (runs) + fase 2 (merge k-vas con heap): ~4N operaciones de E/S secuenciales |
| 4 | Técnicas | Bfer de escritura, compresin, muestreo, poda |
| 5 | Escalado | Multiprocessing y la Ley de Amdahl: el lmite real |
| 6 | Cundo usar qu | Tabla de decisin por situacin |

## Contenido categorizado

| Categora | Descripcin | Ejercicios |
|----------|-------------|------------|
| **Generacin** | Datos sintticos con bfer manual y la semilla para reproducibilidad | E1, S1 |
| **Anlisis** | Agregacin por streaming: memoria O(productos), no O(filas) | E2, S2 |
| **Ordenamiento** | External sort: dos fases, heap de k vas, costo 4N | E3, S3 |
| **Paralelismo** | Fase 1 en varios ncleos y sus lmites reales | S3 |

E = enunciado (`ejercicios/`), S = solución (`soluciones/`)

## Lista de ejercicios y ubicacin de soluciones

| # | Ejercicio | Dificultad | Enunciado | Solucin |
|---|-----------|------------|-----------|----------|
| 1 | Generacin masiva | Bsico | [`ejercicios/ejercicio1_generacion_masiva.py`](ejercicios/ejercicio1_generacion_masiva.py) | [`soluciones/solucion1_generacion_masiva.py`](soluciones/solucion1_generacion_masiva.py) |
| 2 | Anlisis de ventas | Intermedio | [`ejercicios/ejercicio2_analisis_ventas.py`](ejercicios/ejercicio2_analisis_ventas.py) | [`soluciones/solucion2_analisis_ventas.py`](soluciones/solucion2_analisis_ventas.py) |
| 3 | Ordenamiento externo | Experto | [`ejercicios/ejercicio3_ordenamiento_externo.py`](ejercicios/ejercicio3_ordenamiento_externo.py) | [`soluciones/solucion3_ordenamiento_externo.py`](soluciones/solucion3_ordenamiento_externo.py) |

Cada archivo incluye conocimiento previo, fondo matemtico, estrategia, traza, anlisis de coste, casos lmite y verificación experimental.

## Ruta de aprendizaje recomendada

1. **Ejercicio 1** — generar datos a escala. Fije la semilla para que el experimento sea reproducible.
2. **Ejercicio 2** — el paso clave: analizar 1M de registros sin cargarlos. Mida la diferencia de memoria.
3. **Ejercicio 3** — el caso donde el streaming NO alcanza: ordenar todos los datos.
4. **Solucin 3** — por qu paralelizar no siempre acelera (Ley de Amdahl + overhead de serializacin).

## Hallazgos medidos en este tema

| Experimento | Resultado |
|-------------|-----------|
| Streaming vs ingenuo (1M filas, 100 productos) | ~10,000× menos memoria |
| Bfer manual de 1000 (1M registros) | 0.97× — el bufer del SO ya cubre la mayor parte |
| Ordenamiento externo (100,000 nmeros) | Correcto, es permutacin fiel del original |
| Fase 1 paralela (500,000 nmeros, 6 ncleos) | **0.89× — MÁ LENTO**: el overhead de serializar bloques de 10,000 nmeros supera la ganancia |

Ese ltimo resultado es la leccin ms importante del tema: **paralelizar no es gratis**. Hay que medir, no suponer.

## Prerrequisitos

De `00-fundamentos`: logaritmos (§4), sumatorias (§5), recurrencias (§7), heap (§8.6), modelo de memoria (§9), generadores (§10.4).

Adems, del resto del proyecto: Merge Sort (tema 02), `csv` y lectura por lneas (tema 05).

## Teora

Ver [`teoria.md`](teoria.md) — incluye la jerarqua de memoria cuantificada, el anlisis de las ~4N operaciones de E/S del ordenamiento externo y la tabla de decisin por situacin.
