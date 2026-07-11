#!/bin/bash
echo "========================================"
echo "  AHT - Bagimlilik Kurulumu (Linux)"
echo "========================================"
echo ""

echo "[1/4] Sistem paketleri..."
if command -v apt &> /dev/null; then
    sudo apt update -qq && sudo apt install -y -qq python3-pip python3-venv libpcap-dev aircrack-ng mdk4 2>/dev/null
elif command -v pacman &> /dev/null; then
    sudo pacman -Sy --noconfirm python-pip python-virtualenv libpcap aircrack-ng mdk4 2>/dev/null
elif command -v dnf &> /dev/null; then
    sudo dnf install -y python3-pip python3-virtualenv libpcap-devel aircrack-ng mdk4 2>/dev/null
else
    echo "  Paket yoneticisi algilanamadi. pip ve libpcap-dev manuel kurun."
fi
echo "  OK"
echo ""

echo "[2/4] Python paketleri..."
pip3 install --upgrade scapy colorama requests beautifulsoup4 duckduckgo_search 2>/dev/null
echo "  OK"
echo ""

echo "[3/4] IP forwarding..."
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null 2>&1
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf >/dev/null 2>&1
echo "  OK"
echo ""

echo "[4/4] Bettercap (opsiyonel)..."
if ! command -v bettercap &> /dev/null; then
    echo "  Bettercap icin: sudo apt install bettercap (veya https://bettercap.org)"
fi
echo ""

echo "========================================"
echo "  TAMAM. python3 main.py ile calistir"
echo "========================================"
