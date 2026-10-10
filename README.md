# TPA-2002 — Principios de Programación 2

Proyecto de aprendizaje y creación de ejercicios para dominar cada tema del curso a la perfección.

> **Autor:** Maikel Marín Brenes — [Vipermech](https://github.com/MaikelMarin)
>
> **Asistencia de IA:** Este proyecto fue creado con asistencia de inteligencia artificial (OpenCode). La IA colaboró en la creación de la estructura, la redacción de la documentación teórica, la implementación de los ejercicios y el desarrollo de la aplicación web. La dirección, los requisitos y las decisiones del proyecto son del autor.

---

## Cómo ejecutar la página web

El proyecto incluye una aplicación web para explorar todo el contenido (teoría y 93 ejercicios) de forma visual e interactiva. **No requiere instalación de dependencias**: es HTML, CSS y JavaScript puro.

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

Listo. Ya puedes navegar por las 6 temáticas.

> **Importante:** abre la URL con `/web/` al final. El servidor se levanta desde la **raíz del proyecto**, no desde la carpeta `web/`. Si lo levantas desde dentro de `web/`, el contenido no cargará.

### Si el puerto 8080 está ocupado

Usa otro puerto cualquiera:

```bash
python -m http.server 3000
```

Y entra a `http://localhost:3000/web/`.

### ¿Por qué hace falta un servidor?

La página lee los archivos `.md` y `.py` para mostrarlos. Los navegadores **bloquean** esa lectura si abres `index.html` con doble clic (protocolo `file://`), por seguridad. Un servidor local lo resuelve.

### Alternativa sin terminal

Si prefieres no usar la terminal, cualquier servidor estático funciona. Por ejemplo con Node.js:

```bash
npx serve .
```

O con la extensión **Live Server** de VS Code: abre `web/index.html`, clic derecho → *Open with Live Server*.

---

## Qué ofrece la página

| Función | Descripción |
|---------|-------------|
| Navegación | 6 temáticas y 93 documentos organizados en árbol |
| Búsqueda | Busca por nombre, insensible a acentos (`teoria` encuentra `Teoría`). Atajo: tecla `/` |
| Temas | Modo oscuro y claro; se recuerda tu elección |
| Teoría | Markdown renderizado: tablas, código con resaltado, citas |
| Código | Resaltado de sintaxis para Python y C++, con botón de copiar |
| Progreso | Marca los documentos que ya leíste |
| Atajos | Flechas `←` `→` para moverte entre documentos |

---

## Estructura del proyecto

```
Progra 2/
├── README.md                          ← Este archivo
├── contenido.json                     ← Manifiesto de contenido (lo usa la web)
├── web/                               ← Aplicación web (HTML + CSS + JS puro)
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
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
| `README.md` | Temas, contenido categorizado y lista de ejercicios |
| `teoria.md` | Documento teórico detallado con bibliografía |
| `ejercicios/` | Solución de cada ejercicio (un archivo por problema) |

## Ejecutar los ejercicios

Cada ejercicio es un archivo independiente con sus propias pruebas:

```bash
python 01-recursividad/ejercicios/factorial.py
```

También puedes correr todos los ejercicios de una temática:

```bash
for f in 01-recursividad/ejercicios/*.py; do python "$f"; done
```

---

## Nota sobre los archivos excluidos

Este repositorio **no incluye** (ver `.gitignore`):

- `public_TPA-2002_Principios_de_Programación_2.pdf` y `public_Cronograma_...pdf` — son propiedad del **Tecnológico de Costa Rica**. Se usaron como fuente de verdad para definir los contenidos, pero no se redistribuyen.
- Configuración local de agentes (`.agents/`, `AGENTS.md`, `skills-lock.json`, `SKILL.md`).

## Convenciones

- **Lenguaje principal:** Python (`.py`)
- **Ejemplos comparativos:** Java (`.java`) y C++ (`.cpp`)
- **Nombres de archivos:** snake_case, descriptivos
- **Un archivo por ejercicio**
- **Dificultad escalada:** básico → intermedio → avanzado → experto

## Objetivo

Dominar cada tema a la perfección mediante rigor académico, rigor técnico y comprensión profunda. Al finalizar, cada tema debe poder explicarse y aplicarse sin ayuda.
