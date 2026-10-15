r"""
Ejercicio 4: Aadir al final de un archivo
Dificultad: Bsico

CONOCIMIENTO PREVIO NECESARIO
    - Modo "a" (teoria.md 3.1): la diferencia con "w".
    - Sistemas de logs (tema 04, ejercicio 12).
    - Buffering: por qu el append es eficiente.

PROBLEMA
    Aadir contenido al final de un archivo sin borrar lo existente.

FONDO MATEMTICO
    El modo "a" (append) coloca el puntero al FINAL del archivo. Toda
    escritura va al final, sin importar cuntas veces se abra.

    Es la semntica correcta para:
      - Logs: cada evento se aade.
      - Acumuladores: ir sumando resultados.
      - Auditora: no se puede borrar el historial.

    ATENCIN: si dos procesos abren el mismo archivo en modo "a", las
    escrituras pueden entrelazarse. Para concurrencia real hace falta
    bloqueo explcito.

ESTRATEGIA

```python
with open("app.log", "a", encoding="utf-8") as f:
    f.write("[evento] mensaje\n")
```

    Es una sola operación: abrir en modo append. No hace falta leer el
    archivo, buscar el final, ni posicionarse: el sistema operativo lo
    hace.

TRAZA
    Estado inicial:  "lnea 1\n"

    open("f.txt", "a")   -> puntero al final (posición 8)
    f.write("lnea 2\n")  -> escribe en la posición 8

    Estado final:  "lnea 1\nlnea 2\n"

COMPLEJIDAD
    Cada append cuesta O(k) donde k es la cantidad escrita.
    Ir al final es O(1) para el sistema operativo (el tamao se guarda
    en el i-nodo), as que el rendimiento NO degrada con el tamao del
    archivo. Por eso los logs pueden crecer a gigabytes sin problema.

DEMOSTRACIN DE CORRECCIN
    El modo "a" garantiza por especificacin POSIX que toda escritura
    ocurre al final del archivo. Como cada llamada aade bytes al
    final, el contenido previo queda intacto y el nuevo se acumula
    detrás. Luego el resultado es la concatenacin en orden. 

CASOS LMITE
    - Archivo inexistente: se CREA (a diferencia de "r").
    - Archivo vaco: funciona igual.
    - Contenido sin "\n": se pega al final de la ltima lnea.

APLICACIONES
    - Logs de aplicación y de servidor.
    - Acumular resultados de procesamiento por lotes.
    - Archivos de auditora.

RELACIN CON OTROS TEMAS
    - El tema 04 (ejercicio 12) implementa un sistema de logs sobre
      esta primitiva.
"""


def anadir_texto(archivo, texto):
    """Aade texto al final del archivo. O(len(texto))."""
    with open(archivo, "a", encoding="utf-8") as f:
        f.write(texto)


def anadir_linea(archivo, texto):
    """Aade una lnea, garantizando el salto final."""
    with open(archivo, "a", encoding="utf-8") as f:
        f.write(texto.rstrip("\n") + "\n")


if __name__ == "__main__":
    import os

    archivo = "test.txt"

    # Empezar con contenido conocido
    with open(archivo, "w", encoding="utf-8") as f:
        f.write("linea 1\n")

    # Aadir una lnea
    anadir_texto(archivo, "linea 2\n")
    with open(archivo, "r", encoding="utf-8") as f:
        contenido = f.read()
    assert contenido == "linea 1\nlinea 2\n"
    print(f"Tras anadir: {contenido!r}")

    # Aadir varias veces: el orden se conserva
    anadir_texto(archivo, "linea 3\n")
    anadir_texto(archivo, "linea 4\n")
    with open(archivo, "r", encoding="utf-8") as f:
        contenido = f.read()
    assert contenido == "linea 1\nlinea 2\nlinea 3\nlinea 4\n"
    assert contenido.index("linea 2") < contenido.index("linea 3")
    assert contenido.index("linea 3") < contenido.index("linea 4")
    print(f"Orden preservado: {contenido.count(chr(10))} lineas")

    # anadir_linea normaliza el salto final
    with open(archivo, "w", encoding="utf-8") as f:
        f.write("")
    anadir_linea(archivo, "linea A")             # sin \n
    anadir_linea(archivo, "linea B\n")           # con \n
    anadir_linea(archivo, "linea C")             # sin \n
    with open(archivo, "r", encoding="utf-8") as f:
        lineas = f.read().splitlines()
    assert lineas == ["linea A", "linea B", "linea C"], lineas
    print(f"anadir_linea normaliza saltos: {lineas}")

    # Archivo inexistente: se CREA
    if os.path.exists("nuevo.txt"):
        os.remove("nuevo.txt")
    anadir_texto("nuevo.txt", "creado\n")
    assert os.path.exists("nuevo.txt")
    print("El archivo inexistente se crea en modo 'a'")

    # Archivo vacio: funciona
    with open("vacio.txt", "w", encoding="utf-8") as f:
        pass
    anadir_texto("vacio.txt", "primera\n")
    with open("vacio.txt", encoding="utf-8") as f:
        assert f.read() == "primera\n"

    # Muchos appends: el archivo crece correctamente
    with open("muchos.txt", "w", encoding="utf-8") as f:
        pass
    for i in range(1000):
        anadir_linea("muchos.txt", f"Evento {i}")
    with open("muchos.txt", "r", encoding="utf-8") as f:
        n = sum(1 for _ in f)
    assert n == 1000
    print(f"\n1000 appends: {n} lineas, {os.path.getsize('muchos.txt')} bytes")

    # Sin "\n" las escrituras se pegan
    with open("pegado.txt", "w", encoding="utf-8") as f:
        f.write("A")
    anadir_texto("pegado.txt", "B")
    anadir_texto("pegado.txt", "C")
    with open("pegado.txt", encoding="utf-8") as f:
        assert f.read() == "ABC", "sin saltos, todo se pega"
    print("Sin \\n: 'A'+'B'+'C' = 'ABC' (pegado)")

    # Rendimiento: el append NO degrada con el tamano del archivo
    import time
    with open("lento.txt", "w", encoding="utf-8") as f:
        pass

    inicio = time.time()
    for i in range(2000):
        anadir_linea("lento.txt", f"Linea {i}")
    t1 = time.time() - inicio

    inicio = time.time()
    for i in range(2000, 4000):
        anadir_linea("lento.txt", f"Linea {i}")
    t2 = time.time() - inicio

    print(f"\n2000 appends con archivo vacio:   {t1*1000:.0f} ms")
    print(f"2000 appends con archivo de 2000: {t2*1000:.0f} ms")
    print("  (ambos deberian ser similares: ir al final es O(1))")

    for a in ["test.txt", "nuevo.txt", "vacio.txt", "muchos.txt",
              "pegado.txt", "lento.txt"]:
        os.remove(a)

    print("\n Todas las pruebas pasaron")
