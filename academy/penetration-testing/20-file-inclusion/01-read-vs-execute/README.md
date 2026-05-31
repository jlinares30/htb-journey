# Read vs. Execute

## [+] Concept Overview
In the context of File Inclusion vulnerabilities, there is a fundamental difference between disclosing/reading a file's source code and executing the file as active scripting code.

### 1. Read (Disclosure)
* **Mechanism**: The application reads the content of the file and prints it directly back to the user interface (e.g., using functions like `file_get_contents()`, `readfile()`, or custom file viewers).
* **Impact**: Source code disclosure, leakage of sensitive configuration files (e.g., `wp-config.php`, `.env`, database credentials), access to system files (`/etc/passwd`, `/windows/win.ini`).
* **PHP Context**: Wrappers like `php://filter` can be leveraged to read PHP files without execution by encoding the content (e.g., `convert.base64-encode`).

### 2. Execute (Execution)
* **Mechanism**: The application takes the input path and passes it to an execution engine, parser, or templating engine (e.g., using `include`, `require`, `include_once`, `require_once` in PHP).
* **Impact**: If the file contains script blocks (such as `<?php ... ?>`), the interpreter will execute the code. If the file does not contain code, it will often default to reading it as plain text.
* **PHP Context**: Using wrappers, remote file inclusion (RFI), or poisoned logs to execute arbitrary code (RCE).
