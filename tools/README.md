# Herramientas Personalizadas y Scripts

![Workspace](https://img.shields.io/badge/Workspace-Tools-blue?style=flat-square)

Esta carpeta contiene scripts propios y herramientas desarrolladas a lo largo del aprendizaje en Hack The Box para automatizar tareas de reconocimiento, explotación y análisis.

## [+] Lista de Herramientas

### 1. Escáner de Puertos TCP Multihilo (`port_scanner.py`)
Un escáner de puertos TCP escrito en Python puro (sin dependencias externas) que implementa concurrencia con hilos para verificar qué puertos están abiertos rápidamente en un equipo objetivo.

* **Archivo**: [`port_scanner.py`](file:///d:/u/cibersecurity/htb-journey/tools/port_scanner.py)
* **Requisitos**: Python 3.x
* **Uso**:
  ```bash
  python port_scanner.py <IP_o_Host> [opciones]
  ```

#### Opciones disponibles:
* `-p`, `--ports` : Rango de puertos a escanear. Por defecto es `1-1024` (ej: `-p 1-5000` o `-p 80`).
* `-t`, `--threads` : Número de hilos simultáneos. Por defecto es `100` (mayor cantidad = escaneo más rápido).
* `--timeout` : Tiempo de espera en segundos por puerto antes de considerarlo cerrado. Por defecto es `1.0`.

#### Ejemplo de Salida:
```text
=======================================================
 INICIANDO ESCANEO DE PUERTOS
=======================================================
Objetivo:        127.0.0.1
Rango Puertos:   1 - 8080
Hilos activos:   100
Inicio:          2026-05-26 17:50:00
=======================================================

[+] Puerto    22: ABIERTO
[+] Puerto    80: ABIERTO
[+] Puerto  8080: ABIERTO

=======================================================
 ESCANEO COMPLETADO
=======================================================
Fin:             2026-05-26 17:50:05
Puertos abiertos encontrados: 3
Puertos:         22, 80, 8080
=======================================================
```

### 2. Detección de Sistema Operativo por TTL (`whichSystem.py`)
Determina si una máquina objetivo es Linux o Windows analizando el valor de TTL (Time to Live) en las respuestas ICMP.

* **Archivo**: [`whichSystem.py`](file:///d:/Jorge/ciberseguridad/htb-journey/tools/whichSystem.py)
* **Uso**:
  ```bash
  python3 whichSystem.py <IP_Objetivo>
  ```

---

### 3. Extractor de Puertos Nmap (`extractPorts.py`)
Procesa el archivo grepable (`-oG`) generado por Nmap tras un escaneo rápido, extrae la IP, filtra los puertos abiertos en formato separado por comas, los copia automáticamente al portapapeles (`xclip`/`xsel`/`wl-copy`/`clip`) y genera el comando para el escaneo detallado (`-sCV`).

* **Archivo**: [`extractPorts.py`](file:///d:/Jorge/ciberseguridad/htb-journey/tools/extractPorts.py)
* **Uso**:
  ```bash
  # 1. Escaneo rápido de todos los puertos guardando en formato grepable (-oG)
  nmap -p- --open -sS --min-rate 5000 -Pn -n 10.10.10.188 -oG allPorts

  # 2. Extraer puertos y copiar al portapapeles
  python3 extractPorts.py allPorts
  ```

#### Ejemplo de Salida:
```text
=======================================================
 [*] Extrayendo Información de Nmap (-oG)
=======================================================

	[+] Dirección IP: 10.10.10.188
	[+] Puertos Abiertos: 22,80,443,8080

	[*] Puertos copiados automáticamente al portapapeles!

-------------------------------------------------------
 [*] Comando sugerido para escaneo profundo:
     nmap -sCV -p22,80,443,8080 10.10.10.188 -oN targeted
=======================================================
```

---

### 4. Generador de Wordlists Personalizadas (`wordlist_generator.py`)
Genera diccionarios y combinaciones basadas en información de reconocimiento (nombres, años, palabras clave, variaciones de mayúsculas/minúsculas y sustituciones l33t).

* **Archivo**: [`wordlist_generator.py`](file:///d:/Jorge/ciberseguridad/htb-journey/tools/wordlist_generator.py)

---

> [!CAUTION]
> **Uso Ético**: Utiliza estas herramientas únicamente en entornos controlados, máquinas de Hack The Box u otros objetivos autorizados. El escaneo de puertos no autorizado puede ser considerado tráfico malicioso por sistemas de detección de intrusos (IDS/IPS).
