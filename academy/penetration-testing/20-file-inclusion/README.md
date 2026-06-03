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
├── [Read vs Execute](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/01-read-vs-execute/README.md)
├── [Local File Inclusion (LFI)](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/02-local-file-inclusion/README.md)
├── [Basic Bypasses](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/03-basic-bypasses/README.md)
├── [PHP Filters](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/04-php-filters/writeup.md)
├── [PHP Wrappers](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/05-php-wrappers/writeup.md)
├── [Remote File Inclusion (RFI)](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/06-remote-file-inclusion/README.md)
├── [File Upload Attacks](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/07-file-uploads/README.md)
└── [Log Poisoning](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/08-log-poisoning/README.md)
```

### Lab Writeups
* [LFI Machine Writeup](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/02-local-file-inclusion/writeup.md)
* [PHP Wrappers Writeup](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/05-php-wrappers/writeup.md)
* [Bypasses Machine Writeup](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/03-basic-bypasses/writeup.md)
* [PHP Filters Machine Writeup](file:///d:/u/cibersecurity/htb-journey/academy/penetration-testing/20-file-inclusion/04-php-filters/writeup.md)


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
