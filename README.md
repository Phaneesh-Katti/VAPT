# Part-1 Running `tls_client.py`

You can run `tls_client.py` in two different ways:

### ✅ Option 1: As an Executable

Make the script executable and run it directly from the terminal:

```bash
chmod a+x tls_client.py
```
```bash
./tls_client.py <server-name>
```

### ✅ Option 2: Using Python Interpreter

Run it like a standard Python script:

```bash
python ./tls_client.py <server-name>
```

### 📦 About the PCAP File

The .pcap file was captured and analyzed using a simplified version of tls_client.py.

To reproduce similar outputs:

You can uncomment the relevant code inside tls_client.py, or

Use the provided simplified_tls_client.py script instead.

### 🔍 For Analysis
Use:
- `tls_client.py` for full TLS interaction.
- `simplified_tls_client.py` for a stripped-down version focused on analysis.

# Part-2 Vulnerability Assessment and Penetration Testing (VAPT) Report

## 🔍 Overview

This project documents a security assessment conducted on the web application hosted at [`https://home.iitd.ac.in`](https://home.iitd.ac.in). The objective of the assessment was to identify potential vulnerabilities across the application and network layers and provide actionable remediation recommendations.

We employed a combination of **automated tools** and **manual verification techniques** to simulate real-world attack scenarios. Our focus was on uncovering both client-side and server-side weaknesses, as well as network-level exposure.

---

## 🛠 Tools Used

- **OWASP ZAP** – For web application vulnerability scanning (e.g., XSS, CSP, outdated JS).
- **Nmap** – For network port scanning and vulnerability detection.
- **Metasploit Framework** – For exploit testing and proof-of-concept validation.
- **Custom Scripts** – For manual verification and payload crafting.

---

## ⚠️ Key Findings

- **High Risk:**  
  - Use of a vulnerable JavaScript library (`jquery-validation v1.14.0`) with known CVEs.
  
- **Medium Risk:**  
  - Missing Content Security Policy (CSP) headers.  
  - Absence of Anti-CSRF tokens on forms.  

- **Infrastructure-Level Risk:**  
  - Target appears vulnerable to **Slowloris (DoS)** attack (CVE-2007-6750).

---

## ✅ Recommendations

- Regularly update all third-party libraries and dependencies.  
- Implement a strict CSP header to reduce exposure to XSS and content injection.  
- Introduce CSRF protection via synchronizer tokens or similar mechanisms.  
- Harden server configuration to mitigate Slowloris using timeouts and connection limits.  
- Deploy a Web Application Firewall (WAF) and perform regular security audits.

---