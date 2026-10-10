r"""
Ejercicio 13: Detectar ciclos en grafo DIRIGIDO
Dificultad: Avanzado

CONOCIMIENTO PREVIO NECESARIO
    - DFS (ejercicios 4 y 5).
    - Detección de ciclos en NO dirigido (ejercicio 6): la regla allí
      NO sirve aquí.
    - El concepto de arista de retroceso.

PROBLEMA
    Determinar si un grafo DIRIGIDO (dígrafo) contiene un ciclo.

¿POR QUÉ LA REGLA ANTERIOR NO FUNCIONA?
    En un grafo no dirigido basta con "un vecino visitado que no sea
    el padre". En un dígrafo eso es INCORRECTO.

    Contraejemplo:  A → B, C → B
    (A apunta a B, C apunta a B, no hay ciclo)

    Con la regla de no dirigido, al procesar B desde A, el vecino
    visitado C (que no es el padre de B) haría disparar un falso
    positivo. Pero C → B no crea ningún ciclo.

    La razón: en un no dirigido, si u y v se visitan mutuamente hay
    dos caminos. En un dirigido, la arista solo va en un sentido.

LA SOLUCIÓN: TRES ESTADOS (BLANCO, GRIS, NEGRO)
    Cada vértice tiene un estado durante el recorrido:

        BLANCO: no visitado (aún no se entra).
        GRIS:   EN PROCESO (está en la pila de recursión actual).
        NEGRO:  TERMINADO (se exploraron todos sus descendientes).

    La regla: si durante el DFS encontramos un vecino GRIS, hay un
    ciclo. Un vértice GRIS es un ancestro en el recorrido actual, así
    que volver a él cierra un ciclo (arista de retroceso).

    Los vecinos NEGROS son seguros: ya se exploraron por completo y
    no forman ciclo con nadie.

TRAZA sobre: A → B → C → A  (ciclo)

    dfs(A, BLANCO): estado[A] = GRIS
       vecino B: BLANCO → dfs(B)
          estado[B] = GRIS
          vecino C: BLANCO → dfs(C)
             estado[C] = GRIS
             vecino A: ¡GRIS! → CICLO DETECTADO
             (A está en la pila de recursión: A → B → C, y C apunta a A)

    Contraste con A → B, C → B (sin ciclo):
    dfs(A): estado[A]=GRIS
       vecino B: BLANCO → dfs(B)
          estado[B]=GRIS, sin vecinos salientes
          estado[B]=NEGRO, retorna
       estado[A]=NEGRO
    dfs(C): estado[C]=GRIS
       vecino B: estado[B]=NEGRO → NO es ciclo
       estado[C]=NEGRO

    Correcto: sin ciclo. La regla de no dirigido habría fallado aquí.

IMPLEMENTACIÓN

```python
BLANCO, GRIS, NEGRO = 0, 1, 2

def tiene_ciclo_dirigido(grafo):
    estado = {v: BLANCO for v in grafo.vertices}

    def dfs(v):
        estado[v] = GRIS                      # entra en proceso
        for vecino, _ in grafo.vecinos(v):
            if estado[vecino] == GRIS:
                return True                   # arista de retroceso
            if estado[vecino] == BLANCO:
                if dfs(vecino):
                    return True
        estado[v] = NEGRO                     # termina
        return False

    for v in grafo.vertices:                   # puede ser inconexo
        if estado[v] == BLANCO:
            if dfs(v):
                return True
    return False
```

DEMOSTRACIÓN DE CORRECCIÓN
    * Si reporta ciclo: se encontró un vecino GRIS, es decir, un
      ancestro en la pila de recursión actual. El camino desde ese
      ancestro hasta v, más la arista (v, ancestro), forma un ciclo.
    * Si hay un ciclo C: sea v el primer vértice de C que el DFS
      visita. Todos los demás vértices de C son descendientes de v y
      se visitan antes de que v termine (porque el ciclo los conecta
      de vuelta a v). Cuando se procese la arista que cierra el ciclo,
      v sigue GRIS (no ha terminado), así que se detecta. ∎

COMPLEJIDAD
    Tiempo: O(V + E). Cada vértice se visita una vez; cada arista se
    examina una vez desde su origen.
    Espacio: O(V) de pila de recursión en el peor caso.

APLICACIONES
    - Detectar deadlocks: un ciclo en el grafo de espera.
    - Dependencias circulares en compilación o paquetes.
    - Validar que un grafo de tareas es un DAG (para poder hacer
      ordenamiento topológico).

RELACIÓN CON OTROS TEMAS
    - El ordenamiento topológico (teoria.md §5.4) solo es posible en
      DAGs, así que esta verificación es su precondición.
    - La pila GRIS es exactamente la pila de llamadas del sistema
      durante la recursión.
"""


BLANCO, GRIS, NEGRO = 0, 1, 2


class Grafo:
    """Grafo DIRIGIDO con lista de adyacencia."""

    def __init__(self):
        self.adyacencia = {}

    def agregar_arista(self, u, v):
        self.adyacencia.setdefault(u, [])
        self.adyacencia.setdefault(v, [])
        self.adyacencia[u].append((v, 1))      # solo un sentido

    def vecinos(self, v):
        return self.adyacencia.get(v, [])

    @property
    def vertices(self):
        return list(self.adyacencia.keys())


