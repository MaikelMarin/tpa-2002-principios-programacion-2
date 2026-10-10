# 00 — Fundamentos

Andamiaje matemático y computacional necesario para comprender los seis temas del proyecto. Este documento es el cimiento: todo lo demás se apoya en él.

## Qué contiene

| Sección | Contenido |
|---------|-----------|
| 1. Mapa conceptual | Vista general de cómo se relacionan las secciones |
| 2. Notación asintótica | O, Ω, Θ, o, ω: definiciones formales, derivaciones trabajadas, trampas |
| 3. Inducción matemática | Simple, fuerte y estructural, con demostraciones completas |
| 4. Logaritmos y exponenciales | Por qué aparece `log n`, identidades, crecimiento comparado |
| 5. Sumatorias y series | Aritmética, geométrica, armónica; tabla de referencia |
| 6. Análisis de algoritmos | Contar operaciones, casos, invariantes de bucle, análisis amortizado |
| 7. Recurrencias | Tres métodos de solución y Teorema Maestro con ejemplos resueltos |
| 8. Estructuras de datos fundamentales | Arreglo, lista enlazada, pila, cola, hash con tablas de coste |
| 9. Modelo de memoria | Stack vs heap, referencias vs valores, localidad de caché |
| 10. Python esencial | Clases, comprensiones, generadores, `with`, `struct`, `collections` |

## Ruta de lectura recomendada

1. **Sección 2** (notación) — es el lenguaje de todo el proyecto.
2. **Sección 3** (inducción) — necesaria para entender por qué los algoritmos son correctos.
3. **Secciones 4 y 5** (logaritmos y sumatorias) — las herramientas de cálculo.
4. **Secciones 6 y 7** (análisis y recurrencias) — cómo se mide y resuelve el costo.
5. **Sección 8** (estructuras) — la línea de base contra la que se comparan árboles y grafos.
6. **Secciones 9 y 10** (memoria y Python) — consultar según haga falta.

No es necesario leerlo completo antes de empezar. Cada tema indica en su sección **Prerequisitos** qué apartados necesita.

## Demostraciones trabajadas incluidas

- Derivación de `3n² + 5n + 7 = O(n²)`
- Suma de los primeros n naturales (Gauss)
- Correctitud de la búsqueda binaria por invariante
- Inorden de un BST produce secuencia ordenada (inducción estructural)
- Resolución de `T(n) = 2T(n/2) + n` por sustitución, árbol y Teorema Maestro

## Recursos

- Teoría completa: `teoria.md`
- Siguiente tema: `../01-recursividad/`
