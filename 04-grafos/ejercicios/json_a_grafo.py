r"""
Ejercicio 18: JSON a grafo
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Lista de adyacencia (ejercicio 1).
    - Módulo `json` de Python.
    - Estructuras anidadas (00-fundamentos §10.1).

PROBLEMA
    Leer una descripción de grafo en formato JSON y construir el
    objeto Grafo correspondiente.

FONDO MATEMÁTICO
    JSON (JavaScript Object Notation) es el formato estándar de
    intercambio de datos en la web. Un grafo se puede describir con
    un objeto que liste los vértices y las aristas:

```json
{
    "dirigido": false,
    "vertices": ["A", "B", "C"],
    "aristas": [
        {"origen": "A", "destino": "B", "peso": 4},
        {"origen": "B", "destino": "C", "peso": 2}
    ]
}
```

    La lista de aristas implícita las adyacencias: construir la lista
    de adyacencia es recorrer las aristas y añadir cada una.

ESTRATEGIA
    1. Parsear el JSON con json.loads().
    2. Leer si es dirigido.
    3. Crear el grafo con esa configuración.
    4. Añadir cada arista del array.

    Los vértices aislados (sin aristas) deben declararse en el array
    "vertices", porque ninguna arista los mencionaría.

TRAZA de json_a_grafo
    json.loads(...) → dict
    dirigido = False
    Grafo(dirigido=False)
    Para cada arista ["A","B",4] → grafo.agregar_arista("A", "B", 4)

    Resultado: grafo.vecinos("A") = [("B", 4)]

COMPLEJIDAD
    Parsear JSON: O(n) donde n es el tamaño del texto.
    Construir el grafo: O(V + E). Cada arista se procesa una vez.

DETALLE DE DISEÑO: ¿POR QUÉ LISTA DE ARISTAS Y NO ADYACENCIAS?
    Porque es más fácil de escribir a mano y de validar. La lista de
    adyacencia es más conveniente para ALGORITMOS (recorrer vecinos),
    pero para INTERCAMBIO de datos la lista de aristas es más limpia.

    Es el mismo trade-off que matrices vs listas (§3.3).

APLICACIONES
    - Cargar grafos desde archivos de configuración.
    - Intercambio entre sistemas (APIs).
    - Persistencia de grafos pequeños y medianos.

RELACIÓN CON OTROS TEMAS
    - El tema 05 cubre escritura/lectura de archivos.
    - El tema 06 (grandes datos): para grafos enormes, JSON no escala
      bien; se usan formatos binarios o bases de datos de grafos.
"""


import json


class Grafo:
    """Grafo con lista de adyacencia."""

    def __init__(self, dirigido=False):
        self.dirigido = dirigido
        self.adyacencia = {}

    def agregar_vertice(self, v):
        if v not in self.adyacencia:
            self.adyacencia[v] = []

    def agregar_arista(self, u, v, peso=1):
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        self.adyacencia[u].append((v, peso))
        if not self.dirigido:
            self.adyacencia[v].append((u, peso))

    def vecinos(self, v):
        return self.adyacencia.get(v, [])

    @property
    def vertices(self):
        return list(self.adyacencia.keys())


def json_a_grafo(texto_json):
    """Construye un Grafo desde una cadena JSON.

    Formato esperado:
      {"dirigido": bool, "vertices": [...], "aristas": [{"origen":..,
       "destino":.., "peso":..}]}
    """
    datos = json.loads(texto_json)

    grafo = Grafo(dirigido=datos.get("dirigido", False))

    # Registrar vértices aislados (que ninguna arista menciona)
    for vertice in datos.get("vertices", []):
        grafo.agregar_vertice(vertice)

    # Añadir las aristas
    for arista in datos.get("aristas", []):
        grafo.agregar_arista(
            arista["origen"],
            arista["destino"],
            arista.get("peso", 1)
        )

    return grafo


