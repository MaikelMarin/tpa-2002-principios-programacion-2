r"""
Ejercicio 8: Copiar archivo binario
Dificultad: Bsico

CONOCIMIENTO PREVIO NECESARIO
    - Modo binario "rb"/"wb" (teoria.md 3.1).
    - La diferencia entre leer todo y leer por bloques.
    - Buffering.

PROBLEMA
    Copiar un archivo binario de forma eficiente.

FONDO MATEMTICO
    Un archivo binario puede ser enorme (GB). Hay dos formas de
    copiarlo:

    INGNUA (carga todo en memoria):
        with open(origen, "rb") as f:
            datos = f.read()              # O(n) memoria
        with open(destino, "wb") as f:
            f.write(datos)

    POR BLOQUES (memoria constante):
        with open(origen, "rb") as src, open(destino, "wb") as dst:
            while True:
                bloque = src.read(1024)   # O(bloque) memoria
                if not bloque:
                    break
                dst.write(bloque)

    La diferencia: para un archivo de 4 GB, la primera necesita 4 GB
    de RAM; la segunda, 1 KB. Ambas son O(n) en tiempo.

    El tamao de bloque óptimo depende del sistema: 8 KB a 1 MB son
    valores tpicos. Demasiado pequee = muchas llamadas al sistema;
    demasiado grande = se desperdicia memoria sin ganar velocidad.

ESTRATEGIA

```python
def copiar_binario(origen, destino, tamano_buffer=1024):
    with open(origen, "rb") as f_origen, open(destino, "wb") as f_destino:
        while True:
            bloque = f_origen.read(tamano_buffer)
            if not bloque:                # fin del archivo
                break
            f_destino.write(bloque)
```

    Detalles:
      1. Ambos archivos se abren en el mismo `with`: se garantiza que
         los dos se cierren.
      2. `read(tamano)` devuelve MENOS bytes si llega al final. Cuando
         devuelve b"" es que se termin.
      3. Se escribe cada bloque tal cual: no se interpreta nada.

TRAZA de copia de un archivo de 2500 bytes con buffer de 1024
    read(1024) -> 1024 bytes, escribir
    read(1024) -> 1024 bytes, escribir
    read(1024) -> 452 bytes, escribir
    read(1024) -> b"" (vacio) -> break

    4 lecturas, 3 escrituras. Total: 2500 bytes copiados.

COMPLEJIDAD
    Tiempo: O(n / tamano_buffer) llamadas al sistema, O(n) trabajo.
    Espacio: O(tamano_buffer).

    REDUCCIN DE LLAMADAS AL SISTEMA: con buffer de 1024 y archivo de
    1 MB, son 1024 llamadas. Con buffer de 64 KB, solo 16.

CASOS LMITE
    - Archivo vacio: el primer read devuelve b"" y se termina. Se crea
      un archivo destino vacio.
    - Origen == destino: se corrompe (se lee lo que se acaba de
      escribir). Hay que usar un temporal.
    - Archivo mas grande que la RAM: la copia por bloques funciona.

VERIFICACIN DE CORRECCIN
    La copia es correcta si y solo si el destino es idntico byte a
    byte al origen. Es la prueba que se hace siempre.

APLICACIONES
    - Instaladores y gestores de descargas.
    - Backups.
    - Cualquier herramienta que mueva datos binarios.

RELACIN CON OTROS TEMAS
    - El tema 06 muestra que para archivos enormes, el tamao de buffer
      afecta directamente el rendimiento.
"""


def copiar_binario(origen, destino, tamano_buffer=1024):
    """Copia un archivo binario por bloques. O(n) tiempo, O(buffer) memoria."""
    with open(origen, "rb") as f_origen, open(destino, "wb") as f_destino:
        while True:
            bloque = f_origen.read(tamano_buffer)
            if not bloque:                    # fin del archivo
                break
            f_destino.write(bloque)


