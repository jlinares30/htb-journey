#!/usr/bin/env python3
import argparse
import itertools
import sys

# Códigos de color ANSI para la terminal
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Diccionario de sustitución Leet Speak básico
LEET_DICT = {
    'a': '4', 'A': '4',
    'e': '3', 'E': '3',
    'i': '1', 'I': '1',
    'o': '0', 'O': '0',
    's': '5', 'S': '5',
    't': '7', 'T': '7'
}

def aplicar_leet(palabra):
    """Genera una versión leet speak sustituyendo caracteres comunes."""
    nueva_palabra = ""
    for letra in palabra:
        nueva_palabra += LEET_DICT.get(letra, letra)
    return nueva_palabra

def generar_diccionario(datos, sufijos, output_file):
    contrasenas_generadas = set() # Usamos un set para evitar duplicados automáticamente

    # 1. Agregar las palabras base en minúsculas, mayúsculas y Capitalizadas
    for palabra in datos:
        if not palabra: continue
        contrasenas_generadas.add(palabra.lower())
        contrasenas_generadas.add(palabra.upper())
        contrasenas_generadas.add(palabra.capitalize())
        
        # Aplicar reglas Leet Speak a las palabras individuales
        leet = aplicar_leet(palabra)
        contrasenas_generadas.add(leet)
        contrasenas_generadas.add(leet.capitalize())

    # 2. Permutaciones y combinaciones de 2 palabras clave básicas
    # Ejemplo: si los datos son ["empresa", "2026"], generará "empresa2026", "2026empresa", etc.
    if len(datos) >= 2:
        for combo in itertools.permutations(datos, 2):
            p1, p2 = combo
            combinaciones_base = [
                p1.lower() + p2.lower(),
                p1.capitalize() + p2.lower(),
                p1.capitalize() + p2.capitalize(),
                aplicar_leet(p1).capitalize() + p2.lower()
            ]
            contrasenas_generadas.update(combinaciones_base)

    # 3. Añadir sufijos/caracteres especiales al final de todo lo generado
    contrasenas_con_sufijos = set()
    for pwd in contrasenas_generadas:
        for sufijo in sufijos:
            contrasenas_con_sufijos.add(pwd + sufijo)
    
    contrasenas_generadas.update(contrasenas_con_sufijos)

    # 4. Guardar los resultados en el archivo .txt de salida
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for pwd in sorted(contrasenas_generadas):
                f.write(pwd + "\n")
        print(f"{GREEN}[+] Archivo guardado con éxito: {output_file}{RESET}")
        print(f"{GREEN}[+] Total de contraseñas generadas: {len(contrasenas_generadas)}{RESET}")
    except IOError:
        print(f"{RED}[-] Error al escribir en el archivo de salida.{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="Creador de Diccionarios Inteligente para Ataques Dirigidos (OSINT)."
    )
    parser.add_argument("-w", "--words", required=True, help="Palabras clave separadas por comas (ej: nombre,apellido,empresa)")
    parser.add_argument("-s", "--suffixes", default="!,?,123,2025,2026", help="Sufijos comunes separados por comas (default: !,?,123,2025,2026)")
    parser.add_argument("-o", "--output", default="wordlist_custom.txt", help="Nombre del archivo de salida (default: wordlist_custom.txt)")

    args = parser.parse_args()

    # Procesar los argumentos de entrada convirtiéndolos en listas
    lista_palabras = [w.strip() for w in args.words.split(",")]
    lista_sufijos = [s.strip() for s in args.suffixes.split(",")]
    # Añadir un sufijo vacío para mantener también las palabras sin sufijo
    lista_sufijos.append("") 

    print(f"\n{BLUE}" + "=" * 55)
    print(f" GENERANDO WORDLIST PERSONALIZADA")
    print(f"=" * 55 + f"{RESET}")
    print(f"Palabras base: {lista_palabras}")
    print(f"Sufijos:       {lista_sufijos[:-1]}")
    print(f"{BLUE}" + "=" * 55 + f"{RESET}\n")

    generar_diccionario(lista_palabras, lista_sufijos, args.output)

if __name__ == "__main__":
    main()