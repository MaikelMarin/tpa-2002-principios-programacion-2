"""
Ejercicio 5: Lista anidada recursiva
Dificultad: Intermedio

CONOCIMIENTO PREVIO NECESARIO
    - Inducción estructural (00-fundamentos §3.6): la corrección se
      demuestra sobre la estructura, no sobre un entero.
    - Patrón cabeza + cola, extendido a profundidad arbitraria.

PROBLEMA
    Sumar todos los números de una lista que puede contener otras
    listas, a profundidad arbitraria.

        [1, [2, 3], [4, [5, 6]]]   →   21

FONDO MATEMÁTICO
    La estructura se define recursivamente: una lista anidada es, o
    bien un número, o bien una lista de listas anidadas. Cuando la
    estructura es recursiva, el algoritmo debe serlo.

    Definición inductiva de la suma:
        suma(x)      = x                    si x es un número
        suma([])     = 0                    si x es la lista vacía
        suma(x :: L) = suma(x) + suma(L)    en general

ESTRATEGIA
    Recorrer cada elemento de la lista:
      - Si es una lista: el subproblema es del MISMO tipo → recursión.
      - Si es un número: sumarlo directamente (caso base).

    El caso base no es "lista vacía" sino "elemento que no es lista".
    Son dos casos base distintos, y eso es normal en recursión sobre
    estructuras mixtas.

TRAZA DE suma_anidada([1, [2, 3]])
    Llamada                 Elemento   ¿Lista?   Acción
    sn([1,[2,3]])           1          No        total = 1
    sn([1,[2,3]])           [2,3]      Sí        → sn([2,3])
    ↳ sn([2,3])             2          No        total = 2
    ↳ sn([2,3])             3          No        total = 5 → retorna 5
    sn([1,[2,3]])           —          —         1 + 5 = 6

DEMOSTRACIÓN DE CORRECCIÓN (inducción estructural)
    Caso base 1: x es un número. Se retorna x. Correcto.
    Caso base 2: x es la lista vacía. Se retorna 0. Correcto.

    Hipótesis: para toda sublista propia L de x, suma_anidada(L)
    devuelve la suma de todos los números en L.

    Paso: para x = [e1, e2, ..., ek], la función procesa cada ei. Si
    ei es número, se suma directamente (correcto). Si ei es lista, por
    hipótesis la llamada recursiva devuelve su suma correcta. El total
    es la suma de todos los elementos. ∎

COMPLEJIDAD
    Sea n el número TOTAL de elementos contando todos los niveles.
    Tiempo: O(n) — cada elemento se visita exactamente una vez.
    Espacio: O(p) donde p es la profundidad máxima de anidamiento
             (la pila tiene un marco por nivel, no por elemento).

    Distinción importante: si la lista tiene 1,000,000 de elementos
    pero profundidad 2, el espacio de pila es O(2), no O(10^6). Pero
    si la profundidad es 500,000, se agota el límite de recursión
    de Python (~1000) aunque el total de elementos sea pequeeño.

    RIESGO REAL: un JSON profundamente anidado (por ejemplo, generado
    para explotar este límite) puede tumbar un parser recursivo. Los
    parsers de producción limitan la profundidad máxima explícitamente.

DÓNDE APARECE EN EL MUNDO REAL
    - Parsers de JSON y XML: la estructura es un valor, o una lista
      de valores, o un diccionario de valores.
    - Sistemas de archivos: un directorio contiene archivos y otros
      directorios.
    - Árboles de expresiones y de sintaxis abstracta (tema 03).

CASOS LÍMITE
    - Lista vacía: retorna 0.
    - Lista sin anidar: se comporta como la suma simple.
    - Anidamiento profundo: puede agotar la pila. Ver el aviso arriba.
"""


def suma_anidada(lista):
    """Suma recursivamente todos los números de una lista anidada.

    Dos casos base: elemento que no es lista (es número) y lista vacía.
    """
    total = 0
    for elemento in lista:
        if isinstance(elemento, list):
            total += suma_anidada(elemento)   # subproblema del mismo tipo
        else:
            total += elemento                 # caso base: es un número
    return total


def aplanar(lista):
    """Convierte una lista anidada en una lista plana.

    Mismo patrón recursivo, pero acumulando elementos en vez de sumar.
    """
    resultado = []
    for elemento in lista:
        if isinstance(elemento, list):
            resultado.extend(aplanar(elemento))
        else:
            resultado.append(elemento)
    return resultado


def profundidad_maxima(lista):
    """Calcula la profundidad máxima de anidamiento.

    Útil para saber si la recursión es segura antes de ejecutarla.
    """
    if not isinstance(lista, list):
        return 0
    if not lista:
        return 1
    return 1 + max(profundidad_maxima(e) for e in lista)


if __name__ == "__main__":
    # Caso del enunciado
    lista = [1, [2, 3], [4, [5, 6]]]
    print(f"Lista original:  {lista}")
    print(f"Suma:            {suma_anidada(lista)}")
    print(f"Aplanada:        {aplanar(lista)}")
    print(f"Profundidad máx: {profundidad_maxima(lista)}")

    # Casos base
    assert suma_anidada([]) == 0
    assert suma_anidada([1, 2, 3]) == 6, "sin anidar = suma simple"

    # Caso del enunciado: 1+2+3+4+5+6
    assert suma_anidada([1, [2, 3], [4, [5, 6]]]) == 21

    # Estructura más profunda y con negativos
    assert suma_anidada([[1, 2], [3, [4, [5, 6]]]]) == 21
    assert suma_anidada([1, [-2, 3]]) == 2

    # Aplanar produce exactamente los mismos números
    assert sorted(aplanar([1, [2, 3], [4, [5, 6]]])) == [1, 2, 3, 4, 5, 6]

    # Profundidad se mide en niveles, no en elementos
    assert profundidad_maxima([1, 2, 3]) == 1
    assert profundidad_maxima([1, [2, 3]]) == 2
    assert profundidad_maxima([[[[1]]]]) == 4

    # Verificación: la suma de la lista aplanada coincide
    assert sum(aplanar(lista)) == suma_anidada(lista)

    print("\n✓ Todas las pruebas pasaron")
