r"""
Ejercicio 17: Sistema de archivos simple
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - Diccionarios anidados (00-fundamentos §10.1).
    - Recursión sobre estructuras anidadas (tema 01, §3.2).
    - Operaciones de archivo (tema 05).

PROBLEMA
    Implementar un sistema de archivos virtual con directorios,
    archivos y operaciones básicas: crear, leer, eliminar, listar.

FONDO MATEMÁTICO
    Un sistema de archivos es un ÁRBOL:
      - Los nodos internos son DIRECTORIOS.
      - Las hojas son ARCHIVOS.
      - Las aristas son la relación "contiene".

    Por eso las operaciones son recursivas: listar un directorio
    implica listar sus subdirectorios, que a su vez contienen
    subdirectorios.

ESTRATEGIA
    Representar el árbol con diccionarios anidados:

        {
            "/": {
                "documentos": {
                    "nota.txt": "contenido...",
                    "fotos": {
                        "playa.jpg": "<bytes>"
                    }
                }
            }
        }

    Un directorio es un diccionario. Un archivo es una cadena (su
    contenido). Se distinguen por el tipo del valor.

    Las rutas se dividen por "/". Para llegar a un archivo hay que
    bajar nivel a nivel.

TRAZA de navegación
    ruta = "/documentos/nota.txt"
    partes = ["", "documentos", "nota.txt"]   (split por "/")
    actual = raíz
    "documentos" → bajar al subdirectorio
    "nota.txt" → es el archivo. Devolver su contenido.

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción sobre la profundidad de la ruta. Una ruta de
    profundidad 1 nombra un hijo directo de la raíz. Si la ruta tiene
    profundidad k, se resuelve el subproblema de profundidad k−1
    dentro del directorio indicado. ∎

COMPLEJIDAD
    Operación               Complejidad
    crear archivo           O(profundidad de la ruta)
    leer archivo            O(profundidad)
    listar directorio       O(número de hijos directos)
    eliminar archivo        O(profundidad)
    eliminar directorio     O(tamaño del subárbol)
    búsqueda por nombre     O(n) en el peor caso (recorrer todo)

APLICACIONES
    - Sistemas de archivos reales (ext4, NTFS): usan árboles B+.
    - Almacenamiento en memoria de estructuras jerárquicas.
    - Navegadores: el DOM es un árbol similar.

RELACIÓN CON OTROS TEMAS
    - Es la misma estructura de LISTAS ANIDADAS del tema 01 (§3.2):
      un directorio contiene archivos y otros directorios.
"""


class SistemaArchivos:
    """Sistema de archivos virtual representado como árbol de dicts."""

    def __init__(self):
        self.raiz = {}

    def _navegar(self, ruta, crear=False):
        """Baja por la ruta devolviendo el nodo final.

        Las partes vacías (por el / inicial) se ignoran.
        """
        partes = [p for p in ruta.split("/") if p]
        nodo = self.raiz

        for parte in partes:
            if parte not in nodo:
                if crear:
                    nodo[parte] = {}
                else:
                    return None
            nodo = nodo[parte]

        return nodo

    def crear_directorio(self, ruta):
        """Crea un directorio (y los padres que falten)."""
        self._navegar(ruta, crear=True)

    def crear_archivo(self, ruta, contenido=""):
        """Crea un archivo con contenido en la ruta indicada."""
        partes = [p for p in ruta.split("/") if p]
        if not partes:
            raise ValueError("Ruta inválida")

        directorio = self._navegar("/".join(partes[:-1]), crear=True)
        directorio[partes[-1]] = contenido

    def leer_archivo(self, ruta):
        """Lee el contenido de un archivo. None si no existe."""
        partes = [p for p in ruta.split("/") if p]
        if not partes:
            return None

        directorio = self._navegar("/".join(partes[:-1]))
        if directorio is None:
            return None
        return directorio.get(partes[-1])

    def eliminar_archivo(self, ruta):
        """Elimina un archivo. Devuelve True si existía."""
        partes = [p for p in ruta.split("/") if p]
        if not partes:
            return False

        directorio = self._navegar("/".join(partes[:-1]))
        if directorio is None or partes[-1] not in directorio:
            return False

        del directorio[partes[-1]]
        return True

    def listar_directorio(self, ruta):
        """Devuelve los nombres de los hijos directos."""
        nodo = self._navegar(ruta)
        if nodo is None:
            return []
        return list(nodo.keys())

    def es_directorio(self, ruta):
        nodo = self._navegar(ruta)
        return isinstance(nodo, dict)

    def tamano_total(self, ruta="/"):
        """Suma el tamaño del contenido de todos los archivos."""
        nodo = self._navegar(ruta)
        return self._tamano(nodo)

    def _tamano(self, nodo):
        """Cuenta recursivamente el tamaño del contenido."""
        if nodo is None:
            return 0
        if isinstance(nodo, str):
            return len(nodo)                    # archivo: su largo
        return sum(self._tamano(v) for v in nodo.values())


