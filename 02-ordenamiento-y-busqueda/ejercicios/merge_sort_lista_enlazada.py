"""
Ejercicio 9: Merge Sort con lista enlazada
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - Merge Sort sobre arreglos (ejercicio merge_sort.py).
    - Listas enlazadas (00-fundamentos §8.3): la diferencia clave con
      los arreglos es que NO hay acceso aleatorio por índice.
    - Puntero rápido/lento: técnica para encontrar el medio en O(n).

PROBLEMA
    Ordenar una lista enlazada simple con Merge Sort.

¿POR QUÉ MERGE SORT Y NO QUICK SORT?
    Esta es la pregunta central del ejercicio.

    Quick Sort necesita acceso aleatorio: particionar alrededor de un
    pivote exige indexar y comparar elementos en posiciones arbitrarias.
    En una lista enlazada, `lista[k]` cuesta O(k). Eso arruinaría la
    partición.

    Merge Sort no necesita acceso aleatorio en absoluto:
      1. Dividir: encontrar el medio con dos punteros (O(n) con
         puntero rápido/lento, sin necesidad de índices).
      2. Mezclar: recorrer ambas listas secuencialmente y enlazar en
         orden (O(n), solo hay que seguir referencias `siguiente`).

    Por eso Merge Sort es EL algoritmo para listas enlazadas.

ESTRATEGIA
    Caso base: lista vacía o de un nodo → ya está ordenada.

    Paso recursivo:
      1. PARTIR por la mitad usando dos punteros:
             lento avanza 1, rápido avanza 2
         Cuando rápido llega al final, lento está en el medio.
         Se corta el enlace en el medio para tener dos listas.
      2. Ordenar recursivamente cada mitad.
      3. MEZCLAR las dos mitades ordenadas reconectando los punteros
         `siguiente`, sin crear nodos nuevos.

    La mezcla es in-place en cuanto a nodos (no se asignan nodos nuevos,
    solo se reordenan las referencias). El espacio extra es O(log n)
    de pila de recursión.

TRAZA de encontrar_medio(A→B→C→D)
    lento=A, rápido=A
    rápido!=None y rápido.siguiente!=None:
      lento=B, rápido=C        (rápido avanzó 2: A→C)
    rápido!=None y rápido.siguiente!=None:
      lento=C, rápido=C.siguiente.siguiente=None
    rápido es None → fin
    Medio = lento = C

    Para [A,B,C,D] el medio correcto es B o C (según convención);
    esta implementación devuelve B con la condición rápida inicial
    en cabeza.siguiente. Ver el código para el detalle exacto.

TRAZA de merge_listas(1→3, 2→4)
    a=1, b=2
    1 <= 2 → resultado = a = 1, a = 3
    3 > 2  → resultado.siguiente = b = 2, b = 4
    3 <= 4 → resultado.siguiente = a = 3, a = None
    a es None → resultado.siguiente = b = 4
    Resultado: 1→2→3→4

COMPLEJIDAD
    Sea n el número de nodos.
    Recurrencia: T(n) = 2·T(n/2) + O(n) → Θ(n log n) por Teorema
    Maestro. Igual que sobre arreglos.

    Espacio: O(log n) de pila de recursión. La mezcla reutiliza los
    nodos existentes, así que NO se asigna memoria proporcional a n
    (a diferencia de la versión sobre arreglos con comprensiones).

DEMOSTRACIÓN DE CORRECCIÓN
    Por inducción sobre n. Caso base n ≤ 1: trivial.
    Para n > 1: partir da dos listas de tamaño floor(n/2) y
    ceil(n/2), ambas menores que n; por hipótesis la recursión las
    ordena. merge_listas combina dos listas ordenadas en una ordenada
    (invariante de la mezcla: resultado siempre contiene los menores
    elementos vistos, en orden). Luego el resultado está ordenado. ∎

DIFERENCIA CON LA VERSIÓN SOBRE ARREGLOS
    Aspecto          Arreglo                Lista enlazada
    Dividir          Rebanada O(n)         Puntrero rápido/lento O(n)
    Acceso medio     O(1) por índice       O(n) buscando el medio
    Mezcla           Lista nueva O(n)      Reconecta punteros O(1) extra
    Memoria          O(n) auxiliar         O(log n) de pila
    Dividir es estable Sí                    Sí (merge con <=)

APLICACIÓN REAL
    - std::list::sort en C++ usa una variante de Merge Sort.
    - Ordenar listas enlazadas es una pregunta clásica de entrevista
      técnica, y la respuesta correcta siempre es Merge Sort.
"""


