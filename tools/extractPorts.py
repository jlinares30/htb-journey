#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
extractPorts.py
Extrae la IP y los puertos abiertos a partir de un fichero grepable de Nmap (-oG).
Copia automáticamente los puertos al portapapeles y genera el comando sugerido para nmap -sCV.
"""

import sys
import os
import re
import subprocess


def copy_to_clipboard(text):
    """Intenta copiar el texto al portapapeles usando herramientas comunes en Linux/macOS/Windows."""
    try:
        # Linux (xclip)
        p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        p.communicate(input=text.encode('utf-8'))
        return True
    except Exception:
        pass

    try:
        # Linux (xsel)
        p = subprocess.Popen(['xsel', '-b', '-i'], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        p.communicate(input=text.encode('utf-8'))
        return True
    except Exception:
        pass

    try:
        # Linux (wl-copy / Wayland)
        p = subprocess.Popen(['wl-copy'], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        p.communicate(input=text.encode('utf-8'))
        return True
    except Exception:
        pass

    try:
        # Windows (clip)
        p = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True, stderr=subprocess.DEVNULL)
        p.communicate(input=text.encode('utf-8'))
        return True
    except Exception:
        pass

    try:
        # macOS (pbcopy)
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
        p.communicate(input=text.encode('utf-8'))
        return True
    except Exception:
        pass

    return False


def extract_ports(filename):
    if not os.path.exists(filename):
        print(f"\n[!] Error: El archivo '{filename}' no existe.\n")
        sys.exit(1)

    ip_address = None
    ports = []

    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if "Ports:" in line:
                # Extraer IP
                ip_match = re.search(r"Host:\s+(\d{1,3}(?:\.\d{1,3}){3})", line)
                if ip_match:
                    ip_address = ip_match.group(1)

                # Extraer puertos abiertos (formato grepable: 22/open/tcp//ssh///, 80/open/tcp//http///)
                ports_section = line.split("Ports:")[1]
                matches = re.findall(r"(\d+)/open/", ports_section)
                for port in matches:
                    if port not in ports:
                        ports.append(port)

    if not ip_address or not ports:
        print("\n[!] No se encontraron puertos abiertos en el archivo proporcionado.")
        print("[i] Asegúrate de que el archivo fue generado con: nmap ... -oG <archivo>\n")
        sys.exit(1)

    ports_str = ",".join(ports)
    copied = copy_to_clipboard(ports_str)

    print("\n" + "=" * 55)
    print(" [*] Extrayendo Información de Nmap (-oG)")
    print("=" * 55)
    print(f"\n\t[+] Dirección IP: {ip_address}")
    print(f"\t[+] Puertos Abiertos: {ports_str}\n")

    if copied:
        print("\t[*] Puertos copiados automáticamente al portapapeles!")
    else:
        print("\t[!] (Instala 'xclip' o 'xsel' para auto-copiado en Linux)")

    print("\n" + "-" * 55)
    print(" [*] Comando sugerido para escaneo profundo:")
    print(f"     nmap -sCV -p{ports_str} {ip_address} -oN targeted")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"\n[!] Uso: python3 {sys.argv[0]} <fichero-grepable-nmap>\n")
        print("    Ejemplo: nmap -p- -sS --min-rate 5000 -Pn -n 10.10.10.10 -oG allPorts")
        print(f"             python3 {sys.argv[0]} allPorts\n")
        sys.exit(1)

    extract_ports(sys.argv[1])
