# Network Enumeration with Nmap

![CPTS Path](https://img.shields.io/badge/CPTS-Reconnaissance%2C%20Enumeration%20%26%20Attack%20Planning-00ff66?style=flat-square&logo=gitbook&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=flat-square)

> [!NOTE]
> **OFFENSIVE OPERATIONS JOURNAL**
> Dedicated documentation for the CPTS syllabus training.

---

## [+] Mission Objectives
- [x] Understand the mechanics of Network Enumeration with Nmap
- [x] Clear all HTB Academy target labs
- [x] Document repeatable vectors, payloads, and defense bypasses

---

## [>] Tactical Theory & Methodology

Network enumeration consists of systematically identifying active devices, open ports, and running services within a targeted scope. Nmap performs this by transmitting crafted packets and interpreting the response or lack thereof.

### Host Discovery (Host Scanning)
Before scanning ports, Nmap determines if hosts are online.
- **ARP ping (`-PR`)**: Used automatically on local subnets. Fast and highly reliable since it uses Layer 2 protocols.
- **ICMP Echo (`-PE`), Timestamp (`-PP`), Address Mask (`-PM`)**: Classic Layer 3 ping checks. Frequently blocked by modern firewalls.
- **TCP SYN Ping (`-PS<ports>`)**: Sends an empty SYN packet to specified ports. A response (SYN-ACK or RST) indicates the host is alive.
- **TCP ACK Ping (`-PA<ports>`)**: Sends an ACK packet. A host response (RST) indicates the host is alive.
- **UDP Ping (`-PU<ports>`)**: Sends UDP packets to high/unused ports; an ICMP port unreachable response reveals the host is active.

### Port Scan States
Nmap classifies ports into six distinct states based on RFC compliance and packet responses:

| Port State | Description | Response Received |
| :--- | :--- | :--- |
| `open` | An application is actively accepting connections on this port. | SYN-ACK (TCP) or UDP response. |
| `closed` | The port is accessible but no application is listening. | RST (TCP) or ICMP port unreachable (UDP). |
| `filtered` | Nmap cannot determine if the port is open or closed due to packet filtering. | No response (drop) or ICMP unreachable error. |
| `unfiltered` | The port is accessible, but Nmap cannot determine if it is open or closed. | ACK scan response (RST). |
| `open\|filtered` | Nmap cannot determine if the port is open or filtered (common in UDP/FIN/Null/Xmas scans). | No response. |
| `closed\|filtered` | Nmap cannot determine if the port is closed or filtered (common in IP ID idle scans). | No response. |

### TCP Three-Way Handshake vs. SYN Scan
- **TCP Connect Scan (`-sT`)**: Completes the full three-way handshake (`SYN` -> `SYN-ACK` -> `ACK`). It is highly visible in application logs because the OS establishes a connection. Does not require root privileges.
- **SYN Stealth Scan (`-sS`)**: Sends a `SYN` packet and waits for `SYN-ACK`. If received, Nmap sends a `RST` to tear down the connection before it completes. Requires root privileges and is less likely to be logged at the application layer.

```text
SYN Scan (Stealth):
Attacker  -------- SYN ------->  Target
Attacker  <----- SYN-ACK ------  Target
Attacker  -------- RST ------->  Target
```

---

## [!] Arsenal & Payload Log

### Target Definition
```bash
export IP="10.129.x.x"
export CIDR="10.129.0.0/24"
```

### Discovery & Scan Optimization
```bash
# Ping sweep without port scanning (fast discovery)
nmap -sn -oA ping_sweep $CIDR

# Skip host discovery (treat all hosts as online)
nmap -Pn -p- $IP

# Port scan optimization parameters
# -T4 : Aggressive timing (speeds up scan, best for stable networks)
# --min-rate 5000 : Sends at least 5000 packets per second (very fast)
# -F : Scan top 100 ports (fast scan)
nmap -p- --min-rate 5000 -T4 -Pn -oN fast_scan.txt $IP
```

### Scan Types & Protocol Specifics
```bash
# TCP SYN Stealth Scan (Default as root)
nmap -sS -p- $IP

# TCP Connect Scan (Default as non-root)
nmap -sT -p22,80,443 $IP

# UDP Scan (Slow, sends UDP packets to ports, relies on ICMP responses)
nmap -sU -p- --min-rate 1000 $IP

# Version & OS Detection
# -sV : Service version detection
# -O : Operating System detection
# -A : Aggressive scan (includes -sV, -O, -sC, and traceroute)
nmap -sV -O -p- $IP
```

### Nmap Scripting Engine (NSE)
NSE scripts are categorized by safety/intent (`safe`, `default`, `vuln`, `exploit`, `auth`, `brute`, `discovery`).

```bash
# Run default scripts (-sC)
nmap -sC -p- $IP

# Search and run specific vulnerability category scripts
nmap --script "vuln" -p80 $IP

# Target specific services with custom scripts (e.g., SMB enumeration)
nmap --script smb-vuln* -p445 $IP
```

### Evasion & Bypassing Defenses
When firewalls block standard probes, evasive configurations are required:

- **Decoys (`-D`)**: Mixes real scan packets with spoofed IP addresses to obscure the origin.
  ```bash
  nmap -D 10.0.0.1,10.0.0.2,ME -p80 $IP
  ```
- **Source Port Spoofing (`--source-port` / `-g`)**: Exploits firewalls configured to trust incoming traffic originating from common service ports (e.g., DNS port 53).
  ```bash
  nmap --source-port 53 -p80 $IP
  ```
- **Fragment Packets (`-f`)**: Splits the IP header across several packets to bypass primitive packet inspection filters.
  ```bash
  nmap -f -p80 $IP
  ```
- **MTU Specification (`--mtu`)**: Specifies a custom Maximum Transmission Unit (must be a multiple of 8).
  ```bash
  nmap --mtu 24 -p80 $IP
  ```
- **Data Length Modification (`--data-length`)**: Appends random data to payloads to match normal network traffic profiles.
  ```bash
  nmap --data-length 25 -p80 $IP
  ```

---

## [¤] Operation Log (Proof of Concept)

### Typical Scan Methodology Flow

```yaml
Target Host: 10.129.201.50
System/OS: Linux
Objective: Complete Port Profile
```

#### 1. Initial Reconnaissance & Port Sweeping
Establish a rapid profile of all active ports:
```bash
sudo nmap -sS -p- --min-rate 5000 -Pn -oN tcp_all_ports.txt 10.129.201.50
```
*Result identifies open ports: 22/tcp (SSH), 80/tcp (HTTP), and 8080/tcp (HTTP-Proxy).*

#### 2. Deep Dive Service Enumeration
Target specific discovered ports for service banners and OS analysis:
```bash
sudo nmap -sV -sC -O -p22,80,8080 -oN service_details.txt 10.129.201.50
```

---

## [*] Post-Mortem & Defenses

- **Lessons Learned**:
  - Scanning UDP is slow but critical; filter scanning with `--min-rate` or check specific common UDP ports (e.g., SNMP 161, DNS 53) directly to save time.
  - Relying on default ping `-PE` will result in false negatives if the target host firewall drops ICMP Echo requests. Always pivot to `-Pn` or TCP SYN ping if no replies are received.
- **Detection & Mitigation**:
  - **IDS/IPS Systems**: Snort or Suricata can easily flag high-rate scans (`--min-rate 5000`) or standard Nmap signatures (such as TCP SYN scans terminating via RST before completions).
  - **Firewall Rules**: Implement rate limits on SYN packets and drop traffic originating from unusual ports if they do not match standard service mappings. Configure strict ingress rules.
