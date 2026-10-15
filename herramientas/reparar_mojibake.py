#!/usr/bin/env python3
"""
Repara el mojibake (vocales acentuadas perdidas) en docstrings,
comentarios y archivos Markdown.

NO toca identificadores ni cdigo ejecutable: usa tokenize para
modificar solo tokens STRING y COMMENT en archivos .py.

Uso:
    python3 herramientas/reparar_mojibake.py --verificar
    python3 herramientas/reparar_mojibake.py --aplicar
"""
import io
import os
import re
import sys
import tokenize

# Paquete: palabra corrupta -> forma correcta.
# SOLO se incluyen palabras que NO existen en espanol sin tilde, para
# no corromper identificadores de codigo.
CORRECCIONES = {
    'arbol': 'árbol',
    'arboles': 'árboles',
    'subarbol': 'subárbol',
    'subarboles': 'subárboles',
    'solucin': 'solución',
    'soluciones': 'soluciones',       # ya correcta, se ignora
    'vlido': 'válido',
    'vlida': 'válida',
    'vlidos': 'válidos',
    'vlidas': 'válidas',
    'numero': 'número',
    'numeros': 'números',
    'posicin': 'posición',
    'versin': 'versión',
    'direccin': 'dirección',
    'seccin': 'sección',
    'produccin': 'producción',
    'operacin': 'operación',
    'analisis': 'análisis',
    'clasico': 'clásico',
    'clasicos': 'clásicos',
    'construccin': 'construcción',
    'verificacin': 'verificación',
    'repeticin': 'repetición',
    'funcin': 'función',
    'funciones': 'funciones',          # ya correcta
    'precisin': 'precisión',
    'mtodo': 'método',
    'mtodos': 'métodos',
    'aplicacin': 'aplicación',
    'traduccin': 'traducción',
    'clculo': 'cálculo',
    'ultimo': 'último',
    'unico': 'único',
    'unica': 'única',
    'unicos': 'únicos',
    'hipotesis': 'hipótesis',
    'topologico': 'topológico',
    'topologica': 'topológica',
    'eficiencia': 'eficiencia',       # ya correcta, se ignora
    'pblicos': 'públicos',
    'pblico': 'público',
    'monitorizacin': 'monitorización',
    'posibles': 'posibles',           # ya correcta
    'rpidamente': 'rápidamente',
    'rpido': 'rápido',
    'rpida': 'rápida',
    'dndoe': 'dónde',
    'cmo': 'cómo',
    'cuntos': 'cuántos',
    'cunto': 'cuánto',
    'detrs': 'detrás',
    'tras': 'tras',                   # ya correcta
    'adems': 'además',
    'despus': 'después',
    'tipos': 'tipos',                 # ya correcta
    'inicio': 'inicio',               # ya correcta
    'arbol': 'árbol',                 # refuerzo
    'optimizacin': 'optimización',
    'comprobacin': 'comprobación',
    'indexacin': 'indexación',
    'bsqueda': 'búsqueda',
    'bsquedas': 'búsquedas',
    'prctico': 'práctico',
    'prctica': 'práctica',
    'terico': 'teórico',
    'terica': 'teórica',
    'tcnicos': 'técnicos',
    'tcnico': 'técnico',
    'especfico': 'específico',
    'especfica': 'específica',
    'automtico': 'automático',
    'automtica': 'automática',
    'bsico': 'básico',
    'bsica': 'básica',
    'crtico': 'crítico',
    'crtica': 'crítica',
    'mnimo': 'mínimo',
    'mnima': 'mínima',
    'mximo': 'máximo',
    'mxima': 'máxima',
    'ptimo': 'óptimo',
    'ptima': 'óptima',
    'proporcin': 'proporción',
    'razonamiento': 'razonamiento',   # ya correcta
    'diseño': 'diseño',               # ya correcta (no lleva tilde)
}

