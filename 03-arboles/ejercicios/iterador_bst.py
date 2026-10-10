r"""
Ejercicio 15: Iterador para BST
Dificultad: Experto

CONOCIMIENTO PREVIO NECESARIO
    - Inorden iterativo con pila (ejercicio inorden_iterativo.py).
    - Generadores (00-fundamentos §10.4).
    - Análisis amortizado: O(1) promedio por llamada.

PROBLEMA
    Implementar un iterador que recorra un BST en inorden, con
    next() y hasNext() en O(1) amortizado.

¿POR QUÉ IMPORTA EL "AMORTIZADO"?
    Un next() individual puede costar más de O(1): si toca bajar por
    una rama larga para recargar la pila, esa llamada cuesta O(h).

    Pero cada nodo se apila y desapila EXACTAMENTE UNA VEZ en toda la
    vida del iterador. Entonces el trabajo total es O(n) para n
    llamadas, es decir O(1) AMORTIZADO por llamada.

    Es la misma idea que el append() de una lista dinámica: algunas
    llamadas cuestan O(n) (redimensionar), pero el promedio es O(1).

ESTRATEGIA
    Mantener una pila con el "camino pendiente hacia la izquierda".

    - Al construir el iterador: apilar toda la rama izquierda desde
      la raíz. El tope de la pila es el siguiente elemento a visitar.
    - next(): desapilar el tope (ese es el valor a devolver). Si ese
      nodo tiene hijo derecho, apilar toda la rama izquierda de ese
      hijo derecho (los siguientes en inorden).
    - hasNext(): la pila no está vacía.

```python
class IteradorBST:
    def __init__(self, raiz):
        self.pila = []
        self._apilar_izquierdos(raiz)

    def _apilar_izquierdos(self, nodo):
        while nodo:
            self.pila.append(nodo)
            nodo = nodo.izquierdo

    def next(self):
        nodo = self.pila.pop()
        self._apilar_izquierdos(nodo.derecho)   # recargar
        return nodo.valor

    def hasNext(self):
        return len(self.pila) > 0
```

TRAZA sobre:
        7
       / \
      3   15
     / \
    1   5

    __init__: apilar 7, apilar 3, apilar 1
              pila = [7, 3, 1], tope = 1

    next() → pop 1 (devolver 1). 1.derecho es None, no apilar nada.
              pila = [7, 3]
    next() → pop 3 (devolver 3). 3.derecho = 5 → apilar 5.
              pila = [7, 5]
    next() → pop 5 (devolver 5). 5.derecho es None.
              pila = [7]
    next() → pop 7 (devolver 7). 7.derecho = 15 → apilar 15.
              pila = [15]
    next() → pop 15 (devolver 15).
              pila = []
    hasNext() → False

    Secuencia: 1, 3, 5, 7, 15  ← inorden correcto

DEMOSTRACIÓN DEL O(1) AMORTIZADO
    Cada nodo del árbol se apila como máximo una vez y se desapila
    exactamente una vez. El trabajo total de _apilar_izquierdos en
    toda la ejecución es, por tanto, O(n) (cada nodo se procesa una
    vez).

    Distribuido sobre las n llamadas a next(): O(1) por llamada. ∎

COMPLEJIDAD
    next():    O(1) amortizado, O(h) en el peor caso individual.
    hasNext(): O(1).
    Espacio:   O(h) para la pila.

    Contraste con la versión que devuelve una lista completa:
    inorden_iterativo() es O(n) tiempo y O(n) espacio de una sola
    vez. El iterador es O(n) total pero O(h) de espacio y permite
    PARAR a mitad de camino sin haber pagado por el resto.

CUÁNDO USAR ITERADOR vs LISTA
    - Iterador: recorridos parciales (buscar el primer elemento que
      cumpla algo), árboles grandes, composición con otros iteradores.
    - Lista: cuando se necesita todo el recorrido y se quiere
      indexar o recorrer varias veces.

RELACIÓN CON OTROS TEMAS
    - En bases de datos, los cursores sobre índices B-tree funcionan
      exactamente así: mantienen el camino actual y avanzan en O(1)
      amortizado.
    - El patrón "apilar pendientes" es el mismo del DFS iterativo
      (tema 04).
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

    def __repr__(self):
        return f"Nodo({self.valor})"


class IteradorBST:
    """Iterador inorden para BST: O(1) amortizado por next()."""

    def __init__(self, raiz):
        self.pila = []
        self._apilar_izquierdos(raiz)

    def _apilar_izquierdos(self, nodo):
        """Apila todo el camino izquierdo desde `nodo`."""
        while nodo:
            self.pila.append(nodo)
            nodo = nodo.izquierdo

    def next(self):
        """Devuelve el siguiente valor en inorden."""
        nodo = self.pila.pop()
        # Si tiene subárbol derecho, sus elementos vienen después
        self._apilar_izquierdos(nodo.derecho)
        return nodo.valor

    def hasNext(self):
        """¿Quedan elementos?"""
        return len(self.pila) > 0


def insertar(raiz, valor):
    if raiz is None:
        return Nodo(valor)
    if valor < raiz.valor:
        raiz.izquierdo = insertar(raiz.izquierdo, valor)
    elif valor > raiz.valor:
        raiz.derecho = insertar(raiz.derecho, valor)
    return raiz


def inorden_iterativo(raiz):
    """Recorrido completo con pila, para verificar el iterador."""
    pila, resultado = [], []
    actual = raiz
    while actual or pila:
        while actual:
            pila.append(actual)
            actual = actual.izquierdo
        actual = pila.pop()
        resultado.append(actual.valor)
        actual = actual.derecho
    return resultado


if __name__ == "__main__":
    raiz = None
    for val in [7, 3, 15, 1, 5, 11, 20]:
        raiz = insertar(raiz, val)

    # Recorrido completo con el iterador
    it = IteradorBST(raiz)
    resultado = []
    while it.hasNext():
        resultado.append(it.next())

    print(f"Recorrido con iterador: {resultado}")
    assert resultado == [1, 3, 5, 7, 11, 15, 20]
    assert resultado == inorden_iterativo(raiz)

    # Uso parcial: no recorrer todo. OJO: los print de arriba NO deben
    # consumir el iterador; aquí se usa uno nuevo.
    it2 = IteradorBST(raiz)
    print(f"Primer elemento: {it2.next()}")
    print(f"Segundo elemento: {it2.next()}")

    # Con uno nuevo (el anterior ya consumió 2) para las aserciones
    it3 = IteradorBST(raiz)
    assert it3.next() == 1
    assert it3.next() == 3
    # Y se puede continuar después
    assert it3.next() == 5
    assert it3.hasNext() is True

    # El iterador consumido llega al final
    while it3.hasNext():
        it3.next()
    assert it3.hasNext() is False

    # Casos base
    it_vacio = IteradorBST(None)
    assert it_vacio.hasNext() is False

    it_solo = IteradorBST(Nodo(42))
    assert it_solo.hasNext() is True
    assert it_solo.next() == 42
    assert it_solo.hasNext() is False

    # Generador: misma lógica, sintaxis más simple
    def inorden_generador(raiz):
        pila = []
        actual = raiz
        while actual or pila:
            while actual:
                pila.append(actual)
                actual = actual.izquierdo
            actual = pila.pop()
            yield actual.valor
            actual = actual.derecho

    gen = list(inorden_generador(raiz))
    assert gen == resultado, "el generador debe coincidir"

    # Consumo perezoso: parar a la mitad
    gen2 = inorden_generador(raiz)
    assert next(gen2) == 1
    assert next(gen2) == 3
    # El resto no se ha procesado
    assert next(gen2) == 5

    # Verificación de O(1) amortizado: contar apilamientos totales
    class IteradorContador:
        def __init__(self, raiz):
            self.pila = []
            self.apilados = 0
            self._apilar(raiz)

        def _apilar(self, nodo):
            while nodo:
                self.pila.append(nodo)
                self.apilados += 1
                nodo = nodo.izquierdo

        def next(self):
            nodo = self.pila.pop()
            self._apilar(nodo.derecho)
            return nodo.valor

        def hasNext(self):
            return len(self.pila) > 0

    ic = IteradorContador(raiz)
    n_nodos = len(resultado)
    while ic.hasNext():
        ic.next()
    print(f"\nNodos: {n_nodos}, apilamientos totales: {ic.apilados}")
    assert ic.apilados == n_nodos, "cada nodo se apila exactamente una vez"
    print(f"→ {ic.apilados} apilamientos para {n_nodos} next(): O(1) amortizado")

    # Con un árbol grande el amortizado se mantiene
    import random
    random.seed(61)
    valores = random.sample(range(10000), 2000)
    grande = None
    for v in valores:
        grande = insertar(grande, v)

    icg = IteradorContador(grande)
    contador_next = 0
    while icg.hasNext():
        icg.next()
        contador_next += 1
    assert icg.apilados == contador_next, "el amortizado se mantiene"

    print("\n✓ Todas las pruebas pasaron")