def tiene_ciclo_dirigido(grafo):
    """Detecta ciclos en un DÍGRAFO por DFS con 3 estados. O(V+E)."""
    estado = {v: BLANCO for v in grafo.vertices}

    def dfs(v):
        estado[v] = GRIS                        # en proceso

        for vecino, _ in grafo.vecinos(v):
            if estado[vecino] == GRIS:
                return True                     # arista de retroceso
            if estado[vecino] == BLANCO:
                if dfs(vecino):
                    return True

        estado[v] = NEGRO                       # terminado
        return False

    for vertice in grafo.vertices:
        if estado[vertice] == BLANCO:
            if dfs(vertice):
                return True

    return False


def tiene_ciclo_dirigido_iterativo(grafo):
    """Versión iterativa del mismo algoritmo (evita recursión profunda)."""
    BLANCO_, GRIS_, NEGRO_ = 0, 1, 2
    estado = {v: BLANCO_ for v in grafo.vertices}

    for inicio in grafo.vertices:
        if estado[inicio] != BLANCO_:
            continue
        pila = [(inicio, iter(grafo.vecinos(inicio)))]
        estado[inicio] = GRIS_

        while pila:
            vertice, iterador = pila[-1]
            avanzar = False

            for vecino, _ in iterador:
                if estado[vecino] == GRIS_:
                    return True                 # ciclo
                if estado[vecino] == BLANCO_:
                    estado[vecino] = GRIS_
                    pila.append((vecino, iter(grafo.vecinos(vecino))))
                    avanzar = True
                    break

            if not avanzar:
                estado[vertice] = NEGRO_
                pila.pop()

    return False


if __name__ == "__main__":
    # Ciclo simple: A → B → C → A
    g1 = Grafo()
    g1.agregar_arista(0, 1)
    g1.agregar_arista(1, 2)
    g1.agregar_arista(2, 0)
    print(f"A→B→C→A tiene ciclo: {tiene_ciclo_dirigido(g1)}")
    assert tiene_ciclo_dirigido(g1) is True
    assert tiene_ciclo_dirigido_iterativo(g1) is True

    # DAG: sin ciclo
    g2 = Grafo()
    g2.agregar_arista(0, 1)
    g2.agregar_arista(0, 2)
    g2.agregar_arista(1, 3)
    g2.agregar_arista(2, 3)
    print(f"DAG (0→1,0→2,1→3,2→3) tiene ciclo: {tiene_ciclo_dirigido(g2)}")
    assert tiene_ciclo_dirigido(g2) is False

    # EL CASO QUE ROMPE LA REGLA DE NO DIRIGIDO
    # A → B y C → B: sin ciclo, pero la regla de "padre" fallaría
    g3 = Grafo()
    g3.agregar_arista(0, 1)                       # A → B
    g3.agregar_arista(2, 1)                       # C → B
    print(f"\nA→B, C→B tiene ciclo: {tiene_ciclo_dirigido(g3)}")
    assert tiene_ciclo_dirigido(g3) is False, "¡sin ciclo!"

    # Demostrar que la regla de NO dirigido daría un falso positivo
    def regla_no_dirigida(grafo):
        visitados = set()
        def dfs(v, padre):
            visitados.add(v)
            for vecino, _ in grafo.vecinos(v):
                if vecino not in visitados:
                    if dfs(vecino, v):
                        return True
                elif vecino != padre:
                    return True
            return False
        for v in grafo.vertices:
            if v not in visitados:
                if dfs(v, None):
                    return True
        return False

    print(f"  Regla de no dirigido diría: {regla_no_dirigida(g3)} (¡incorrecto!)")
    assert regla_no_dirigida(g3) is True, "la regla de no dirigido FALLA aquí"

    # Self-loop: un vértice que apunta a sí mismo
    g4 = Grafo()
    g4.adyacencia[0] = [(0, 1)]
    print(f"Self-loop (0→0) tiene ciclo: {tiene_ciclo_dirigido(g4)}")
    assert tiene_ciclo_dirigido(g4) is True, "un self-loop es un ciclo"

    # Casos base
    vacio = Grafo()
    assert tiene_ciclo_dirigido(vacio) is False

    aislado = Grafo()
    aislado.adyacencia = {5: []}
    assert tiene_ciclo_dirigido(aislado) is False

    # Ciclo en una componente inconexa
    mixto = Grafo()
    mixto.agregar_arista(0, 1)                    # DAG
    mixto.agregar_arista(2, 3)                    # ciclo
    mixto.agregar_arista(3, 2)
    print(f"\nInconexo con ciclo en una parte: {tiene_ciclo_dirigido(mixto)}")
    assert tiene_ciclo_dirigido(mixto) is True

    # Cadena larga sin ciclo (DAG lineal)
    cadena = Grafo()
    for i in range(200):
        cadena.agregar_arista(i, i + 1)
    print(f"Cadena de 200 vértices, ciclo: {tiene_ciclo_dirigido(cadena)}")
    assert tiene_ciclo_dirigido(cadena) is False

    # Cadena larga CON ciclo al final
    cadena_ciclo = Grafo()
    for i in range(200):
        cadena_ciclo.agregar_arista(i, i + 1)
    cadena_ciclo.agregar_arista(200, 0)            # cierra el ciclo
    assert tiene_ciclo_dirigido(cadena_ciclo) is True, "ciclo al final"

    # Ambas implementaciones coinciden
    for g in [g1, g2, g3, g4, mixto, cadena, cadena_ciclo]:
        assert tiene_ciclo_dirigido(g) == tiene_ciclo_dirigido_iterativo(g)

    print("\n✓ Todas las pruebas pasaron")
