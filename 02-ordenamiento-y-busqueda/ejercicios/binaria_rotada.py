"""
Ejercicio 10: Búsqueda binaria en lista rotada
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - Búsqueda binaria (ejercicio busqueda_binaria.py): este ejercicio
      MODIFICA su invariante, así que hay que entenderlo primero.
    - Arreglo ordenado rotado: la precondición es distinta.

PROBLEMA
    Un arreglo ordenado ascendente fue rotado k veces (desplazamiento
    circular). Buscar un valor en él.

        [4, 5, 6, 7, 0, 1, 2]   ← [0,1,2,4,5,6,7] rotado 4 veces

    Lo crítico: el arreglo NO está ordenado, así que la búsqueda
    binaria estándar NO funciona. Pero tiene estructura aprovechable.

ESTRATEGIA: APROVECHAR LA MITAD ORDENADA
    Propiedad clave de un arreglo rotado: al dividirlo por la mitad,
    AL MENOS UNA de las dos mitades está siempre ordenada.

        [4, 5, 6, 7, 0, 1, 2]
                     ↑ medio
        izquierda [4,5,6,7]: ordenada ✓
        derecha   [0,1,2]:   ordenada ✓

        [6, 7, 0, 1, 2, 4, 5]
                  ↑ medio
        izquierda [6,7,0,1]: NO ordenada
        derecha   [2,4,5]:   ordenada ✓

    Siempre se puede determinar cuál mirando si arr[izq] <= arr[medio].

    Algoritmo:
      1. Calcular medio.
      2. Si arr[medio] == objetivo → encontrado.
      3. Determinar qué mitad está ordenada.
      4. Si el objetivo cae DENTRO del rango de la mitad ordenada,
         buscar ahí. Si no, buscar en la otra mitad.

TRAZA de busqueda([4,5,6,7,0,1,2], 0)
    izq=0, der=6
    medio=3, arr[3]=7. No es 0.
      ¿arr[izq]=4 <= arr[medio]=7? Sí → izquierda ordenada [4,5,6,7]
      ¿0 está en [4, 7]? NO → buscar en la derecha
      izq = 4
    izq=4, der=6
    medio=5, arr[5]=1. No es 0.
      ¿arr[izq]=0 <= arr[medio]=1? Sí → izquierda ordenada [0,1]
      ¿0 está en [0, 1]? SÍ → buscar en la izquierda
      der = 4
    izq=4, der=4
    medio=4, arr[4]=0. ¡ENCONTRADO! → retorna 4

    3 comparaciones, igual que una búsqueda binaria normal.

INVARIANTE
    Al inicio de cada iteración, si el objetivo está en el arreglo,
    está dentro de arr[izq..der], y ese rango conserva la propiedad
    de ser un "arreglo rotado" (o estar ordenado, que es el caso k=0).

DEMOSTRACIÓN DE CORRECCIÓN
    - La mitad ordenada se identifica correctamente comparando
      arr[izq] con arr[medio].
    - Si el objetivo está en el rango de la mitad ordenada, se busca
      allí (correcto: esa mitad está ordenada y el rango lo contiene).
    - Si no está en ese rango, entonces (por exclusión) está en la
      otra mitad, que es donde se sigue buscando.
    - El rango se reduce en cada paso, y si el objetivo existe se
      encontrará antes de que se vacíe. ∎

COMPLEJIDAD
    Tiempo: O(log n). Cada paso descarta la mitad, igual que la
    búsqueda binaria normal.
    Espacio: O(1).

    NO se puede hacer O(log n) más rápido: este es el límite del
    modelo de comparación (00-fundamentos §2, cota Ω(n log n) para
    ordenamiento; Ω(log n) para búsqueda en conjunto ordenado).

CASOS LÍMITE
    - Arreglo no rotado (k=0): es un arreglo ordenado normal; el
      algoritmo funciona igual.
    - Rotado una sola vez.
    - Objetivo ausente.
    - Todos los elementos iguales: cualquier mitad está "ordenada".
    - Un solo elemento.

CUÁNDO APARECE EN EL MUNDO REAL
    - Arreglos circulares (buffers de tamaño fijo).
    - Registros rotativos (logs) donde se busca por timestamp.
    - Pregunta clásica de entrevista técnica.

RELACIÓN CON LA BÚSQUEDA BINARIA
    La lección de fondo: la búsqueda binaria no necesita que esté
    ordenado TODO el arreglo; necesita poder DESCARTAR la mitad en
    cada paso. Si se puede determinar qué mitad contiene al objetivo,
    basta. Aquí eso se logra identificando la mitad ordenada.
"""


