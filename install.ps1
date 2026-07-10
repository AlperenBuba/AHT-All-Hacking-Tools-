#requires -RunAsAdministrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AHT - Bagimlilik Kurulumu (PowerShell)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Python paketleri..." -ForegroundColor Yellow
pip install --upgrade scapy colorama requests --quiet 2>$null
Write-Host "  OK" -ForegroundColor Green

Write-Host "[2/3] Npcap kontrol..." -ForegroundColor Yellow
if (Test-Path "$env:SystemRoot\System32\drivers\npcap.sys") {
    Write-Host "  Npcap zaten kurulu" -ForegroundColor Green
} else {
    Write-Host "  Npcap indiriliyor..." -ForegroundColor Yellow
    $url = "https://npcap.com/dist/npcap-1.79.exe"
    $out = "$env:TEMP\npcap-installer.exe"
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        $wc = New-Object System.Net.WebClient
        $wc.DownloadFile($url, $out)
        Write-Host "  Indirildi: $out" -ForegroundColor Green
        Write-Host "  KURULUM: Dosyayi acip kurulumu tamamlayin." -ForegroundColor Yellow
        Write-Host "  (WinPcap API uyumluluk modunu isaretleyin)" -ForegroundColor Yellow
        Start-Process $out
    } catch {
        Write-Host "  HATA: $_" -ForegroundColor Red
        Write-Host "  Manuel indir: $url" -ForegroundColor Red
    }
}

Write-Host "[3/3] IP forwarding (registry)..." -ForegroundColor Yellow
try {
    reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v IPEnableRouter /t REG_DWORD /d 1 /f
    Write-Host "  OK (yeniden baslatma gerekebilir)" -ForegroundColor Green
} catch {
    Write-Host "  HATA: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TAMAM." -ForegroundColor Cyan
Write-Host "  1. Npcap kurulumunu tamamlayin" -ForegroundColor Cyan
Write-Host "  2. python main.py ile calistirin" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Read-Host "ENTER"
