"""
Ejercicio 9: Merge Sort con lista enlazada
Dificultad: Experto

Implementa Merge Sort para una lista enlazada simple.
"""

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, valor):
        nuevo = Nodo(valor)
        if not self.cabeza:
            self.cabeza = nuevo
            return
        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nuevo

    def a_lista(self):
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append(actual.valor)
            actual = actual.siguiente
        return resultado

    @staticmethod
    def desde_lista(lista):
        le = ListaEnlazada()
        for v in lista:
            le.agregar(v)
        return le


def merge_sort_lista(cabeza):
    """Ordena una lista enlazada usando Merge Sort."""
    if not cabeza or not cabeza.siguiente:
        return cabeza
    medio = encontrar_medio(cabeza)
    siguiente_a_medio = medio.siguiente
    medio.siguiente = None
    izquierda = merge_sort_lista(cabeza)
    derecha = merge_sort_lista(siguiente_a_medio)
    return merge_listas(izquierda, derecha)


def encontrar_medio(cabeza):
    """Encuentra el nodo medio usando punteros rápido y lento."""
    if not cabeza:
        return cabeza
    lento = cabeza
    rapido = cabeza.siguiente
    while rapido and rapido.siguiente:
        lento = lento.siguiente
        rapido = rapido.siguiente.siguiente
    return lento


def merge_listas(a, b):
    """Mezcla dos listas enlazadas ordenadas."""
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


if __name__ == "__main__":
    lista = ListaEnlazada.desde_lista([4, 2, 1, 3])
    print(f"Original: {lista.a_lista()}")
    lista.cabeza = merge_sort_lista(lista.cabeza)
    print(f"Ordenado: {lista.a_lista()}")

    assert lista.a_lista() == [1, 2, 3, 4]
    print("\n✓ Todas las pruebas pasaron")
