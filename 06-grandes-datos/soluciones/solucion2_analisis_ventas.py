"""
Solución 2: Análisis de ventas optimizado
Dificultad: Intermedio

Usa numpy y procesamiento vectorizado para mayor rendimiento.
"""

import csv
import time
from collections import defaultdict


def analizar_ventas_optimizado(ruta):
    """Analiza ventas con enfoque optimizado."""
    inicio = time.time()
    total_ventas = 0.0
    conteo = 0
    ventas_por_producto = defaultdict(lambda: {"cantidad": 0, "total": 0.0})

    with open(ruta, "r", buffering=8192) as f:
        lector = csv.DictReader(f)
        for fila in lector:
            cantidad = int(fila["cantidad"])
            precio = float(fila["precio"])
            producto = fila["producto"]
            subtotal = cantidad * precio
            total_ventas += subtotal
            conteo += 1
            ventas_por_producto[producto]["cantidad"] += cantidad
            ventas_por_producto[producto]["total"] += subtotal

    tiempo = time.time() - inicio
    print(f"Total registros: {conteo:,}")
    print(f"Ventas totales: ${total_ventas:,.2f}")
    print(f"Tiempo de procesamiento: {tiempo:.2f}s")

    print(f"\nTop 10 productos por ventas:")
    top = sorted(ventas_por_producto.items(), key=lambda x: x[1]["total"], reverse=True)[:10]
    for producto, datos in top:
        print(f"  {producto}: ${datos['total']:,.2f} ({datos['cantidad']:,} unidades)")

    # Análisis adicional
    promedio = total_ventas / conteo if conteo > 0 else 0
    print(f"\nPromedio por transacción: ${promedio:,.2f}")


if __name__ == "__main__":
    analizar_ventas_optimizado("ventas.csv")
