# 01 - OSI Model & Data Encapsulation

![Topic](https://img.shields.io/badge/Networking-OSI%20Model-blue?style=flat-square)

> [!NOTE]
> The **OSI (Open Systems Interconnection) Model** is a conceptual framework created by ISO that standardizes the functions of a telecommunication or computing system into 7 distinct layers.

---

## [+] The 7 Layers of the OSI Model

| Layer # | Layer Name | Protocol Data Unit (PDU) | Primary Function & Focus | Key Protocols / Standards | Cybersecurity Relevance |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **7** | **Application** | Data | Human-computer interaction, network services to applications. | HTTP, HTTPS, FTP, SSH, DNS, SMTP | Web attacks, API abuse, C2 traffic |
| **6** | **Presentation** | Data | Data formatting, encryption, decryption, compression. | TLS/SSL, ASCII, JPEG, BASE64 | Encryption bypass, TLS manipulation |
| **5** | **Session** | Data | Interhost communication management, session establishment/teardown. | NetBIOS, RPC, SOCKS | Session hijacking, RPC enumeration |
| **4** | **Transport** | Segment (TCP) / Datagram (UDP) | End-to-end connections, flow control, error checking, port addressing. | TCP, UDP | Port scanning, SYN floods, socket binding |
| **3** | **Network** | Packet | Path determination, logical IP addressing, routing across networks. | IPv4, IPv6, ICMP, IPsec | IP spoofing, ICMP tunneling, routing attacks |
| **2** | **Data Link** | Frame | Physical addressing (MAC), error detection, node-to-node transfer. | Ethernet, Wi-Fi (802.11), ARP, VLAN | ARP spoofing, MAC flooding, VLAN hopping |
| **1** | **Physical** | Bits | Transmission of raw bit streams over physical medium. | Cables (Cat6, Fiber), Hubs, Network Interface Cards (NIC) | Hardware implants, physical tapping, jamming |

---

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#1e293b',
    'primaryTextColor': '#f8fafc',
    'primaryBorderColor': '#94a3b8',
    'lineColor': '#38bdf8',
    'secondaryColor': '#0f172a',
    'tertiaryColor': '#1e1b4b',
    'fontFamily': 'Inter, system-ui, sans-serif'
  }
}}%%
graph TD
    subgraph Upper ["🌐 Upper Layers (Software & Data)"]
        L7["🖥️ Layer 7: Application<br/><i>HTTP, HTTPS, SSH, DNS</i>"] -->|PDU: Data| L6["🔒 Layer 6: Presentation<br/><i>TLS/SSL, Compression, Encryption</i>"]
        L6 -->|PDU: Data| L5["🔄 Layer 5: Session<br/><i>RPC, NetBIOS, SOCKS</i>"]
    end

    subgraph Lower ["⚙️ Transport & Hardware Layers"]
        L5 -->|PDU: Data| L4["⚡ Layer 4: Transport<br/><i>TCP / UDP (Ports & Sockets)</i>"]
        L4 -->|PDU: Segment / Datagram| L3["🗺️ Layer 3: Network<br/><i>IPv4, IPv6, ICMP, Routing</i>"]
        L3 -->|PDU: Packet| L2["🔗 Layer 2: Data Link<br/><i>Ethernet, MAC Addresses, ARP, VLAN</i>"]
        L2 -->|PDU: Frame| L1["🔌 Layer 1: Physical<br/><i>Fiber, Cat6 Cables, Radio Waves</i>"]
    end

    classDef cAppStyle fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#e2e8f0;
    classDef cTransStyle fill:#1e1b4b,stroke:#a855f7,stroke-width:2px,color:#f3e8ff;
    classDef cLinkStyle fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#ecfdf5;

    class L7,L6,L5 cAppStyle;
    class L4,L3 cTransStyle;
    class L2,L1 cLinkStyle;
```

---

## [+] Protocol Data Units (PDUs) & Encapsulation

As data travels down the OSI stack from Layer 7 to Layer 1 during transmission, each layer adds its own header (and sometimes trailer). This process is called **Encapsulation**.

When receiving data, the process is reversed from Layer 1 up to Layer 7, stripping headers at each step. This is called **Decapsulation**.

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'actorBkg': '#0f172a',
    'actorBorder': '#38bdf8',
    'actorTextColor': '#f8fafc',
    'actorLineColor': '#38bdf8',
    'signalColor': '#9fef00',
    'signalTextColor': '#f8fafc',
    'labelBoxBkgColor': '#1e293b',
    'labelBoxBorderColor': '#475569',
    'labelTextColor': '#e2e8f0'
  }
}}%%
sequenceDiagram
    autonumber
    participant App as 💻 Application (L7-L5)
    participant Trans as ⚡ Transport (L4)
    participant Net as 🗺️ Network (L3)
    participant DLink as 🔗 Data Link (L2)
    participant Phys as 🔌 Physical (L1)

    Note over App: 📄 [Data Payload] Created
    App->>Trans: Encapsulate Data
    Note over Trans: ➕ Adds TCP/UDP Header<br/>📦 PDU: Segment
    Trans->>Net: Encapsulate Segment
    Note over Net: ➕ Adds IP Header<br/>📦 PDU: Packet
    Net->>DLink: Encapsulate Packet
    Note over DLink: ➕ Adds Eth Header & FCS Trailer<br/>📦 PDU: Frame
    DLink->>Phys: Transmit Frame
    Note over Phys: 📡 Binary Signals: 01001000 01100101...
```

---

## [+] Practical Security Implications

- **Layer 2 (Data Link)**: Attacks like ARP poisoning allow Man-in-the-Middle (MitM) positioning inside a local LAN segment.
- **Layer 3 (Network)**: Firewalls operate heavily here by checking source/destination IP addresses and routing rules.
- **Layer 4 (Transport)**: Port scanners like Nmap manipulate TCP flags (SYN, FIN, NULL, XMAS) to detect open/filtered ports.
- **Layer 7 (Application)**: Web Application Firewalls (WAF) inspect payload data (Layer 7) to block attacks like SQL Injection and XSS.

---

## [*] Navigation

- **Previous**: [README.md](file:///d:/Jorge/ciberseguridad/htb-journey/academy/network-fundamentals/README.md)
- **Next**: [02-tcp-ip-model-and-protocols.md](file:///d:/Jorge/ciberseguridad/htb-journey/academy/network-fundamentals/02-tcp-ip-model-and-protocols.md)
