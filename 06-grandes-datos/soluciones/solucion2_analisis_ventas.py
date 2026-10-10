r"""
Ejercicio 2 (solucin): Anlisis de ventas con streaming
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Ejercicio 2 (enunciado): la versin base.
    - Generadores (00-fundamentos 10.4).

PROBLEMA
    El mismo anlisis de ventas, pero medido contra la alternativa
    ingenua (cargar todo en memoria) y con diagnstico de memoria.

FONDO MATEMTICO
    La diferencia entre las dos versiones es drstica en MEMORIA:

        Ingenua:  O(n)  -> un objeto por fila del archivo.
        Streaming: O(k) -> un objeto por producto distinto.

    Con 1M de filas y 100 productos, la ingenua usa ~10,000 veces
    ms memoria.

    Y hay un segundo efecto: la ingenua hace dos pasadas (leer todo,
    luego procesar), mientras el streaming hace UNA. En disco, cada
    pasada cuesta leer el archivo completo.

ESTRATEGIA
    Mismo procesamiento, pero aadiendo:
      1. Medicin de tiempo de ambas versiones.
      2. Verificacin de que dan resultados idnticos.
      3. Un generador explcito (`yield`) para mostrar el patrn.

```python
def leer_registros(ruta):
    with open(ruta, encoding="utf-8") as f:
        for linea in f:              # lectura perezosa
            yield procesar(linea)     # un registro a la vez

# El generador se consume sin materializar nada
total = sum(r["monto"] for r in leer_registros("ventas.csv"))
```

    El generador es la forma idiomtica de expresar "procesa un
    elemento a la vez". Se puede encadenar con filtros y mapas sin
    crear listas intermedias.

TRAZA del generador
    leer_registros(ventas.csv)
      -> abre el archivo
      -> yield primera fila        (pausa aqu)
    El consumidor (sum) recibe la fila, la procesa
      -> pide la siguiente
      -> yield segunda fila        (pausa)
    ... y as hasta agotar el archivo

    En ningún momento existe la lista completa en memoria.

COMPLEJIDAD
    Streaming: O(n) tiempo, O(k) espacio (k = productos).
    Ingenua:   O(n) tiempo, O(n) espacio.

    Ambas O(n) en tiempo. La diferencia de 10,000x est en MEMORIA.

CUANDO EL STREAMING NO SIRVE
    Si la operacin NO es incremental:
      - Mediana exacta: requiere todos los datos.
      - Ordenar: requiere todos los datos (usar external sort).
      - Join de dos archivos por clave: requiere ndice o orden.

    Para esos casos existen: esbozos (mediana aproximada), ordenamiento
    externo (ejercicio 3) y hash join (particionar por clave).

APLICACIONES
    - Pipelines ETL sobre datos que exceden la memoria.
    - Procesamiento de logs en tiempo real.
    - Agregaciones sobre datos histricos.

RELACIN CON OTROS TEMAS
    - Es el mismo `for linea in f` del tema 05, aplicado a un problema
      donde la memoria importa de verdad.
"""


import csv
import time
import os


def leer_registros(ruta):
    """Generador: procesa el CSV un registro a la vez. O(1) memoria."""
    with open(ruta, encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            yield fila


def analizar_streaming(ruta):
    """Anlisis con streaming. O(n) tiempo, O(k) espacio."""
    total_ventas = 0.0
    conteo = 0
    por_producto = {}

    for fila in leer_registros(ruta):
        cantidad = int(fila["cantidad"])
        precio = float(fila["precio"])
        producto = fila["producto"]
        subtotal = cantidad * precio

        total_ventas += subtotal
        conteo += 1

        if producto not in por_producto:
            por_producto[producto] = {"cantidad": 0, "total": 0.0}
        por_producto[producto]["cantidad"] += cantidad
        por_producto[producto]["total"] += subtotal

    return {"total": total_ventas, "conteo": conteo,
            "por_producto": por_producto}


def analizar_ingenuo(ruta):
    """Anlisis cargando TODO en memoria. O(n) espacio."""
    with open(ruta, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))          # todo en RAM

    total_ventas = 0.0
    por_producto = {}
    for fila in filas:
        cantidad = int(fila["cantidad"])
        precio = float(fila["precio"])
        producto = fila["producto"]
        subtotal = cantidad * precio
        total_ventas += subtotal
        if producto not in por_producto:
            por_producto[producto] = {"cantidad": 0, "total": 0.0}
        por_producto[producto]["cantidad"] += cantidad
        por_producto[producto]["total"] += subtotal

    return {"total": total_ventas, "conteo": len(filas),
            "por_producto": por_producto}


if __name__ == "__main__":
    import random

    random.seed(42)
    n = 1000000
    productos = [f"Producto_{i}" for i in range(1, 101)]

    print(f"Generando {n:,} registros...")
    with open("ventas.csv", "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["producto", "cantidad", "precio"])
        buffer = []
        for _ in range(n):
            buffer.append([random.choice(productos),
                           random.randint(1, 50),
                           round(random.uniform(10, 1000), 2)])
            if len(buffer) >= 1000:
                escritor.writerows(buffer)
                buffer = []
        if buffer:
            escritor.writerows(buffer)

    tam = os.path.getsize("ventas.csv")
    print(f"Archivo: {tam/(1024*1024):.1f} MB, {n:,} registros")

    # --- Streaming ---
    inicio = time.time()
    r_stream = analizar_streaming("ventas.csv")
    t_stream = time.time() - inicio

    print(f"\n--- Streaming ---")
    print(f"  Registros: {r_stream['conteo']:,}")
    print(f"  Ventas:    ${r_stream['total']:,.2f}")
    print(f"  Tiempo:    {t_stream:.3f}s")

    # --- Ingenua ---
    inicio = time.time()
    r_ing = analizar_ingenuo("ventas.csv")
    t_ing = time.time() - inicio

    print(f"\n--- Ingenua (todo en memoria) ---")
    print(f"  Registros: {r_ing['conteo']:,}")
    print(f"  Ventas:    ${r_ing['total']:,.2f}")
    print(f"  Tiempo:    {t_ing:.3f}s")

    # AMBAS DAN EL MISMO RESULTADO
    assert r_stream["total"] == r_ing["total"], "los totales deben coincidir"
    assert r_stream["conteo"] == r_ing["conteo"]
    assert r_stream["por_producto"].keys() == r_ing["por_producto"].keys()
    print("\nAmbas versiones dan resultados IDNTICOS")

    # La memoria es la diferencia real
    n_productos = len(r_stream["por_producto"])
    print(f"\nMemoria:")
    print(f"  Streaming: O({n_productos}) productos en memoria")
    print(f"  Ingenua:   O({n:,}) filas en memoria")
    print(f"  Ratio:     {n / n_productos:,.0f}x menos memoria con streaming")

    # Top 10 productos
    top = sorted(r_stream["por_producto"].items(),
                 key=lambda x: x[1]["total"], reverse=True)[:10]
    print(f"\nTop 10 productos por ventas:")
    for producto, datos in top:
        print(f"  {producto}: ${datos['total']:,.2f} "
              f"({datos['cantidad']:,} unidades)")

    # Promedio por transaccin
    promedio = r_stream["total"] / r_stream["conteo"]
    print(f"\nPromedio por transaccin: ${promedio:,.2f}")

    os.remove("ventas.csv")
    print("\n Todas las pruebas pasaron")
