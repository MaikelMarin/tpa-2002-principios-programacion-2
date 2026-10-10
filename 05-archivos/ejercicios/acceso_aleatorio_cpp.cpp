/*
 * Ejercicio 13: Acceso aleatorio en C++
 * Dificultad: Avanzado
 *
 * Manipula el puntero de lectura/escritura para acceder directamente
 * a cualquier posición del archivo.
 */

#include <fstream>
#include <iostream>
#include <string>
using namespace std;

int main() {
    // Crear archivo con datos conocidos
    ofstream archivo("test.bin", ios::binary);
    const char datos[] = "ABCDEFGHIJ";
    archivo.write(datos, 10);
    archivo.close();

    // Leer desde posición 3
    ifstream lectura("test.bin", ios::binary);
    lectura.seekg(3);
    char buffer[5] = {0};
    lectura.read(buffer, 4);
    cout << "Datos en posicion 3: " << buffer << endl;
    lectura.close();

    // Escribir en posición 5
    fstream escritura("test.bin", ios::binary | ios::in | ios::out);
    escritura.seekp(5);
    escritura.write("XY", 2);
    escritura.close();

    // Verificar contenido final
    ifstream verificar("test.bin", ios::binary);
    string contenido((istreambuf_iterator<char>(verificar)),
                      istreambuf_iterator<char>());
    cout << "Contenido modificado: " << contenido << endl;
    verificar.close();

    return 0;
}
