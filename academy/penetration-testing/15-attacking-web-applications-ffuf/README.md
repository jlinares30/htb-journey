# Attacking Web Applications with Ffuf

![CPTS Path](https://img.shields.io/badge/CPTS-Web%20Exploitation-00ff66?style=flat-square&logo=gitbook&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-00ff66?style=flat-square)

> [!NOTE]
> **OFFENSIVE OPERATIONS JOURNAL**
> Dedicated documentation for the CPTS syllabus training on web fuzzing and discovery using `ffuf` (Fuzz Faster U Fool).

---

## [+] Mission Objectives
- [x] Understand the mechanics of Attacking Web Applications with Ffuf
- [x] Document repeatable vectors, payloads, and defense bypasses
- [x] Master directory, file, extension, subdomain, VHost, and parameter fuzzing

---

## [>] Tactical Theory & Methodology

Fuzzing is the art of sending unexpected or semi-structured data to inputs to discover hidden entry points, files, directories, subdomains, virtual hosts, or parameter vulnerabilities.

```text
Fuzzing Targets:
├── Directory/File Discovery: Uncovering hidden paths and application files.
├── Domain/VHost Fuzzing: Discovering internal subdomains and virtual hosts mapped to the same IP.
└── Parameter Fuzzing:
    ├── GET Parameters: Fuzzing query string keys (?FUZZ=value)
    ├── POST Parameters: Fuzzing body keys (d: "FUZZ=value")
    └── Parameter Values: Fuzzing input values to bypass authorization (e.g. id=FUZZ)
```

### Key Filtering Options in FFUF
Since web servers return status codes and response bodies for almost everything, filtering is crucial to eliminate noise:
- `-fc`: Filter HTTP status codes (e.g., `-fc 404,403`)
- `-fs`: Filter response size (e.g., `-fs 290`)
- `-fl`: Filter number of lines in response (e.g., `-fl 12`)
- `-fw`: Filter word count in response (e.g., `-fw 35`)
- `-fr`: Filter using a regular expression against the response (e.g., `-fr "Not Found"`)

---

## [!] Arsenal & Payload Log

### 1. Basic Directory and File Discovery
```bash
# Directory Fuzzing
ffuf -w /usr/share/wordlists/dirb/common.txt -u http://10.129.x.x:PORT/FUZZ

# Extension Fuzzing (finding which extensions are active, e.g., php, html, txt)
ffuf -w /usr/share/wordlists/seclists/Discovery/Web-Content/web-extensions.txt -u http://10.129.x.x:PORT/indexFUZZ

# Page Fuzzing (combining directories with known extension)
ffuf -w /usr/share/wordlists/dirb/common.txt -u http://10.129.x.x:PORT/FUZZ.php

# Recursive Fuzzing
ffuf -w /usr/share/wordlists/dirb/common.txt -u http://10.129.x.x:PORT/FUZZ -recursion -recursion-depth 1 -e .php,.html -v
```

### 2. Subdomain and VHost Fuzzing
```bash
# Subdomain Fuzzing (requires DNS resolution / public zone)
ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u http://FUZZ.target.local/

# VHost Fuzzing (Fuzzes Host header directly on target IP; essential for internal domains)
ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u http://10.129.x.x:PORT/ -H "Host: FUZZ.target.local" -fs 290
```

### 3. Parameter Fuzzing
```bash
# GET Parameter Fuzzing
ffuf -w /usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt -u http://10.129.x.x:PORT/admin/admin.php?FUZZ=key -fs 290

# POST Parameter Fuzzing
ffuf -w /usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt -u http://10.129.x.x:PORT/admin/admin.php -X POST -d "FUZZ=key" -H "Content-Type: application/x-www-form-urlencoded" -fs 290

# Fuzzing Parameter Values (e.g. sequential IDs or brute-forcing numbers)
seq 1 1000 > ids.txt
ffuf -w ids.txt -u http://10.129.x.x:PORT/admin/admin.php -X POST -d "id=FUZZ" -H "Content-Type: application/x-www-form-urlencoded" -fs 290
```

### 4. Advanced Request & Target Customizations (HTB Academy)
```bash
# Using Multiple Wordlists (e.g. fuzzing parameter name AND value simultaneously)
# Assign aliases to wordlists using ':' and use them in the URL/data string
ffuf -w /path/to/params.txt:W1 -w /path/to/values.txt:W2 -u http://10.129.x.x:PORT/admin/admin.php?W1=W2 -fs 290

# Sending Custom Headers & Cookies (Authentication & Target Bypasses)
ffuf -w wordlist.txt -u http://10.129.x.x:PORT/FUZZ -H "Cookie: session=xyz" -H "User-Agent: Mozilla/5.0"

# POST JSON Fuzzing
# Note: JSON payload formatting requires quoting the body correctly
ffuf -w wordlist.txt -u http://10.129.x.x:PORT/api/lookup -X POST -d '{"username": "FUZZ"}' -H "Content-Type: application/json" -fs 290
```

### 5. Output Management & Logging
```bash
# Saving output to a file (JSON format)
ffuf -w wordlist.txt -u http://10.129.x.x:PORT/FUZZ -o results.json -of json

# Saving output in multiple formats (e.g. md, html, csv)
ffuf -w wordlist.txt -u http://10.129.x.x:PORT/FUZZ -o results -of md
```

---

## [¤] Operation Log (Proof of Concept)

### Typical Discovery Workflow

1. **Perform Directory Discovery**:
   Identify directories like `/admin`, `/api`, `/dev`.
2. **Perform Extension/Page Fuzzing**:
   Identify if it is a PHP site, and find admin script: `/admin/admin.php`.
3. **Parameter Scan**:
   Identify parameter accepted by `/admin/admin.php`.
4. **Exploit/Extract Info**:
   Submit specific inputs to extract details (e.g., flags).

---

## [*] Post-Mortem & Defenses
- **Lessons Learned**: Always run a quick test request first to check the baseline response size, then use `-fs` or `-fl` to filter it out. Otherwise, false positives will flood the output.
- **Detection & Mitigation**: Web Application Firewalls (WAFs) and rate-limiters (like fail2ban or Nginx rate-limiting) should be configured to detect burst traffic from single IPs. Check logs for high-frequency requests with identical user-agents.
