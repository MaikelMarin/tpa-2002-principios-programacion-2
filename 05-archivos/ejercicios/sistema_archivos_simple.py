"""
Ejercicio 14: Sistema de archivos simple
Dificultad: Experto

Implementa un sistema de archivos virtual con operaciones básicas.
"""


class SistemaArchivosSimple:
    def __init__(self):
        self.archivos = {}
        self.directorios = {"/": []}

    def crear_directorio(self, ruta):
        """Crea un directorio en la ruta especificada."""
        if ruta not in self.directorios:
            self.directorios[ruta] = []
            padre = self._directorio_padre(ruta)
            if padre in self.directorios:
                self.directorios[padre].append(ruta)

    def crear_archivo(self, ruta, contenido=""):
        """Crea un archivo con contenido."""
        self.archivos[ruta] = contenido
        padre = self._directorio_padre(ruta)
        if padre in self.directorios:
            self.directorios[padre].append(ruta)

    def leer_archivo(self, ruta):
        """Lee el contenido de un archivo."""
        return self.archivos.get(ruta, None)

    def eliminar_archivo(self, ruta):
        """Elimina un archivo."""
        if ruta in self.archivos:
            del self.archivos[ruta]
            padre = self._directorio_padre(ruta)
            if padre in self.directorios and ruta in self.directorios[padre]:
                self.directorios[padre].remove(ruta)

    def listar_directorio(self, ruta):
        """Lista el contenido de un directorio."""
        return self.directorios.get(ruta, [])

    def _directorio_padre(self, ruta):
        """Obtiene el directorio padre de una ruta."""
        if ruta == "/":
            return None
        partes = ruta.rstrip("/").split("/")
        if len(partes) <= 1:
            return "/"
        return "/".join(partes[:-1]) or "/"


if __name__ == "__main__":
    fs = SistemaArchivosSimple()
    fs.crear_directorio("/documentos")
    fs.crear_archivo("/documentos/nota.txt", "Hola, mundo!")
    fs.crear_archivo("/documentos/datos.csv", "nombre,edad\nAna,25")

    print("Contenido de /documentos:")
    for item in fs.listar_directorio("/documentos"):
        print(f"  {item}")

    print(f"\nLeer /documentos/nota.txt: {fs.leer_archivo('/documentos/nota.txt')}")

    assert fs.leer_archivo("/documentos/nota.txt") == "Hola, mundo!"
    assert "/documentos/nota.txt" in fs.listar_directorio("/documentos")
    print("\n✓ Todas las pruebas pasaron")
