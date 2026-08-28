# Network Fundamentals

![HTB Academy](https://img.shields.io/badge/HTB%20Academy-Network%20Fundamentals-1f2026?style=flat-square&logo=hackthebox)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow?style=flat-square)

> [!NOTE]
> **HTB ACADEMY MODULE: NETWORK FUNDAMENTALS**
> Documentation of fundamental networking theory, protocol stack mechanics, traffic analysis, and core concepts essential for cybersecurity and penetration testing.

---

## [+] Module Overview

Understanding network fundamentals is critical for both offensive security (identifying attack vectors, traffic analysis, evasion) and defensive security (monitoring, incident response, network hardening).

### Key Topics Covered:
1. **[01-osi-model.md](file:///d:/Jorge/ciberseguridad/htb-journey/academy/network-fundamentals/01-osi-model.md)**: The 7-layer OSI Model, PDUs, encapsulation, and decapsulation.
2. **[02-tcp-ip-model-and-protocols.md](file:///d:/Jorge/ciberseguridad/htb-journey/academy/network-fundamentals/02-tcp-ip-model-and-protocols.md)**: TCP/IP stack, TCP 3-way handshake, UDP, ports, ARP, DNS, DHCP, and HTTP/S.
3. **[03-ip-addressing-and-subnetting.md](file:///d:/Jorge/ciberseguridad/htb-journey/academy/network-fundamentals/03-ip-addressing-and-subnetting.md)**: IPv4/IPv6 structure, CIDR notation, subnetting calculation, and network tools (Wireshark, tcpdump).

---

## [+] Learning Objectives

- [ ] Master the 7 layers of the OSI model and 4 layers of the TCP/IP model
- [ ] Analyze packet encapsulation and header formats across protocols
- [ ] Grasp TCP socket connections, handshakes, flags, and connection states
- [ ] Understand key infrastructure protocols (ARP, DNS, DHCP, ICMP, Routing)
- [ ] Perform IPv4 subnetting and network identification
- [ ] Apply networking knowledge to network scanning, traffic capture, and exploitation analysis

---

## [+] Quick Command Cheat Sheet

```bash
# Network Interfaces & Routing
ip a / ifconfig                   # Display interface configurations
ip route / route -n               # Display routing table
ping -c 4 <target_ip>             # ICMP echo test

# Resolution & Connections
arp -a                            # Display local ARP cache
ss -tulpn / netstat -tulpn        # Display active sockets and listening ports
dig <domain> @<dns_server>        # Query DNS records
nslookup <domain>                 # Perform basic DNS lookup

# Traffic Capture & Analysis
tcpdump -i eth0 icmp              # Capture ICMP packets on eth0 interface
tcpdump -n -i eth0 port 80        # Capture HTTP traffic without DNS resolving
```

---

## [*] Navigation

- **Next Document**: [01-osi-model.md](file:///d:/Jorge/ciberseguridad/htb-journey/academy/network-fundamentals/01-osi-model.md)
