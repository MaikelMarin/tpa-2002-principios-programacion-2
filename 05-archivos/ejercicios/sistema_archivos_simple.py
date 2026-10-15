r"""
Ejercicio 14: Sistema de archivos simple
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - Diccionarios anidados (00-fundamentos 10.1).
    - Recursin sobre estructuras anidadas (tema 01, 3.2).
    - Operaciones de archivo (tema 05).
    - El concepto de ruta (path).

PROBLEMA
    Implementar un sistema de archivos virtual con directorios,
    archivos, y operaciones: crear, leer, eliminar, listar.

FONDO MATEMTICO
    Un sistema de archivos es un RBOL:
      - Nodos internos = DIRECTORIOS.
      - Hojas = ARCHIVOS.
      - Aristas = relacion "contiene".

    Por eso las operaciones son recursivas: listar un directorio
    implica listar sus subdirectorios.

ESTRATEGIA
    Representar el rbol con diccionarios anidados:

        {
            "documentos": {
                "nota.txt": "contenido...",
                "fotos": {
                    "playa.jpg": "<bytes>"
                }
            }
        }

    Un directorio es un diccionario. Un archivo es una cadena (su
    contenido). Se distinguen por el TIPO del valor.

    Las rutas se dividen por "/". Para llegar a un archivo hay que
    bajar nivel a nivel.

TRAZA de navegacion
    ruta = "/documentos/nota.txt"
    split("/") -> ["", "documentos", "nota.txt"]
    filtrar vacios -> ["documentos", "nota.txt"]
    nodo = raiz
    "documentos" -> bajar al subdirectorio
    "nota.txt" -> es el archivo. Devolver su contenido.

DEMOSTRACIN DE CORRECCIN
    Por induccin sobre la profundidad de la ruta. Una ruta de
    profundidad 1 nombra un hijo directo de la raiz. Si la ruta tiene
    profundidad k, se resuelve el subproblema de profundidad k-1
    dentro del directorio indicado. Caso base: profundidad 0 = raz. 

COMPLEJIDAD
    Operacion               Complejidad
    crear archivo           O(profundidad de la ruta)
    leer archivo            O(profundidad)
    listar directorio       O(hijos directos)
    eliminar archivo        O(profundidad)
    eliminar directorio     O(tamano del subárbol)
    busqueda por nombre     O(n) peor caso (recorrer todo)

    Note: todas las operaciones trabajan sobre la PROFUNDIDAD de la
    ruta, no sobre el tamano total del sistema. Es la ventaja de la
    estructura jerrquica frente a una lista plana.

NORMALIZACIN DE RUTAS
    Rutas equivalentes deben resolverse igual:
        "/x/y.txt" == "//x//y.txt" == "/x/y.txt/"
    Se logra dividiendo por "/" y descartando las partes vacias.

APLICACIONES
    - Sistemas de archivos reales (ext4, NTFS): usan rboles B+.
    - Almacenamiento en memoria de estructuras jerrquicas.
    - Navegadores: el DOM es un rbol similar.

RELACIN CON OTROS TEMAS
    - Es la misma estructura de LISTAS ANIDADAS del tema 01 (3.2):
      un directorio contiene archivos y otros directorios.
"""


class SistemaArchivosSimple:
    """Sistema de archivos virtual representado como rbol de dicts."""

    def __init__(self):
        self.raiz = {}

    def _navegar(self, ruta, crear=False):
        """Baja por la ruta devolviendo el nodo final (o None)."""
        # Normalizar: dividir por "/" y descartar partes vacias
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
            raise ValueError("Ruta invalida")

        # Navegar al directorio PADRE, crendolo si falta
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
        """Elimina un archivo. True si existia."""
        partes = [p for p in ruta.split("/") if p]
        if not partes:
            return False

        directorio = self._navegar("/".join(partes[:-1]))
        if directorio is None or partes[-1] not in directorio:
            return False

        del directorio[partes[-1]]
        return True

    def listar_directorio(self, ruta):
        """Devuelve los nombres de los hijos DIRECTOS."""
        nodo = self._navegar(ruta)
        if nodo is None:
            return []
        return list(nodo.keys())

    def es_directorio(self, ruta):
        nodo = self._navegar(ruta)
        return isinstance(nodo, dict)

    def tamano_total(self, ruta="/"):
        """Suma el tamao del contenido de todos los archivos."""
        return self._tamano(self._navegar(ruta))

    def _tamano(self, nodo):
        """Cuenta recursivamente el tamao del contenido."""
        if nodo is None:
            return 0
        if isinstance(nodo, str):
            return len(nodo)                    # archivo: su largo
        return sum(self._tamano(v) for v in nodo.values())


if __name__ == "__main__":
    import os

    fs = SimpleFileSystem() if False else SistemaArchivosSimple()

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

    # Creacion implicita de padres
    fs.crear_archivo("/a/b/c/profundo.txt", "x")
    assert fs.leer_archivo("/a/b/c/profundo.txt") == "x"
    assert fs.es_directorio("/a/b/c") is True
    print("Creacion implicita de /a/b/c verificada")

    # Tamao total recursivo
    tam = fs.tamano_total("/documentos")
    assert tam == len("Hola, mundo!") + len("<imagen>") + 0, tam
    print(f"\nTamao total de /documentos: {tam} caracteres")

    # Casos base: raiz vacia
    vacio = SistemaArchivosSimple()
    assert vacio.listar_directorio("/") == []
    assert vacio.leer_archivo("/algo") is None
    assert vacio.tamano_total("/") == 0

    # Un solo archivo
    simple = SistemaArchivosSimple()
    simple.crear_archivo("/solo.txt", "contenido")
    assert simple.listar_directorio("/") == ["solo.txt"]
    assert simple.leer_archivo("/solo.txt") == "contenido"
    assert simple.tamano_total("/") == len("contenido")

    # Estructura profunda
    profundo = SistemaArchivosSimple()
    for i in range(10):
        profundo.crear_archivo(f"/n{i}/n{i+1}/archivo{i}.txt", "x" * i)
    assert profundo.leer_archivo("/n5/n6/archivo5.txt") == "xxxxx"

    # El listado solo muestra hijos DIRECTOS
    # /n4 solo contiene el subdirectorio n5; el archivo est un nivel
    # ms abajo, en /n4/n5.
    assert "n5" in profundo.listar_directorio("/n4")
    assert profundo.listar_directorio("/n4") == ["n5"], "solo el hijo directo"
    assert "archivo4.txt" in profundo.listar_directorio("/n4/n5")
    assert "n7" not in profundo.listar_directorio("/n5"), "no es nieto"

    # Un archivo dentro de un subdirectio NO aparece en la raiz
    assert "nota.txt" not in fs.listar_directorio("/")
    assert "documentos" in fs.listar_directorio("/")

    # Rutas equivalentes
    fs2 = SistemaArchivosSimple()
    fs2.crear_archivo("/x/y.txt", "dato")
    assert fs2.leer_archivo("//x//y.txt") == "dato", "barras dobles"
    assert fs2.leer_archivo("/x/y.txt/") == "dato", "barra final"
    print("\nRutas equivalentes normalizadas correctamente")

    print("\n Todas las pruebas pasaron")
