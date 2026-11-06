#!/bin/bash
# ---------------------------------------------------------------
#  Local PDF Watermark - one-click launcher for macOS
#  Double-click this file to start the app.
#  (First time only: right-click > Open, then confirm.)
# ---------------------------------------------------------------

cd "$(dirname "$0")" || exit 1

PORT=5173
URL="http://127.0.0.1:$PORT"

say_error() {
  # Show a friendly macOS dialog, and also print it in the Terminal.
  echo ""
  echo "❌ $1"
  osascript -e "display dialog \"$1\" buttons {\"OK\"} default button 1 with title \"Local PDF Watermark\" with icon caution" >/dev/null 2>&1
}

clear
echo "==============================================="
echo "   🔒 Local PDF Watermark"
echo "   Your files never leave this computer."
echo "==============================================="
echo ""

# 1. Already running? Just open the browser.
if curl -s --max-time 2 "$URL" | grep -q "<title>Local PDF Watermark"; then
  echo "✅ The app is already running. Opening your browser..."
  open "$URL"
  exit 0
elif lsof -nP -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; then
  say_error "Port $PORT is already used by another program. Close it and try again."
  exit 1
fi

# 2. Find a Python 3.9 or newer.
PY=""
for candidate in python3.14 python3.13 python3.12 python3.11 python3.10 python3.9 python3 \
                 /usr/local/bin/python3 /opt/homebrew/bin/python3 /usr/bin/python3; do
  if command -v "$candidate" >/dev/null 2>&1 && \
     "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; then
    PY="$(command -v "$candidate")"
    break
  fi
done

if [ -z "$PY" ]; then
  say_error "Python 3.9 or newer is required. The download page will open: install Python, then double-click this file again."
  open "https://www.python.org/downloads/macos/"
  exit 1
fi

# 3. First launch (or broken setup): install everything in a private folder.
if [ ! -x .venv/bin/python ] || ! .venv/bin/python -c 'import flask, pypdf, reportlab, cryptography' >/dev/null 2>&1; then
  echo "⏳ First launch: setting things up (about 1 minute, needs internet once)..."
  rm -rf .venv
  if ! "$PY" -m venv .venv || ! .venv/bin/pip install -q --disable-pip-version-check -r requirements.txt; then
    rm -rf .venv
    say_error "Setup failed. Check your internet connection and try again."
    exit 1
  fi
  echo "✅ Setup done."
  echo ""
fi

# 4. Start the app (it opens the browser by itself).
echo "🚀 Starting... your browser will open at $URL"
echo ""
echo "👉 Keep this window open while you use the app."
echo "👉 To stop the app, close this window (or press Ctrl+C)."
echo ""
.venv/bin/python app.py