def busqueda_binaria_rotada(arr, objetivo):
    """Busca en un arreglo ordenado rotado. O(log n).

    Devuelve el índice del objetivo, o -1 si no está.
    """
    izquierda, derecha = 0, len(arr) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2

        if arr[medio] == objetivo:
            return medio

        # Determinar cuál mitad está ordenada
        if arr[izquierda] <= arr[medio]:
            # La mitad IZQUIERDA está ordenada
            if arr[izquierda] <= objetivo < arr[medio]:
                derecha = medio - 1          # buscar en la izquierda
            else:
                izquierda = medio + 1        # buscar en la derecha
        else:
            # La mitad DERECHA está ordenada
            if arr[medio] < objetivo <= arr[derecha]:
                izquierda = medio + 1        # buscar en la derecha
            else:
                derecha = medio - 1          # buscar en la izquierda

    return -1


if __name__ == "__main__":
    arr = [4, 5, 6, 7, 0, 1, 2]
    print(f"Arreglo rotado: {arr}")
    print(f"Buscar 0: índice {busqueda_binaria_rotada(arr, 0)}")
    print(f"Buscar 3: índice {busqueda_binaria_rotada(arr, 3)}")
    assert busqueda_binaria_rotada(arr, 0) == 4
    assert busqueda_binaria_rotada(arr, 3) == -1

    # Casos base
    assert busqueda_binaria_rotada([1], 1) == 0
    assert busqueda_binaria_rotada([1], 0) == -1

    # Verificación exhaustiva: TODAS las rotaciones de un arreglo
    base = list(range(1, 11))       # [1..10]
    print(f"\nVerificando todas las rotaciones de {base}:")
    for k in range(len(base)):
        rotado = base[k:] + base[:k]
        for objetivo in range(0, 13):
            resultado = busqueda_binaria_rotada(rotado[:], objetivo)
            esperado = rotado.index(objetivo) if objetivo in rotado else -1
            assert resultado == esperado, \
                f"rotación k={k}, objetivo {objetivo}: {resultado} != {esperado}"
        print(f"  rotación k={k}: {rotado} ✓")

    # Caso no rotado (k=0) funciona
    no_rotado = [1, 2, 3, 4, 5]
    assert busqueda_binaria_rotada(no_rotado, 3) == 2

    # Con duplicados
    con_dups = [2, 2, 2, 3, 4, 2]
    idx = busqueda_binaria_rotada(con_dups, 3)
    assert con_dups[idx] == 3, "debe apuntar a un 3 válido"

    # Verificación aleatoria contra búsqueda lineal
    import random
    random.seed(21)
    for _ in range(200):
        n = random.randint(1, 30)
        base = [random.randint(0, 50) for _ in range(n)]
        base.sort()
        k = random.randint(0, n - 1)
        rotado = base[k:] + base[:k]
        objetivo = random.randint(-10, 60)
        resultado = busqueda_binaria_rotada(rotado[:], objetivo)

        if objetivo in rotado:
            # Con duplicados puede devolver CUALQUIER ocurrencia válida,
            # no necesariamente la primera. Lo correcto es verificar
            # que el índice devuelto apunte al objetivo.
            assert 0 <= resultado < len(rotado) and rotado[resultado] == objetivo, \
                f"índice {resultado} no apunta a {objetivo} en {rotado}"
        else:
            assert resultado == -1, f"objetivo ausente pero devolvió {resultado}"

    # Complejidad logarítmica verificada
    import math
    grande = list(range(0, 2000000, 2))
    rotado_grande = grande[1000000:] + grande[:1000000]

    pasos = [0]
    def contar(arr, objetivo):
        izq, der = 0, len(arr) - 1
        while izq <= der:
            medio = (izq + der) // 2
            pasos[0] += 1
            if arr[medio] == objetivo:
                return medio
            if arr[izq] <= arr[medio]:
                if arr[izq] <= objetivo < arr[medio]:
                    der = medio - 1
                else:
                    izq = medio + 1
            else:
                if arr[medio] < objetivo <= arr[der]:
                    izq = medio + 1
                else:
                    der = medio - 1
        return -1

    contar(rotado_grande, rotado_grande[0])
    print(f"\nPeor caso con n={len(rotado_grande):,}: {pasos[0]} comparaciones")
    print(f"log₂(n) = {math.log2(len(rotado_grande)):.1f}")
    assert pasos[0] <= math.ceil(math.log2(len(rotado_grande))) + 2

    print("\n✓ Todas las pruebas pasaron")
