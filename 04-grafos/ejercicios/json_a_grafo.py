"""
Ejercicio 18: JSON a grafo
Dificultad: Intermedio

Convierte una representación JSON de un grafo a un objeto Grafo.
"""


import json


class Grafo:
    def __init__(self, dirigido=False):
        self.dirigido = dirigido
        self.adyacencia = {}

    def agregar_arista(self, u, v, peso=1):
        if u not in self.adyacencia:
            self.adyacencia[u] = []
        if v not in self.adyacencia:
            self.adyacencia[v] = []
        self.adyacencia[u].append((v, peso))
        if not self.dirigido:
            self.adyacencia[v].append((u, peso))

    def vecinos(self, v):
        return self.adyacencia.get(v, [])


def json_a_grafo(json_str):
    """Convierte una cadena JSON a un objeto Grafo."""
    datos = json.loads(json_str)
    grafo = Grafo(dirigido=datos.get("dirigido", False))
    for arista in datos.get("aristas", []):
        grafo.agregar_arista(arista["origen"], arista["destino"], arista.get("peso", 1))
    return grafo


if __name__ == "__main__":
    json_str = '''
    {
        "dirigido": false,
        "aristas": [
            {"origen": 0, "destino": 1, "peso": 4},
            {"origen": 0, "destino": 2, "peso": 1},
            {"origen": 1, "destino": 2, "peso": 2}
        ]
    }
    '''

    grafo = json_a_grafo(json_str)
    print(f"Grafo desde JSON: {grafo.adyacencia}")

    assert grafo.vecinos(0) == [(1, 4), (2, 1)]
    assert grafo.vecinos(1) == [(0, 4), (2, 2)]
    print("\n✓ Todas las pruebas pasaron")
