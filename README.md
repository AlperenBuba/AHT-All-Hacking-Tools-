<p align="center">
  <img src="AHT-Window.png" alt="AHT-Window" width="800">
</p>

<h1 align="center">AHT - All Hacking Tools</h1>

<p align="center">
  <b>Version:</b> 1.0b &nbsp;|&nbsp; <b>Author:</b> Alperen Buba &nbsp;|&nbsp;
  <b>Platform:</b> 🪟 Windows / 🐧 Linux
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?logo=python">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey">
  <img src="https://img.shields.io/badge/license-GPLv3-red">
</p>

<p align="center">
  <b>OSINT | SMS Bomber | Network Tools | Phishing</b>
</p>

AHT is a comprehensive security testing tool that combines OSINT, SMS bombing, network tools, phishing, port scanning, MSFVenom payload generation and more in a single CLI tool.

---

## Features

### 1. SMS Bomber
- **Turkish APIs (33 services):** KahveDunyasi, BIM, EnglishHome, Hayatsu, HizliEcza, MetroTR, FileMarket, Komagene, UysalMarket, Yapp, LittleCaesars, Domino's, Frink, Bodrum, Pidem, Koton, Alixavien, JimmyKey, WMF, Suiste, KimGb, TiklaGelsin, Naosstars, Akasya, Akbati, Porty, Tasdelen, KofteciYusuf, Coffy, Hamidiye, Orwi
- **International APIs:** Textbelt, Callmebot
- 3 threads + random service selection
- Unlimited mode (Turbo), stop with CTRL+C
- Random delay (rate-limit protection)

### 2. WiFi Deauth
- Aircrack-ng (aireplay-ng)
- MDK4
- Scapy Deauth
- Monitor mode support

### 3. Network Tools (Bettercap)
- ARP Spoofing
- Network scanning
- Bettercap integration

### 4. IP Geolocation
- IP address location lookup
- ISP and city information

### 5. Port Scanner
- TCP port scanning
- Fast and detailed modes

### 6. MAC Changer
- Network interface MAC address change
- Random MAC generation

### 7. DDoS Tool
- HTTP Flood attacks
- Target IP/port support

### 8. OSINT (Open Source Intelligence)
- **User Search:** Sherlock social media account scanning
- **Web Search:** DuckDuckGo search
- **Phone Number OSINT:** Number analysis, carrier info, Google dork links, txt save
- **Google Dorking:** File-type filter menu, Google scraping with DuckDuckGo fallback, txt save

### 9. MSFVenom Payload Generator
- Automatic download and install of Metasploit Framework (if missing)
- Platform selection: Windows, Android, Linux, Mac, PHP, Python
- LHOST/LPORT configuration
- Output formats: exe, py, php, war, elf, apk, raw

### 10. Phishing
- **Fake Page Generator:** Instagram, Facebook, Google, Twitter/X
- **Phishing Server:** HTTP server collecting visitor info (IP, location, browser)
- **Cloudflare Tunnel:** Public URL via Cloudflared

---

## Installation

### Windows

**Recommended:** Download the pre-built .exe from [TurkByteSoftware](https://alperenbuba.github.io/TurkByteSoftware/)

or run from source:

```bash
python main.py
```

All dependencies (Python packages, Npcap, IP forwarding) are auto-installed on first run.

### Linux

```bash
pip install scapy colorama requests beautifulsoup4 duckduckgo_search
python3 main.py
```

---

## Usage

```bash
python main.py
```

Use number keys to navigate the menu. Press **L** to switch language.

### Main Menu

```
[1]  SMS Bomber
[2]  WiFi Deauth
[3]  Network Tools
[4]  IP Geolocation
[5]  Port Scanner
[6]  MAC Changer
[7]  DDoS Tool
[8]  OSINT
[9]  Phishing
[10] MSFVenom Payload Generator
[L]  Switch Language
[0]  Exit
```

---

## Warning

> This tool is for **educational** and **security testing** purposes only. All legal responsibility lies with the user. Using it against unauthorized systems may be **illegal**.

---

<p align="center">
  <sub>Built by Alperen Buba</sub>
</p>
