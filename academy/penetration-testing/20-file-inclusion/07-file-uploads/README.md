# File Upload Attacks (Ataques de Subida de Archivos)

![CPTS Path](https://img.shields.io/badge/CPTS-Web%20Exploitation-00ff66?style=flat-square&logo=gitbook&logoColor=white)

Las vulnerabilidades de subida de archivos permiten a un atacante subir archivos maliciosos (normalmente scripts como webshells) al sistema de archivos del servidor para luego ejecutarlos, logrando potencialmente una Ejecución Remota de Código (RCE).

---

## [+] Vectores Comunes de Explotación

### 1. Subida Libre de Archivos (Unrestricted File Upload)
La aplicación no valida de ninguna forma el tipo o extensión del archivo subido.
*   **Acción:** Subir un archivo con extensión ejecutable (como `.php` o `.asp`) que contenga código de comandos y acceder a él a través del navegador.

### 2. Evasión de Filtros del Lado del Cliente (Client-Side - Javascript)
La validación se realiza únicamente en el navegador del usuario antes de enviar la petición HTTP.
*   **Bypass:**
    1. Desactivar Javascript en el navegador.
    2. O bien, interceptar la petición de subida con un proxy de interceptación (como Burp Suite) y cambiar la extensión del archivo de una permitida (ej. `shell.png`) a la deseada (ej. `shell.php`) antes de enviarla.

### 3. Evasión de Filtros del Lado del Servidor (Server-Side)

#### Blacklist de Extensiones
El servidor prohíbe extensiones comunes.
*   **Bypass:** Probar extensiones alternativas que el intérprete del servidor pueda procesar:
    *   **PHP:** `.php3`, `.php4`, `.php5`, `.phtml`, `.phar`, `.pgif`
    *   **ASP.NET:** `.aspx`, `.ashx`, `.asmx`, `.axd`

#### Filtro de Content-Type
El servidor valida la cabecera `Content-Type` de la petición HTTP recibida.
*   **Bypass:** Modificar la cabecera en el proxy:
    ```http
    Content-Type: image/png
    ```

#### Validación de Magic Bytes (Firmas de Archivos)
El servidor comprueba los primeros bytes del archivo para cerciorarse de su tipo (ej. `89 50 4E 47` para PNG).
*   **Bypass:** Agregar los bytes mágicos de una imagen válida al inicio de nuestro archivo de script (como la firma `GIF89a;` al inicio del archivo de texto antes de la sección del script).

---

## [*] Medidas de Mitigación
1.  **Renombrar Archivos:** Utilizar nombres generados aleatoriamente (ej. mediante hash MD5/SHA256) y no preservar el nombre original.
2.  **Directorios No Ejecutables:** Configurar el servidor web para que no permita la ejecución de scripts dentro de la carpeta donde se almacenan los archivos subidos.
3.  **Validación de Tipo Robusta:** Utilizar funciones del lado del servidor que analicen el contenido real del archivo (no basarse únicamente en extensiones o Content-Type provistos por el usuario).
