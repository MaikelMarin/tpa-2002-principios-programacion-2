"""
Ejercicio 4: Suma recursiva de lista
Dificultad: Básico

Patrón "cabeza + cola":
    suma(lista) = lista[0] + suma(lista[1:])
    suma([]) = 0
"""

def suma_lista(lista):
    """Suma todos los elementos de una lista de forma recursiva."""
    if not lista:
        return 0
    return lista[0] + suma_lista(lista[1:])


def suma_lista_indice(lista, indice=0):
    """Versión alternativa usando índice (evita crear sublistas)."""
    if indice >= len(lista):
        return 0
    return lista[indice] + suma_lista_indice(lista, indice + 1)


if __name__ == "__main__":
    print(f"suma_lista([1,2,3,4,5]) = {suma_lista([1, 2, 3, 4, 5])}")
    print(f"suma_lista([]) = {suma_lista([])}")
    print(f"suma_lista([10]) = {suma_lista([10])}")

    assert suma_lista([1, 2, 3, 4, 5]) == 15
    assert suma_lista([]) == 0
    assert suma_lista([10]) == 10
    assert suma_lista_indice([1, 2, 3, 4, 5]) == 15
    print("\n✓ Todas las pruebas pasaron")
