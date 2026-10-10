r"""
Ejercicio 2: Anlisis de ventas con grandes datos
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Streaming y generadores (teoria.md 2).
    - Lectura lnea por lnea (tema 05, ejercicio 3).
    - defaultdict (00-fundamentos 10.8).

PROBLEMA
    Analizar un archivo de ventas con millones de registros usando
    procesamiento por streaming, sin cargar el archivo en memoria.

FONDO MATEMTICO
    El archivo tiene, digamos, 1,000,000 de filas. Cargarlo completo
    con readlines() creara 1M de strings en RAM (varios cientos de MB).

    Con streaming, la memoria es O(1): solo la lnea actual mas el
    estado agregado (un diccionario de totales por producto).

    EL ESTADO AGREGADO ES LA CLAVE: en vez de guardar todos los datos,
    se guarda solo lo que se necesita del resultado.

        Por producto:  {"cantidad": int, "total": float}
        Global:        total_ventas, conteo

    Si hubiera que guardar todo el detalle, el streaming no servira.
    Funciona porque la pregunta (totales por producto) se puede
    responder incrementalmente.

ESTRATEGIA

```python
total_ventas = 0.0
conteo = 0
ventas_por_producto = defaultdict(lambda: {"cantidad": 0, "total": 0.0})

with open("ventas.csv") as f:
    for fila in csv.DictReader(f):      # una fila en memoria
        cantidad = int(fila["cantidad"])
        precio = float(fila["precio"])
        producto = fila["producto"]
        subtotal = cantidad * precio

        total_ventas += subtotal
        conteo += 1
        ventas_por_producto[producto]["cantidad"] += cantidad
        ventas_por_producto[producto]["total"] += subtotal
```

    Note que el bucle NO acumula filas: solo actualiza agregados.

TRAZA del estado (3 productos, 5 filas)
    Fila: P1, 2, 300  -> total=600, P1={cant:2, tot:600}
    Fila: P2, 1, 150  -> total=750, P2={cant:1, tot:150}
    Fila: P1, 3, 100  -> total=1050, P1={cant:5, tot:900}
    Fila: P3, 5, 20   -> total=1150, P3={cant:5, tot:100}

    Estado final: memoria O(3 productos), no O(5 filas). Con 1M de
    filas y 100 productos, la memoria seguira siendo O(100).

COMPLEJIDAD
    Tiempo: O(n). Cada fila se procesa una vez con trabajo O(1).
    Espacio: O(k) donde k es el nmero de productos DISTINTOS,
             no el nmero de filas.

    Ese O(k) en vez de O(n) es toda la diferencia: si hay 100
    productos y 1M de filas, la memoria es 100 veces menor.

LA CONDICIN PARA QUE EL STREAMING FUNCIONE
    La agregacin debe ser INCREMENTAL: poder calcular el resultado
    final combinando resultados parciales.

    Suma, conteo, max, min: s (son asociativos y conmutativos).
    Mediana: NO (para la mediana exacta hacen falta todos los datos;
    se aproxima con esbozos).
    Ordenar: NO exacto (requiere ordenamiento externo, ejercicio 3).

APLICACIONES
    - Procesar logs de servidor (gigabytes).
    - Reportes financieros sobre millones de transacciones.
    - ETL (extract, transform, load) en pipelines de datos.

RELACIN CON OTROS TEMAS
    - El ejercicio 3 resuelve el caso donde el streaming NO alcanza
      (ordenar requiere todos los datos).
"""


import csv
from collections import defaultdict


def analizar_ventas(ruta):
    """Analiza ventas por streaming. O(n) tiempo, O(k) espacio.

    k = nmero de productos distintos, NO el nmero de filas.
    """
    total_ventas = 0.0
    conteo = 0
    ventas_por_producto = defaultdict(lambda: {"cantidad": 0, "total": 0.0})

    with open(ruta, "r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:                      # una fila a la vez
            cantidad = int(fila["cantidad"])
            precio = float(fila["precio"])
            producto = fila["producto"]
            subtotal = cantidad * precio

            total_ventas += subtotal
            conteo += 1
            ventas_por_producto[producto]["cantidad"] += cantidad
            ventas_por_producto[producto]["total"] += subtotal

    return {
        "total": total_ventas,
        "conteo": conteo,
        "por_producto": dict(ventas_por_producto)
    }


if __name__ == "__main__":
    import os
    import random

    # Generar 1,000,000 de registros
    random.seed(2024)
    n = 1000000
    productos = [f"Producto_{i}" for i in range(1, 101)]

    with open("ventas.csv", "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["producto", "cantidad", "precio"])
        for _ in range(n):
            escritor.writerow([
                random.choice(productos),
                random.randint(1, 50),
                round(random.uniform(10, 1000), 2)
            ])

    tam = os.path.getsize("ventas.csv")
    print(f"Archivo generado: {n:,} registros, {tam/(1024*1024):.1f} MB")

    # Verificar el conteo de lneas ANTES de analizar
    n_lineas = sum(1 for _ in open("ventas.csv", encoding="utf-8"))
    assert n_lineas == n + 1, f"{n_lineas} != {n+1}"
    print(f"Lneas verificadas: {n_lineas:,} (incluye cabecera)")

    # Analizar por streaming
    resultado = analizar_ventas("ventas.csv")

    print(f"\nTotal registros: {resultado['conteo']:,}")
    print(f"Ventas totales: ${resultado['total']:,.2f}")
    assert resultado["conteo"] == n

    # PRODUCTOS: solo 100 entradas en memoria, no 1M
    assert len(resultado["por_producto"]) == 100
    print(f"Productos distintos: {len(resultado['por_producto'])}")
    print("  (memoria O(100), no O(1,000,000))")

    # Verificar la consistencia interna de los agregados con una
    # SEGUNDA pasada de streaming (no se carga el archivo).
    suma_cantidades = sum(d["cantidad"] for d in resultado["por_producto"].values())
    with open("ventas.csv", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        suma_directa = sum(int(fila["cantidad"]) for fila in lector)
    assert suma_cantidades == suma_directa, "las cantidades deben cuadrar"
    print(f"Suma de cantidades verificada: {suma_cantidades:,}")

    # El total por producto suma el total global
    suma_totales = sum(d["total"] for d in resultado["por_producto"].values())
    assert abs(suma_totales - resultado["total"]) < 0.01, "los totales deben cuadrar"
    print("Totales por producto cuadran con el total global")

    # Top productos
    top = sorted(resultado["por_producto"].items(),
                 key=lambda x: x[1]["total"], reverse=True)[:5]
    print(f"\nTop 5 productos por ventas:")
    for producto, datos in top:
        print(f"  {producto}: ${datos['total']:,.2f} ({datos['cantidad']:,} unidades)")

    for a in ["ventas.csv"]:
        os.remove(a)

    print("\n Todas las pruebas pasaron")
