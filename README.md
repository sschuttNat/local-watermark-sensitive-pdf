# Local Watermark for Sensitive PDFs

A tiny, offline-first app to protect sensitive PDF documents **directly on your computer** — no upload, no cloud, no LLM, no third-party service.

> Your documents never leave your machine.

## Why?

People often need to share sensitive documents: ID cards, payslips, tax notices, bank statements, rental applications... A common habit is to drop them into an online PDF tool or an AI assistant to add a watermark or hide some information. That means handing your most private data to a server you don't control.

This project does the job **100% locally**, with a dead-simple interface.

## Features (planned)

- 🖋️ **Watermark** every page with a custom text (e.g. *"Only for rental application – Agency X – 2026-11-06"*)
- 🎚️ Adjustable opacity, size, angle and repetition (tiled watermark)
- 🔒 **Flatten** the output so the watermark can't be easily removed
- 🔑 Optional **password protection** of the resulting PDF
- 🧹 Strip metadata (author, software, creation date...)
- 📂 Drag & drop one or several PDFs, get protected copies next to the originals
- ✈️ Works fully **offline** — no network calls, no telemetry

## How it works

1. Open the app
2. Drop your PDF(s)
3. Type the watermark text (who it's for, why, and when)
4. Click **Protect**
5. Get `yourfile_protected.pdf` in the same folder

The original file is never modified.

## Tech stack (planned)

- **Python 3** with [`pypdf`](https://github.com/py-pdf/pypdf) and [`reportlab`](https://www.reportlab.com/) for PDF processing
- A minimal local GUI (Tkinter) and a CLI for power users
- No external API, no account, no internet connection required

## Quick start (coming soon)

```bash
git clone https://github.com/sschuttNat/local-watermark-sensitive-pdf.git
cd local-watermark-sensitive-pdf
pip install -r requirements.txt

# GUI
python app.py

# CLI
python protect.py my_id_card.pdf --text "For Agency X only - 2026-11-06"
```

## Privacy principles

- Files are processed in memory on your machine only
- Nothing is sent anywhere — you can verify it by running the app with your network disabled
- Open source, so anyone can audit the code

## Roadmap

- [ ] CLI watermarking
- [ ] Simple GUI with drag & drop
- [ ] Rasterize option (convert pages to images to make the watermark non-removable)
- [ ] Manual redaction (black boxes over selected areas)
- [ ] Packaged executables for macOS, Windows and Linux

## Contributing

Ideas, issues and pull requests are welcome. Keep it simple: the goal is a small tool anyone can use and trust.

## License

[MIT](LICENSE)
