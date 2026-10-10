"""
Ejercicio 14: Palíndromo recursivo
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Patrón cabeza + cola aplicado a cadenas.
    - Inducción sobre la longitud de la cadena.

PROBLEMA
    Determinar si una cadena es palíndromo: se lee igual de izquierda
    a derecha que de derecha a izquierda. Ignorar espacios y
    mayúsculas.

        "anita lava la tina"          → palíndromo
        "A man a plan a canal Panama"  → palíndromo
        "hola"                         → no palíndromo

FONDO MATEMÁTICO
    Definición inductiva de palíndromo sobre una cadena s:
        - La cadena vacía es palíndromo.
        - Una cadena de un carácter es palíndromo.
        - s es palíndromo si y solo si:
              primer(s) == ultimo(s)   Y   el interior de s es palíndromo

    Es exactamente cabeza + cola, pero con cabeza = primer carácter
    y cola = todos menos el último.

ESTRATEGIA
    1. NORMALIZAR: quitar espacios y pasar a minúsculas. Hacer esto
       una sola vez al inicio, no en cada llamada recursiva.
    2. Comparar el primer y el último carácter.
    3. Si difieren, no es palíndromo (se puede cortar inmediatamente).
    4. Si coinciden, recursar sobre el interior.
    5. Caso base: cuando los índices se cruzan o son iguales → es
       palíndromo (se verificaron todos los pares).

    Se usan dos índices (izq, der) en vez de rebanadas, para evitar
    el costo O(n) por copia que se vio en el ejercicio 4.

TRAZA DE verificar("ana", 0, 2)
    Llamada          izq der   s[izq]  s[der]  ¿Iguales?   Acción
    verificar(a,0,2)  0   2     a       a       Sí         → verificar(1,1)
    verificar(a,1,1)  1   1     n       n       Sí         izq>=der → True

    Resultado: es palíndromo.

    Contraste con "hola":
    verificar(h,0,3)  0  3     h  a   No  → False inmediato

DEMOSTRACIÓN DE CORRECCIÓN (inducción sobre la longitud)
    Caso base: izq >= der. Se han comparado todos los pares de
    posiciones simétricas y coincidían. La cadena es palíndromo.

    Hipótesis: verificar(izq+1, der-1) es correcto.

    Paso: si s[izq] != s[der], ningún palíndromo puede tener extremos
    distintos, así que retornar False es correcto. Si son iguales, toda
    la cadena es palíndromo si y solo si el interior lo es, que es lo
    que evalúa la llamada recursiva. ∎

COMPLEJIDAD
    Tiempo: O(n) — cada carácter se compara una vez.
    Espacio: O(n) de pila — un marco por par comparado.
             La normalización crea una copia: O(n) adicional.

CASOS LÍMITE
    - Cadena vacía: es palíndromo (caso base trivial).
    - Un carácter: es palíndromo.
    - Solo espacios: al normalizar queda vacía → palíndromo.
    - Mayúsculas y espacios: se ignoran por normalización.

POR QUÉ NORMALIZAR ANTES
    La normalización es O(n). Si se hiciera dentro de la recursión,
    se repetiría en cada nivel y el costo sería O(n^2). Es el mismo
    error que `lista[1:]` en el ejercicio 4: esconder un O(n) dentro
    de una operación que parece O(1).

RELACIÓN CON OTROS TEMAS
    El mismo patrón "comparar extremos y recursar al interior"
    aparece en la búsqueda binaria (tema 02), donde se descarta la
    mitad y se recursa sobre el resto.
"""


def normalizar(texto):
    """Quita espacios y pasa a minúsculas. O(n), una sola vez."""
    return texto.lower().replace(" ", "")


def es_palindromo(texto):
    """Verifica recursivamente si una cadena es palíndromo.

    Usa dos índices (izq, der) para evitar copiar la cadena.
    """
    texto = normalizar(texto)

    def verificar(izquierda, derecha):
        if izquierda >= derecha:        # caso base: se cruzaron
            return True
        if texto[izquierda] != texto[derecha]:
            return False                # extremos distintos → cortar
        return verificar(izquierda + 1, derecha - 1)

    return verificar(0, len(texto) - 1)


def es_palindromo_simple(texto):
    """Versión no recursiva, para verificar que ambas coinciden."""
    texto = normalizar(texto)
    return texto == texto[::-1]


if __name__ == "__main__":
    pruebas = [
        ("ana", True),
        ("reconocer", True),
        ("anita lava la tina", True),
        ("A man a plan a canal Panama", True),
        ("hola", False),
        ("python", False),
        ("", True),                       # cadena vacía
        ("a", True),                      # un carácter
        ("   ", True),                    # solo espacios
        ("Aa", True),                     # caso mayúsculas
        ("ab", False),
        ("abcba", True),
    ]

    print("Verificación de palíndromos:")
    for texto, esperado in pruebas:
        resultado = es_palindromo(texto)
        marca = "✓" if resultado == esperado else "✗"
        print(f"  {marca} {texto!r:38} → {resultado}")

    # Todas las pruebas
    for texto, esperado in pruebas:
        assert es_palindromo(texto) == esperado, f"falló con {texto!r}"

    # Ambas versiones coinciden siempre
    for texto, _ in pruebas:
        assert es_palindromo(texto) == es_palindromo_simple(texto)

    print("\n✓ Todas las pruebas pasaron")
