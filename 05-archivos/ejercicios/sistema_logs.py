r"""
Ejercicio 12: Sistema de logs simple
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Modo append "a" (ejercicio 4): los logs NUNCA se truncan.
    - El formato de logs: timestamp, nivel, mensaje.
    - Gestor de contexto `with` (00-fundamentos 10.5).

PROBLEMA
    Registrar eventos con marca de tiempo, nivel de severidad y
    mensaje, escribindolos a un archivo.

FONDO MATEMTICO
    Un log es una secuencia de eventos ordenados cronolgicamente. El
    formato estndar (syslog, CLF) tiene tres campos:

        [timestamp] [NIVEL] mensaje

    Los niveles habituales, de menor a mayor severidad:
        DEBUG < INFO < WARNING < ERROR < CRITICAL

    El nivel permite FILTRAR: en produccin se registra INFO hacia
    arriba; en desarrollo, todo. Sin niveles, un log es intil a escala.

ESTRATEGIA
    Una clase con tres mtodos pblicos (info, warning, error) que
    comparten una implementacin comn:

```python
class SistemaLogs:
    def __init__(self, archivo):
        self.archivo = archivo

    def log(self, nivel, mensaje):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{timestamp}] [{nivel}] {mensaje}\n"
        with open(self.archivo, "a", encoding="utf-8") as f:
            f.write(linea)
```

    Cinco decisiones, ninguna decorativa:
      1. Modo "a": cada evento AADE al final. Con "w" se borrara el
         histrico completo.
      2. encoding="utf-8": el problema de siempre.
      3. `with`: cierra siempre, incluso con excepcin.
      4. El "\\n" final: sin l, todas las lneas se pegaran.
      5. Un solo mtodo interno (log) y tres envolturas: evita duplicar
         el formato en cada nivel.

TRAZA de uso
    logs.info("Aplicacin iniciada")
      -> [2024-01-15 10:30:00] [INFO] Aplicacin iniciada

    logs.error("Error de conexin")
      -> [2024-01-15 10:30:05] [ERROR] Error de conexin

COMPLEJIDAD
    Cada llamada: O(1) amortizado. La escritura va a un bufer que el
    sistema operativo vaca en bloque, as que una lnea cuesta O(1)
    aunque el archivo crezca.

    Overhead real: abrir y cerrar el archivo en cada evento tiene
    costo de sistema. En produccin se usa un archivo persistente o
    el mdulo logging.

POR QU USAR LA BIBLIOTECA logging EN PRODUCCIN
    Esta implementacin es didctica. El mdulo `logging` de Python
    ofrece:
      - Rotacin de archivos (evita que crezcan sin lmite).
      - Niveles configurables y filtros.
      - Handlers mltiples (archivo + consola + red).
      - Formato configurable.
      - Thread-safety.

    Regla: usar esto para aprender, `logging` para cdigo real.

APLICACIONES
    - Depuracin: rastrear el flujo de ejecucin.
    - Auditora: registrar quin hizo qu y cundo.
    - Monitorizacin: detectar errores en produccin.

RELACIN CON OTROS TEMAS
    - El tema 06 (grandes datos) muestra cmo PROCESAR logs masivos sin
      cargarlos en memoria: leer con `for linea in f`.
"""


from datetime import datetime


class SistemaLogs:
    """Sistema de logs simple con append y niveles."""

    def __init__(self, archivo="app.log"):
        self.archivo = archivo

    def log(self, nivel, mensaje):
        """Escribe una lnea con timestamp y nivel. O(1) amortizado."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{timestamp}] [{nivel}] {mensaje}\n"

        # Modo "a": append, no borra el histrico.
        # encoding="utf-8": no depender del locale del sistema.
        with open(self.archivo, "a", encoding="utf-8") as f:
            f.write(linea)

    def info(self, mensaje):
        self.log("INFO", mensaje)

    def warning(self, mensaje):
        self.log("WARNING", mensaje)

    def error(self, mensaje):
        self.log("ERROR", mensaje)


if __name__ == "__main__":
    import os

    archivo = "test.log"
    logs = SistemaLogs(archivo)

    logs.info("Aplicacin iniciada")
    logs.warning("Espacio en disco bajo")
    logs.error("Error de conexin")

    with open(archivo, "r", encoding="utf-8") as f:
        contenido = f.read()
    print("Contenido del log:")
    print(contenido)

    # Los tres niveles estn registrados
    assert "INFO" in contenido
    assert "WARNING" in contenido
    assert "ERROR" in contenido

    # Los mensajes estn completos
    assert "Aplicacin iniciada" in contenido
    assert "Espacio en disco bajo" in contenido
    assert "Error de conexin" in contenido

    # Formato: [timestamp] [NIVEL] mensaje, una lnea por evento
    lineas = contenido.strip().split("\n")
    assert len(lineas) == 3, "tres eventos, tres lneas"
    for linea in lineas:
        assert linea.startswith("["), "empieza con timestamp"
        assert "] [" in linea, "los dos campos entre corchetes"

    # Las entradas tienen salto de lnea: no se pegan
    assert contenido.count("\n") == 3

    # APPEND: una segunda ronda AADE, no borra
    logs.info("Segunda ronda")
    with open(archivo, "r", encoding="utf-8") as f:
        contenido2 = f.read()
    assert contenido in contenido2, "el append conserva lo anterior"
    assert "Segunda ronda" in contenido2
    assert contenido2.count("\n") == 4
    print("Append verificado: el histrico se conserva")

    # El timestamp tiene el formato correcto
    primera = contenido2.split("\n")[0]
    ts = primera[primera.index("[") + 1: primera.index("]")]
    assert len(ts) == 19, f"timestamp inesperado: {ts}"
    assert ts[4] == "-" and ts[7] == "-" and ts[10] == " "
    assert ts[13] == ":" and ts[16] == ":"
    print(f"Timestamp con formato vlido: {ts}")

    # El orden cronolgico se preserva
    assert contenido2.index("Aplicacin iniciada") < contenido2.index("Segunda ronda")

    # Archivo nuevo: se crea si no existe
    os.remove(archivo)
    assert not os.path.exists(archivo)
    logs2 = SistemaLogs(archivo)
    logs2.info("Desde cero")
    assert os.path.exists(archivo), "se cre el archivo"

    # Muchas escrituras: el archivo crece correctamente
    with open(archivo, "w", encoding="utf-8") as f:
        pass
    for i in range(1000):
        logs2.info(f"Evento {i}")
    with open(archivo, "r", encoding="utf-8") as f:
        n = sum(1 for _ in f)
    assert n == 1000
    print(f"\n1000 eventos escritos: {n} lneas")
    print(f"Tamao del archivo: {os.path.getsize(archivo)} bytes")

    # El rendimiento no degrada con el tamao (append es O(1) al final)
    import time
    with open(archivo, "w", encoding="utf-8") as f:
        pass

    inicio = time.time()
    for i in range(2000):
        logs2.info(f"Lote 1 evento {i}")
    t1 = time.time() - inicio

    inicio = time.time()
    for i in range(2000):
        logs2.info(f"Lote 2 evento {i}")
    t2 = time.time() - inicio

    print(f"\n2000 eventos con archivo vacio:  {t1*1000:.0f} ms")
    print(f"2000 eventos con archivo de 2000: {t2*1000:.0f} ms")
    print("  (similares: ir al final es O(1), no depende del tamao)")

    os.remove(archivo)
    print("\n Todas las pruebas pasaron")