if __name__ == "__main__":
    import os

    # Crear archivo de prueba
    with open("origen.bin", "wb") as f:
        f.write(b"\x00\x01\x02\x03" * 100)        # 400 bytes

    assert os.path.getsize("origen.bin") == 400

    # Copiar
    copiar_binario("origen.bin", "destino.bin")

    # VERIFICACIN: idntico byte a byte
    with open("origen.bin", "rb") as f1:
        original = f1.read()
    with open("destino.bin", "rb") as f2:
        copia = f2.read()

    assert original == copia, "la copia debe ser idntica"
    assert os.path.getsize("destino.bin") == 400
    print(f"Archivo de 400 bytes copiado y verificado")

    # Caso base: archivo vacio
    with open("vacio.bin", "wb") as f:
        pass
    copiar_binario("vacio.bin", "vacio_copia.bin")
    assert os.path.getsize("vacio_copia.bin") == 0
    with open("vacio_copia.bin", "rb") as f:
        assert f.read() == b""
    print("Archivo vacio: copia vacia correcta")

    # Archivo de 1 byte
    with open("uno.bin", "wb") as f:
        f.write(b"\xff")
    copiar_binario("uno.bin", "uno_copia.bin")
    with open("uno_copia.bin", "rb") as f:
        assert f.read() == b"\xff"

    # Archivo ms grande que el buffer
    datos_grandes = bytes(range(256)) * 40    # 10,240 bytes
    with open("grande.bin", "wb") as f:
        f.write(datos_grandes)
    copiar_binario("grande.bin", "grande_copia.bin", tamano_buffer=1024)
    with open("grande_copia.bin", "rb") as f:
        assert f.read() == datos_grandes
    print(f"Archivo de 10,240 bytes con buffer de 1024: correcto")

    # El tamao del buffer NO afecta el resultado
    for tam in [1, 7, 512, 4096, 100000]:
        copiar_binario("grande.bin", "test_tam.bin", tamano_buffer=tam)
        with open("test_tam.bin", "rb") as f:
            assert f.read() == datos_grandes, f"fallo con buffer {tam}"
    print("El resultado es identico con cualquier tamao de buffer")

    # Medir el efecto del buffer en el rendimiento
    import time
    grande_real = os.urandom(1024 * 1024)        # 1 MB
    with open("mb.bin", "wb") as f:
        f.write(grande_real)

    print(f"\nCopiando 1 MB con distintos buffers:")
    for tam in [512, 4096, 65536]:
        inicio = time.time()
        copiar_binario("mb.bin", "mb_copia.bin", tamano_buffer=tam)
        t = time.time() - inicio
        with open("mb_copia.bin", "rb") as f:
            assert f.read() == grande_real
        print(f"  buffer {tam:>6}: {t*1000:.0f} ms")

    # Buffer demasiado pequee: ms llamadas al sistema
    # (no se mide tiempo pero se explica el principio)
    n_llamadas_512 = 1024 * 1024 // 512
    n_llamadas_64k = 1024 * 1024 // 65536
    print(f"\nLlamadas al sistema para 1 MB:")
    print(f"  buffer 512:   {n_llamadas_512:,} llamadas")
    print(f"  buffer 64 KB: {n_llamadas_64k} llamadas")
    print(f"  Reduccin: {n_llamadas_512 // n_llamadas_64k}x menos llamadas")

    # Verificacin con hashing: ms robusto que comparar en memoria
    import hashlib

    def hash_archivo(ruta):
        h = hashlib.sha256()
        with open(ruta, "rb") as f:
            for bloque in iter(lambda: f.read(4096), b""):
                h.update(bloque)
        return h.hexdigest()

    h1 = hash_archivo("origen.bin")
    h2 = hash_archivo("destino.bin")
    assert h1 == h2
    print(f"\nHash SHA-256 coincide: {h1[:16]}...")

    for a in ["origen.bin", "destino.bin", "vacio.bin", "vacio_copia.bin",
              "uno.bin", "uno_copia.bin", "grande.bin", "grande_copia.bin",
              "test_tam.bin", "mb.bin", "mb_copia.bin"]:
        if os.path.exists(a):
            os.remove(a)

    print("\n Todas las pruebas pasaron")
