# 🕵️ ShadowRecon

> Automated Web Recon & Vulnerability Detection Framework

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux-red)

ShadowRecon is a modular Python-based framework for automated web reconnaissance and vulnerability detection. Built for penetration testers and bug bounty hunters.

---

## ⚡ Features

- 🌐 Subdomain Enumeration (DNS brute-force, multithreaded)
- 🔍 Port & Service Fingerprinting
- 🛠️ Web Technology Detection (CMS, frameworks, security headers)
- 💉 SQL Injection Detection
- 🔥 XSS Detection (Reflected)
- 🔓 IDOR Detection
- 📊 HTML + JSON Report Generation

---

## 🚀 Installation
```bash
git clone git@github.com:saksht/ShadowRecon.git
cd ShadowRecon
pip3 install -r requirements.txt
```

---

## 🎯 Usage
```bash
# Run all modules
python3 shadowrecon.py -t http://target.com --all -o report

# Run specific modules
python3 shadowrecon.py -t http://target.com --subdomains --tech --portscan

# Vuln detection only
python3 shadowrecon.py -t http://target.com --sqli --xss --idor -o vuln_report
```

---

## 📸 Demo
```
Target: http://testsite.com
[*] Subdomains Found: admin, api, dev, staging
[*] Open Ports: 80/HTTP, 443/HTTPS, 3306/MySQL
[*] Tech Stack: WordPress, jQuery, PHP
[+] SQLi Found: /index.php?id=1 → payload: '
[+] XSS Found: /?q=<script>alert(1)</script>
[+] Report saved: report.html & report.json
```

---

## ⚠️ Disclaimer

This tool is intended for authorized penetration testing and educational purposes only. Do not use against systems you don't have explicit permission to test.

---

## 👤 Author

**Akshat Singh** — [@saksht](https://github.com/saksht)

> Part of the Shadow toolkit — see also [ShadowC2](https://github.com/saksht/ShadowC2)
