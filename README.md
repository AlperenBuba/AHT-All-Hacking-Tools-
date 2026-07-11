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

AHT, OSINT, SMS bombing, network tools, phishing, port scanning ve daha fazlasını tek bir CLI aracında birleştiren kapsamlı bir güvenlik test aracıdır.

---

<h2>🚀 Özellikler</h2>

<h3>📱 1. SMS Bomber</h3>

<ul>
  <li><b>Türk API'leri (33 servis):</b> KahveDunyasi, BIM, EnglishHome, Hayatsu, HizliEcza, MetroTR, FileMarket, Komagene, UysalMarket, Yapp, LittleCaesars, Domino's, Frink, Bodrum, Pidem, Koton, Alixavien, JimmyKey, WMF, Suiste, KimGb, TiklaGelsin, Naosstars, Akasya, Akbati, Porty, Tasdelen, KofteciYusuf, Coffy, Hamidiye, Orwi</li>
  <li><b>Uluslararası API'ler:</b> Textbelt, Callmebot</li>
  <li>⚡ 3 thread + random servis seçimi</li>
  <li>♾️ Sınırsız mod (Turbo), CTRL+C ile durdurma</li>
  <li>⏱️ Random delay (rate-limit koruması)</li>
</ul>

<h3>📶 2. WiFi Deauth</h3>
<ul>
  <li>🔨 Aircrack-ng (aireplay-ng)</li>
  <li>💥 MDK4</li>
  <li>🐍 Scapy Deauth</li>
  <li>📡 Monitor mod desteği</li>
</ul>

<h3>🛡️ 3. Network Tools (Bettercap)</h3>
<ul>
  <li>🎭 ARP Spoofing</li>
  <li>🔎 Ağ taraması</li>
  <li>⚙️ Bettercap entegrasyonu</li>
</ul>

<h3>🌍 4. IP Geolocation</h3>
<ul>
  <li>📍 IP adresi konum sorgulama</li>
  <li>🏢 ISS ve şehir bilgisi</li>
</ul>

<h3>🔌 5. Port Scanner</h3>
<ul>
  <li>🔓 TCP bağlantı noktası tarama</li>
  <li>⚡ Hızlı ve detaylı mod</li>
</ul>

<h3>🔧 6. MAC Changer</h3>
<ul>
  <li>🔄 Ağ arayüzü MAC adresi değiştirme</li>
  <li>🎲 Rastgele MAC oluşturma</li>
</ul>

<h3>💣 7. DDoS Tool</h3>
<ul>
  <li>🌊 HTTP Flood saldırıları</li>
  <li>🎯 Hedef IP/port desteği</li>
</ul>

<h3>🔍 8. OSINT (Açık Kaynak İstihbaratı)</h3>
<ul>
  <li>👤 <b>Kullanıcı Tara:</b> Sherlock ile sosyal medya hesap tarama</li>
  <li>🌐 <b>Web Ara:</b> DuckDuckGo üzerinden arama</li>
  <li>📞 <b>Telefon Numarası OSINT:</b> Numara analizi, operatör tespiti, txt kayıt</li>
  <li>🔎 <b>Google Dorking:</b> Google'da dork sorguları, sonuçları txt kaydetme</li>
</ul>

<h3>🎣 9. Phishing (Oltalama)</h3>
<ul>
  <li>📄 <b>Sahte Sayfa Oluşturucu:</b> Instagram, Facebook, Google, Twitter/X</li>
  <li>🌐 <b>Phishing Sunucusu:</b> HTTP sunucu ile ziyaretçi bilgileri toplama (IP, lokasyon, tarayıcı)</li>
  <li>☁️ <b>Cloudflare Tunnel:</b> Cloudflared ile herkese açık URL oluşturma</li>
</ul>

---

<h2>📥 Kurulum</h2>

<h3>🪟 Windows</h3>

<pre lang="batch">install.bat</pre>

veya:

<pre lang="batch">pip install -r requirements.txt</pre>

<h3>🐧 Linux</h3>

<pre lang="bash">pip install -r requirements.txt</pre>

<h3>📦 Alternatif (teker teker)</h3>

<pre lang="bash">pip install scapy colorama requests beautifulsoup4 duckduckgo_search</pre>

<h3>📡 Npcap (Windows - Ağ işlemleri için)</h3>

<p>Npcap, Windows'ta ağ taraması, ARP spoofing ve WiFi deauth gibi işlemler için gereklidir.</p>
<p><code>install.bat</code> dosyasını <b>Yönetici olarak çalıştırın</b> (Sağ tık → Yönetici olarak çalıştır).</p>

---

<h2>▶️ Kullanım</h2>

<pre lang="bash">python main.py</pre>

<p>Menüde gezinmek için sayı tuşlarını kullanın. 🌐 Dil değiştirmek için <kbd>L</kbd> tuşuna basın.</p>

<h3>📋 Ana Menü</h3>

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
│  [L] 🌐 Dil Değiştir / Switch Language  │
│  [0] ❌ Çıkış                           │
└─────────────────────────────────────────┘
</pre>

---

<h2>⚠️ Uyarı</h2>

<blockquote>
  Bu araç yalnızca <b>eğitim</b> ve <b>güvenlik testi</b> amaçlıdır. Kullanımından doğacak tüm yasal sorumluluk kullanıcıya aittir. İzinsiz sistemlere karşı kullanılması <b>yasa dışı</b> olabilir.
</blockquote>

---

<p align="center">
  <sub>Built with ❤️ by Alperen Buba</sub>
</p>
