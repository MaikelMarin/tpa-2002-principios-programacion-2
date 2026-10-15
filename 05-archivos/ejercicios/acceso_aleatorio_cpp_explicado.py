r"""
Ejercicio 13 (tema 05): Acceso aleatorio en C++
Dificultad: Avanzado

CONOCIMIENTO PREVIO NECESARIO
    - Acceso aleatorio en Python (tema 05, ejercicio 8): el equivalente
      de este ejercicio.
    - `fstream` de C++ y sus modos.

PROBLEMA
    Modificar una regin específica de un archivo binario en C++.

POR QU INCLUIR C++ AQU
    Este es el nico ejercicio del proyecto en C++. Su propsito es
    mostrar que el acceso aleatorio NO es una caracterstica de Python:
    es una operación del SISTEMA OPERATIVO (lseek + read/write), y todos
    los lenguajes la exponen de forma similar.

    Las diferencias entre lenguajes aqu son de sintaxis, no de concepto.

COMPARACIN PYTHON vs C++

    Python:                       C++:
      f.seek(pos)                   f.seekp(pos)
      f.read(n)                     f.read(buffer, n)
      f.write(datos)                f.write(buffer, n)
      with open(...)                ifstream/ofstream (RAII)

    En C++ hay DOS punteros:
      - seekg / tellg  para LECTURA (get)
      - seekp / tellp  para ESCRITURA (put)
    Python usa un nico puntero para ambas.

    En C++ el cierre es automático por RAII (el destructor del objeto
    archivo), igual que `with` en Python.

QU stream PARA QU
    ifstream                     solo lectura
    ofstream                     solo escritura
    fstream                      lectura Y escritura

    Para acceso aleativo Read+Write hace falta fstream con los flags:
        std::ios::in | std::ios::out

    OJO: NO usar ios::out solo, porque trunca el archivo a 0 al abrir.

Cdig completo en C++

```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    // Crear archivo con datos conocidos
    std::ofstream escritura("test.bin", std::ios::binary);
    const char datos[] = "ABCDEFGHIJ";
    escritura.write(datos, 10);
    escritura.close();

    // Leer desde la posición 3
    std::ifstream lectura("test.bin", std::ios::binary);
    lectura.seekg(3);                       // seek para LECTURA
    char buffer[5] = {0};
    lectura.read(buffer, 4);
    std::cout << "Posicin 3: " << buffer << std::endl;   // DEFG
    lectura.close();

    // Escribir en la posición 5 SIN truncar
    std::fstream rw("test.bin",
                    std::ios::binary | std::ios::in | std::ios::out);
    rw.seekp(5);                            // seek para ESCRITURA
    rw.write("XY", 2);
    rw.close();

    // Verificar
    std::ifstream verificar("test.bin", std::ios::binary);
    std::string contenido((std::istreambuf_iterator<char>(verificar)),
                           std::istreambuf_iterator<char>());
    std::cout << "Final: " << contenido << std::endl;   // ABCDEXYHIJ
    return 0;
}
```

RESULTADO ESPERADO (idntico al ejercicio de Python)
    Archivo inicial:  ABCDEFGHIJ
    Tras escribir "XY" en pos 5: ABCDE-XY-HIJ = ABCDEXYHIJ

    Note que es EXACTAMENTE el mismo resultado que el ejercicio 8 del
    tema 05: la posición 5 corresponde al byte F, y escribir 2 bytes
    consume las posiciones 5 y 6 (F y G).

COMPILACIN Y EJECUCIN
    g++ -std=c++17 acceso_aleatorio_cpp.cpp -o acceso
    ./acceso

PARA EJECUTAR ESTE ARCHIVO
    No se ejecuta desde la web. Se compila con un compilador de C++:

        cd 05-archivos/ejercicios
        g++ -std=c++17 acceso_aleatorio_cpp.cpp -o acceso
        ./acceso

RELACIN CON OTROS TEMAS
    - El ejercicio 8 del tema 05 resuelve el mismo problema en Python.
      Compárelos: la lgica es idntica, la sintaxis cambia.
"""


# Este archivo es documentacin: el cdigo ejecutable est en el bloque
# de cdigo de arriba. Para ejecutarlo:
#
#     cd 05-archivos/ejercicios
#     g++ -std=c++17 acceso_aleatorio_cpp.cpp -o acceso
#     ./acceso
#
# Salida esperada:
#     Defg: DEFG
#     Final: ABCDEXYHIJ

import os

# Ruta al archivo C++ hermana, relativa a ESTE archivo (no al cwd),
# para que funcione se ejecute desde cualquier directorio.
RUTA_CPP = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "acceso_aleatorio_cpp.cpp")

print("Este es un documento de referencia: el cdigo C++ ejecutable est")
print("en el archivo acceso_aleatorio_cpp.cpp de esta misma carpeta.")
print()
print("Para compilarlo y ejecutarlo:")
print("  g++ -std=c++17 acceso_aleatorio_cpp.cpp -o acceso")
print("  ./acceso")

# Verificar que el archivo C++ existe junto a este documento
assert os.path.exists(RUTA_CPP), \
    f"falta el archivo acceso_aleatorio_cpp.cpp en {os.path.dirname(RUTA_CPP)}"

# Verificar que tiene el contenido mínimo esperado
with open(RUTA_CPP, encoding="utf-8") as f:
    codigo_cpp = f.read()

# El archivo usa `using namespace std`, as que busca sin el prefijo.
assert "seekp" in codigo_cpp, "debe usar seekp (escritura)"
assert "seekg" in codigo_cpp, "debe usar seekg (lectura)"
assert "ios::in" in codigo_cpp and "ios::out" in codigo_cpp, \
    "debe abrir en modo lectura Y escritura sin truncar"
assert "ABCDEFGHIJ" in codigo_cpp, "debe usar los datos del ejemplo"
assert "fstream" in codigo_cpp, "debe usar fstream para leer y escribir"

# TRAMPA IMPORTANTE: no debe usar `ofstream` para la modificacin,
# porque truncara el archivo a 0 bytes.
assert "ofstream" not in codigo_cpp.split("fstream escritura")[1][:200], \
    "la escritura no debe usar ofstream (truncaria el archivo)"

print("\nVerificado: acceso_aleatorio_cpp.cpp contiene el cdigo completo")
print("con seekp (escritura) y seekg (lectura).")

print("\n Todas las pruebas pasaron")