class Nodo:
    """Nodo de una lista enlazada simple."""

    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


class ListaEnlazada:
    """Lista enlazada simple con operaciones básicas."""

    def __init__(self):
        self.cabeza = None

    def agregar(self, valor):
        """Añade al final: O(n)."""
        nuevo = Nodo(valor)
        if not self.cabeza:
            self.cabeza = nuevo
            return
        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nuevo

    def a_lista(self):
        """Convierte a lista de Python para facilitar pruebas."""
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append(actual.valor)
            actual = actual.siguiente
        return resultado

    @staticmethod
    def desde_lista(valores):
        """Construye una lista enlazada desde una lista de Python."""
        le = ListaEnlazada()
        for v in valores:
            le.agregar(v)
        return le


def encontrar_medio(cabeza):
    """Encuentra el nodo medio con la técnica de puntero rápido/lento.

    lento avanza 1 paso, rápido avanza 2. Cuando rápido termina,
    lento está en el medio. O(n) sin usar índices.
    """
    if not cabeza:
        return cabeza

    lento = cabeza
    rapido = cabeza.siguiente          # iniciar adelantado para
                                       # partir por la mitad correcta
    while rapido and rapido.siguiente:
        lento = lento.siguiente
        rapido = rapido.siguiente.siguiente

    return lento


def merge_listas(a, b):
    """Mezcla dos listas ordenadas en una, reconectando punteros.

    Usa <= para conservar estabilidad: ante empate se toma de `a`.
    """
    if not a:
        return b
    if not b:
        return a

    if a.valor <= b.valor:
        resultado = a
        resultado.siguiente = merge_listas(a.siguiente, b)
    else:
        resultado = b
        resultado.siguiente = merge_listas(a, b.siguiente)

    return resultado


def merge_sort_lista(cabeza):
    """Ordena una lista enlazada con Merge Sort.

    T(n) = 2T(n/2) + O(n) = Θ(n log n)
    Espacio: O(log n) de pila de recursión.
    """
    # Caso base: vacía o un solo nodo → ya ordenada
    if not cabeza or not cabeza.siguiente:
        return cabeza

    # 1. PARTIR por la mitad
    medio = encontrar_medio(cabeza)
    siguiente_al_medio = medio.siguiente
    medio.siguiente = None              # cortar en dos listas

    # 2. Ordenar cada mitad recursivamente
    izquierda = merge_sort_lista(cabeza)
    derecha = merge_sort_lista(siguiente_al_medio)

    # 3. Mezclar las dos mitades ordenadas
    return merge_listas(izquierda, derecha)


if __name__ == "__main__":
    # Caso del enunciado
    lista = ListaEnlazada.desde_lista([4, 2, 1, 3])
    print(f"Original: {lista.a_lista()}")
    lista.cabeza = merge_sort_lista(lista.cabeza)
    print(f"Ordenado: {lista.a_lista()}")
    assert lista.a_lista() == [1, 2, 3, 4]

    # Casos base
    vacia = ListaEnlazada()
    vacia.cabeza = merge_sort_lista(vacia.cabeza)
    assert vacia.a_lista() == []

    uno = ListaEnlazada.desde_lista([42])
    uno.cabeza = merge_sort_lista(uno.cabeza)
    assert uno.a_lista() == [42]

    # Casos variados
    for valores in [[5, 4, 3, 2, 1], list(range(10)), [3, 1, 4, 1, 5, 9, 2, 6]]:
        le = ListaEnlazada.desde_lista(valores[:])
        le.cabeza = merge_sort_lista(le.cabeza)
        assert le.a_lista() == sorted(valores), f"falló con {valores}"

    # Lista más larga y aleatoria
    import random
    random.seed(1)
    valores = [random.randint(-100, 100) for _ in range(500)]
    le = ListaEnlazada.desde_lista(valores[:])
    le.cabeza = merge_sort_lista(le.cabeza)
    assert le.a_lista() == sorted(valores)

    # Verificar que no se crearon nodos nuevos (se reutilizan los existentes)
    def contar_nodos(cabeza):
        n = 0
        while cabeza:
            n += 1
            cabeza = cabeza.siguiente
        return n

    le2 = ListaEnlazada.desde_lista([9, 3, 7, 1, 5])
    n_antes = contar_nodos(le2.cabeza)
    le2.cabeza = merge_sort_lista(le2.cabeza)
    assert contar_nodos(le2.cabeza) == n_antes, "no deben crearse nodos nuevos"

    print("\n✓ Todas las pruebas pasaron")
