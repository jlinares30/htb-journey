# HTB Academy: Linux Fundamentals

## 📁 1. Estructura del Sistema de Archivos (FHS)
A diferencia de Windows, en Linux todo nace desde la raíz `/`. No existen los discos `C:` o `D:`.



### Directorios Críticos a Recordar:
*   `/etc`: Contiene los archivos de configuración del sistema (ej. `/etc/passwd` para usuarios).
*   `/var/log`: Aquí se almacenan los registros (logs) del sistema. Vital para forense y auditoría.
*   `/tmp` y `/dev/shm`: Directorios temporales con permisos de escritura para cualquier usuario. Muy usados para subir exploits.
*   `/bin` y `/sbin`: Almacenan los binarios (comandos) ejecutables del sistema.

---

## 🛠️ 2. Comandos Esenciales (Cheat Sheet)

### Navegación y Gestión de Archivos
```bash
# Listar archivos mostrando permisos, tamaño ocultos y formato humano
ls -lah

# Crear directorios de forma recursiva (crea carpetas padres si no existen)
mkdir -p /tmp/htb/labs/maquina1

# Buscar archivos por nombre en todo el sistema desde la raíz
find / -name "flag.txt" 2>/dev/null