r"""
Ejercicio 14: Run-Length Encoding (RLE)
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Compresión sin pérdida: qué es y para qué sirve.
    - Listas y tuplas en Python.

PROBLEMA
    Comprimir una secuencia reemplazando series de elementos
    repetidos por un contador y el elemento.

        "AAABBBCCCCAD"  →  [(A,3), (B,3), (C,4), (A,1), (D,1)]

FONDO MATEMÁTICO
    RLE es un algoritmo de compresión SIN PÉRDIDA: los datos
    originales se pueden reconstruir exactamente.

    Su eficacia depende por completo de los datos:
      - Muchas repeticiones → comprime muy bien.
      - Sin repeticiones → puede AUMENTAR el tamaño (cada elemento
        necesitaría su contador).

    Por eso RLE se usa donde las repeticiones son frecuentes:
    imágenes con áreas planas, mapas de bits, faxes, datos
    científicos con valores repetidos.

ESTRATEGIA DE CODIFICACIÓN
    Un solo recorrido lineal:

        1. Inicializar con el primer elemento y contador 1.
        2. Para cada elemento siguiente:
             - Si es IGUAL al actual → incrementar el contador.
             - Si es DISTINTO → guardar (actual, contador) y empezar
               de nuevo con el nuevo elemento.
        3. Al final, guardar la última racha.

TRAZA de codificar("AAABBB")
    actual = 'A', contador = 1

    'A' == 'A' → contador = 2
    'A' == 'A' → contador = 3
    'B' != 'A' → guardar (A, 3). actual = 'B', contador = 1
    'B' == 'B' → contador = 2
    'B' == 'B' → contador = 3

    Fin del bucle → guardar (B, 3)

    Resultado: [(A,3), (B,3)]

    ¡IMPORTANTE! El paso final de guardar la última racha es fácil de
    olvidar. Sin él, se pierde el último grupo.

ESTRATEGIA DE DECODIFICACIÓN
    Expandir cada tupla:

        [(A,3), (B,3)]  →  A A A B B B

    Es exactamente la operación inversa. La verificación de
    round-trip (codificar → decodificar = original) es la prueba de
    corrección más importante.

COMPLEJIDAD
    Codificar:    O(n) tiempo, O(k) espacio donde k es el número de
                  rachas distintas.
    Decodificar:  O(n) tiempo, O(n) espacio (la salida tiene tamaño n).
    Round-trip:   O(n) total.

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción sobre las rachas. La codificación produce una lista
    donde cada tupla (x, c) representa exactamente c copias de x, y
    las tuplas aparecen en el mismo orden que las rachas originales.
    La decodificación expande cada tupla a c copias de x. Luego la
    concatenación reproduce la secuencia original exactamente. ∎

CUÁNDO RLE ES BUENA IDEA
    Datos                           Compresión
    "AAAAAAAAAAAAAAAAAAAA" (20 A)   20 → 2 elementos: excelente
    Texto en inglés natural          ~1.1x: casi nula
    Datos aleatorios                 EMPEORA (contador por elemento)

COMPARACIÓN CON OTROS ALGORITMOS
    Algoritmo     Idea                          Ratio típico
    RLE           Rachas repetidas              Bueno si hay rachas
    Huffman       Códigos de longitud variable  2-3x en texto
    LZ77/LZ78     Diccionario de frases         2-4x en texto
    DEFLATE       LZ77 + Huffman               3-5x (gzip, zip)
    Brotli        Context modeling + LZ         3-6x (web)

    RLE es el más simple de todos y el peor en general, pero sirve
    como introducción exacta al concepto de compresión.

APLICACIONES REALES
    - Formato BMP/TIFF: compresión RLE nativa.
    - Fax (grupo 3/4 ITU).
    - Índices de bases de datos columnar (valores repetidos).
    - Transmisión de mapas de bits.
"""


def codificar_rle(datos):
    """Codifica con RLE. O(n).

    Devuelve una lista de tuplas (elemento, contador).
    """
    if not datos:
        return []

    resultado = []
    actual = datos[0]
    contador = 1

    for elemento in datos[1:]:
        if elemento == actual:
            contador += 1                  # misma racha
        else:
            resultado.append((actual, contador))    # cerrar racha
            actual = elemento
            contador = 1

    # No olvidar la ÚLTIMA racha
    resultado.append((actual, contador))
    return resultado


def decodificar_rle(datos_codificados):
    """Decodifica RLE. O(n) donde n es el tamaño original."""
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

    # Round-trip: la propiedad más importante
    assert decodificado == list(datos), "el round-trip debe ser exacto"
    assert "".join(decodificado) == datos

    # El código esperado
    assert codificado == [('A', 3), ('B', 3), ('C', 4), ('A', 1), ('D', 1)]

    # Casos base
    assert codificar_rle("") == [], "cadena vacía"
    assert codificar_rle("A") == [("A", 1)], "un solo elemento"
    assert decodificar_rle([]) == []

    # Un solo carácter repetido
    assert codificar_rle("A" * 20) == [("A", 20)]
    assert decodificar_rle([("A", 20)]) == ["A"] * 20

    # Todo distinto: RLE no comprime, mantiene el tamaño
    distinto = "ABCDE"
    cod_distinto = codificar_rle(distinto)
    print(f"\nSin repeticiones: {cod_distinto}")
    assert cod_distinto == [("A", 1), ("B", 1), ("C", 1), ("D", 1), ("E", 1)]
    assert decodificar_rle(cod_distinto) == list(distinto)

    # Funciona con cualquier tipo de dato, no solo caracteres
    numeros = [1, 1, 1, 2, 2, 3]
    cod_num = codificar_rle(numeros)
    print(f"Lista de números: {cod_num}")
    assert cod_num == [(1, 3), (2, 2), (3, 1)]
    assert decodificar_rle(cod_num) == numeros

    # Rachas intercaladas
    intercalado = "AABBAA"
    cod_int = codificar_rle(intercalado)
    print(f"Intercalado 'AABBAA': {cod_int}")
    assert cod_int == [("A", 2), ("B", 2), ("A", 2)]
    assert decodificar_rle(cod_int) == list(intercalado)

    # Medir la compresión real
    def ratio(original, codificado):
        if not original:
            return 0
        # Aproximación: cada tupla pesa 2, cada original 1
        return len(codificado) * 2 / len(original)

    muy_repetido = "A" * 100
    r = ratio(muy_repetido, codificar_rle(muy_repetido))
    print(f"\n100 'A' → ratio {r:.2f} (excelente)")
    assert r < 0.1

    sin_repeticion = "ABCDEFGHIJ"
    r2 = ratio(sin_repeticion, codificar_rle(sin_repeticion))
    print(f"10 distintos → ratio {r2:.2f} (RLE no ayuda)")
    assert r2 > 1, "sin repeticiones, RLE empeora el tamaño"

    # Verificación aleatoria exhaustiva
    import random
    random.seed(201)
    for _ in range(500):
        n = random.randint(0, 50)
        alfabeto = random.choice(["AB", "ABC", "ABCDE"])
        secuencia = "".join(random.choice(alfabeto) for _ in range(n))
        cod = codificar_rle(secuencia)
        assert decodificar_rle(cod) == list(secuencia), \
            f"round-trip falló con {secuencia}"

    # Verificar que el conteo reconstruye la longitud
    for _ in range(100):
        n = random.randint(0, 30)
        sec = "".join(random.choice("XYZ") for _ in range(n))
        cod = codificar_rle(sec)
        suma = sum(c for _, c in cod)
        assert suma == len(sec), "los contadores deben sumar la longitud"

    print("\n✓ Todas las pruebas pasaron")
