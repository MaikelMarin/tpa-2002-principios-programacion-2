r"""
Ejercicio 11: Run-Length Encoding (RLE)
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Compresin sin prdida (teoria.md 6.3).
    - Listas y tuplas en Python.

PROBLEMA
    Comprimir un archivo de texto reemplazando series de caracteres
    repetidos por un contador y el caracter.

    Ver tambin el ejercicio 14 del tema 04, que implementa RLE sobre
    secuencias en memoria. Aqu el foco es el archivo: comprimir un
    archivo real y descomprimirlo.

FONDO MATEMTICO
    RLE es un algoritmo de compresin SIN PRDIDA: los datos originales
    se pueden reconstruir exactamente.

    Su eficacia depende de los datos:
      - Muchas repeticiones -> comprime muy bien.
      - Sin repeticiones -> puede AUMENTAR el tamao.

    Por eso RLE se usa donde las repeticiones son frecuentes: imgenes
    con reas planas, mapas de bits, faxes, datos cientficos.

ESTRATEGIA DE ARCHIVOS

```python
def comprimir_archivo(origen, destino):
    with open(origen, "rb") as src, open(destino, "wb") as dst:
        bloque = src.read(1)               # primer byte
        contador = 1
        while True:
            siguiente = src.read(1)
            if siguiente == bloque:
                contador += 1
            else:
                if contador > 1:           # solo comprime si repite
                    dst.write(contador.to_bytes(2, "big"))
                dst.write(bloque)
                if not siguiente:
                    break
                bloque = siguiente
                contador = 1
```

    FORMATO DE SALIDA: pares fijos de 2 bytes.
        [longitud: 1 byte][byte: 1 byte]

    La longitud va de 1 a 255. Cada byte del archivo original
    pertenece a exactamente un par, y el par se auto-describe: no
    hace falta ningn byte de escape.

    POR QU NO USAR UN BYTE DE ESCAPE (El errorclsico):
    La tentacin es usar 0x00 como marcador de "viene contador".
    Eso es INCORRECTO en binario: el byte 0x00 puede aparecer
    legtimamente en los datos, y el descompresor lo confundira con
    una marca. El round-trip fallara.

    Con pares fijos (longitud, byte) el formato es INSENSIBLE al
    contenido: cualquier byte es vlido como dato.

TRAZA de compresin de "AAABBB"
    'A' repetido 3 veces -> escape(0) + contador(3) + byte('A')
    'B' repetido 3 veces -> escape(0) + contador(3) + byte('B')
    Total: 8 bytes (vs 6 originales -> aqu RLE no ayuda)

    Contraste con "A" x 100:
    100 repeticiones -> escape + contador(100) + byte('A')
    Total: 4 bytes (vs 100 -> compresin 25:1)

COMPLEJIDAD
    Tiempo: O(n) — una pasada sobre el archivo.
    Espacio: O(1) — solo necesidada el byte actual y el contador.

CASOS LMITE
    - Archivo vaco: no se escribe nada.
    - Un solo byte: se escribe sin contador.
    - Rachas de ms de 65,535: el contador de 2 bytes desborda. Hay que
      partirlo en varias rachas.
    - Datos sin repeticin: el archivo CRECE.

APLICACIONES
    - Formatos BMP y TIFF tienen compresin RLE nativa.
    - Faxes (ITU T.4/T.6).

RELACIN CON OTROS TEMAS
    - El ejercicio 14 del tema 04 implementa RLE en memoria.
    - El tema 06 muestra compresin como tcnica para reducir E/S.
"""


def comprimir_rle(origen, destino):
    """Comprime con RLE. O(n) tiempo, O(1) memoria.

    Formato: cada par se codifica como (longitud: 1 byte) + (byte).
    La longitud va de 1 a 255. NO usa bytes de escape, as que
    funciona con CUALQUIER dato binario.
    """
    MAX_RACHA = 255

    with open(origen, "rb") as src_, open(destino, "wb") as dst:
        bloque = src_.read(1)
        if not bloque:
            return                                   # archivo vacio

        contador = 1
        while True:
            siguiente = src_.read(1)

            # Cerrar la racha si cambi el byte, si se alcanz el
            # mximo de 255, o si se termin el archivo.
            if siguiente != bloque or contador == MAX_RACHA:
                dst.write(bytes([contador]))
                dst.write(bloque)
                if not siguiente:
                    break
                bloque = siguiente
                contador = 1
            else:
                contador += 1


def descomprimir_rle(origen, destino):
    """Descomprime RLE. Lee pares (longitud, byte) y los expande."""
    with open(origen, "rb") as src_, open(destino, "wb") as dst:
        while True:
            cabecera = src_.read(1)
            if not cabecera:
                break
            longitud = cabecera[0]
            byte = src_.read(1)
            if not byte:
                raise ValueError("Archivo RLE truncado")
            dst.write(byte * longitud)


