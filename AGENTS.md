# AGENTS.md

## Repositorio

Espacio de estudio del curso **TPA-2002 – Principios de Programación 2** (Tecnológico de Costa Rica, Técnico en Desarrollo de Aplicaciones de Software).

Proyecto de aprendizaje y creación de ejercicios y problemas para dominar cada tema a la perfección. No hay build, tests, lint, CI ni manifiestos de paquetes.

## Objetivo académico

Cada tema debe dominarse a la perfección mediante:
- **Rigor académico:** fundamentos teóricos sólidos, no solo código que funciona.
- **Rigor técnico:** implementaciones correctas, eficientes y bien documentadas.
- **Comprensión profunda:** entender el porqué de cada algoritmo, su evolución histórica, sus trade-offs y sus casos de uso.
- **Dominio completo:** al finalizar este proyecto, cada tema debe poder explicarse y aplicarse sin ayuda.

## Estructura del repositorio

```
Progra 2/
├── AGENTS.md                          ← Este archivo
├── README.md                          ← Explicación general del proyecto y estructura
├── public_TPA-2002_...pdf             ← Programa del curso (fuente de verdad)
├── public_Cronograma_...pdf           ← Cronograma semanal
│
├── 01-recursividad/
│   ├── README.md                      ← Temas, contenido categorizado, lista de ejercicios y ubicación de soluciones
│   ├── teoria.md                      ← Información teórica con bibliografía y recursos utilizados
│   └── ejercicios/
│       ├── factorial.py
│       ├── fibonacci.py
│       ├── fibonacci_memo.py
│       ├── potencia.py
│       ├── suma_lista.py
│       ├── lista_anidada.py
│       ├── burbuja.py
│       ├── seleccion.py
│       ├── insercion.py
│       ├── quick_sort.py
│       ├── merge_sort.py
│       ├── busqueda_lineal.py
│       ├── busqueda_binaria.py
│       ├── n_reinas.py
│       ├── torres_hanoi.py
│       ├── permutaciones.py
│       ├── knapsack.py
│       ├── quick_sort_inplace.py
│       ├── merge_sort_lista_enlazada.py
│       ├── fibonacci_bottom_up.py
│       ├── binaria_rotada.py
│       └── palindromo.py
│
├── 02-ordenamiento-y-busqueda/
│   ├── README.md
│   ├── teoria.md
│   └── ejercicios/
│       ├── burbuja.py
│       ├── seleccion.py
│       ├── insercion.py
│       ├── quick_sort.py
│       ├── merge_sort.py
│       ├── busqueda_lineal.py
│       ├── busqueda_binaria.py
│       ├── quick_sort_inplace.py
│       ├── merge_sort_lista_enlazada.py
│       ├── binaria_rotada.py
│       └── ordenamiento_hibrido.py
│
├── 03-árboles/
│   ├── README.md
│   ├── teoria.md
│   └── ejercicios/
│       ├── nodo_y_arbol.py
│       ├── recorridos.py
│       ├── contar_nodos.py
│       ├── altura_arbol.py
│       ├── buscar_bst.py
│       ├── insertar_bst.py
│       ├── eliminar_bst.py
│       ├── es_bst_valido.py
│       ├── min_max_bst.py
│       ├── inorden_iterativo.py
│       ├── arboles_identicos.py
│       ├── es_balanceado.py
│       ├── postorden_iterativo.py
│       ├── lca_bst.py
│       ├── iterador_bst.py
│       ├── arbol_avl.py
│       ├── bst_a_lista_enlazada.py
│       ├── arbol_expresiones.py
│       ├── k_esimo_menor.py
│       └── serializar_bst.py
│
├── 04-grafos/
│   ├── README.md
│   ├── teoria.md
│   └── ejercicios/
│       ├── grafo_adyacencia.py
│       ├── grafo_matriz.py
│       ├── bfs_iterativo.py
│       ├── dfs_iterativo.py
│       ├── dfs_recursivo.py
│       ├── detectar_ciclos.py
│       ├── camino_minimo_bfs.py
│       ├── copiar_binario.py
│       ├── csv_a_diccionario.py
│       ├── dijkstra.py
│       ├── es_bipartito.py
│       ├── run_length_encoding.py
│       ├── sistema_logs.py
│       ├── grafo_dirigido_ciclos.py
│       ├── kruskal.py
│       ├── prim.py
│       ├── sistema_archivos_simple.py
│       └── json_a_grafo.py
│
├── 05-archivos/
│   ├── README.md
│   ├── teoria.md
│   └── ejercicios/
│       ├── leer_texto.py
│       ├── escribir_texto.py
│       ├── leer_linea_por_linea.py
│       ├── anadir_texto.py
│       ├── escritura_binaria.py
│       ├── lectura_binaria.py
│       ├── acceso_secuencial.py
│       ├── acceso_aleatorio.py
│       ├── contar_lineas_palabras.py
│       ├── copiar_binario.py
│       ├── csv_a_diccionario.py
│       ├── run_length_encoding.py
│       ├── sistema_logs.py
│       ├── acceso_aleatorio_cpp.cpp
│       └── sistema_archivos_simple.py
│
└── 06-grandes-datos/
    ├── README.md
    ├── teoria.md
    ├── ejercicios/
    │   ├── ejercicio1_generacion_masiva.py
    │   ├── ejercicio2_analisis_ventas.py
    │   └── ejercicio3_ordenamiento_externo.py
    └── soluciones/
        ├── solucion1_generacion_masiva.py
        ├── solucion2_analisis_ventas.py
        └── solucion3_ordenamiento_externo.py
```

