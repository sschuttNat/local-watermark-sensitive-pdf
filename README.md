# Local Watermark for Sensitive PDFs

A tiny, offline-first app to protect sensitive PDF documents **directly on your computer** — no upload, no cloud, no LLM, no third-party service.

> Your documents never leave your machine.

## Why?

People often need to share sensitive documents: ID cards, payslips, tax notices, bank statements, rental applications... A common habit is to drop them into an online PDF tool or an AI assistant to add a watermark or hide some information. That means handing your most private data to a server you don't control.

This project does the job **100% locally**, with a dead-simple interface.

## Features

- 🖋️ **Tiled diagonal watermark** on every page with your own text (e.g. *"For Agency X only – rental application – 2026-11-06"*)
- 📂 Drag & drop **one or several PDFs** at once
- ⬇️ Protected copies are saved **straight to your `~/Downloads` folder** as `name_protected.pdf` (originals untouched, never overwritten)
- 🎚️ Adjustable opacity, text size and color
- 🔑 Optional **password protection** (AES-256) of the output PDF
- 🧹 Strips producer/creator metadata
- 🔄 Handles portrait, landscape and rotated pages
- ✈️ Works fully **offline** — the local server only listens on `127.0.0.1`, no network calls, no telemetry

## Requirements

- Python **3.9+**

## Easy install (macOS, no technical knowledge needed)

1. Install **Python** from [python.org/downloads](https://www.python.org/downloads/macos/) if you don't have it (the launcher will tell you if it's missing).
2. On this page, click the green **Code** button → **Download ZIP**, then double-click the ZIP to unzip it.
3. Open the folder and **right-click `start.command` → Open**, then confirm *Open* (macOS asks only the first time).
4. The first launch takes about a minute to set up. Your browser then opens the app.

Next times, just **double-click `start.command`**. Keep the Terminal window open while using the app, and close it to stop the app.

## Quick start (developers)

```bash
git clone https://github.com/sschuttNat/local-watermark-sensitive-pdf.git
cd local-watermark-sensitive-pdf
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Your browser opens on `http://127.0.0.1:5173`:

1. Drop your PDF(s)
2. Type the watermark text (who it's for, why, and when)
3. Click **Protect & save to Downloads**

On macOS you can also just **double-click `start.command`** (it sets everything up on first launch).

### Command line

```bash
.venv/bin/python protect.py id_card.pdf payslip.pdf --text "For Agency X only - 2026-11-06"
# options: --opacity 25 --size 28 --color "#808080" --password secret --out ./folder
```

## Project structure

| File | Role |
| --- | --- |
| `watermark.py` | Core PDF watermarking logic (pypdf + reportlab) |
| `app.py` | Local web UI (Flask, bound to 127.0.0.1) |
| `templates/index.html` | The single-page interface |
| `protect.py` | Command-line interface |
| `start.command` | macOS double-click launcher |

## Privacy principles

- Files are processed in memory on your machine only
- Nothing is sent anywhere — you can verify it by running the app with your network disabled
- Open source, so anyone can audit the code

## Limitations

The watermark is added as a vector layer on top of the page. Someone with PDF editing skills could remove it. A rasterize option (see roadmap) will make it much harder.

## Roadmap

- [x] CLI watermarking
- [x] Simple UI with drag & drop
- [ ] Rasterize option (convert pages to images to make the watermark non-removable)
- [ ] Manual redaction (black boxes over selected areas)
- [ ] Packaged executables for macOS, Windows and Linux

## Contributing

Ideas, issues and pull requests are welcome. Keep it simple: the goal is a small tool anyone can use and trust.