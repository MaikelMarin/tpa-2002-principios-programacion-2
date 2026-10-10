"""
Ejercicio 5: Suma recursiva de lista anidada
Dificultad: Intermedio

Suma todos los elementos de una lista que puede contener otras listas.

Ejemplo:
    [1, [2, 3], [4, [5, 6]]] → 21
"""

def suma_anidada(lista):
    """Suma recursivamente todos los elementos de una lista anidada."""
    total = 0
    for elemento in lista:
        if isinstance(elemento, list):
            total += suma_anidada(elemento)
        else:
            total += elemento
    return total


def aplanar(lista):
    """Convierte una lista anidada en una lista plana."""
    resultado = []
    for elemento in lista:
        if isinstance(elemento, list):
            resultado.extend(aplanar(elemento))
        else:
            resultado.append(elemento)
    return resultado


if __name__ == "__main__":
    lista = [1, [2, 3], [4, [5, 6]]]
    print(f"Lista original: {lista}")
    print(f"Suma: {suma_anidada(lista)}")
    print(f"Aplanada: {aplanar(lista)}")

    assert suma_anidada([1, [2, 3], [4, [5, 6]]]) == 21
    assert suma_anidada([]) == 0
    assert suma_anidada([1, 2, 3]) == 6
    assert suma_anidada([[1, 2], [3, 4]]) == 10
    assert aplanar([1, [2, 3], [4, [5, 6]]]) == [1, 2, 3, 4, 5, 6]
    print("\n✓ Todas las pruebas pasaron")
