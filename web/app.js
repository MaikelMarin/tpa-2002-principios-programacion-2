/* ============================================
   TPA-2002 — Principios de Programación 2
   Lógica de la aplicación
   ============================================ */
'use strict';


/* ===== ESTADO ===== */
const estado = {
    topics: [],
    items: [],        // todos los documentos planos
    actual: -1,       // índice del documento visible
    leidos: new Set(JSON.parse(localStorage.getItem('leidos') || '[]')),
    busquedaSel: -1
};

/* ===== UTILIDADES ===== */
const $ = (sel) => document.querySelector(sel);
const el = (tag, cls, html) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html !== undefined) n.innerHTML = html;
    return n;
};

function toast(msg) {
    const t = $('#toast');
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(t._timer);
    t._timer = setTimeout(() => t.classList.remove('show'), 2200);
}

function escapar(texto) {
    return texto
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

/* ===== RESALTADO DE SINTAXIS ===== */
const PALABRAS_PY = new Set(['def', 'return', 'if', 'elif', 'else', 'for', 'while', 'in', 'not', 'and', 'or', 'is', 'import', 'from', 'as', 'class', 'try', 'except', 'finally', 'raise', 'with', 'lambda', 'yield', 'global', 'nonlocal', 'pass', 'break', 'continue', 'assert', 'del', 'True', 'False', 'None']);
const PALABRAS_CPP = new Set(['int', 'void', 'float', 'double', 'char', 'bool', 'if', 'else', 'for', 'while', 'return', 'class', 'struct', 'public', 'private', 'protected', 'using', 'namespace', 'std', 'const', 'static', 'new', 'delete', 'true', 'false', 'nullptr', 'include', 'template', 'typename', 'virtual', 'override']);
const BUILTINS = new Set(['print', 'len', 'range', 'int', 'float', 'str', 'list', 'dict', 'set', 'tuple', 'sorted', 'enumerate', 'zip', 'sum', 'min', 'max', 'abs', 'type', 'isinstance', 'map', 'filter', 'open', 'cout', 'cin', 'endl', 'string', 'vector', 'main']);

function resaltar(codigo, lang) {
    const claves = lang === 'cpp' ? PALABRAS_CPP : PALABRAS_PY;

    // Tokenizador de una sola pasada: evita conflictos entre patrones
    const PATRON = new RegExp([
        '(#[^\\n]*)',                                                        // 1 comentario
        '(\\/\\/[^\\n]*)',                                                   // 2 comentario línea
        '(\\/\\*[\\s\\S]*?\\*\\/)',                                          // 3 comentario bloque
        '("""[\\s\\S]*?"""|\'\'\'[\\s\\S]*?\'\'\')',                         // 4 docstring
        '("(?:\\\\.|[^"\\\\\\n])*"|\'(?:\\\\.|[^\'\\\\\\n])*\')',           // 5 cadena
        '(@[A-Za-z_]\\w*)',                                                  // 6 decorador
        '\\b(\\d+\\.?\\d*)\\b',                                              // 7 número
        '\\b([A-Za-z_]\\w*)\\b'                                              // 8 palabra
    ].join('|'), 'g');

    let salida = '';
    let ultimo = 0;
    let m;

    while ((m = PATRON.exec(codigo)) !== null) {
        // Texto previo sin token
        salida += escapar(codigo.slice(ultimo, m.index));
        ultimo = m.index + m[0].length;

        const [texto] = m;
        let cls = null;

        if (m[1] !== undefined || m[2] !== undefined || m[3] !== undefined) {
            cls = 'tok-com';
        } else if (m[4] !== undefined || m[5] !== undefined) {
            cls = 'tok-str';
        } else if (m[6] !== undefined) {
            cls = 'tok-dec';
        } else if (m[7] !== undefined) {
            cls = 'tok-num';
        } else if (m[8] !== undefined) {
            if (claves.has(texto)) cls = 'tok-kw';
            else if (BUILTINS.has(texto)) cls = 'tok-fun';
        }

        salida += cls ? `<span class="${cls}">${escapar(texto)}</span>` : escapar(texto);
    }

    salida += escapar(codigo.slice(ultimo));
    return salida;
}

/* ===== RENDERIZADOR MARKDOWN ===== */
function renderMarkdown(md) {
    const lineas = md.split('\n');
    let html = '';
    let i = 0;

    while (i < lineas.length) {
        const linea = lineas[i];

        // Bloques de código
        const cerca = linea.match(/^```(\w*)\s*$/);
        if (cerca) {
            const lang = cerca[1] || '';
            const cuerpo = [];
            i++;
            while (i < lineas.length && !/^```\s*$/.test(lineas[i])) {
                cuerpo.push(lineas[i]);
                i++;
            }
            i++; // cerrar ```
            html += bloqueCodigo(cuerpo.join('\n'), lang);
            continue;
        }

        // Encabezados
        const enc = linea.match(/^(#{1,6})\s+(.*)$/);
        if (enc) {
            const nivel = enc[1].length;
            html += `<h${nivel}>${enLinea(enc[2])}</h${nivel}>`;
            i++;
            continue;
        }

        // Línea horizontal
        if (/^(-{3,}|\*{3,}|_{3,})\s*$/.test(linea)) {
            html += '<hr>';
            i++;
            continue;
        }

        // Tabla
        if (linea.includes('|') && i + 1 < lineas.length && /^\s*\|?[\s:|-]+\|/.test(lineas[i + 1])) {
            const filas = [];
            while (i < lineas.length && lineas[i].includes('|')) {
                filas.push(lineas[i]);
                i++;
            }
            html += tabla(filas);
            continue;
        }

        // Lista
        if (/^\s*[-*+]\s+/.test(linea)) {
            const items = [];
            while (i < lineas.length && /^\s*[-*+]\s+/.test(lineas[i])) {
                items.push(lineas[i].replace(/^\s*[-*+]\s+/, ''));
                i++;
            }
            html += `<ul>${items.map((x) => `<li>${enLinea(x)}</li>`).join('')}</ul>`;
            continue;
        }
        if (/^\s*\d+\.\s+/.test(linea)) {
            const items = [];
            while (i < lineas.length && /^\s*\d+\.\s+/.test(lineas[i])) {
                items.push(lineas[i].replace(/^\s*\d+\.\s+/, ''));
                i++;
            }
            html += `<ol>${items.map((x) => `<li>${enLinea(x)}</li>`).join('')}</ol>`;
            continue;
        }

        // Bloque de cita
        if (/^>\s?/.test(linea)) {
            const cuerpo = [];
            while (i < lineas.length && /^>\s?/.test(lineas[i])) {
                cuerpo.push(lineas[i].replace(/^>\s?/, ''));
                i++;
            }
            html += `<blockquote>${enLinea(cuerpo.join('<br>'))}</blockquote>`;
            continue;
        }

        // Párrafo normal
        if (linea.trim() === '') {
            i++;
            continue;
        }
        const parrafo = [];
        while (
            i < lineas.length &&
            lineas[i].trim() !== '' &&
            !/^(#{1,6}\s|```|\s*[-*+]\s|\s*\d+\.\s|>\s?)/.test(lineas[i]) &&
            !/^(-{3,}|\*{3,}|_{3,})\s*$/.test(lineas[i]) &&
            !(lineas[i].includes('|') && i + 1 < lineas.length && /^\s*\|?[\s:|-]+\|/.test(lineas[i + 1]))
        ) {
            parrafo.push(lineas[i]);
            i++;
        }
        html += `<p>${enLinea(parrafo.join(' '))}</p>`;
    }

    return html;
}

function enLinea(texto) {
    return escapar(texto)
        .replace(/`([^`]+)`/g, '<code class="inline">$1</code>')
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>')
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
}

function bloqueCodigo(codigo, lang) {
    const nombreLang = lang === 'cpp' ? 'C++' : (lang === 'python' ? 'Python' : lang.toUpperCase());
    const clases = lang === 'cpp' ? 'language-cpp' : 'language-python';
    return `<div class="code-block">
        <div class="code-head">
            <span class="code-lang">${nombreLang}</span>
            <button class="code-copy" data-copy="1">Copiar</button>
        </div>
        <pre><code class="${clases}">${resaltar(codigo, lang)}</code></pre>
    </div>`;
}

function tabla(filas) {
    const limpiar = (celda) => celda.trim().replace(/^\||\|$/g, '').trim();
    const celdas = filas.map((f) => f.split('|').map(limpiar).filter((c) => c !== '' || f.split('|').length > 2));
    const cabeza = celdas[0].filter((c) => c !== '');
    const cuerpo = celdas.slice(2);
    let html = '<div class="table-wrap"><table><thead><tr>';
    for (const c of cabeza) html += `<th>${enLinea(c)}</th>`;
    html += '</tr></thead><tbody>';
    for (const fila of cuerpo) {
        const celdasFila = fila.filter((c) => c !== '');
        if (!celdasFila.length) continue;
        html += '<tr>';
        for (const c of celdasFila) html += `<td>${enLinea(c)}</td>`;
        html += '</tr>';
    }
    html += '</tbody></table></div>';
    return html;
}

/* ===== CARGA DE DATOS ===== */
async function cargarContenido() {
    let topics;
    try {
        const resp = await fetch('../contenido.json');
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        topics = await resp.json();
    } catch (err) {
        console.error('No se pudo cargar contenido.json', err);
        $('#sidebar-nav').innerHTML = '<div class="sidebar-loading">Error al cargar el contenido</div>';
        return;
    }

    // Endurecer las rutas de contenido
    const contenido = topics.map((t) => ({
        ...t,
        files: t.files.map((f) => ({ ...f, path: '../' + f.path }))
    }));

    estado.topics = contenido;

    let orden = 0;
    for (const topic of contenido) {
        for (const file of topic.files) {
            estado.items.push({
                ...file,
                topic: topic.title,
                topicId: topic.id,
                icon: topic.icon,
                orden: orden++
            });
        }
    }

    armarBarraLateral();
    armarBuscador();
    actualizarProgreso();
    actualizarEstadisticas();
    abrirDesdeHash();
}

/* ===== BARRA LATERAL ===== */
function armarBarraLateral() {
    const nav = $('#sidebar-nav');
    nav.innerHTML = '';

    // Botón de bienvenida
    const grupoInicio = el('div', 'topic-group open');
    const btnInicio = el('button', 'topic-head');
    btnInicio.innerHTML = `<span class="topic-icon">🏠</span><span class="topic-name">Inicio</span>`;
    btnInicio.addEventListener('click', () => mostrarBienvenida());
    grupoInicio.appendChild(btnInicio);
    nav.appendChild(grupoInicio);

    for (const topic of estado.topics) {
        const grupo = el('div', 'topic-group');
        const head = el('button', 'topic-head');
        head.innerHTML = `
            <span class="topic-icon">${topic.icon}</span>
            <span class="topic-name">${escapar(topic.title)}</span>
            <span class="topic-count">${topic.files.length}</span>
            <svg class="topic-chevron" viewBox="0 0 24 24" width="14" height="14"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>`;

        head.addEventListener('click', () => grupo.classList.toggle('open'));

        const lista = el('div', 'topic-files');
        for (const file of topic.files) {
            const item = estado.items.find((x) => x.path === file.path);
            const btn = el('button', 'file-link');
            btn.dataset.path = file.path;
            const nombreCorto = file.name.length > 30 ? file.name.slice(0, 30) + '…' : file.name;
            btn.innerHTML = `
                <span class="file-dot"></span>
                <span class="file-name" title="${escapar(file.name)}">${escapar(nombreCorto)}</span>
                ${file.ext ? `<span class="file-ext">${escapar(file.ext)}</span>` : ''}`;
            btn.addEventListener('click', () => abrirArchivo(item.orden));
            lista.appendChild(btn);
        }

        grupo.appendChild(head);
        grupo.appendChild(lista);
        nav.appendChild(grupo);
    }

    marcarLeidos();
}

function marcarLeidos() {
    document.querySelectorAll('.file-link').forEach((btn) => {
        const path = btn.dataset.path;
        btn.classList.toggle('read', estado.leidos.has(path));
    });
}

function marcarActivo() {
    document.querySelectorAll('.file-link').forEach((btn) => {
        const path = btn.dataset.path;
        btn.classList.toggle('active', estado.leidos.has(path) && estado.items[estado.actual]?.path === path);
    });
    const actual = estado.items[estado.actual];
    if (!actual) return;
    // Abrir el grupo del tema actual
    const enlaces = [...document.querySelectorAll('.file-link')];
    const activo = enlaces.find((b) => b.dataset.path === actual.path);
    if (activo) {
        activo.closest('.topic-group')?.classList.add('open');
        activo.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
    // Actualizar URL
    history.replaceState(null, '', '#doc=' + actual.path);
    if (estado.leidos.has(actual.path) === false) {
        estado.leidos.add(actual.path);
        localStorage.setItem('leidos', JSON.stringify([...estado.leidos]));
        actualizarProgreso();
        marcarLeidos();
    }
}

/* ===== ABRIR ARCHIVO ===== */
async function abrirArchivo(indice) {
    if (indice < 0 || indice >= estado.items.length) return;
    estado.actual = indice;
    const item = estado.items[indice];

    // Cambiar vistas
    $('#welcome').hidden = true;
    $('#doc-view').hidden = false;

    // Barra de herramientas del documento
    $('#breadcrumb').innerHTML = `
        <span class="breadcrumb-item">
            <span>${item.icon}</span>
            <button class="breadcrumb-link" data-tema="${escapar(item.topic)}">${escapar(item.topic)}</button>
        </span>
        <span class="breadcrumb-sep">/</span>
        <span class="breadcrumb-item breadcrumb-current">${escapar(item.name)}</span>`;
    $('#breadcrumb').querySelector('.breadcrumb-link')?.addEventListener('click', () => mostrarTema(item.topic));

    const etiquetas = { readme: 'Índice', teoria: 'Teoría', ejercicio: 'Ejercicio', solucion: 'Solución' };
    const badge = $('#doc-badge');
    badge.textContent = etiquetas[item.type] || item.type;
    badge.hidden = false;

    // Navegación anterior/siguiente
    $('#prev-doc').disabled = indice === 0;
    $('#next-doc').disabled = indice === estado.items.length - 1;
    if (indice > 0) $('#prev-name').textContent = estado.items[indice - 1].name;
    if (indice < estado.items.length - 1) $('#next-name').textContent = estado.items[indice + 1].name;

    // Cuerpo del documento
    const cuerpo = $('#doc-body');
    cuerpo.innerHTML = '<p class="cargando">Cargando documento…</p>';

    try {
        const resp = await fetch(item.path);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const texto = await resp.text();
        window.scrollTo({ top: 0, behavior: 'auto' });
        if (item.ext === 'py' || item.ext === 'cpp' || item.ext === 'java') {
            const lang = item.ext === 'py' ? 'python' : 'cpp';
            cuerpo.innerHTML = bloqueCodigo(texto, lang);
        } else {
            cuerpo.innerHTML = renderMarkdown(texto);
        }
    } catch (err) {
        cuerpo.innerHTML = `<blockquote>No se pudo cargar el archivo <code>${escapar(item.path)}</code>: ${escapar(err.message)}</blockquote>`;
    }

    marcarActivo();
    ligarCopiarCodigo();
    cerrarBarraLateralMovil();
}

/* ===== BIENVENIDA ===== */
function mostrarBienvenida() {
    $('#doc-view').hidden = true;
    $('#welcome').hidden = false;
    estado.actual = -1;
    history.replaceState(null, '', location.pathname);
    window.scrollTo({ top: 0, behavior: 'smooth' });
    marcarActivo();
}

function mostrarTema(titulo) {
    const topic = estado.topics.find((t) => t.title === titulo);
    if (!topic || !topic.files.length) return;
    const primero = estado.items.find((x) => x.path === topic.files[0].path);
    if (primero) abrirArchivo(primero.orden);
}

function actualizarEstadisticas() {
    const total = estado.items.length;
    const codigo = estado.items.filter((i) => i.ext === 'py' || i.ext === 'cpp').length;
    $('#stat-files').textContent = total;
    $('#stat-code').textContent = codigo;

    // Tarjetas de temas
    const grid = $('#topic-grid');
    grid.innerHTML = '';
    const descripciones = {
        'Recursividad': 'Fundamentos, backtracking, funciones recursivas clásicas y comparación con iteración.',
        'Ordenamiento Y Busqueda': 'Burbuja, selección, inserción, Quick Sort, Merge Sort, búsqueda binaria y lineal.',
        'Arboles': 'Árboles binarios, BST, AVL, recorridos y balanceo de árboles.',
        'Grafos': 'BFS, DFS, Dijkstra, Kruskal, Prim, ciclos y grafos bipartitos.',
        'Archivos': 'Lectura y escritura de archivos de texto y binarios, acceso secuencial y aleatorio.',
        'Grandes Datos': 'Procesamiento de grandes volúmenes de datos, ordenamiento externo y optimización.'
    };
    for (const topic of estado.topics) {
        const desc = descripciones[topic.title] || '';
        const tarjeta = el('button', 'topic-card');
        tarjeta.innerHTML = `
            <span class="topic-card-icon">${topic.icon}</span>
            <h3>${escapar(topic.title)}</h3>
            <p>${escapar(desc)}</p>
            <span class="topic-card-meta">${topic.files.length} documentos</span>`;
        tarjeta.addEventListener('click', () => mostrarTema(topic.title));
        grid.appendChild(tarjeta);
    }
}

/* ===== PROGRESO ===== */
function actualizarProgreso() {
    const leidos = estado.items.filter((i) => estado.leidos.has(i.path)).length;
    const total = estado.items.length || 1;
    $('#progress-count').textContent = `${leidos}/${estado.items.length}`;
    $('#progress-fill').style.width = `${(leidos / total) * 100}%`;
    marcarLeidos();
}

/* ===== BUSCADOR ===== */
function normalizar(texto) {
    return texto
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u030f]/g, '')  // quitar diacríticos
        .replace(/ñ/g, 'n');
}

function armarBuscador() {
    const input = $('#search-input');
    const resultados = $('#search-results');

    input.addEventListener('input', () => {
        const consulta = normalizar(input.value.trim());
        if (consulta.length < 1) {
            resultados.classList.remove('open');
            resultados.innerHTML = '';
            return;
        }
        const coincidencias = estado.items
            .filter((item) =>
                normalizar(item.name).includes(consulta) ||
                normalizar(item.topic).includes(consulta)
            )
            .slice(0, 12);

        resultados.innerHTML = '';
        if (!coincidencias.length) {
            resultados.innerHTML = '<div class="search-empty">Sin resultados</div>';
        } else {
            coincidencias.forEach((item, idx) => {
                const b = el('button', 'search-result' + (idx === 0 ? ' selected' : ''));
                b.innerHTML = `
                    <span class="search-result-icon">${item.icon}</span>
                    <span class="search-result-body">
                        <span class="search-result-name">${resaltarCoincidencia(item.name, input.value.trim())}</span>
                        <span class="search-result-topic">${escapar(item.topic)}</span>
                    </span>`;
                b.addEventListener('click', () => {
                    abrirArchivo(item.orden);
                    resultados.classList.remove('open');
                    input.value = '';
                });
                resultados.appendChild(b);
            });
        }
        resultados.classList.add('open');
        estado.busquedaSel = 0;
    });

    input.addEventListener('keydown', (e) => {
        const items = [...resultados.querySelectorAll('.search-result')];
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
            e.preventDefault();
            if (!items.length) return;
            estado.busquedaSel += e.key === 'ArrowDown' ? 1 : -1;
            if (estado.busquedaSel >= items.length) estado.busquedaSel = 0;
            if (estado.busquedaSel < 0) estado.busquedaSel = items.length - 1;
            items.forEach((b, i) => b.classList.toggle('selected', i === estado.busquedaSel));
        } else if (e.key === 'Enter') {
            e.preventDefault();
            const sel = items[estado.busquedaSel];
            if (sel) sel.click();
        } else if (e.key === 'Escape') {
            resultados.classList.remove('open');
            input.blur();
        }
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('#search-box')) resultados.classList.remove('open');
    });
}

function resaltarCoincidencia(nombre, consulta) {
    const idx = nombre.toLowerCase().indexOf(consulta);
    if (idx === -1) return escapar(nombre);
    return escapar(nombre.slice(0, idx)) +
        `<mark class="search-hit">${escapar(nombre.slice(idx, idx + consulta.length))}</mark>` +
        escapar(nombre.slice(idx + consulta.length));
}

/* ===== COPIAR CÓDIGO ===== */
function ligarCopiarCodigo() {
    document.querySelectorAll('.code-copy').forEach((btn) => {
        if (btn._ligado) return;
        btn._ligado = true;
        btn.addEventListener('click', async () => {
            const codigo = btn.closest('.code-block').querySelector('code').innerText;
            try {
                await navigator.clipboard.writeText(codigo);
            } catch {
                // Alternativa para navegadores sin API de portapapeles
                const area = document.createElement('textarea');
                area.value = codigo;
                document.body.appendChild(area);
                area.select();
                document.execCommand('copy');
                area.remove();
            }
            btn.textContent = 'Copiado';
            btn.classList.add('copied');
            toast('Código copiado al portapapeles');
            setTimeout(() => { btn.textContent = 'Copiar'; btn.classList.remove('copied'); }, 1800);
        });
    });
}

/* ===== COPIAR DOCUMENTO COMPLETO ===== */
$('#copy-btn')?.addEventListener('click', async () => {
    const item = estado.items[estado.actual];
    if (!item) return;
    const resp = await fetch(item.path);
    const texto = await resp.text();
    try {
        await navigator.clipboard.writeText(texto);
        toast('Documento copiado');
    } catch {
        toast('No se pudo copiar');
    }
});

/* ===== NAVEGACIÓN DE DOCUMENTOS ===== */
$('#prev-doc')?.addEventListener('click', () => { if (estado.actual > 0) abrirArchivo(estado.actual - 1); });
$('#next-doc')?.addEventListener('click', () => { if (estado.actual < estado.items.length - 1) abrirArchivo(estado.actual + 1); });

/* ===== BARRA LATERAL MÓVIL ===== */
const sidebar = $('#sidebar');
$('#menu-btn')?.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    $('#sidebar-overlay').classList.toggle('open');
});
$('#sidebar-overlay')?.addEventListener('click', () => {
    sidebar.classList.remove('open');
    $('#sidebar-overlay').classList.remove('open');
});

function cerrarBarraLateralMovil() {
    if (window.innerWidth <= 1024) {
        sidebar.classList.remove('open');
        $('#sidebar-overlay').classList.remove('open');
    }
}

/* ===== BOTÓN DE INICIO ===== */
$('#brand-home')?.addEventListener('click', (e) => { e.preventDefault(); mostrarBienvenida(); });

/* ===== CAMBIO DE TEMA ===== */
const TEMA_CLAVE = 'tema';
function aplicarTema(tema) {
    document.documentElement.setAttribute('data-theme', tema);
    localStorage.setItem(TEMA_CLAVE, tema);
}

(function initTema() {
    const guardado = localStorage.getItem(TEMA_CLAVE);
    if (guardado) {
        aplicarTema(guardado);
    } else {
        const prefiereClaro = window.matchMedia('(prefers-color-scheme: light)').matches;
        aplicarTema(prefiereClaro ? 'light' : 'dark');
    }
})();

$('#theme-btn')?.addEventListener('click', () => {
    const actual = document.documentElement.getAttribute('data-theme');
    aplicarTema(actual === 'dark' ? 'light' : 'dark');
});

/* ===== REINICIAR PROGRESO ===== */
$('#reset-progress')?.addEventListener('click', () => {
    estado.leidos = new Set();
    localStorage.removeItem('leidos');
    actualizarProgreso();
    toast('Progreso reiniciado');
});

/* ===== ATAJOS DE TECLADO ===== */
document.addEventListener('keydown', (e) => {
    const enCampo = e.target.matches('input, textarea');
    if (e.key === '/' && !enCampo) {
        e.preventDefault();
        $('#search-input').focus();
    } else if (e.key === 'Escape' && !enCampo) {
        $('#search-results').classList.remove('open');
    } else if (enCampo) return;
    else if (e.key === 'ArrowRight' && estado.actual < estado.items.length - 1) {
        abrirArchivo(estado.actual + 1);
    } else if (e.key === 'ArrowLeft' && estado.actual > 0) {
        abrirArchivo(estado.actual - 1);
    }
});

/* ===== INICIALIZACIÓN ===== */
function abrirDesdeHash() {
    const m = location.hash.match(/#doc=(.+)$/);
    if (m) {
        const item = estado.items.find((x) => x.path === '../' + decodeURIComponent(m[1]));
        if (item) {
            abrirArchivo(item.orden);
            return;
        }
    }
    mostrarBienvenida();
}

cargarContenido();
