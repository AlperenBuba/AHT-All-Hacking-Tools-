#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
source "$DIR/venv/bin/activate" 2>/dev/null
python3 "$DIR/main.py"
