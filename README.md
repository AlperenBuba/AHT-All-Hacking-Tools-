# AHT v1.0b — All Hacking Tools

Çok fonksiyonlu siber güvenlik araç seti. Terminal menüleri üzerinden ARP spoofing/MITM, WiFi deauth, SMS bomber, port tarama, MAC değiştirme, DDoS ve daha fazlası.

**YouTube Kanalı:** [Alperen Buba](https://www.youtube.com/@Alperenbuba/videos)

---

## ⚠️ Yasal Uyarı

Bu araç yalnızca **eğitim amaçlı, siber güvenlik farkındalığı ve yetkili penetrasyon testleri** için geliştirilmiştir. Yetkisiz sistemlerde veya izinsiz ağlarda kullanımı tamamen kullanıcının sorumluluğundadır. Geliştirici hiçbir şekilde sorumluluk kabul etmez.

---

## Kurulum

### 1. Npcap Kurulumu (Windows için zorunlu)

ARP spoofing, sniffing ve L2 paket işlemleri için Npcap gereklidir.

**PowerShell'i Yönetici olarak aç** ve şu komutları çalıştır:

```powershell
cd C:\Users\alper\OneDrive\Documents\GitHub\AHT-All-Hacking-Tools-
Set-ExecutionPolicy Bypass -Scope Process -Force
.\install.ps1
```

Bu komutlar:
- Npcap kurulum dosyasını indirir ve açar
- Python bağımlılıklarını yükler (`scapy`, `colorama`, `requests`)
- Windows IP forwarding kayıt defteri anahtarını etkinleştirir

**Npcap kurulumunda "WinPcap API-compatible Mode" seçeneğini işaretlemeyi unutma.**

Alternatif olarak manuel indir: https://npcap.com/dist/npcap-1.79.exe

### 2. Python Bağımlılıkları

Elle kurmak istersen:

```bash
pip install scapy colorama requests
```

### 3. IP Forwarding (Windows)

`install.ps1` otomatik yapar. Elle yapmak için:

```powershell
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v IPEnableRouter /t REG_DWORD /d 1 /f
```

*Değişikliğin etkin olması için bilgisayarı yeniden başlatman gerekebilir.*

---

## Çalıştırma

```bash
python main.py
```

Windows'ta yönetici yetkisi gerektiren işlemler için PowerShell'i yönetici olarak açıp çalıştır.

---

## Kullanım

- Menülerde `0` girerek bir önceki menüye dönülür.
- IP, port, arayüz gibi sorularda **boş ENTER** işlemi iptal eder ve ana menüye döner.
- Tüm araçlar **CTRL+C** ile durdurulabilir.

### Ana Menü

| No | Araç | Açıklama |
|----|------|----------|
| 1 | SMS Bomber | Hedef numaraya SMS gönderimi |
| 2 | WiFi Deauth | WiFi istemcilerini bağlantıdan düşürme (3 yöntem) |
| 3 | Network Tools | Ağ tarama, ARP spoofing/MITM, sniffing, bağlantı kesme, engelleme |
| 4 | IP Geolocation | IP adresi konum sorgulama |
| 5 | Port Scanner | Hedef IP üzerinde port tarama |
| 6 | MAC Changer | Ağ arayüzü MAC adresi değiştirme |
| 7 | DDoS Tool | HTTP/SYN/UDP saldırıları |

### Network Tools Alt Menüsü

| No | Araç | Açıklama |
|----|------|----------|
| 1 | Ağ Taraması | Ağdaki cihazları bul (ARP taraması) |
| 2 | ARP Spoofing (MITM) | Hedef-gateway arasında ARP zehirleme + canlı trafik izleme |
| 3 | HTTP/DNS Sniffing | Ağdaki HTTP istekleri ve DNS sorgularını canlı izle |
| 4 | Bağlı Cihazlar | Ağdaki aktif cihazları listele |
| 5 | Bağlantıyı Kes | Hedef cihazın internet bağlantısını kes (ARP + IPv6 zehirleme) |
| 6 | İnternet Engelle/Kaldır | Hedefe giden trafiği engelle veya kaldır |

---

## Gereksinimler

| Bağımlılık | Versiyon | Açıklama |
|------------|----------|----------|
| Python | 3.8+ | Çalışma ortamı |
| Npcap | 1.79+ | Paket yakalama (Windows) |
| scapy | 2.5+ | Ağ paket işleme |
| colorama | 0.4+ | Renkli terminal çıktısı |
| requests | 2.28+ | HTTP istekleri |

---

## Geliştirici

- **Alperen Buba**
- **Proje:** AHT (All Hacking Tools)
- **Lisans:** MIT

> "Knowledge is the ultimate security vulnerability."