if __name__ == "__main__":
    json_str = """
    {
        "dirigido": false,
        "vertices": ["A", "B", "C", "D"],
        "aristas": [
            {"origen": "A", "destino": "B", "peso": 4},
            {"origen": "B", "destino": "C", "peso": 2},
            {"origen": "A", "destino": "C", "peso": 1}
        ]
    }
    """

    grafo = json_a_grafo(json_str)
    print(f"Vértices: {grafo.vertices}")
    print(f"Dirigido: {grafo.dirigido}")
    print(f"Vecinos de A: {grafo.vecinos('A')}")

    # Los vértices del JSON están todos presentes
    assert set(grafo.vertices) == {"A", "B", "C", "D"}

    # D está aislado (declarado pero sin aristas): aparece sin vecinos
    assert grafo.vecinos("D") == []
    assert "D" in grafo.adyacencia, "los vértices declarados deben existir"

    # Las aristas se registraron con su peso
    assert grafo.vecinos("A") == [("B", 4), ("C", 1)]
    assert ("C", 1) in grafo.vecinos("A"), "el peso se conserva"

    # No dirigido: la arista aparece en ambos lados
    assert grafo.vecinos("B") == [("A", 4), ("C", 2)]
    assert ("A", 4) in grafo.vecinos("B")

    # Caso base: JSON vacío
    g_vacio = json_a_grafo('{"dirigido": false, "vertices": [], "aristas": []}')
    assert g_vacio.vertices == []
    assert g_vacio.adyacencia == {}

    # Sin el campo "dirigido": por defecto no dirigido
    g_sin_campo = json_a_grafo('{"vertices": ["X"], "aristas": []}')
    assert g_sin_campo.dirigido is False, "valor por defecto"

    # Grafo DIRIGIDO desde JSON
    json_dir = """
    {
        "dirigido": true,
        "vertices": ["S", "T"],
        "aristas": [
            {"origen": "S", "destino": "T", "peso": 3}
        ]
    }
    """
    g_dir = json_a_grafo(json_dir)
    assert g_dir.dirigido is True
    assert g_dir.vecinos("S") == [("T", 3)]
    assert g_dir.vecinos("T") == [], "dirigido: T no apunta a S"

    # Sin el campo "peso": por defecto 1
    json_sin_peso = """
    {
        "vertices": ["P", "Q"],
        "aristas": [{"origen": "P", "destino": "Q"}]
    }
    """
    g_sp = json_a_grafo(json_sin_peso)
    assert g_sp.vecinos("P") == [("Q", 1)], "peso por defecto 1"

    # JSON malformado: json.loads lanza excepción
    try:
        json_a_grafo("{no es válido}")
        raise AssertionError("debía lanzar error de parseo")
    except json.JSONDecodeError:
        print("\nJSON malformado detectado correctamente")

    # Grafo más grande generado programáticamente
    import random
    random.seed(211)
    n = 300
    vertices = [f"V{i}" for i in range(n)]
    aristas = [{"origen": f"V{random.randrange(n)}",
                "destino": f"V{random.randrange(n)}",
                "peso": random.randint(1, 50)}
               for _ in range(600)]
    grande = json_a_grafo(json.dumps({"vertices": vertices, "aristas": aristas}))
    assert len(grande.vertices) == n, "todos los vértices declarados"

    # Round-trip: serializar y volver a cargar da el mismo grafo
    def grafo_a_json(g):
        aristas_out = []
        vistos = set()
        for u in g.vertices:
            for v, peso in g.vecinos(u):
                par = tuple(sorted((str(u), str(v))))
                if par not in vistos:
                    vistos.add(par)
                    aristas_out.append({"origen": u, "destino": v, "peso": peso})
        return json.dumps({"dirigido": g.dirigido,
                           "vertices": g.vertices,
                           "aristas": aristas_out})

    g2 = json_a_grafo(grafo_a_json(grafo))
    assert set(g2.vertices) == set(grafo.vertices)
    # Mismo número de aristas (contando pares únicos)
    def num_aristas_unicas(g):
        pares = set()
        for u in g.vertices:
            for v, _ in g.vecinos(u):
                pares.add(tuple(sorted((str(u), str(v)))))
        return len(pares)
    assert num_aristas_unicas(g2) == num_aristas_unicas(grafo)

    print(f"Round-trip con {len(grafo.vertices)} vértices verificado")

    print("\n✓ Todas las pruebas pasaron")
