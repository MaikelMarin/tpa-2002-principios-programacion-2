"""
Ejercicio 2: Análisis de ventas con 1M de registros
Dificultad: Intermedio

Analiza un archivo de ventas con más de 1 millón de registros usando
procesamiento por bloques (streaming).
"""

import csv
from collections import defaultdict


def analizar_ventas(ruta):
    """Analiza ventas usando streaming (sin cargar todo en memoria)."""
    total_ventas = 0.0
    conteo = 0
    ventas_por_producto = defaultdict(lambda: {"cantidad": 0, "total": 0.0})

    with open(ruta, "r") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            cantidad = int(fila["cantidad"])
            precio = float(fila["precio"])
            producto = fila["producto"]

            total_ventas += cantidad * precio
            conteo += 1
            ventas_por_producto[producto]["cantidad"] += cantidad
            ventas_por_producto[producto]["total"] += cantidad * precio

    print(f"Total registros: {conteo}")
    print(f"Ventas totales: ${total_ventas:,.2f}")
    print(f"\nTop 5 productos por ventas:")
    top = sorted(ventas_por_producto.items(), key=lambda x: x[1]["total"], reverse=True)[:5]
    for producto, datos in top:
        print(f"  {producto}: ${datos['total']:,.2f} ({datos['cantidad']} unidades)")


if __name__ == "__main__":
    # Generar datos de prueba
    import random
    with open("ventas.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["producto", "cantidad", "precio"])
        productos = [f"Producto_{i}" for i in range(1, 101)]
        for _ in range(1000000):
            writer.writerow([
                random.choice(productos),
                random.randint(1, 50),
                round(random.uniform(10, 1000), 2)
            ])

    analizar_ventas("ventas.csv")
