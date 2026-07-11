#!/bin/bash
echo "========================================"
echo "  AHT - Bagimlilik Kurulumu (Linux)"
echo "========================================"
echo ""

DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[1/5] Sistem paketleri..."
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

echo "[2/5] Sanal ortam (venv) olusturuluyor..."
python3 -m venv "$DIR/venv"
source "$DIR/venv/bin/activate"
pip install --upgrade pip 2>/dev/null
echo "  OK"
echo ""

echo "[3/5] Python paketleri (sistem)..."
sudo pip3 install scapy colorama requests beautifulsoup4 duckduckgo_search 2>/dev/null
echo "  OK"
echo ""

echo "[4/5] Python paketleri (venv)..."
pip install scapy colorama requests beautifulsoup4 duckduckgo_search 2>/dev/null
echo "  OK"
echo ""

echo "[5/5] IP forwarding..."
sudo sysctl -w net.ipv4.ip_forward=1 >/dev/null 2>&1
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf >/dev/null 2>&1
echo "  OK"
echo ""

if ! command -v bettercap &> /dev/null; then
    echo "  Bettercap icin: sudo apt install bettercap"
fi
echo ""

echo "========================================"
echo "  TAMAM. Calistirma:"
echo "  ./aht.sh   veya   python3 main.py"
echo "========================================"
