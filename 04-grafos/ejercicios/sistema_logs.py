"""
Ejercicio 12: Sistema de logs simple
Dificultad: Intermedio

Escribe mensajes de log con timestamp a un archivo.
"""


from datetime import datetime


class SistemaLogs:
    def __init__(self, archivo="app.log"):
        self.archivo = archivo

    def log(self, nivel, mensaje):
        """Escribe un mensaje de log con timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{timestamp}] [{nivel}] {mensaje}\n"
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

    logs = SistemaLogs("test.log")
    logs.info("Aplicación iniciada")
    logs.warning("Espacio en disco bajo")
    logs.error("Error de conexión")

    with open("test.log", "r") as f:
        contenido = f.read()

    print("Contenido del log:")
    print(contenido)

    assert "INFO" in contenido
    assert "WARNING" in contenido
    assert "ERROR" in contenido
    os.remove("test.log")
    print("\n✓ Todas las pruebas pasaron")
