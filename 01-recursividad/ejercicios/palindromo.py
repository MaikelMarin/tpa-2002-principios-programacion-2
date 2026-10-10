"""
Ejercicio 14: Palíndromo recursivo
Dificultad: Básico

Un palíndromo es una palabra o frase que se lee igual de izquierda a derecha
que de derecha a izquierda, ignorando espacios y mayúsculas.
"""

def es_palindromo(texto):
    """Verifica si una cadena es palíndromo recursivamente."""
    # Normalizar: quitar espacios y convertir a minúsculas
    texto = texto.lower().replace(" ", "")

    def verificar(izquierda, derecha):
        if izquierda >= derecha:
            return True
        if texto[izquierda] != texto[derecha]:
            return False
        return verificar(izquierda + 1, derecha - 1)

    return verificar(0, len(texto) - 1)


def es_palindromo_simple(texto):
    """Versión simple (no recursiva) para comparación."""
    texto = texto.lower().replace(" ", "")
    return texto == texto[::-1]


if __name__ == "__main__":
    pruebas = [
        ("ana", True),
        ("reconocer", True),
        ("anita lava la tina", True),
        ("A man a plan a canal Panama", True),
        ("hola", False),
        ("python", False),
        ("", True),
        ("a", True),
    ]

    for texto, esperado in pruebas:
        resultado = es_palindromo(texto)
        print(f"'{texto}' → {resultado}")
        assert resultado == esperado
        assert es_palindromo_simple(texto) == esperado

    print("\n✓ Todas las pruebas pasaron")
