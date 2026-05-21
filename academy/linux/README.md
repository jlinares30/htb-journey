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

> [!TIP]
> En auditorías de seguridad y pentesting, es muy común encontrarse con "dumb shells" donde el prompt no se muestra o está roto. Saber cómo está estructurado te ayudará a identificar rápidamente si has logrado escalar privilegios a root (al notar el cambio de `$` a `#`).