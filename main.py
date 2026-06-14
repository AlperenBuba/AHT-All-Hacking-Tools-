import platform
import os
import subprocess
import time

OS = platform.system()
Root = None
System = None
Selection = None
Location = "Home"

# OS Tanımlama ve Root yetkisi algılama
if OS == "Windows":
    import ctypes
    WinRoot = ctypes.windll.shell32.IsUserAnAdmin()
    System = "Windows"
    if WinRoot == 0:
        Root = False
    else:
        Root = True
elif OS == "Linux":
    System = "Linux"
    if os.geteuid() == 0:
        Root = True
    else:
        Root = False
elif OS == "Darwin":
    System = "Mac OS"
    if os.geteuid() == 0:
        Root = True
    else:
        Root = False
else:
    System = "Unknown"
    if os.geteuid() == 0:
        Root = True
    else:
        Root = False

# --| Ana Menü |-- #
while True:
    subprocess.call("cls" if platform.system() == "Windows" else "clear", shell=True)
    if Location == "Home":
        print(f"""
     █████╗ ██╗  ██╗████████╗
    ██╔══██╗██║  ██║╚══██╔══╝
    ███████║███████║   ██║   
    ██╔══██║██╔══██║   ██║   
    ██║  ██║██║  ██║   ██║   
    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                    version 1.0b - Alperen Buba\n\n\n
        
Select the action you want to perform
        
1. Sms Bomber\n
        """)
        Selection = int(input(":"))
        match Selection:
            case 1: Location = "sms_bomber"
            # Diğer seçenekler Gelecek
            
    elif Location == "sms_bomber":
        print(f"""
     █████╗ ██╗  ██╗████████╗
    ██╔══██╗██║  ██║╚══██╔══╝
    ███████║███████║   ██║   
    ██╔══██║██╔══██║   ██║   
    ██║  ██║██║  ██║   ██║   
    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                    version 1.0b - Alperen Buba\n\n\n
        
<--| AHT | SMS BOMBER |-->\n
        """)
        time.sleep(1)
        Location = "Home"