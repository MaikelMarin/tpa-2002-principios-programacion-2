"""
Ejercicio 11: Run-Length Encoding (RLE)
Dificultad: Intermedio

Algoritmo de compresión sin pérdida para secuencias repetidas.
"""


def codificar_rle(datos):
    """Codifica datos usando Run-Length Encoding."""
    if not datos:
        return []
    resultado = []
    actual = datos[0]
    contador = 1
    for elemento in datos[1:]:
        if elemento == actual:
            contador += 1
        else:
            resultado.append((actual, contador))
            actual = elemento
            contador = 1
    resultado.append((actual, contador))
    return resultado


def decodificar_rle(datos_codificados):
    """Decodifica datos codificados con RLE."""
    resultado = []
    for elemento, contador in datos_codificados:
        resultado.extend([elemento] * contador)
    return resultado


if __name__ == "__main__":
    datos = "AAABBBCCCCAD"
    print(f"Original: {datos}")

    codificado = codificar_rle(datos)
    print(f"Codificado: {codificado}")

    decodificado = decodificar_rle(codificado)
    print(f"Decodificado: {''.join(decodificado)}")

    assert decodificar_rle(codificar_rle(datos)) == list(datos)
    assert codificar_rle("AAABBB") == [('A', 3), ('B', 3)]
    print("\n✓ Todas las pruebas pasaron")
