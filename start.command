#!/bin/bash
# Double-click this file on macOS to launch the app.
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  PY=$(command -v python3.13 || command -v python3.12 || command -v python3.11 || command -v python3)
  echo "Setting up (first launch only) with $PY..."
  "$PY" -m venv .venv && .venv/bin/pip install -q -r requirements.txt || exit 1
fi
.venv/bin/python app.py
