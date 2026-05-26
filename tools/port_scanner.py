#!/usr/bin/env python3
"""
Escáner de Puertos TCP Multihilo
--------------------------------------------------
Este es un script de ejemplo que demuestra cómo construir herramientas personalizadas
de reconocimiento en Python. Utiliza hilos (threading) para escanear un rango de puertos
de forma rápida.

Uso:
    python port_scanner.py <IP_o_Host> -p <rango_de_puertos> -t <hilos>

Ejemplo:
    python port_scanner.py 127.0.0.1 -p 1-1000 -t 50
"""

import socket
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Códigos de color ANSI para mejorar la interfaz visual en terminal
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def escanear_puerto(ip, puerto, timeout=1.0):
    """
    Intenta establecer una conexión TCP de tres vías (3-way handshake) 
    con un puerto específico en la IP objetivo.
    """
    try:
        # AF_INET especifica IPv4, SOCK_STREAM especifica protocolo TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            # connect_ex devuelve 0 si la conexión fue exitosa
            resultado = s.connect_ex((ip, puerto))
            if resultado == 0:
                print(f"{GREEN}[+] Puerto {puerto:5d}: ABIERTO{RESET}")
                return puerto
    except Exception as e:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(
        description="Escáner de Puertos TCP Multihilo en Python para Pentesting/Auditoría."
    )
    parser.add_argument("target", help="Dirección IP o Nombre de Host del objetivo (ej. 127.0.0.1 o google.com)")
    parser.add_argument("-p", "--ports", default="1-1024", help="Rango de puertos a escanear (ej. 1-1024 o 80)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Número de hilos concurrentes (default: 100)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Tiempo de espera de conexión en segundos (default: 1.0)")
    
    args = parser.parse_args()
    
    # Procesar el rango de puertos
    try:
        if "-" in args.ports:
            puerto_inicio, puerto_fin = map(int, args.ports.split("-"))
        else:
            puerto_inicio = puerto_fin = int(args.ports)
    except ValueError:
        print(f"{RED}[-] Formato de rango de puertos inválido. Usa e.g. 1-1024 o 80{RESET}")
        sys.exit(1)
        
    # Validar puertos
    if puerto_inicio < 1 or puerto_fin > 65535 or puerto_inicio > puerto_fin:
        print(f"{RED}[-] Rango de puertos inválido (debe estar entre 1 y 65535){RESET}")
        sys.exit(1)

    print(f"\n{BLUE}" + "=" * 55)
    print(f" INICIANDO ESCANEO DE PUERTOS")
    print(f"=" * 55 + f"{RESET}")
    print(f"Objetivo:        {args.target}")
    print(f"Rango Puertos:   {puerto_inicio} - {puerto_fin}")
    print(f"Hilos activos:   {args.threads}")
    print(f"Inicio:          {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{BLUE}" + "=" * 55 + f"{RESET}\n")
    
    # Resolver host a IP
    try:
        ip_objetivo = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"{RED}[- ] No se pudo resolver el host '{args.target}'{RESET}")
        sys.exit(1)
        
    puertos = list(range(puerto_inicio, puerto_fin + 1))
    puertos_abiertos = []
    
    # Uso de ThreadPoolExecutor para paralelizar el escaneo
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        # Enviamos las tareas al pool de hilos
        futuros = [
            executor.submit(escanear_puerto, ip_objetivo, puerto, args.timeout) 
            for puerto in puertos
        ]
        
        # Obtenemos los resultados a medida que finalizan
        for futuro in futuros:
            resultado = futuro.result()
            if resultado is not None:
                puertos_abiertos.append(resultado)
                
    print(f"\n{BLUE}" + "=" * 55 + f"{RESET}")
    print(f" ESCANEO COMPLETADO")
    print(f"=" * 55 + f"{RESET}")
    print(f"Fin:             {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Puertos abiertos encontrados: {GREEN}{len(puertos_abiertos)}{RESET}")
    if puertos_abiertos:
        print(f"Puertos:         {GREEN}{', '.join(map(str, sorted(puertos_abiertos)))}{RESET}")
    print(f"{BLUE}" + "=" * 55 + f"{RESET}\n")

if __name__ == "__main__":
    main()