if __name__ == "__main__":
    fs = SistemaArchivos()

    # Crear estructura
    fs.crear_directorio("/documentos")
    fs.crear_directorio("/documentos/fotos")
    fs.crear_archivo("/documentos/nota.txt", "Hola, mundo!")
    fs.crear_archivo("/documentos/fotos/playa.jpg", "<imagen>")
    fs.crear_archivo("/documentos/datos.csv", "a,b\n1,2\n")

    print("Contenido de /documentos:")
    print(f"  {sorted(fs.listar_directorio('/documentos'))}")

    assert sorted(fs.listar_directorio("/documentos")) == \
        ["datos.csv", "fotos", "nota.txt"]

    # Leer archivos
    assert fs.leer_archivo("/documentos/nota.txt") == "Hola, mundo!"
    assert fs.leer_archivo("/documentos/fotos/playa.jpg") == "<imagen>"
    print(f"\n/datos.csv = {fs.leer_archivo('/documentos/datos.csv')!r}")

    # Archivo inexistente
    assert fs.leer_archivo("/documentos/inexistente.txt") is None
    assert fs.leer_archivo("/no/existe/ruta") is None

    # Directorios vs archivos
    assert fs.es_directorio("/documentos") is True
    assert fs.es_directorio("/documentos/fotos") is True
    assert fs.es_directorio("/documentos/nota.txt") is False
    assert fs.es_directorio("/no/existe") is False

    # Eliminar archivo
    assert fs.eliminar_archivo("/documentos/datos.csv") is True
    assert fs.leer_archivo("/documentos/datos.csv") is None
    assert fs.eliminar_archivo("/documentos/datos.csv") is False, "ya no existe"
    print("\nArchivo eliminado correctamente")

    # Directorio con la creación implícita de padres
    fs.crear_archivo("/a/b/c/profundo.txt", "x")
    assert fs.leer_archivo("/a/b/c/profundo.txt") == "x"
    assert fs.es_directorio("/a/b/c") is True
    print("Creación implícita de /a/b/c verificada")

    # Caso base: raíz vacía
    vacio = SistemaArchivos()
    assert vacio.listar_directorio("/") == []
    assert vacio.leer_archivo("/algo") is None

    # Caso base: un solo archivo
    simple = SistemaArchivos()
    simple.crear_archivo("/solo.txt", "contenido")
    assert simple.listar_directorio("/") == ["solo.txt"]
    assert simple.leer_archivo("/solo.txt") == "contenido"

    # Estructura jerárquica profunda
    profundo = SistemaArchivos()
    actual = "/"
    for i in range(10):
        actual += f"nivel{i}/"
        profundo.crear_archivo(actual + f"archivo{i}.txt", "x" * i)
    assert profundo.leer_archivo("/nivel0/nivel1/nivel2/archivo2.txt") == "xx"

    # El listado de un directorio solo muestra hijos DIRECTOS
    assert "nivel1" in profundo.listar_directorio("/nivel0")
    assert "archivo0.txt" in profundo.listar_directorio("/nivel0")
    assert "nivel2" not in profundo.listar_directorio("/nivel0"), "no es nieto"

    # Verificación: un archivo dentro de un directorio no aparece
    # en el listado de la RAÍZ
    assert "nota.txt" not in fs.listar_directorio("/")
    assert "documentos" in fs.listar_directorio("/")

    # Rutas con barras dobles o finales se normalizan
    fs2 = SistemaArchivos()
    fs2.crear_archivo("/x/y.txt", "dato")
    assert fs2.leer_archivo("//x//y.txt") == "dato", "barras dobles"
    assert fs2.leer_archivo("/x/y.txt/") == "dato", "barra final"

    print("\n✓ Todas las pruebas pasaron")
