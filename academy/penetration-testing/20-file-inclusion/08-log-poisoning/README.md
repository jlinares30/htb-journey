# Log Poisoning (Envenenamiento de Logs)

![CPTS Path](https://img.shields.io/badge/CPTS-Web%20Exploitation-00ff66?style=flat-square&logo=gitbook&logoColor=white)

El envenenamiento de logs (Log Poisoning) es una técnica que consiste en inyectar código malicioso (usualmente PHP) en los archivos de registro o logs del servidor para luego forzar su ejecución a través de una vulnerabilidad de Local File Inclusion (LFI). Esto permite pasar de una lectura pasiva de archivos a una Ejecución Remota de Código (RCE).

---

## [+] Mecánica del Ataque
1.  **Inyección:** El atacante realiza una acción que genera un registro en algún log del servidor (como Apache, Nginx, SSH o FTP), pero altera los datos enviados para que contengan código PHP malicioso.
2.  **Inclusión:** El atacante utiliza un parámetro vulnerable a LFI para incluir el archivo de log envenenado.
3.  **Ejecución:** Dado que el servidor web interpreta el archivo a través de la función de inclusión (ej. `include()`), el código inyectado en el log se ejecuta en el servidor.

---

## [>] Vectores de Envenenamiento Comunes

### 1. Apache / Nginx Access Logs
El servidor web registra la cabecera `User-Agent` de todas las peticiones entrantes.
*   **Ruta típica:**
    *   `/var/log/apache2/access.log`
    *   `/var/log/nginx/access.log`
*   **Método de inyección:**
    Enviar una petición HTTP modificando el campo `User-Agent` para incluir código malicioso PHP (por ejemplo, llamando a funciones de ejecución de comandos como `system` pasándole un parámetro GET/POST).
*   **Ejecución:**
    Llamar al archivo de log a través de la URL vulnerable agregando el comando deseado en los parámetros de la URL.

### 2. SSH Auth Logs
El servicio SSH registra todos los intentos de conexión (incluidos los fallidos) con el nombre de usuario provisto.
*   **Ruta típica:**
    *   `/var/log/auth.log`
    *   `/var/log/secure`
*   **Método de inyección:**
    Intentar conectar por SSH usando código PHP como nombre de usuario (ej. inyectando una función de ejecución en el campo de usuario al realizar la conexión SSH).
*   **Ejecución:**
    Cargar el archivo de log de autenticación a través del LFI.

---

## [*] Desafíos y Consideraciones
*   **Permisos de Lectura:** El usuario que ejecuta el servidor web (ej. `www-data` o `nginx`) debe tener permisos de lectura sobre el archivo de log para que esta explotación sea exitosa. Por defecto, `/var/log/auth.log` y `/var/log/apache2/access.log` suelen tener restricciones de permisos estrictas que requieren configuración manual o mala administración para ser accesibles.
*   **Corrupción del Log:** Si cometes un error de sintaxis en el código PHP inyectado, el intérprete de PHP fallará al incluir el log, arrojando errores y rompiendo el procesamiento de esa página hasta que el log rote o se limpie.
