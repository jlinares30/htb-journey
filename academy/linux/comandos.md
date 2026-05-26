# 🐧 Guía de Referencia: Comandos de Linux

Bienvenido a tu bitácora de comandos de Linux. Este documento sirve como una referencia rápida y organizada por categorías para consultar la sintaxis y el propósito de los comandos esenciales en auditorías y administración de sistemas.

---

## 🔍 Índice de Categorías

1. [Ayuda y Documentación](#-ayuda-y-documentación)
2. [Navegación y Exploración del Sistema](#-navegación-y-exploración-del-sistema)

---

## 📚 Ayuda y Documentación

Cuando trabajas en la terminal, no necesitas memorizar cada parámetro. Linux provee mecanismos internos para entender cómo funciona cualquier herramienta.

| Comando | Sintaxis Básica | Descripción | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`man`** | `man <comando>` | Abre el manual oficial de la herramienta seleccionada, detallando su uso, argumentos y banderas. | `man ls` |
| **`apropos`** | `apropos <palabra_clave>` | Busca en las descripciones de todas las páginas del manual por coincidencias con la palabra clave. Útil cuando olvidas el nombre del comando. | `apropos "directory listing"` |
| **`--help`** / **`-h`** | `<comando> --help` | Muestra una guía rápida de ayuda en la propia salida estándar sin abrir el manual completo. | `ls --help` |

> [!TIP]
> Si una página de `man` es demasiado larga, puedes buscar palabras dentro de ella presionando `/`, escribiendo el término a buscar y pulsando `Enter`. Usa `n` para ir al siguiente resultado y `q` para salir del manual.

---

## 📁 Navegación y Exploración del Sistema

Comandos para inspeccionar directorios, listar contenidos y entender dónde estamos parados en la jerarquía del sistema.

| Comando | Sintaxis Básica | Descripción | Ejemplo de Uso |
| :--- | :--- | :--- | :--- |
| **`ls`** | `ls [opciones] [ruta]` | Lista el contenido (archivos y carpetas) del directorio actual o de la ruta especificada. | `ls /etc` |
| **`ls -h`** | `ls -lh [ruta]` | La bandera `-h` (*human-readable*) muestra el tamaño de los archivos en formatos legibles (KB, MB, GB) en lugar de bytes. | `ls -lh /var/log` |

> [!IMPORTANT]
> La bandera `-h` de `ls` por sí sola no mostrará los tamaños a menos que se combine con una bandera que active la visualización de tamaños, como `-l` (formato largo) o `-s` (mostrar tamaño de bloques). Por ello, el uso estándar recomendado es **`ls -lh`**.

### Banderas Comunes de `ls` a Recordar:
* `-l` : Muestra el listado en formato largo (detalla permisos, propietario, grupo, tamaño y fecha de modificación).
* `-a` : Muestra archivos ocultos (aquellos que empiezan con un punto `.`, como `.bashrc`).
* `-t` : Ordena los archivos por fecha de modificación (los más nuevos primero).
* `-R` : Lista directorios de forma recursiva.
