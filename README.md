# TPA-2002 — Principios de Programación 2

Proyecto de aprendizaje y creación de ejercicios para dominar cada tema del curso a la perfección.

> **Autor:** Maikel Marín Brenes — [Vipermech](https://github.com/MaikelMarin)
>
> **Asistencia de IA:** Este proyecto fue creado con asistencia de inteligencia artificial (OpenCode). La IA colaboró en la creación de la estructura, la redacción de la documentación teórica, la implementación de los ejercicios y el desarrollo de la aplicación web. La dirección, los requisitos y las decisiones del proyecto son del autor.

---

## Cómo ejecutar la página web

El proyecto incluye una aplicación web para explorar todo el contenido (teoría y ejercicios) de forma visual e interactiva. **No requiere instalación de dependencias**: es HTML, CSS y JavaScript puro.

### Requisito único

Tener **Python 3** instalado (para levantar el servidor local). No hace falta `pip install` de nada.

### Pasos

**1. Abre una terminal en la carpeta raíz del proyecto** (donde está este README).

**2. Levanta el servidor:**

```bash
python -m http.server 8080
```

Verás un mensaje como `Serving HTTP on 0.0.0.0 port 8080`. Déjalo corriendo.

**3. Abre tu navegador y entra a:**

```
http://localhost:8080/web/
```

Listo. Ya puedes navegar por las 7 temáticas.

> **Importante:** abre la URL con `/web/` al final. El servidor se levanta desde la **raíz del proyecto**, no desde la carpeta `web/`. Si lo levantas desde dentro de `web/`, el contenido no cargará (la aplicación lee `../contenido.json`).

### Si el puerto 8080 está ocupado

```bash
python -m http.server 3000
```

Y entra a `http://localhost:3000/web/`.

### ¿Por qué hace falta un servidor?

La página lee los archivos `.md` y `.py` para mostrarlos. Los navegadores **bloquean** esa lectura si abres `index.html` con doble clic (protocolo `file://`), por seguridad. Un servidor local lo resuelve.

### Alternativa sin terminal

Cualquier servidor estático funciona. Por ejemplo con Node.js:

```bash
npx serve .
```

O con la extensión **Live Server** de VS Code: abre `web/index.html`, clic derecho → *Open with Live Server*.

---

## Qué ofrece la página

| Función | Descripción |
|---------|-------------|
| Navegación | 7 temáticas y 100 documentos organizados en árbol |
| Búsqueda | Busca por nombre, insensible a acentos (`teoria` encuentra `Teoría`). Atajo: tecla `/` |
| Temas | Modo oscuro y claro; se recuerda tu elección |
| Teoría | Markdown renderizado: tablas, código con resaltado, citas |
| Código | Resaltado de sintaxis para Python y C++, con botón de copiar |
| Progreso | Marca los documentos que ya leíste |
| Atajos | Flechas `←` `→` para moverte entre documentos |

---

## Estructura del proyecto

```
Proyecto/
├── README.md                          ← Este archivo
├── contenido.json                     ← Manifiesto de contenido (lo usa la web)
├── web/                               ← Aplicación web (HTML + CSS + JS puro)
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── 00-fundamentos/                    ← Andamiaje matemático y computacional
├── 01-recursividad/                   ← Fundamentos de recursividad
├── 02-ordenamiento-y-busqueda/        ← Métodos de ordenamiento y búsqueda
├── 03-arboles/                        ← Estructuras de datos jerárquicas
├── 04-grafos/                         ← Estructuras de datos tipo red
├── 05-archivos/                       ← Procesamiento de archivos
└── 06-grandes-datos/                  ← Procesamiento de grandes volúmenes de datos
```

Cada temática contiene:

| Elemento | Descripción |
|----------|-------------|
| `README.md` | Temas, mapa conceptual, contenido categorizado, ruta de aprendizaje y lista de ejercicios |
| `teoria.md` | Documento teórico detallado con demostraciones y bibliografía |
| `ejercicios/` | Solución de cada ejercicio (un archivo por problema) |
| `soluciones/` | Solo en el tema 06: versión ampliada con mediciones |

---

## El hilo conductor

Los 7 temas no son una lista suelta: forman una progresión donde cada uno se apoya en el anterior.

| Tema | Se apoya en | Idea que aporta |
|------|-------------|-----------------|
| **00 Fundamentos** | — | Notación asintótica, inducción, recurrencias, costes de estructuras. **Es el cimiento de todo lo demás** |
| **01 Recursividad** | 00 (inducción) | Resolver un problema dividiéndolo en versiones más pequeñas de sí mismo |
| **02 Ordenamiento** | 01 (divide y vencerás) | La primera aplicación real de la recursión; la cota Ω(n log n) |
| **03 Árboles** | 01 (recursión sobre estructuras) | La estructura de datos donde la recursión es natural |
| **04 Grafos** | 01, 02, 03 | Generalizar los árboles a redes arbitrarias |
| **05 Archivos** | 00 (memoria) | Persistencia: lo que pasa cuando los datos no caben en RAM |
| **06 Grandes datos** | Todo lo anterior | Qué hacer cuando ni siquiera el disco alcanza |

### Los tres ejes que cruzan todo el proyecto

1. **Rigor académico** — cada algoritmo trae su demostración de corrección y su análisis de complejidad desarrollado, no solo la fórmula final.
2. **Rigor técnico** — cada ejercicio es ejecutable y se verifica a sí mismo. **88/88 archivos pasan sus pruebas.**
3. **Comprensión profunda** — cada tema incluye historia (de dónde salió el algoritmo), trade-offs (por qué existe más de uno) y casos límite (cuándo falla).

---

## Ejecutar los ejercicios

Cada ejercicio es un archivo independiente con sus propias pruebas:

```bash
python 01-recursividad/ejercicios/factorial.py
```

La salida termina con `✓ Todas las pruebas pasaron` si todo va bien.

Para correr una temática completa:

```bash
for f in 01-recursividad/ejercicios/*.py; do python "$f"; done
```

---

## Cómo leer cada ejercicio

Todos siguen la misma estructura, para que sepas siempre dónde buscar:

| Sección | Qué contiene |
|---------|--------------|
| **Conocimiento previo** | Qué apartados de `00-fundamentos` y de otros temas necesitas |
| **Problema** | Qué se pide, en una o dos frases |
| **Fondo matemático** | La teoría detrás: definiciones, propiedades, por qué funciona |
| **Estrategia** | Cómo se aborda el problema y por qué de esa forma |
| **Traza** | Estado paso a paso de la ejecución, con tablas |
| **Demostración** | Argumento de corrección (inducción o invariante) |
| **Complejidad** | Análisis razonado de tiempo y espacio |
| **Casos límite** | Vacío, un elemento, no encontrado, desbordamiento |
| **Verificación** | Pruebas automáticas, a veces contra fuerza bruta |

Si un ejercicio asume algo que no entiendes, la sección **Conocimiento previo** te dice exactamente a dónde ir.

---

## Contenido de cada temática

| # | Temática | Ejercicios | Contenido |
|---|----------|------------|-----------|
| 00 | Fundamentos | — | Notación asintótica, inducción, logaritmos, sumatorias, análisis, recurrencias, estructuras, memoria, Python |
| 01 | Recursividad | 18 | Factorial, Fibonacci (3 versiones), backtracking (7 problemas), N reinas, Hanói, Knapsack |
| 02 | Ordenamiento y búsqueda | 11 | Los 5 ordenamientos, 2 búsquedas, Quick in-place, Merge en lista enlazada, híbrido |
| 03 | Árboles | 20 | BST completo, AVL con rotaciones, recorridos iterativos, LCA, k-ésimo, serialización |
| 04 | Grafos | 18 | Lista y matriz de adyacencia, BFS, DFS, ciclos (dirigidos y no), Dijkstra, Kruskal, Prim, bipartito |
| 05 | Archivos | 15 | Texto, binario con `struct`, acceso aleatorio, CSV, RLE, sistema de archivos virtual |
| 06 | Grandes datos | 6 | Generación masiva, análisis por streaming, ordenamiento externo (secuencial y paralelo) |

---

## Nota sobre los archivos excluidos

Este repositorio **no incluye** (ver `.gitignore`):

- `public_TPA-2002_Principios_de_Programación_2.pdf` y `public_Cronograma_...pdf` — son propiedad del **Tecnológico de Costa Rica**. Se usaron como fuente de verdad para definir los contenidos, pero no se redistribuyen.
- Configuración local de agentes (`.agents/`, `skills-lock.json`, `SKILL.md`).

Nota: `AGENTS.md` **sí** está versionado a propósito: documenta las convenciones del proyecto.

## Convenciones

- **Lenguaje principal:** Python (`.py`)
- **Ejemplos comparativos:** C++ (`acceso_aleatorio_cpp.cpp`) y comparativas con Java en la teoría
- **Nombres de archivos:** snake_case, descriptivos
- **Un archivo por ejercicio**
- **Dificultad escalada:** básico → intermedio → avanzado → experto

## Objetivo

Dominar cada tema a la perfección mediante rigor académico, rigor técnico y comprensión profunda. Al finalizar, cada tema debe poder explicarse y aplicarse sin ayuda.
