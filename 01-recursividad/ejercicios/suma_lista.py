"""
Ejercicio 4: Suma recursiva de lista
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Patrón cabeza + cola: la forma canónica de recorrer una lista
      recursivamente.
    - Inducción (00-fundamentos §3): la corrección se demuestra por
      inducción sobre la longitud.

PROBLEMA
    Sumar todos los elementos de una lista de números.

FONDO MATEMÁTICO
    La suma sobre una lista se define inductivamente:
        suma([])      = 0                      (elemento neutro)
        suma(x :: L) = x + suma(L)             (cabeza + suma de la cola)

    Esta definición es exactamente recursiva, y es la que se traduce
    al código. El 0 es el elemento neutro de la suma: sumarlo no
    cambia el resultado, por eso funciona como caso base.

ESTRATEGIA
    Dos versiones con el mismo resultado pero distinto coste:

    Versión A (con rebanadas): `lista[0] + suma(lista[1:])`.
        Clara y directa, pero `lista[1:]` CREA UNA COPIA de la cola:
        O(n) por llamada, O(n^2) en total. Inaceptable para listas
        grandes.

    Versión B (con índice): pasar la posición actual como parámetro.
        No copia nada: O(n) total. Es la que se usaría en la práctica.

    La versión A se conserva porque es la forma más pura del patrón y
    porque aparece en los libros de programación funcional.

TRAZA DE suma([1, 2, 3])
    Versión A (rebano):
      s([1,2,3]) = 1 + s([2,3])
      s([2,3])   = 2 + s([3])
      s([3])     = 3 + s([])
      s([])      = 0            ← caso base
      Al desapilar: 3+0=3, 2+3=5, 1+5=6

    Versión B (índice) para la misma lista:
      Llamada        i   ¿Base?   Cálculo
      suma_indice(L,0) 0 No      1 + suma_indice(L,1)
      suma_indice(L,1) 1 No      2 + suma_indice(L,2)
      suma_indice(L,2) 2 No      3 + suma_indice(L,3)
      suma_indice(L,3) 3 Sí      retorna 0

DEMOSTRACIÓN DE CORRECCIÓN (inducción sobre la longitud)
    Caso base: lista vacía. La suma es 0 y la función retorna 0.

    Hipótesis: suma(cola) devuelve la suma de la cola.

    Paso: suma(lista) = lista[0] + suma(cola) = lista[0] + (suma de
    la cola), que es la suma de todos los elementos. ∎

COMPLEJIDAD
    Versión A: T(n) = T(n-1) + O(n) = O(n^2)  ← la copia domina
               Espacio: O(n) de pila + O(n) por las copias
    Versión B: T(n) = T(n-1) + O(1) = O(n)     ← correcta
               Espacio: O(n) de pila

    LECCIÓN: la recursión en sí es O(n); el coste oculto estaba en
    `lista[1:]`. Al analizar recursión sobre listas siempre hay que
    preguntarse si la operación de "obtener la cola" es O(1) o O(n).

CASOS LÍMITE
    - Lista vacía: retorna 0. El 0 es el neutro, no un error.
    - Lista de un elemento: retorna ese elemento.
    - Lista con negativos: funciona igual (la suma es cerrada en Z).

RELACIÓN CON OTROS TEMAS
    Este patrón es idéntico al recorrido preorden de un árbol con un
    solo hijo (tema 03). Si se entiende aquí, los árboles ya están
    medio entendidos.
"""


def suma_lista(lista):
    """Suma recursiva usando rebanadas: O(n^2) por las copias.

    Forma más pura del patrón cabeza + cola, pero ineficiente.
    """
    if not lista:                    # lista vacía = caso base
        return 0
    return lista[0] + suma_lista(lista[1:])   # cabeza + suma de la cola


def suma_lista_indice(lista, indice=0):
    """Suma recursiva con índice: O(n). Sin copias de la lista."""
    if indice >= len(lista):         # se recorrió todo
        return 0
    return lista[indice] + suma_lista_indice(lista, indice + 1)


def contar_lista(lista, indice=0):
    """Cuenta elementos con el mismo patrón: refuerza la estructura."""
    if indice >= len(lista):
        return 0
    return 1 + contar_lista(lista, indice + 1)


if __name__ == "__main__":
    print("Suma recursiva (versión con rebanadas):")
    print(f"  suma([1,2,3,4,5]) = {suma_lista([1, 2, 3, 4, 5])}")
    print(f"  suma([])          = {suma_lista([])}")
    print(f"  suma([10])        = {suma_lista([10])}")

    print("\nSuma recursiva (versión con índice):")
    print(f"  suma_indice([1,2,3,4,5]) = {suma_lista_indice([1, 2, 3, 4, 5])}")

    print(f"\nContar([1,2,3,4,5]) = {contar_lista([1, 2, 3, 4, 5])}")

    # Caso base
    assert suma_lista([]) == 0, "la suma vacía debe ser 0"
    assert suma_lista_indice([]) == 0

    # Caso de un elemento
    assert suma_lista([10]) == 10

    # Caso general
    assert suma_lista([1, 2, 3, 4, 5]) == 15
    assert suma_lista_indice([1, 2, 3, 4, 5]) == 15

    # Con negativos: la suma es cerrada en los enteros
    assert suma_lista([5, -3, -2]) == 0

    # Ambas versiones coinciden siempre
    for lista in [[], [7], [1, -1, 2, -2], [100, 200, 300]]:
        assert suma_lista(lista) == suma_lista_indice(lista), f"discrepancia en {lista}"

    # Contar es el mismo patrón
    assert contar_lista([1, 2, 3, 4, 5]) == 5
    assert contar_lista([]) == 0

    print("\n✓ Todas las pruebas pasaron")
