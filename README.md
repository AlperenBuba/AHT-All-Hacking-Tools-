<p align="center">
  <img src="AHT-Window.png" alt="AHT-Window" width="800">
</p>

<h1 align="center">⚔️ AHT - All Hacking Tools ⚔️</h1>

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
  <b>🔍 OSINT &nbsp;|&nbsp; 📱 SMS Bomber &nbsp;|&nbsp; 🌐 Network Tools &nbsp;|&nbsp; 🎣 Phishing</b>
</p>

AHT is a comprehensive security testing tool that combines OSINT, SMS bombing, network tools, phishing, port scanning and more in a single CLI tool.

---

<h2>🚀 Features</h2>

<h3>📱 1. SMS Bomber</h3>

<ul>
  <li><b>Turkish APIs (33 services):</b> KahveDunyasi, BIM, EnglishHome, Hayatsu, HizliEcza, MetroTR, FileMarket, Komagene, UysalMarket, Yapp, LittleCaesars, Domino's, Frink, Bodrum, Pidem, Koton, Alixavien, JimmyKey, WMF, Suiste, KimGb, TiklaGelsin, Naosstars, Akasya, Akbati, Porty, Tasdelen, KofteciYusuf, Coffy, Hamidiye, Orwi</li>
  <li><b>International APIs:</b> Textbelt, Callmebot</li>
  <li>⚡ 3 threads + random service selection</li>
  <li>♾️ Unlimited mode (Turbo), stop with CTRL+C</li>
  <li>⏱️ Random delay (rate-limit protection)</li>
</ul>

<h3>📶 2. WiFi Deauth</h3>
<ul>
  <li>🔨 Aircrack-ng (aireplay-ng)</li>
  <li>💥 MDK4</li>
  <li>🐍 Scapy Deauth</li>
  <li>📡 Monitor mode support</li>
</ul>

<h3>🛡️ 3. Network Tools (Bettercap)</h3>
<ul>
  <li>🎭 ARP Spoofing</li>
  <li>🔎 Network scanning</li>
  <li>⚙️ Bettercap integration</li>
</ul>

<h3>🌍 4. IP Geolocation</h3>
<ul>
  <li>📍 IP address location lookup</li>
  <li>🏢 ISP and city information</li>
</ul>

<h3>🔌 5. Port Scanner</h3>
<ul>
  <li>🔓 TCP port scanning</li>
  <li>⚡ Fast and detailed modes</li>
</ul>

<h3>🔧 6. MAC Changer</h3>
<ul>
  <li>🔄 Network interface MAC address change</li>
  <li>🎲 Random MAC generation</li>
</ul>

<h3>💣 7. DDoS Tool</h3>
<ul>
  <li>🌊 HTTP Flood attacks</li>
  <li>🎯 Target IP/port support</li>
</ul>

<h3>🔍 8. OSINT (Open Source Intelligence)</h3>
<ul>
  <li>👤 <b>User Search:</b> Sherlock social media account scanning</li>
  <li>🌐 <b>Web Search:</b> DuckDuckGo search</li>
  <li>📞 <b>Phone Number OSINT:</b> Number analysis, carrier detection, txt save</li>
  <li>🔎 <b>Google Dorking:</b> Google dork queries, save results to txt</li>
</ul>

<h3>🎣 9. Phishing</h3>
<ul>
  <li>📄 <b>Fake Page Generator:</b> Instagram, Facebook, Google, Twitter/X</li>
  <li>🌐 <b>Phishing Server:</b> HTTP server collecting visitor info (IP, location, browser)</li>
  <li>☁️ <b>Cloudflare Tunnel:</b> Public URL via Cloudflared</li>
</ul>

---

<h2>📥 Installation</h2>

<h3>🪟 Windows</h3>

<pre lang="batch">install.bat</pre>

or:

<pre lang="batch">pip install -r requirements.txt</pre>

<h3>🐧 Linux</h3>

<pre lang="bash">pip install -r requirements.txt</pre>

<h3>📦 Alternative (one by one)</h3>

<pre lang="bash">pip install scapy colorama requests beautifulsoup4 duckduckgo_search</pre>

<h3>📡 Npcap (Windows - Network operations)</h3>

<p>Npcap is required for network scanning, ARP spoofing and WiFi deauth on Windows.</p>
<p>Run <code>install.bat</code> as <b>Administrator</b> (Right click → Run as administrator).</p>

---

<h2>▶️ Usage</h2>

<pre lang="bash">python main.py</pre>

<p>Use number keys to navigate the menu. Press <kbd>L</kbd> to switch language.</p>

<h3>📋 Main Menu</h3>

<pre>
┌─────────────────────────────────────────┐
│  [1] 📱 SMS Bomber                      │
│  [2] 📶 WiFi Deauth                     │
│  [3] 🛡️ Network Tools                   │
│  [4] 🌍 IP Geolocation                  │
│  [5] 🔌 Port Scanner                    │
│  [6] 🔧 MAC Changer                     │
│  [7] 💣 DDoS Tool                       │
│  [8] 🔍 OSINT                           │
│  [9] 🎣 Phishing                        │
│  [L] 🌐 Switch Language                 │
│  [0] ❌ Exit                            │
└─────────────────────────────────────────┘
</pre>

---

<h2>⚠️ Warning</h2>

<blockquote>
  This tool is for <b>educational</b> and <b>security testing</b> purposes only. All legal responsibility lies with the user. Using it against unauthorized systems may be <b>illegal</b>.
</blockquote>

---

<p align="center">
  <sub>Built with ❤️ by Alperen Buba</sub>
</p>