if __name__ == "__main__":
    import os

    # Crear archivo muy comprimible
    with open("original.txt", "wb") as f:
        f.write(b"A" * 100 + b"B" * 50 + b"C" * 10)

    comprimir_rle("original.txt", "comprimido.bin")

    tam_original = os.path.getsize("original.txt")
    tam_comprimido = os.path.getsize("comprimido.bin")
    print(f"Original:    {tam_original} bytes")
    print(f"Comprimido:  {tam_comprimido} bytes")
    print(f"Ratio:       {tam_original / tam_comprimido:.1f}:1")
    assert tam_comprimido < tam_original, "debera comprimir"

    # Descomprimir y verificar que es IDNTICO
    descomprimir_rle("comprimido.bin", "restaurado.txt")
    with open("original.txt", "rb") as f1, open("restaurado.txt", "rb") as f2:
        assert f1.read() == f2.read(), "el round-trip debe ser exacto"
    print("Round-trip verificado: identico byte a byte")

    # Caso base: archivo vacio
    with open("vacio.txt", "wb") as f:
        pass
    comprimir_rle("vacio.txt", "vacio.bin")
    assert os.path.getsize("vacio.bin") == 0
    descomprimir_rle("vacio.bin", "vacio_out.txt")
    assert os.path.getsize("vacio_out.txt") == 0
    print("Archivo vacio: round-trip correcto")

    # Un solo byte
    with open("uno.txt", "wb") as f:
        f.write(b"X")
    comprimir_rle("uno.txt", "uno.bin")
    descomprimir_rle("uno.bin", "uno_out.txt")
    with open("uno_out.txt", "rb") as f:
        assert f.read() == b"X"
    print("Un solo byte: round-trip correcto")

    # Datos SIN repeticin: RLE empeora el tamao
    with open("aleatorio.bin", "wb") as f:
        f.write(os.urandom(500))                 # bytes aleatorios
    comprimir_rle("aleatorio.bin", "aleatorio_rle.bin")
    tam_al = os.path.getsize("aleatorio.bin")
    tam_al_rle = os.path.getsize("aleatorio_rle.bin")
    print(f"\nDatos aleatorios de {tam_al} bytes:")
    print(f"  Comprimido: {tam_al_rle} bytes ({tam_al_rle/tam_al:.2f}x el original)")
    print("  RLE NO ayuda con datos sin repeticion")
    # El round-trip sigue siendo correcto aunque ocupe mas
    descomprimir_rle("aleatorio_rle.bin", "aleatorio_out.bin")
    with open("aleatorio.bin", "rb") as f1, open("aleatorio_out.bin", "rb") as f2:
        assert f1.read() == f2.read()
    print("  Round-trip sigue siendo exacto")

    # Racha que cabe en 2 bytes de contador (max 65535)
    with open("racha.txt", "wb") as f:
        f.write(b"Z" * 65535)
    comprimir_rle("racha.txt", "racha.bin")
    descomprimir_rle("racha.bin", "racha_out.txt")
    with open("racha_out.txt", "rb") as f:
        assert f.read() == b"Z" * 65535
    print(f"\nRacha de 65,535 bytes: {os.path.getsize('racha.bin')} bytes comprimidos")

    # Verificacin exhaustiva con muchos patrones
    import random
    random.seed(231)
    for _ in range(200):
        n = random.randint(0, 500)
        # Generar datos con mezcla de repeticiones y aleatoriedad
        partes = []
        while sum(len(p) for p in partes) < n:
            if random.random() < 0.5:
                partes.append(bytes([random.randrange(256)]) *
                              random.randint(1, 20))     # racha
            else:
                partes.append(os.urandom(random.randint(1, 10)))  # aleatorio
        datos = b"".join(partes)[:n]

        with open("test.bin", "wb") as f:
            f.write(datos)
        comprimir_rle("test.bin", "test_rle.bin")
        descomprimir_rle("test_rle.bin", "test_out.bin")
        with open("test_out.bin", "rb") as f:
            assert f.read() == datos, f"round-trip fallo con {len(datos)} bytes"

    print("200 casos aleatorios verificados")

    for a in ["original.txt", "comprimido.bin", "restaurado.txt", "vacio.txt",
              "vacio.bin", "vacio_out.txt", "uno.txt", "uno.bin", "uno_out.txt",
              "aleatorio.bin", "aleatorio_rle.bin", "aleatorio_out.bin",
              "racha.txt", "racha.bin", "racha_out.txt", "test.bin",
              "test_rle.bin", "test_out.bin"]:
        if os.path.exists(a):
            os.remove(a)

    print("\n Todas las pruebas pasaron")
