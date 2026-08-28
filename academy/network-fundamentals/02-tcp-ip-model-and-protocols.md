# 02 - TCP/IP Model & Core Protocols

![Topic](https://img.shields.io/badge/Networking-TCP%2FIP%20%26%20Protocols-blue?style=flat-square)

> [!NOTE]
> While the OSI Model is theoretical, the **TCP/IP Model (Internet Protocol Suite)** is the practical operational model implemented in modern computer networks and the Internet.

---

## [+] OSI Model vs. TCP/IP Model Mapping

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#1e293b',
    'primaryTextColor': '#f8fafc',
    'primaryBorderColor': '#38bdf8',
    'lineColor': '#38bdf8',
    'fontFamily': 'Inter, system-ui, sans-serif'
  }
}}%%
graph LR
    subgraph OSI ["📐 OSI Model (7 Layers)"]
        O7["7. Application"]
        O6["6. Presentation"]
        O5["5. Session"]
        O4["4. Transport"]
        O3["3. Network"]
        O2["2. Data Link"]
        O1["1. Physical"]
    end

    subgraph TCPIP ["🚀 TCP/IP Model (4 Layers)"]
        T4["🌐 4. Application Layer"]
        T3["⚡ 3. Transport Layer"]
        T2["🗺️ 2. Internet Layer"]
        T1["🔗 1. Network Interface"]
    end

    O7 --> T4
    O6 --> T4
    O5 --> T4
    O4 --> T3
    O3 --> T2
    O2 --> T1
    O1 --> T1

    classDef osiStyle fill:#0f172a,stroke:#64748b,stroke-width:1px,color:#cbd5e1;
    classDef tcpStyle fill:#1e1b4b,stroke:#a855f7,stroke-width:2px,color:#f3e8ff;

    class O7,O6,O5,O4,O3,O2,O1 osiStyle;
    class T4,T3,T2,T1 tcpStyle;
```

---

## [+] TCP vs. UDP Comparison

| Feature | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
| :--- | :--- | :--- |
| **Connection Type** | Connection-oriented (Handshake required) | Connectionless (Fire and forget) |
| **Reliability** | Guaranteed delivery (retransmissions, sequencing) | Best-effort (no delivery guarantee) |
| **Header Size** | 20-60 Bytes | 8 Bytes |
| **Speed** | Slower (overhead due to reliability controls) | Faster (minimal overhead) |
| **Use Cases** | HTTP/S, SSH, FTP, SMTP, SMB | DNS queries, Video Streaming, VoIP, DHCP |

---

## [+] TCP Connection Life Cycle

### 1. TCP 3-Way Handshake (Establishment)
```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'actorBkg': '#0f172a',
    'actorBorder': '#38bdf8',
    'actorTextColor': '#f8fafc',
    'signalColor': '#38bdf8',
    'signalTextColor': '#f8fafc',
    'labelBoxBkgColor': '#1e293b',
    'labelBoxBorderColor': '#94a3b8',
    'labelTextColor': '#f8fafc'
  }
}}%%
sequenceDiagram
    autonumber
    participant Client as 💻 Client (Initiator)
    participant Server as 🖥️ Server (Listener)

    Note over Server: 🟢 State: LISTEN
    Client->>Server: 1. SYN (Seq = x)
    Note over Server: 🟡 State: SYN-RECEIVED
    Server->>Client: 2. SYN-ACK (Seq = y, Ack = x + 1)
    Note over Client: 🟢 State: ESTABLISHED
    Client->>Server: 3. ACK (Seq = x + 1, Ack = y + 1)
    Note over Server: 🟢 State: ESTABLISHED
    Note over Client,Server: 🤝 Connection Ready - Data Exchange Commences
```

### 2. TCP Graceful Connection Teardown (FIN / ACK)
```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'actorBkg': '#0f172a',
    'actorBorder': '#f97316',
    'actorTextColor': '#f8fafc',
    'signalColor': '#f97316',
    'signalTextColor': '#f8fafc',
    'labelBoxBkgColor': '#1e293b',
    'labelBoxBorderColor': '#cbd5e1',
    'labelTextColor': '#f8fafc'
  }
}}%%
sequenceDiagram
    autonumber
    participant HostA as 💻 Host A
    participant HostB as 🖥️ Host B

    HostA->>HostB: 1. FIN (Seq = a)
    HostB->>HostA: 2. ACK (Ack = a + 1)
    HostB->>HostA: 3. FIN (Seq = b)
    HostA->>HostB: 4. ACK (Ack = b + 1)
    Note over HostA,HostB: 🔴 Socket Session Terminated
```

### Connection Flags Overview:
- **SYN (Synchronize)**: Initiates connection sequence.
- **ACK (Acknowledge)**: Confirms receipt of packet.
- **FIN (Finish)**: Initiates graceful shutdown.
- **RST (Reset)**: Abruptly terminates connection due to error/unwanted port.
- **PSH (Push)**: Forces immediate delivery of buffered data.
- **URG (Urgent)**: Indicates data marked as urgent.

---

## [+] Essential Network Protocols & Ports

| Protocol | Default Port | Transport | Purpose / Description |
| :--- | :--- | :--- | :--- |
| **FTP** | 21 (Data 20) | TCP | File Transfer Protocol |
| **SSH** | 22 | TCP | Secure Shell (Encrypted remote terminal) |
| **Telnet** | 23 | TCP | Unencrypted remote terminal |
| **SMTP** | 25 | TCP | Simple Mail Transfer Protocol |
| **DNS** | 53 | UDP / TCP | Domain Name System (IP resolution) |
| **DHCP** | 67 (Server), 68 (Client) | UDP | Dynamic Host Configuration Protocol |
| **HTTP** | 80 | TCP | Hypertext Transfer Protocol |
| **Kerberos** | 88 | TCP/UDP | Authentication protocol (Active Directory) |
| **POP3** | 110 | TCP | Post Office Protocol |
| **RPC / Endpoint Mapper** | 135 | TCP | Remote Procedure Call |
| **NetBIOS** | 139 | TCP | Network Basic Input/Output System |
| **IMAP** | 143 | TCP | Internet Message Access Protocol |
| **SNMP** | 161 | UDP | Simple Network Management Protocol |
| **LDAP** | 389 | TCP | Lightweight Directory Access Protocol |
| **HTTPS** | 443 | TCP | HTTP Secure (TLS/SSL encrypted) |
| **SMB** | 445 | TCP | Server Message Block (File/Printer sharing) |
| **RDP** | 3389 | TCP | Remote Desktop Protocol |

---

## [*] Navigation

- **Previous**: [01-osi-model.md](file:///d:/Jorge/ciberseguridad/htb-journey/academy/network-fundamentals/01-osi-model.md)
- **Next**: [03-ip-addressing-and-subnetting.md](file:///d:/Jorge/ciberseguridad/htb-journey/academy/network-fundamentals/03-ip-addressing-and-subnetting.md)
