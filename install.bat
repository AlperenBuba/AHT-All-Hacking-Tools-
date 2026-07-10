@echo off
title AHT Kurulum
chcp 65001 >nul

echo ========================================
echo   AHT - Bagimlilik Kurulumu
echo ========================================
echo.

echo [1/3] Python paketleri...
pip install --upgrade scapy colorama requests 2>nul
echo  OK
echo.

echo [2/3] Npcap kontrol...
if exist "%SystemRoot%\System32\drivers\npcap.sys" (
    echo  Npcap zaten kurulu
) else (
    echo  Npcap indiriliyor...
    curl -sL -o "%TEMP%\npcap.exe" "https://npcap.com/dist/npcap-1.79.exe"
    if exist "%TEMP%\npcap.exe" (
        echo  Npcap kuruluyor...
        start /wait "" "%TEMP%\npcap.exe" /S
        del "%TEMP%\npcap.exe"
        echo  OK
    ) else (
        echo  HATA: indirilemedi! https://npcap.com/dist/npcap-1.79.exe
    )
)
echo.

echo [3/3] IP forwarding...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v IPEnableRouter /t REG_DWORD /d 1 /f >nul
echo  OK (yeniden baslatma gerekebilir)
echo.

echo ========================================
echo   TAMAM. python main.py ile calistir
echo ========================================
pause