# Palabra -> regex con fronteras de palabra
REGEX_CORRECCIONES = {
    mala: re.compile(r'\b' + re.escape(mala) + r'\b')
    for mala in CORRECCIONES
    if CORRECCIONES[mala] != mala       # descartar identidades
}


def aplicar_correcciones(texto):
    """Reemplaza palabras corruptas por su forma correcta."""
    if not texto:
        return texto, 0
    cambios = 0
    for mala, patron in REGEX_CORRECCIONES.items():
        texto, n = patron.subn(CORRECCIONES[mala], texto)
        cambios += n
    return texto, cambios


def reparar_python(ruta):
    """Repara solo strings y comentarios de un archivo .py.

    Usa tokenize para no tocar identificadores ni codigo ejecutable.
    Devuelve (modificado, num_cambios).
    """
    with open(ruta, encoding='utf-8') as f:
        original = f.read()

    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(original).readline))
    except (tokenize.TokenError, IndentationError):
        return 0, 0                        # archivo ilegible: no tocar

    # Mapa offset(absoluto) -> token, para reconstruir sin perder nada
    offsets = []
    pos = 0
    for linea in original.splitlines(keepends=True):
        offsets.append(pos)
        pos += len(linea)

    def offset(linea, col):
        if 1 <= linea <= len(offsets):
            return offsets[linea - 1] + col
        return len(original)

    partes = []
    ultimo = 0
    cambios = 0

    for tok in tokens:
        if tok.type not in (tokenize.STRING, tokenize.COMMENT):
            continue
        nuevo_texto, n = aplicar_correcciones(tok.string)
        if n == 0:
            continue
        inicio_tok = offset(*tok.start)
        fin_tok = offset(*tok.end)
        partes.append(original[ultimo:inicio_tok])
        partes.append(nuevo_texto)
        ultimo = fin_tok
        cambios += n

    if not partes:
        return 0, 0

    partes.append(original[ultimo:])
    nuevo_contenido = ''.join(partes)

    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(nuevo_contenido)

    return 1, cambios


def reparar_markdown(ruta):
    """Repara un archivo Markdown completo (es pura prosa)."""
    with open(ruta, encoding='utf-8') as f:
        original = f.read()
    nuevo, cambios = aplicar_correcciones(original)
    if nuevo != original:
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(nuevo)
        return 1, cambios
    return 0, 0


def main():
    aplicar = '--aplicar' in sys.argv
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    archivos_py = 0
    archivos_md = 0
    total_cambios = 0

    for raiz, dirs, archivos in os.walk(base):
        if '.git' in raiz or 'herramientas' in raiz:
            continue
        for nombre in sorted(archivos):
            ruta = os.path.join(raiz, nombre)
            if nombre.endswith('.py'):
                if aplicar:
                    modificado, cambios = reparar_python(ruta)
                else:
                    with open(ruta, encoding='utf-8') as f:
                        contenido = f.read()
                    _, cambios = aplicar_correcciones(contenido)
                    modificado = 1 if cambios else 0
                if cambios:
                    archivos_py += modificado
                    total_cambios += cambios
                    print(f"  {cambios:3d}  {os.path.relpath(ruta, base)}")
            elif nombre.endswith('.md'):
                if aplicar:
                    modificado, cambios = reparar_markdown(ruta)
                else:
                    with open(ruta, encoding='utf-8') as f:
                        contenido = f.read()
                    _, cambios = aplicar_correcciones(contenido)
                    modificado = 1 if cambios else 0
                if cambios:
                    archivos_md += modificado
                    total_cambios += cambios
                    print(f"  {cambios:3d}  {os.path.relpath(ruta, base)}")

    print(f"\nArchivos .py con mojibake: {archivos_py}")
    print(f"Archivos .md con mojibake: {archivos_md}")
    print(f"Total de palabras a reparar: {total_cambios}")
    print(f"Modo: {'APLICAR' if aplicar else 'VERIFICAR (sin escribir)'}")


if __name__ == '__main__':
    main()
