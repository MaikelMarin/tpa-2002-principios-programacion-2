r"""
Ejercicio 12: Sistema de logs simple
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Escritura en modo append (tema 05, ejercicio 2).
    - El formato de logs: timestamp, nivel, mensaje.
    - Gestor de contexto `with` (00-fundamentos §10.5).

PROBLEMA
    Implementar un sistema de logs que registre eventos con marca de
    tiempo, nivel de severidad y mensaje, escribiendo a un archivo.

FONDO MATEMÁTICO
    Un log es una secuencia de eventos ordenados cronológicamente. El
    formato estándar (p. ej. syslog, CLF) tiene tres campos:

        [timestamp] [nIVEL] mensaje

    Los niveles habituales, de menor a mayor severidad:
        DEBUG < INFO < WARNING < ERROR < CRITICAL

    El nivel permite filtrar: en producción se suele registrar INFO
    hacia arriba; en desarrollo, todo.

ESTRATEGIA
    Una clase con tres métodos (info, warning, error) que comparten
    una implementación común:

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

    Puntos clave:
      1. Modo "a" (append): cada llamada AÑADE al final. Con "w" se
         borraría el log anterior.
      2. `encoding="utf-8"`: el valor por defecto depende del sistema
         operativo, lo que causa errores difíciles de depurar.
      3. `with`: garantiza el cierre incluso si hay excepción.
      4. El `\n` al final: sin él, todas las líneas se pegarían.

TRAZA de uso
    logs.info("Aplicación iniciada")
      → [2024-01-15 10:30:00] [INFO] Aplicación iniciada

    logs.error("Error de conexión")
      → [2024-01-15 10:30:05] [ERROR] Error de conexión

COMPLEJIDAD
    Cada llamada: O(1) amortizado. La escritura va a un búfer que el
    sistema operativo vacía en bloque, así que una línea cuesta O(1)
    aunque el archivo crezca.

    Nota: escribir una línea por evento con open/close cada vez tiene
    overhead de sistema. En producción se usa un archivo abierto
    persistente o una biblioteca especializada (logging).

POR QUÉ USAR LA BIBLIOTECA logging EN PRODUCCIÓN
    Esta implementación es didáctica. El módulo `logging` de Python
    ofrece: rotación de archivos, niveles configurables, handlers
    múltiples (archivo + consola + red), formato configurable y
    thread-safety. Para código real se usa `logging`.

APLICACIONES
    - Depuración: rastrear el flujo de ejecución.
    - Auditoría: registrar quién hizo qué y cuándo.
    - Monitorización: detectar errores en producción.

RELACIÓN CON OTROS TEMAS
    - El tema 05 cubre las operaciones de archivo que esto usa.
    - El tema 06 (grandes datos) muestra cómo PROCESAR logs masivos
      sin cargarlos en memoria.
"""


from datetime import datetime


class SistemaLogs:
    """Sistema de logs simple con append y niveles."""

    def __init__(self, archivo="app.log"):
        self.archivo = archivo

    def log(self, nivel, mensaje):
        """Escribe una línea con timestamp y nivel. O(1) amortizado."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{timestamp}] [{nivel}] {mensaje}\n"

        # Modo "a": append, no borra lo anterior
        # encoding="utf-8": evita depender del locale del sistema
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

    logs.info("Aplicación iniciada")
    logs.warning("Espacio en disco bajo")
    logs.error("Error de conexión")

    with open(archivo, "r", encoding="utf-8") as f:
        contenido = f.read()

    print("Contenido del log:")
    print(contenido)

    # Los tres niveles están registrados
    assert "INFO" in contenido
    assert "WARNING" in contenido
    assert "ERROR" in contenido

    # Los mensajes están completos
    assert "Aplicación iniciada" in contenido
    assert "Espacio en disco bajo" in contenido
    assert "Error de conexión" in contenido

    # Formato: [timestamp] [NIVEL] mensaje, una línea por evento
    lineas = contenido.strip().split("\n")
    assert len(lineas) == 3, "tres eventos, tres líneas"
    for linea in lineas:
        assert linea.startswith("["), "empieza con timestamp"
        assert "]" in linea and "[" in linea, "tiene los dos campos"
        partes = linea.split("] ")
        assert len(partes) >= 2, "timestamp y resto separables"

    # Las entradas tienen salto de línea: no se pegan
    assert contenido.count("\n") == 3

    # APPEND: una segunda ronda debe AÑADIR, no borrar
    logs.info("Segunda ronda")
    with open(archivo, "r", encoding="utf-8") as f:
        contenido2 = f.read()
    assert contenido in contenido2, "el modo append conserva lo anterior"
    assert "Segunda ronda" in contenido2
    assert contenido2.count("\n") == 4

    # El timestamp tiene el formato correcto
    primera = contenido2.split("\n")[0]
    inicio = primera.index("[") + 1
    fin = primera.index("]")
    ts = primera[inicio:fin]
    # Formato: AAAA-MM-DD HH:MM:SS
    assert len(ts) == 19, f"timestamp inesperado: {ts}"
    assert ts[4] == "-" and ts[7] == "-" and ts[10] == " "
    assert ts[13] == ":" and ts[16] == ":"

    # El orden cronológico se preserva (append)
    assert contenido2.index("Aplicación iniciada") < contenido2.index("Segunda ronda")

    # Archivo nuevo: se crea si no existe
    os.remove(archivo)
    assert not os.path.exists(archivo)
    logs2 = SistemaLogs(archivo)
    logs2.info("Desde cero")
    assert os.path.exists(archivo), "se creó el archivo"
    with open(archivo, "r", encoding="utf-8") as f:
        assert "Desde cero" in f.read()

    # Muchas escrituras: el archivo crece correctamente
    with open(archivo, "w") as f:
        pass                                        # vaciar
    for i in range(1000):
        logs2.info(f"Evento {i}")
    with open(archivo, "r", encoding="utf-8") as f:
        n = sum(1 for _ in f)
    assert n == 1000, f"esperaba 1000 líneas, hay {n}"
    print(f"\n1000 eventos escritos: {n} líneas")
    print(f"Tamaño del archivo: {os.path.getsize(archivo)} bytes")

    os.remove(archivo)
    print("\n✓ Todas las pruebas pasaron")