## Convenciones

- **Lenguaje principal:** Python (extensión `.py`)
- **Ejemplos comparativos:** Java (`.java`) y C++ (`.cpp`) cuando ayuden a entender la evolución de un concepto
- **Nombres de archivos:** snake_case, descriptivos del ejercicio que resuelven
- **Un archivo por ejercicio:** cada problema es un archivo separado
- **Dificultad escalada:** cada tema cubre ejercicios de nivel básico, intermedio, avanzado y experto

## Fuentes de verdad

- `public_TPA-2002_Principios_de_Programación_2.pdf` — Programa del curso: competencias, contenidos, metodología y bibliografía.
- `public_Cronograma_Principios_de_Programación_2.pdf` — Cronograma semanal con evaluaciones.
- Papers científicos, académicos o información de referentes del mundo tech.

## Trabajo esperado

- Crear y resolver ejercicios de programación en **Python** como lenguaje principal.
- Incluir ejemplos comparativos en **Java** y **C++** cuando ayude a entender la evolución de cada concepto.
- Los ejercicios deben escalar en dificultad (básico → intermedio → avanzado → experto).
- Cada tema debe tener un documento teórico (`teoria.md`) con su respectivo apartado de bibliografía y recursos utilizados.
- Los documentos deben ser detallados y demostrar dominio del tema.
- Seguir una estructura y formato consistentes en todos los archivos.

## Cómo investigar

Fuentes de mayor valor primero:
- Los PDFs raíz del curso y cualquier manifiesto o configuración del workspace
- Config de build, test, lint, typecheck, CI, pre-commit, task runners (si existen)
- Archivos de instrucción existentes (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, `.opencode/`)
- Si la arquitectura no es clara tras leer config y docs, inspeccionar archivos representativos
- Historia, evolución y actualidad de la temática: indagar en recursos externos que sean fuentes confiables y veraces (papers de investigadores, artículos de líderes del mundo tech, entre otros)
- Guardar la fuente de donde se toma el conocimiento y adjuntarla al final de cada temática como recursos utilizados

Fuentes ejecutables sobre prosa. Si hay conflicto, confiar en el código.

## Qué extraer

- Estructurar la información de forma clara y jerárquica
- Información detallada que demuestre dominio del tema
- Comandos exactos del desarrollo, especialmente los no obvios
- Cómo correr un test o verificación puntual
- Orden de comandos cuando importa
- Convenciones que difieren de los defaults del lenguaje o framework
- Gotchas de setup, entorno o lenguaje de programación

## Qué excluir

- Fuentes no reconocidas o comprobadas
- Información genérica que no aporte al dominio del tema
- Contenido que pueda verificarse directamente en el código o los PDFs

En duda, preguntar.
