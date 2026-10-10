"""
Ejercicio 2: Potencia recursiva
Dificultad: Básico

Recurrencia:
    potencia(b, e) = b × potencia(b, e-1)
    potencia(b, 0) = 1
"""

def potencia(base, exponente):
    """Calcula base^exponente de forma recursiva."""
    if exponente < 0:
        raise ValueError("Exponente negativo no soportado en esta implementación")
    if exponente == 0:
        return 1
    return base * potencia(base, exponente - 1)


def potencia_eficiente(base, exponente):
    """Versión optimizada usando divide y vencerás: O(log n)."""
    if exponente < 0:
        raise ValueError("Exponente negativo no soportado")
    if exponente == 0:
        return 1
    mitad = potencia_eficiente(base, exponente // 2)
    if exponente % 2 == 0:
        return mitad * mitad
    return base * mitad * mitad


if __name__ == "__main__":
    print(f"2^10 = {potencia(2, 10)}")
    print(f"3^4 = {potencia(3, 4)}")
    print(f"5^0 = {potencia(5, 0)}")
    print(f"2^10 (eficiente) = {potencia_eficiente(2, 10)}")

    assert potencia(2, 10) == 1024
    assert potencia(3, 4) == 81
    assert potencia(5, 0) == 1
    assert potencia_eficiente(2, 10) == 1024
    print("\n✓ Todas las pruebas pasaron")
