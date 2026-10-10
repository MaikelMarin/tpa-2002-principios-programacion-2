"""
Ejercicio 2: Potencia recursiva
Dificultad: Básico

CONOCIMIENTO PREVIO NECESARIO
    - Logaritmos (00-fundamentos §4): la versión eficiente reduce el
      problema a la mitad, y eso da exactamente log(e) pasos.
    - Divide y vencerás: es el primer ejemplo del proyecto donde la
      reducción no es "n-1" sino "n/2".

PROBLEMA
    Calcular b elevado a e (b^e), para e ≥ 0.

FONDO MATEMÁTICO
    La definición permite dos recurrencias distintas, y la elección
    entre ellas es todo el ejercicio:

        Ingenua:    b^e = b · b^(e-1)          → O(e)
        Eficiente:  b^e = (b^(e/2))^2  si e par
                    b^e = b · (b^((e-1)/2))^2 si e impar
                                                     → O(log e)

    La segunda funciona porque elevar al cuadrado una potencia ya
    calculada duplica el exponente de golpe.

ESTRATEGIA (versión eficiente)
    1. Si e = 0, retornar 1 (caso base: todo número elevado a 0 es 1).
    2. Calcular mitad = b^(e // 2) recursivamente.
    3. Si e es par, el resultado es mitad × mitad.
       Si e es impar, sobra un factor b: b × mitad × mitad.

    Calcular `mitad` UNA sola vez es importante: si se llamara dos
    veces a la función, el costo volvería a ser lineal.

TRAZA DE potencia(2, 10)
    Llamada      (b,e)   Paridad   Sub-llamada
    p(2,10)      (2,10)  par       p(2,5)
    p(2,5)       (2,5)   impar     p(2,2)
    p(2,2)       (2,2)   par       p(2,1)
    p(2,1)       (2,1)   impar     p(2,0)
    p(2,0)       (2,0)   base      retorna 1

    5 llamadas para exponente 10, no 10. En general: ⌊log₂(e)⌋ + 1.

DEMOSTRACIÓN DE CORRECCIÓN (inducción sobre e)
    Caso base: e = 0. Retorna 1 = b^0. Correcto.

    Hipótesis: potencia(b, k) = b^k para todo k < e.

    Paso: sea m = potencia(b, e//2) = b^(e//2) por hipótesis.
      - Si e es par, e = 2·(e//2), retorna m·m = b^(e//2)·b^(e//2)
        = b^(2·e//2) = b^e. Correcto.
      - Si e es impar, e = 2·(e//2) + 1, retorna b·m·m =
        b^(1 + 2·e//2) = b^e. Correcto. ∎

COMPLEJIDAD
    Recurrencia: T(e) = T(e/2) + O(1)
    Por Teorema Maestro (a=1, b=2, c=0, f(n)=1=Θ(n^0)): caso 2.
    Tiempo: O(log e)
    Espacio: O(log e) de pila

    Para e = 1,000,000: la versión ingenua hace un millón de
    multiplicaciones; la eficiente, 20.

CASOS LÍMITE
    - e = 0: retorna 1 (incluso 0^0 se define como 1 aquí).
    - e negativo: no soportado en esta implementación; se podría
      extender retornando 1/potencia(b, -e) con control de división
      por cero cuando b = 0.

EJERCICIO RELACIONADO
    Esta función es el ejemplo canónico de divide y vencerás que
    después se verá en Merge Sort (tema 02).
"""


def potencia(base, exponente):
    """b^e por recursión ingenua: O(e)."""
    if exponente < 0:
        raise ValueError("Exponente negativo no soportado en esta implementación")
    if exponente == 0:
        return 1
    return base * potencia(base, exponente - 1)


def potencia_eficiente(base, exponente):
    """b^e por divide y vencerás: O(log e).

    Clave: calcular la potencia del subproblema UNA sola vez y
    reutilizarla para el caso par y el impar.
    """
    if exponente < 0:
        raise ValueError("Exponente negativo no soportado en esta implementación")
    if exponente == 0:
        return 1

    mitad = potencia_eficiente(base, exponente // 2)  # subproblema

    if exponente % 2 == 0:
        return mitad * mitad                # b^e = (b^(e/2))^2
    return base * mitad * mitad             # b^e = b · (b^((e-1)/2))^2


if __name__ == "__main__":
    print("Versión ingenua:")
    print(f"  2^10 = {potencia(2, 10)}")
    print(f"  3^4  = {potencia(3, 4)}")
    print(f"  5^0  = {potencia(5, 0)}")

    print("\nVersión eficiente (divide y vencerás):")
    print(f"  2^10 = {potencia_eficiente(2, 10)}")
    print(f"  2^20 = {potencia_eficiente(2, 20)}")
    print(f"  10^8 = {potencia_eficiente(10, 8)}")

    # Ambas versiones deben coincidir siempre
    for b in [0, 1, 2, 3, 7]:
        for e in range(0, 12):
            assert potencia(b, e) == potencia_eficiente(b, e), f"discrepancia en {b}^{e}"

    # Casos base
    assert potencia_eficiente(5, 0) == 1
    assert potencia_eficiente(1, 100) == 1
    assert potencia_eficiente(0, 5) == 0

    # Exponente negativo
    try:
        potencia_eficiente(2, -1)
        raise AssertionError("debía lanzar ValueError")
    except ValueError:
        pass

    print("\n✓ Todas las pruebas pasaron")
