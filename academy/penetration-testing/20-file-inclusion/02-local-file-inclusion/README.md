# Local File Inclusion (LFI)

## [+] Concept Overview
Local File Inclusion (LFI) occurs when an application includes a file, usually exposing it through a path input that is not properly sanitized, allowing an attacker to read or execute files local to the server.

### Common Vulnerable PHP Functions
* `include()` / `include_once()`
* `require()` / `require_once()`
* `file_get_contents()` (Read-only LFI)

### Typical Target Paths
#### Linux
* `/etc/passwd` (Users list)
* `/etc/hosts` (Local DNS)
* `/var/log/apache2/access.log` (Log Poisoning target)
* `/home/USER/.ssh/id_rsa` (Private SSH keys)

#### Windows
* `C:\Windows\win.ini` (Standard diagnostic file)
* `C:\Windows\System32\drivers\etc\hosts` (Hosts file)
* `C:\Users\Administrator\.ssh\id_rsa`
