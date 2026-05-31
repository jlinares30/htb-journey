# File Inclusion

![CPTS Path](https://img.shields.io/badge/CPTS-Web%20Exploitation-00ff66?style=flat-square&logo=gitbook&logoColor=white)
![Status](https://img.shields.io/badge/Status-Pending-lightgrey?style=flat-square)

> [!NOTE]
> **OFFENSIVE OPERATIONS JOURNAL**
> Dedicated documentation for the CPTS syllabus training.

---

## [+] Mission Objectives
- [ ] Understand the mechanics of File Inclusion
- [ ] Clear all HTB Academy target labs
- [ ] Document repeatable vectors, payloads, and defense bypasses

---

## [>] Tactical Theory & Methodology
*Record core architectural concepts, protocols, or logic flaws encountered here.*

```text
Vulnerability/Concept Map:
├── [Read vs Execute](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/read-vs-execute/README.md)
├── [Local File Inclusion (LFI)](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/local-file-inclusion/README.md)
├── [Basic Bypasses](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/basic-bypasses/README.md)
└── [PHP Filters & Wrappers](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/php-filters/README.md)
```

### Lab Writeups
* [LFI Machine Writeup](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/local-file-inclusion/writeup.md)
* [Bypasses Machine Writeup](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/basic-bypasses/writeup.md)
* [PHP Filters Machine Writeup](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/php-filters/writeup.md)


---

## [!] Arsenal & Payload Log
*Useful scripts, tool flags, one-liners, and manual exploits.*

```bash
# Target Variable definition
export IP="10.129.x.x"

# Quick scan reference
# command -t $IP --payload ...
```

---

## [¤] Operation Log (Proof of Concept)
*Detailed writeups of target compromises and host intrusions.*

```yaml
Target Host: 10.129.x.x
System/OS: Linux / Windows
Objective: User / Root Flag
```

### 1. Reconnaissance & Foothold
*How the entry point was identified and compromised.*

### 2. Privilege Escalation / Lateral Movement
*How local privileges were upgraded or other network assets were reached.*

---

## [*] Post-Mortem & Defenses
- **Lessons Learned**: *Where did I lose time? What was the rabbit hole?*
- **Detection & Mitigation**: *How would a blue team spot this attack?*
