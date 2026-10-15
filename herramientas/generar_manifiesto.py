#!/usr/bin/env python3
"""
Genera contenido.json con ndice de bsqueda por contenido.

Cada entrada del manifiesto gana un campo `keywords`: las palabras ms
relevantes extradas del contenido real del archivo. Esto permite
buscar por conceptos ("backtracking", "poda") aunque no aparezcan en
el nombre del archivo ni en el ttulo del tema.

Uso:
    python3 herramientas/generar_manifiesto.py
"""
import json
import os
import re
import unicodedata
from collections import Counter

# Palabras vacas en espaol. Se descartan porque aparecen en casi todos
# los archivos y no ayudan a distinguirlos.
STOPWORDS = set("""
para como pero sus esa ese eso estos estas este esta los las una unos unas del con sin por que
cual cuando donde quien porque si nos ya muy mas les algo nada tanto tanto cada otro otra otros
otras entre desde hasta sobre tras segun sea sean siendo sido eran eran hay han habia haber
hace hacen hacer hizo pueden podemos puede podria deben debemos debe deberia tiene tienen
tener tengo tenemos tenia tenian donde ademas asi aunque entonces mientras tanto pues como
cual cuales cuyo cuya cuyos cuyas cuyo esto aquel aquella aquellos aquellas
""".split())

# Palabras propias del andamiaje del proyecto: son frecuentes en todos
# los archivos y tampoco discriminan.
STOPWORDS_TECNICAS = set("""
ejercicio ejercicios solucion soluciones problema problemas ver ver() return return()
test tests assert self none true false print def class import from with open file archivo
archivos >>> todo todas todos este esta estas estos
""".split())


def normalizar(texto):
    """Minusculas y sin diacriticos, para que 'backtracking' == 'backtracking'."""
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto.lower()


def extraer_palabras(texto, minimo=5):
    """Extrae palabras significativas de un texto."""
    texto = normalizar(texto)
    # Separar por cualquier cosa que no sea letra o numero
    palabras = re.findall(r'[a-z][a-z0-9_]{%d,}' % (minimo - 1), texto)
    return [p for p in palabras
            if p not in STOPWORDS and p not in STOPWORDS_TECNICAS]


def es_identificador(palabra):
    """True si la palabra parece un identificador de codigo."""
    if '_' in palabra:                    # resolver_sudoku, es_valido
        return True
    if palabra.isdigit():
        return True
    if len(palabra) > 15:                 # nombres largos de variables
        return True
    return False


def palabras_clave(contenido, tope=40):
    """Las N palabras ms frecuentes y distintivas del contenido.

    Se descartan identificadores de codigo: no ayudan a buscar
    conceptos y engordan el manifiesto.
    """
    palabras = [p for p in extraer_palabras(contenido) if not es_identificador(p)]
    if not palabras:
        return []
    conteo = Counter(palabras)
    # Priorizar por frecuencia, luego alfabetico para ser determinista
    ordenadas = sorted(conteo.items(), key=lambda kv: (-kv[1], kv[0]))
    return [palabra for palabra, _ in ordenadas[:tope]]


def primera_linea_util(contenido):
    """Primera lnea no vacia del archivo (suele ser el ttulo)."""
    for linea in contenido.split('\n'):
        linea = linea.strip().strip('"').strip("'").strip('#').strip()
        if linea and not linea.startswith(('"""', "'''", '-', '=', '/', '*')):
            if len(linea) > 3:
                return linea[:120]
    return ''


def generar(base):
    """Construye el manifiesto completo con keywords por archivo."""
    iconos = {'00': '📚', '01': '🔄', '02': '📊', '03': '🌳',
              '04': '🕸️', '05': '📁', '06': '💾'}
    nombres = {'00': 'Fundamentos'}

    topics = []
    for carpeta in sorted(os.listdir(base)):
        ruta_carpeta = os.path.join(base, carpeta)
        if not os.path.isdir(ruta_carpeta) or not carpeta[0].isdigit():
            continue

        num, slug = carpeta.split('-', 1)
        topic = {
            'id': carpeta,
            'title': nombres.get(num, slug.replace('-', ' ').title()),
            'icon': iconos.get(num, '📦'),
            'files': []
        }

        # Archivos propios del tema (README y teoria)
        for nombre, tipo in [('README.md', 'readme'), ('teoria.md', 'teoria')]:
            ruta = os.path.join(ruta_carpeta, nombre)
            if os.path.exists(ruta):
                with open(ruta, encoding='utf-8') as f:
                    contenido = f.read()
                topic['files'].append({
                    'name': 'Índice' if tipo == 'readme' else 'Teoría',
                    'path': f'{carpeta}/{nombre}',
                    'type': tipo,
                    'keywords': palabras_clave(contenido)
                })

        # Ejercicios y soluciones
        for sub in ['ejercicios', 'soluciones']:
            ruta_sub = os.path.join(ruta_carpeta, sub)
            if not os.path.isdir(ruta_sub):
                continue
            for nombre in sorted(os.listdir(ruta_sub)):
                ruta = os.path.join(ruta_sub, nombre)
                # FIX: solo archivos reales (evita __pycache__)
                if not os.path.isfile(ruta) or nombre.startswith('.'):
                    continue
                with open(ruta, encoding='utf-8', errors='replace') as f:
                    contenido = f.read()
                topic['files'].append({
                    'name': nombre.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title(),
                    'path': f'{carpeta}/{sub}/{nombre}',
                    'type': 'ejercicio' if sub == 'ejercicios' else 'solucion',
                    'ext': nombre.rsplit('.', 1)[1] if '.' in nombre else '',
                    'keywords': palabras_clave(contenido)
                })

        topics.append(topic)

    return topics


if __name__ == '__main__':
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    topics = generar(base)

    salida = os.path.join(base, 'contenido.json')
    with open(salida, 'w', encoding='utf-8') as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)

    total = sum(len(t['files']) for t in topics)
    print(f'Manifiesto generado: {salida}')
    print(f'  Temas:   {len(topics)}')
    print(f'  Archivos: {total}')

    # Verificacin automtica del ndice
    print('\nVerificacin del ndice de bsqueda:')
    pruebas = {
        'back': ['subconjuntos', 'laberinto', 'sudoku', 'coloreo'],
        'poda': [],
        'recursividad': [],
        'dijkstra': [],
    }
    for termino, esperados in pruebas.items():
        encontrados = [
            f['path'] for t in topics for f in t['files']
            if termino in ' '.join(f.get('keywords', [])).lower()
            or termino in normalizar(f['name'])
            or termino in normalizar(t['title'])
        ]
        ok = '✓' if encontrados else '✗'
        print(f'  {ok} "{termino}" → {len(encontrados)} archivos')
        for ruta in esperados:
            coincide = any(ruta in e for e in encontrados)
            print(f'     {"✓" if coincide else "✗"} {ruta}')
        if not encontrados:
            raise SystemExit(f'FALLO: "{termino}" no encontr nada')

    print('\nndice verificado.')
